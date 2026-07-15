#!/usr/bin/env python3
"""Register a falsifiable experiment inside an existing research cycle."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


from ..core.paths import TEMPLATES_ROOT


TEMPLATE = TEMPLATES_ROOT / "HYPOTHESIS.md.tmpl"
ID_PATTERN = re.compile(r"^[A-M][0-9]{2}-[a-z0-9][a-z0-9-]{2,59}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def render(template: str, replacements: dict[str, object]) -> str:
    for key, value in replacements.items():
        template = template.replace(f"__{key}__", str(value))
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True, help="Path to the cycle directory")
    parser.add_argument("--id", required=True, dest="hypothesis_id")
    parser.add_argument("--name", required=True)
    parser.add_argument("--observable-state", required=True)
    parser.add_argument("--future-outcome", required=True)
    parser.add_argument("--expected-relationship", required=True)
    parser.add_argument("--falsification-test", required=True)
    parser.add_argument("--promotion-criteria", required=True)
    parser.add_argument("--variant-cap", required=True, type=int)
    parser.add_argument("--formation-horizons", default="coarse short, medium, long")
    parser.add_argument("--outcome-horizons", default="from TARGET_MATRIX.csv")
    parser.add_argument("--thresholds", default="training-defined coarse bins")
    parser.add_argument("--models", default="descriptive profile, threshold baseline")
    args = parser.parse_args()

    if not ID_PATTERN.fullmatch(args.hypothesis_id):
        parser.error("id must look like B01-momentum-coarse")
    if args.variant_cap < 1:
        parser.error("variant-cap must be positive")

    cycle = Path(args.cycle).expanduser().resolve()
    manifest_path = cycle / "cycle.json"
    if not manifest_path.is_file():
        print(f"error: missing {manifest_path}", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    family = args.hypothesis_id[0]
    allowed = manifest.get("search_budget", {}).get("required_families", [])
    if family not in allowed:
        print(f"error: family {family} is not in this cycle's declared family set", file=sys.stderr)
        return 1

    ledger_path = cycle / "HYPOTHESIS_LEDGER.csv"
    with ledger_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if any(row["hypothesis_id"] == args.hypothesis_id for row in reader):
            print(f"error: {args.hypothesis_id} already exists in ledger", file=sys.stderr)
            return 1
        fields = reader.fieldnames
    if not fields:
        print("error: hypothesis ledger has no header", file=sys.stderr)
        return 1

    experiment_dir = cycle / "experiments" / args.hypothesis_id
    if experiment_dir.exists():
        print(f"error: experiment already exists: {experiment_dir}", file=sys.stderr)
        return 1
    experiment_dir.mkdir(parents=True)
    (experiment_dir / "src").mkdir()
    (experiment_dir / "results").mkdir()

    registered_at = utc_now()
    experiment = {
        "schema_version": "1.0",
        "hypothesis_id": args.hypothesis_id,
        "family": family,
        "short_name": args.name,
        "registered_at_utc": registered_at,
        "status": "registered",
        "observable_state": args.observable_state,
        "future_outcome": args.future_outcome,
        "expected_relationship": args.expected_relationship,
        "falsification_test": args.falsification_test,
        "promotion_criteria": args.promotion_criteria,
        "search": {
            "variant_cap": args.variant_cap,
            "formation_horizons": csv_list(args.formation_horizons),
            "outcome_horizons": csv_list(args.outcome_horizons),
            "thresholds": csv_list(args.thresholds),
            "models": csv_list(args.models),
            "variants_run": 0,
        },
        "result": {
            "classification": None,
            "gross_effect_bps": None,
            "net_effect_bps": None,
            "confidence_interval_bps": None,
            "effective_observations": None,
            "main_failure_risk": None,
        },
    }
    (experiment_dir / "experiment.json").write_text(json.dumps(experiment, indent=2) + "\n", encoding="utf-8")

    hypothesis_text = render(
        TEMPLATE.read_text(encoding="utf-8"),
        {
            "HYPOTHESIS_ID": args.hypothesis_id,
            "SHORT_NAME": args.name,
            "OBSERVABLE_STATE": args.observable_state,
            "FUTURE_OUTCOME": args.future_outcome,
            "EXPECTED_RELATIONSHIP": args.expected_relationship,
            "FALSIFICATION_TEST": args.falsification_test,
            "PROMOTION_CRITERIA": args.promotion_criteria,
            "FAMILY": family,
            "VARIANT_CAP": args.variant_cap,
            "FORMATION_HORIZONS": args.formation_horizons,
            "OUTCOME_HORIZONS": args.outcome_horizons,
            "THRESHOLDS": args.thresholds,
            "MODELS": args.models,
        },
    )
    (experiment_dir / "HYPOTHESIS.md").write_text(hypothesis_text, encoding="utf-8")

    row = {
        "hypothesis_id": args.hypothesis_id,
        "family": family,
        "short_name": args.name,
        "observable_state": args.observable_state,
        "future_outcome": args.future_outcome,
        "expected_relationship": args.expected_relationship,
        "variant_cap": args.variant_cap,
        "variants_run": 0,
        "status": "registered",
        "main_evidence": "",
        "main_failure_risk": "",
        "registered_at_utc": registered_at,
        "updated_at_utc": registered_at,
    }
    with ledger_path.open("a", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=fields).writerow(row)

    print(experiment_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
