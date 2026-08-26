from __future__ import annotations

import argparse
import csv
from pathlib import Path

import psycopg
from psycopg import sql


def load_csv(conninfo: str, csv_path: str | Path, schema: str, table: str, delimiter: str = "|") -> int:
    csv_path = Path(csv_path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh, delimiter=delimiter)
        header = next(reader)
        columns = [c.strip() for c in header]

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(schema)))
            cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
                    sql.Identifier(schema),
                    sql.Identifier(table),
                    sql.SQL(", ").join(
                        sql.SQL("{} TEXT").format(sql.Identifier(c)) for c in columns
                    ),
                )
            )
            conn.commit()
            with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
                with cur.copy(
                    sql.SQL("COPY {}.{} ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER {})").format(
                        sql.Identifier(schema),
                        sql.Identifier(table),
                        sql.SQL(", ").join(sql.Identifier(c) for c in columns),
                        sql.Literal(delimiter),
                    )
                ) as copy:
                    while chunk := fh.read(1024 * 1024):
                        copy.write(chunk)
            conn.commit()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Load cleaned MAUDE CSV into PostgreSQL")
    parser.add_argument("--conninfo", required=True)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--schema", default="raw")
    parser.add_argument("--table", required=True)
    parser.add_argument("--delimiter", default="|")
    args = parser.parse_args()
    load_csv(args.conninfo, args.file, args.schema, args.table, args.delimiter)
    print(f"Loaded {args.file} into {args.schema}.{args.table}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
