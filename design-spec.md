# EDITORIAL SVG REPORT DESIGN SPEC

Use this document to build research reports that look like finished editorial
graphics while remaining responsive, selectable, accessible, and inspectable in
the browser.

This system reproduces the visual method used by the Birdeye RWA report without
making React or a large chart runtime the foundation of the report. Ordinary
HTML and CSS must build the page. Charts must be build-time inline SVG. A small
vanilla JavaScript file is optional for exact-value tooltips only.

## 1. Required result

The report must feel like a designed publication, not a dashboard, notebook,
slide deck, or collection of UI cards.

- Use a nearly black page around pale, image-like chart plates.
- Put one substantial chart per row.
- Render charts as inline SVG, never as screenshots.
- Keep every chart sharp at any display density.
- Make the resting chart complete without hovering.
- Keep source data available in an adjacent native HTML table.
- Use JavaScript only when HTML, CSS, and SVG cannot provide the behavior.
- Do not load React, Recharts, D3, ECharts, Plotly, or another browser chart
  runtime merely to display a finished report.

The target architecture is:

```text
data file
  -> build-time chart generator
  -> semantic HTML document
       -> ordinary text and layout: HTML
       -> visual styling and responsiveness: CSS
       -> chart geometry: inline SVG
       -> exact values: native HTML table
       -> optional hover tooltip: one small vanilla JS module
```

## 2. Relationship to other rules

This is the implementation spec for the Birdeye-like editorial SVG style.
Analytical honesty, source requirements, and chart-selection rules in
`plot-rules.md` still apply.

This file intentionally makes two narrow visual exceptions:

1. A pale chart plate may sit on the black report page.
2. An area chart may use one same-color opacity fade from `35%` to `0%`.

These exceptions do not permit white notebook screenshots, multicolor
gradients, decorative glows, glass effects, or gradient-filled page furniture.

The original reference sometimes places charts side by side. This specification
does not. Our reports use one full-width chart per row so labels and evidence
remain readable.

## 3. Technology rule

### Default: build-time inline SVG

Generate the chart's coordinates while building the report and write the final
`<svg>` directly into the HTML. The browser should receive finished vector
marks, axes, labels, and gridlines.

This provides the important properties of the reference design:

- vector sharpness;
- responsive scaling;
- selectable and inspectable markup;
- a polished image-like resting state;
- no chart-library download or hydration delay;
- deterministic print and PDF output.

The generator may be written in Python, TypeScript, Rust, or another build-time
language. Its implementation is not shipped to the reader.

### Allowed fallback: Recharts in an existing React application

The reference report uses Next.js and Recharts. Recharts draws SVG and is an
acceptable adapter when a repository is already a React application and charts
must update in the browser.

It is not the default for a finished report. Do not add React to a static report
only to draw charts. If Recharts is used, its output must match the tokens,
dimensions, labels, SVG structure, and QA rules in this document.

### Forbidden defaults

- Do not use `<canvas>` for normal report charts.
- Do not use a PNG or JPEG as the primary chart.
- Do not use an iframe.
- Do not use a remote chart service.
- Do not require JavaScript for titles, sources, legends, units, caveats, or the
  basic ability to understand the figure.

## 4. Page anatomy

Use semantic HTML. The required hierarchy is:

```html
<body>
  <header class="report-header">...</header>

  <main class="report-shell">
    <article class="report-article">
      <section class="report-section" aria-labelledby="section-market">
        <header class="section-header">...</header>
        <div class="prose">...</div>

        <figure class="chart-figure" id="market-cap-chart">
          <header class="chart-header">...</header>
          <div class="chart-stage">...</div>
          <figcaption class="chart-caption">...</figcaption>
          <details class="chart-data">...</details>
        </figure>
      </section>
    </article>
  </main>

  <footer class="report-footer">...</footer>
</body>
```

Do not replace this structure with nested generic `<div>` elements. Do not wrap
every paragraph or section in a card.

## 5. Design tokens

