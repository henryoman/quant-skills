# LIQ DLMM HTML Report Design Guide

> **Status:** domain-specific companion for durable LIQ DLMM and trading-research HTML reports. For the general visual system, use `report-design.md`.
> **Audience:** humans and agents authoring research reports, strategy notes, experiment summaries, wallet analyses, and operator-facing evidence.
> **Reference reports:** `H96_MANUAL_DLMM_FUTURE_EDGE_AND_ENTRY_FILTERS_2026_07_13.html` and `H96_UPDATE_2026_07_13.html`.
> **Scope:** what a report looks like, how it communicates, how every chart and table is constructed, and how a self-contained HTML artifact behaves in the `/reports` iframe, on mobile, and in print.

This guide is intentionally prescriptive. LIQ reports are not miniature marketing sites and not generic dashboards. They are durable research artifacts used to make or audit trading decisions. Their visual job is to shorten the path from **question → evidence → interpretation → decision → caveat → source** without making weak evidence look strong.

The default report is a minimal, black, high-contrast research memo with excellent graphs. It should feel closer to a carefully typeset trading notebook than an app dashboard: one reading column, restrained type, hairline dividers, compact metrics, plain tables, and charts that explain themselves. Richness comes from evidence and annotation, not decoration.

---

## 1. Normative language

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are requirements:

- **MUST / MUST NOT:** required for a report to be considered conforming.
- **SHOULD / SHOULD NOT:** expected unless a specific analytical reason is documented.
- **MAY:** optional and context-dependent.

When visual taste conflicts with analytical legibility, analytical legibility wins. When visual emphasis conflicts with statistical importance, statistical importance wins.

---

## 2. The visual thesis

### 2.1 Subject, audience, and single job

- **Subject:** evidence about DLMM positions, pools, strategies, wallet behavior, market state, execution friction, and risk.
- **Primary audience:** an operator or researcher who already understands trading but needs to see what changed, why it matters, and how trustworthy the result is.
- **Single job:** enable a correct evidence-based decision or a correct statement that no decision is justified.

### 2.2 House character

The house style is **instrument-panel restraint plus research-memo clarity**:

- black working canvas;
- white and gray typography;
- mono numerals;
- one-pixel rules rather than decorative containers;
- charts treated as measured evidence, not illustration;
- semantic color used sparingly and redundantly;
- source and sample context kept visually attached to claims;
- dense information, calm spacing, no ornamental clutter.

### 2.3 Signature element: the evidence rail

Every important visual MUST have a three-part evidence rail:

```text
Finding / question stated as a sentence
┌──────────────────────────────────────────────────────────────┐
│ chart, table, or analytical diagram                          │
└──────────────────────────────────────────────────────────────┘
Sample · unit · period · method · uncertainty · source
```

The rail is not a literal box. Usually it is:

1. a short, claim-led heading above the visual;
2. the unframed visual;
3. a compact caption below it containing sample, unit, period, method, and source.

This is the memorable LIQ device. It prevents a graph from floating free of the evidence that gives it meaning.

### 2.4 What “minimal” means

Minimal does **not** mean sparse, vague, or under-labeled. It means every visible mark does analytical work.

- A gridline helps estimate a value: keep it.
- A second border repeats an existing boundary: remove it.
- A legend makes the reader shuttle between names and marks: directly label the marks instead.
- A color encodes the same thing already encoded by vertical position: usually remove it.
- An annotation identifies a policy threshold, regime break, outlier, or data gap: keep it.
- A KPI repeats a number already stated in the opening sentence: do not promote it to a card.

---

## 3. Lessons from the reference reports

### 3.1 Keep from the future-edge notebook

The future-edge report demonstrates useful restraint:

- a bounded reading width;
- strong title, plain metadata, then immediate executive summary;
- short prompts or section labels beside longer outputs;
- simple HTML bars for a single comparison;
- dense tables with tabular numerals;
- plain semantic callouts for warning, evidence, and positive findings;
- conclusions that distinguish observation from promotion-ready policy;
- explicit caveats and next questions.

### 3.2 Keep from the strategy-update artifact

The strategy-update report demonstrates useful rigor:

- self-contained HTML with a restrictive content-security policy;
- light, dark, mobile, and print behavior;
- a strong sequence from summary metrics to mechanics, performance path, concentration, losses, controls, and sources;
- vector chart fallbacks and accessible chart-data tables;
- visible sample counts, units, definitions, and source provenance;
- truncated large tables with honest result counts;
- responsive tables rather than crushed columns;
- print-safe visuals and deliberate page-break behavior.

### 3.3 Do not copy blindly

These examples are references, not pixel templates. New reports SHOULD improve on them:

- Prefer the repository’s black report surface over a generic white analytical page.
- Prefer divider rows over repeated rounded metric cards.
- Avoid a sticky report header inside the `/reports` viewer; the surrounding viewer already supplies navigation context.
- Avoid excessive source tooltips. Put concise source context in the evidence rail and full provenance in `Sources`.
- Avoid hundreds of DOM nodes for a chart when a compact inline SVG or semantic HTML bar chart will do.
- Avoid displaying raw precision that exceeds the measurement’s precision.

---

## 4. Page anatomy

### 4.1 Canonical reading order

Every report SHOULD use this order:

1. **Header** — title, exact scope, status, generated time, data cutoff.
2. **Read** — the shortest defensible answer to the report’s question.
3. **Decision** — what changes now, what remains unchanged, and why.
4. **Key numbers** — 3–6 numbers needed to understand magnitude and uncertainty.
5. **Evidence path** — visuals ordered to build the argument, not grouped by chart type.
6. **Failure cases / counterevidence** — where the thesis does not hold.
7. **Risk and caveats** — data gaps, confounding, selection bias, dependence, and execution constraints.
8. **Next run** — preregistered follow-up, required sample, and promotion criteria.
9. **Sources and reproduction** — source paths, time coverage, query/build command, artifact timestamp.

Use `Read`, `Decision`, `Evidence`, `Counterevidence`, `Risk`, `Next run`, and `Sources` when those names fit. Avoid `Overview`, `Insights`, and `Analytics` when a more informative heading exists.

### 4.2 Narrative wireframe

```text
┌───────────────────────────────────────────────────────────────┐
│ KICKER / STATUS                                  DATA CUTOFF  │
│ Report title                                                   │
│ Scope sentence: population, period, unit, exclusions           │
├───────────────────────────────────────────────────────────────┤
│ READ                                                          │
│ One to three sentences with the result and confidence.         │
├───────────────────────────────────────────────────────────────┤
│ metric      metric       metric       metric                   │
├───────────────────────────────────────────────────────────────┤
│ DECISION                                                      │
│ change / no change / shadow-only / blocked                     │
├───────────────────────────────────────────────────────────────┤
│ Evidence heading stated as a finding                           │
│                                                               │
│                     PRIMARY CHART                              │
│                                                               │
│ n · unit · range · method · source                             │
├───────────────────────────────────────────────────────────────┤
│ Secondary chart                 Compact supporting table       │
├───────────────────────────────────────────────────────────────┤
│ COUNTEREVIDENCE / FAILURE CASES                                │
├───────────────────────────────────────────────────────────────┤
│ RISK · NEXT RUN · SOURCES                                     │
└───────────────────────────────────────────────────────────────┘
```

### 4.3 One visual, one question

Every chart MUST answer one written question. If a chart cannot be introduced by one sentence, it is probably combining too many analytical jobs.

Good:

- “Did cumulative realized P&L recover after the July 8 drawdown?”
- “Which duration cohorts contain most gross loss?”
- “Does higher prior-hour volume correspond to lower catastrophe rate?”

Bad:

- “Performance analytics.”
- “Strategy metrics.”
- “Interesting patterns.”

### 4.4 The first viewport

