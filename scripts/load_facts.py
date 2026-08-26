from __future__ import annotations

import argparse
import csv
import io
import zipfile
from datetime import datetime
from pathlib import Path

import psycopg

BASE_FIELDS = [
    "MDR_REPORT_KEY", "EVENT_KEY", "REPORT_NUMBER", "REPORT_SOURCE_CODE",
    "NUMBER_DEVICES_IN_EVENT", "NUMBER_PATIENTS_IN_EVENT", "DATE_RECEIVED",
    "ADVERSE_EVENT_FLAG", "PRODUCT_PROBLEM_FLAG", "DATE_REPORT", "DATE_OF_EVENT",
    "EVENT_TYPE", "MFR_REPORT_TYPE", "MANUFACTURER_NAME", "TYPE_OF_REPORT",
    "SOURCE_TYPE", "DATE_ADDED", "DATE_CHANGED", "REPORTER_STATE_CODE",
    "REPORTER_COUNTRY_CODE", "PMA_PMN_NUM", "SUMMARY_REPORT",
]
DEVICE_FIELDS = [
    "MDR_REPORT_KEY", "DEVICE_EVENT_KEY", "DEVICE_SEQUENCE_NO", "IMPLANT_FLAG",
    "DATE_REMOVED_FLAG", "IMPLANT_DATE_YEAR", "DATE_REMOVED_YEAR",
    "SERVICED_BY_3RD_PARTY_FLAG", "DATE_RECEIVED", "BRAND_NAME", "GENERIC_NAME",
    "MANUFACTURER_D_NAME", "MODEL_NUMBER", "CATALOG_NUMBER", "LOT_NUMBER",
    "OTHER_ID_NUMBER", "DEVICE_AVAILABILITY", "DATE_RETURNED_TO_MANUFACTURER",
    "DEVICE_REPORT_PRODUCT_CODE", "DEVICE_AGE_TEXT", "DEVICE_EVALUATED_BY_MANUFACTUR",
    "COMBINATION_PRODUCT_FLAG", "UDI-DI", "UDI-PUBLIC",
]


def open_source(path: Path, member: str):
    if path.suffix.lower() != ".zip":
        return path.open("r", encoding="utf-8-sig", errors="replace", newline=""), None
    archive = zipfile.ZipFile(path)
    return io.TextIOWrapper(archive.open(member), encoding="utf-8-sig", errors="replace", newline=""), archive


def date_value(value: str, formats: tuple[str, ...]) -> str:
    value = value.strip()
    if not value:
        return ""
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def integer_value(value: str) -> str:
    value = value.strip()
    try:
        return str(int(value)) if value else ""
    except ValueError:
        return ""


