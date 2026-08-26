# Python ETL

Planned pipeline:

1. Discover and validate source files.
2. Read source data with explicit dtypes where appropriate.
3. Validate schema and required fields.
4. Generate stable report/device keys.
5. Separate valid and quarantined records.
6. Normalize dates and controlled values.
7. Produce DQ metrics and validation logs.
8. Load validated populations to PostgreSQL.
9. Preserve source snapshot metadata for reproducibility.

No raw FDA source files are committed to the repository by default. Download the appropriate official MAUDE snapshot separately and configure a local data path.
