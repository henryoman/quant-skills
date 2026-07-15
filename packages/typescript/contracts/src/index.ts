export type ReportProfile = "current" | "mellow" | "graph_guided";
export type PlotKind =
  | "line"
  | "bar"
  | "scatter"
  | "histogram"
  | "heatmap"
  | "drawdown"
  | "calibration"
  | "table";

export interface AxisSpec {
  field: string;
  label: string;
  unit: string;
  scale: "linear" | "log" | "time" | "category";
  baseline?: number;
}

export interface SeriesSpec {
  field: string;
  label: string;
  role: "primary" | "comparison" | "uncertainty" | "support";
  colorToken: string;
}

export interface PlotSpec {
  plotId: string;
  kind: PlotKind;
  question: string;
  title: string;
  subtitle: string;
  x: AxisSpec;
  y: AxisSpec;
  series: readonly SeriesSpec[];
  howToRead: string;
  whatItShows?: string;
  whyItMatters?: string;
  whatItDoesNotProve?: string;
  supportField?: string;
  uncertaintyMethod?: string;
  provenance: Readonly<Record<string, unknown>>;
}

export interface EvidenceBlock {
  blockId: string;
  finding: string;
  plot: PlotSpec;
  exactValues: readonly Readonly<Record<string, unknown>>[];
  limitations: readonly string[];
}

export interface ReportDocument {
  reportId: string;
  title: string;
  decision: string;
  classification: string;
  scope: string;
  profile: ReportProfile;
  evidence: readonly EvidenceBlock[];
  rejectedIdeas: readonly string[];
  provenance: Readonly<Record<string, unknown>>;
}

export function validatePlotSpec(spec: PlotSpec): string[] {
  const errors: string[] = [];
  for (const [field, value] of Object.entries({
    plotId: spec.plotId,
    question: spec.question,
    title: spec.title,
    subtitle: spec.subtitle,
    howToRead: spec.howToRead,
  })) {
    if (!value.trim()) errors.push(`${field} is required`);
  }
  if (spec.series.length === 0) errors.push("at least one series is required");
  if (spec.kind === "heatmap" && !spec.supportField) errors.push("heatmaps require supportField");
  return errors;
}

export function validateReportDocument(report: ReportDocument): string[] {
  const errors: string[] = [];
  if (report.evidence.length === 0) errors.push("at least one evidence block is required");
  if (report.rejectedIdeas.length === 0) errors.push("rejected ideas must be preserved");
  for (const block of report.evidence) {
    errors.push(...validatePlotSpec(block.plot).map((error) => `${block.blockId}: ${error}`));
    if (block.limitations.length === 0) errors.push(`${block.blockId}: at least one limitation is required`);
    if (report.profile === "graph_guided") {
      if (!block.plot.whatItShows) errors.push(`${block.blockId}: whatItShows is required`);
      if (!block.plot.whyItMatters) errors.push(`${block.blockId}: whyItMatters is required`);
      if (!block.plot.whatItDoesNotProve) errors.push(`${block.blockId}: whatItDoesNotProve is required`);
    }
  }
  return errors;
}
