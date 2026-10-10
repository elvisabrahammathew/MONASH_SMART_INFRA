# Local data setup

Do not commit the supplied raw data without written permission from the data owner.

Place the supplied files in `data/raw/` before running the pipeline:

```text
data/raw/
|- 5occupancySensor_MayToDec2024_9MRows.zip
|- 5EnvSensor_MayToDec2024_180kRows.zip
`- Sensor ID and Locations.xlsx
```

`data/raw/` and `data/processed/` are ignored by Git. The pipeline produces
re-creatable local extracts under `data/processed/`; commit only small, approved
summary tables and figures to `results/` if your teaching team permits it.

The raw occupancy archive is approximately 1.6 GB when uncompressed. Leave it
zipped and let the pipeline read it in chunks. Do not open it in Excel.
