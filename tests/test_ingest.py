from pathlib import Path

from src.maude_pipeline.ingest import stream_delimited


def test_stream_ingest_quarantines_bad_rows(tmp_path: Path):
    source = tmp_path / "source.txt"
    source.write_text(
        "MDR_REPORT_KEY|A|B\n"
        "R1|x|y\n"
        "|x|y\n"
        "R2|x\n",
        encoding="utf-8",
    )
    clean = tmp_path / "clean.csv"
    quarantine = tmp_path / "quarantine.csv"

    result = stream_delimited(source, clean, quarantine)

    assert result.rows_read == 3
    assert result.valid_rows == 1
    assert result.malformed_rows == 1
    assert result.missing_key_rows == 1
    assert "R1|x|y" in clean.read_text(encoding="utf-8")
    q = quarantine.read_text(encoding="utf-8")
    assert "MISSING_MDR_REPORT_KEY" in q
    assert "FIELD_COUNT_2_EXPECTED_3" in q
