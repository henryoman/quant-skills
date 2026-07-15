"""Explicit execution-cost model."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CostModel:
    fee_bps_per_side: float
    spread_bps_round_trip: float
    slippage_bps_round_trip: float
    funding_bps_per_trade: float = 0.0
    borrow_bps_per_trade: float = 0.0
    impact_bps_per_trade: float = 0.0
    safety_margin_bps: float = 0.0

    def __post_init__(self) -> None:
        values = asdict(self)
        for name, value in values.items():
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def round_trip_bps(self) -> float:
        return (
            2 * self.fee_bps_per_side
            + self.spread_bps_round_trip
            + self.slippage_bps_round_trip
            + self.funding_bps_per_trade
            + self.borrow_bps_per_trade
            + self.impact_bps_per_trade
            + self.safety_margin_bps
        )

    def net_return_bps(self, gross_return_bps: float) -> float:
        value = float(gross_return_bps)
        if not math.isfinite(value):
            raise ValueError("gross return must be finite")
        return value - self.round_trip_bps

    def stress(self, gross_return_bps: float, multiplier: float) -> float:
        if not math.isfinite(multiplier) or multiplier < 0:
            raise ValueError("multiplier must be finite and nonnegative")
        return float(gross_return_bps) - self.round_trip_bps * multiplier
