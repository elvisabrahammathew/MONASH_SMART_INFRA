"""Read and validate the supplied sensor-location workbook."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _normalise_identifier(value: object) -> str | None:
    """Return an identifier as text without Excel's trailing `.0` artifact."""
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text[:-2] if text.endswith(".0") else text


def load_sensor_metadata(workbook: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load environmental and occupancy mappings from the supplied workbook.

    Args:
        workbook: Path to ``Sensor ID and Locations.xlsx``.

    Returns:
        A pair: environmental-sensor metadata and occupancy-space metadata.

    Raises:
        ValueError: If the workbook does not contain the expected two sheets.
    """
    sheets = pd.read_excel(workbook, sheet_name=None, dtype=object)
    if len(sheets) < 2:
        raise ValueError("Expected environmental and occupancy mapping sheets.")

    environmental = next(
        (frame.copy() for name, frame in sheets.items() if name.strip().upper().startswith("ENV")),
        None,
    )
    occupancy = next(
        (frame.copy() for name, frame in sheets.items() if name.strip().upper().startswith("OCC")),
        None,
    )
    if environmental is None or occupancy is None:
        raise ValueError("Could not identify ENV and OCC sheets in metadata workbook.")

    environmental.columns = [str(column).strip().lower() for column in environmental.columns]
    occupancy.columns = [str(column).strip().lower() for column in occupancy.columns]
    environmental["sensorid"] = environmental["id"].map(_normalise_identifier)
    occupancy["floorspaceid"] = occupancy["spaceid"].map(_normalise_identifier)
    occupancy["room"] = occupancy["floor/room"].astype("string")
    return environmental, occupancy


def resolve_room(occupancy_metadata: pd.DataFrame, room: str) -> pd.Series:
    """Resolve one unique room label to its occupancy ``floorspaceid``.

    Args:
        occupancy_metadata: Data frame returned by :func:`load_sensor_metadata`.
        room: Room label such as ``G.25``.

    Returns:
        Metadata row for the requested room.

    Raises:
        ValueError: If the room is absent or maps to more than one occupancy space.
    """
    matches = occupancy_metadata.loc[
        occupancy_metadata["room"].str.casefold().eq(room.casefold()),
    ].dropna(subset=["floorspaceid"])
    unique = matches.drop_duplicates("floorspaceid")
    if unique.empty:
        raise ValueError(f"No occupancy mapping exists for room {room!r}.")
    if len(unique) != 1:
        choices = ", ".join(unique["floorspaceid"].astype(str))
        raise ValueError(
            f"Room {room!r} maps to multiple occupancy spaces ({choices}). "
            "Select a floorspace ID explicitly."
        )
    return unique.iloc[0]


def metadata_summary(workbook: str | Path) -> pd.DataFrame:
    """Return a concise mapping table suitable for a data-audit report."""
    environmental, occupancy = load_sensor_metadata(workbook)
    return pd.DataFrame(
        {
            "mapping": ["environmental sensors", "occupancy spaces"],
            "rows": [len(environmental), len(occupancy)],
            "unique_identifiers": [
                environmental["sensorid"].nunique(dropna=True),
                occupancy["floorspaceid"].nunique(dropna=True),
            ],
        }
    )
