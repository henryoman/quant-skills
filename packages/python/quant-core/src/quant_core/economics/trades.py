"""Trade-level economic evidence metrics."""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence
from typing import Any

from ..math.statistics import percentile


def max_drawdown(returns_bps: Sequence[float]) -> float:
    """Return maximum compounded drawdown in percent."""
    equity = 1.0
    peak = 1.0
    worst = 0.0
    for item in returns_bps:
        value = float(item)
        if not math.isfinite(value) or value <= -10_000:
            raise ValueError("trade returns must be finite and greater than -10,000 bps")
        equity *= 1.0 + value / 10_000
        peak = max(peak, equity)
        worst = min(worst, (equity / peak - 1.0) * 100)
    return worst


def trade_metrics(returns_bps: Sequence[float]) -> dict[str, Any]:
    """Compute exact descriptive and path-dependent trade metrics."""
    values = [float(item) for item in returns_bps]
    if not values:
        return {"count": 0}
    if not all(math.isfinite(item) for item in values):
        raise ValueError("trade returns must be finite")
    positives = [item for item in values if item > 0]
    negatives = [item for item in values if item < 0]
    positive_sum = sum(positives)
    negative_sum = abs(sum(negatives))
    profit_factor = positive_sum / negative_sum if negative_sum else (math.inf if positive_sum else math.nan)
    ordered = sorted(values)
    return {
        "count": len(values),
        "mean_bps": statistics.fmean(values),
        "median_bps": statistics.median(values),
        "stdev_bps": statistics.stdev(values) if len(values) > 1 else 0.0,
        "hit_rate": len(positives) / len(values),
        "profit_factor": profit_factor,
        "sum_bps": sum(values),
        "max_drawdown_pct": max_drawdown(values),
        "p05_bps": percentile(ordered, 0.05),
        "p95_bps": percentile(ordered, 0.95),
    }


def concentration(returns_bps: Sequence[float]) -> dict[str, float]:
    """Measure whether a small number of trades dominates observed PnL."""
    values = [float(item) for item in returns_bps]
    if not all(math.isfinite(item) for item in values):
        raise ValueError("trade returns must be finite")
    absolute_total = sum(abs(item) for item in values)
    positive_total = sum(item for item in values if item > 0)
    by_absolute = sorted((abs(item) for item in values), reverse=True)
    by_positive = sorted((item for item in values if item > 0), reverse=True)
    return {
        "top_5_absolute_share": sum(by_absolute[:5]) / absolute_total if absolute_total else 0.0,
        "top_10_absolute_share": sum(by_absolute[:10]) / absolute_total if absolute_total else 0.0,
        "top_5_positive_profit_share": sum(by_positive[:5]) / positive_total if positive_total else 0.0,
    }
