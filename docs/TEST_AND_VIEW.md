# Test and view the project

Run every command from the repository root in PowerShell.

## 1. Run the automated tests

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results\test-report.html --self-contained-html -q
Start-Process results\test-report.html
```

The command should report `6 passed`. The report records checks for resampling, target alignment, chronological splitting, regression metrics, availability-threshold metrics, and an end-to-end workflow.

## 2. Recreate the G.25 forecast outputs

```powershell
.\.venv\Scripts\python.exe -m occupancy.pipeline `
  --metadata "C:\Users\elvis\Downloads\Sensor ID and Locations.xlsx" `
  --occupancy-zip "C:\Users\elvis\Downloads\5occupancySensor_MayToDec2024_9MRows.zip" `
  --room G.25 `
  --output-dir data\processed\g25_30min
```

The command scans the 9-million-row archive and writes an audit, prepared data, model metrics, predictions, and PNG figures. Raw and processed data stay out of Git by design.

## 3. Display outputs and evaluate them

```powershell
Import-Csv data\processed\g25_30min\metrics_validation.csv | Format-Table -AutoSize
Import-Csv data\processed\g25_30min\metrics_final_test.csv | Format-Table -AutoSize
Import-Csv data\processed\g25_30min\availability_metrics_validation.csv | Format-Table -AutoSize
Import-Csv data\processed\g25_30min\availability_metrics_final_test.csv | Format-Table -AutoSize
Import-Csv data\processed\g25_30min\availability_threshold_sensitivity.csv | Format-Table -AutoSize
Start-Process data\processed\g25_30min\figures\test_forecast_last_week.png
Start-Process data\processed\g25_30min\figures\test_mae_comparison.png
Start-Process data\processed\g25_30min\figures\availability_f1_comparison.png
Start-Process data\processed\g25_30min\figures\availability_confusion_matrix.png
```

`metrics_validation.csv` selects the regression model without using final-test data. `metrics_final_test.csv` gives the final headcount comparison. The availability tables compare every method under the fixed 0.5-person rule. The threshold table shows what changes if “available” is defined differently; it is interpretation, not post-test model selection.

## 4. Recreate the horizon sensitivity study

```powershell
.\.venv\Scripts\python.exe -m occupancy.sensitivity `
  --occupancy data\processed\g25_30min\occupancy_resampled.csv `
  --output results\horizon_sensitivity.csv
Import-Csv results\horizon_sensitivity.csv | Format-Table horizon_minutes,period,model,mae_people,rmse_people,bias_people,fit_seconds -AutoSize
```

## 5. Regenerate code documentation

```powershell
.\.venv\Scripts\python.exe -m pdoc -o docs\html src\occupancy
Start-Process docs\html\index.html
```

## 6. Repeat from a fresh environment

Follow [RUNBOOK.md](RUNBOOK.md) after cloning. Do not commit the raw archives, processed CSV files, or virtual environment.
