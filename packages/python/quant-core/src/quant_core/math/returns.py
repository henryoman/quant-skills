"""Price-return transformations with explicit validation."""

from __future__ import annotations

import math
from collections.abc import Sequence


def _positive(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def simple_return(start: float, end: float) -> float:
    """Return ``end / start - 1`` for positive finite prices."""
    return _positive(end, "end") / _positive(start, "start") - 1.0


def log_return(start: float, end: float) -> float:
    """Return the natural-log price change for positive finite prices."""
    return math.log(_positive(end, "end") / _positive(start, "start"))


def to_basis_points(decimal_return: float) -> float:
    """Convert a decimal return to basis points."""
    value = float(decimal_return)
    if not math.isfinite(value):
        raise ValueError("decimal_return must be finite")
    return value * 10_000.0


def forward_log_returns(prices: Sequence[float], horizon: int) -> list[float | None]:
    """Compute forward log returns without shortening or reindexing the series."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    output: list[float | None] = [None] * len(prices)
    for index in range(max(0, len(prices) - horizon)):
        output[index] = log_return(prices[index], prices[index + horizon])
    return output
