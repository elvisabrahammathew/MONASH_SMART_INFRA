"""Baselines, regression models, and metrics for occupancy forecasts."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from .features import TARGET, predictor_columns


def regression_metrics(actual: pd.Series | np.ndarray, predicted: pd.Series | np.ndarray) -> dict[str, float]:
    """Calculate error values in people for one set of forecasts."""
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    return {
        "mae_people": float(mean_absolute_error(actual_array, predicted_array)),
        "rmse_people": float(np.sqrt(mean_squared_error(actual_array, predicted_array))),
        "bias_people": float(np.mean(predicted_array - actual_array)),
        "r2": float(r2_score(actual_array, predicted_array)),
    }


class ScheduleBaseline:
    """Predict the training-set mean for the same weekday and 15-minute bin."""

    def fit(self, features: pd.DataFrame, target: pd.Series) -> "ScheduleBaseline":
        """Fit the time-of-week lookup without using later observations."""
        frame = pd.DataFrame({"weekday": features["weekday"], "time_bin": features["time_bin"], TARGET: target})
        self.group_means = frame.groupby(["weekday", "time_bin"])[TARGET].mean()
        self.global_mean = float(target.mean())
        return self

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        """Return calendar-pattern forecasts, falling back to the global mean."""
        keys = pd.MultiIndex.from_frame(features[["weekday", "time_bin"]])
        values = self.group_means.reindex(keys).to_numpy(dtype=float)
        return np.where(np.isnan(values), self.global_mean, values)


@dataclass
class ModelResult:
    """One evaluated model and the runtime needed to train and predict."""

    name: str
    estimator: object
    metrics: dict[str, float]
    fit_seconds: float
    predict_seconds: float
    prediction: np.ndarray


def candidate_models(random_state: int = 42) -> dict[str, object]:
    """Return regression methods explicitly connected to Week 5 material."""
    preprocessing = [("imputer", SimpleImputer(strategy="median", add_indicator=True)), ("scaler", StandardScaler())]
    return {
        "ridge_regression": Pipeline(preprocessing + [("model", Ridge(alpha=1.0))]),
        "decision_tree": Pipeline(
            [("imputer", SimpleImputer(strategy="median", add_indicator=True)), ("model", DecisionTreeRegressor(max_depth=12, min_samples_leaf=20, random_state=random_state))]
        ),
        "support_vector_regression": Pipeline(preprocessing + [("model", SVR(C=10.0, epsilon=0.2, gamma="scale"))]),
    }


def evaluate_candidates(training: pd.DataFrame, evaluation: pd.DataFrame, *, random_state: int = 42) -> list[ModelResult]:
    """Fit baselines and candidate regressions on one past period, then evaluate later data."""
    columns = predictor_columns(training)
    x_train, y_train = training[columns], training[TARGET]
    x_eval, y_eval = evaluation[columns], evaluation[TARGET]
    results: list[ModelResult] = []

    baselines: dict[str, object] = {
        "persistence": None,
        "weekday_time_baseline": ScheduleBaseline(),
    }
    for name, model in baselines.items():
        start = perf_counter()
        if name == "persistence":
            prediction = x_eval["occupancy_now"].to_numpy(dtype=float)
        else:
            model.fit(x_train, y_train)
            prediction = model.predict(x_eval)
        fit_seconds = perf_counter() - start
        start = perf_counter()
        # The predictions above are already generated; this captures negligible
        # baseline post-processing consistently without fitting on evaluation data.
        prediction = np.asarray(prediction, dtype=float)
        predict_seconds = perf_counter() - start
        results.append(ModelResult(name, model, regression_metrics(y_eval, prediction), fit_seconds, predict_seconds, prediction))

    for name, model in candidate_models(random_state).items():
        start = perf_counter()
        model.fit(x_train, y_train)
        fit_seconds = perf_counter() - start
        start = perf_counter()
        prediction = model.predict(x_eval)
        predict_seconds = perf_counter() - start
        results.append(ModelResult(name, model, regression_metrics(y_eval, prediction), fit_seconds, predict_seconds, prediction))
    return results


def metrics_frame(results: list[ModelResult], *, period: str) -> pd.DataFrame:
    """Convert model results into a report-ready comparison table."""
    rows = []
    for result in results:
        rows.append({"period": period, "model": result.name, **result.metrics, "fit_seconds": result.fit_seconds, "predict_seconds": result.predict_seconds})
    return pd.DataFrame(rows).sort_values("mae_people").reset_index(drop=True)