def copy_csv(cur, table: str, columns: list[str], rows):
    """COPY transformed rows to PostgreSQL in bounded memory."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    count = 0

    def flush():
        nonlocal buf, writer
        if buf.tell() == 0:
            return
        buf.seek(0)
        with cur.copy(f"COPY {table} ({', '.join(columns)}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)") as copy:
            copy.write(buf.read())
        buf = io.StringIO()
        writer = csv.writer(buf)

    for row in rows:
        writer.writerow(row)
        count += 1
        if buf.tell() >= 1024 * 1024:
            flush()
    flush()
    return count


def load_base(source: Path):
    fh, archive = open_source(source, "mdrfoi.txt")
    try:
        reader = csv.DictReader(fh, delimiter="|")
        for r in reader:
            yield [
                r["MDR_REPORT_KEY"].strip(), r["EVENT_KEY"].strip(), r["REPORT_NUMBER"].strip(),
                r["REPORT_SOURCE_CODE"].strip(), integer_value(r["NUMBER_DEVICES_IN_EVENT"]),
                integer_value(r["NUMBER_PATIENTS_IN_EVENT"]), date_value(r["DATE_RECEIVED"], ("%m/%d/%Y",)),
                r["ADVERSE_EVENT_FLAG"].strip(), r["PRODUCT_PROBLEM_FLAG"].strip(),
                date_value(r["DATE_REPORT"], ("%m/%d/%Y",)), date_value(r["DATE_OF_EVENT"], ("%m/%d/%Y",)),
                r["EVENT_TYPE"].strip(), r["MFR_REPORT_TYPE"].strip(), r["MANUFACTURER_NAME"].strip(),
                r["TYPE_OF_REPORT"].strip(), r["SOURCE_TYPE"].strip(), date_value(r["DATE_ADDED"], ("%m/%d/%Y",)),
                date_value(r["DATE_CHANGED"], ("%m/%d/%Y",)), r["REPORTER_STATE_CODE"].strip(),
                r["REPORTER_COUNTRY_CODE"].strip(), r["PMA_PMN_NUM"].strip(), r["SUMMARY_REPORT"].strip(),
            ]
    finally:
        fh.close()
        if archive: archive.close()


def load_device(source: Path):
    fh, archive = open_source(source, "DEVICE.txt")
    try:
        reader = csv.DictReader(fh, delimiter="|")
        for r in reader:
            yield [
                r["MDR_REPORT_KEY"].strip(), r["DEVICE_EVENT_KEY"].strip(), integer_value(r["DEVICE_SEQUENCE_NO"]),
                r["IMPLANT_FLAG"].strip(), r["DATE_REMOVED_FLAG"].strip(), integer_value(r["IMPLANT_DATE_YEAR"]),
                integer_value(r["DATE_REMOVED_YEAR"]), r["SERVICED_BY_3RD_PARTY_FLAG"].strip(),
                date_value(r["DATE_RECEIVED"], ("%Y/%m/%d", "%m/%d/%Y")), r["BRAND_NAME"].strip(),
                r["GENERIC_NAME"].strip(), r["MANUFACTURER_D_NAME"].strip(), r["MODEL_NUMBER"].strip(),
                r["CATALOG_NUMBER"].strip(), r["LOT_NUMBER"].strip(), r["OTHER_ID_NUMBER"].strip(),
                r["DEVICE_AVAILABILITY"].strip(), date_value(r["DATE_RETURNED_TO_MANUFACTURER"], ("%Y/%m/%d", "%m/%d/%Y")),
                r["DEVICE_REPORT_PRODUCT_CODE"].strip(), r["DEVICE_AGE_TEXT"].strip(),
                r["DEVICE_EVALUATED_BY_MANUFACTUR"].strip(), r["COMBINATION_PRODUCT_FLAG"].strip(),
                r["UDI-DI"].strip(), r["UDI-PUBLIC"].strip(),
            ]
    finally:
        fh.close()
        if archive: archive.close()


def main() -> int:
    p = argparse.ArgumentParser(description="Load verified MAUDE source fields into PostgreSQL")
    p.add_argument("--base", required=True, type=Path)
    p.add_argument("--device", required=True, type=Path)
    p.add_argument("--conninfo", default="postgresql://maude:maude_local_password@localhost:5432/maude_pms_analytics")
    args = p.parse_args()

    with psycopg.connect(args.conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE fact.maude_device, fact.maude_report")
            cur.execute("CREATE TEMP TABLE stg_report AS SELECT * FROM fact.maude_report WITH NO DATA")
            cur.execute("CREATE TEMP TABLE stg_device AS SELECT * FROM fact.maude_device WITH NO DATA")

            copy_csv(cur, "stg_report", BASE_FIELDS, load_base(args.base))
            cur.execute("SELECT COUNT(*) FROM stg_report")
            base_count = cur.fetchone()[0]
            cur.execute("SELECT mdr_report_key FROM stg_report GROUP BY 1 HAVING COUNT(*) > 1 LIMIT 1")
            if cur.fetchone():
                raise RuntimeError("Duplicate MDR_REPORT_KEY detected in staging")
            cur.execute("INSERT INTO fact.maude_report SELECT * FROM stg_report")

            copy_csv(cur, "stg_device", DEVICE_FIELDS, load_device(args.device))
            cur.execute("SELECT COUNT(*) FROM stg_device")
            device_count = cur.fetchone()[0]
            cur.execute("SELECT device_event_key FROM stg_device GROUP BY 1 HAVING COUNT(*) > 1 LIMIT 1")
            if cur.fetchone():
                raise RuntimeError("Duplicate DEVICE_EVENT_KEY detected in staging")
            cur.execute("SELECT COUNT(*) FROM stg_device d LEFT JOIN fact.maude_report r USING (mdr_report_key) WHERE r.mdr_report_key IS NULL")
            orphan_count = cur.fetchone()[0]
            cur.execute("INSERT INTO fact.maude_device SELECT * FROM stg_device WHERE mdr_report_key IN (SELECT mdr_report_key FROM fact.maude_report)")

        conn.commit()

    print(f"Loaded reports: {base_count:,}")
    print(f"Loaded device rows: {device_count:,}")
    print(f"Orphan device rows excluded from fact load: {orphan_count:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
