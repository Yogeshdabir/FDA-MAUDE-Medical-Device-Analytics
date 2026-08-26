# Data Model Design

## Analytical Grains

### Report Fact
One row per valid `MDR_REPORT_KEY`.

### Device Fact
One row per valid device-event record. Multiple device records may relate to one report.

## Core Model

```text
DIM_DATE
DIM_PRODUCT
DIM_EVENT_TYPE
DIM_PROBLEM_CODE
       |
       v
FACT_MAUDE_REPORT ---- FACT_MAUDE_DEVICE
```

## Critical Rule

Never calculate distinct report KPIs by counting device rows. Report-level metrics use `DISTINCTCOUNT(MDR_REPORT_KEY)` or an equivalent report-grain aggregation.

## Synthetic Layer

Synthetic workflow entities are separate from the FDA-derived facts:

```text
SYNTHETIC_INVESTIGATION
        |
        v
SYNTHETIC_FINDING
        |
        v
SYNTHETIC_CAPA
        |
        v
SYNTHETIC_EFFECTIVENESS_CHECK
```
