# Final results: G.25 laboratory availability forecasting

This page is the presentation-ready interpretation of the reproducible metric files. A laboratory is considered available when sensor-derived headcount is 0.5 people or below. This does **not** establish confirmed booking availability or independent accuracy of the sensor.

## Main 30-minute forecast result

The model was selected using validation data only. Ridge regression had the lowest validation MAE (1.080 people), so it was the selected regression model before final testing.

| Final-test model | MAE (people) | RMSE (people) | Bias (people) | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Persistence | **0.461** | 0.944 | 0.009 | Lowest typical absolute error |
| Support-vector regression | 0.507 | **0.794** | 0.047 | Lowest large-error-weighted score |
| Ridge regression | 0.579 | 0.837 | 0.272 | Selected on validation; overpredicts on test |
| Decision tree | 0.591 | 0.911 | 0.225 | Similar MAE to ridge |
| Weekday/time baseline | 1.168 | 1.589 | 0.969 | Does not generalise well to the final period |

**Accurate conclusion:** Ridge was selected fairly from validation, but persistence had the best final-test MAE. Do not claim that ridge is the best overall model. The final-period behaviour appears more stable than the development periods, making the current headcount a strong forecast.

## Availability signal from the selected model

The validation-selected ridge forecast was converted into an availability signal using the 0.5-person threshold.

| Measure | Final-test value |
| --- | ---: |
| Availability accuracy | 64.6% |
| Availability precision | 88.1% |
| Availability recall | 53.8% |
| Availability F1 score | 66.8% |
| Final-test issue times | 3,968 |

The high precision means that when the model says the lab is available, it is usually also sensor-recorded as available. The lower recall means it misses some genuinely available periods. This is appropriate for a cautious room-readiness indicator, but it is not sufficient to promise a room to a user without a booking-system or access-control check.

## Forecast-horizon sensitivity

| Horizon | Validation-selected model | Best final-test MAE model | Best final-test MAE (people) |
| --- | --- | --- | ---: |
| 15 minutes | Ridge regression | Persistence | **0.407** |
| 30 minutes | Ridge regression | Persistence | **0.461** |
| 60 minutes | Ridge regression | Persistence | **0.547** |

The result is technically plausible: uncertainty increases as the forecast horizon increases. The 15-minute persistence forecast is the strongest tested practical baseline for this room and period.

## Figures

![Observed versus selected-ridge forecast for the final test week](figures/g25_30min_forecast_last_week.png)

![Final-test MAE comparison for the 30-minute horizon](figures/g25_30min_mae_comparison.png)

## How to check the result yourself

1. Inspect `metrics_validation.csv` first. It must select the model without using the final test period.
2. Inspect `metrics_final_test.csv` second. It must show the final comparison once, without choosing a new winner afterwards.
3. Confirm the time split in `audit.json` and that the pipeline uses only historical features.
4. Run the five automated tests. These verify the software logic, not whether the sensor is independently correct.
5. Report the limitations: one room, no manual ground truth, a 21.6-hour outage, no booking-system integration, and no validated environmental-sensor mapping.
