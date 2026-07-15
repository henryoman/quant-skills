import type { PlotSpec } from "@quant/contracts";

export function conditionalProfileSpec(input: {
  feature: string;
  target: string;
  unit: string;
  scope: string;
}): PlotSpec {
  return {
    plotId: `conditional-${input.feature}-${input.target}`,
    kind: "line",
    question: `How does ${input.target} change across ${input.feature}?`,
    title: `Conditional ${input.target} by training-defined ${input.feature} bin`,
    subtitle: input.scope,
    x: { field: "featureBin", label: `${input.feature} bin`, unit: "", scale: "category" },
    y: { field: "effect", label: input.target, unit: input.unit, scale: "linear", baseline: 0 },
    series: [
      { field: "effect", label: "Conditional effect", role: "primary", colorToken: "focus" },
      { field: "lower", label: "Lower interval", role: "uncertainty", colorToken: "interval" },
      { field: "upper", label: "Upper interval", role: "uncertainty", colorToken: "interval" },
    ],
    howToRead: "Move across training-defined bins and compare the effect with zero, the unconditional baseline, support, and uncertainty.",
    supportField: "sampleCount",
    uncertaintyMethod: "declare in provenance",
    provenance: {},
  };
}

export function costDelaySpec(scope: string): PlotSpec {
  return {
    plotId: "cost-delay-stress",
    kind: "heatmap",
    question: "Where does net expectancy survive plausible cost and execution delay?",
    title: "Net expectancy across cost and delay stress",
    subtitle: scope,
    x: { field: "extraCostBps", label: "Additional cost", unit: "bps", scale: "linear" },
    y: { field: "delayBars", label: "Execution delay", unit: "bars", scale: "linear" },
    series: [{ field: "netExpectancyBps", label: "Net expectancy", role: "primary", colorToken: "diverging" }],
    howToRead: "Verify that the plausible operating region remains above zero; an isolated zero-cost cell is fragile.",
    supportField: "tradeCount",
    provenance: {},
  };
}
