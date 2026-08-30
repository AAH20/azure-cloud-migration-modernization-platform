from __future__ import annotations

import argparse
import json
from pathlib import Path

from .planner import assess
from .render import markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile a cloud migration assessment, 7R portfolio and dependency waves")
    parser.add_argument("estate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = assess(json.loads(args.estate.read_text()))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "migration-assessment.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.output / "migration-assessment.md").write_text(markdown(report))
    receipt = {key: report[key] for key in ("schema_version", "scenario", "evidence_level", "readiness", "receipt_sha256")}
    (args.output / "migration-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
