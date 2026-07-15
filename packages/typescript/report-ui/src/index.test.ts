import { describe, expect, test } from "bun:test";
import { conditionalProfileSpec } from "@quant/plotting";
import { renderReport } from "./index";

describe("report rendering", () => {
  test("escapes content and preserves rejected ideas", () => {
    const plot = {
      ...conditionalProfileSpec({ feature: "volume", target: "return", unit: "bps", scope: "test" }),
      whatItShows: "No stable lift",
      whyItMatters: "Costs dominate",
      whatItDoesNotProve: "Future failure",
    };
    const html = renderReport({
      reportId: "r1",
      title: "BTC <script>",
      decision: "Stop",
      classification: "rejected",
      scope: "BTCUSDT",
      profile: "graph_guided",
      evidence: [{ blockId: "b1", finding: "No edge", plot, exactValues: [], limitations: ["One venue"] }],
      rejectedIdeas: ["Naive momentum"],
      provenance: {},
    });
    expect(html).toContain("BTC &lt;script&gt;");
    expect(html).toContain("Naive momentum");
  });
});
