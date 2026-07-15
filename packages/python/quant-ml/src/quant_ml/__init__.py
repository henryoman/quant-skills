"""Optional machine-learning adapters with no eager framework dependency."""

from .dataset import WindowSpec, build_supervised_windows
from .protocols import ProbabilisticModel

__all__ = ["ProbabilisticModel", "WindowSpec", "build_supervised_windows"]
