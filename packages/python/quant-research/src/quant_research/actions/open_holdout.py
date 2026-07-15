#!/usr/bin/env python3
"""Open a locked holdout only after freezing and hashing the research procedure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cycle")
    parser.add_argument("--procedure-frozen", action="store_true", help="Confirm selection and execution procedure is frozen")
    args = parser.parse_args()

    if not args.procedure_frozen:
        parser.error("--procedure-frozen is required")

    cycle = Path(args.cycle).expanduser().resolve()
    manifest_path = cycle / "cycle.json"
    try:
        manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read cycle.json: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if manifest.get("status") != "frozen":
        errors.append("cycle.json status must be 'frozen'")
    search = manifest.get("search_budget", {})
    if search.get("stage") != "locked_evaluation":
        errors.append("search_budget.stage must be 'locked_evaluation'")
    scope = manifest.get("scope", {})
    if not scope.get("data_path") or not scope.get("data_hash"):
        errors.append("scope.data_path and scope.data_hash must be frozen")
    validation = manifest.get("validation", {})
    for name in ("train", "validation"):
        split = validation.get(name, {})
        if not split.get("start") or not split.get("end"):
            errors.append(f"validation.{name} boundaries must be frozen")
    holdout = validation.get("locked_holdout", {})
    if holdout.get("status") != "sealed":
        errors.append("locked holdout must still be sealed")
    if holdout.get("opened_at_utc"):
        errors.append("locked holdout already has an opening timestamp")
    if not holdout.get("start") or not holdout.get("end"):
        errors.append("locked holdout boundaries must be frozen")
    if "TODO" in (cycle / "DATA_CARD.md").read_text(encoding="utf-8"):
        errors.append("DATA_CARD.md still contains TODO markers")

    hypotheses = read_rows(cycle / "HYPOTHESIS_LEDGER.csv")
    if not hypotheses:
        errors.append("no hypotheses are registered")
    unfinished = [row.get("hypothesis_id", "") for row in hypotheses if row.get("status") in {"registered", "running"}]
    if unfinished:
        errors.append(f"unfinished hypotheses: {', '.join(unfinished)}")
    promoted = [
        row for row in hypotheses
        if row.get("status") in {"conditionally_useful", "candidate_executable_alpha"}
    ]
    if not promoted:
        errors.append("no hypothesis is promoted for locked evaluation")

    validation_run = subprocess.run(
        [sys.executable, "-m", "quant_research.actions.validate_cycle", str(cycle), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        validation_result = json.loads(validation_run.stdout)
    except json.JSONDecodeError:
        errors.append(f"cycle validator did not return JSON: {validation_run.stderr.strip()}")
        validation_result = {"errors": []}
    errors.extend(f"validator: {item}" for item in validation_result.get("errors", []))

    if errors:
        for item in errors:
            print(f"error: {item}", file=sys.stderr)
        return 1

    freeze_paths = [
        cycle / "cycle.json",
        cycle / "DATA_CARD.md",
        cycle / "TARGET_MATRIX.csv",
        cycle / "HYPOTHESIS_LEDGER.csv",
        cycle / "EXPERIMENT_LEDGER.csv",
        cycle / "BROAD_EXPERIMENT_MATRIX.csv",
    ]
    freeze_paths.extend(sorted((cycle / "experiments").glob("*/experiment.json")))
    freeze_paths.extend(sorted((cycle / "experiments").glob("*/HYPOTHESIS.md")))
    freeze_record = {
        "cycle_id": manifest["cycle_id"],
        "frozen_at_utc": utc_now(),
        "files": {
            str(path.relative_to(cycle)): digest(path)
            for path in freeze_paths
            if path.is_file()
        },
    }
    (cycle / "FROZEN_PROCEDURE.json").write_text(json.dumps(freeze_record, indent=2) + "\n", encoding="utf-8")

    opened_at = utc_now()
    holdout["status"] = "open"
    holdout["opened_at_utc"] = opened_at
    holdout["reuse_count"] = int(holdout.get("reuse_count", 0)) + 1
    manifest["status"] = "locked_evaluation"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    marker = cycle / ".holdout-sealed"
    if marker.exists():
        marker.unlink()
    with (cycle / "RUN_LOG.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": "holdout_opened", "at_utc": opened_at}) + "\n")

    print(f"holdout opened at {opened_at}")
    print(cycle / "FROZEN_PROCEDURE.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
