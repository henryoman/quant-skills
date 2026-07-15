#!/usr/bin/env python3
"""Validate a quant-alpha research cycle and its integrity gates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


CYCLE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{5,79}$")
HYPOTHESIS_ID = re.compile(r"^[A-M][0-9]{2}-[a-z0-9][a-z0-9-]{2,59}$")
ALLOWED_DECISIONS = {
    "Stop: no credible evidence.",
    "Gather more data.",
    "Change target or horizon.",
    "Investigate a specific candidate.",
    "Run a locked confirmation.",
    "Begin paper-trading validation.",
}
ALLOWED_STATUSES = {
    "registered",
    "running",
    "rejected",
    "inconclusive",
    "interesting_not_tradable",
    "predictive_economically_weak",
    "conditionally_useful",
    "candidate_executable_alpha",
}
REQUIRED_FILES = {
    "cycle.json",
    "DATA_CARD.md",
    "TARGET_MATRIX.csv",
    "HYPOTHESIS_LEDGER.csv",
    "EXPERIMENT_LEDGER.csv",
    "BROAD_EXPERIMENT_MATRIX.csv",
    "DECISION.md",
    "RUN_LOG.jsonl",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def get_nested(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def load_csv(path: Path, required_headers: list[str], report: Report) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            missing = [item for item in required_headers if item not in headers]
            if missing:
                report.error(f"{path.name}: missing columns {', '.join(missing)}")
            return list(reader)
    except (OSError, csv.Error) as exc:
        report.error(f"{path.name}: cannot read CSV: {exc}")
        return []


def validate_manifest(cycle: Path, manifest: dict[str, Any], report: Report) -> None:
    required = [
        "schema_version",
        "cycle_id",
        "status",
        "objective",
        "scope.asset",
        "scope.venue",
        "scope.bar_interval",
        "scope.timezone",
        "scope.fields",
        "information_boundary.feature_cutoff",
        "information_boundary.decision_time",
        "information_boundary.execution_price",
        "information_boundary.execution_delay_bars",
        "validation.method",
        "validation.purge_bars",
        "validation.embargo_bars",
        "validation.locked_holdout.status",
        "economics.fee_bps_per_side",
        "economics.spread_bps_round_trip",
        "economics.slippage_bps_round_trip",
        "economics.safety_margin_bps",
        "search_budget.total_variant_cap",
        "search_budget.max_family_share",
        "search_budget.required_families",
    ]
    for path in required:
        value = get_nested(manifest, path)
        if value is None or value == "" or value == []:
            report.error(f"cycle.json: missing required value {path}")

    cycle_id = manifest.get("cycle_id", "")
    if not CYCLE_ID.fullmatch(str(cycle_id)):
        report.error("cycle.json: invalid cycle_id")
    if cycle.name != cycle_id:
        report.error(f"cycle directory '{cycle.name}' does not match cycle_id '{cycle_id}'")

    fields = {str(item).lower() for item in get_nested(manifest, "scope.fields") or []}
    missing_fields = {"timestamp", "open", "high", "low", "close", "volume"} - fields
    if missing_fields:
        report.warn(f"scope.fields lacks standard OHLCV fields: {', '.join(sorted(missing_fields))}")

    delay = get_nested(manifest, "information_boundary.execution_delay_bars")
    if isinstance(delay, (int, float)) and delay < 1:
        report.error("execution delay must be at least one bar for the default close-observe convention")

    costs = [
        get_nested(manifest, "economics.fee_bps_per_side"),
        get_nested(manifest, "economics.spread_bps_round_trip"),
        get_nested(manifest, "economics.slippage_bps_round_trip"),
        get_nested(manifest, "economics.safety_margin_bps"),
    ]
    numeric_costs = [float(item) for item in costs if isinstance(item, (int, float))]
    if numeric_costs and sum(numeric_costs) == 0:
        report.warn("all execution costs and the estimation safety margin are zero")
    if any(item < 0 for item in numeric_costs):
        report.error("economic cost inputs cannot be negative")

    max_horizon = max(get_nested(manifest, "targets.registered_horizons_bars") or [0])
    purge = get_nested(manifest, "validation.purge_bars") or 0
    embargo = get_nested(manifest, "validation.embargo_bars") or 0
    if purge < max_horizon:
        report.error("purge_bars is smaller than the maximum registered target horizon")
    if embargo < max_horizon:
        report.warn("embargo_bars is smaller than the maximum registered target horizon")

    holdout = get_nested(manifest, "validation.locked_holdout") or {}
    holdout_status = holdout.get("status")
    opened_at = holdout.get("opened_at_utc")
    reuse = holdout.get("reuse_count", 0)
    reuse_cap = get_nested(manifest, "search_budget.holdout_reuse_cap") or 1
    sealed_marker = cycle / ".holdout-sealed"
    if holdout_status == "sealed":
        if opened_at:
            report.error("holdout is marked sealed but opened_at_utc is populated")
        if not sealed_marker.exists():
            report.error("sealed holdout is missing .holdout-sealed marker")
    elif sealed_marker.exists():
        report.error("holdout is not sealed but .holdout-sealed marker still exists")
    if isinstance(reuse, int) and reuse > reuse_cap:
        report.error(f"holdout reuse_count {reuse} exceeds cap {reuse_cap}")

    data_path = get_nested(manifest, "scope.data_path")
    if data_path:
        path = Path(str(data_path))
        if path.is_absolute():
            report.error("scope.data_path must be relative to the cycle directory")
        elif "_archive_do_not_use" in path.parts:
            report.error("scope.data_path may not reference _archive_do_not_use")
        elif not (cycle / path).exists():
            report.warn(f"declared data path does not exist: {data_path}")
    else:
        report.warn("scope.data_path is not set")
    if not get_nested(manifest, "scope.data_hash"):
        report.warn("scope.data_hash is not set")
    audit_status = get_nested(manifest, "scope.data_audit.status")
    if audit_status == "blocked":
        report.error("data audit is blocked by critical data-quality failures")
    elif audit_status == "review_required":
        report.warn("data audit requires documented review before alpha testing")
    elif audit_status not in {None, "passed"}:
        report.error(f"unknown data audit status: {audit_status}")
    elif audit_status is None:
        report.warn("no data audit status is recorded")

    split_paths = ["validation.train", "validation.validation", "validation.locked_holdout"]
    for split_path in split_paths:
        split = get_nested(manifest, split_path) or {}
        if not split.get("start") or not split.get("end"):
            report.warn(f"{split_path} date boundaries are not frozen")


def validate_targets(cycle: Path, report: Report) -> None:
    headers = [
        "target_id",
        "target_type",
        "horizon_bars",
        "entry_clock",
        "exit_clock",
        "unit",
        "economic_interpretation",
        "overlap",
        "ambiguity_rule",
        "status",
    ]
    rows = load_csv(cycle / "TARGET_MATRIX.csv", headers, report)
    if not rows:
        report.error("TARGET_MATRIX.csv has no registered targets")
        return
    ids = [row.get("target_id", "") for row in rows]
    duplicates = [item for item, count in Counter(ids).items() if item and count > 1]
    if duplicates:
        report.error(f"duplicate target IDs: {', '.join(duplicates)}")
    types = {row.get("target_type") for row in rows}
    if len(types) < 3:
        report.warn("target matrix contains fewer than three logically distinct target types")
    for row in rows:
        try:
            if int(row.get("horizon_bars", "0")) <= 0:
                raise ValueError
        except ValueError:
            report.error(f"target {row.get('target_id')}: horizon_bars must be positive")
        if not row.get("entry_clock") or not row.get("exit_clock"):
            report.error(f"target {row.get('target_id')}: entry and exit clocks are required")


def validate_hypotheses(cycle: Path, manifest: dict[str, Any], report: Report) -> None:
    headers = [
        "hypothesis_id",
        "family",
        "short_name",
        "observable_state",
        "future_outcome",
        "expected_relationship",
        "variant_cap",
        "variants_run",
        "status",
        "main_evidence",
        "main_failure_risk",
        "registered_at_utc",
        "updated_at_utc",
    ]
    rows = load_csv(cycle / "HYPOTHESIS_LEDGER.csv", headers, report)
    if not rows:
        report.warn("no hypotheses are registered")
        return

    allowed_families = set(get_nested(manifest, "search_budget.required_families") or [])
    variant_total = 0
    family_caps: Counter[str] = Counter()
    ids: list[str] = []
    for row in rows:
        hypothesis_id = row.get("hypothesis_id", "")
        ids.append(hypothesis_id)
        if not HYPOTHESIS_ID.fullmatch(hypothesis_id):
            report.error(f"invalid hypothesis ID: {hypothesis_id}")
        family = row.get("family", "")
        if family != hypothesis_id[:1]:
            report.error(f"{hypothesis_id}: family column does not match ID")
        if family not in allowed_families:
            report.error(f"{hypothesis_id}: family {family} was not declared in cycle.json")
        try:
            cap = int(row.get("variant_cap", "0"))
            run = int(row.get("variants_run", "0"))
            if cap < 1 or run < 0 or run > cap:
                raise ValueError
        except ValueError:
            report.error(f"{hypothesis_id}: invalid variant cap or run count")
            cap = 0
        variant_total += cap
        family_caps[family] += cap
        if row.get("status") not in ALLOWED_STATUSES:
            report.error(f"{hypothesis_id}: invalid status '{row.get('status')}'")
        experiment = cycle / "experiments" / hypothesis_id / "experiment.json"
        hypothesis = cycle / "experiments" / hypothesis_id / "HYPOTHESIS.md"
        if not experiment.is_file() or not hypothesis.is_file():
            report.error(f"{hypothesis_id}: missing experiment.json or HYPOTHESIS.md")

    duplicates = [item for item, count in Counter(ids).items() if item and count > 1]
    if duplicates:
        report.error(f"duplicate hypothesis IDs: {', '.join(duplicates)}")

    total_cap = get_nested(manifest, "search_budget.total_variant_cap") or 0
    if variant_total > total_cap:
        report.error(f"declared hypothesis variants {variant_total} exceed cycle cap {total_cap}")
    max_share = get_nested(manifest, "search_budget.max_family_share") or 0.20
    family_limit = total_cap * max_share
    for family, count in family_caps.items():
        if count > family_limit:
            report.error(f"family {family} variant cap {count} exceeds {max_share:.0%} of cycle budget")

    missing_families = sorted(allowed_families - set(family_caps))
    stage = get_nested(manifest, "search_budget.stage")
    if missing_families:
        message = f"hypothesis families not yet covered: {', '.join(missing_families)}"
        if stage in {"broad_search_complete", "candidate_refinement", "adversarial_validation", "locked_evaluation"}:
            report.error(message)
        else:
            report.warn(message)


def validate_decision(cycle: Path, report: Report) -> None:
    path = cycle / "DECISION.md"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        report.error(f"cannot read DECISION.md: {exc}")
        return
    selected = []
    for line in lines:
        match = re.match(r"^- \[[xX]\] (.+)$", line.strip())
        if match:
            selected.append(match.group(1))
    invalid = [item for item in selected if item not in ALLOWED_DECISIONS]
    if invalid:
        report.error(f"unknown selected research decisions: {', '.join(invalid)}")
    if len(selected) > 1:
        report.error("DECISION.md selects more than one research decision")
    elif not selected:
        report.warn("DECISION.md has no selected research decision")
    todo_count = sum(1 for line in lines if "TODO" in line)
    if todo_count:
        report.warn(f"DECISION.md contains {todo_count} unresolved TODO markers")


def validate_archive_references(cycle: Path, report: Report) -> None:
    for path in cycle.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".csv", ".py", ".yaml", ".yml"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "_archive_do_not_use" in content:
            report.error(f"{path.relative_to(cycle)} references forbidden archive material")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cycle", help="Path to cycle directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    cycle = Path(args.cycle).expanduser().resolve()
    report = Report()
    missing = sorted(name for name in REQUIRED_FILES if not (cycle / name).is_file())
    for name in missing:
        report.error(f"missing required file: {name}")

    manifest: dict[str, Any] = {}
    manifest_path = cycle / "cycle.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            report.error(f"cannot parse cycle.json: {exc}")

    if manifest:
        validate_manifest(cycle, manifest, report)
    if (cycle / "TARGET_MATRIX.csv").is_file():
        validate_targets(cycle, report)
    if manifest and (cycle / "HYPOTHESIS_LEDGER.csv").is_file():
        validate_hypotheses(cycle, manifest, report)
    if (cycle / "DECISION.md").is_file():
        validate_decision(cycle, report)
    validate_archive_references(cycle, report)

    result = {
        "cycle": str(cycle),
        "valid": not report.errors and (not args.strict or not report.warnings),
        "errors": report.errors,
        "warnings": report.warnings,
    }
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"cycle: {cycle}")
        print(f"errors: {len(report.errors)}")
        for item in report.errors:
            print(f"  ERROR: {item}")
        print(f"warnings: {len(report.warnings)}")
        for item in report.warnings:
            print(f"  WARN: {item}")

    if report.errors:
        return 1
    if args.strict and report.warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
