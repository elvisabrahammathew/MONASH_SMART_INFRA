import numpy as np

from occupancy.models import regression_metrics


def test_regression_metrics_match_hand_calculation() -> None:
    metrics = regression_metrics(np.array([0.0, 2.0]), np.array([1.0, 2.0]))

    assert metrics["mae_people"] == 0.5
    assert metrics["rmse_people"] == np.sqrt(0.5)
    assert metrics["bias_people"] == 0.5
