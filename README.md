# FDA MAUDE Medical Device Event Intelligence & Quality Analytics

## Overview

An end-to-end MedTech analytics portfolio project built around public FDA MAUDE reporting data. The project demonstrates business analysis, Python ETL, data-quality controls, PostgreSQL/SQL analytics, Power BI reporting, testing/UAT, and a clearly separated synthetic investigation/CAPA workflow.

> **Important:** This repository is a portfolio/demo project. MAUDE reporting data does not by itself establish incidence, prevalence, failure rates, comparative safety, or causality. Investigation, root-cause, CAPA, and effectiveness information in the synthetic workflow is fictional and is not FDA-sourced.

## Business Problem

Public post-market reporting data is large, distributed across related files, and contains structural and completeness issues. The objective is to create a transparent and reproducible analytical workflow that preserves data grain, exposes data-quality limitations, and helps stakeholders understand reporting patterns without overstating what the data can prove.

## Objectives

- Validate source structure and data quality before analysis.
- Preserve separate report-level and device-level analytical grains.
- Build reproducible SQL analytics and Power BI measures.
- Reconcile core KPIs between source/SQL reference calculations and BI outputs.
- Present reporting patterns as review candidates rather than automatic safety conclusions.
- Demonstrate a separate synthetic quality workflow from review candidate through investigation, CAPA, and effectiveness check.
- Maintain requirements traceability, testing, UAT, and validation evidence.

## Architecture

```text
FDA MAUDE files
      |
      v
Python ingestion + validation
      |
      +--> quarantine / DQ evidence
      |
      v
clean analytical data
      |
      v
PostgreSQL
  |             |
  v             v
Report Fact   Device Fact
  \             /
   \           /
    v         v
      Dimensions
          |
          v
   Analytical SQL views
          |
          v
       Power BI
          |
          +--> Executive Overview
          +--> Device/Product Analysis
          +--> Event/Reporting Patterns
          +--> Data Quality
          +--> Methodology & Limitations

Synthetic workflow (separate)
Pattern -> Review -> Investigation -> CAPA -> Effectiveness
```

## Project Phases

1. Source assessment and baseline
2. Business requirements and user stories
3. Process and workflow design
4. Data dictionary and data model
5. Data-quality framework
6. Python ETL and validation
7. SQL analytics and Power BI model
8. Synthetic quality workflow
9. Testing, reconciliation, and UAT
10. Portfolio presentation and release package

## Technology Stack

| Layer | Technology |
|---|---|
| Source | FDA MAUDE |
| ETL | Python / pandas |
| Database | PostgreSQL |
| Analytics | SQL |
| BI | Power BI / DAX |
| Testing | Python, SQL, Power BI validation, UAT |
| Documentation | Markdown |
| Version control | Git / GitHub |

## Repository Structure

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
```

## Validation Principles

Core validation controls include:

- report-key uniqueness
- device-key uniqueness
- Base/Device orphan reconciliation
- report-vs-device grain protection
- monthly trend reconciliation
- event/product aggregation reconciliation
- DAX-to-SQL KPI reconciliation
- Power BI filter and relationship testing
- synthetic-data isolation testing
- UAT and requirements traceability

## Synthetic Data Boundary

Synthetic investigation, root-cause, CAPA, and effectiveness records are stored separately and must be marked as synthetic. They cannot modify or overwrite FDA source-derived facts or MAUDE analytical counts.

## Limitations

MAUDE is a passive reporting system. Reports may be incomplete, inaccurate, duplicated, or submitted for different purposes. Report counts are not exposure-adjusted rates and do not independently establish device causality or comparative safety. This project therefore presents reporting patterns and data-quality indicators rather than confirmed safety conclusions.

## Reproducibility

The implementation will document source snapshot/date, transformation rules, schema assumptions, validation checks, model grain, and version history. Raw FDA data should be downloaded separately from the official source and should not be committed to this repository unless licensing/size considerations permit it.

## Portfolio Positioning

This project demonstrates the combination of:

**MedTech/PMS domain knowledge + Business Analysis + Data Engineering + SQL + Power BI + Data Quality + Validation/UAT.**

## Status

**Portfolio foundation initialized.** Implementation artifacts, source-specific extracts, executable ETL, SQL deployment scripts, Power BI files, and validation evidence will be added as they are built and verified.
