from __future__ import annotations

import argparse
import os
from pathlib import Path

from sqlalchemy import create_engine, text


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply MAUDE PostgreSQL schemas and analytical views")
    parser.add_argument("--sql-dir", default="sql")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL", "postgresql+psycopg://maude:maude_local_password@localhost:5432/maude_pms_analytics"))
    args = parser.parse_args()

    engine = create_engine(args.database_url)
    for filename in ["01_create_schemas.sql", "02_core_tables.sql", "03_analytical_views.sql"]:
        sql = Path(args.sql_dir, filename).read_text(encoding="utf-8")
        with engine.begin() as conn:
            conn.execute(text(sql))
        print(f"Applied {filename}")
    print("PostgreSQL schema deployment complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
