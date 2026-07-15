"""Renderer-independent chart specifications."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ChartKind = Literal[
    "line",
    "bar",
    "scatter",
    "histogram",
    "heatmap",
    "drawdown",
    "calibration",
    "table",
]


@dataclass(frozen=True)
class AxisSpec:
    field: str
    label: str
    unit: str = ""
    scale: Literal["linear", "log", "time", "category"] = "linear"
    baseline: float | None = None


@dataclass(frozen=True)
class SeriesSpec:
    field: str
    label: str
    role: Literal["primary", "comparison", "uncertainty", "support"] = "primary"
    color_token: str = "focus"


@dataclass(frozen=True)
class PlotSpec:
    plot_id: str
    kind: ChartKind
    question: str
    title: str
    subtitle: str
    x: AxisSpec
    y: AxisSpec
    series: tuple[SeriesSpec, ...]
    how_to_read: str
    what_it_shows: str = ""
    why_it_matters: str = ""
    what_it_does_not_prove: str = ""
    support_field: str | None = None
    uncertainty_method: str | None = None
    provenance: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        for name in ("plot_id", "question", "title", "subtitle", "how_to_read"):
            if not getattr(self, name).strip():
                errors.append(f"{name} is required")
        if not self.series:
            errors.append("at least one series is required")
        if self.kind == "heatmap" and not self.support_field:
            errors.append("heatmaps require a support_field")
        return errors

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def as_contract(self) -> dict[str, Any]:
        """Return the language-neutral camelCase artifact consumed by TypeScript."""
        return {
            "plotId": self.plot_id,
            "kind": self.kind,
            "question": self.question,
            "title": self.title,
            "subtitle": self.subtitle,
            "x": asdict(self.x),
            "y": asdict(self.y),
            "series": [
                {
                    "field": item.field,
                    "label": item.label,
                    "role": item.role,
                    "colorToken": item.color_token,
                }
                for item in self.series
            ],
            "howToRead": self.how_to_read,
            "whatItShows": self.what_it_shows,
            "whyItMatters": self.why_it_matters,
            "whatItDoesNotProve": self.what_it_does_not_prove,
            "supportField": self.support_field,
            "uncertaintyMethod": self.uncertainty_method,
            "provenance": self.provenance,
        }
