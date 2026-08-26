from __future__ import annotations

import csv
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


def _open_text(path: Path) -> tuple[TextIO, object]:
    if path.suffix.lower() == ".zip":
        archive = zipfile.ZipFile(path)
        names = [n for n in archive.namelist() if not n.endswith("/")]
        if not names:
            archive.close()
            raise ValueError(f"ZIP contains no files: {path}")
        member = names[0]
        return (  # type: ignore[return-value]
            __import__("io").TextIOWrapper(archive.open(member), encoding="utf-8-sig", errors="replace", newline=""),
            archive,
        )
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
    """Stream a MAUDE-style delimited file, preserving malformed rows in quarantine."""
    source_path = Path(source)
    output_path = Path(output_file)
    quarantine_path = Path(quarantine_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)

    fh, archive = _open_text(source_path)
    try:
        reader = csv.reader(fh, delimiter=delimiter)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"Source file is empty: {source_path}")
        header = [h.strip() for h in header]
        key_indices = [i for i, h in enumerate(header) if h.casefold() == key_column.casefold()]
        key_idx = key_indices[0] if key_indices else None
        expected = expected_fields if expected_fields is not None else len(header)

        with output_path.open("w", encoding="utf-8", newline="") as good_fh, \
             quarantine_path.open("w", encoding="utf-8", newline="") as bad_fh:
            good_writer = csv.writer(good_fh, delimiter=delimiter)
            bad_writer = csv.writer(bad_fh, delimiter=",")
            good_writer.writerow(header)
            bad_writer.writerow(["source_row_number", "field_count", "dq_reason", "raw_record"])

            rows = valid = malformed = missing_key = 0
            for row_number, row in enumerate(reader, start=2):
                if max_rows is not None and rows >= max_rows:
                    break
                rows += 1
                raw_record = delimiter.join(row)
                reasons: list[str] = []
                if len(row) != expected:
                    reasons.append(f"FIELD_COUNT_{len(row)}_EXPECTED_{expected}")
                    malformed += 1
                if key_idx is None or key_idx >= len(row) or not row[key_idx].strip():
                    reasons.append("MISSING_MDR_REPORT_KEY")
                    missing_key += 1
                if reasons:
                    bad_writer.writerow([row_number, len(row), ";".join(reasons), raw_record])
                    continue
                good_writer.writerow([v.strip() for v in row])
                valid += 1

    finally:
        fh.close()
        if archive is not None:
            archive.close()  # type: ignore[attr-defined]

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
    Path(output).write_text(
        json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8"
    )
