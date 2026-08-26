# Power BI Connection

This folder contains the Power BI semantic-model specification and connection guidance for the PostgreSQL analytical layer.

## PostgreSQL connection

Use:

- Server: `localhost`
- Port: `5432`
- Database: `maude_pms_analytics`
- Authentication: Database
- User: `maude`

Do not commit passwords or `.pbix` files containing credentials.

## Tables/views to import

Recommended first connection:

- `analytical.monthly_report_trend`
- `analytical.product_report_summary`
- `analytical.device_report_reconciliation`
- `analytical.data_quality_summary`
- `fact.maude_report`
- `fact.maude_device`

## Recommended model

Keep report and device facts at separate grains. Use `MDR_REPORT_KEY` to relate device records to report records, but calculate report-level KPIs with `DISTINCTCOUNT(MDR_REPORT_KEY)`.

## Initial pages

1. Executive Overview
2. Device & Product Analysis
3. Event & Reporting Patterns
4. Data Quality
5. Methodology & Limitations

MAUDE reporting counts must not be presented as incidence, prevalence, failure rates, or confirmed causality. Synthetic investigation/CAPA information must remain clearly separated from FDA-derived data.
