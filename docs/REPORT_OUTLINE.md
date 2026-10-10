# Report outline

Keep the main report to 5-10 pages. References and appendices do not count toward the limit.

1. **Engineering problem and intended use** — occupancy forecasting for G.25; relevance to anticipatory ventilation/HVAC scheduling; scope and exclusions.
2. **Data, inputs, and outputs** — use `DATA_DICTIONARY.md`; show data coverage and quality issues.
3. **Method** — 15-minute aggregation, 30-minute target, leakage-safe features, chronological split, model and baseline definitions.
4. **Verification and validation** — unit tests, test report, source-data audit, chronological validation design, and metrics.
5. **Results and method comparison** — validation selection table, final-test table, runtime, and forecast figure.
6. **Sensitivity and optimisation** — 15/30/60-minute horizons, profile results, and an accuracy/runtime trade-off.
7. **Limitations and lessons** — sensor outages, no independent ground truth, uncertain mapping, distribution shift, and lack of energy evidence.
8. **AI-use reflection** — concise version of `AI_USAGE.md`, completed with your own reflection.
