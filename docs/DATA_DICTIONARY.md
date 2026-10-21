# Data dictionary

## Analysis scope

| Item | Definition |
| --- | --- |
| Study space | Building 60, room G.25, Keenan Lab |
| Occupancy space ID | `227f1068-9e41-469f-bef0-275f27a0bdba` |
| Analysis period | 1 May-31 December 2024, Australia/Melbourne time |
| Analysis interval | 15 minutes |
| Forecast horizon | 30 minutes (two analysis intervals) |
| Target | `target_headcount`: observed headcount two intervals after the forecast issue time |
| Availability rule | A room is advisory-available when sensor-derived headcount is less than or equal to 0.5 people. This is not a confirmed booking or access-control decision. |

## Raw occupancy archive

| Column | Meaning | Handling |
| --- | --- | --- |
| `id` | Source-record identifier | Used to keep the latest duplicate sensor event. |
| `deviceid` | Occupancy device identifier | Audited; one device occurs for G.25 in the analysed period. |
| `floorspaceid` | Space UUID | Filters the archive to G.25 using the supplied metadata workbook. |
| `occupancystatus` | Status label such as `CurrentlyOccupied`, `RecentlyOccupied`, or `NotOccupied` | Retained for audit counts; headcount is the regression value. |
| `headcount` | Sensor-reported number of people | Parsed as numeric; expected domain is non-negative. |
| `collecteddate` | Event timestamp including source timezone offset | Converted to Australia/Melbourne time. |

## Derived occupancy fields

| Field | Meaning |
| --- | --- |
| `headcount` | Last observed count in each 15-minute bin. Short outages are carried forward for no more than 60 minutes. |
| `observed_in_bin` | `True` when the bin contains a source observation. |
| `forward_filled` | `True` when the count was carried from a prior bin. |
| `occupancy_now` | Headcount known when the forecast is issued. Required for a valid forecast. |
| `occupancy_lag_1`, `occupancy_lag_2`, `occupancy_lag_4`, `occupancy_lag_8` | Earlier headcounts at 15-, 30-, 60-, and 120-minute lags. |
| `occupancy_mean_previous_4`, `occupancy_std_previous_4` | Mean and standard deviation over the four earlier bins. |
| `hour_sin`, `hour_cos` | Cyclic time-of-day representation. |
| `weekday`, `weekend`, `time_bin` | Calendar predictors available when a forecast is issued. |
| `actual_available` | `True` when the observed future sensor-derived headcount is less than or equal to 0.5 people. |
| `forecast_available` | `True` when the selected model's forecast headcount is less than or equal to 0.5 people. |
| `availability_correct` | `True` when `actual_available` and `forecast_available` agree. |
| `true_unavailable`, `false_available`, `false_unavailable`, `true_available` | Counts in the availability confusion matrix, where `false_available` is the safety-relevant case in which the signal says available but the later sensor reading is occupied. |

## Evaluation outputs

| File | Meaning |
| --- | --- |
| `availability_metrics_validation.csv` | Model-by-model availability accuracy, precision, recall, F1, and confusion counts on validation data. |
| `availability_metrics_final_test.csv` | The same comparison on the final chronological test period. |
| `availability_threshold_sensitivity.csv` | Ridge availability metrics at stated thresholds of 0.0, 0.5, and 1.0 people; it does not change the selected model. |

## Invalid and missing-data policy

- A long sensor outage is not converted to zero people.
- Forecast rows without current headcount are excluded, because persistence cannot issue a valid forecast.
- Missing lag or optional environmental features are handled by the training-only median imputer inside each regression pipeline.
- Duplicate source events at the same timestamp and device retain the last source-record ID.
- Negative headcounts or unparseable timestamps require investigation and must be reported if found.

## Environmental archive

The archive contains JSON records for battery voltage, carbon dioxide, humidity, formaldehyde, pressure, temperature, light volatile organic compounds, and particulate matter. These variables are not included in the main G.25 model because the supplied metadata does not provide a confirmed co-located environmental sensor. If a verified mapping is provided, records are deduplicated by variable and timestamp, resampled to 15-minute bins, and only short internal gaps are interpolated.
