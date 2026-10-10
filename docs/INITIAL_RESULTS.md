# Initial G.25 forecasting results

This is an initial, reproducible modelling run. It is evidence for method selection and limitations, not a claim that the occupancy sensor has been independently validated.

## Experiment definition

- **Space:** Building 60, room G.25 (Keenan Lab), mapped to floor-space ID `227f1068-9e41-469f-bef0-275f27a0bdba`.
- **Source period:** 1 May-31 December 2024, Melbourne local time.
- **Input interval:** 15 minutes.
- **Forecast target:** headcount 30 minutes after the forecast issue time.
- **Predictors:** current and lagged headcount, rolling history, time of day, weekday, and weekend flag.
- **Excluded predictors:** environmental measurements, because the supplied metadata does not establish a co-located environmental sensor for G.25.
- **Split:** chronological 60% training, 20% validation, 20% final test; no timestamps were shuffled.

## Data quality

| Measure | Value |
| --- | ---: |
| Raw occupancy events | 643,290 |
| Resampled 15-minute bins | 23,516 |
| Feature rows eligible for a forecast | 19,838 |
| Raw headcount range | 0 to 35 people |
| Median gap between source events | 4 seconds |
| Largest gap between source events | 77,778 seconds (21.6 hours) |
| Bins still missing after the 60-minute carry rule | 3,146 |
| Bins forward-filled under the carry rule | 3,780 |

The pipeline does not turn a long sensor outage into zero people. It leaves the value missing and excludes that time as a forecast issue point. This protects the evaluation from falsely treating absent data as an empty room.

## Validation results used for model selection

| Model | MAE (people) | RMSE (people) | Bias (people) | Fit time (s) |
| --- | ---: | ---: | ---: | ---: |
| Ridge regression | 1.080 | 1.966 | -0.158 | 0.039 |
| Support-vector regression | 1.131 | 2.102 | -0.376 | 13.090 |
| Decision-tree regression | 1.146 | 2.083 | -0.182 | 0.083 |
| Persistence | 1.152 | 2.313 | 0.005 | 0.000 |
| Weekday/time baseline | 1.452 | 2.528 | -0.565 | 0.014 |

Ridge regression was selected before examining the test period because it had the lowest validation MAE. This is the model to report as the selected method for this configuration.

## Final-test comparison

| Model | MAE (people) | RMSE (people) | Bias (people) | Fit time (s) |
| --- | ---: | ---: | ---: | ---: |
| Persistence | 0.461 | 0.944 | 0.009 | 0.000 |
| Support-vector regression | 0.507 | 0.794 | 0.047 | 21.889 |
| Ridge regression | 0.579 | 0.837 | 0.272 | 0.035 |
| Decision-tree regression | 0.591 | 0.911 | 0.225 | 0.097 |
| Weekday/time baseline | 1.155 | 1.581 | 0.967 | 0.007 |

Persistence unexpectedly has the lowest final-test MAE, while support-vector regression has the lowest final-test RMSE. This is a meaningful result: the occupancy pattern in the final period differs from development periods, and the selected ridge model tends to overpredict by 0.261 people. Do not change the selected model after seeing the test results. Instead, report this as a limitation and investigate the time-series plot and error distribution.

## Required follow-up analysis

1. Run the documented pipeline for 15-, 30-, and 60-minute horizons; select each model only from its validation period.
2. Compare final-test MAE, RMSE, bias, and runtime across these horizons.
3. Inspect errors during arrivals, departures, and the period around the 21.6-hour outage.
4. Plot headcount by weekday and time-of-day to explain the poor generalisation of the weekday/time baseline.
5. Ask the teaching team for a corrected occupancy-to-environment sensor mapping before adding environmental measurements.
6. Keep a dated experiment log recording each configuration, result, and decision.
