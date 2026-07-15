#!/usr/bin/env python3
"""Evaluate trade-level evidence after explicit costs and uncertainty."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

from quant_core.economics.costs import CostModel
from quant_core.economics.trades import concentration, trade_metrics
from quant_core.math.statistics import block_bootstrap_mean


def display(value: Any, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "n/a"
        if math.isinf(value):
            return "∞"
        return f"{value:.{digits}f}"
    return str(value)


def json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def markdown(result: dict[str, Any]) -> str:
    gross = result["gross"]
    net = result["net"]
    interval = result["net_mean_block_bootstrap_95pct_bps"]
    lines = [
        "# Trade Evidence Evaluation",
        "",
        "## Economic result",
        "",
        f"- Trades: {net['count']:,}",
        f"- Mean gross return: {display(gross['mean_bps'])} bps/trade",
        f"- Mean modeled cost: {display(result['mean_modeled_cost_bps'])} bps/trade",
        f"- Mean net return: {display(net['mean_bps'])} bps/trade",
        f"- Block-bootstrap 95% interval for mean net return: [{display(interval[0])}, {display(interval[1])}] bps",
        f"- Remaining break-even cost capacity: {display(result['remaining_break_even_cost_bps'])} bps/trade",
        f"- Net hit rate: {display(net['hit_rate'] * 100, 2)}%",
        f"- Net profit factor: {display(net['profit_factor'])}",
        f"- Maximum compounded drawdown: {display(net['max_drawdown_pct'], 2)}%",
        "",
        "## Cost model",
        "",
        "| Component | bps/trade |",
        "|---|---:|",
    ]
    for key, value in result["global_cost_model_bps"].items():
        lines.append(f"| {key.replace('_', ' ')} | {display(value)} |")
    lines.extend(["", "## Long/short asymmetry", "", "| Side | Trades | Mean net bps | Hit rate | Profit factor |", "|---|---:|---:|---:|---:|"])
    for side, side_metrics in result["by_side"].items():
        lines.append(
            f"| {side} | {side_metrics['count']} | {display(side_metrics.get('mean_bps'))} | "
            f"{display(side_metrics.get('hit_rate', 0) * 100, 2)}% | {display(side_metrics.get('profit_factor'))} |"
        )
    lines.extend(["", "## Cost stress", "", "| Cost multiplier | Mean net bps |", "|---:|---:|"])
    for item in result["cost_stress"]:
        lines.append(f"| {display(item['multiplier'], 2)}× | {display(item['mean_net_bps'])} |")
    concentration_data = result["concentration"]
    lines.extend(
        [
            "",
            "## Concentration",
            "",
            f"- Top five trades' share of absolute PnL: {display(concentration_data['top_5_absolute_share'] * 100, 2)}%",
            f"- Top ten trades' share of absolute PnL: {display(concentration_data['top_10_absolute_share'] * 100, 2)}%",
            f"- Top five winners' share of positive PnL: {display(concentration_data['top_5_positive_profit_share'] * 100, 2)}%",
            "",
            "## Interpretation gate",
            "",
            result["interpretation"],
            "",
            "This evaluator measures trade-level economic evidence. It does not prove that",
            "signals were selected without leakage, that fills were available, that market",
            "impact is correctly modeled, or that the result survives the complete research",
            "ledger and locked holdout.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trades_csv")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--gross-return-col", default="gross_return_bps")
    parser.add_argument("--side-col", default="side")
    parser.add_argument("--fee-bps-per-side", type=float, required=True)
    parser.add_argument("--spread-bps-round-trip", type=float, required=True)
    parser.add_argument("--slippage-bps-round-trip", type=float, required=True)
    parser.add_argument("--funding-bps-per-trade", type=float, default=0.0)
    parser.add_argument("--borrow-bps-per-trade", type=float, default=0.0)
    parser.add_argument("--impact-bps-per-trade", type=float, default=0.0)
    parser.add_argument("--safety-margin-bps", type=float, default=0.0)
    parser.add_argument("--block-size", type=int, default=10)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=1729)
    args = parser.parse_args()

    cost_values = [
        args.fee_bps_per_side,
        args.spread_bps_round_trip,
        args.slippage_bps_round_trip,
        args.funding_bps_per_trade,
        args.borrow_bps_per_trade,
        args.impact_bps_per_trade,
        args.safety_margin_bps,
    ]
    if any(item < 0 for item in cost_values):
        parser.error("costs cannot be negative")
    if args.bootstrap_samples < 100:
        parser.error("bootstrap-samples must be at least 100")

    path = Path(args.trades_csv).expanduser().resolve()
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    gross: list[float] = []
    sides: list[str] = []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if args.gross_return_col not in headers:
            print(f"error: missing column {args.gross_return_col}", file=sys.stderr)
            return 1
        for row_number, row in enumerate(reader, start=2):
            try:
                value = float(row[args.gross_return_col])
                if not math.isfinite(value):
                    raise ValueError("non-finite")
            except (TypeError, ValueError):
                print(f"error: invalid gross return on row {row_number}", file=sys.stderr)
                return 1
            gross.append(value)
            side = row.get(args.side_col, "unknown").strip().lower() or "unknown"
            sides.append(side)
    if not gross:
        print("error: trade file is empty", file=sys.stderr)
        return 1

    cost_model = CostModel(
        fee_bps_per_side=args.fee_bps_per_side,
        spread_bps_round_trip=args.spread_bps_round_trip,
        slippage_bps_round_trip=args.slippage_bps_round_trip,
        funding_bps_per_trade=args.funding_bps_per_trade,
        borrow_bps_per_trade=args.borrow_bps_per_trade,
        impact_bps_per_trade=args.impact_bps_per_trade,
        safety_margin_bps=args.safety_margin_bps,
    )
    base_cost = cost_model.round_trip_bps
    net = [cost_model.net_return_bps(item) for item in gross]
    low, high = block_bootstrap_mean(net, args.block_size, args.bootstrap_samples, args.seed)
    by_side = {
        side: trade_metrics([value for value, observed_side in zip(net, sides) if observed_side == side])
        for side in sorted(set(sides))
    }
    stress = []
    for multiplier in (0.5, 1.0, 1.25, 1.5, 2.0):
        stress.append({
            "multiplier": multiplier,
            "mean_net_bps": statistics.fmean(cost_model.stress(item, multiplier) for item in gross),
        })

    mean_net = statistics.fmean(net)
    if low > 0:
        interpretation = (
            "Mean net return remains above zero at the lower block-bootstrap bound. "
            "Treat this as economic evidence requiring full leakage, selection, fill, "
            "capacity, delay, regime, and locked-holdout validation—not as proven alpha."
        )
    elif high <= 0:
        interpretation = "The block-bootstrap interval is entirely nonpositive after modeled costs; reject or materially redesign the candidate."
    elif mean_net > 0:
        interpretation = "Point-estimate net expectancy is positive but uncertainty includes zero; classify the economic evidence as inconclusive."
    else:
        interpretation = "Point-estimate net expectancy is nonpositive after modeled costs; the candidate is not economically usable under this model."

    result = {
        "source": str(path),
        "gross": trade_metrics(gross),
        "net": trade_metrics(net),
        "net_mean_block_bootstrap_95pct_bps": [low, high],
        "block_size": args.block_size,
        "bootstrap_samples": args.bootstrap_samples,
        "mean_modeled_cost_bps": base_cost,
        "remaining_break_even_cost_bps": mean_net,
        "global_cost_model_bps": {
            "fee_per_side": args.fee_bps_per_side,
            "spread_round_trip": args.spread_bps_round_trip,
            "slippage_round_trip": args.slippage_bps_round_trip,
            "funding_per_trade": args.funding_bps_per_trade,
            "borrow_per_trade": args.borrow_bps_per_trade,
            "impact_per_trade": args.impact_bps_per_trade,
            "safety_margin": args.safety_margin_bps,
        },
        "by_side": by_side,
        "cost_stress": stress,
        "concentration": concentration(net),
        "interpretation": interpretation,
    }
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "TRADE_EVALUATION.json").write_text(
        json.dumps(json_safe(result), indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "TRADE_EVALUATION.md").write_text(markdown(result), encoding="utf-8")
    print(output_dir / "TRADE_EVALUATION.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
