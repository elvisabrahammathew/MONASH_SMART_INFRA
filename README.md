# MMA3001 | Room Occupancy Forecasting

This project forecasts sensor-derived headcount for **Building 60, room G.25 (Keenan Lab)**. It evaluates whether recent occupancy history and calendar information can predict headcount 30 minutes ahead for ventilation and HVAC planning.

> The project supports planning only. It does not control HVAC equipment, prove energy savings, or independently validate the occupancy sensor.

## Question and approach

**Question:** Can G.25 headcount be forecast 30 minutes ahead more accurately than simple persistence and weekday/time baselines?

- **Data:** timestamped occupancy events, 1 May–31 December 2024.
- **Preparation:** irregular events aggregated into 15-minute bins; values are carried forward for at most 60 minutes, then left missing.
- **Features:** current and lagged headcount, rolling history, time of day, weekday, and weekend.
- **Models:** persistence, weekday/time baseline, ridge regression, decision tree, and support-vector regression (SVR).
- **Validation:** chronological 60% training / 20% validation / 20% final-test split. No timestamps are shuffled.
- **Environmental data:** excluded because no validated co-located G.25 sensor mapping was supplied.

## Results

Ridge regression was selected from validation MAE (**1.080 people**) before the final test. On the untouched 30-minute final test period, persistence had the best MAE (**0.461 people**), while SVR had the lowest RMSE (**0.794 people**).

| Forecast horizon | Best final-test MAE | Model |
| --- | ---: | --- |
| 15 minutes | 0.407 people | Persistence |
| 30 minutes | 0.461 people | Persistence |
| 60 minutes | 0.547 people | Persistence |

Error rises with forecast horizon. The final test period was more stable than development periods, so the simple persistence baseline generalised better than the validation-selected ridge model. This is reported as a result, not hidden.

View the [full results and figures](results/FINAL_RESULTS.md), [sensitivity CSV](results/horizon_sensitivity.csv), and [data audit](docs/DATA_AUDIT.md).

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

The latest run has **5 passing tests**. They verify resampling, target alignment, chronological splits, metric calculations, and a synthetic end-to-end workflow.

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

The results measure agreement with later **sensor-derived** observations, not independently observed occupancy. The analysis covers one room and contains a maximum source-data outage of 21.6 hours. Raw and processed data are excluded from Git because redistribution permission has not been confirmed.

## Submission artifacts

- [Written report](report/MMA3001_Occupancy_Forecasting_Report.docx)
- [Final presentation deck](presentation/MMA3001_Occupancy_Forecasting_Presentation_FINAL.pptx)
- [Presentation script](presentation/DEMO_SCRIPT.md)
- [HTML code documentation](docs/html/index.html)
- [Final submission checklist](SUBMISSION_CHECKLIST.md)
- [AI-use disclosure](docs/AI_USAGE.md)

Project code is released under the [MIT License](LICENSE). Dataset permissions are separate.
