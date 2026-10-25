# Submission requirement evidence

This page maps the unit submission requirements to concrete repository evidence.

| Requirement | Evidence in this repository |
| --- | --- |
| Defined engineering problem relevant to mechanical engineering | `README.md` defines a 30-minute laboratory-occupancy forecast as a cautious input to laboratory readiness and demand-responsive ventilation planning. It explicitly excludes HVAC-control, comfort, and energy-saving claims that the data cannot support. |
| Numerical method and/or machine learning method | `src/occupancy/models.py` compares persistence and weekday/time baselines with ridge regression, decision-tree regression, and support-vector regression. |
| Model development | `src/occupancy/data.py`, `features.py`, and `models.py` implement data extraction, 15-minute resampling, feature construction, model fitting, and metric calculation. |
| Validation and verification | Chronological 60/20/20 train/validation/test split in `features.py`; six automated tests in `tests/`; generated test report in `results/test-report.html`; data audit in `docs/DATA_AUDIT.md`. |
| Sensitivity analysis | `src/occupancy/sensitivity.py` and `results/horizon_sensitivity.csv` compare 15-, 30-, and 60-minute horizons. `results/availability_threshold_sensitivity.csv` documents the stated availability-threshold interpretation. |
| Engineering interpretation | `results/FINAL_RESULTS.md` reports model performance, availability metrics, forecast-horizon trade-offs, and the limits of sensor-derived occupancy evidence. |
| Reproducible workflow and version control | Git repository with functional `main` branch, `README.md`, `docs/RUNBOOK.md`, `requirements.txt`, and `pyproject.toml`. Raw data are excluded through `.gitignore`. |
| Computational tools | Python, pandas, NumPy, scikit-learn, matplotlib, pytest, pytest-html, and pdoc are listed in `requirements.txt`. |
| README | `README.md` contains scope, method, results, setup, reproduction, tests, outputs, and limitations. |
| HTML documentation | `docs/html/index.html` is generated from docstrings using pdoc. |
| Licence | `LICENSE` contains the MIT Licence. |
| Functional source code with docstrings and comments | Reusable modules are in `src/occupancy/`; each module and public function has docstrings, with inline comments where reasoning is not obvious. |
| Tests and test report | Four test modules provide six tests; `results/test-report.html` records the latest passing run. |
| AI disclosure | `docs/AI_USAGE.md` states the tool, uses, approximate contribution, verification, decisions, limitations, errors, and learning impact. |

## Final student checks

1. Run the six tests from your own VS Code terminal.
2. Open `results/test-report.html` and `docs/html/index.html`.
3. Confirm GitHub displays the latest `main` branch.
4. Open the Word report and PowerPoint to check pagination, slide rendering, personal details, and final speaking time.
