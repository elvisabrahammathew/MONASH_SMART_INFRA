# Project runbook

## Chosen scope

The project asks:

> Can Building 60, room G.25 (Keenan Lab) availability 30 minutes ahead be inferred from headcount forecasts more reliably than persistence and a weekday/time baseline?

The analysis uses a 15-minute interval and limits the source archive to 1 May–31 December 2024. The target is a non-negative future headcount. A predicted count at or below 0.5 people produces an advisory availability signal; it does not confirm a booking or access decision.

G.25 has a unique mapped occupancy space. Environmental predictors are excluded because the supplied material does not confirm an environmental sensor co-located with G.25.

## Setup

From the repository root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
```

Place the supplied downloads in `data/raw/`; this directory is intentionally ignored by Git.

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

The output folder contains:

- `audit.json`: source-data coverage, gaps, headcount range, and split sizes.
- `metrics_validation.csv`: headcount comparison used to select the regression model.
- `metrics_final_test.csv`: untouched final-test headcount comparison.
- `availability_metrics_validation.csv` and `availability_metrics_final_test.csv`: model-by-model availability metrics at the 0.5-person rule.
- `availability_threshold_sensitivity.csv`: selected-ridge metrics at stated 0.0, 0.5, and 1.0-person rules.
- `predictions_final_test.csv`: final-test forecasts from the validation-selected model.
- `figures/`: forecast, MAE, availability-F1, and confusion-matrix PNG files.

## Horizon sensitivity study

```powershell
.\.venv\Scripts\python.exe -m occupancy.sensitivity `
  --occupancy data/processed/g25_30min/occupancy_resampled.csv `
  --output results/horizon_sensitivity.csv
```

This compares 15-, 30-, and 60-minute horizons under the same chronological split.

## Verification and final checks

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results/test-report.html --self-contained-html -q
.\.venv\Scripts\python.exe -m pdoc -o docs/html src/occupancy
```

The tests should report `6 passed`. Before submission, inspect the figures and `audit.json`, confirm raw data remain untracked, and make claims only about agreement with later sensor-derived observations.

## Course-method connection

The project uses version control, documentation, testing, data-quality checks, chronological validation, regression, baseline comparison, model evaluation, and sensitivity analysis. Interpolation is limited to short internal environmental-data gaps if a verified co-located sensor becomes available; missing occupancy is never treated as zero. ODE and PDE methods are outside the stated forecasting question.
