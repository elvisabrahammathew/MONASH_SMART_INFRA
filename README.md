# MMA3001 | Room Occupancy Prediction

An individual Numerical Methods and Machine Learning project investigating how building sensor data can support short-term room occupancy forecasting and inform ventilation and HVAC scheduling.

**Status: assessment-ready.** The raw data remain local and excluded from Git. The repository contains reproducible code, tests, generated documentation, a data audit, sensitivity results, report draft, and presentation deck.

## Engineering problem

Room occupancy varies throughout the day. Forecasting these changes could help building operators anticipate ventilation demand and plan HVAC operation.

This project investigates whether historical occupancy measurements and calendar information can predict future occupancy more accurately than simple baseline methods. Its engineering contribution is an evaluated forecasting method and an explanation of its accuracy, computational cost, and limitations.

The initial scope is occupancy prediction for one room. HVAC control and measured energy savings are outside the initial scope; they must not be inferred from forecasting accuracy alone.

## Research question

> Can the occupant headcount in Building 60, room G.25 (Keenan Lab) be forecast 30 minutes ahead from recent headcount and calendar information more accurately than persistence and weekday/time baselines?

The analysis aggregates state observations to 15-minute bins and explicitly filters the source data to 1 May-31 December 2024. Ridge regression, decision-tree regression, and support-vector regression are selected and compared using later validation observations. See [the runbook](docs/RUNBOOK.md) for exact commands.

## Dataset and LiDAR scope

The proposed data source is the Monash Smart Infrastructure occupancy and environmental dataset described in the supplied Dataset 2 project information. The expected options are approximately one year of observations for a single room in the MSM Lab, or approximately one month of observations across Building 60. These are expected scopes, not confirmed contents of a received dataset.

The supplied data are timestamped occupancy-state and headcount observations rather than raw point clouds. The extracts do not document the sensing technology or provide independently observed ground truth, so this repository does not claim that the sensor is LiDAR or that its headcount is independently accurate.

Before modelling, confirm:

- The data release and access conditions; the supplied slide states that ethics clearance was pending.
- Whether occupancy represents a person count, a binary occupied/unoccupied label, or another measurement.
- How occupancy measurements were produced and whether independent validation is available.
- The available environmental variables, units, room identifiers, and quality flags.
- Timestamp timezone, sampling frequency, missing observations, and recording coverage.
- Permissions for storing, sharing, and providing assessor access to the data.

If only binary occupancy is provided, the problem and evaluation will be revised to classification. If the project instead uses raw LiDAR scans, its inputs, processing methods, and independent validation requirements will be revised before implementation.

## Inputs and outputs

| Item | Proposed specification |
| --- | --- |
| Time | Timestamp with a documented timezone and sampling convention |
| Location | Room or zone identifier; initially one selected room |
| Occupancy | Historical measured person counts, subject to confirmation |
| Environmental measurements | Excluded from the main G.25 model until a co-located mapping is verified |
| Forecast | Predicted occupancy count at a specified future timestamp |
| Data-quality information | Flags identifying missing, stale, or unsupported inputs |
| Evaluation outputs | Error metrics, baseline comparisons, runtime measurements, and figures |

Exact file formats, column names, valid ranges, and units are documented in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md). Missing sensor readings are never treated as zero occupancy. The pipeline documents duplicate timestamps, invalid counts, long outages, and unsupported inputs.

## Computational workflow

1. **Audit the data:** inspect coverage, sampling intervals, missingness, unusual values, and occupancy patterns.
2. **Define evaluation periods:** separate earlier development data from later validation and final test periods.
3. **Prepare inputs:** apply documented cleaning rules and construct historical features using only information available at forecast time.
4. **Build baselines:** compare persistence with typical occupancy for the same weekday and time, estimated from training data.
5. **Develop the main model:** begin with linear or ridge regression and justify the selected features and settings.
6. **Compare and refine:** use validation data to assess model choices, forecast horizons, and feature contributions.
7. **Evaluate the final method:** report performance on an untouched future test period and analyse failure cases.
8. **Reproduce the analysis:** regenerate results, tests, and documentation using the recorded environment and configuration.

