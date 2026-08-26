from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FileValidation:
    file: str
    rows: int
    expected_fields: int | None
    malformed_rows: int
    missing_key_rows: int

    def to_dict(self):
        return asdict(self)


_KEY_ALIASES = {
    "mdr_report_key",
    "mdr report key",
    "mdr-report-key",
}


def _find_key_index(header: list[str], aliases: set[str] = _KEY_ALIASES) -> int | None:
    normalized = {alias.casefold().strip().replace("_", " ").replace("-", " ") for alias in aliases}
    for i, value in enumerate(header):
        candidate = value.casefold().strip().replace("_", " ").replace("-", " ")
        if candidate in normalized:
            return i
    return None


def validate_delimited_file(path: str | Path, expected_fields: int | None = None,
                            key_column: str | None = "MDR_REPORT_KEY", delimiter: str = "|") -> FileValidation:
    path = Path(path)
    rows = malformed = missing_key = 0
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as fh:
        reader = csv.reader(fh, delimiter=delimiter)
        try:
            header = [h.strip() for h in next(reader)]
        except StopIteration:
            return FileValidation(path.name, 0, expected_fields, 0, 0)
        key_idx = _find_key_index(header) if key_column else None
        for row in reader:
            rows += 1
            if expected_fields is not None and len(row) != expected_fields:
                malformed += 1
            if key_idx is not None and (key_idx >= len(row) or not row[key_idx].strip()):
                missing_key += 1
    return FileValidation(path.name, rows, expected_fields, malformed, missing_key)
