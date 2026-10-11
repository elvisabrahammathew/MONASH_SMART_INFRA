import numpy as np

from occupancy.models import availability_metrics, regression_metrics


def test_regression_metrics_match_hand_calculation() -> None:
    metrics = regression_metrics(np.array([0.0, 2.0]), np.array([1.0, 2.0]))

    assert metrics["mae_people"] == 0.5
    assert metrics["rmse_people"] == np.sqrt(0.5)
    assert metrics["bias_people"] == 0.5


def test_availability_metrics_use_explicit_vacancy_threshold() -> None:
    """A forecast at or below 0.5 people is interpreted as available."""
    metrics = availability_metrics([0, 1, 0, 2], [0.4, 0.6, 0.8, 1.0], threshold=0.5)

    assert metrics["availability_accuracy"] == 0.75
    assert metrics["availability_precision"] == 1.0
