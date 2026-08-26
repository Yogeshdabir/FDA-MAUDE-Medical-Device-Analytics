from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ingest import stream_delimited
from .profile import profile_csv, write_profile


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="FDA MAUDE Phase 1 ingestion and DQ pipeline")
    p.add_argument("--base", type=Path, help="MAUDE Base .txt/.zip")
    p.add_argument("--device", type=Path, help="MAUDE Device .txt/.zip")
    p.add_argument("--delimiter", default="|", help="Source delimiter (default: |)")
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    p.add_argument("--max-rows", type=int, default=None, help="Optional development limit")
    p.add_argument("--profile-only", action="store_true")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if not args.base and not args.device:
        raise SystemExit("Provide --base and/or --device")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for label, source in (("base", args.base), ("device", args.device)):
        if source is None:
            continue
        if args.profile_only:
            if source.suffix.lower() == ".zip":
                raise SystemExit("--profile-only currently expects extracted .txt/.csv files")
            profile = profile_csv(source, args.delimiter)
            write_profile(profile, args.output_dir / f"{label}_profile.json")
            results.append(profile)
            continue
        result = stream_delimited(
            source,
            args.output_dir / f"{label}_clean.csv",
            args.output_dir / f"{label}_quarantine.csv",
            expected_fields=None,
            delimiter=args.delimiter,
            max_rows=args.max_rows,
        )
        results.append(result.__dict__)

    (args.output_dir / "ingestion_summary.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
