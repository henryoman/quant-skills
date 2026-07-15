"""Dependence-aware statistical helpers."""

from __future__ import annotations

import math
import random
import statistics
from collections.abc import Sequence


def percentile(sorted_values: Sequence[float], probability: float) -> float:
    """Linearly interpolate a percentile from an already sorted sequence."""
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between zero and one")
    if not sorted_values:
        return math.nan
    position = (len(sorted_values) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return float(sorted_values[low])
    weight = position - low
    return float(sorted_values[low] * (1 - weight) + sorted_values[high] * weight)


def block_bootstrap_mean(
    values: Sequence[float],
    block_size: int,
    samples: int,
    seed: int,
) -> tuple[float, float]:
    """Return a moving-block-bootstrap 95% interval for the sample mean."""
    clean = [float(item) for item in values]
    if not clean:
        return math.nan, math.nan
    if samples < 100:
        raise ValueError("samples must be at least 100")
    if not all(math.isfinite(item) for item in clean):
        raise ValueError("values must be finite")
    rng = random.Random(seed)
    count = len(clean)
    block_size = max(1, min(block_size, count))
    means: list[float] = []
    for _ in range(samples):
        draw: list[float] = []
        while len(draw) < count:
            start = rng.randrange(count)
            for offset in range(block_size):
                draw.append(clean[(start + offset) % count])
                if len(draw) == count:
                    break
        means.append(statistics.fmean(draw))
    means.sort()
    return percentile(means, 0.025), percentile(means, 0.975)
