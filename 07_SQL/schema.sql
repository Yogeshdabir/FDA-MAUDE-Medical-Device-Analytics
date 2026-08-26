CREATE SCHEMA IF NOT EXISTS clean;
CREATE SCHEMA IF NOT EXISTS fact;
CREATE SCHEMA IF NOT EXISTS dim;
CREATE SCHEMA IF NOT EXISTS analytical;
CREATE SCHEMA IF NOT EXISTS synthetic;

-- Report grain: one row per valid MDR report.
CREATE TABLE IF NOT EXISTS fact.fact_maude_report (
    mdr_report_key TEXT PRIMARY KEY,
    date_received DATE,
    date_of_event DATE,
    event_type TEXT,
    adverse_event_flag TEXT,
    product_problem_flag TEXT,
    report_source TEXT
);

-- Device grain: potentially many device records per report.
CREATE TABLE IF NOT EXISTS fact.fact_maude_device (
    device_event_key TEXT PRIMARY KEY,
    mdr_report_key TEXT NOT NULL,
    device_report_product_code TEXT,
    brand_name TEXT,
    generic_name TEXT,
    manufacturer_d_name TEXT,
    model_number TEXT,
    FOREIGN KEY (mdr_report_key)
        REFERENCES fact.fact_maude_report(mdr_report_key)
);

CREATE TABLE IF NOT EXISTS dim.dim_date (
    date_key DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER
);

CREATE TABLE IF NOT EXISTS dim.dim_product (
    product_code TEXT PRIMARY KEY,
    product_category TEXT,
    product_name TEXT
);

CREATE TABLE IF NOT EXISTS dim.dim_problem_code (
    fda_code TEXT PRIMARY KEY,
    problem_description TEXT
);

-- Synthetic quality workflow is deliberately isolated from FDA-derived facts.
CREATE TABLE IF NOT EXISTS synthetic.investigation (
    investigation_id BIGSERIAL PRIMARY KEY,
    mdr_report_key TEXT,
    investigation_status TEXT NOT NULL,
    review_trigger TEXT,
    priority TEXT,
    risk_category TEXT,
    synthetic_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS synthetic.capa (
    capa_id BIGSERIAL PRIMARY KEY,
    investigation_id BIGINT NOT NULL REFERENCES synthetic.investigation(investigation_id),
    capa_type TEXT,
    action_description TEXT,
    owner_role TEXT,
    priority TEXT,
    capa_status TEXT,
    effectiveness_required BOOLEAN,
    synthetic_flag BOOLEAN NOT NULL DEFAULT TRUE
);
