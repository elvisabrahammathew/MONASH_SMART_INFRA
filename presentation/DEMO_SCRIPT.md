# Five-minute presentation and demonstration

## Before the appointment

Open these tabs before you start:

1. The final slide deck or this script.
2. GitHub repository home page showing the README and folder structure.
3. `docs/html/index.html` for HTML code documentation.
4. `results/test-report.html` for the automated-test report.
5. The final metric table and forecast figure from the selected horizon.

Keep raw data files closed. They are large and are not needed for the demonstration.

## Slide 1 — Problem and scope (0:00-0:40)

Say:

> My project predicts room occupancy 30 minutes ahead for Building 60, room G.25, the Keenan Lab. The intended use is to give building operators an early indication of likely occupancy for ventilation or HVAC planning. It does not directly control HVAC equipment or claim energy savings.

Show the research question, input, output, and chosen room.

## Slide 2 — Data and quality audit (0:40-1:20)

Say:

> I used 643,290 occupancy events from May to December 2024. I converted irregular sensor events to 15-minute bins. I found a maximum outage of 21.6 hours, so I carried the previous state forward for no more than one hour and then treated the value as missing. Missing data were never assumed to mean zero people.

Show the data-quality table. Explain that environmental measurements were excluded because the supplied mapping did not confirm a co-located environmental sensor for G.25.

## Slide 3 — Method and code (1:20-2:10)

Say:

> The code reads the large archive in chunks, filters to G.25, creates lagged occupancy and calendar features, then predicts headcount two 15-minute intervals ahead. I compared persistence and weekday/time baselines with ridge regression, a decision tree, and support-vector regression.

Demonstrate, briefly:

- `src/occupancy/data.py`: chunking, resampling, and the one-hour carry rule.
- `src/occupancy/features.py`: lag features and the future target.
- `src/occupancy/models.py`: baselines, regression models, MAE, RMSE, bias, and runtime.
- `src/occupancy/pipeline.py`: reproducible command-line entry point.

Do not read code line by line. Explain the job of each file.

## Slide 4 — Validation and results (2:10-3:20)

Say:

> I split the data chronologically: 60% training, 20% validation, and 20% final test. I never shuffled timestamps. Ridge regression had the best validation MAE, 1.089 people, and was selected before I looked at the final test period.

Then show the final-test table:

> On the final test period, persistence had the best MAE at 0.461 people, while SVR had the lowest RMSE. The selected ridge model overpredicted by 0.261 people. This indicates that the room behaviour changed between development and the final period, so I report the limitation instead of claiming the complex model always wins.

## Slide 5 — Verification, repository, and lessons (3:20-4:25)

Show GitHub, then HTML documentation and the test report.

Say:

> The repository separates reusable source code, tests, documentation, results, and local raw data. The raw archive is ignored by Git. Four automated tests currently verify resampling behaviour, future-target alignment, chronological splitting, and hand-calculated metrics. The HTML documentation is generated from source docstrings.

> The main lesson is that a strong baseline can outperform a more complex model after operating conditions shift. Data quality and correct time-based validation were more important than adding more algorithms.

## Slide 6 — AI disclosure and closing (4:25-5:00)

Say:

> I used Codex for planning, code drafting, and documentation support. I checked the suggestions against the supplied files, ran the tests, and corrected a missing-current-occupancy issue found during validation. I remain responsible for the method, results, and conclusions.

End with:

> The next step is a 15-, 30-, and 60-minute horizon sensitivity study and further investigation of errors around occupancy transitions and outages.

## Demonstration checklist

- Confirm the repository is on the final `main` branch and GitHub is accessible.
- Run `pytest` once before the appointment; do not wait for a live test run unless requested.
- Be able to explain what each test proves and what it does not prove.
- Have the final commands, metric CSVs, figures, test report, and HTML documentation already open.
- Practise once with a five-minute timer. Stop at five minutes even if a slide remains.