Use these values unless a repository has an explicit brand token replacing the
same role.

```css
:root {
  color-scheme: dark;

  /* Page */
  --page: #0d0d0d;
  --page-deep: #000000;
  --page-text: #f6f6f6;
  --page-muted: #b0b0b0;
  --page-faint: #6d6d6d;
  --page-rule: rgba(255, 255, 255, 0.10);

  /* Chart plate */
  --plate: #f9f6ff;
  --plate-ink: #091320;
  --plate-muted: rgba(9, 19, 32, 0.68);
  --plate-faint: rgba(9, 19, 32, 0.46);
  --plate-grid: rgba(9, 19, 32, 0.07);
  --plate-border: rgba(9, 19, 32, 0.10);

  /* Reference-inspired chart palette */
  --series-primary: #be945b;
  --series-primary-light: #d3b48a;
  --series-primary-dark: #615a4f;
  --series-blue: #2c6499;
  --series-blue-light: #739cc1;
  --series-negative: #a5230f;
  --series-warning: #ed6109;
  --series-neutral: #9b9180;

  /* Geometry */
  --report-max: 1226px;
  --prose-max: 768px;
  --chart-max: 800px;
  --chart-height: 448px;
  --chart-radius: 2px;
  --chart-padding: 16px;
  --section-gap: clamp(64px, 9vw, 132px);
}
```

Use `--series-primary` for a normal single-series chart. For multiple series,
assign colors explicitly and preserve each mapping throughout the report. Never
allow a library to choose colors automatically.

## 6. Typography

Use one sans-serif family for report prose and chart text. Prefer a locally
hosted variable font. A safe stack is:

```css
font-family: Inter, Geist, ui-sans-serif, system-ui, -apple-system,
  BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Use tabular numerals for quantitative labels:

```css
.chart-figure,
table {
  font-variant-numeric: tabular-nums lining-nums;
}
```

Required sizes:

| Element | Size | Weight | Color |
|---|---:|---:|---|
| Report title | `clamp(40px, 7vw, 88px)` | `600` | page text |
| Section title | `clamp(24px, 4vw, 40px)` | `600` | page text |
| Body | `18px / 1.65` | `400` | page text at 80% opacity |
| Chart title | `20px / 1.4` | `600` | plate ink |
| Chart subtitle | `13px / 1.5` | `400` | plate muted |
| Axis labels | `14px` | `500` | plate ink |
| Legend and source | `12px` | `400` | plate muted |
| Tooltip | `12px` | `400–500` | plate ink |

Do not shrink axis text below `11px`. Increase height, reduce tick count, or
change chart form instead.

## 7. Base HTML document

Start from this document. Keep the visible content in HTML even when a framework
is used to assemble it.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="dark" />
    <title>Research report</title>
    <link rel="stylesheet" href="/report.css" />
  </head>

  <body>
    <header class="report-header">
      <div class="report-header__inner">
        <a class="wordmark" href="/">Research</a>
        <span class="report-kicker">Market structure report</span>
      </div>
    </header>

    <main class="report-shell">
      <article class="report-article">
        <header class="hero">
          <p class="eyebrow">H1 2026</p>
          <h1>Descriptive report title</h1>
          <p class="dek">
            One precise sentence explaining the population, period, and
            analytical subject.
          </p>
        </header>

        <section class="report-section" aria-labelledby="market-overview">
          <header class="section-header">
            <p class="eyebrow">01</p>
            <h2 id="market-overview">Market overview</h2>
          </header>

          <div class="prose">
            <p>
              Write the analytical context as connected prose. Quantify the
              important difference and state the relevant period.
            </p>
          </div>

          <!-- Insert chart figure here. -->
        </section>
      </article>
    </main>

    <footer class="report-footer">
      <p>Methods, provenance, and publication date.</p>
    </footer>

    <!-- Include only if optional tooltips are enabled. -->
    <!-- <script type="module" src="/report-tooltips.js"></script> -->
  </body>
</html>
```

