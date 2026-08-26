CREATE OR REPLACE VIEW analytical.monthly_report_trend AS
SELECT
    date_trunc('month', date_received)::date AS report_month,
    COUNT(*) AS report_count,
    COUNT(DISTINCT mdr_report_key) AS distinct_report_count
FROM fact.maude_report
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW analytical.product_report_summary AS
SELECT
    product_code,
    COUNT(*) AS report_count,
    COUNT(DISTINCT mdr_report_key) AS distinct_report_count
FROM fact.maude_report
GROUP BY product_code;

CREATE OR REPLACE VIEW analytical.device_report_reconciliation AS
SELECT
    r.mdr_report_key,
    COUNT(d.device_event_key) AS device_count
FROM fact.maude_report r
LEFT JOIN fact.maude_device d USING (mdr_report_key)
GROUP BY r.mdr_report_key;

CREATE OR REPLACE VIEW analytical.data_quality_summary AS
SELECT
    (SELECT COUNT(*) FROM fact.maude_report) AS report_rows,
    (SELECT COUNT(DISTINCT mdr_report_key) FROM fact.maude_report) AS distinct_reports,
    (SELECT COUNT(*) FROM fact.maude_device) AS device_rows,
    (SELECT COUNT(DISTINCT device_event_key) FROM fact.maude_device) AS distinct_devices,
    (SELECT COUNT(*) FROM fact.maude_device d LEFT JOIN fact.maude_report r USING (mdr_report_key) WHERE r.mdr_report_key IS NULL) AS orphan_devices;
