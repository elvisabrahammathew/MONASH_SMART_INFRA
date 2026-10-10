# AI-use reflection log

## Current disclosure

Codex was used for project planning, interpreting the supplied brief and data structure, proposing the focused G.25 forecasting question, drafting repository documentation, generating an initial Python implementation, and suggesting presentation material.

The student remains responsible for the engineering question, all final code, data decisions, calculations, conclusions, citations, and presentation answers. AI output was checked by inspecting raw archive structure, executing the pipeline components on the supplied data, running automated tests, and reviewing generated metrics.

## Verification and corrections

| AI-assisted item | How it was checked | Correction or limitation identified |
| --- | --- | --- |
| Proposed occupancy/environment model | Compared sensor IDs and locations in the supplied workbook and archives | No verified environmental-to-G.25 mapping exists, so environmental features were excluded. |
| Initial data processing | Loaded the G.25 source records in chunks and inspected dates, gaps, counts, and duplicate handling | The archive contains dates beyond its filename period, so the analysis explicitly filters May-December 2024. |
| Forecast features | Tested future-target alignment and chronological split behaviour | Rows with missing current occupancy were excluded because persistence cannot forecast them. |
| Model comparison | Ran ridge, decision tree, SVR, and baselines on chronologically later data | Ridge won validation MAE, but persistence had lower final-test MAE; this is reported as a limitation rather than hidden. |

## Student reflection to complete

Before submitting, add dated entries explaining:

1. Which code sections you read and can explain without assistance.
2. Which AI suggestions you rejected, changed, or found unhelpful.
3. Why you selected the final horizon and model from validation evidence.
4. How this assistance affected your understanding of leakage, missing data, regression metrics, and reproducibility.
5. Your approximate judgement of AI contribution to planning, code drafting, testing, and writing.
