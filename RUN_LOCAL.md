# Run the local Phase 1 pipeline

## 1. Clone
```bash
git clone https://github.com/Yogeshdabir/FDA-MAUDE-Medical-Device-Analytics.git
cd FDA-MAUDE-Medical-Device-Analytics
```

## 2. Create and activate a Python environment
Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run automated tests
```bash
pytest -q
```

## 5. Run the sample pipeline
```bash
python -m src.maude_pipeline --base data/sample/base_sample.txt --output-dir outputs/sample
```

The sample intentionally contains one missing `MDR_REPORT_KEY` and one malformed row. The pipeline creates a clean CSV, quarantine CSV, and `ingestion_summary.json`.

## 6. Run the real MAUDE files
Download the approved MAUDE files separately from FDA. The FDA publishes downloadable ZIP files and updates the current-year files monthly: https://www.fda.gov/medical-devices/medical-device-reporting-mdr-how-report-medical-device-problems/mdr-data-files

You can point the pipeline directly at the ZIP files:
```bash
python -m src.maude_pipeline \
  --base /path/to/mdrfoi.zip \
  --device /path/to/device.zip \
  --output-dir outputs/maude_2026
```

The pipeline streams rows, infers the expected field count from the source header, writes valid records to clean CSV files, and writes malformed/missing-key rows to quarantine files.

## 7. Generate a standalone profile from an extracted file
```bash
python scripts/profile_sources.py /path/to/mdrfoi.txt --output outputs/base_profile.json
```

## 8. Start local PostgreSQL
Docker Desktop is the easiest option:
```bash
docker compose up -d
```

Connection string:
```text
postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics
```

## 9. Create the database schemas
If `psql` is installed:
```bash
psql postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics -f sql/01_create_schemas.sql
```

## 10. Load a cleaned CSV into PostgreSQL
```bash
python -m src.maude_pipeline.load_postgres \
  --conninfo "postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics" \
  --file outputs/maude_2026/base_clean.csv \
  --schema raw \
  --table maude_base_clean
```

Repeat for the Device file with a different table name.

## Current implementation boundary
The repository now has a runnable streaming ingestion, quarantine, profiling, test, and PostgreSQL bulk-load foundation. The full star-schema build, analytical SQL views, and Power BI model are the next implementation layer; no raw FDA files are committed to GitHub.
