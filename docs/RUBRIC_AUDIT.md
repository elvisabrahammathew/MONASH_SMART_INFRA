# Rubric audit

This audit evaluates the current repository against the MMA3001 project brief. **Met** means that the repository contains evidence. **Partial** means useful work exists but additional evidence is needed. **Outstanding** must be completed before submission.

| Rubric area | Status | Evidence and required action |
| --- | --- | --- |
| Engineering problem, inputs, outputs | Met | The research question, G.25 scope, inputs, output, engineering use and boundaries are stated in `README.md`, the report, and `docs/DATA_DICTIONARY.md`. |
| Repository structure and README | Met | The repository has reusable source, tests, documentation, data-handling rules, MIT licence, runbook, report, presentation and an assessment-ready README. Commit and push the final local changes before submission. |
| Comments, docstrings, HTML documentation | Met | Source modules use docstrings and HTML documentation is generated in `docs/html/`. Regenerate it after every material source-code edit. |
| Validation and engineering credibility | Met | A chronological split, five automated tests, data audit, baseline comparison, final-test metrics and 15/30/60-minute sensitivity study are retained in `results/horizon_sensitivity.csv`. A fresh-clone run remains a final student check. |
| Computational-method justification | Met | Persistence and weekday/time baselines are compared with ridge regression, decision-tree regression and SVR. The report explains method selection before testing and the final-period distribution shift. |
| AI use and reflection | Met, pending personalisation | `docs/AI_USAGE.md` documents assistance and verification. Add a brief personal note only if it would make the record more accurate. Be able to explain the project unaided. |
| Written report | Met | `report/MMA3001_Laboratory_Availability_Report.docx` is a submission-ready draft based on the reproducible results. Check your name, unit requirements and final pagination before upload. |
| Presentation and demonstration | Met | `presentation/MMA3001_Occupancy_Forecasting_Presentation.pptx` and `presentation/DEMO_SCRIPT.md` provide a six-slide, five-minute structure. Rehearse once and open the evidence pages before presenting. |
| Submission administration | User action required | Confirm due dates, book the Week 14 presentation, make the repository accessible, push the final commit, and submit the report plus a zipped repository clone. |

## What must happen before you claim the project is complete

1. Follow `docs/TEST_AND_VIEW.md` once from your own VS Code terminal and inspect the generated figures.
2. Check the report pagination and slide rendering on your own machine before submission.
3. Commit and push the final changes, then complete Moodle and presentation-booking steps.
