# Run the local Phase 1 validator

## 1. Clone
```bash
git clone https://github.com/Yogeshdabir/FDA-MAUDE-Medical-Device-Analytics.git
cd FDA-MAUDE-Medical-Device-Analytics
```

## 2. Create environment
Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run tests
```bash
pytest -q
```

## 5. Run the sample validator
The sample intentionally contains one missing key and one malformed row.
```bash
python -m src.maude_pipeline --base data/sample/base_sample.txt --output outputs/sample_validation.json
```

Expected result includes:
- rows: 4
- malformed_rows: 1
- missing_key_rows: 1

## 6. Run against your MAUDE files
```bash
python -m src.maude_pipeline --base /path/to/base_file.txt --device /path/to/device_file.txt --output outputs/validation_summary.json
```

The current Phase 1 CLI validates delimited-file structure and key completeness. It does not yet download MAUDE data, load PostgreSQL, or generate the Power BI dashboard; those are subsequent implementation steps.
