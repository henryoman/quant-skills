"""Past-only realized-volatility features."""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

from ..math.returns import log_return


def realized_volatility(closes: Sequence[float], lookback: int, *, annualization: float = 1.0) -> float:
    """Compute root-mean-square log return over a completed trailing window."""
    if lookback < 2 or len(closes) < lookback + 1:
        raise ValueError("lookback must be at least two with enough closes")
    if not math.isfinite(annualization) or annualization <= 0:
        raise ValueError("annualization must be finite and positive")
    sample = closes[-lookback - 1 :]
    returns = [log_return(start, end) for start, end in zip(sample, sample[1:])]
    return math.sqrt(statistics.fmean(item * item for item in returns) * annualization)
