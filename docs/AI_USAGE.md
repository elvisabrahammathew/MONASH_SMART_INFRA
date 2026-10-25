# AI Use Report for MMA3001 Project

## 1. Purpose of this statement

This statement documents how artificial intelligence was used during my MMA3001 project, **Smart Laboratory Availability Forecasting for Building 60, Room G.25**.

The project uses time-stamped occupancy-sensor data to forecast future headcount and convert this into an advisory laboratory-availability signal. The model predicts whether the laboratory is likely to be empty in 30 minutes. It is not a booking system, access-control system, or independent validation of sensor accuracy.

I used AI to support planning, programming, debugging, documentation, GitHub workflow, results interpretation, and presentation preparation. I remained responsible for the final scope, decisions, verification, submitted files, and engineering claims.

## 2. AI tool used

The main AI tool used was **OpenAI Codex**.

I used Codex through a chat interface connected to my local project folder and GitHub repository. It could inspect code, explain errors, suggest changes, create documentation, run tests, and help organise files.

I did not use AI to generate source data, manipulate model outputs, invent results, or replace the requirement to verify the project myself.

## 3. Approximate level of AI contribution

AI made a substantial contribution to technical drafting and workflow support.

It assisted with:

- structuring the GitHub repository;
- drafting Python modules;
- explaining Python, Git, VS Code, and package-installation issues;
- generating documentation drafts;
- helping organise automated tests;
- explaining model outputs and possible limitations;
- preparing presentation and report material.

However, AI did not independently choose the project data, validate the sensor data against reality, decide the final engineering claims, or determine whether the results were suitable for submission.

My work included reviewing the supplied files, choosing the project scope, approving or rejecting suggestions, running and inspecting outputs, checking documentation, reviewing GitHub changes, and preparing to explain the method and results.

## 4. My independent engineering decisions

I made or approved the following decisions:

1. **Problem scope:** I selected Building 60, room G.25, Keenan Lab, as the analysis location because it had a usable occupancy-space mapping in the supplied metadata.
2. **Forecasting question:** I selected a 30-minute laboratory-availability forecast as the main question. This is a practical time period because users can make a decision before arriving at or using the laboratory.
3. **Time resolution and sensitivity horizons:** I used 15-minute data intervals. I selected 15, 30, and 60-minute horizons because they represent one, two, and four 15-minute forecast steps. This allowed comparison between short-term accuracy and useful advance notice.
4. **Availability definition:** I approved the rule that a predicted headcount of less than or equal to 0.5 means advisory availability. Regression models can predict fractional values, so the threshold provides a practical definition of an empty room.
5. **Validation approach:** I used a chronological 60% training, 20% validation, and 20% final-test split. I did not use random splitting because future occupancy data must not influence earlier forecasts.
6. **Model selection rule:** I selected the model using validation MAE before examining the final test period. Ridge regression had the lowest validation MAE.
7. **Interpretation of final-test results:** I retained the result that persistence outperformed ridge regression on the final test period. I did not change the selection rule after viewing the final test result.
8. **Environmental variables:** I excluded environmental sensor variables because the provided metadata did not confirm that an environmental sensor was located in G.25. I did not want to make unsupported assumptions.
9. **Engineering limits:** I limited the final claims to forecasting later sensor-derived headcounts. I did not claim confirmed room bookings, sensor ground truth, HVAC savings, thermal comfort, or access-control decisions.

## 5. Representative AI prompts and how I used the responses

The following are representative examples. They show the type of assistance received rather than reproducing every message in the full chat history.

| Representative prompt or request | AI support received | My independent action |
| --- | --- | --- |
| “Help me interpret the project brief and identify a feasible scope.” | Explained possible forecasting directions and suggested narrowing the project to one room. | I selected G.25 as the final scope after reviewing the supplied metadata and considering the available data. |
| “How should I structure the repository for a reproducible project?” | Suggested folders for source code, tests, documentation, results, reports, and presentation files. | I created and maintained the repository structure and checked which files should be tracked or excluded from GitHub. |
| “What checks should I carry out on the supplied sensor data?” | Suggested checking mapping quality, timestamp coverage, missing data, sensor gaps, resampling, and chronological validation. | I reviewed the G.25 mapping, data-audit outputs, source date range, longest outage, and generated figures. |
| “Can you explain chronological validation and possible time leakage?” | Explained why time-series observations should not be randomly shuffled. | I used and checked the chronological training, validation, and final-test design. |
| “What do MAE, RMSE, precision, recall, and F1 mean for this project?” | Explained how the metrics measure headcount error and availability-signal performance. | I interpreted the final metric tables and reported that ridge won validation MAE while persistence performed better on the final test. |
| “Are 15, 30, and 60-minute horizons suitable?” | Explained the relationship between 15-minute bins and the three forecast horizons. | I retained all three horizons and selected 30 minutes as the main practical use case. |
| “How can I verify that the sensitivity analysis uses the correct local time?” | Identified that calendar features should use Melbourne time rather than UTC. | I approved the correction, reran the sensitivity analysis, and checked that the tests still passed. |
| “How should I prepare the repository for submission?” | Helped identify required README, documentation, test report, licence, source code, and GitHub evidence. | I checked the final repository contents, results, test report, and submission checklist. |

