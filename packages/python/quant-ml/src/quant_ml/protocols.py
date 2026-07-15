"""Framework-neutral model contracts."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, TypeVar


FeatureRow = Sequence[float]
Target = TypeVar("Target")


class ProbabilisticModel(Protocol[Target]):
    def fit(self, features: Sequence[FeatureRow], targets: Sequence[Target]) -> "ProbabilisticModel[Target]": ...

    def predict_proba(self, features: Sequence[FeatureRow]) -> Sequence[Sequence[float]]: ...
