"""Registry for extensible, past-only lookback indicators."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from .momentum import path_efficiency, trailing_log_return
from .range_location import range_position
from .volatility import realized_volatility
from .volume import relative_volume


@dataclass(frozen=True)
class FeatureContext:
    closes: Sequence[float]
    highs: Sequence[float]
    lows: Sequence[float]
    volumes: Sequence[float]


@dataclass(frozen=True)
class IndicatorDefinition:
    name: str
    family: str
    description: str
    minimum_lookback: int
    last_observable: str
    compute: Callable[[FeatureContext, int], float]


INDICATORS: tuple[IndicatorDefinition, ...] = (
    IndicatorDefinition(
        "trailing_log_return",
        "momentum",
        "Log return from the lookback close through the completed current close.",
        1,
        "bar_t_close",
        lambda context, lookback: trailing_log_return(context.closes, lookback),
    ),
    IndicatorDefinition(
        "path_efficiency",
        "path",
        "Net displacement divided by total absolute close-to-close movement.",
        1,
        "bar_t_close",
        lambda context, lookback: path_efficiency(context.closes, lookback),
    ),
    IndicatorDefinition(
        "relative_volume",
        "activity",
        "Current completed-bar volume divided by the median of prior bars only.",
        1,
        "bar_t_close",
        lambda context, lookback: relative_volume(context.volumes, lookback),
    ),
    IndicatorDefinition(
        "range_position",
        "range_location",
        "Current close position inside the completed trailing high-low range.",
        1,
        "bar_t_close",
        lambda context, lookback: range_position(context.highs, context.lows, context.closes[-1], lookback),
    ),
    IndicatorDefinition(
        "realized_volatility",
        "volatility",
        "Root-mean-square log return over the completed trailing window.",
        2,
        "bar_t_close",
        lambda context, lookback: realized_volatility(context.closes, lookback),
    ),
)


def indicator_names() -> tuple[str, ...]:
    return tuple(item.name for item in INDICATORS)


def get_indicator(name: str) -> IndicatorDefinition:
    for item in INDICATORS:
        if item.name == name:
            return item
    raise KeyError(name)
