# Test and view the project

Run every command from the repository root in PowerShell.

## 1. Run the automated tests

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results\test-report.html --self-contained-html -q
Start-Process results\test-report.html
```

The command should report `5 passed`. The browser report records each test and its result.

## 2. Recreate the G.25 forecast outputs

```powershell
.\.venv\Scripts\python.exe -m occupancy.pipeline `
  --metadata "C:\Users\elvis\Downloads\Sensor ID and Locations.xlsx" `
  --occupancy-zip "C:\Users\elvis\Downloads\5occupancySensor_MayToDec2024_9MRows.zip" `
  --room G.25 `
  --output-dir data\processed\g25_30min
```

This takes time because it scans the 9-million-row archive. It writes an audit, prepared data, metrics, predictions, and two PNG figures to `data\processed\g25_30min`. Raw and processed data stay out of Git by design.

## 3. Display the outputs

```powershell
Import-Csv data\processed\g25_30min\metrics_validation.csv | Format-Table -AutoSize
Import-Csv data\processed\g25_30min\metrics_final_test.csv | Format-Table -AutoSize
Get-Content data\processed\g25_30min\audit.json
Start-Process data\processed\g25_30min\figures\test_forecast_last_week.png
Start-Process data\processed\g25_30min\figures\test_mae_comparison.png
```

`metrics_validation.csv` selects a model without using final test data. `metrics_final_test.csv` is the untouched final comparison. The forecast plot shows observed and selected-model headcounts for the final week; the MAE plot compares all methods.

## 4. Recreate the horizon sensitivity study

```powershell
.\.venv\Scripts\python.exe -m occupancy.sensitivity `
  --occupancy data\processed\g25_30min\occupancy_resampled.csv `
  --output results\horizon_sensitivity.csv
Import-Csv results\horizon_sensitivity.csv | Format-Table horizon_minutes,period,model,mae_people,rmse_people,bias_people,fit_seconds -AutoSize
```

The command compares 15-, 30-, and 60-minute forecasts under the same chronological split and records both validation and final-test metrics. It uses the saved resampled data, so it does not reopen the large ZIP.

## 5. Regenerate code documentation

```powershell
.\.venv\Scripts\python.exe -m pdoc -o docs\html src\occupancy
Start-Process docs\html\index.html
```

## 6. Repeat from a fresh environment

Follow [RUNBOOK.md](RUNBOOK.md) after cloning the repository. Do not commit the raw archives, processed CSV files, or virtual environment.
