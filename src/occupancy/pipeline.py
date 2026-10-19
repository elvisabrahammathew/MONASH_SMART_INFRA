"""Command-line pipeline for leakage-safe laboratory-availability forecasting.

Example:
    python -m occupancy.pipeline --metadata "...\\Sensor ID and Locations.xlsx" ^
        --occupancy-zip "...\\5occupancySensor_MayToDec2024_9MRows.zip" ^
        --room G.25 --output-dir data/processed/g25_may_dec_2024
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .data import (
    load_environment_measurements,
    load_occupancy_events,
    occupancy_audit,
    resample_environment,
    resample_occupancy,
)
from .features import TARGET, build_feature_table, chronological_split
from .metadata import load_sensor_metadata, resolve_room
from .models import availability_metrics, availability_metrics_frame, evaluate_candidates, metrics_frame, threshold_sensitivity_frame


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forecast a laboratory's near-term availability from sensor observations.")
    parser.add_argument("--metadata", type=Path, required=True, help="Path to Sensor ID and Locations.xlsx")
    parser.add_argument("--occupancy-zip", type=Path, required=True, help="Path to the occupancy ZIP archive")
    parser.add_argument("--room", default="G.25", help="Mapped room label; default: G.25 (Keenan Lab)")
    parser.add_argument("--floorspace-id", help="Use this instead of resolving --room from metadata")
    parser.add_argument("--start", default="2024-05-01", help="Inclusive analysis start in Melbourne time")
    parser.add_argument("--end", default="2024-12-31", help="Inclusive analysis end in Melbourne time")
    parser.add_argument("--frequency", default="15min", help="Regular aggregation interval; default: 15min")
    parser.add_argument("--horizon-minutes", type=int, default=30, help="Forecast horizon; default: 30 minutes")
    parser.add_argument("--max-carry", default="60min", help="Largest sensor outage treated as a held state")
    parser.add_argument("--availability-threshold", type=float, default=0.5, help="Headcount at or below this value means available; default: 0.5")
    parser.add_argument("--environment-zip", type=Path, help="Optional environmental ZIP archive")
    parser.add_argument("--environment-sensor-id", help="Optional environmental sensor in the same room")
    parser.add_argument("--output-dir", type=Path, required=True, help="Local directory for regenerated results")
    return parser.parse_args()


def _json_default(value: object) -> object:
    """Convert common NumPy and pandas values for the JSON audit file."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (pd.Timestamp, pd.Timedelta)):
        return str(value)
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def _write_figure(predictions: pd.DataFrame, metrics: pd.DataFrame, destination: Path) -> None:
    """Create compact figures for the report and README."""
    destination.mkdir(parents=True, exist_ok=True)
    recent = predictions.tail(min(7 * 24 * 4, len(predictions)))
    fig, axis = plt.subplots(figsize=(11, 4.5))
    axis.plot(recent.index, recent["actual"], label="observed headcount", color="#1f2937", linewidth=1.2)
    axis.plot(recent.index, recent["prediction"], label="selected forecast", color="#0f766e", linewidth=1.2)
    axis.set(title="Final test headcount forecasts supporting availability", xlabel="Time", ylabel="People")
    axis.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(destination / "test_forecast_last_week.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8, 4.5))
    ordered = metrics.sort_values("mae_people")
    axis.bar(ordered["model"], ordered["mae_people"], color="#0f766e")
    axis.set(title="Final test MAE by model", xlabel="Model", ylabel="MAE (people)")
    axis.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(destination / "test_mae_comparison.png", dpi=180)
    plt.close(fig)


def _write_availability_figures(metrics: pd.DataFrame, selected: dict[str, float | int], destination: Path) -> None:
    """Create report-ready availability-comparison and confusion-matrix figures."""
    ordered = metrics.sort_values("availability_f1", ascending=True)
    fig, axis = plt.subplots(figsize=(8, 4.5))
    axis.barh(ordered["model"], ordered["availability_f1"], color="#0f766e")
    axis.set(title="Final-test availability F1 by model", xlabel="F1 score", xlim=(0, 1))
    fig.tight_layout()
    fig.savefig(destination / "availability_f1_comparison.png", dpi=180)
    plt.close(fig)

    matrix = np.array(
        [
            [selected["true_unavailable"], selected["false_available"]],
            [selected["false_unavailable"], selected["true_available"]],
        ]
    )
    fig, axis = plt.subplots(figsize=(5.5, 4.5))
    image = axis.imshow(matrix, cmap="YlGnBu")
    axis.set(
        title="Selected-model availability confusion matrix",
        xlabel="Forecast availability",
        ylabel="Observed availability",
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["Unavailable", "Available"],
        yticklabels=["Unavailable", "Available"],
    )
    for row in range(2):
        for column in range(2):
            axis.text(column, row, f"{matrix[row, column]:,}", ha="center", va="center", color="black", fontsize=14, fontweight="bold")
    fig.colorbar(image, ax=axis, label="Forecast issue times")
    fig.tight_layout()
    fig.savefig(destination / "availability_confusion_matrix.png", dpi=180)
    plt.close(fig)


def main() -> None:
    """Extract a selected room, develop models, and save auditable outputs."""
    args = _parse_arguments()
    if bool(args.environment_zip) != bool(args.environment_sensor_id):
        raise ValueError("Provide both --environment-zip and --environment-sensor-id, or neither.")

    environmental_metadata, occupancy_metadata = load_sensor_metadata(args.metadata)
    if args.floorspace_id:
        floorspace_id = args.floorspace_id
        room_description = f"user-selected occupancy space {floorspace_id}"
    else:
        room_record = resolve_room(occupancy_metadata, args.room)
        floorspace_id = str(room_record["floorspaceid"])
        room_description = f"Building {room_record.get('building')}, room {room_record['room']}"

    frequency_delta = pd.Timedelta(args.frequency)
    horizon_delta = pd.Timedelta(minutes=args.horizon_minutes)
    if horizon_delta % frequency_delta:
        raise ValueError("horizon-minutes must be an exact multiple of frequency.")
    horizon_steps = int(horizon_delta / frequency_delta)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = args.output_dir / "figures"

    events = load_occupancy_events(args.occupancy_zip, floorspace_id, start=args.start, end=args.end)
    occupancy = resample_occupancy(events, frequency=args.frequency, max_carry=args.max_carry)
    occupancy.to_csv(args.output_dir / "occupancy_resampled.csv")

    environment = None
    environment_note = "No environmental features used: no validated co-located environmental mapping was supplied."
    if args.environment_zip:
        # The user must provide this only after verifying co-location in metadata.
        measurements = load_environment_measurements(
            args.environment_zip,
            args.environment_sensor_id,
            start=args.start,
            end=args.end,
        )
        measurements.to_csv(args.output_dir / "environment_tidy.csv", index=False)
        environment = resample_environment(measurements, frequency=args.frequency)
        environment_note = f"Environmental features from sensor {args.environment_sensor_id}."

    features = build_feature_table(occupancy, horizon_steps=horizon_steps, environment=environment)
    features.to_csv(args.output_dir / "features.csv")
    train, validation, test = chronological_split(features)

    validation_results = evaluate_candidates(train, validation)
    validation_metrics = metrics_frame(validation_results, period="validation")
    validation_metrics.to_csv(args.output_dir / "metrics_validation.csv", index=False)
    availability_metrics_frame(validation_results, validation[TARGET], period="validation", threshold=args.availability_threshold).to_csv(
        args.output_dir / "availability_metrics_validation.csv", index=False
    )
    selected_name = validation_metrics.iloc[0]["model"]

    development = pd.concat([train, validation])
    test_results = evaluate_candidates(development, test)
    test_metrics = metrics_frame(test_results, period="final_test")
    test_metrics.to_csv(args.output_dir / "metrics_final_test.csv", index=False)
    test_availability = availability_metrics_frame(test_results, test[TARGET], period="final_test", threshold=args.availability_threshold)
    test_availability.to_csv(args.output_dir / "availability_metrics_final_test.csv", index=False)
    selected_result = next(result for result in test_results if result.name == selected_name)
    predictions = pd.DataFrame(
        {
            "actual_headcount": test[TARGET],
            "forecast_headcount": selected_result.prediction,
            "actual_available": test[TARGET] <= args.availability_threshold,
            "forecast_available": selected_result.prediction <= args.availability_threshold,
        },
        index=test.index,
    )
    predictions["availability_correct"] = predictions["actual_available"] == predictions["forecast_available"]
    predictions.index.name = "timestamp"
    predictions.to_csv(args.output_dir / "predictions_final_test.csv")
    figure_predictions = predictions.rename(columns={"actual_headcount": "actual", "forecast_headcount": "prediction"})
    _write_figure(figure_predictions, test_metrics, figure_dir)
    availability = availability_metrics(test[TARGET], selected_result.prediction, threshold=args.availability_threshold)
    availability.update({"selected_model": selected_name, "forecast_horizon_minutes": args.horizon_minutes, "test_rows": int(len(test))})
    with (args.output_dir / "availability_final_test.json").open("w", encoding="utf-8") as file:
        json.dump(availability, file, indent=2, default=_json_default)
    thresholds = pd.concat(
        [
            threshold_sensitivity_frame(validation[TARGET], next(result for result in validation_results if result.name == selected_name).prediction, period="validation"),
            threshold_sensitivity_frame(test[TARGET], selected_result.prediction, period="final_test"),
        ],
        ignore_index=True,
    )
    thresholds.to_csv(args.output_dir / "availability_threshold_sensitivity.csv", index=False)
    _write_availability_figures(test_availability, availability, figure_dir)

    audit = occupancy_audit(events, occupancy)
    audit.update(
        {
            "room": room_description,
            "floorspace_id": floorspace_id,
            "analysis_start": args.start,
            "analysis_end": args.end,
            "frequency": args.frequency,
            "forecast_horizon_minutes": args.horizon_minutes,
            "feature_rows": int(len(features)),
            "train_rows": int(len(train)),
            "validation_rows": int(len(validation)),
            "test_rows": int(len(test)),
            "selected_on_validation": selected_name,
            "availability_threshold_people": args.availability_threshold,
            "environment_note": environment_note,
            "available_environmental_mappings": int(environmental_metadata["sensorid"].nunique(dropna=True)),
        }
    )
    with (args.output_dir / "audit.json").open("w", encoding="utf-8") as file:
        json.dump(audit, file, indent=2, default=_json_default)
    print(f"Completed laboratory-availability forecast for {room_description}.")
    print(f"Selected by validation MAE: {selected_name}")
    print(f"Outputs written to: {args.output_dir}")


if __name__ == "__main__":
    main()
