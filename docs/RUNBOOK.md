# Project runbook

## Chosen scope

The current project asks:

> Can Building 60, room G.25 (Keenan Lab) availability 30 minutes ahead be inferred from headcount forecasts more reliably than persistence and a weekday/time baseline?

The project uses a 15-minute analysis interval and restricts the supplied extract to 1 May-31 December 2024. The source archive names this period, but the raw records contain dates outside it, so the code filters the date range explicitly.

This is a regression problem with an operational availability output. The target is a non-negative person count; a predicted count at or below 0.5 means available. The signal supports ad hoc room booking and study-space allocation; it is not a confirmed booking or access-control decision.

## Why this scope

The occupancy workbook maps only two spaces that occur in the supplied occupancy archive: G.20 and G.25. G.25 is identified in the workbook as the Keenan Lab and has a single mapped occupancy space. It is therefore a reproducible starting point.

The supplied environmental archive cannot yet be joined to G.25 responsibly. Its available sensor IDs do not provide a confirmed co-located mapping to the G.25 occupancy space. Do not add environmental predictors until the teaching team provides a verified mapping. This limitation belongs in the report.

The project does not claim that the occupancy sensor is LiDAR. The supplied extracts identify occupancy records and devices but do not document sensing technology or independent ground truth.

## Setup

From the repository root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
```

Place the three provided downloads in `data/raw/`. They are excluded from Git because the occupancy archive is large and its sharing conditions have not been confirmed.

```text
data/raw/
|- 5occupancySensor_MayToDec2024_9MRows.zip
|- 5EnvSensor_MayToDec2024_180kRows.zip
`- Sensor ID and Locations.xlsx
```

## Run the main experiment

```powershell
.\.venv\Scripts\python.exe -m occupancy.pipeline `
  --metadata "data/raw/Sensor ID and Locations.xlsx" `
  --occupancy-zip "data/raw/5occupancySensor_MayToDec2024_9MRows.zip" `
  --room G.25 `
  --start 2024-05-01 `
  --end 2024-12-31 `
  --frequency 15min `
  --horizon-minutes 30 `
  --output-dir data/processed/g25_30min
```

This creates:

- `audit.json`: data coverage, gaps, headcount range, status counts, and split sizes.
- `occupancy_resampled.csv`: the 15-minute source series and data-quality flags.
- `features.csv`: model inputs and the future target.
- `metrics_validation.csv`: development comparison used to choose the model.
- `metrics_final_test.csv`: untouched final test comparison.
- `predictions_final_test.csv`: predictions for the selected model.
- `figures/`: final-test forecast and MAE comparison plots.

## Sensitivity study

Run the pipeline twice more, changing only `--horizon-minutes` to `15` and `60`, and use separate output folders such as `data/processed/g25_15min` and `data/processed/g25_60min`.

Compare the final-test MAE, RMSE, bias, fit time, and prediction time. This produces evidence for the forecast-horizon trade-off rather than assuming that a horizon is appropriate.

## Verification, documentation, and final checks

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results/test-report.html --self-contained-html
.\.venv\Scripts\python.exe -m pdoc -o docs/html src/occupancy
```

Before submission, delete no data automatically. Confirm the raw files are ignored, run the pipeline from a clean clone using only this runbook, and inspect `audit.json` before making performance claims.

## Course-method connection

The project uses the parts of the unit that fit its question:

- Week 1: version control, code documentation, testing, validation, and AI disclosure.
- Week 2: timing, runtime comparison, numerical/data-quality errors, and sensitivity analysis.
- Week 3: interpolation is used only for short internal environmental-data gaps if a verified co-located sensor becomes available; missing occupancy is never interpolated as a person count.
- Week 5: ridge regression, decision-tree regression, support-vector regression, regression performance evaluation, and model selection.

Newton-Cotes integration, ODEs, and PDEs are not included because they do not answer the stated occupancy-forecasting question. Forcing them into the method would weaken the technical justification.