One nonlinear comparison may be added if time and data support it. Additional complexity will be justified by evidence rather than assumed to improve the solution.

## Validation and verification

### Predictive validation

- Preserve time order when splitting the data; do not randomly shuffle observations for forecasting evaluation.
- Fit learned preprocessing and model parameters using training data only.
- Ensure training target timestamps do not extend into validation or test periods.
- Use only sensor information that would have been available when each forecast was issued.
- Select model settings using validation data and reserve the final test period for final evaluation.
- Exclude unavailable target measurements from scoring and report the number of excluded observations.

For count prediction, the planned measures are mean absolute error (MAE), root mean squared error (RMSE), and signed bias, all expressed in people. Training and prediction runtime will also be recorded. Error analysis will distinguish occupied and unoccupied periods and examine arrivals, departures, and sensor outages.

Sensitivity analysis will examine a manageable selection of forecast horizons, feature groups, missing-input scenarios, and model settings. The final choice will consider both predictive accuracy and computational cost.

### Code verification

Automated tests check resampling behaviour, future-target alignment, chronological split boundaries, and metric calculations against hand-worked examples. The generated [test report](results/test-report.html) records the latest results. Passing software tests are reported separately from evidence of predictive accuracy.


## Setup and reproduction

The executable pipeline is [src/occupancy/pipeline.py](src/occupancy/pipeline.py). Dependencies are recorded in `requirements.txt`; exact setup, execution, testing, and HTML-documentation commands are in [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Data handling

Dataset redistribution permissions have not yet been confirmed. Original data must be excluded from version control before they are added to the working directory. A private repository does not itself establish permission to upload restricted data.

The repository will document how an authorised assessor can obtain or access the data. Any synthetic sample will be labelled clearly and used only to demonstrate execution or test behaviour, not as evidence of real-world predictive accuracy.

## Results and limitations

Initial results are recorded in [docs/INITIAL_RESULTS.md](docs/INITIAL_RESULTS.md). Ridge regression was selected from validation MAE, but persistence had a lower final-test MAE; this is reported as a distribution-shift limitation rather than hidden.

Known limitations of the proposed scope include:

- Agreement with sensor-generated occupancy labels does not independently establish the sensor's counting accuracy.
- Results for one room may not generalise to other rooms, buildings, or operating periods.
- Sensor outages, measurement error, and changing usage patterns may affect performance.
- A useful occupancy forecast does not by itself demonstrate safe HVAC control or energy savings.

The final results include baseline comparisons, measured performance, a 15/30/60-minute sensitivity study, and an evidence-based explanation of the selected method. See [the sensitivity metrics](results/horizon_sensitivity.csv), [the report draft](report/MMA3001_Occupancy_Forecasting_Report.docx), and [the presentation deck](presentation/MMA3001_Occupancy_Forecasting_Presentation.pptx).

## AI use and individual responsibility

Codex was used for project planning, code drafting, documentation, and presentation support. The current disclosure and student-completion prompts are in [docs/AI_USAGE.md](docs/AI_USAGE.md). These activities are not experimental evidence.

The student remains responsible for the final question, implementation, verification, references, interpretation, and submitted claims. Verification that has not been performed will not be claimed.

## Assessment deliverables

The supplied MMA3001 project brief requires:

- An individual written report of 5-10 pages, with references and appendices excluded from the ten-page limit.
- An accessible GitHub repository containing a README, source-code licence, functional main branch, comments and docstrings, HTML source-code documentation, test functions, and a test report.
- Submission of the written report and a zipped clone of the repository through Moodle, together with an accessible repository link.
- A five-minute presentation followed by three minutes of questions in Week 14; the presentation appointment must be booked and attended.

Exact submission dates must be checked in the Unit Overview Spreadsheet. Student-proposed projects require teaching-team approval before substantial work begins.

## Sources and licence

Project planning is based on `MMA3001_2026_Project_Brief.pdf` and the supplied **Project Information - Dataset 2** slide. These teaching materials are not included in this repository.

The source code is released under the [MIT License](LICENSE). Dataset permissions are separate and have not yet been confirmed.
