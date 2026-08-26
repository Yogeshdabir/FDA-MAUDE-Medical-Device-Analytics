# Synthetic Quality Workflow

> **DEMONSTRATION DATA:** Investigation, root cause, CAPA and effectiveness information in this workflow is fictional and is not FDA-sourced.

## Workflow

```text
MAUDE reporting pattern
        |
        v
Review candidate
        |
        v
Synthetic investigation
        |
        v
Synthetic finding / root-cause category
        |
        v
Synthetic CAPA
        |
        v
Synthetic effectiveness check
```

## Rules

- Synthetic records must carry `synthetic_flag = TRUE`.
- Synthetic workflow data must remain in separate tables/schema.
- Synthetic conclusions cannot modify FDA-derived facts or KPIs.
- A reporting increase is a review candidate, not an automatic safety conclusion.
- Root cause may remain unknown.
