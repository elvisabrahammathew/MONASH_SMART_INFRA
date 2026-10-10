import numpy as np
import pandas as pd

from occupancy.features import build_feature_table, chronological_split
from occupancy.models import evaluate_candidates, metrics_frame


def test_candidate_workflow_returns_all_models_and_finite_metrics() -> None:
    """Run the modelling workflow on a small synthetic time series."""
    index = pd.date_range("2024-05-01", periods=120, freq="15min", tz="Australia/Melbourne")
    headcount = 3 + np.sin(np.arange(len(index)) / 4) + (np.arange(len(index)) % 5 == 0)
    occupancy = pd.DataFrame({"headcount": headcount}, index=index)

    table = build_feature_table(occupancy, horizon_steps=2)
    train, validation, _ = chronological_split(table)
    results = evaluate_candidates(train, validation)
    metrics = metrics_frame(results, period="validation")

    assert set(metrics["model"]) == {
        "persistence",
        "weekday_time_baseline",
        "ridge_regression",
        "decision_tree",
        "support_vector_regression",
    }
    assert np.isfinite(metrics[["mae_people", "rmse_people", "bias_people"]].to_numpy()).all()
