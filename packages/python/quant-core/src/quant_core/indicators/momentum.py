"""Past-only momentum and path-efficiency features."""

from __future__ import annotations

import math
from collections.abc import Sequence

from ..math.returns import log_return


def trailing_log_return(closes: Sequence[float], lookback: int) -> float:
    """Return the log change from ``lookback`` bars ago through the current bar."""
    if lookback < 1 or len(closes) < lookback + 1:
        raise ValueError("insufficient closes for lookback")
    return log_return(closes[-lookback - 1], closes[-1])


def path_efficiency(closes: Sequence[float], lookback: int) -> float:
    """Return net displacement divided by total absolute path movement."""
    if lookback < 1 or len(closes) < lookback + 1:
        raise ValueError("insufficient closes for lookback")
    sample = [float(item) for item in closes[-lookback - 1 :]]
    if not all(math.isfinite(item) and item > 0 for item in sample):
        raise ValueError("closes must be finite and positive")
    displacement = abs(sample[-1] - sample[0])
    path = sum(abs(current - previous) for previous, current in zip(sample, sample[1:]))
    return displacement / path if path else 0.0
