# AI-use reflection and verification record

I used Codex as a support tool while completing this project. It helped me organise the repository, draft and explain parts of the Python code, interpret errors, and structure the documentation and presentation material. I did not treat AI output as evidence. I checked the project decisions against the supplied files, generated outputs, and automated tests before using them in the final project.

## What I checked myself

I checked the sensor-location workbook and confirmed that Building 60, room G.25 had a usable occupancy-space mapping. I checked the analysis date range, the data audit, the forecast plots, model metric tables, and the automated test results. I also checked that the chronological train, validation, and final-test periods were used in that order, rather than randomly shuffling timestamps.

I selected 15, 30, and 60-minute forecast horizons because the data are represented in 15-minute bins. These horizons show the trade-off between short-term forecast accuracy and useful advance notice. I kept 30 minutes as the main project horizon because it gives a student or laboratory user enough time to decide whether to use the room, while still remaining close enough to the current sensor observation to be practical.

The regression models predict a continuous headcount, so they can produce fractional values. I used a 0.5-person threshold to turn that forecast into an advisory availability signal: a predicted headcount of 0.5 or below represents an empty room. This does not mean the room is confirmed as bookable or accessible.

## Decisions based on the results

Ridge regression achieved the best validation MAE and was selected before the final test period was examined. On the final test period, persistence performed better. This means that using the current headcount as the next forecast generalised better when room behaviour changed in the later period. I kept this result in the project rather than changing the selection rule after seeing the final test results.

I excluded environmental predictors from the final model. The supplied metadata did not prove that an environmental sensor was located in G.25, so combining those records with the occupancy data would have introduced an unsupported assumption.

The project predicts later sensor-derived headcounts. It does not validate the occupancy sensor against manual observations, confirm room bookings, or prove that a user can access the room.

## AI suggestions I checked or changed

I did not accept the suggestion to include environmental measurements without a verified mapping to G.25. I also checked the timezone handling in the horizon-sensitivity script and accepted a correction that returns timestamps to Australia/Melbourne time before creating time-of-day and weekday features. I verified the correction by rerunning the sensitivity study and the automated tests.

I remain responsible for the research question, code, calculations, evidence, interpretation, citations, and presentation. I can explain the purpose of each model, the validation design, the availability threshold, and the project limitations.
