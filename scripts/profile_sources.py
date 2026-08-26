from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.maude_pipeline.profile import profile_csv, write_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile an extracted MAUDE file")
    parser.add_argument("file", type=Path)
    parser.add_argument("--delimiter", default="|")
    parser.add_argument("--output", type=Path, default=Path("outputs/profile.json"))
    args = parser.parse_args()
    profile = profile_csv(args.file, args.delimiter)
    write_profile(profile, args.output)
    print(json.dumps(profile, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
