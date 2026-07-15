"""Rolling range and location features."""

from __future__ import annotations

import math
from collections.abc import Sequence


def range_position(highs: Sequence[float], lows: Sequence[float], close: float, lookback: int) -> float:
    """Locate the current close inside the completed trailing high-low range."""
    if lookback < 1 or len(highs) < lookback or len(lows) < lookback:
        raise ValueError("insufficient range history for lookback")
    high_window = [float(item) for item in highs[-lookback:]]
    low_window = [float(item) for item in lows[-lookback:]]
    close = float(close)
    if not all(math.isfinite(item) and item > 0 for item in high_window + low_window + [close]):
        raise ValueError("prices must be finite and positive")
    upper = max(high_window)
    lower = min(low_window)
    if upper < lower:
        raise ValueError("rolling high is below rolling low")
    return (close - lower) / (upper - lower) if upper > lower else 0.5
