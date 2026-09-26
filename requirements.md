# Project Requirements

This checklist separates requirements in the supplied MMA3001 project brief from the proposed implementation plan. Unchecked items have not been verified as complete. This Markdown file is documentation; it is not a pip installation file.

## Assessment requirements

Source: `MMA3001_2026_Project_Brief.pdf`, especially pages 2 and 4-15. Check the Unit Overview Spreadsheet for exact submission dates.

### Problem and scope

- [ ] Define a specific engineering problem relevant to mechanical or aerospace engineering.
- [ ] Explain its importance, intended use, assumptions, scope, and limitations.
- [ ] Obtain teaching-team approval before substantial work if proposing a student-selected project.
- [ ] Apply at least one numerical or machine-learning technique taught in the unit.
- [ ] Specify primary inputs and outputs, including formats, units, domains, and meaning.
- [ ] Document handling of invalid, missing, and unsupported inputs.

### Computational work

- [ ] Implement a functioning, reproducible computational workflow.
- [ ] Explain how the method works, why it was selected, and its parameters and limitations.
- [ ] Compare the selected approach with at least one credible baseline or alternative.
- [ ] Justify the validation design and evaluation metrics.
- [ ] Explain whether validation information influenced model selection.
- [ ] Identify failure modes and what the validation cannot establish.
- [ ] Analyse performance and relevant sensitivity or optimisation questions.
- [ ] Use timing and profiling to support performance analysis; consider arithmetic intensity or FLOPS where appropriate.
- [ ] Compare the baseline/original solution with the selected/improved solution and justify the final design.
- [ ] Interpret findings in the engineering context and explain lessons learned.

### GitHub and documentation

- [ ] Maintain a logical repository structure and meaningful development history.
- [ ] Keep the main branch functional.
- [ ] Provide a README covering purpose, environment, dependencies, data access, and execution.
- [ ] Include a source-code licensing agreement; document dataset permissions separately.
- [ ] Use helpful inline comments and consistent docstrings describing parameters, returns, exceptions, and usage where relevant.
- [ ] Generate HTML source-code documentation that matches the submitted code.
- [ ] Include test functions and a generated test report.
- [ ] Verify reproduction from a fresh clone using the documented instructions.
- [ ] Ensure assessors can access the final repository and necessary authorised data.

### AI reflection

- [ ] Disclose all material AI use, including project planning and documentation assistance.
- [ ] Record tools, purposes, approximate contribution, and reasons for using AI.
- [ ] Explain how generated content was checked and corrected.
- [ ] Identify decisions retained by the student and errors or unhelpful suggestions from AI.
- [ ] Reflect on the effect of AI on understanding and workflow.
- [ ] Be able to explain the work without AI during the presentation and questions.

### Submission

- [ ] Confirm submission dates in the Unit Overview Spreadsheet.
- [ ] Prepare the individual 5-10-page report; references and appendices are excluded from the ten-page limit.
- [ ] Cover the problem, data, methods, validation, results, comparison, optimisation, limitations, lessons, AI reflection, and references.
- [ ] Submit the report through Moodle.
- [ ] Provide an accessible final repository link.
- [ ] Submit a zipped clone of the repository through Moodle.
- [ ] Book and attend the Week 14 presentation appointment.
- [ ] Prepare a five-minute presentation and three-minute question period, including a repository/documentation demonstration and testing evidence.

## Proposed occupancy-project requirements

These are working design choices, not additional requirements imposed by the brief. Revise them when the dataset and research question are confirmed.

- [ ] Confirm whether the data contain LiDAR point clouds, processed person counts, or binary occupancy.
- [ ] Confirm how reference occupancy measurements were produced and checked.
- [ ] Confirm data release, access, ethics conditions, and redistribution permissions.
- [ ] Choose one room and a forecast horizon appropriate to the sampling interval and intended use.
- [ ] Document the data schema, timezone, sampling interval, units, coverage, and missingness.
- [ ] Preserve original data and make cleaning reproducible.
- [ ] Never interpret a missing sensor measurement as zero occupancy without justification.
- [ ] Establish chronological training, validation, and final test periods.
- [ ] Ensure training target timestamps do not cross into validation or test periods.
- [ ] Fit learned preprocessing only on training data and use only information available at forecast time.
- [ ] Compare persistence and training-derived weekday/time baselines with the main model.
- [ ] For count prediction, report MAE, RMSE, signed bias, and runtime; revise metrics if the task becomes classification.
- [ ] Inspect errors during occupied periods, arrivals/departures, and outages.
- [ ] Test input validation, feature/target alignment, split boundaries, hand-calculated metrics, and the end-to-end workflow.
- [ ] Run a manageable sensitivity study of forecast horizon, features, missing inputs, or model settings.
- [ ] Distinguish prediction agreement with sensor labels from independent validation of sensor accuracy.
- [ ] Avoid claiming building-wide generalisation or energy savings without supporting evidence.

## Planned software dependencies

These packages are proposed for implementation. They have not yet been installed or verified for this repository.

| Package | Purpose |
| --- | --- |
| numpy | Numerical arrays and calculations |
| pandas | Tabular sensor data and timestamp processing |
| matplotlib | Analysis and report figures |
| scikit-learn | Baselines, regression, preprocessing, and metrics |
| jupyter | Exploratory notebooks |
| pytest | Automated tests |
| pytest-html | HTML test reports |
| pdoc | HTML source-code documentation |

Use a project-specific Python virtual environment. Record the tested Python version and package versions once setup is complete. A separate `requirements.txt` will hold the pip dependency list; do not pass this Markdown checklist to `pip install -r`.

## Completion evidence

For each completed item, retain evidence in the relevant source code, test report, experiment log, generated documentation, report, or submission record. A checked box is an organisational aid, not a substitute for that evidence.