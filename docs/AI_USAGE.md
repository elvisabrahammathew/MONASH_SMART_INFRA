# AI-use reflection and verification record

## AI tool, purpose, and contribution

I used **OpenAI Codex** as a support tool while completing this project. It helped me organise the repository, draft and explain parts of the Python code, interpret errors, and structure documentation and presentation material. Its contribution was substantial for drafting and workflow organisation, but it did not determine the final engineering question, data scope, model-selection rule, results, or conclusions. I did not treat AI output as evidence.

I used AI for these tasks because the project combines data extraction, time-series feature construction, regression evaluation, testing, documentation, and version control. It made it faster to generate a structured starting point and understand error messages, but I still needed to verify every material decision against the supplied data and generated results.

## What I checked myself

I checked the sensor-location workbook and confirmed that Building 60, room G.25 had a usable occupancy-space mapping. I checked the analysis date range, the data audit, forecast plots, model metric tables, and automated test results. I also checked that the chronological train, validation, and final-test periods were used in that order rather than randomly shuffling timestamps.

I selected 15, 30, and 60-minute forecast horizons because the data are represented in 15-minute bins. These horizons show the trade-off between short-term forecast accuracy and useful advance notice. I kept 30 minutes as the main project horizon because it gives a laboratory user time to decide whether to use the room while remaining close enough to the current sensor observation to be practical.

The regression models predict a continuous headcount, so they can produce fractional values. I used a 0.5-person threshold to turn that forecast into an advisory availability signal: a predicted headcount of 0.5 or below represents an empty room. This does not mean the room is confirmed as bookable or accessible.

## Decisions and limitations

Ridge regression achieved the best validation MAE and was selected before the final test period was examined. On the final test period, persistence performed better. This means that using the current headcount as the next forecast generalised better when room behaviour changed in the later period. I kept this result rather than changing the selection rule after seeing the final test results.

I excluded environmental predictors from the final model because the supplied metadata did not prove that an environmental sensor was located in G.25. Combining those records with occupancy data would have introduced an unsupported assumption.

The project predicts later sensor-derived headcounts. It does not validate the occupancy sensor against manual observations, confirm room bookings, prove a person can access the room, or model HVAC energy, thermal comfort, or ventilation control outcomes.

## AI suggestions I checked, changed, or rejected

I rejected the suggestion to include environmental measurements without a verified mapping to G.25. I also checked the timezone handling in the horizon-sensitivity script and accepted a correction that returns timestamps to Australia/Melbourne time before creating time-of-day and weekday features. I verified the correction by rerunning the sensitivity study and the automated tests.

AI-generated drafts also required editing. Some early documentation wording and formatting were unclear or inconsistent, so I corrected the language, verified the reported figures against CSV outputs, and kept only claims supported by the data.

AI made the workflow faster by helping me structure and debug the project, but it also made it necessary for me to read the code carefully and understand each step before presenting it. I remain responsible for the research question, code, calculations, evidence, interpretation, citations, and presentation. I can explain the purpose of each model, validation design, availability threshold, and project limitations.