At a typical iframe viewport, the first screen SHOULD reveal:

- what the report is about;
- the sample and cutoff;
- the primary answer;
- the decision status;
- at least the beginning of the first evidence visual.

Do not spend the first viewport on a giant title, abstract illustration, navigation, or decorative summary cards.

---

## 5. Foundations and tokens

### 5.1 Canonical tokens

```css
:root {
  color-scheme: dark;

  /* Surfaces */
  --report-bg: #000000;
  --report-surface: #080808;
  --report-surface-raised: #101010;

  /* Type */
  --report-ink: #f5f5f5;
  --report-muted: #b8b8b8;
  --report-faint: #7a7a7a;

  /* Rules and chart scaffolding */
  --report-line: #242424;
  --report-line-strong: #3a3a3a;
  --report-grid: #202020;

  /* Series */
  --chart-primary: #f5f5f5;
  --chart-secondary: #a8a8a8;
  --chart-tertiary: #686868;
  --chart-focus: #67b7ff;

  /* Semantics — never rely on these without text/sign/shape */
  --positive: #58c978;
  --negative: #ff6b66;
  --warning: #e4b84c;
  --unknown: #909090;

  /* Typography */
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;

  /* Geometry */
  --measure-copy: 72ch;
  --measure-report: 1120px;
  --measure-wide: 1280px;
  --radius-functional: 4px;
}
```

### 5.2 Color rules

1. The report canvas MUST be `#000` or visually indistinguishable from it.
2. Body text SHOULD be slightly below pure white; chart labels MAY use pure white when small.
3. Gray carries comparison, secondary information, gridlines, metadata, and unavailable state.
4. Blue is a **focus series**, selected cohort, link, or interactive state—not generic decoration.
5. Green and red are reserved for outcome semantics. They MUST be paired with a sign, label, arrow, line style, or position.
6. Amber means uncertainty, warning, provisional, or research-only. It MUST NOT mean “neutral.”
7. Never use a rainbow categorical palette.
8. Never use red versus green as the only differentiator.
9. A single chart SHOULD use no more than three neutral series plus one focus series.
10. A page SHOULD contain no more than one high-chroma focus color at a time.

### 5.3 Type system

Use the system sans stack for prose and the mono stack for numbers, timestamps, addresses, hashes, units embedded in values, and source paths.

| Role | Size | Line height | Weight | Notes |
|---|---:|---:|---:|---|
| Report title | `clamp(30px, 4vw, 42px)` | `1.04` | `700` | Sentence case; max ~20 words |
| Deck / scope | `15–17px` | `1.55` | `400` | Max `72ch` |
| Section title | `18px` | `1.25` | `650` | Names the analytical job |
| Visual finding | `15–16px` | `1.35` | `650` | A sentence, not a chart noun |
| Body | `15px` | `1.65` | `400` | Default reading text |
| Table | `12–13px` | `1.45` | `400` | Numerals tabular |
| Metadata | `11–12px` | `1.4` | `500` | Mono; uppercase only for very short labels |
| Axis / direct label | `11–12px` | `1.2` | `500` | Never smaller than `10px` |

Typography requirements:

- Use `font-variant-numeric: tabular-nums lining-nums` on metrics, tables, axes, and captions.
- Do not uppercase long headings or prose.
- Do not use light font weights on dark backgrounds.
- Do not center body text, captions, tables, or chart headings.
- Keep prose line length between `55ch` and `78ch`.
- Use real minus signs (`−`) in static prose when practical; machine-rendered signed values MAY use `-`.
- Keep unit style consistent: `2.52 SOL`, `−333 bps`, `14.8%`, `42 min`, `2026-07-13 18:00 UTC`.

### 5.4 Spacing system

Use a 4px base rhythm:

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

- Related label/value pairs: `4–8px`.
- Chart title to chart: `12–16px`.
- Chart to evidence caption: `8–12px`.
- Paragraph to paragraph: `10–14px`.
- Section internal padding: `24–32px`.
- Major analytical chapter separation: `40–56px` plus a rule.
- Page padding: `28px 24px 64px` desktop; `20px 16px 48px` mobile.

### 5.5 Lines, surfaces, and radius

- Default section separator: `1px solid var(--report-line)`.
- Major separator: `1px solid var(--report-line-strong)`.
- Tables use horizontal row rules, not full cell grids.
- A chart does not need a border when its plotting area is clear.
- Radius is functional only: `4px` for focusable controls, code, or a bounded warning.
- No shadows.
- No gradients.
- No glass effects.
- No nested panels.
- No floating cards for ordinary narrative sections.

---

## 6. Layout

### 6.1 Main container

```css
.report {
  width: min(calc(100% - 48px), var(--measure-report));
  margin-inline: auto;
  padding-block: 28px 64px;
}

.prose { max-width: var(--measure-copy); }
.wide { width: min(100%, var(--measure-wide)); }
```

The report MUST remain readable inside the `/reports` iframe, where the viewer sidebar reduces available width. Do not assume a full desktop browser width.

### 6.2 Columns

- One column is the default.
- Two columns MAY be used for two directly comparable visuals or a visual plus a short supporting table.
- Two columns MUST collapse by `760px`.
- A prose section SHOULD NOT use newspaper columns.
- A chart plus prose rail MAY use `minmax(0, 2fr) minmax(220px, 1fr)` only when the prose rail contains interpretation specific to that chart.
- Three or more columns are reserved for a compact metric strip, never long-form content.

```css
.split {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 32px;
}

@media (max-width: 760px) {
  .split { grid-template-columns: minmax(0, 1fr); gap: 24px; }
}
```

### 6.3 Section framing

```css
.report-section {
  padding-block: 28px;
  border-top: 1px solid var(--report-line);
}

.report-section:first-of-type {
  border-top-color: var(--report-line-strong);
}
```

Do not wrap `.report-section` in a card. The page itself is the surface.

### 6.4 Density

Dense is acceptable when hierarchy remains obvious:

- tables may show 10–25 rows by default;
- primary charts should usually be `280–460px` tall;
- small multiples may be `120–180px` each;
- metric strips should be one or two rows;
- captions remain adjacent to their visual;
- every long table has a short sentence telling the reader what to look for.

---

## 7. Report header, status, and scope

### 7.1 Required header content

Every report MUST show:

- a specific title;
- the population or subject;
- the analysis period and timezone;
- the data cutoff or generated timestamp;
- inclusion/exclusion scope;
- decision status: `descriptive`, `research-only`, `shadow`, `validated`, `promoted`, `blocked`, or `superseded`.

```html
<header class="report-header">
  <div class="report-kicker">Research-only · H96 manual DLMM</div>
  <h1>Future edge and entry filters</h1>
  <p class="report-deck">
    Complete reconstructed closes through 2026-07-13 00:10 UTC;
    open and ambiguous positions excluded.
  </p>
  <dl class="report-meta">
    <div><dt>Sample</dt><dd>222 positions / 61 pools</dd></div>
    <div><dt>Unit</dt><dd>SOL, ROI, bps</dd></div>
    <div><dt>Generated</dt><dd>2026-07-13 18:22 UTC</dd></div>
  </dl>
</header>
```

### 7.2 Status is analytical, not decorative

Status MAY be styled with a short label and a rule. Avoid pill-shaped badges unless the status is interactive. The status text MUST explain its consequence nearby:

- `Research-only — do not bind to a live strategy.`
- `Shadow — log decisions but do not reject entries.`
- `Validated — passed the declared holdout criteria.`
- `Superseded — retain for provenance; do not use as current policy.`

---

## 8. Executive read and decision block

### 8.1 The read

The first paragraph SHOULD contain:

1. direction and magnitude;
2. sample and independent unit;
3. uncertainty or the primary limitation;
4. whether the result changes live behavior.

Example:

