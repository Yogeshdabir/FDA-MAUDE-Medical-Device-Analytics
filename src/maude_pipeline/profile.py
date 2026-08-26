from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _pct(n: int, d: int) -> float:
    return round((n / d * 100), 4) if d else 0.0


def profile_csv(path: str | Path, delimiter: str = "|") -> dict[str, Any]:
    """Stream a delimited file and return a compact quality profile."""
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        reader = csv.reader(fh, delimiter=delimiter)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"Empty file: {path}")
        header = [h.strip() for h in header]
        counts = Counter()
        missing = Counter()
        distinct_keys: set[str] = set()
        duplicate_keys = 0
        key_idx = next((i for i, h in enumerate(header) if h.casefold() == "mdr_report_key"), None)
        rows = 0
        malformed = 0
        field_counts = Counter()

        for row in reader:
            rows += 1
            field_counts[len(row)] += 1
            if len(row) != len(header):
                malformed += 1
            for i, value in enumerate(row[: len(header)]):
                if not value.strip():
                    missing[header[i]] += 1
            if key_idx is not None and key_idx < len(row):
                key = row[key_idx].strip()
                if key:
                    if key in distinct_keys:
                        duplicate_keys += 1
                    else:
                        distinct_keys.add(key)
        return {
            "file": str(path),
            "rows": rows,
            "columns": len(header),
            "header": header,
            "field_count_distribution": dict(field_counts),
            "malformed_rows": malformed,
            "distinct_mdr_report_keys": len(distinct_keys),
            "duplicate_mdr_report_key_rows": duplicate_keys,
            "missingness": {
                field: {"count": n, "percent": _pct(n, rows)}
                for field, n in sorted(missing.items())
            },
        }


def write_profile(profile: dict[str, Any], output: str | Path) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(profile, indent=2), encoding="utf-8")
