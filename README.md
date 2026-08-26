# FDA MAUDE Medical Device Event Intelligence & Quality Analytics

## Overview

An end-to-end MedTech analytics portfolio project built around public FDA MAUDE reporting data. The implementation combines streaming Python ingestion, data-quality controls, PostgreSQL/SQL analytics, Power BI reporting, testing/UAT, and a clearly separated synthetic investigation/CAPA workflow.

> **Important:** This is a portfolio/demo project. MAUDE reporting data does not by itself establish incidence, prevalence, failure rates, comparative safety, or causality. Synthetic investigation, root-cause, CAPA, and effectiveness information is fictional and not FDA-sourced.

## Current implementation

The repository now contains a runnable Phase 1 foundation that can:

- Stream `.txt` or `.zip` MAUDE-style delimited files without loading the entire file into memory.
- Infer expected field count from the source header.
- Detect malformed rows and missing `MDR_REPORT_KEY` values.
- Preserve rejected rows in quarantine output rather than silently dropping them.
- Produce JSON ingestion summaries and field-level data-quality profiles.
- Run automated pytest coverage for the ingestion/quarantine logic.
- Bulk-load cleaned CSV output into PostgreSQL.
- Start a local PostgreSQL 16 instance with Docker Compose.

## Business problem

Public post-market reporting data is large, distributed across related files, and contains structural and completeness issues. The objective is to create a transparent and reproducible analytical workflow that preserves data grain, exposes data-quality limitations, and helps stakeholders understand reporting patterns without overstating what the data can prove.

## Architecture

```text
FDA MAUDE ZIP/TXT files
          |
          v
Streaming Python ingestion
          |
          +----> quarantine / DQ evidence
          |
          v
Clean source outputs
          |
          v
PostgreSQL raw/staging/clean/DQ/model layers
          |
          v
Analytical SQL views
          |
          v
Power BI semantic model + dashboard
          |
          +--> Executive Overview
          +--> Device/Product Analysis
          +--> Event/Reporting Patterns
          +--> Data Quality
          +--> Methodology & Limitations

Separate synthetic demonstration workflow:
Pattern -> Review -> Investigation -> CAPA -> Effectiveness
```

## Data model principles

- `MDR_REPORT_KEY` is preserved as a string and used for report reconciliation.
- Report-level and device-level records are modeled separately.
- Distinct report count and device-record count are separate measures.
- Malformed records are quarantined and counted.
- Base/device orphan keys are surfaced rather than silently discarded.
- Problem-code mappings are not invented when reference data is missing.
- Raw FDA data is not committed to the repository.

## Technology stack

| Layer | Technology |
|---|---|
| Source | FDA MAUDE |
| ETL | Python / pandas-compatible workflow; streaming csv processing for large files |
| Database | PostgreSQL 16 |
| Analytics | SQL |
| BI | Power BI / DAX |
| Testing | pytest, SQL reconciliation, Power BI validation, UAT |
| Documentation | Markdown |
| Version control | Git / GitHub |

## Repository structure

```text
00_Project_Overview/
01_Source_Assessment/
02_Business_Requirements/
03_Process_Maps/
04_Data_Dictionary/
05_Data_Quality/
06_Python_ETL/
07_SQL/
08_Data_Model/
09_PowerBI/
10_Testing_and_UAT/
11_Synthetic_CAPA/
12_Executive_Case_Study/
13_Demo_Materials/
14_Limitations_and_References/
src/maude_pipeline/
tests/
scripts/
sql/
data/sample/
```

## Quick start

```bash
git clone https://github.com/Yogeshdabir/FDA-MAUDE-Medical-Device-Analytics.git
cd FDA-MAUDE-Medical-Device-Analytics
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
pytest -q
```

Run the included sample:
```bash
python -m src.maude_pipeline --base data/sample/base_sample.txt --output-dir outputs/sample
```

Run the pipeline against downloaded FDA MAUDE files:
```bash
python -m src.maude_pipeline \
  --base /path/to/mdrfoi.zip \
  --device /path/to/device.zip \
  --output-dir outputs/maude_2026
```

Start PostgreSQL locally:
```bash
docker compose up -d
```

See [`RUN_LOCAL.md`](RUN_LOCAL.md) for the complete local workflow.

## FDA source

FDA publishes downloadable MAUDE data files and states that the downloadable ZIP files are updated monthly. Use the official FDA MDR Data Files page for the current source snapshot:

https://www.fda.gov/medical-devices/medical-device-reporting-mdr-how-report-medical-device-problems/mdr-data-files

## Validation principles

Core controls include report-key uniqueness, device-key uniqueness, Base/Device reconciliation, report-vs-device grain protection, malformed-row quarantine, date validation, event/product aggregation reconciliation, DAX-to-SQL KPI reconciliation, Power BI relationship/filter testing, synthetic-data isolation, UAT, and requirements traceability.

## Limitations

MAUDE is a passive reporting source. Reports may be incomplete, inaccurate, duplicated, or submitted for different purposes. Report counts are not exposure-adjusted rates and do not independently establish device causality or comparative safety. The project therefore presents reporting patterns and data-quality indicators rather than confirmed safety conclusions.

## Synthetic data boundary

Synthetic investigation, root-cause, CAPA, and effectiveness records are stored separately and must be marked as synthetic. They cannot modify or overwrite FDA source-derived facts or MAUDE analytical counts.

## Portfolio positioning

**MedTech/PMS domain knowledge + Business Analysis + Data Engineering + SQL + Power BI + Data Quality + Validation/UAT.**

## Status

**Phase 1 executable foundation implemented.** Next layers are the full DQ/report-to-device reconciliation module, production PostgreSQL star-schema deployment, analytical SQL views, Power BI implementation, synthetic workflow data generation, and final validation evidence.
