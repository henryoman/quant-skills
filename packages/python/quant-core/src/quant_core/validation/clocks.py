"""Information-boundary contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InformationClock:
    feature_last_bar: int
    decision_bar: int
    order_bar: int
    execution_bar: int
    target_last_bar: int


def validate_information_clock(clock: InformationClock) -> list[str]:
    """Return clock violations without guessing how to repair them."""
    errors: list[str] = []
    if clock.feature_last_bar > clock.decision_bar:
        errors.append("feature uses information after the decision bar")
    if clock.decision_bar > clock.order_bar:
        errors.append("order precedes the decision")
    if clock.order_bar > clock.execution_bar:
        errors.append("execution precedes the order")
    if clock.target_last_bar <= clock.execution_bar:
        errors.append("target does not extend beyond execution")
    return errors
