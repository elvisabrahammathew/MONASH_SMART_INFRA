"""Leakage-safe feature construction and chronological data splits."""

from __future__ import annotations

import numpy as np
import pandas as pd


TARGET = "target_headcount"


def build_feature_table(
    occupancy: pd.DataFrame,
    *,
    horizon_steps: int,
    lags: tuple[int, ...] = (1, 2, 4, 8),
    environment: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Create predictors that would have been known at each forecast time.

    Args:
        occupancy: Regular time-indexed data frame containing ``headcount``.
        horizon_steps: Number of resampled bins to forecast ahead.
        lags: Previous occupancy bins supplied to the regression models.
        environment: Optional time-indexed environmental measurements. The caller
            must confirm that the sensor is in the same space before supplying it.

    Returns:
        A feature table indexed by forecast issue time. Rows lacking a future
        target are removed; missing predictors remain for model imputation.

    Raises:
        ValueError: If inputs are malformed or use an invalid forecast horizon.
    """
    if horizon_steps < 1:
        raise ValueError("horizon_steps must be at least 1.")
    if "headcount" not in occupancy.columns:
        raise ValueError("occupancy must contain a 'headcount' column.")
    if not isinstance(occupancy.index, pd.DatetimeIndex):
        raise ValueError("occupancy must use a DatetimeIndex.")
    if not occupancy.index.is_monotonic_increasing:
        occupancy = occupancy.sort_index()

    result = pd.DataFrame(index=occupancy.index)
    result["occupancy_now"] = occupancy["headcount"]
    for lag in sorted(set(lags)):
        if lag < 1:
            raise ValueError("All lag values must be positive.")
        result[f"occupancy_lag_{lag}"] = occupancy["headcount"].shift(lag)
    result["occupancy_mean_previous_4"] = occupancy["headcount"].shift(1).rolling(4, min_periods=2).mean()
    result["occupancy_std_previous_4"] = occupancy["headcount"].shift(1).rolling(4, min_periods=2).std()

    minute = occupancy.index.hour * 60 + occupancy.index.minute
    result["hour_sin"] = np.sin(2 * np.pi * minute / (24 * 60))
    result["hour_cos"] = np.cos(2 * np.pi * minute / (24 * 60))
    result["weekday"] = occupancy.index.dayofweek
    result["weekend"] = (occupancy.index.dayofweek >= 5).astype(int)
    result["time_bin"] = (minute // 15).astype(int)

    if environment is not None:
        if not isinstance(environment.index, pd.DatetimeIndex):
            raise ValueError("environment must use a DatetimeIndex.")
        environment = environment.reindex(result.index)
        environment = environment.add_prefix("environment_")
        result = result.join(environment)

    # A negative shift is used only to construct the label. It is never retained
    # as an input feature, preventing the model from seeing future occupancy.
    result[TARGET] = occupancy["headcount"].shift(-horizon_steps)
    # A forecast is only operationally meaningful when the current occupancy
    # measurement is present. Other older predictors may be missing and are
    # imputed inside the fitted model pipeline.
    return result.dropna(subset=[TARGET, "occupancy_now"])


def chronological_split(
    table: pd.DataFrame,
    *,
    train_fraction: float = 0.60,
    validation_fraction: float = 0.20,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split a feature table into contiguous train, validation, and test periods."""
    if not 0 < train_fraction < 1 or not 0 < validation_fraction < 1:
        raise ValueError("Split fractions must lie between zero and one.")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("train_fraction + validation_fraction must be less than one.")
    if len(table) < 30:
        raise ValueError("At least 30 feature rows are required for a three-way split.")
    table = table.sort_index()
    train_end = int(len(table) * train_fraction)
    validation_end = int(len(table) * (train_fraction + validation_fraction))
    return table.iloc[:train_end].copy(), table.iloc[train_end:validation_end].copy(), table.iloc[validation_end:].copy()


def predictor_columns(table: pd.DataFrame) -> list[str]:
    """Return feature columns while excluding the future target."""
    return [column for column in table.columns if column != TARGET]
