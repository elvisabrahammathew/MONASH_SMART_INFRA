# Final submission checklist

## Include in Git and the ZIP

- [ ] `README.md`, `requirements.txt`, `pyproject.toml`, and `LICENSE`
- [ ] `src/` and `tests/`
- [ ] `docs/`, including `docs/html/` and `docs/TEST_AND_VIEW.md`
- [ ] `results/test-report.html` and `results/horizon_sensitivity.csv`
- [ ] `report/MMA3001_Occupancy_Forecasting_Report.docx`
- [ ] `presentation/MMA3001_Occupancy_Forecasting_Presentation.pptx` and `presentation/DEMO_SCRIPT.md`
- [ ] `scripts/build_report.py` (the report builder)

## Exclude from Git and the ZIP

- [ ] `.venv/`, `.pip-tmp/`, `.pytest_cache/`, and `.ppt-build/`
- [ ] `data/raw/` and `data/processed/` unless the teaching team has explicitly authorised data redistribution
- [ ] `report/rendered/` and `*.pptx.inspect.ndjson` (local build checks)

## Final verification

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results\test-report.html --self-contained-html -q
git add .
git status
git commit -m "Prepare final MMA3001 submission"
git push origin main
```

Review `git status` before committing. It should not list raw data or local virtual-environment/cache folders.

## Submit

1. Open the report in Word and check the pagination, name, and references.
2. Open the presentation in PowerPoint and rehearse with a five-minute timer.
3. Confirm the GitHub repository is accessible to the assessor.
4. Create a ZIP from the committed repository folder, excluding ignored files.
5. Upload the report, repository URL, and required ZIP to Moodle; complete the Week 14 presentation booking.
