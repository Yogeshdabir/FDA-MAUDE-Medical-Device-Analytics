CREATE TABLE IF NOT EXISTS fact.maude_report (
    mdr_report_key TEXT PRIMARY KEY,
    event_key TEXT,
    report_number TEXT,
    report_source_code TEXT,
    number_devices_in_event INTEGER,
    number_patients_in_event INTEGER,
    date_received DATE,
    adverse_event_flag TEXT,
    product_problem_flag TEXT,
    date_report DATE,
    date_of_event DATE,
    event_type TEXT,
    mfr_report_type TEXT,
    manufacturer_name TEXT,
    type_of_report TEXT,
    source_type TEXT,
    date_added DATE,
    date_changed DATE,
    reporter_state_code TEXT,
    reporter_country_code TEXT,
    pma_pmn_num TEXT,
    summary_report TEXT,
    source_file TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact.maude_device (
    mdr_report_key TEXT NOT NULL,
    device_event_key TEXT PRIMARY KEY,
    device_sequence_no INTEGER,
    implant_flag TEXT,
    date_removed_flag TEXT,
    implant_date_year INTEGER,
    date_removed_year INTEGER,
    serviced_by_3rd_party_flag TEXT,
    date_received DATE,
    brand_name TEXT,
    generic_name TEXT,
    manufacturer_d_name TEXT,
    model_number TEXT,
    catalog_number TEXT,
    lot_number TEXT,
    other_id_number TEXT,
    device_availability TEXT,
    date_returned_to_manufacturer DATE,
    device_report_product_code TEXT,
    device_age_text TEXT,
    device_evaluated_by_manufactur TEXT,
    combination_product_flag TEXT,
    udi_di TEXT,
    udi_public TEXT,
    source_file TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_device_report FOREIGN KEY (mdr_report_key)
        REFERENCES fact.maude_report (mdr_report_key)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS ix_device_report_key ON fact.maude_device(mdr_report_key);
CREATE INDEX IF NOT EXISTS ix_device_product_code ON fact.maude_device(device_report_product_code);
CREATE INDEX IF NOT EXISTS ix_report_product_code ON fact.maude_report(pma_pmn_num);
CREATE INDEX IF NOT EXISTS ix_report_date_received ON fact.maude_report(date_received);
