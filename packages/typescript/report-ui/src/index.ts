import { validateReportDocument, type EvidenceBlock, type ReportDocument } from "@quant/contracts";

const escapeHtml = (value: string): string =>
  value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");

function renderEvidence(block: EvidenceBlock, guided: boolean): string {
  const plot = block.plot;
  return `<section class="evidence" data-plot-id="${escapeHtml(plot.plotId)}">
    <p class="question">${escapeHtml(plot.question)}</p>
    <h2>${escapeHtml(block.finding)}</h2>
    <h3>${escapeHtml(plot.title)}</h3>
    <p class="scope">${escapeHtml(plot.subtitle)}</p>
    ${guided ? `<aside><strong>How to read</strong><p>${escapeHtml(plot.howToRead)}</p></aside>` : ""}
    <div class="plot" role="img" aria-label="${escapeHtml(plot.title)}" data-plot-kind="${plot.kind}"></div>
    ${plot.whatItShows ? `<p><strong>What it shows:</strong> ${escapeHtml(plot.whatItShows)}</p>` : ""}
    ${plot.whyItMatters ? `<p><strong>Why it matters:</strong> ${escapeHtml(plot.whyItMatters)}</p>` : ""}
    ${plot.whatItDoesNotProve ? `<p><strong>What it does not prove:</strong> ${escapeHtml(plot.whatItDoesNotProve)}</p>` : ""}
    <ul class="limitations">${block.limitations.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
  </section>`;
}

export function renderReport(document: ReportDocument): string {
  const errors = validateReportDocument(document);
  if (errors.length > 0) throw new Error(`Invalid report: ${errors.join("; ")}`);
  return `<article class="report profile-${document.profile}">
    <header><p class="scope">${escapeHtml(document.scope)}</p><h1>${escapeHtml(document.title)}</h1></header>
    <section class="decision"><strong>${escapeHtml(document.classification)}</strong><p>${escapeHtml(document.decision)}</p></section>
    ${document.evidence.map((block) => renderEvidence(block, document.profile === "graph_guided")).join("")}
    <section><h2>Rejected ideas</h2><ul>${document.rejectedIdeas.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
  </article>`;
}
