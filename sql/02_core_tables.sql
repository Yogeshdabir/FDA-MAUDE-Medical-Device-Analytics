CREATE TABLE IF NOT EXISTS fact.maude_report (
    mdr_report_key TEXT PRIMARY KEY,
    event_type TEXT,
    report_date DATE,
    date_received DATE,
    manufacturer_name TEXT,
    product_code TEXT,
    source_file TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact.maude_device (
    device_event_key TEXT PRIMARY KEY,
    mdr_report_key TEXT NOT NULL,
    device_sequence INTEGER,
    brand_name TEXT,
    generic_name TEXT,
    manufacturer_d_name TEXT,
    model_number TEXT,
    catalog_number TEXT,
    lot_number TEXT,
    serial_number TEXT,
    source_file TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_device_report FOREIGN KEY (mdr_report_key)
        REFERENCES fact.maude_report (mdr_report_key)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS ix_device_report_key ON fact.maude_device(mdr_report_key);
CREATE INDEX IF NOT EXISTS ix_report_product_code ON fact.maude_report(product_code);
CREATE INDEX IF NOT EXISTS ix_report_date_received ON fact.maude_report(date_received);