## 8. Base CSS

Use plain CSS. A utility framework is unnecessary for this layout.

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  background: var(--page);
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-width: 320px;
  background: var(--page);
  color: var(--page-text);
  font-family: Inter, Geist, ui-sans-serif, system-ui, sans-serif;
  text-rendering: optimizeLegibility;
}

img,
svg {
  display: block;
  max-width: 100%;
}

a {
  color: inherit;
}

.report-header {
  position: relative;
  border-bottom: 1px solid var(--page-rule);
}

.report-header__inner,
.report-shell,
.report-footer {
  width: min(calc(100% - 40px), var(--report-max));
  margin-inline: auto;
}

.report-header__inner {
  display: flex;
  min-height: 64px;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.wordmark {
  font-weight: 650;
  text-decoration: none;
}

.report-kicker,
.eyebrow {
  color: var(--page-muted);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero {
  max-width: 1000px;
  padding-block: clamp(80px, 14vw, 184px);
}

.hero h1 {
  max-width: 13ch;
  margin: 12px 0 24px;
  font-size: clamp(40px, 7vw, 88px);
  font-weight: 600;
  letter-spacing: -0.045em;
  line-height: 0.98;
}

.dek {
  max-width: 62ch;
  margin: 0;
  color: var(--page-muted);
  font-size: clamp(18px, 2.2vw, 24px);
  line-height: 1.5;
}

.report-section {
  padding-block: var(--section-gap);
  border-top: 1px solid var(--page-rule);
}

.section-header,
.prose {
  width: min(100%, var(--prose-max));
  margin-inline: auto;
}

.section-header h2 {
  margin: 8px 0 0;
  font-size: clamp(24px, 4vw, 40px);
  line-height: 1.1;
}

.prose {
  margin-top: 36px;
  color: rgb(246 246 246 / 0.80);
  font-size: 18px;
  line-height: 1.65;
  text-align: left;
}

.prose p {
  margin: 0 0 24px;
}

.report-footer {
  margin-top: 100px;
  padding-block: 40px 80px;
  border-top: 1px solid var(--page-rule);
  color: var(--page-muted);
  font-size: 13px;
}

@media (max-width: 640px) {
  .report-header__inner,
  .report-shell,
  .report-footer {
    width: min(calc(100% - 28px), var(--report-max));
  }

  .report-kicker {
    display: none;
  }

  .prose {
    font-size: 16px;
  }
}
```

## 9. Required chart figure

Every chart must use this semantic wrapper.

```html
<figure class="chart-figure" id="rwa-share">
  <header class="chart-header">
    <h3>RWA market capitalization relative to stablecoins</h3>
    <p>
      Daily observations · Jan 2024–Jun 2026 · percent of stablecoin market cap
    </p>
  </header>

  <div class="chart-stage">
    <svg
      class="chart-svg"
      viewBox="0 0 768 448"
      role="img"
      aria-labelledby="rwa-share-title rwa-share-desc"
      preserveAspectRatio="xMidYMid meet"
    >
      <title id="rwa-share-title">
        RWA market capitalization relative to stablecoins
      </title>
      <desc id="rwa-share-desc">
        Area chart showing the percentage rising over the selected period.
      </desc>

      <defs>
        <linearGradient id="rwa-share-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#be945b" stop-opacity="0.35" />
          <stop offset="100%" stop-color="#be945b" stop-opacity="0" />
        </linearGradient>
        <clipPath id="rwa-share-clip">
          <rect x="72" y="20" width="671" height="374" />
        </clipPath>
      </defs>

      <g class="grid" aria-hidden="true">
        <line x1="72" y1="394" x2="743" y2="394" />
        <line x1="72" y1="300" x2="743" y2="300" />
        <line x1="72" y1="207" x2="743" y2="207" />
        <line x1="72" y1="113" x2="743" y2="113" />
        <line x1="72" y1="20" x2="743" y2="20" />
      </g>

      <g class="axis-labels" aria-hidden="true">
        <text x="60" y="398" text-anchor="end">0%</text>
        <text x="60" y="304" text-anchor="end">2.5%</text>
        <text x="60" y="211" text-anchor="end">5.0%</text>
        <text x="60" y="117" text-anchor="end">7.5%</text>
        <text x="60" y="24" text-anchor="end">10.0%</text>

        <text x="72" y="430" text-anchor="start">Jan 2024</text>
        <text x="240" y="430" text-anchor="middle">Aug 2024</text>
        <text x="408" y="430" text-anchor="middle">Mar 2025</text>
        <text x="576" y="430" text-anchor="middle">Oct 2025</text>
        <text x="743" y="430" text-anchor="end">Jun 2026</text>
      </g>

      <!-- The generator replaces these example paths with data-derived paths. -->
      <g clip-path="url(#rwa-share-clip)">
        <path class="area-fill" d="M72 350 ... L743 105 L743 394 L72 394 Z" />
        <path class="series-line" d="M72 350 ... L743 105" />
      </g>

      <!-- Optional build-time point targets for the tiny tooltip module. -->
      <g class="hit-targets" aria-hidden="true">
        <circle
          cx="743"
          cy="105"
          r="12"
          data-chart-point
          data-label="Jun 30, 2026"
          data-value="7.72%"
        />
      </g>
    </svg>

    <span class="chart-watermark" aria-hidden="true">RESEARCH</span>
    <output class="chart-tooltip" hidden></output>
  </div>

  <figcaption class="chart-caption">
    <p class="chart-reading">
      <strong>Read:</strong> the line gives RWA capitalization as a percentage
      of stablecoin capitalization; the shaded area emphasizes magnitude.
    </p>
    <p class="chart-source">Source: Artemis and RWA.xyz.</p>
  </figcaption>

  <details class="chart-data">
    <summary>View exact data</summary>
    <div class="table-scroll">
      <table>
        <caption>Values plotted in this figure</caption>
        <thead>
          <tr><th scope="col">Date</th><th scope="col">Share</th></tr>
        </thead>
        <tbody>
          <tr><td>2024-01-01</td><td>1.34%</td></tr>
          <tr><td>2026-06-30</td><td>7.72%</td></tr>
        </tbody>
      </table>
    </div>
  </details>
</figure>
```

Never leave `...` in shipped SVG paths. It is present above only to keep the
spec readable. The build step must write complete valid path data.

## 10. Chart CSS

```css
.chart-figure {
  width: min(100%, var(--chart-max));
  margin: clamp(48px, 8vw, 96px) auto 0;
  padding: var(--chart-padding);
  overflow: hidden;
  border: 0;
  border-radius: var(--chart-radius);
  background: var(--plate);
  color: var(--plate-ink);
  font-variant-numeric: tabular-nums lining-nums;
}

.chart-header {
  margin-bottom: 16px;
}

.chart-header h3 {
  margin: 0;
  color: var(--plate-ink);
  font-size: 20px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: -0.01em;
}

.chart-header p {
  margin: 4px 0 0;
  color: var(--plate-muted);
  font-size: 13px;
  line-height: 1.5;
}

.chart-stage {
  position: relative;
  min-height: var(--chart-height);
  isolation: isolate;
}

.chart-svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.chart-svg--narrow {
  display: none;
}

.grid line {
  stroke: var(--plate-grid);
  stroke-width: 2;
  vector-effect: non-scaling-stroke;
}

.axis-labels {
  fill: var(--plate-ink);
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
}

.area-fill {
  fill: url(#rwa-share-fill);
}

.series-line {
  fill: none;
  stroke: var(--series-primary);
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
  vector-effect: non-scaling-stroke;
}

.hit-targets circle {
  fill: transparent;
  stroke: transparent;
  pointer-events: all;
}

.chart-watermark {
  position: absolute;
  z-index: -1;
  inset: 50% auto auto 50%;
  translate: -50% -50%;
  color: var(--plate-ink);
  font-size: clamp(28px, 7vw, 60px);
  font-weight: 700;
  letter-spacing: 0.12em;
  opacity: 0.055;
  pointer-events: none;
  user-select: none;
  white-space: nowrap;
}

.chart-caption {
  margin-top: 20px;
  color: var(--plate-muted);
  font-size: 12px;
  line-height: 1.55;
}

.chart-caption p {
  margin: 4px 0 0;
}

.chart-caption strong {
  color: var(--plate-ink);
}

.chart-data {
  margin-top: 16px;
  border-top: 1px solid var(--plate-border);
  padding-top: 12px;
  color: var(--plate-muted);
  font-size: 12px;
}

.chart-data summary {
  width: fit-content;
  cursor: pointer;
  color: var(--plate-ink);
  font-weight: 600;
}

.table-scroll {
  margin-top: 12px;
  overflow-x: auto;
}

.chart-data table {
  width: 100%;
  border-collapse: collapse;
  color: var(--plate-ink);
}

.chart-data caption {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}

.chart-data th,
.chart-data td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--plate-border);
  text-align: left;
  white-space: nowrap;
}

.chart-data th:last-child,
.chart-data td:last-child {
  text-align: right;
}

.chart-tooltip {
  position: absolute;
  z-index: 5;
  max-width: 240px;
  padding: 8px;
  border: 1px solid #cccccc;
  background: #ffffff;
  color: var(--plate-ink);
  font-size: 12px;
  line-height: 1.4;
  pointer-events: none;
  transform: translate(10px, calc(-100% - 10px));
}

@media (max-width: 640px) {
  :root {
    --chart-height: 360px;
  }

  .chart-figure {
    padding: 12px;
  }

  .chart-header h3 {
    font-size: 16px;
  }

  .axis-labels {
    font-size: 12px;
  }

  .chart-svg--wide {
    display: none;
  }

  .chart-svg--narrow {
    display: block;
  }
}

@media print {
  body {
    background: #ffffff;
    color: #111111;
  }

  .chart-figure {
    break-inside: avoid;
    border: 1px solid #dddddd;
  }

  .chart-data:not([open]) {
    display: none;
  }
}
```

## 11. Build-time SVG contract

The generator receives reviewed rows and emits only chart geometry and labels.
Page layout stays in the HTML template.

Required input contract:

```json
{
  "id": "rwa-share",
  "type": "area",
  "title": "RWA market capitalization relative to stablecoins",
  "subtitle": "Daily observations · Jan 2024–Jun 2026 · percent",
  "source": "Artemis and RWA.xyz",
  "x": { "field": "date", "type": "date" },
  "y": { "field": "share", "type": "percent", "domain": [0, 0.10] },
  "series": [{ "field": "share", "label": "RWA / stablecoins", "color": "#be945b" }],
  "rows": []
}
```

Required output properties:

- one deterministic SVG `viewBox`;
- complete `<title>` and `<desc>` elements;
- four to six deliberate ticks per axis;
- complete path, line, rect, circle, and text geometry;
- no inline event handlers;
- no external font or image dependency inside the SVG;
- `vector-effect="non-scaling-stroke"` on important strokes;
- point targets with `data-label` and `data-value` only when tooltips are enabled;
- the exact HTML data table generated from the same rows;
- no invented interpolation across missing observations.

When scaling the desktop SVG would make labels smaller than `12px`, emit two
build-time SVG layouts from the same rows:

- `.chart-svg--wide` with `viewBox="0 0 768 448"` and five x-axis ticks;
- `.chart-svg--narrow` with `viewBox="0 0 360 360"` and three x-axis ticks.

Place both SVGs in the same `.chart-stage` and let the CSS media query select
one. Give the narrow SVG its own unique title, description, gradient, and clip
path IDs. This preserves readable text without resize JavaScript. Never produce
the two layouts from different data.

For a normal `800px` chart plate, use a `768 × 448` SVG after the plate's
`16px` left and right padding. Reserve approximately:

- left axis: `72px`;
- right breathing room: `25px`;
- top: `20px`;
- bottom labels: `54px`;
- plotting rectangle: `671 × 374px`.

## 12. Minimal optional JavaScript

Do not ship this file unless exact hover values materially improve the chart.
The report must remain understandable if this script fails or is disabled.

```js
// report-tooltips.js
for (const stage of document.querySelectorAll(".chart-stage")) {
  const tooltip = stage.querySelector(".chart-tooltip");
  if (!tooltip) continue;

  const show = (point) => {
    const box = stage.getBoundingClientRect();
    const pointBox = point.getBoundingClientRect();

    tooltip.textContent = `${point.dataset.label}: ${point.dataset.value}`;
    tooltip.style.left = `${pointBox.left - box.left + pointBox.width / 2}px`;
    tooltip.style.top = `${pointBox.top - box.top}px`;
    tooltip.hidden = false;
  };

  const hide = () => {
    tooltip.hidden = true;
  };

  for (const point of stage.querySelectorAll("[data-chart-point]")) {
    point.addEventListener("pointerenter", () => show(point));
    point.addEventListener("pointerleave", hide);
    point.addEventListener("focus", () => show(point));
    point.addEventListener("blur", hide);
  }
}
```

If keyboard access to individual points is required, set `tabindex="0"` and an
accurate `aria-label` on only the important points. Do not add hundreds of data
points to the tab order. The exact data table remains the complete accessible
representation.

## 13. Chart grammar

Use the smallest honest form for the comparison.

### Time series

- Use a line for change over time.
- Use the single-color area fade only when magnitude relative to zero matters.
- Use four or five x-axis ticks by default.
- Remove point markers from dense series; show only important endpoints or
  events.
- Never smooth a line in a way that changes extrema or timing.

### Category comparison

- Use sorted horizontal bars.
- Start the quantitative axis at zero.
- Put the category label and exact value next to the bar when space permits.
- Use one primary color plus a neutral comparator. Do not make every bar a
  different color.

### Composition over time

- Use stacked areas only when the total is meaningful.
- Use a maximum of five named components plus `Other`.
- Preserve stack order and colors everywhere.
- Pair shares with exact totals in the subtitle or table.

### Distribution

- Use a histogram for shape and an ECDF when threshold probability matters.
- Show sample size, bin policy, and relevant threshold.
- Do not use a decorative density curve without observed counts.

### Relationship

- Use scatter or hexbin depending on point count.
- Show sample size and observation grain.
- Make the important benchmark or break-even line visible.
- Do not use bubble size unless the third quantity changes the decision.

### Exact lookup

- Use a native HTML table.
- Right-align numeric cells.
- Keep units in column headings.
- Do not simulate a table with positioned SVG text.

## 14. Image-like finish without fake imagery

The polished effect comes from restraint and consistency, not decoration.

- Keep the chart plate flat and nearly square-cornered.
- Use the same `448px` stage height for ordinary figures.
- Use a `3px` main line with round joins.
- Use horizontal gridlines at approximately `7%` ink opacity.
- Remove y-axis tick marks and the visible y-axis rule.
- Keep the x-axis rule at approximately `7%` ink opacity.
- Use five deliberate date ticks instead of automatic crowded ticks.
- Use a faint centered project watermark, never the Birdeye trademark.
- Keep the tooltip white, square, small, and factual.
- Put source and note text immediately below the chart.
- Do not animate the chart on load.
- Do not add zoom controls, filters, dropdowns, or legends unless the evidence
  requires them.

## 15. Responsive rules

The SVG must use `viewBox` and scale with its container. Do not calculate width
in JavaScript.

At widths below `640px`:

- retain the same data and claim;
- reduce x-axis ticks from five to three if necessary;
- keep y-axis units visible;
- reduce plate padding from `16px` to `12px`;
- use at least `12px` axis text;
- increase SVG height when labels need more room;
- never rotate labels;
- never create page-level horizontal scrolling.

Tables may scroll inside `.table-scroll`. The report page may not.

## 16. Accessibility and fallback

Every chart must include:

- a visible HTML title and subtitle;
- SVG `<title>` and `<desc>`;
- `role="img"` and `aria-labelledby` on the SVG;
- units in visible text;
- a source;
- a nearby exact-value HTML table;
- a non-color distinction when multiple series could be confused;
- sufficient contrast for labels and lines;
- a complete interpretation that does not depend on hover.

When CSS is unavailable, the document order must still read correctly. When
JavaScript is unavailable, the chart, caption, source, and table must still work.

## 17. Data-density rules

Dense means more decision-relevant evidence, not more visual furniture.

- Each chart answers one explicit analytical question.
- Preserve enough observations to show the real shape.
- Remove redundant titles, repeated KPIs, duplicate legends, and decorative
  badges.
- Put exact supporting values in the table rather than covering the plot with
  labels.
- Label important breaks, thresholds, failures, and endpoints.
- Never hide weak periods, missing data, costs, or adverse observations.
- Never create a chart merely because a section exists.

## 18. Rules for an LLM implementing this spec

An LLM must follow this sequence:

1. Read the source data and state the chart question.
2. Choose the simplest chart family that answers it.
3. Define units, domain, tick policy, series mapping, source, and limitation.
4. Generate the semantic HTML wrapper.
5. Generate complete inline SVG at build time.
6. Generate the exact HTML data table from the same rows.
7. Apply the CSS tokens in this document.
8. Add optional tooltip JavaScript only if exact hover lookup is useful.
9. Render the report at desktop, tablet, and phone widths.
10. Inspect the actual result and revise all collisions or misleading scales.

The LLM must not:

- begin from a dashboard template;
- use generic cards for prose;
- output a screenshot of a chart;
- use a canvas renderer;
- install a browser chart library without a documented need;
- use automatic library colors or tick counts;
- omit the source or units;
- claim completion without inspecting the rendered report;
- leave placeholder SVG paths, invented values, or sample rows in production.

## 19. Acceptance checklist

- [ ] The page is nearly black and centered.
- [ ] Prose is no wider than `768px`.
- [ ] Each ordinary chart plate is no wider than `800px` and approximately
      `448px` tall inside.
- [ ] There is one chart per row.
- [ ] Every chart is inline SVG, not canvas or a bitmap.
- [ ] The page, title, caption, source, and data table work without JavaScript.
- [ ] Optional JavaScript is limited to progressive enhancement.
- [ ] The chart plate uses the pale reference surface and dark ink tokens.
- [ ] Main lines use explicit colors and consistent series mappings.
- [ ] Gridlines, ticks, and axes are quiet but readable.
- [ ] Area gradients, when used, are one-color opacity fades only.
- [ ] Every chart includes visible units, scope, source, and a reading note.
- [ ] Exact values come from the same reviewed rows as the SVG.
- [ ] Missing values are not rendered as zero.
- [ ] Nothing collides or clips at `1440px`, `768px`, and `390px` widths.
- [ ] The print/PDF rendering remains sharp and legible.
- [ ] The final rendered artifact has been visually inspected.

## 20. Short instruction

> Build the report as semantic HTML and plain CSS. Generate every chart as
> build-time inline SVG inside a `<figure>`; do not use canvas, screenshots, or a
> browser chart library by default. Use a nearly black page, an `800px` pale
> chart plate, a `448px` SVG stage, dark `#091320` chart ink, quiet horizontal
> gridlines, explicit series colors, a `3px` primary line, and at most a
> same-color `35%`-to-`0%` area fade. Keep titles, scope, units, reading notes,
> sources, and exact HTML tables visible without JavaScript. Add only a tiny
> optional vanilla-JS tooltip enhancement. Put one chart per row, test desktop,
> tablet, mobile, and print, and do not deliver before inspecting the result.
