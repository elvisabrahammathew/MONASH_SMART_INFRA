"""Reproduce the forecast-horizon sensitivity study from saved occupancy data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .features import build_feature_table, chronological_split
from .models import evaluate_candidates, metrics_frame


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare occupancy forecast horizons without rereading raw archives.")
    parser.add_argument("--occupancy", type=Path, required=True, help="CSV created by occupancy.pipeline")
    parser.add_argument("--output", type=Path, required=True, help="Destination CSV for all metrics")
    parser.add_argument("--horizons", type=int, nargs="+", default=[15, 30, 60], help="Forecast horizons in minutes")
    parser.add_argument("--frequency-minutes", type=int, default=15, help="Sampling period of the saved CSV")
    return parser.parse_args()


def main() -> None:
    """Evaluate all candidate models for each requested forecast horizon."""
    args = _arguments()
    occupancy = pd.read_csv(args.occupancy, index_col="timestamp")
    # CSV offsets differ across daylight-saving boundaries. Parse them on a
    # shared UTC timeline, then return to Melbourne time for calendar features.
    occupancy.index = pd.to_datetime(occupancy.index, utc=True).tz_convert("Australia/Melbourne")
    rows: list[pd.DataFrame] = []
    for horizon in args.horizons:
        if horizon < args.frequency_minutes or horizon % args.frequency_minutes:
            raise ValueError("Every horizon must be a positive multiple of frequency-minutes.")
        features = build_feature_table(occupancy, horizon_steps=horizon // args.frequency_minutes)
        train, validation, test = chronological_split(features)
        validation_metrics = metrics_frame(evaluate_candidates(train, validation), period="validation")
        selected = validation_metrics.iloc[0]["model"]
        final_metrics = metrics_frame(evaluate_candidates(pd.concat([train, validation]), test), period="final_test")
        for metrics in (validation_metrics, final_metrics):
            metrics.insert(0, "horizon_minutes", horizon)
            metrics["selected_by_validation"] = selected
            metrics["feature_rows"] = len(features)
            rows.append(metrics)
    result = pd.concat(rows, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(result.to_string(index=False))
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()
