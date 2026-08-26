from pathlib import Path

from src.maude_pipeline.validator import validate_delimited_file


def test_valid_file(tmp_path: Path):
    p = tmp_path / "base.txt"
    p.write_text("MDR_REPORT_KEY|A|B\nR1|x|y\nR2|x|y\n", encoding="utf-8")
    result = validate_delimited_file(p, expected_fields=3, key_column="MDR_REPORT_KEY")
    assert result.rows == 2
    assert result.malformed_rows == 0
    assert result.missing_key_rows == 0


def test_malformed_and_missing_key(tmp_path: Path):
    p = tmp_path / "device.txt"
    p.write_text("MDR_REPORT_KEY|A|B\nR1|x|y\n|x\n", encoding="utf-8")
    result = validate_delimited_file(p, expected_fields=3, key_column="MDR_REPORT_KEY")
    assert result.rows == 2
    assert result.malformed_rows == 1
    assert result.missing_key_rows == 1
