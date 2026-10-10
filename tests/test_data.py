import pandas as pd

from occupancy.data import resample_occupancy


def test_resampling_marks_short_carried_gaps() -> None:
    timestamps = pd.to_datetime(["2024-05-01 08:02:00+10:00", "2024-05-01 08:31:00+10:00"])
    events = pd.DataFrame(
        {
            "timestamp": timestamps,
            "headcount": [3, 1],
            "deviceid": ["device", "device"],
            "occupancystatus": ["CurrentlyOccupied", "CurrentlyOccupied"],
        }
    )

    output = resample_occupancy(events, frequency="15min", max_carry="30min")

    assert output.loc[timestamps[0].floor("15min"), "headcount"] == 3
    assert output["forward_filled"].sum() == 1
    assert output.iloc[-1]["headcount"] == 1
