import numpy as np
import pandas as pd

from occupancy.features import TARGET, build_feature_table, chronological_split


def _occupancy_frame() -> pd.DataFrame:
    index = pd.date_range("2024-05-01 08:00", periods=80, freq="15min", tz="Australia/Melbourne")
    return pd.DataFrame({"headcount": np.arange(len(index), dtype=float)}, index=index)


def test_future_target_is_aligned_and_not_a_predictor() -> None:
    table = build_feature_table(_occupancy_frame(), horizon_steps=2, lags=(1, 2))

    first_time = table.index[0]
    assert table.loc[first_time, TARGET] == 2.0
    assert table.loc[first_time, "occupancy_now"] == 0.0
    assert TARGET not in [column for column in table.columns if column != TARGET]


def test_chronological_split_preserves_time_order() -> None:
    train, validation, test = chronological_split(build_feature_table(_occupancy_frame(), horizon_steps=1))

    assert train.index.max() < validation.index.min() < test.index.min()
    assert len(train) + len(validation) + len(test) == 79