> The expected-positive shadow score improved mean holdout ROI by 4.29 points across 36 positions, but its pool-clustered interval crossed zero and accepted only 10 positions from 7 pools. Keep it shadow-only; no live entry binding changes.

### 8.2 Decision syntax

Use one of these explicit forms:

- **Change:** what changes, exact scope, effective artifact/config, and why.
- **No change:** what remains unchanged and what evidence is missing.
- **Shadow:** what is logged, how it is scored, and the promotion test.
- **Blocked:** missing data/quality/execution precondition.

Avoid “looks promising,” “strong signal,” or “significant” without a numeric definition.

### 8.3 Callouts

Callouts are for exceptional interpretive states, not ordinary paragraphs.

```css
.callout {
  padding: 12px 0 12px 16px;
  border-left: 3px solid var(--report-line-strong);
}
.callout[data-tone="warning"] { border-left-color: var(--warning); }
.callout[data-tone="negative"] { border-left-color: var(--negative); }
.callout[data-tone="positive"] { border-left-color: var(--positive); }
```

Each callout MUST contain a label and an action or interpretation. Color alone is insufficient.

---

## 9. Metrics and number formatting

### 9.1 Metric selection

Show only metrics needed to interpret the report’s main claim. A typical strategy report uses:

- sample size and independent cluster count;
- net P&L;
- mean or median ROI;
- profit factor or expectancy;
- max drawdown;
- bad-loss/catastrophe rate;
- fee floor or execution-cost hurdle;
- confidence/uncertainty range.

Do not show vanity counts or duplicate a chart endpoint as a KPI unless it anchors the entire report.

### 9.2 Metric strip

```html
<dl class="metric-strip" aria-label="Key results">
  <div>
    <dt>Realized net</dt>
    <dd class="num">+2.522 SOL</dd>
    <small>222 complete closes</small>
  </div>
  <div>
    <dt>Profit factor</dt>
    <dd class="num">1.37×</dd>
    <small>gross wins / gross losses</small>
  </div>
  <div>
    <dt>Max drawdown</dt>
    <dd class="num">−1.118 SOL</dd>
    <small>close-by-close equity</small>
  </div>
</dl>
```

```css
.metric-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  margin: 24px 0 0;
  border-block: 1px solid var(--report-line);
}
.metric-strip > div {
  min-width: 0;
  padding: 14px 16px;
  border-right: 1px solid var(--report-line);
}
.metric-strip > div:last-child { border-right: 0; }
.metric-strip dt { color: var(--report-muted); font-size: 12px; }
.metric-strip dd { margin: 4px 0 0; font: 650 20px/1.15 var(--font-mono); }
.metric-strip small { display: block; margin-top: 5px; color: var(--report-faint); }
```

### 9.3 Precision rules

Precision MUST reflect decision usefulness:

| Measure | Default display | Example |
|---|---:|---|
| SOL P&L under 0.1 | 4 decimals | `+0.0779 SOL` |
| SOL P&L 0.1–10 | 3 decimals | `−1.118 SOL` |
| Large SOL aggregate | 2 decimals | `+24.61 SOL` |
| ROI / rates | 1 decimal | `14.8%` |
| Close comparisons | 2 decimals | `+4.29 pp` |
| Basis points | whole or 1 decimal | `−333.4 bps` |
| Counts | integer | `222` |
| Ratios | 2 decimals | `1.37×` |
| Probability | 2 decimals or percent | `0.18` / `18%` |
| Duration | sensible unit | `42.9 min`, `7.3 h` |

- Keep extra precision in downloadable/source data, not in the visible report.
- Use `pp` for percentage-point differences and `%` for relative percentages.
- State denominators: `10 / 36 (27.8%)`, not only `27.8%`.
- Use `n/a` for not applicable and `—` for absent; explain the distinction in a table note.
- Never coerce missing values to zero.

---

## 10. The chart contract

Every chart MUST satisfy all of the following.

### 10.1 Above the plot

- A finding-led title or explicit analytical question.
- Optional one-sentence interpretation if the conclusion is not obvious.
- No redundant title inside the SVG/canvas.

### 10.2 Inside the plot

- Clear axes and units.
- A visible zero, baseline, or policy threshold when analytically relevant.
- Direct labels for the primary series or important endpoints.
- Honest scales and consistent ordering.
- Uncertainty marks when uncertainty was estimated.
- Annotations only for decision-relevant events or outliers.

### 10.3 Below the plot

- Sample size and independent unit.
- Date range and timezone.
- Aggregation/estimator.
- Exclusions or missing-data count.
- Uncertainty method if shown.
- Source path or short source name.
- An accessible data table, visible or disclosed, for nontrivial charts.

### 10.4 Example evidence rail

```html
<figure class="evidence-figure">
  <figcaption>
    <strong>Most gains arrived after the deepest drawdown.</strong>
    <span>The cumulative path recovered from −1.12 SOL to finish at +2.52 SOL.</span>
  </figcaption>
  <div class="chart" aria-label="Cumulative realized net P and L by close sequence">
    <!-- inline SVG -->
  </div>
  <p class="evidence-note">
    n=222 complete closes · close order · SOL · 2026-07-04–2026-07-12 UTC ·
    no interpolation · source: position_fee_inclusive_outcomes.csv
  </p>
  <details class="chart-data">
    <summary>Chart data</summary>
    <!-- compact semantic table -->
  </details>
</figure>
```

---

## 11. Choosing the correct visual

Choose based on the analytical question, never based on variety.

| Question | Preferred visual | Avoid |
|---|---|---|
| How did a value evolve over ordered time/events? | line or step chart | unordered bars |
| What caused an aggregate to move? | waterfall | pie chart |
| Which categories are larger/smaller? | sorted horizontal bars | donut, 3D bars |
| How are outcomes distributed? | histogram + median/quantiles; ECDF for tails | mean-only bar |
| What is the relationship between two continuous variables? | scatter + transparent points + fit/interval if justified | connected scatter points |
| How do two dimensions interact? | heatmap with fixed scale and cell counts | rainbow surface |
| How do cohorts compare with uncertainty? | dot-and-whisker | bars with hidden intervals |
| What fraction belongs to a few categories? | sorted bars or cumulative Pareto | pie with many slices |
| How do actual and baseline differ? | paired dots, slopegraph, or difference bars | two unrelated charts |
| Is a DLMM position in range? | bin/range strip with active marker | generic gauge |
| What happened across a trade lifecycle? | event timeline / state strip | decorative flowchart |
| Which observations drive risk? | ranked loss bars + cumulative share | word cloud |
| How stable is a result across folds/pools? | small multiples or forest plot | aggregate KPI only |
| Exact values and lookup matter most? | table | chart for chart’s sake |

If the reader needs exact values for many rows, use a table. If the reader needs shape, trend, ranking, concentration, or relationship, use a chart. Often the correct answer is a chart followed by a short table of the most important rows.

---

## 12. Chart anatomy and geometry

### 12.1 Plot dimensions

- Primary chart: width `100%`, target height `320–440px`.
- Secondary chart: `240–340px`.
- Small multiple: `120–180px` per panel.
- Minimum useful plot width: `280px` after margins.
- Use `viewBox` SVGs so charts scale without losing sharpness.
- Do not set only CSS width/height on an SVG without a matching `viewBox`.

### 12.2 Margins

Default SVG plot margins:

```js
const margin = { top: 18, right: 72, bottom: 42, left: 58 };
```

Adjust based on labels, not habit:

- long y tick labels require a wider left margin;
- direct endpoint labels require a wider right margin;
- rotated x labels require a deeper bottom margin;
- prefer fewer or abbreviated labels before rotating text.

### 12.3 Scales

