"""Dependency-free causal rolling-window operations."""

from __future__ import annotations

import math
import statistics
from collections.abc import Callable, Sequence


def rolling_apply(
    values: Sequence[float],
    window: int,
    function: Callable[[Sequence[float]], float],
    *,
    include_current: bool = True,
) -> list[float | None]:
    """Apply a function to past-only windows while preserving row alignment."""
    if window < 1:
        raise ValueError("window must be positive")
    output: list[float | None] = []
    for index in range(len(values)):
        stop = index + 1 if include_current else index
        start = stop - window
        if start < 0:
            output.append(None)
            continue
        sample = [float(item) for item in values[start:stop]]
        if len(sample) != window or not all(math.isfinite(item) for item in sample):
            output.append(None)
            continue
        output.append(float(function(sample)))
    return output


def rolling_mean(values: Sequence[float], window: int, *, include_current: bool = True) -> list[float | None]:
    return rolling_apply(values, window, statistics.fmean, include_current=include_current)


def rolling_median(values: Sequence[float], window: int, *, include_current: bool = True) -> list[float | None]:
    return rolling_apply(values, window, statistics.median, include_current=include_current)


def rolling_std(values: Sequence[float], window: int, *, include_current: bool = True) -> list[float | None]:
    def population_std(sample: Sequence[float]) -> float:
        return statistics.pstdev(sample)

    return rolling_apply(values, window, population_std, include_current=include_current)
