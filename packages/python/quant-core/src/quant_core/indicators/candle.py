"""Normalized completed-bar geometry."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CandleGeometry:
    signed_body_fraction: float
    absolute_body_fraction: float
    upper_wick_fraction: float
    lower_wick_fraction: float
    close_location: float
    range_over_previous_close: float | None

    def as_dict(self) -> dict[str, float | None]:
        return asdict(self)


def candle_geometry(
    open_price: float,
    high: float,
    low: float,
    close: float,
    *,
    previous_close: float | None = None,
) -> CandleGeometry:
    """Describe one valid completed bar without candlestick-name folklore."""
    values = [float(open_price), float(high), float(low), float(close)]
    if not all(math.isfinite(item) and item > 0 for item in values):
        raise ValueError("OHLC prices must be finite and positive")
    open_price, high, low, close = values
    if high < max(open_price, close) or low > min(open_price, close) or high < low:
        raise ValueError("impossible OHLC relationship")
    bar_range = high - low
    if bar_range == 0:
        signed_body = absolute_body = upper_wick = lower_wick = 0.0
        close_location = 0.5
    else:
        signed_body = (close - open_price) / bar_range
        absolute_body = abs(close - open_price) / bar_range
        upper_wick = (high - max(open_price, close)) / bar_range
        lower_wick = (min(open_price, close) - low) / bar_range
        close_location = (close - low) / bar_range
    normalized_range = None
    if previous_close is not None:
        previous = float(previous_close)
        if not math.isfinite(previous) or previous <= 0:
            raise ValueError("previous_close must be finite and positive")
        normalized_range = bar_range / previous
    return CandleGeometry(
        signed_body_fraction=signed_body,
        absolute_body_fraction=absolute_body,
        upper_wick_fraction=upper_wick,
        lower_wick_fraction=lower_wick,
        close_location=close_location,
        range_over_previous_close=normalized_range,
    )