- Bar charts MUST start their quantitative axis at zero.
- Line/scatter charts MAY use a nonzero domain when shape requires it, but MUST make the domain clear and MUST NOT imply an area comparison.
- Diverging charts SHOULD use a symmetric domain around zero when positive and negative magnitudes are compared.
- Related small multiples MUST share scales unless the purpose is explicitly local shape comparison and each scale is labeled.
- Log scales MUST say `log` in the axis title and SHOULD annotate meaningful powers.
- Do not silently clip outliers. If clipping is required, show a break/clipped mark and state the count.
- Time axes MUST state timezone.

### 12.4 Axes and ticks

- Axis titles include the unit unless every tick already contains it.
- Prefer 4–6 labeled ticks per quantitative axis.
- Horizontal gridlines MAY follow y ticks; vertical gridlines are usually unnecessary.
- Draw the zero line stronger than ordinary gridlines.
- Avoid an enclosing plot box.
- Do not repeat `%` or `SOL` on every tick if the axis title carries the unit and space is constrained.
- Abbreviate large values consistently: `1.2k`, `3.4M`; never mix raw and abbreviated ticks.
- Use tabular numerals for all tick labels.

### 12.5 Series and lines

- Primary line: `2px`.
- Secondary line: `1.5px` and gray or dashed.
- Reference line: `1px`, dashed, muted.
- Confidence band: `10–18%` opacity with a crisp central estimate.
- Scatter points: `3–5px` radius, `25–55%` opacity depending on density.
- Highlighted point: `5–7px`, outlined, directly labeled.
- Avoid smoothing unless the method is named and the raw observations remain visible.
- Do not add point markers to every observation on a dense line.

### 12.6 Legends and direct labels

Direct labels are preferred. Put the series name at the final visible point, next to the bar, or beside a line segment with adequate space.

Use a legend only when:

- there are more than three series;
- labels would collide;
- a color/shape scale has a reusable meaning across many panels.

Legend rules:

- place above or below the plot, never in a floating translucent box;
- order legend items like the visual order at the chart endpoint or table;
- show both line style and color;
- use full human labels, not raw field names;
- never make the reader decode more than six categories in one chart.

### 12.7 Annotation hierarchy

Use annotations in this order:

1. policy threshold or baseline;
2. maximum drawdown / regime break / data discontinuity;
3. one to three decision-driving outliers;
4. start and end values;
5. optional contextual event.

Annotations MUST be factual and short. “Exit guard activated” is better than “Huge crash!” Use a leader line when the label is not adjacent to the mark.

---

## 13. Detailed chart recipes

### 13.1 Cumulative P&L / equity curve

**Use for:** realized path, close-by-close strategy progression, drawdown recovery.

Required:

- start at zero;
- use ordered close timestamp or close sequence;
- show a zero line;
- label final P&L;
- mark maximum peak-to-trough drawdown;
- distinguish realized from mark-to-market;
- state whether simultaneous closes have deterministic ordering;
- state excluded open/ambiguous positions.

Recommended encoding:

- white `2px` line for cumulative net;
- gray zero line;
- red-tinted vertical span or thin segment for max drawdown interval;
- direct labels for peak, trough, and final value;
- optional bottom rug for close density only if it adds meaning.

Do not:

- fill the entire area under the curve with a bright gradient;
- use green above zero and red below zero without also showing the zero line;
- hide early negative periods by starting the y-axis near the final value;
- imply continuous intraperiod equity when only close events are known. Use a step line when that distinction matters.

### 13.2 Drawdown chart

**Use for:** depth, duration, and recovery of losses from prior peaks.

- Domain SHOULD end at zero and extend downward.
- Use negative values explicitly.
- Label deepest drawdown and recovery date/sequence.
- If unrecovered, label `open drawdown`.
- Pair with the equity curve when recovery context matters.
- Prefer a simple line or restrained area at low opacity.

### 13.3 Sorted horizontal bar chart

**Use for:** pool P&L, loss drivers, duration cohorts, feature importance, failure reasons.

- Sort descending by the measure unless chronological/ordinal order is meaningful.
- Place category labels on the y-axis.
- Put exact values at bar ends.
- Start at zero.
- For signed values, use a central zero baseline and bars extending both directions.
- Show `n` beside each category if reliability varies materially.
- Limit to roughly 12–20 categories; group the rest as `Other` only when that grouping is honest.

For loss magnitude, either display signed negative bars or clearly label the measure `loss magnitude`. Never show a positive red number without clarifying that it is magnitude.

### 13.4 Loss concentration / Pareto chart

**Use for:** “How much of gross loss comes from the worst positions/pools?”

Preferred forms:

- ranked horizontal loss bars with a cumulative-share line; or
- cumulative share by ranked position alone.

Required:

- denominator (`gross realized loss`);
- count of losing observations;
- cumulative thresholds at 50%, 80%, or policy-relevant levels;
- labels for top contributors;
- note that concentration does not imply ex-ante predictability.

### 13.5 Histogram

**Use for:** ROI, duration, P&L, slippage, fee yield distributions.

- State bin width or binning rule.
- Show sample size.
- Mark median; optionally mark zero and key risk thresholds.
- Use consistent-width bins.
- If tails dominate, add an inset, clipped tail note, or companion ECDF.
- Do not use a smoothed density alone for small samples.
- Avoid automatic bins that change between comparable panels.

### 13.6 ECDF

**Use for:** tail risk and full-distribution comparisons where arbitrary histogram bins would distract.

- y-axis is `share ≤ x` or `share ≥ x`; state which.
- show zero and catastrophe threshold.
- directly label cohorts at a meaningful quantile.
- use the same x domain across cohorts.
- include cohort sample sizes.

### 13.7 Scatter plot

**Use for:** continuous feature versus outcome, execution impact versus size, volatility versus loss.

- Show raw points.
- Use transparency and slight outline for overlap.
- Use log scale for multiplicative liquidity/volume ranges when justified.
- Label only decision-driving outliers.
- If a fit is shown, name the model and show uncertainty.
- Include correlation only with method (`Pearson`, `Spearman`, etc.) and sample.
- Cluster/color by pool or wallet only if that structure is part of the question.
- Never connect unordered points.
- Never claim causality from slope alone.

### 13.8 Dot-and-whisker / forest plot

**Use for:** cohort effect estimates, model coefficients, validation folds, policy uplift.

- Dot = point estimate.
- Horizontal whisker = declared interval.
- Vertical reference = zero/no-effect/baseline.
- Sort by estimate or conceptual order.
- Write `n` and interval method in the row/caption.
- Use hollow or gray marks for exploratory estimates and a focus color only for preregistered/primary estimates.
- If the interval crosses zero, the visual MUST make that obvious.

This is usually superior to a bar chart for model or uplift estimates.

### 13.9 Heatmap

**Use for:** hour × weekday activity, duration × market-cap cohorts, bin distance × time, fold × feature stability.

- Use a single sequential scale for magnitude and a diverging scale centered at a meaningful zero for signed outcomes.
- Use perceptually ordered colors; never rainbow.
- Keep the same scale across comparable heatmaps.
- Show missing cells with a distinct hatch/outline/`—`, not the zero color.
- Include cell counts when sparse samples can mislead.
- Label extreme or policy-relevant cells directly.
- When cells are large enough, print values inside only if contrast remains adequate.
- Sort axes by time/ordinal meaning, not metric magnitude, unless ranking is the question.

### 13.10 Waterfall

**Use for:** gross wins → gross losses → fees/costs → net, or baseline → rule effects → final result.

- Start and end totals are visually distinct from intermediate changes.
- Every bar has a signed value.
- Connector lines are subtle.
- The arithmetic MUST reconcile exactly after visible rounding or include a rounding note.
- Do not mix already-net and gross components.
- Avoid using a waterfall if components overlap or are not additive.

### 13.11 Paired dots / slopegraph

