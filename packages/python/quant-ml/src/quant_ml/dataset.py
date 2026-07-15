"""Framework-neutral sequence-window construction."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowSpec:
    lookback_rows: int
    forecast_gap_rows: int = 1

    def __post_init__(self) -> None:
        if self.lookback_rows < 1:
            raise ValueError("lookback_rows must be positive")
        if self.forecast_gap_rows < 1:
            raise ValueError("forecast_gap_rows must be positive")


def build_supervised_windows(
    features: Sequence[Sequence[float]],
    targets: Sequence[float],
    spec: WindowSpec,
) -> tuple[list[list[list[float]]], list[float], list[int]]:
    """Build aligned windows and return their original target row indices."""
    if len(features) != len(targets):
        raise ValueError("features and targets must have equal length")
    windows: list[list[list[float]]] = []
    labels: list[float] = []
    indices: list[int] = []
    first_target = spec.lookback_rows - 1 + spec.forecast_gap_rows
    for target_index in range(first_target, len(features)):
        stop = target_index - spec.forecast_gap_rows + 1
        start = stop - spec.lookback_rows
        windows.append([[float(value) for value in row] for row in features[start:stop]])
        labels.append(float(targets[target_index]))
        indices.append(target_index)
    return windows, labels, indices
