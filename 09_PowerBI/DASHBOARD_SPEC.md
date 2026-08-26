# Power BI Dashboard Specification

## Page 1 — Executive Overview

- Distinct MAUDE Reports
- Device Records
- Adverse Event Reports
- Product Problem Reports
- Monthly reporting trend
- Event-type distribution
- Reporting period/source snapshot

## Page 2 — Device & Product Analysis

- Product code
- Device category
- Brand/model where available
- Manufacturer
- Device-record analysis
- Drill-through capability

## Page 3 — Event & Reporting Patterns

- Event type
- Reporting trends
- Reporting delay indicators where valid
- Review-candidate patterns

## Page 4 — Data Quality

- DQ scorecard
- Missingness
- Malformed/quarantined records
- Orphan records
- Key uniqueness
- Reconciliation status

## Page 5 — Methodology & Limitations

- Source and snapshot/date
- Processing approach
- Table grain
- Transformation rules
- Limitations
- Regulatory interpretation disclaimer

## Core Measure Rule

`Distinct MAUDE Reports` must be calculated at report grain and must not be inflated by device-level relationships.
