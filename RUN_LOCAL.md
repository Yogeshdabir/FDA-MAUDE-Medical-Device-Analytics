# Run the local Phase 1–2 pipeline

## 1. Clone
```bash
git clone https://github.com/Yogeshdabir/FDA-MAUDE-Medical-Device-Analytics.git
cd FDA-MAUDE-Medical-Device-Analytics
```

## 2. Python environment
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

## 3. Dependencies
```bash
pip install -r requirements.txt
```

## 4. Automated tests
```bash
pytest -q
```

## 5. Run the sample ingestion
```bash
python -m src.maude_pipeline --base data/sample/base_sample.txt --output-dir outputs/sample
```

The sample intentionally contains one missing `MDR_REPORT_KEY` and one malformed row. The pipeline writes clean output, quarantine output, and an ingestion summary.

## 6. Run real MAUDE files
Download the approved MAUDE files separately from FDA. Do not commit raw source ZIPs to GitHub.
```bash
python -m src.maude_pipeline \
  --base /path/to/mdrfoi.zip \
  --device /path/to/device.zip \
  --output-dir outputs/maude_2026
```

The pipeline streams rows and preserves malformed/missing-key rows in quarantine.

## 7. Start PostgreSQL
Requires Docker Desktop.
```bash
docker compose up -d
```

Connection:
```text
postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics
```

## 8. Deploy the analytical schema
```bash
python scripts/load_postgres.py
```

This applies:
- `sql/01_create_schemas.sql`
- `sql/02_core_tables.sql`
- `sql/03_analytical_views.sql`

## 9. Verify PostgreSQL
```bash
psql postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics
```

Then:
```sql
SELECT * FROM analytical.data_quality_summary;
SELECT * FROM analytical.monthly_report_trend;
```

## Current implementation boundary
The repository now contains executable streaming ingestion, quarantine, source validation, tests, PostgreSQL schemas, core report/device tables, and analytical views. The next layer is the production-quality mapping from the exact MAUDE source columns into the report/device tables, followed by Power BI/PBIP integration and reconciliation evidence.
