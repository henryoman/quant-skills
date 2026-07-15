import type { ReportDocument } from "@quant/contracts";
import { conditionalProfileSpec } from "@quant/plotting";
import { renderReport } from "@quant/report-ui";

const plot = {
  ...conditionalProfileSpec({
    feature: "relative volume",
    target: "next-minute return",
    unit: "bps",
    scope: "Example contract · no empirical claim",
  }),
  whatItShows: "No data is loaded in this shell.",
  whyItMatters: "The app renders validated research artifacts rather than recomputing results.",
  whatItDoesNotProve: "This example contains no evidence of alpha.",
};

const document: ReportDocument = {
  reportId: "studio-shell",
  title: "Quant Report Studio",
  decision: "Load a validated report artifact to begin.",
  classification: "no evidence loaded",
  scope: "Frontend boundary",
  profile: "graph_guided",
  evidence: [
    {
      blockId: "contract-example",
      finding: "Research computation remains outside the frontend",
      plot,
      exactValues: [],
      limitations: ["Static shell only", "No dataset connected"],
    },
  ],
  rejectedIdeas: ["Recomputing backtests inside UI components"],
  provenance: {},
};

const root = globalThis.document?.querySelector<HTMLElement>("#app");
if (root) root.innerHTML = renderReport(document);
