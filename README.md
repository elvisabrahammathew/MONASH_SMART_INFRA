# MMA3001 | Room Occupancy Prediction

An individual Numerical Methods and Machine Learning project investigating how building sensor data can support short-term room occupancy forecasting and inform ventilation and HVAC scheduling.

**Status: project planning.** This repository currently contains the project outline. The dataset has not been added, and the computational workflow, tests, and results have not yet been implemented. The research question below is provisional until the available data and project scope are confirmed.

## Engineering problem

Room occupancy varies throughout the day. Forecasting these changes could help building operators anticipate ventilation demand and plan HVAC operation.

This project will investigate whether historical occupancy measurements and available environmental sensor data can predict future occupancy more accurately than simple baseline methods. Its engineering contribution will be an evaluated forecasting method and an explanation of its accuracy, computational cost, and limitations.

The initial scope is occupancy prediction for one room. HVAC control and measured energy savings are outside the initial scope; they must not be inferred from forecasting accuracy alone.

## Research question

> Can recent occupancy measurements and available environmental data predict room occupancy 15 minutes ahead more accurately than persistence and weekday/time baselines?

The forecast horizon will be confirmed after inspecting the sampling interval, data coverage, and intended engineering use. At least one selected numerical or machine-learning method will be explicitly linked to material taught in MMA3001.

## Dataset and LiDAR scope

The proposed data source is the Monash Smart Infrastructure occupancy and environmental dataset described in the supplied Dataset 2 project information. The expected options are approximately one year of observations for a single room in the MSM Lab, or approximately one month of observations across Building 60. These are expected scopes, not confirmed contents of a received dataset.

The intended project involves LiDAR-based occupancy sensing. However, the supplied dataset description does not confirm the sensor technology or whether raw LiDAR point clouds will be available. The current plan assumes timestamped occupancy measurements rather than raw point-cloud processing.

Before modelling, confirm:

- The data release and access conditions; the supplied slide states that ethics clearance was pending.
- Whether occupancy represents a person count, a binary occupied/unoccupied label, or another measurement.
- Whether LiDAR supplies those measurements and how the measurements were validated.
- The available environmental variables, units, room identifiers, and quality flags.
- Timestamp timezone, sampling frequency, missing observations, and recording coverage.
- Permissions for storing, sharing, and providing assessor access to the data.

If only binary occupancy is provided, the problem and evaluation will be revised to classification. If the project instead uses raw LiDAR scans, its inputs, processing methods, and independent validation requirements will be revised before implementation.

## Planned inputs and outputs

| Item | Proposed specification |
| --- | --- |
| Time | Timestamp with a documented timezone and sampling convention |
| Location | Room or zone identifier; initially one selected room |
| Occupancy | Historical measured person counts, subject to confirmation |
| Environmental measurements | Only variables supplied in the dataset, with documented units |
| Forecast | Predicted occupancy count at a specified future timestamp |
| Data-quality information | Flags identifying missing, stale, or unsupported inputs |
| Evaluation outputs | Error metrics, baseline comparisons, runtime measurements, and figures |

Exact file formats, column names, valid ranges, and units will be recorded in a data dictionary once the data are available. Missing sensor readings will not be treated as zero occupancy. Rules for duplicate timestamps, invalid counts, long outages, and unsupported inputs will be documented and tested.

## Planned computational workflow

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

Automated tests will check input validation, historical feature construction, future target alignment, chronological split boundaries, metric calculations against hand-worked examples, and execution of the complete workflow on a small sample.

Tests and a generated test report are planned but are not yet available. Passing software tests will be reported separately from evidence of predictive accuracy.


## Setup and reproduction

There is no executable pipeline or dependency file yet. Installation and execution instructions will be added alongside the first working implementation and checked from a fresh clone.

The intended environment is Python, using libraries for numerical analysis, tabular data, plotting, machine learning, testing, and HTML documentation. Exact Python and package versions will be recorded after the environment is created and tested.

The completed instructions will cover:

1. Creating an isolated Python environment and installing the recorded dependencies.
2. Obtaining authorised data and placing it in the expected local directory.
3. Running preprocessing, baseline modelling, training, and evaluation.
4. Running automated tests and generating the test report.
5. Generating HTML source-code documentation.
6. Reproducing the reported tables and figures.

## Data handling

Dataset redistribution permissions have not yet been confirmed. Original data must be excluded from version control before they are added to the working directory. A private repository does not itself establish permission to upload restricted data.

The repository will document how an authorised assessor can obtain or access the data. Any synthetic sample will be labelled clearly and used only to demonstrate execution or test behaviour, not as evidence of real-world predictive accuracy.

## Results and limitations

**No experiments have been completed and no performance claims are made at this stage.**

Known limitations of the proposed scope include:

- Agreement with sensor-generated occupancy labels does not independently establish the sensor's counting accuracy.
- Results for one room may not generalise to other rooms, buildings, or operating periods.
- Sensor outages, measurement error, and changing usage patterns may affect performance.
- A useful occupancy forecast does not by itself demonstrate safe HVAC control or energy savings.

The final results will include baseline comparisons, measured performance, failure cases, and an evidence-based explanation of the selected method.

## AI use and individual responsibility

Codex was used to assist with interpreting the supplied project brief, proposing a provisional project scope and timeline, suggesting a repository structure, and drafting this README. These activities are planning and documentation assistance; they are not experimental evidence.

The student remains responsible for the final question, implementation, verification, references, interpretation, and submitted claims. A detailed AI-use log will record the tool, purpose, approximate contribution, checks performed, rejected or corrected suggestions, and the effect on the student's understanding. Verification that has not yet been performed will not be claimed.

## Assessment deliverables

The supplied MMA3001 project brief requires:

- An individual written report of 5-10 pages, with references and appendices excluded from the ten-page limit.
- An accessible GitHub repository containing a README, source-code licence, functional main branch, comments and docstrings, HTML source-code documentation, test functions, and a test report.
- Submission of the written report and a zipped clone of the repository through Moodle, together with an accessible repository link.
- A five-minute presentation followed by three minutes of questions in Week 14; the presentation appointment must be booked and attended.

Exact submission dates must be checked in the Unit Overview Spreadsheet. Student-proposed projects require teaching-team approval before substantial work begins.

## Sources and licence

Project planning is based on `MMA3001_2026_Project_Brief.pdf` and the supplied **Project Information - Dataset 2** slide. These teaching materials are not included in this repository.

A source-code licence has not yet been selected or added. Dataset permissions are separate from any future code licence.
