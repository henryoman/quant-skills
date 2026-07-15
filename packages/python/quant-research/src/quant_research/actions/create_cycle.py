#!/usr/bin/env python3
"""Create a registered, leakage-aware quantitative research cycle."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


from ..core.paths import TEMPLATES_ROOT


ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{5,79}$")
INTERVAL_PATTERN = re.compile(r"^[1-9][0-9]*(s|m|h|d)$")
BASE_FAMILIES = list("ABCDEFGHIJKL")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_horizons(value: str) -> list[int]:
    horizons = sorted({int(item) for item in csv_list(value)})
    if not horizons or any(item <= 0 for item in horizons):
        raise argparse.ArgumentTypeError("horizons must be positive comma-separated integers")
    return horizons


def copy_asset(name: str, destination: Path) -> None:
    destination.write_bytes((TEMPLATES_ROOT / name).read_bytes())


def write_target_matrix(path: Path, horizons: list[int]) -> None:
    fields = [
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
    rows: list[dict[str, object]] = []
    for horizon in horizons:
        suffix = f"h{horizon}"
        common = {
            "horizon_bars": horizon,
            "entry_clock": "bar_t_plus_1_open",
            "exit_clock": f"close_after_{horizon}_bars",
            "overlap": "yes" if horizon > 1 else "no",
            "status": "registered",
        }
        rows.extend(
            [
                {
                    **common,
                    "target_id": f"log_return_{suffix}",
                    "target_type": "log_return",
                    "unit": "bps",
                    "economic_interpretation": "gross directional payoff before costs",
                    "ambiguity_rule": "not_applicable",
                },
                {
                    **common,
                    "target_id": f"direction_{suffix}",
                    "target_type": "direction",
                    "unit": "probability",
                    "economic_interpretation": "probability of positive executable return",
                    "ambiguity_rule": "zero_return_is_not_positive",
                },
                {
                    **common,
                    "target_id": f"future_range_{suffix}",
                    "target_type": "future_range",
                    "unit": "bps",
                    "economic_interpretation": "opportunity magnitude and risk-sizing input",
                    "ambiguity_rule": "use_future_high_low_range",
                },
                {
                    **common,
                    "target_id": f"mae_{suffix}",
                    "target_type": "maximum_adverse_excursion",
                    "unit": "bps",
                    "economic_interpretation": "conditional downside and stop-out risk",
                    "ambiguity_rule": "no_intrabar_order_claim",
                },
            ]
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_manifest(args: argparse.Namespace, families: list[str]) -> dict[str, object]:
    fields = csv_list(args.fields)
    return {
        "schema_version": "1.0",
        "cycle_id": args.cycle_id,
        "created_at_utc": utc_now(),
        "status": "draft",
        "objective": args.objective,
        "scope": {
            "asset": args.asset,
            "venue": args.venue,
            "instrument_type": args.instrument_type,
            "bar_interval": args.interval,
            "timezone": args.timezone,
            "date_range": {"start": args.start, "end": args.end},
            "fields": fields,
            "data_path": args.data_path,
            "data_hash": "",
        },
        "information_boundary": {
            "bar_timestamp_semantics": args.timestamp_semantics,
            "feature_cutoff": "bar_t_close",
            "decision_time": "after_bar_t_close",
            "order_time": "after_decision",
            "execution_price": args.execution_price,
            "execution_delay_bars": args.execution_delay_bars,
        },
        "targets": {
            "matrix": "TARGET_MATRIX.csv",
            "registered_horizons_bars": args.horizons,
        },
        "validation": {
            "method": "chronological_walk_forward",
            "train": {"start": "", "end": ""},
            "validation": {"start": "", "end": ""},
            "walk_forward": {"folds": 0, "definition": ""},
            "purge_bars": max(args.horizons),
            "embargo_bars": max(args.horizons),
            "locked_holdout": {
                "start": "",
                "end": "",
                "status": "sealed",
                "opened_at_utc": None,
                "reuse_count": 0,
            },
        },
        "economics": {
            "fee_bps_per_side": args.fee_bps_per_side,
            "spread_bps_round_trip": args.spread_bps_round_trip,
            "slippage_bps_round_trip": args.slippage_bps_round_trip,
            "funding_bps_per_day": args.funding_bps_per_day,
            "borrow_bps_per_day": args.borrow_bps_per_day,
            "impact_model": "not_modeled",
            "safety_margin_bps": args.safety_margin_bps,
        },
        "search_budget": {
            "stage": "structural_profiling",
            "total_variant_cap": args.total_variant_cap,
            "max_family_share": 0.20,
            "required_families": families,
            "holdout_reuse_cap": 1,
        },
        "paths": {
            "data_card": "DATA_CARD.md",
            "target_matrix": "TARGET_MATRIX.csv",
            "hypothesis_ledger": "HYPOTHESIS_LEDGER.csv",
            "experiment_ledger": "EXPERIMENT_LEDGER.csv",
            "broad_experiment_matrix": "BROAD_EXPERIMENT_MATRIX.csv",
            "decision": "DECISION.md",
            "experiments": "experiments",
            "results": "results",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle-id", required=True)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--venue", required=True)
    parser.add_argument("--interval", required=True, help="Bar interval, for example 1m or 5m")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--root", default="research/cycles")
    parser.add_argument("--instrument-type", default="spot")
    parser.add_argument("--timezone", default="UTC")
    parser.add_argument("--start", default="")
    parser.add_argument("--end", default="")
    parser.add_argument("--data-path", default="")
    parser.add_argument("--fields", default="timestamp,open,high,low,close,volume")
    parser.add_argument("--timestamp-semantics", choices=["open_time", "close_time", "unknown"], default="unknown")
    parser.add_argument("--execution-price", default="bar_t_plus_1_open")
    parser.add_argument("--execution-delay-bars", type=int, default=1)
    parser.add_argument("--horizons", type=parse_horizons, default=parse_horizons("1,5,15,60"))
    parser.add_argument("--families", default=",".join(BASE_FAMILIES))
    parser.add_argument("--multi-asset", action="store_true")
    parser.add_argument("--total-variant-cap", type=int, default=120)
    parser.add_argument("--fee-bps-per-side", type=float, default=0.0)
    parser.add_argument("--spread-bps-round-trip", type=float, default=0.0)
    parser.add_argument("--slippage-bps-round-trip", type=float, default=0.0)
    parser.add_argument("--funding-bps-per-day", type=float, default=0.0)
    parser.add_argument("--borrow-bps-per-day", type=float, default=0.0)
    parser.add_argument("--safety-margin-bps", type=float, default=0.0)
    args = parser.parse_args()

    if not ID_PATTERN.fullmatch(args.cycle_id):
        parser.error("cycle-id must be 6-80 lowercase letters, digits, or hyphens")
    if not INTERVAL_PATTERN.fullmatch(args.interval):
        parser.error("interval must look like 30s, 1m, 5m, 1h, or 1d")
    if args.execution_delay_bars < 1:
        parser.error("execution-delay-bars must be at least 1")
    if args.total_variant_cap < 1:
        parser.error("total-variant-cap must be positive")
    data_path = Path(args.data_path)
    if data_path.is_absolute():
        parser.error("data-path must be relative to the cycle directory")
    if "_archive_do_not_use" in data_path.parts:
        parser.error("data-path may not reference _archive_do_not_use")

    families = [item.upper() for item in csv_list(args.families)]
    if args.multi_asset and "M" not in families:
        families.append("M")
    invalid = [item for item in families if item not in list("ABCDEFGHIJKLM")]
    if invalid:
        parser.error(f"unknown hypothesis families: {', '.join(invalid)}")

    root = Path(args.root).expanduser().resolve()
    destination = root / args.cycle_id
    if destination.exists():
        print(f"error: cycle already exists: {destination}", file=sys.stderr)
        return 1

    destination.mkdir(parents=True)
    (destination / "experiments").mkdir()
    (destination / "results").mkdir()
    (destination / "data").mkdir()
    (destination / ".holdout-sealed").write_text("Do not open the locked holdout before the procedure is frozen.\n", encoding="utf-8")

    manifest = build_manifest(args, families)
    (destination / "cycle.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    copy_asset("DATA_CARD.md", destination / "DATA_CARD.md")
    copy_asset("HYPOTHESIS_LEDGER.csv", destination / "HYPOTHESIS_LEDGER.csv")
    copy_asset("EXPERIMENT_LEDGER.csv", destination / "EXPERIMENT_LEDGER.csv")
    copy_asset("BROAD_EXPERIMENT_MATRIX.csv", destination / "BROAD_EXPERIMENT_MATRIX.csv")
    copy_asset("DECISION.md", destination / "DECISION.md")
    write_target_matrix(destination / "TARGET_MATRIX.csv", args.horizons)
    (destination / "RUN_LOG.jsonl").touch()

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