**Use for:** baseline versus candidate per pool, before versus after, train versus holdout.

- Use one row/line per independent unit.
- Keep baseline consistently on the left and candidate on the right.
- Sort by change or baseline, then say which.
- Highlight direction with position first, color second.
- Label aggregate median/mean separately from individual units.
- Avoid if there are more than ~20 units without small-multiple or filtering support.

### 13.12 Small multiples

**Use for:** the same relationship across pools, wallets, regimes, folds, or time windows.

- Identical geometry and shared scales.
- Same series colors and ordering in every panel.
- Panel title includes cohort and `n`.
- Arrange in a meaningful reading order.
- Keep annotations sparse and consistent.
- Provide an aggregate panel only if aggregation is defensible.

### 13.13 DLMM bin/range strip

**Use for:** active-bin position, lower/upper range, liquidity distribution, out-of-range state.

Must show:

- lower and upper bin IDs;
- lower and upper prices when known;
- active bin and active price;
- liquidity distribution or occupied span;
- in-range/out-of-range/truncated/unknown state in text;
- direction and token orientation;
- timestamp of the snapshot.

Encoding:

```text
lower                                             upper
bin 1021                                         bin 1073
     ▁▂▃▅▇██▆▄▂▁
                  ▲ active 1046 · $0.00421
```

- Bars encode liquidity, not decorative equal-height ticks.
- The active marker should be a vertical rule/triangle with a direct label.
- When the active bin is outside the rendered domain, pin an arrow to the correct edge and label `active +18 bins above range`.
- If prices are unknown, do not fabricate them; fall back to bin IDs.

### 13.14 Trade lifecycle timeline

**Use for:** entry, adds, claims, rebalances, partial removes, exit, swap/unwind, and guard events.

- Time runs left to right or top to bottom.
- Event shape encodes event type; labels state action and amount.
- The timeline MUST preserve separate DLMM and Jupiter action naming.
- Use the concrete routine slug only when the log actually records it.
- Trigger/signal, semantic routine role, resolved routine, atomic actions, transaction, and confirmation should remain distinguishable.
- Failed/simulated transactions use a different line style and explicit status label.
- Never imply that a trigger directly performed wallet actions.

### 13.15 Sankey, network, radar, donut, gauge, and 3D charts

These are not default LIQ visuals:

- **Sankey:** MAY be used only for a true conserved flow with reconciled quantities. Usually a waterfall or table is clearer.
- **Network:** MAY be used for actual wallet/pool relationships when topology is the question. Must include a readable adjacency table.
- **Radar:** MUST NOT be used; values depend on axis order and area exaggerates difference.
- **Donut/pie:** SHOULD NOT be used. Use sorted bars. A two-part share MAY be shown as a labeled 100% strip.
- **Gauge:** MUST NOT be used. Use a number plus threshold strip.
- **3D:** MUST NOT be used.

---

## 14. Uncertainty, sample size, and statistical honesty

### 14.1 Independent unit

Every inferential visual MUST state both row count and the more defensible independent unit:

- `n=222 positions / 61 pools`;
- `36 holdout positions / 22 pools`;
- `12 wallets / 4 chronological folds`.

Position count alone may overstate evidence when positions share pools, wallets, or market regimes.

### 14.2 Intervals

- Name the interval: bootstrap CI, pool-clustered bootstrap, Bayesian credible interval, quantile range, standard error, etc.
- State level: `90%` or `95%`.
- If resampling, state the resampling unit.
- If an estimate has no interval, do not style it like a confirmed effect.
- An interval crossing the no-effect line MUST remain visible; do not crop it.
- Do not use error bars without saying what they mean.

### 14.3 Exploratory versus confirmatory

Use explicit labels:

- `descriptive` — summarizes observed data;
- `exploratory` — selected or tuned on these data;
- `validation` — evaluated under a declared procedure;
- `holdout` — untouched final evaluation;
- `shadow` — computed prospectively without controlling live action;
- `promoted` — mapped into an active strategy/config contract.

Do not make exploratory charts more saturated or more prominent than holdout results merely because they look cleaner.

### 14.4 Missingness and exclusions

Every report MUST account for:

- missing rows;
- unmatched pools/positions;
- open lifecycles;
- ambiguous attribution;
- stale market data;
- failed quotes;
- unavailable fee separation;
- filtered outliers, if any.

Missing data gets its own state, not zero and not omission without a note.

---

## 15. Tables

### 15.1 When a table is the right visual

Use a table for exact lookup, audit detail, heterogeneous fields, or a short ranked list. Do not turn every result into a chart.

### 15.2 Table anatomy

```html
<div class="table-wrap" tabindex="0" role="region" aria-label="Holdout policy comparison">
  <table>
    <caption>Holdout policy comparison</caption>
    <thead>
      <tr>
        <th scope="col">Rule</th>
        <th scope="col" class="num">Positions</th>
        <th scope="col" class="num">Pools</th>
        <th scope="col" class="num">Mean ROI</th>
        <th scope="col" class="num">Net SOL</th>
      </tr>
    </thead>
    <tbody><!-- rows --></tbody>
  </table>
</div>
<p class="table-note">Final chronological holdout · values are fee-inclusive.</p>
```

### 15.3 Styling

```css
.table-wrap {
  max-width: 100%;
  overflow: auto;
  border-block: 1px solid var(--report-line);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  font-variant-numeric: tabular-nums lining-nums;
}
th, td {
  padding: 9px 10px;
  border-bottom: 1px solid var(--report-line);
  text-align: left;
  vertical-align: top;
}
th {
  color: var(--report-muted);
  font-size: 11px;
  font-weight: 650;
}
th.num, td.num {
  text-align: right;
  font-family: var(--font-mono);
  white-space: nowrap;
}
tbody tr:last-child td { border-bottom: 0; }
```

### 15.4 Table rules

- Numeric columns right-align.
- Labels left-align.
- Headers state units or the caption defines them.
- Keep decimals aligned through consistent precision.
- Sort order MUST be evident from the surrounding sentence, header marker, or note.
- Sticky headers MAY be used for long screen tables, but MUST be disabled for print.
- Long addresses use middle truncation visually; the full value remains in `title`, an accessible label, or a details view.
- Do not truncate pool labels that distinguish same-token pools; include a short address suffix.
- Use row striping only for extremely wide/dense lookup tables, and keep it subtle.
- Highlight at most one or two rows, with a text label explaining why.
- For more than ~25 default rows, show the most relevant rows and disclose `Showing 20 of 222`; provide the remaining data in a `<details>` table or source artifact.
- Do not paginate a self-contained report unless the table is genuinely interactive and keyboard accessible.

---

## 16. Diagrams and non-chart visuals

### 16.1 Use diagrams only for relationships

A diagram is justified when prose cannot cleanly express sequence, hierarchy, state, ownership, or routing. It is not a substitute for missing analysis.

### 16.2 Execution-chain diagram

When a report explains live behavior, preserve the clean chain:

```text
config/snapshot
      ↓
signal/trigger
      ↓
semantic routine role
      ↓
named routine
      ↓
atomic actions
      ↓
transaction path
      ↓
append-only logs
```

Visual rules:

- left-to-right for wide pages; top-to-bottom on narrow pages;
- nodes are text plus thin rules, not glossy cards;
- arrows encode direction only;
- label branch conditions;
- show trust/execution boundaries with a dashed divider and text;
- never collapse the trigger and wallet action into one node;
- never invent generic `enter`, `exit`, or separate kill-switch routines;
- hard-exit signals resolve through `fast-exit` to `exit-fast` in the managed dynamic meme lane;
- Jupiter swap actions remain visually and semantically separate from DLMM routines.

### 16.3 Decision trees

