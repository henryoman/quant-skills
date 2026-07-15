import { describe, expect, test } from "bun:test";
import { validatePlotSpec, type PlotSpec } from "./index";

describe("plot contract", () => {
  test("requires support for heatmaps", () => {
    const spec: PlotSpec = {
      plotId: "cost-delay",
      kind: "heatmap",
      question: "Does expectancy survive?",
      title: "Cost and delay stress",
      subtitle: "Locked test",
      x: { field: "cost", label: "Cost", unit: "bps", scale: "linear" },
      y: { field: "delay", label: "Delay", unit: "bars", scale: "linear" },
      series: [{ field: "net", label: "Net", role: "primary", colorToken: "diverging" }],
      howToRead: "Inspect the plausible operating region.",
      provenance: {},
    };
    expect(validatePlotSpec(spec)).toContain("heatmaps require supportField");
  });
});
