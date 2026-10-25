# MMA3001 | Smart Laboratory Availability Forecasting

This project forecasts whether **Building 60, room G.25 (Keenan Lab)** will be available 30 minutes ahead. It converts sensor-derived headcount forecasts into a clear available/not-available signal for laboratory readiness and demand-responsive ventilation planning, while also supporting ad hoc laboratory use decisions.

> The project supports planning only. An “available” signal means sensor-derived headcount is 0.5 people or below; it is not a confirmed booking, access-control decision, or independent occupancy audit.

## Question and approach

**Engineering question:** Can G.25 availability 30 minutes ahead be inferred from a headcount forecast more reliably than simple persistence and weekday/time baselines, providing a cautious occupancy input for laboratory readiness and ventilation planning?

- **Data:** timestamped occupancy events, 1 May–31 December 2024.
- **Preparation:** irregular events aggregated into 15-minute bins; values are carried forward for at most 60 minutes, then left missing.
- **Features:** current and lagged headcount, rolling history, time of day, weekday, and weekend.
- **Models:** persistence, weekday/time baseline, ridge regression, decision tree, and support-vector regression (SVR).
- **Validation:** chronological 60% training / 20% validation / 20% final-test split. No timestamps are shuffled.
- **Availability rule:** a future sensor-derived headcount of 0.5 people or below is treated as available.
- **Mechanical-engineering relevance:** occupancy is an input to laboratory readiness and demand-responsive ventilation planning; this project does not claim to model HVAC control, thermal comfort, or energy savings.`r`n- **Environmental data:** excluded because no validated co-located G.25 sensor mapping was supplied.

## Results

Ridge regression was selected from validation MAE (**1.080 people**) before the final test. Its final headcount forecasts are translated into an availability signal. Persistence had the best 30-minute final-test MAE (**0.461 people**), while SVR had the lowest RMSE (**0.794 people**).

| Forecast horizon | Best final-test MAE | Model |
| --- | ---: | --- |
| 15 minutes | 0.407 people | Persistence |
| 30 minutes | 0.461 people | Persistence |
| 60 minutes | 0.547 people | Persistence |

Error rises with forecast horizon. The final test period was more stable than development periods, so the simple persistence baseline generalised better than the validation-selected ridge model. This is reported as a result, not hidden.

View the [full results and figures](results/FINAL_RESULTS.md), [availability model comparison](results/availability_metrics_final_test.csv), [threshold sensitivity](results/availability_threshold_sensitivity.csv), [horizon sensitivity](results/horizon_sensitivity.csv), and [data audit](docs/DATA_AUDIT.md).

## Run and test

Create a virtual environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

Run the automated tests:

```powershell
python -m pytest --html=results\test-report.html --self-contained-html -q
Start-Process results\test-report.html
```

The latest run has **6 passing tests**. They verify resampling, target alignment, chronological splits, regression metrics, availability-threshold metrics, and a synthetic end-to-end workflow.

Recreate the 30-minute forecast outputs from the authorised local raw archives:

```powershell
python -m occupancy.pipeline `
  --metadata "C:\Users\elvis\Downloads\Sensor ID and Locations.xlsx" `
  --occupancy-zip "C:\Users\elvis\Downloads\5occupancySensor_MayToDec2024_9MRows.zip" `
  --room G.25 `
  --output-dir data\processed\g25_30min
```

Open the figures:

```powershell
Start-Process results\figures\g25_30min_forecast_last_week.png
Start-Process results\figures\g25_30min_mae_comparison.png
Start-Process results\figures\availability_f1_comparison.png
Start-Process results\figures\availability_confusion_matrix.png
```

More commands and output explanations are in [docs/TEST_AND_VIEW.md](docs/TEST_AND_VIEW.md) and [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Repository contents

| Path | Contents |
| --- | --- |
| `src/occupancy/` | Extraction, audit, feature, model, pipeline, and sensitivity code |
| `tests/` | Automated tests |
| `results/` | Test report, metric CSV, figures, and interpretation |
| `docs/` | Runbook, data dictionary, audit, AI disclosure, and HTML documentation |
| `report/` | Submission-ready written report |
| `presentation/` | Final slide deck and five-minute demonstration script |

## Important limitations and data handling

The results measure agreement with later **sensor-derived** observations, not confirmed bookings or independently observed occupancy. The analysis covers one room and contains a maximum source-data outage of 21.6 hours. Raw and processed data are excluded from Git because redistribution permission has not been confirmed.

## Submission artifacts

- [Written report](report/MMA3001_Laboratory_Availability_Report.docx)
- [Final presentation deck](presentation/MMA3001_Laboratory_Availability_Presentation_FINAL.pptx)
- [Presentation script](presentation/DEMO_SCRIPT.md)
- [HTML code documentation](docs/html/index.html)
- [Final submission checklist](SUBMISSION_CHECKLIST.md)
- [AI-use disclosure](docs/AI_USAGE.md)

Project code is released under the [MIT License](LICENSE). Dataset permissions are separate.
