# Final submission checklist

## Include in Git and the ZIP

- [ ] `README.md`, `requirements.txt`, `pyproject.toml`, and `LICENSE`
- [ ] `src/` and `tests/`
- [ ] `docs/`, including `docs/html/`, `docs/TEST_AND_VIEW.md`, and `docs/AI_USAGE.md`
- [ ] `results/test-report.html`, `results/horizon_sensitivity.csv`, availability metric CSVs, and submission figures
- [ ] `report/MMA3001_Laboratory_Availability_Report.docx`
- [ ] `presentation/MMA3001_Laboratory_Availability_Presentation_FINAL.pptx` and `presentation/DEMO_SCRIPT.md`

## Exclude from Git and the ZIP

- [ ] `.venv/`, `.pip-tmp/`, `.pytest_cache/`, and `.ppt-build/`
- [ ] `data/raw/` and `data/processed/` unless the teaching team explicitly authorises redistribution
- [ ] `report/rendered/`, `*.pptx.inspect.ndjson`, and Office temporary files beginning with `~$`
- [ ] Superseded presentation drafts

## Final verification

```powershell
.\.venv\Scripts\python.exe -m pytest --html=results\test-report.html --self-contained-html -q
git status
git add .
git commit -m "Prepare final MMA3001 submission"
git push origin main
```

Review `git status` before committing. It must not list raw data, virtual environments, caches, Office temporary files, or superseded drafts.

## Submit

1. Open the report in Word and check page count, name, references, tables, and figures.
2. Open the final presentation deck and rehearse it with a five-minute timer.
3. Confirm the GitHub repository is accessible to the assessor.
4. Create a ZIP from the committed repository, excluding ignored files.
5. Upload the report, repository URL, and required ZIP to Moodle; complete the Week 14 presentation booking.
