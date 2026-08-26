CREATE TABLE IF NOT EXISTS dq.pipeline_run (
    run_id BIGSERIAL PRIMARY KEY,
    run_started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source_base_rows BIGINT,
    source_device_rows BIGINT,
    loaded_report_rows BIGINT,
    loaded_device_rows BIGINT,
    malformed_base_rows BIGINT DEFAULT 0,
    malformed_device_rows BIGINT DEFAULT 0,
    duplicate_report_keys BIGINT DEFAULT 0,
    duplicate_device_keys BIGINT DEFAULT 0,
    orphan_device_rows BIGINT DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'RUNNING'
);

CREATE OR REPLACE VIEW analytical.dq_reconciliation AS
SELECT
    (SELECT COUNT(*) FROM fact.maude_report) AS loaded_report_rows,
    (SELECT COUNT(DISTINCT mdr_report_key) FROM fact.maude_report) AS distinct_report_keys,
    (SELECT COUNT(*) FROM fact.maude_device) AS loaded_device_rows,
    (SELECT COUNT(DISTINCT device_event_key) FROM fact.maude_device) AS distinct_device_keys,
    (SELECT COUNT(*) FROM fact.maude_device d LEFT JOIN fact.maude_report r USING (mdr_report_key)
        WHERE r.mdr_report_key IS NULL) AS orphan_device_rows,
    (SELECT COUNT(*) FROM fact.maude_report WHERE mdr_report_key IS NULL OR btrim(mdr_report_key) = '') AS missing_report_keys,
    (SELECT COUNT(*) FROM fact.maude_device WHERE device_event_key IS NULL OR btrim(device_event_key) = '') AS missing_device_keys;

CREATE OR REPLACE VIEW analytical.dq_status AS
SELECT
    *,
    CASE
        WHEN loaded_report_rows = distinct_report_keys
         AND loaded_device_rows = distinct_device_keys
         AND orphan_device_rows = 0
         AND missing_report_keys = 0
         AND missing_device_keys = 0
        THEN 'PASS'
        ELSE 'REVIEW'
    END AS reconciliation_status
FROM analytical.dq_reconciliation;