- Use only for actual mutually exclusive decisions.
- Put the question on the branch, not in a legend.
- Label every branch condition.
- End nodes state a result/action, not `yes`/`no` alone.
- Include unknown/error/missing-data branches.
- Keep depth under five levels; otherwise use a rule table.

### 16.4 Architecture and ownership maps

- Group by runtime/ownership boundary.
- Use arrows only for real calls/data flow.
- Label read-only versus mutating paths.
- Put execution-capable components in a clearly labeled boundary.
- Do not imply `apps/live-gui` signs or sends wallet transactions.

### 16.5 Screenshots

Screenshots MAY document a visual bug, operator flow, or external evidence that cannot be represented as structured data. They MUST NOT replace charts generated from available structured data.

For screenshots:

- crop to the relevant surface;
- redact secrets, full RPC URLs, wallet keys, tokens, and private identifiers;
- add a one-sentence caption and capture timestamp;
- use a thin neutral border only if the image edge disappears into the canvas;
- do not add fake device frames, shadows, perspective, or decorative backgrounds;
- preserve enough resolution for labels to remain legible;
- include textual findings outside the image for accessibility.

### 16.6 Icons and illustrations

- Decorative illustration is not part of the default report language.
- Icons MAY clarify warnings, external links, downloads, or status, but must have labels.
- Do not use emoji as the only status encoding.
- Logos MAY identify a protocol/source once; do not repeat them in section headers.

---

## 17. Interaction

### 17.1 Default to static

The default report is fully understandable without interaction. Interaction is allowed only when it reduces clutter or enables a real analytical task.

Good interactions:

- disclose chart data;
- inspect an exact point;
- toggle a small number of comparable series;
- select a pool/wallet while keeping the aggregate visible;
- expand full source provenance;
- copy a source path or address.

Bad interactions:

- hiding the main conclusion behind hover;
- auto-playing animation;
- tooltips containing the only unit or series name;
- carousels;
- scroll-jacking;
- animated counters;
- drag/zoom on a small chart with no analytical need;
- filters that silently change sample size.

### 17.2 Tooltip contract

Tooltips MUST:

- be accessible by keyboard/focus, not hover only;
- show series/category, x value, y value, and unit;
- show `n` when the point aggregates observations;
- remain inside the viewport;
- not obscure the selected mark when avoidable;
- close on Escape;
- never contain the only source citation.

For a self-contained static report, direct labels plus a data table are usually better than tooltips.

### 17.3 Filters

If a filter changes the evidence:

- display the active filter in plain text;
- update sample counts and captions;
- preserve a visible `All` baseline;
- do not make the URL or report state non-reproducible without showing the state;
- provide a reset action;
- avoid more than 5–7 visible filter choices without a search/list pattern.

### 17.4 Motion

- Charts SHOULD render immediately without entrance animation.
- Hover transitions MAY be `80–140ms`.
- Respect `prefers-reduced-motion: reduce`.
- Do not animate a line drawing itself; it delays evidence and implies narrative drama.

---

## 18. Accessibility

Accessibility is part of analytical correctness.

### 18.1 Required semantic structure

- One `<h1>`.
- Headings descend without skipped levels.
- Each chart uses `<figure>` and `<figcaption>`.
- Tables use `<caption>`, `<thead>`, `<tbody>`, and scoped headers.
- Metric strips use `<dl>`, `<dt>`, and `<dd>`.
- Warnings use text labels, not only color.
- Interactive elements are native buttons, links, inputs, or details/summary when possible.

### 18.2 Chart accessibility

Every nontrivial chart MUST provide:

1. a concise accessible name describing its subject;
2. a visible finding-led caption;
3. a data table or structured textual summary;
4. redundant encoding beyond color;
5. readable contrast and label size.

Decorative SVG elements use `aria-hidden="true"`. If the SVG itself carries the accessible name, use `role="img"`, `<title>`, and `<desc>` with unique IDs.

### 18.3 Contrast and color vision

- Normal text contrast: at least 4.5:1.
- Large text/major chart marks: at least 3:1.
- Gridlines may be lower contrast because they are nonessential, but zero/baseline lines must remain visible.
- Positive/negative pairs also use `+`/`−`, labels, direction, or line style.
- Test in grayscale: the chart’s primary conclusion should survive.

### 18.4 Focus and keyboard

```css
:focus-visible {
  outline: 2px solid var(--chart-focus);
  outline-offset: 3px;
}
```

- Scrollable table regions require `tabindex="0"` and an accessible label.
- Disclosure controls must expose open/closed state natively.
- Never remove focus outlines without a replacement.

---

## 19. Responsive behavior in the report viewer

### 19.1 Container reality

Reports load in an iframe inside a two-column viewer. Responsive CSS responds to iframe width, not the outer browser width. Design the document as if its desktop width may still be only `700–900px`.

### 19.2 Breakpoints

Use content-driven breakpoints:

- `980px`: wide chart/table layouts may reduce gaps.
- `760px`: two-column visuals collapse; title and metadata stack.
- `560px`: metric strips become two or one columns; tables scroll.
- `420px`: chart labels abbreviate; evidence captions stack.

### 19.3 Mobile rules

- Minimum body size remains `14px`.
- Axes remain at least `10px`.
- Never uniformly scale a desktop chart down until labels are microscopic.
- Reduce tick count, shorten labels, move direct labels, and increase chart height when needed.
- Horizontal category bars are preferred over vertical bars with rotated labels.
- Tables scroll horizontally inside a labeled region.
- Do not force the whole page wider than the iframe.
- Long paths and addresses use `overflow-wrap:anywhere` outside tables.
- Touch targets for controls are at least `40×40px` even if the visible control is compact.

### 19.4 Responsive chart strategy

For inline SVG:

1. keep a stable `viewBox`;
2. set `width:100%; height:auto`;
3. use a mobile-specific rendering pass when label collisions persist;
4. reduce x ticks before rotating them;
5. switch vertical bars to horizontal bars on small widths when categories are verbose;
6. keep data and meaning identical across variants.

---

## 20. Print and PDF

Reports SHOULD print cleanly even if screen mode is dark.

```css
@media print {
  :root {
    color-scheme: light;
    --report-bg: #ffffff;
    --report-surface: #ffffff;
    --report-ink: #111111;
    --report-muted: #4f4f4f;
    --report-faint: #6f6f6f;
    --report-line: #d8d8d8;
    --report-line-strong: #aaaaaa;
    --report-grid: #e6e6e6;
    --chart-primary: #111111;
    --chart-secondary: #666666;
    --chart-tertiary: #999999;
  }

  html, body { background: #fff !important; color: #111 !important; }
  .report { width: 100%; padding: 0; }
  .report-section { break-before: auto; }
  figure, table, .metric-strip, .callout { break-inside: avoid; }
  thead { display: table-header-group; }
  a { color: inherit; text-decoration: underline; }
  .screen-only { display: none !important; }
  .print-only { display: block !important; }
}
```

Print requirements:

- Use light-background chart variables or a dedicated light SVG variant.
- Do not rely on browsers printing background fills.
- Keep chart labels dark and series distinguishable by line style.
- Avoid orphaned chart headings at page bottoms.
- Repeat table headers.
- Show full source paths or footnote references.
- Disable sticky positioning.
- Hide interactive-only controls.
- Ensure every page can be understood if printed separately by keeping the figure caption attached.

---

## 21. Self-contained HTML and security

### 21.1 Portability

Durable reports SHOULD be self-contained or use only repository-synced relative assets. They MUST NOT require a public CDN, remote font, analytics script, or network request to render.

Preferred:

- inline CSS;
- inline SVG;
- embedded JSON for chart data;
- local relative images copied by the report-library sync;
- no framework runtime unless genuinely necessary;
- no build-time dependency visible at render time.

### 21.2 Content security policy

A strict standalone artifact MAY use:

