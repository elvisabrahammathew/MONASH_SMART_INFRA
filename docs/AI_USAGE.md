# AI-use disclosure and verification record

Codex was used to help interpret the project brief and supplied data structure, draft Python modules and documentation, organise the repository, generate presentation material, and identify consistency issues during review. AI assistance was used as drafting and planning support; it was not treated as experimental evidence.

## Verification performed

| AI-assisted area | Verification and resulting decision |
| --- | --- |
| Problem scope | The supplied archive and metadata were inspected. The scope was narrowed to Building 60, room G.25 because it had a direct floor-space mapping. |
| Environmental inputs | Sensor IDs and location metadata were checked. No verified co-located environmental mapping was found for G.25, so environmental features were excluded. |
| Data preparation | The G.25 records were processed in chunks and audited for date coverage, gaps, headcount range and missing bins. The analysis explicitly filters May–December 2024. |
| Leakage controls | Automated tests confirm future-target alignment and chronological splits. Features are limited to information available at forecast issue time. |
| Model comparison | Persistence, weekday/time baseline, ridge regression, decision tree and SVR were evaluated on chronological validation and final-test periods. Ridge was selected from validation; persistence later had lower final-test MAE and this limitation is reported. |
| Availability signal | The regression forecast is translated to advisory availability only when predicted headcount is less than or equal to 0.5 people. The final availability metrics are reported with the limitation that this is not a booking guarantee. |
| Software quality | Six automated tests were run, the HTML test report was generated, and source-code documentation was regenerated from docstrings. |

## Reflection on the role of AI

AI accelerated initial project scaffolding, code drafting and document organisation. The final project decisions were constrained by the supplied data: the lack of a verified environmental mapping prevented an environmental model, the 15-minute sampling interval motivated 15-, 30- and 60-minute horizons, and the 0.5-person rule made the continuous headcount forecast interpretable as an availability signal. The final-test result showed that the simple persistence baseline outperformed the validation-selected ridge model on MAE; this was retained as an engineering finding rather than adjusted away.

The student remains responsible for the research question, all submitted code, method choices, calculations, evidence, claims, citations and presentation answers. The submitted interpretation is limited to agreement with later sensor-derived observations; it does not claim independent sensor validation, confirmed bookings, access-control decisions or energy savings.
