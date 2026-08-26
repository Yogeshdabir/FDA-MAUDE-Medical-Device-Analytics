from __future__ import annotations

import argparse
import json
from pathlib import Path
from .validator import validate_delimited_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FDA MAUDE delimited source files")
    parser.add_argument("--base", type=Path, help="Base MAUDE file")
    parser.add_argument("--device", type=Path, help="Device MAUDE file")
    parser.add_argument("--delimiter", default="|", help="Input delimiter")
    parser.add_argument("--output", type=Path, default=Path("outputs/validation_summary.json"))
    args = parser.parse_args()

    results = []
    if args.base:
        results.append(validate_delimited_file(args.base, 86, "MDR_REPORT_KEY", args.delimiter).to_dict())
    if args.device:
        results.append(validate_delimited_file(args.device, 34, "MDR_REPORT_KEY", args.delimiter).to_dict())
    if not results:
        parser.error("Provide --base and/or --device")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