```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none';
           img-src data: blob: 'self';
           style-src 'unsafe-inline';
           script-src 'unsafe-inline';
           connect-src 'none';
           font-src data:;
           object-src 'none';
           base-uri 'none';
           form-action 'none'">
<meta name="referrer" content="no-referrer">
```

If external assets are truly required, document them and ensure the synced report remains functional offline. Do not weaken CSP casually.

### 21.3 Data injection

- Serialize embedded data with a safe JSON serializer.
- Escape user/source strings inserted into HTML.
- Prefer DOM `textContent` over string concatenation.
- Do not embed secrets, full RPC URLs, wallet keys, auth tokens, or private operator data.
- Do not put executable instructions from untrusted source content into the DOM.

### 21.4 Artifact size and performance

- Aim for under `1 MB` when practical.
- Prefer SVG paths and compact JSON to base64 PNGs for simple charts.
- Downsample only when the visual resolution cannot display every point; preserve raw data separately and state the method.
- Do not render hundreds of offscreen tooltip nodes.
- Avoid chart libraries for one or two simple charts.
- A report SHOULD become readable before any enhancement script runs.
- Enhancement failure MUST leave headings, conclusions, tables, and static chart fallbacks intact.

---

## 22. Inline SVG implementation pattern

Inline SVG is the default for custom LIQ charts because it is sharp, portable, themeable, accessible, and dependency-free.

### 22.1 Base markup

```html
<figure class="evidence-figure" id="equity-figure">
  <figcaption id="equity-caption">
    <strong>The book recovered its maximum drawdown and closed positive.</strong>
    <span>Cumulative fee-inclusive realized P&amp;L by completed position.</span>
  </figcaption>
  <svg
    class="chart-svg"
    viewBox="0 0 960 380"
    role="img"
    aria-labelledby="equity-title equity-desc"
    preserveAspectRatio="xMidYMid meet"
  >
    <title id="equity-title">Cumulative realized P&amp;L</title>
    <desc id="equity-desc">
      Close-by-close P&amp;L falls to a maximum drawdown of 1.118 SOL and ends at positive 2.522 SOL.
    </desc>
    <g class="grid"></g>
    <g class="axes"></g>
    <path class="series series-primary" d=""></path>
    <g class="annotations"></g>
  </svg>
  <p class="evidence-note">n=222 positions / 61 pools · SOL · close order · UTC · source: …</p>
</figure>
```

### 22.2 SVG CSS

```css
.chart-svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
  font-family: var(--font-sans);
}
.grid line { stroke: var(--report-grid); stroke-width: 1; shape-rendering: crispEdges; }
.axis line { stroke: var(--report-line-strong); shape-rendering: crispEdges; }
.axis text, .chart-label { fill: var(--report-muted); font-size: 11px; }
.zero-line { stroke: var(--report-line-strong); stroke-width: 1.25; }
.series { fill: none; vector-effect: non-scaling-stroke; }
.series-primary { stroke: var(--chart-primary); stroke-width: 2; }
.series-secondary { stroke: var(--chart-secondary); stroke-width: 1.5; stroke-dasharray: 5 4; }
.annotation-line { stroke: var(--report-muted); stroke-width: 1; }
.annotation-text { fill: var(--report-ink); font-size: 11px; font-weight: 600; }
```

### 22.3 Minimal scale helpers

```js
const linear = (domainMin, domainMax, rangeMin, rangeMax) => {
  const span = domainMax - domainMin || 1;
  return value => rangeMin + ((value - domainMin) / span) * (rangeMax - rangeMin);
};

const pointsToPath = points => points
  .map((point, index) => `${index ? "L" : "M"}${point.x.toFixed(2)},${point.y.toFixed(2)}`)
  .join(" ");

const signed = (value, digits = 2) =>
  `${value > 0 ? "+" : value < 0 ? "−" : ""}${Math.abs(value).toFixed(digits)}`;
```

Implementation requirements:

- Validate finite numbers before generating coordinates.
- Sort only when ordering is part of the chart contract; never silently reorder time.
- Preserve raw values separately from pixel coordinates.
- Use `document.createElementNS` and `textContent` for dynamic labels.
- Use unique title/description IDs when multiple charts exist.
- Avoid `foreignObject` for essential labels because print/export support varies.

---

## 23. Semantic HTML bar pattern

For a small ranked comparison, semantic HTML is often better than SVG.

```html
<div class="bar-list" aria-label="Share of gross loss by cohort">
  <div class="bar-row">
    <span class="bar-label">ROI ≤ −5%</span>
    <span class="bar-track" aria-hidden="true">
      <span class="bar-fill" style="--value: 89.2%"></span>
    </span>
    <span class="bar-value">89.2%</span>
  </div>
</div>
```

```css
.bar-list { display: grid; gap: 10px; }
.bar-row {
  display: grid;
  grid-template-columns: minmax(110px, 160px) minmax(120px, 1fr) 72px;
  gap: 12px;
  align-items: center;
}
.bar-label, .bar-value { font-size: 12px; }
.bar-value { text-align: right; font-family: var(--font-mono); }
.bar-track { height: 12px; background: var(--report-line); }
.bar-fill { display: block; width: var(--value); height: 100%; background: var(--chart-primary); }
```

The visible numeric label is mandatory. The bar is the pattern; the number is the exact value.

---

## 24. Full portable skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="referrer" content="no-referrer">
  <title>Specific report title</title>
  <style>
    /* Paste canonical tokens and component rules here. */
  </style>
</head>
<body>
  <main class="report">
    <header class="report-header">
      <p class="report-kicker">Research-only · strategy evidence</p>
      <h1>Specific report title</h1>
      <p class="report-deck prose">
        Population, period, timezone, units, exclusions, and the exact question.
      </p>
      <dl class="report-meta">
        <div><dt>Cutoff</dt><dd>YYYY-MM-DD HH:mm UTC</dd></div>
        <div><dt>Sample</dt><dd>N positions / K pools</dd></div>
        <div><dt>Status</dt><dd>Shadow; no live change</dd></div>
      </dl>
    </header>

    <section class="report-section" aria-labelledby="read-heading">
      <h2 id="read-heading">Read</h2>
      <p class="lede prose">Shortest defensible answer, including uncertainty.</p>
      <dl class="metric-strip"><!-- 3–6 metrics --></dl>
    </section>

    <section class="report-section" aria-labelledby="decision-heading">
      <h2 id="decision-heading">Decision</h2>
      <div class="callout" data-tone="warning">
        <strong>Shadow only.</strong>
        <p>What is logged, what is unchanged, and what promotes it.</p>
      </div>
    </section>

    <section class="report-section" aria-labelledby="evidence-heading">
      <h2 id="evidence-heading">Evidence</h2>
      <figure class="evidence-figure"><!-- primary chart + rail --></figure>
      <div class="split"><!-- supporting visuals --></div>
    </section>

    <section class="report-section" aria-labelledby="counter-heading">
      <h2 id="counter-heading">Counterevidence</h2>
      <p class="prose">Where the claim weakens, reverses, or lacks coverage.</p>
    </section>

    <section class="report-section" aria-labelledby="risk-heading">
      <h2 id="risk-heading">Risk and caveats</h2>
      <ul class="prose"><!-- concrete limitations --></ul>
    </section>

    <section class="report-section" aria-labelledby="next-heading">
      <h2 id="next-heading">Next run</h2>
      <ol class="prose"><!-- preregistered follow-up and promotion bar --></ol>
    </section>

    <footer class="report-section report-footer" aria-labelledby="sources-heading">
      <h2 id="sources-heading">Sources and reproduction</h2>
      <ol class="source-list"><!-- paths, queries, timestamps --></ol>
    </footer>
  </main>
