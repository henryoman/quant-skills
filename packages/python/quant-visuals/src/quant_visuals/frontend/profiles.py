"""Presentation profiles kept independent from chart computation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ProfileSettings:
    prose_width_px: int
    evidence_width: str
    graph_explanation: str
    density: str
    accent_token: str


class ReportProfile(str, Enum):
    CURRENT = "current"
    MELLOW = "mellow"
    GRAPH_GUIDED = "graph_guided"

    @property
    def settings(self) -> ProfileSettings:
        return {
            ReportProfile.CURRENT: ProfileSettings(760, "full", "standard", "medium_high", "focus"),
            ReportProfile.MELLOW: ProfileSettings(760, "1040px", "concise", "low", "mellow_accent"),
            ReportProfile.GRAPH_GUIDED: ProfileSettings(760, "full", "required_guided_blocks", "medium_high", "focus"),
        }[self]
