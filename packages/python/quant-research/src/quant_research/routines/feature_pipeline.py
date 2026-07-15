"""Compose interpretable past-only indicators into aligned feature rows."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from quant_core.indicators.candle import candle_geometry
from quant_core.indicators.registry import INDICATORS, FeatureContext


REQUIRED_FIELDS = ("open", "high", "low", "close", "volume")


def _number(bar: Mapping[str, Any], field: str) -> float:
    try:
        value = float(bar[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"bar has invalid {field}") from exc
    if not math.isfinite(value):
        raise ValueError(f"bar has non-finite {field}")
    return value


def build_feature_row(history: Sequence[Mapping[str, Any]], lookbacks: Sequence[int]) -> dict[str, float]:
    """Build features observable at the close of the final completed bar."""
    normalized_lookbacks = sorted({int(item) for item in lookbacks})
    if not normalized_lookbacks or normalized_lookbacks[0] < 1:
        raise ValueError("lookbacks must be positive")
    if len(history) < max(normalized_lookbacks) + 1:
        raise ValueError("insufficient bar history")
    bars = history[-max(normalized_lookbacks) - 1 :]
    for bar in bars:
        for field in REQUIRED_FIELDS:
            _number(bar, field)

    current = bars[-1]
    previous = bars[-2]
    geometry = candle_geometry(
        _number(current, "open"),
        _number(current, "high"),
        _number(current, "low"),
        _number(current, "close"),
        previous_close=_number(previous, "close"),
    )
    output = {key: value for key, value in geometry.as_dict().items() if value is not None}
    closes = [_number(bar, "close") for bar in bars]
    highs = [_number(bar, "high") for bar in bars]
    lows = [_number(bar, "low") for bar in bars]
    volumes = [_number(bar, "volume") for bar in bars]
    context = FeatureContext(closes=closes, highs=highs, lows=lows, volumes=volumes)
    for lookback in normalized_lookbacks:
        suffix = f"_{lookback}"
        for indicator in INDICATORS:
            if lookback >= indicator.minimum_lookback:
                output[f"{indicator.name}{suffix}"] = indicator.compute(context, lookback)
    return output
