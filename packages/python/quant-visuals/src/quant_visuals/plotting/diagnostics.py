"""Factories for required quantitative diagnostic plots."""

from __future__ import annotations

from .specs import AxisSpec, PlotSpec, SeriesSpec


def conditional_profile_spec(*, feature: str, target: str, unit: str, scope: str) -> PlotSpec:
    return PlotSpec(
        plot_id=f"conditional-{feature}-{target}",
        kind="line",
        question=f"How does {target} change across {feature}?",
        title=f"Conditional {target} by training-defined {feature} bin",
        subtitle=scope,
        x=AxisSpec(field="feature_bin", label=f"{feature} bin", scale="category"),
        y=AxisSpec(field="effect", label=target, unit=unit, baseline=0.0),
        series=(
            SeriesSpec(field="effect", label="Conditional effect", role="primary", color_token="focus"),
            SeriesSpec(field="lower", label="Lower interval", role="uncertainty", color_token="interval"),
            SeriesSpec(field="upper", label="Upper interval", role="uncertainty", color_token="interval"),
        ),
        how_to_read="Move left to right across training-defined bins; compare the effect with zero, the unconditional baseline, and its uncertainty interval.",
        support_field="sample_count",
        uncertainty_method="declare in figure provenance",
    )


def support_heatmap_spec(*, x_feature: str, y_feature: str, outcome: str, unit: str, scope: str) -> PlotSpec:
    return PlotSpec(
        plot_id=f"heatmap-{x_feature}-{y_feature}-{outcome}",
        kind="heatmap",
        question=f"Does {outcome} change across the joint {x_feature} and {y_feature} state?",
        title=f"Conditional {outcome} by {x_feature} × {y_feature}",
        subtitle=scope,
        x=AxisSpec(field="x_bin", label=f"{x_feature} bin", scale="category"),
        y=AxisSpec(field="y_bin", label=f"{y_feature} bin", scale="category"),
        series=(SeriesSpec(field="effect", label=outcome, role="primary", color_token="diverging"),),
        how_to_read="Read each cell as a conditional effect and inspect the paired support count; prefer broad supported regions over isolated extreme cells.",
        support_field="sample_count",
        uncertainty_method="block bootstrap or dependence-aware interval",
        provenance={"unit": unit},
    )


def cost_stress_spec(*, scope: str) -> PlotSpec:
    return PlotSpec(
        plot_id="cost-delay-stress",
        kind="heatmap",
        question="Where does net expectancy survive plausible cost and execution delay?",
        title="Net expectancy across cost and delay stress",
        subtitle=scope,
        x=AxisSpec(field="extra_cost_bps", label="Additional round-trip cost", unit="bps"),
        y=AxisSpec(field="delay_bars", label="Execution delay", unit="bars"),
        series=(SeriesSpec(field="net_expectancy_bps", label="Net expectancy", color_token="diverging"),),
        how_to_read="Find the plausible operating region and verify it remains above zero; an isolated zero-cost, zero-delay cell is not deployable evidence.",
        support_field="trade_count",
    )
