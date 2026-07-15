"""Frontend-neutral evidence and report contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..plotting.specs import PlotSpec
from .profiles import ReportProfile


@dataclass(frozen=True)
class EvidenceBlock:
    block_id: str
    finding: str
    plot: PlotSpec
    exact_values: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ()

    def validate(self, profile: ReportProfile) -> list[str]:
        errors = [f"plot: {item}" for item in self.plot.validate()]
        if not self.finding.strip():
            errors.append("finding is required")
        if not self.limitations:
            errors.append("at least one limitation is required")
        if profile is ReportProfile.GRAPH_GUIDED:
            for name in ("what_it_shows", "why_it_matters", "what_it_does_not_prove"):
                if not getattr(self.plot, name).strip():
                    errors.append(f"graph-guided profile requires {name}")
        return errors


@dataclass(frozen=True)
class ReportDocument:
    report_id: str
    title: str
    decision: str
    classification: str
    scope: str
    profile: ReportProfile
    evidence: tuple[EvidenceBlock, ...]
    rejected_ideas: tuple[str, ...]
    provenance: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        for name in ("report_id", "title", "decision", "classification", "scope"):
            if not getattr(self, name).strip():
                errors.append(f"{name} is required")
        if not self.evidence:
            errors.append("at least one evidence block is required")
        if not self.rejected_ideas:
            errors.append("rejected ideas must be preserved")
        for block in self.evidence:
            errors.extend(f"{block.block_id}: {item}" for item in block.validate(self.profile))
        return errors

    def as_dict(self) -> dict[str, Any]:
        output = asdict(self)
        output["profile"] = self.profile.value
        return output