</body>
</html>
```

---

## 25. Writing for visuals

### 25.1 Chart titles

Use titles that state the observed relationship:

- Good: `The worst 10 positions produced 27.1% of gross loss.`
- Good: `Expected-positive improved mean ROI, but its interval crossed zero.`
- Good: `Eight-to-24-hour positions had the best observed net P&L.`
- Weak: `Loss concentration`.
- Weak: `Model results`.
- Bad: `Amazing recovery!`.

If the evidence is inconclusive, the title must remain inconclusive:

- `Holdout uplift is positive but unresolved.`
- `No stable time-of-day edge appears across wallets.`

### 25.2 Captions

Use this compact sequence:

```text
n / clusters · unit · period and timezone · estimator/aggregation · exclusions · interval method · source
```

Example:

```text
n=36 positions / 22 pools · mean fee-inclusive ROI · final chronological holdout ·
95% pool bootstrap, 10,000 resamples · 5 unmatched positions excluded · source: analysis.json
```

### 25.3 Labels

- Use human labels: `Prior-hour volume`, not `log_volume_ratio_1h`.
- Preserve the raw field name in the source/method note when useful.
- Use consistent terms across prose, chart, table, and code.
- A threshold label states its action: `live guard: −10%`, not merely `−10`.
- A baseline label says what it is: `all eligible`, not `control` unless it is a true control.

### 25.4 Claims

Match claim strength to evidence:

| Evidence | Appropriate language |
|---|---|
| descriptive cohort | `was associated with`, `contained`, `observed` |
| holdout but imprecise | `directionally improved`, `interval crossed zero` |
| stable preregistered holdout | `improved under the declared test` |
| causal experiment | `caused`, only if design supports it |
| missing denominator | `cannot estimate rate` |

Never turn hindsight-only fields such as realized duration or rebalance count into “entry filters” without a pre-entry feature definition.

---

## 26. Source provenance and reproducibility

### 26.1 Visible provenance

The evidence rail contains the short source. The final `Sources` section contains full provenance:

- repository-relative path;
- source type and schema/version if known;
- observed date range;
- data cutoff;
- transformation/query/build path;
- artifact generation timestamp;
- checksum or run ID when available;
- known omissions.

### 26.2 Reproduction block

```html
<details class="reproduction">
  <summary>Reproduce this report</summary>
  <pre><code>exact repository-root command</code></pre>
  <p>Inputs: …</p>
  <p>Output: …</p>
</details>
```

- Commands must be exact and run from a named working directory.
- Do not include secrets or environment values.
- Do not claim reproducibility if the input snapshot is mutable or missing; state that limitation.

### 26.3 Report versus live policy

A report MUST explicitly say whether it changes live behavior. Research artifacts do not silently become strategy bindings. If a result is promoted, link or name the specific strategy/config snapshot and semantic routine-role mapping it affects.

---

## 27. Anti-patterns

### 27.1 Visual decoration

Do not use:

- decorative hero art;
- gradients, glow, glass, shadows, or background particles;
- oversized KPI numbers with little context;
- nested rounded cards;
- arbitrary section numbering;
- fake terminal chrome;
- chart containers added only to fill space;
- animated counters;
- decorative icons beside every heading.

### 27.2 Chart malpractice

Do not use:

- truncated bar axes;
- dual y-axes unless an exceptional analytical case is documented;
- rainbow scales;
- pie/donut charts with many slices;
- 3D marks;
- smoothed lines that hide raw volatility;
- unlabeled uncertainty bars;
- different scales for visually compared small multiples;
- category order chosen to dramatize a claim;
- a mean without distribution/sample context;
- a correlation chart phrased as causation;
- a chart that silently excludes losses, unmatched rows, or failed trades.

### 27.3 Trading-specific misrepresentation

Do not:

- add identifiable fee floor to net P&L when net already includes it;
- label gross LP output as net profit;
- compare a fee yield to price movement without execution and inventory costs;
- merge positions across same-label pools without a pool identifier;
- treat positions as independent when pools/wallets cluster them;
- classify post-entry outcomes as pre-entry predictors;
- mix realized and marked P&L without separate series and definitions;
- imply missing executable quotes have zero cost;
- show a backtest candidate as live policy without status and binding evidence;
- visually collapse signals, routine roles, named routines, actions, and transactions.

---

## 28. Review checklist

### 28.1 Editorial

- [ ] The title names the subject and question.
- [ ] The header states sample, period, timezone, exclusions, cutoff, and status.
- [ ] The first paragraph gives the answer and its largest limitation.
- [ ] The decision is explicit: change, no change, shadow, or blocked.
- [ ] Every heading helps the reader understand the argument.
- [ ] Counterevidence and failure cases are visible.
- [ ] Caveats are concrete, not boilerplate.
- [ ] The report states whether live behavior changes.

### 28.2 Metrics

- [ ] Units and denominators are present.
- [ ] Precision is consistent and not false precision.
- [ ] Missing values are not coerced to zero.
- [ ] Percent versus percentage-point changes are correct.
- [ ] Gross, net, realized, marked, and fee-floor measures are distinguished.
- [ ] Position and independent pool/wallet counts are both stated where relevant.

### 28.3 Every chart

- [ ] It answers one written question.
- [ ] The title states a finding or honest uncertainty.
- [ ] The chosen chart type matches the question.
- [ ] Axes, units, timezone, and scale are clear.
- [ ] Bars start at zero.
- [ ] Relevant zero/baseline/policy thresholds are visible.
- [ ] Series are directly labeled where practical.
- [ ] Color is redundant with text, sign, shape, or line style.
- [ ] Sample and cluster counts are visible.
- [ ] Intervals are shown and defined when estimated.
- [ ] Missing/excluded data is stated.
- [ ] A source/method caption is attached.
- [ ] A data table or structured summary is available.
- [ ] The conclusion survives grayscale.

### 28.4 Tables

- [ ] Table has a semantic caption and scoped headers.
- [ ] Numeric columns are right-aligned and tabular.
- [ ] Units and sort order are clear.
- [ ] Addresses preserve enough identity to distinguish pools.
- [ ] Long tables state shown/total rows.
- [ ] Mobile overflow is contained and keyboard accessible.

### 28.5 Responsive and accessible

- [ ] Works at iframe widths of 1280, 900, 760, 560, and 360px.
- [ ] No page-wide horizontal overflow.
- [ ] Text remains at least 14px body / 10px axes.
- [ ] Two-column layouts collapse cleanly.
- [ ] Focus indicators are visible.
- [ ] No essential information exists only on hover.
- [ ] Heading order is valid.
- [ ] Figures, metrics, tables, and controls use semantic HTML.
- [ ] Reduced motion is respected.

### 28.6 Portable artifact

- [ ] Opens directly as a local file or synced report asset.
- [ ] Renders inside `/reports` without external network access.
- [ ] Main content survives JavaScript failure.
- [ ] No secrets, full private RPC URLs, or auth material are embedded.
- [ ] CSP and referrer policy are appropriate.
- [ ] Source paths and reproduction command are present.
- [ ] Print/PDF uses a legible light treatment.
- [ ] SVG charts remain vector and do not clip labels.
- [ ] Artifact size and DOM complexity are reasonable.

---

## 29. Acceptance bar

A conforming LIQ report should pass this five-second test:

1. **What is this?** — obvious from title and scope.
2. **What happened?** — obvious from the read and primary visual.
3. **How large and how certain?** — obvious from numbers, sample, and intervals.
4. **What changes?** — explicit in the decision status.
5. **Can I audit it?** — source and method are attached to the evidence.

It should also pass the five-minute test: a skeptical reader can inspect the distributions, counterevidence, missingness, independence assumptions, and sources without reverse-engineering the page.

The design is successful when it is visually quiet but analytically difficult to misread. The graph is not there to make the report look complete. The graph is there because spatial encoding makes the evidence faster and more honest to understand than prose or a table alone.
