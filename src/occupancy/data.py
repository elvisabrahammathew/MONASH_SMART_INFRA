"""Extraction and time-alignment routines for supplied sensor archives."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


TIMEZONE = "Australia/Melbourne"


def _csv_member(archive: zipfile.ZipFile) -> str:
    """Return the only CSV member in a source ZIP archive."""
    members = [item.filename for item in archive.infolist() if item.filename.lower().endswith(".csv")]
    if len(members) != 1:
        raise ValueError(f"Expected exactly one CSV file in archive; found {members!r}.")
    return members[0]


def _to_local_time(values: pd.Series) -> pd.Series:
    """Parse source timestamps and convert them to Melbourne local time."""
    return pd.to_datetime(values, errors="coerce", utc=True).dt.tz_convert(TIMEZONE)


def _bound(value: str | None, *, is_end: bool) -> pd.Timestamp | None:
    """Convert a command-line date to an inclusive local timestamp bound."""
    if value is None:
        return None
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize(TIMEZONE)
    else:
        timestamp = timestamp.tz_convert(TIMEZONE)
    if is_end and len(value) == 10:
        timestamp += pd.Timedelta(days=1) - pd.Timedelta(nanoseconds=1)
    return timestamp


def load_occupancy_events(
    archive_path: str | Path,
    floorspace_id: str,
    *,
    start: str | None = None,
    end: str | None = None,
    chunksize: int = 250_000,
) -> pd.DataFrame:
    """Read only one occupancy space from the large, zipped event file.

    The source provides state observations rather than evenly spaced samples. The
    returned table retains every event; resampling occurs separately.
    """
    columns = ["id", "deviceid", "floorspaceid", "occupancystatus", "headcount", "collecteddate"]
    pieces: list[pd.DataFrame] = []
    start_at, end_at = _bound(start, is_end=False), _bound(end, is_end=True)
    with zipfile.ZipFile(archive_path) as archive:
        with archive.open(_csv_member(archive)) as csv_file:
            for chunk in pd.read_csv(
                csv_file,
                usecols=columns,
                dtype={"deviceid": "string", "floorspaceid": "string", "occupancystatus": "string"},
                chunksize=chunksize,
            ):
                selected = chunk.loc[chunk["floorspaceid"].eq(str(floorspace_id))].copy()
                if selected.empty:
                    continue
                selected["timestamp"] = _to_local_time(selected["collecteddate"])
                selected["headcount"] = pd.to_numeric(selected["headcount"], errors="coerce")
                selected = selected.dropna(subset=["timestamp", "headcount"])
                if start_at is not None:
                    selected = selected.loc[selected["timestamp"] >= start_at]
                if end_at is not None:
                    selected = selected.loc[selected["timestamp"] <= end_at]
                if not selected.empty:
                    pieces.append(selected)
    if not pieces:
        raise ValueError(
            "No occupancy events matched the requested floorspace and date range. "
            "Check the ID, archive, and dates."
        )
    events = pd.concat(pieces, ignore_index=True).sort_values(["timestamp", "id"])
    return events.drop_duplicates(["timestamp", "deviceid"], keep="last").reset_index(drop=True)


def resample_occupancy(
    events: pd.DataFrame,
    *,
    frequency: str = "15min",
    max_carry: str = "60min",
) -> pd.DataFrame:
    """Convert irregular occupancy events to a regular, quality-flagged series.

    A bin receives its last observed headcount. Brief gaps are forward-filled as
    the last known sensor state, while longer gaps remain missing rather than
    being silently treated as an empty room.
    """
    if events.empty:
        raise ValueError("Cannot resample an empty event table.")
    series = events.set_index("timestamp")["headcount"].sort_index()
    observed = series.resample(frequency).last()
    limit = max(1, int(pd.Timedelta(max_carry) / pd.Timedelta(frequency)))
    output = pd.DataFrame({"headcount": observed.ffill(limit=limit)})
    output["observed_in_bin"] = observed.notna()
    output["forward_filled"] = output["headcount"].notna() & ~output["observed_in_bin"]
    output.index.name = "timestamp"
    return output


def occupancy_audit(events: pd.DataFrame, resampled: pd.DataFrame) -> dict[str, object]:
    """Calculate concise data-quality evidence for the project report."""
    gaps = events["timestamp"].sort_values().diff().dropna()
    return {
        "raw_events": int(len(events)),
        "start": str(events["timestamp"].min()),
        "end": str(events["timestamp"].max()),
        "devices": int(events["deviceid"].nunique()),
        "headcount_min": float(events["headcount"].min()),
        "headcount_max": float(events["headcount"].max()),
        "status_counts": events["occupancystatus"].value_counts(dropna=False).to_dict(),
        "median_event_gap_seconds": float(gaps.median().total_seconds()) if not gaps.empty else np.nan,
        "largest_event_gap_seconds": float(gaps.max().total_seconds()) if not gaps.empty else np.nan,
        "resampled_bins": int(len(resampled)),
        "missing_resampled_bins": int(resampled["headcount"].isna().sum()),
        "forward_filled_bins": int(resampled["forward_filled"].sum()),
    }


def load_environment_measurements(
    archive_path: str | Path,
    sensor_id: str,
    *,
    start: str | None = None,
    end: str | None = None,
    variables: Iterable[str] | None = None,
    chunksize: int = 20_000,
) -> pd.DataFrame:
    """Extract a tidy table of measurements from nested environmental JSON.

    This function deliberately removes repeated copies of the same variable-time
    measurement, which occur in the supplied source extract.
    """
    start_at, end_at = _bound(start, is_end=False), _bound(end, is_end=True)
    requested = {name.casefold() for name in variables} if variables else None
    rows: list[dict[str, object]] = []
    with zipfile.ZipFile(archive_path) as archive:
        with archive.open(_csv_member(archive)) as csv_file:
            for chunk in pd.read_csv(csv_file, usecols=["sensorid", "jsondata"], dtype={"sensorid": "string"}, chunksize=chunksize):
                for payload_text in chunk.loc[chunk["sensorid"].eq(str(sensor_id)), "jsondata"].dropna():
                    for item in json.loads(payload_text):
                        variable = item["variable"]
                        name = str(variable["name"])
                        if requested is not None and name.casefold() not in requested:
                            continue
                        for observation in item.get("values", []):
                            timestamp = pd.to_datetime(observation.get("time"), unit="s", utc=True).tz_convert(TIMEZONE)
                            if (start_at is not None and timestamp < start_at) or (end_at is not None and timestamp > end_at):
                                continue
                            rows.append({"timestamp": timestamp, "variable": name, "unit": variable.get("unit"), "value": observation.get("value")})
    measurements = pd.DataFrame(rows)
    if measurements.empty:
        raise ValueError("No environmental measurements matched the requested sensor and date range.")
    measurements["value"] = pd.to_numeric(measurements["value"], errors="coerce")
    return measurements.dropna(subset=["value"]).drop_duplicates(["timestamp", "variable"], keep="last")


def resample_environment(measurements: pd.DataFrame, *, frequency: str = "15min") -> pd.DataFrame:
    """Aggregate measurements to bins and interpolate only short internal gaps."""
    wide = measurements.pivot_table(index="timestamp", columns="variable", values="value", aggfunc="mean")
    return wide.resample(frequency).mean().interpolate(method="time", limit=4, limit_area="inside")
