"""Causally normalized activity features."""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence


def relative_volume(volumes: Sequence[float], lookback: int, *, epsilon: float = 1e-12) -> float:
    """Compare current volume with the median of prior bars only."""
    if lookback < 1 or len(volumes) < lookback + 1:
        raise ValueError("insufficient volume history for lookback")
    current = float(volumes[-1])
    history = [float(item) for item in volumes[-lookback - 1 : -1]]
    if not math.isfinite(current) or current < 0:
        raise ValueError("current volume must be finite and nonnegative")
    if not all(math.isfinite(item) and item >= 0 for item in history):
        raise ValueError("volume history must be finite and nonnegative")
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and positive")
    baseline = statistics.median(history)
    return current / (baseline + epsilon)
