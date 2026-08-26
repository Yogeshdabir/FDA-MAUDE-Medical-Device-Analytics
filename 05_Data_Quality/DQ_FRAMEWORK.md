# Data Quality Framework

## Dimensions

- Completeness
- Validity
- Uniqueness
- Consistency
- Referential integrity
- Timeliness
- Traceability

## Core Checks

1. Expected source schema.
2. Required report keys.
3. Report-key uniqueness at report grain.
4. Device-key uniqueness at device grain.
5. Base/Device orphan reconciliation.
6. Date validity and chronology.
7. Product-code completeness.
8. Lookup/reference mapping coverage.
9. Quarantine counts.
10. Source-to-model reconciliation.

## Quarantine Principle

Malformed records are retained in a quarantine population with reason codes rather than silently dropped.
