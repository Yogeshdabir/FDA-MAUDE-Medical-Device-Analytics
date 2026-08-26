from __future__ import annotations

import csv
import io
import json
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, TextIO


@dataclass
class IngestResult:
    source: str
    header_fields: int
    rows_read: int
    valid_rows: int
    malformed_rows: int
    missing_key_rows: int
    output_file: str | None
    quarantine_file: str | None


_KEY_ALIASES = {"mdr_report_key", "mdr report key", "mdr-report-key"}


def _normalize_header(value: str) -> str:
    return value.casefold().strip().replace("_", " ").replace("-", " ")


def _find_key_index(header: list[str], key_column: str) -> int | None:
    target = _normalize_header(key_column)
    if target in {_normalize_header(x) for x in _KEY_ALIASES}:
        target = "mdr report key"
    for i, value in enumerate(header):
        if _normalize_header(value) == target:
            return i
    return None


def _open_text(path: Path) -> tuple[TextIO, zipfile.ZipFile | None]:
    if path.suffix.lower() == ".zip":
        archive = zipfile.ZipFile(path)
        names = [n for n in archive.namelist() if not n.endswith("/")]
        if not names:
            archive.close()
            raise ValueError(f"ZIP contains no files: {path}")
        member = names[0]
        return io.TextIOWrapper(
            archive.open(member), encoding="utf-8-sig", errors="replace", newline=""
        ), archive
    return path.open("r", encoding="utf-8-sig", errors="replace", newline=""), None


def stream_delimited(
    source: str | Path,
    output_file: str | Path,
    quarantine_file: str | Path,
    expected_fields: int | None = None,
    key_column: str = "MDR_REPORT_KEY",
    delimiter: str = "|",
    max_rows: int | None = None,
) -> IngestResult:
    """Stream a MAUDE-style delimited file while preserving rejected rows."""
    source_path = Path(source)
    output_path = Path(output_file)
    quarantine_path = Path(quarantine_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)

    fh, archive = _open_text(source_path)
    rows = valid = malformed = missing_key = 0
    header: list[str] = []
    try:
        reader = csv.reader(fh, delimiter=delimiter)
        first = next(reader, None)
        if first is None:
            raise ValueError(f"Source file is empty: {source_path}")
        header = [h.strip() for h in first]
        expected = expected_fields if expected_fields is not None else len(header)
        key_idx = _find_key_index(header, key_column)

        with output_path.open("w", encoding="utf-8", newline="") as good_fh, \
             quarantine_path.open("w", encoding="utf-8", newline="") as bad_fh:
            good_writer = csv.writer(good_fh, delimiter=delimiter)
            bad_writer = csv.writer(bad_fh)
            good_writer.writerow(header)
            bad_writer.writerow(["source_row_number", "field_count", "dq_reason", "raw_record"])

            for row_number, row in enumerate(reader, start=2):
                if max_rows is not None and rows >= max_rows:
                    break
                rows += 1
                reasons: list[str] = []
                if len(row) != expected:
                    reasons.append(f"FIELD_COUNT_{len(row)}_EXPECTED_{expected}")
                if key_idx is None:
                    reasons.append("MDR_REPORT_KEY_COLUMN_NOT_FOUND")
                elif key_idx >= len(row) or not row[key_idx].strip():
                    reasons.append("MISSING_MDR_REPORT_KEY")

                if any(r.startswith("FIELD_COUNT_") for r in reasons):
                    malformed += 1
                if "MISSING_MDR_REPORT_KEY" in reasons:
                    missing_key += 1
                if reasons:
                    bad_writer.writerow([row_number, len(row), ";".join(reasons), delimiter.join(row)])
                else:
                    good_writer.writerow([value.strip() for value in row])
                    valid += 1
    finally:
        fh.close()
        if archive is not None:
            archive.close()

    return IngestResult(
        source=str(source_path),
        header_fields=len(header),
        rows_read=rows,
        valid_rows=valid,
        malformed_rows=malformed,
        missing_key_rows=missing_key,
        output_file=str(output_path),
        quarantine_file=str(quarantine_path),
    )


def write_manifest(results: Iterable[IngestResult], output: str | Path) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
