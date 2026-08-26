# Testing and UAT Plan

## Test Layers

1. Source/schema validation
2. ETL/transformation tests
3. Data-quality tests
4. SQL aggregation tests
5. Data-model/key/cardinality tests
6. DAX/Power BI measure reconciliation
7. Dashboard filter and drill-through tests
8. Synthetic workflow isolation tests
9. User acceptance testing
10. Regression testing

## Critical Controls

- Source report count reconciles to report fact.
- Source device count reconciles to device fact, subject to documented quarantine rules.
- Report count remains unchanged when a report has multiple device rows.
- Monthly trends reconcile to independent SQL calculations.
- Product and event distributions reconcile to reference queries.
- Synthetic records cannot change FDA-derived KPIs.

## UAT Personas

### Quality Manager
Identify reporting patterns and review candidates.

### Product Quality Analyst
Investigate a product/event combination without double-counting reports.

### Data Steward
Review completeness, malformed records, orphan relationships, and reconciliation.

## Release Gate

Release only when critical defects are zero, core KPI reconciliation passes, data-model tests pass, limitations are visible, and UAT is accepted.