AI provided drafting, explanation, debugging, and documentation support throughout the project. I used this support to work more efficiently, but I remained responsible for selecting the scope, reviewing the supplied data, checking outputs, running tests, interpreting results, deciding which claims were justified, and preparing the final submission. AI-assisted code and writing were reviewed before inclusion. I did not use AI output as experimental evidence.

## 6. How AI-generated code and writing were checked

I checked AI-assisted material through the following process.

### Data and metadata checks

I checked the metadata workbook and confirmed that G.25 had a usable occupancy-space mapping. I reviewed the date range and used data from May to December 2024.

I checked the data-audit outputs, including:

- number of occupancy events;
- 15-minute resampled intervals;
- headcount range;
- missing intervals;
- forward-filled intervals;
- longest data outage;
- timestamp coverage.

### Code and workflow checks

I reviewed the role of each main source file:

- `data.py` handles sensor archive extraction, timestamp conversion, filtering, resampling, and audit information;
- `features.py` creates lagged occupancy features, calendar features, and the future target;
- `models.py` defines baselines, machine-learning models, and performance metrics;
- `pipeline.py` runs the reproducible end-to-end workflow;
- `sensitivity.py` compares 15-, 30-, and 60-minute horizons.

I also checked that the code avoids time leakage by using only information available at each forecast time.

### Test checks

I ran the automated tests and checked that the project reported:

```text
6 passed
```

The tests cover:

- occupancy resampling and short carried gaps;
- correct future-target alignment;
- chronological train/validation/test splitting;
- hand-calculated regression metrics;
- availability-threshold metrics;
- a synthetic end-to-end modelling workflow.

### Result checks

I reviewed:

- validation MAE results;
- final-test MAE, RMSE, and bias results;
- availability accuracy, precision, recall, and F1;
- the forecast figure;
- the final-test MAE comparison;
- the availability F1 comparison;
- the selected-model confusion matrix;
- horizon sensitivity results.

## 7. AI limitations, errors, and rejected suggestions

AI assistance had limitations and required checking.

### Environmental-data suggestion

AI supported the possibility of including environmental variables. I rejected this for the final model because the supplied metadata did not verify a co-located environmental sensor for G.25. Using environmental features without that mapping would have weakened the engineering validity of the project.

### Documentation and formatting errors

Some early AI-generated documentation included wording, grammar, formatting, and consistency problems. These included unclear sentences, outdated test counts, and formatting errors in Markdown. These were corrected during review.

### Time-zone issue

During review, an issue was identified in the horizon-sensitivity workflow. Timestamps were parsed through UTC, which could have made time-of-day and weekday features represent UTC rather than Melbourne local time.

I accepted the correction to return timestamps to `Australia/Melbourne` before creating time-of-day and weekday features. I then reran the sensitivity analysis and automated tests.

### Limits of the model

AI cannot determine whether the room was actually available for booking, whether people could access it, whether sensor headcount is independently correct, or whether a prediction would reduce HVAC energy use.

Those claims would require additional evidence such as:

- manual occupancy observations;
- booking-system data;
- access-control data;
- verified environmental-sensor mapping;
- HVAC operational data;
- energy-consumption data.

## 8. How AI affected my workflow and understanding

AI made my workflow faster by helping me break the project into manageable stages:

1. inspect the supplied data and metadata;
2. select a feasible room and question;
3. create a reproducible repository;
4. clean and resample the sensor data;
5. create time-safe prediction features;
6. compare machine-learning models and baselines;
7. validate models chronologically;
8. run sensitivity analysis;
9. document and test the workflow;
10. prepare results for presentation.

AI also improved my understanding of:

- why time-series data must be evaluated chronologically;
- why random train/test splitting would be inappropriate;
- why baseline models are important;
- why persistence can outperform more complex regression models;
- why validation selection must occur before final testing;
- why sensor-derived availability is different from booking availability;
- why limitations must be reported clearly.

## 9. Final responsibility statement

I remain responsible for the final submitted work, including:

- the engineering question;
- code and repository contents;
- data handling;
- model selection;
- validation design;
- sensitivity analysis;
- calculations;
- figures;
- written report;
- presentation;
- interpretation of results;
- citations and academic integrity.

The final project forecasts future sensor-derived headcounts for one laboratory. It does not claim independent ground-truth occupancy validation, confirmed booking availability, access-control decisions, HVAC control performance, thermal-comfort outcomes, or energy savings.
