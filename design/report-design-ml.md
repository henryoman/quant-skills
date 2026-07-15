# Research Report Design Standard

This document is the default visual specification for research HTML reports in this repository. It is intentionally prescriptive and dense so a report can be designed without asking what “looks right” each time.

The goal is not decoration. The goal is to make alpha evidence fast to scan, hard to misread, and easy to audit. Every visual should help answer whether an edge exists, survives costs, and deserves a stricter forward test.

## 1. Non-negotiable defaults

Unless a task explicitly says otherwise:

- Use a pure-black research canvas with near-white text and quiet neutral structure.
- Render every chart, heatmap, image, and major table **one per row at the full available report width**.
- Never use side-by-side chart grids, thumbnail galleries, or `max-width` caps that shrink plots.
- Use a single-column report flow. Text can have a readable line length, but the chart immediately below it must still use the full available width.
- Prefer a small number of strong charts over a dashboard of tiny panels.
- Give every chart a descriptive title, an assumptions-rich subtitle, visible units, and a nearby interpretation.
- Use color to encode data, never merely to decorate a report.
- Use blue for favorable/positive magnitude, red for adverse/negative magnitude, orange for marginal or warning territory, and grey for neutral/near-zero/not-applicable states.
- Do not use red-versus-green as the default performance encoding. It is less accessible and visually harsher than the current blue-versus-red system.
- Keep grid lines, borders, axes, and card chrome quiet. Data marks and labels should dominate.
- Make charts clickable to expand into a near-full-screen black modal when the report is interactive.
- Preserve an exact data table or inspectable tooltip for every chart when practical.
- Never let a dense parameter surface imply more independent evidence than exists. Display unique markets, trades, sample size, and evidence level near the visual.
- Active Solana Up/Down reporting is 5-minute only. Do not mix legacy 15-minute results into a current report.

## 2. Visual character

The intended look is technical, sparse, and high-contrast:

- Pure black page, not blue-black or charcoal.
- Flat surfaces with minimal shadows.
- Fine neutral borders rather than heavy card outlines.
- System sans-serif for prose and labels.
- Monospace/tabular numerals for values, timestamps, bps, prices, PnL, counts, and identifiers.
- Compact headings, generous vertical separation between ideas, and wide visual footprints.
- Saturated color only inside data marks, heatmap cells, status accents, or the active interaction target.
- No gradients in chart marks, glossy effects, glassmorphism, 3D charts, background textures, ornamental illustrations, or arbitrary colored containers.
- Rounded corners are allowed for metric cards and dialogs, but charts themselves should feel flat and rectangular.

The report should feel like an evidence terminal that is comfortable to read for a long session, not like a marketing site.

## 3. Canonical dark tokens

Use these tokens as the default screen theme. They match the strongest current report treatment.

```css
:root {
  color-scheme: dark;

  /* Canvas and surfaces */
  --report-canvas: #000000;
  --report-surface: #070707;
  --report-surface-subtle: #0d0d0d;
  --report-surface-raised: #111111;

  /* Type */
  --report-ink: #f2f2f2;
  --report-muted: #c9c9c9;
  --report-tertiary: #a9a9a9;
  --report-table-text: #d2d2d2;

  /* Structure and interaction */
  --report-border: rgba(255, 255, 255, 0.13);
  --report-border-quiet: rgba(255, 255, 255, 0.07);
  --report-grid: rgba(255, 255, 255, 0.10);
  --report-grid-strong: rgba(255, 255, 255, 0.20);
  --report-accent: #8ac5ff;
  --report-focus: #8ac5ff;

  /* Semantic state; do not automatically use these as chart series colors */
  --report-pass: #79d996;
  --report-pass-bg: rgba(64, 180, 99, 0.16);
  --report-fail: #ff8583;
  --report-fail-bg: rgba(224, 74, 70, 0.16);
  --report-warning: #e7b84b;
  --report-warning-bg: rgba(231, 184, 75, 0.14);

  /* Geometry */
  --report-radius: 12px;
  --report-card-radius: 16px;
  --report-content-pad: clamp(18px, 2.5vw, 40px);
  --report-section-gap: 32px;
}
```

Rules:

- Page background is `#000000`.
- Use `#070707` or `#0d0d0d` only when a surface needs separation from the canvas.
- Primary text is `#f2f2f2`; secondary copy is `#c9c9c9`; metadata and quiet labels are `#a9a9a9`.
- Borders should usually be 1 px at 7–13% white opacity.
- Do not use a shadow when a border or spacing boundary is sufficient.
- Links and keyboard focus use `#8ac5ff`.
- Keep the number of simultaneous non-neutral colors low.

### Print tokens

Print/PDF should switch to a light theme for legibility and ink use. Preserve the same hierarchy and data semantics.

```css
@media print {
  :root {
    color-scheme: light;
    --report-canvas: #ffffff;
    --report-surface: #ffffff;
    --report-surface-subtle: #f7f7f7;
    --report-ink: #0d0d0d;
    --report-muted: #5d5d5d;
    --report-tertiary: #767676;
    --report-table-text: #3f3f3f;
    --report-border: rgba(13, 13, 13, 0.12);
    --report-grid: rgba(13, 13, 13, 0.10);
  }
}
```

Do not make a screen capture of the dark report and drop it into a PDF. Render a true print variant with readable labels and retained cell distinctions.

## 4. Typography and numeric formatting

### Font stack

```css
--font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
```

Use sans-serif for titles, prose, axis labels, legends, and annotations. Use monospace or `font-variant-numeric: tabular-nums` for numeric columns, tooltip values, data labels, prices, timestamps, bps, ROI, PnL, and counts.

### Type scale

- Page title: `clamp(24px, 3vw, 40px)`, weight 600, line height 1.1–1.2.
- Section heading: 20–24 px, weight 600, line height 1.2.
- Chart title: 16–18 px, weight 550–600, line height 1.3.
- Chart subtitle: 12–14 px, weight 400, muted.
- Body: 14–16 px, line height 1.55–1.7.
- Axis and legend: 11–13 px.
- Metadata/source/caveat: 11–12 px.
- KPI value: 24–32 px, weight 600, tabular numerals.

Avoid light font weights on the black background. Avoid all-caps except for short eyebrow labels, statuses, and compact table headers. Never shrink text below 11 px to make a chart fit; give the chart more space instead.

### Number formatting

- Show the unit in the axis title, subtitle, column header, or value suffix.
- Use consistent precision inside a comparison: `18.97%`, not a mixture of `19%`, `18.970%`, and `0.1897`.
- Default precision: price 2–4 decimals as appropriate; probability 1–2 percentage points; ROI/PnL rate 1–2 decimals; bps 1–2 decimals; counts no decimals.
- Use a true minus sign if the renderer supports it; always show a sign on signed return/PnL labels when that makes direction easier to scan.
- Prefer `$10`, `$0.02`, `39.49%`, `18.97 bps`, `15 trades`, and `22 markets` over unlabeled bare numbers.
- Use `—` for unavailable, `N/A` for not applicable, and an explicit `0` only for a real measured zero.
- Do not round away the sign of a small value. If needed, show `<0.01` or add precision.

## 5. Page and chart layout

### Page flow

The default report sequence is:

1. Title and one-sentence scope.
2. Executive summary with the decision, strongest evidence, and main disqualifier.
3. Compact assumptions/evidence strip.
4. Repeating evidence sections: question → chart → read → caveat.
5. Exact results table where useful.
6. Next experiments.
7. Caveats, evidence level, and decision.
8. Sources/provenance.

Charts must be placed immediately after the text that frames their analytical question. Do not collect charts into a detached gallery.

### Width and columns

```css
.report {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0 var(--report-content-pad) 56px;
  background: var(--report-canvas);
}

.report-stack {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: var(--report-section-gap);
  width: 100%;
  max-width: none;
}

.chart-panel,
.heatmap-panel,
.report-table {
  grid-column: 1;
  width: 100%;
  max-width: none;
  min-width: 0;
}

.prose {
  max-width: 86ch;
}
```

Never use this for report charts:

```css
/* Forbidden for report visuals */
.charts { grid-template-columns: repeat(2, 1fr); }
.chart { max-width: 768px; }
.gallery { display: flex; flex-wrap: wrap; }
```

Text may be kept to 78–86 characters for readability. Visuals do not inherit that cap.

### Spacing

- 24–40 px page side padding on desktop.
- 16–24 px page side padding on small screens.
- 32–48 px between major evidence sections.
- 14–18 px between chart title/subtitle and plot.
- 16–24 px between plot and its interpretation/caption.
- 4–6 px between heatmap cells when cells are large; 1–3 px when the matrix is dense.
- Minimum heatmap cell height: 44 px in-report; 64 px in expanded view.

Whitespace separates ideas. Card borders should not be used to compensate for poor spacing.

### Chart height

Do not force all charts into one fixed aspect ratio.

- Simple bar/line chart: usually 420–620 px desktop height.
- Dense multi-series chart: 560–760 px.
- Heatmap: derive height from row count; aim for 44–64 px per row plus headers.
- Expanded modal: at least 70 vh of plot area, up to roughly 94 vh overall.
- On mobile, allow vertical growth and horizontal scrolling for intrinsically wide matrices instead of crushing labels.

## 6. Required chart anatomy

Every chart should have these elements in this order:

1. **Neutral descriptive title** — what is plotted.
2. **Subtitle** — scope, time range, grain, sample size, fixed assumptions, and unit.
3. **Plot** — full width with readable axes.
4. **Legend** only if it adds information not already visible from direct labels or axis categories.
5. **Read** — one to three sentences explaining the supported takeaway.
6. **Caveat/evidence label** — proxy-only, backtest, paper-traded, fillable, live-filled, or settlement-backed.
7. **Source/inspection affordance** — source label, tooltip, and/or expandable exact data table.

Recommended wording:

```text
Title: Spot-trend ROI by budget and entry time
Subtitle: SOL 5m · 22 resolved markets · max 10s quote offset · $0.02/contract fee stress
Read: The 180-second peak persists across displayed budgets, but all cells reuse the same small event set.
Evidence: Executable-depth replay; no queue position, rejects, latency, or official-settlement verification.
```

Do not use a clever headline that overstates the result. Put interpretation in the `Read` paragraph. “This rule makes money” is not a neutral chart title; “Net PnL by entry rule and split” is.

## 7. Choosing the chart

Use the simplest form that matches the comparison.

| Analytical question | Default chart | Notes |
|---|---|---|
| How did a metric move through time? | Line | Aim for at least 8–12 time points. |
| Which rule/category is larger? | Sorted horizontal bar | Start at zero for absolute magnitudes. |
| How do validation and test compare? | Grouped bar or dot plot | Keep one scale and fixed category ordering. |
| How is a sample split across Up/Down or states? | Stacked bar | Show both count and percentage when concentration matters. |
| What is the distribution of trade PnL? | Histogram | Show zero, median, tails, and sample size. |
| How do distributions differ by rule/regime? | Box plot plus points or small-multiple histogram | Do not hide tiny samples behind a box. |
| Is one numeric feature associated with another? | Scatter | Aim for 12–20+ comparable observations; label outliers. |
| Which two-parameter regions work? | Heatmap | Show counts and fixed assumptions; control multiple-testing interpretation. |
| How does PnL accumulate by trade? | Equity/cumulative PnL line | Add drawdown or loss markers only if readable. |
| What explains a start-to-end change? | Waterfall | Use only when components add cleanly. |
| How concentrated is PnL? | Ranked bar/Pareto | Show top trade/day/market share. |
| What is the exact audit record? | Table | Use when exact lookup matters more than shape. |

### Chart-specific rules

#### Lines

- Use a line only for an ordered continuous axis, usually time.
- Keep the raw observation grain clear.
- Use 2 px as the default focal stroke; 1–1.5 px for context lines.
- Add markers only when points are sparse or each observation matters.
- Direct-label line ends when possible.
- Use dashed neutral lines for benchmarks, zero, 50% probability, or calibration ideals.
- Do not smooth financial or trading series unless the smoothed series is explicitly labeled and the raw series remains available.

#### Bars

- Standard magnitude bars start at zero.
- Sort descending unless order is temporal, ordinal, or semantically fixed.
- Use horizontal bars for long rule names.
- One measure across categories normally uses one color. Highlight a single focal category only when the narrative requires it.
- Do not assign a different rainbow color to every bar.
- Put exact values at bar ends when the labels fit.
- Signed bars must show a strong zero line and reserve space on both sides.

#### Scatter plots

- Use observations at one consistent grain; do not mix totals and individual markets.
- X and Y must share population, filters, and time window.
- Show `n`, and retain a volume/sample-size field for tooltip reliability checks.
- Use size only if a third variable materially changes the interpretation.
- Label outliers or a small number of decision-relevant points, not every point in a dense cloud.
- Add a regression line only when the model and uncertainty are relevant; never use it as decoration.

#### Histograms and distributions

- Use stable, interpretable bin boundaries.
- Mark zero, median, and any cost hurdle.
- Do not hide losing tails with a truncated domain.
- If wins are extremely skewed, show a log or symlog companion view and label the transform prominently.
- Report median, mean, max loss, and concentration rather than relying on the picture alone.

#### Stacked composition

- Use no more than five meaningful categories.
- Keep stack order consistent across panels.
- For Up/Down, preserve the same color mapping everywhere.
- If exact cross-category comparison is more important than composition, use grouped bars instead.

## 8. Color system for charts

### Palette policy

Choose one palette policy per chart:

- **Single-root preferred:** one non-neutral color plus shades and neutral references. Default for simple lines, bars, distributions, scatters, and rankings.
- **Two-root cap:** at most two non-neutral roots plus neutrals. Default for signed values, Up/Down, focal-versus-context, validation-versus-test, and benchmark comparisons.
- **Multi-category exception:** up to five roots when category identity is the actual analytical point. Group additional categories into `Other` or change the chart.

### Approved roots

```css
--chart-blue-xlight: #e0f2fe;
--chart-blue-light:  #7dd3fc;
--chart-blue:        #38bdf8;
--chart-blue-mid:    #0284c7;
--chart-blue-dark:   #075985;

--chart-red-xlight:  #fee2e2;
--chart-red-light:   #fca5a5;
--chart-red:         #ef4444;
--chart-red-mid:     #b91c1c;
--chart-red-dark:    #7f1d1d;

--chart-orange-light:#fdba74;
--chart-orange:      #f97316;
--chart-orange-dark: #9a3412;

--chart-gold:        #eab308;
--chart-olive:       #84cc16;
--chart-pink:        #ec4899;

--chart-neutral-light:#a1a1aa;
--chart-neutral:      #52525b;
--chart-neutral-dark: #27272a;
```

The default multi-category order is blue, gold, orange, olive, pink. Do not introduce purple, teal, or arbitrary library defaults unless a task has a concrete semantic need.

### Semantic mapping

- Positive return/edge/ROI: blue.
- Negative return/loss/adverse slippage: red.
- Marginal, fragile, warning, or near-threshold: orange.
- Near zero: neutral grey.
- Benchmark/reference/ideal line: dark or light neutral, usually dashed.
- Passed validation/status: green may be used in a badge or small status mark, not as the default positive data scale.
- Failed validation/status: red may be used in a badge, but do not confuse a status color with a quantitative magnitude scale.
- Missing data: near-black or hatched neutral with `—`; never map missing to zero.
- No eligible trades: separate state from missing data and real zero.

### Stable series mappings

Within one report, the same entity must keep the same color, marker, and order everywhere. If `Up` is blue in one chart it cannot become orange in another. Define the mapping once in code rather than relying on a chart library’s implicit category order.

Example:

```ts
const SERIES = {
  up: { color: "#38bdf8", lineStyle: "solid", marker: "circle" },
  down: { color: "#f97316", lineStyle: "solid", marker: "square" },
  validation: { color: "#7dd3fc", fillOpacity: 0.55 },
  test: { color: "#0284c7", fillOpacity: 1 },
  benchmark: { color: "#a1a1aa", lineStyle: "dashed" },
};
```

Never depend on color alone. Pair color with direct labels, ordering, marker shape, open versus filled marks, or line style.

## 9. Heatmaps

Heatmaps are a first-class report form for parameter surfaces, timing × rule comparisons, regime matrices, feature correlation, confusion/calibration matrices, and dense condition atlases.

### When to use a heatmap

Use a heatmap when:

- Both axes are meaningful dimensions or ordered parameter values.
- The reader needs to see regions, ridges, cliffs, instability, or isolated pockets.
- There are enough cells for spatial pattern to matter.
- A table would be slower to scan and a scatter would obscure the matrix structure.

Do not use a heatmap when:

- One axis has only one meaningful value.
- There are fewer than roughly 8 useful cells and exact comparison is easier with bars or a table.
- Cell sample sizes differ wildly and cannot be shown.
- The surface is mostly missing values.
- The apparent pattern comes from tuning on the same few markets without a clear multiple-testing warning.

### Matrix construction

- X-axis should usually be the dimension read left-to-right: time to close, threshold, horizon, or budget.
- Y-axis should be the dimension read top-to-bottom: rule, regime, side, fee stress, or second threshold.
- Sort ordered parameters numerically, not lexicographically (`30s, 60s, 120s`, not `120s, 30s, 60s`).
- Preserve semantic category order where one exists; otherwise order by a stable rule defined before looking at the result.
- Do not reorder rows independently for each heatmap if panels are meant to be compared.
- Use square-ish cells when dimensions are symmetric; use rectangular cells when labels or the number of columns require it.
- Keep cell geometry identical across directly comparable heatmaps.

### Scale types

Choose the scale from the metric semantics, not from which palette looks best.

#### Diverging scale

Use for signed ROI, signed PnL, signed bps, residuals, forecast error, and differences from a benchmark.

- The semantic center is normally exactly zero.
- Negative is red, near-zero is grey, positive is blue.
- Use symmetric limits around zero when comparing positive and negative magnitude is the point.
- Use asymmetric fixed thresholds only when the thresholds have explicit trading meaning and are documented.
- Do not let a single outlier wash out the entire surface; use robust limits or threshold bins and preserve the exact outlier value in the label/tooltip.

Current preferred nine-step diverging palette:

```css
--heatmap-1: #7f1d1d;
--heatmap-2: #b91c1c;
--heatmap-3: #ef4444;
--heatmap-4: #f97316;
--heatmap-5: #52525b;
--heatmap-6: #38bdf8;
--heatmap-7: #0284c7;
--heatmap-8: #0369a1;
--heatmap-9: #075985;
```

Current default ROI/bps thresholds when a fixed trading interpretation is useful:

| Value | Fill |
|---:|---|
| `<= -50` | `#991b1b` / deep red |
| `(-50, -25]` | `#ef4444` / red |
| `(-25, -5]` | `#f97316` / orange |
| `(-5, 0]` | `#52525b` / neutral grey |
| `(0, 15)` | `#38bdf8` / light blue |
| `[15, 30)` | `#0284c7` / medium blue |
| `>= 30` | `#075985` / deep blue |

These thresholds are defaults, not universal truths. Change them when the metric’s economically meaningful breakpoints differ, and state the new thresholds in the legend or subtitle. Comparable panels must use the same thresholds.

#### Sequential scale

Use for non-negative quantities such as volume, opportunity size, absolute move, trade count, depth, latency, or sample coverage.

- Use light-to-dark blue for “more”.
- Use light-to-dark red only when “more” is uniformly worse, such as reject rate or drawdown magnitude.
- Start from a meaningful zero or minimum.
- Never use a diverging scale for a quantity that cannot be negative.

Preferred blue sequential anchors:

```text
#e0f2fe → #7dd3fc → #38bdf8 → #0284c7 → #075985
```

Preferred adverse red sequential anchors:

```text
#fee2e2 → #fca5a5 → #f87171 → #dc2626 → #991b1b → #7f1d1d
```

#### Categorical matrix

If cells are states rather than magnitudes—`pass`, `fail`, `pending`, `missing`—use a small categorical palette and explicit text/icons. Do not imply continuous distance between categories.

### Domain and normalization

- For a family of comparable heatmaps, calculate one shared domain from the combined comparison set.
- For a standalone exploratory heatmap, robust limits may use the 2nd–98th or 5th–95th percentiles, but the caption must disclose clipping.
- Never normalize each row or column independently unless the question specifically concerns within-row/within-column relative shape. Label that normalization prominently.
- Never compare colors across panels that use different domains without visibly separate legends.
- If a value is capped for color, the cell label and tooltip still show the uncapped value.

### Cell labels

Default to exact labels inside cells when the matrix is small enough:

- ROI/PnL rate: signed percentage.
- Return: signed bps.
- Count: integer, optionally prefixed by `n=` in a secondary line.
- Two-line cell: primary metric large; sample size or trade count small.

Example cell:

```text
+39.49%
n=15 · 14W/1L
```

Cell text must switch between near-white and near-black based on fill luminance. Add a subtle keyline when adjacent cells have similar colors. Do not use tiny text to force all statistics into the cell; move secondary details to the tooltip.

### Missing, empty, and unreliable cells

Treat these states separately:

- Real zero: neutral quantitative color with `0.00`.
- No eligible trades: dark neutral with `n=0`.
- Missing/not collected: near-black or hatched with `—`.
- Insufficient sample: retain the quantitative fill but add a visible low-confidence cue such as an outline, dot, hatch, or reduced saturation; include `n`.
- Invalid combination: black/transparent with `N/A`.

Never color `n=0` as profitable because a computed ROI defaulted to zero.

### Heatmap tooltips

Hover/focus should show enough evidence to audit a cell:

```text
Rule: Spot trend
Entry: 180s to close
Budget: $10
Max quote offset: 10s
Fee stress: $0.02 / contract
Trades: 15
Unique markets: 15
Wins / losses: 14 / 1
PnL: +59.23 USDC
ROI: +39.49%
Max loss: -0.61 USDC
Evidence: executable-depth replay
```

Tooltips must be keyboard-focusable, remain within the viewport, and never be the only place that units or sample size exist.

### Heatmap legends

- Place a compact horizontal legend above or below the plot.
- Show exact endpoints, zero, and economically meaningful thresholds.
- Label the metric and unit directly in the legend.
- If thresholds are discrete, draw discrete swatches rather than a continuous gradient.
- If cells are clipped to robust limits, label the end bins `≤` and `≥`.

### Heatmap interpretation rules

- Favor broad stable regions over isolated best cells.
- Explicitly call out cliffs where a small parameter change flips the sign.
- Compare neighboring cells, not only the maximum.
- Display the number of parameter combinations searched and the number of unique underlying markets.
- Treat repeated cells built from the same events as correlated evidence.
- Mark the selected/frozen rule with a restrained outline or glyph; do not recolor it and destroy the shared scale.
- If a surface is discovery-only, say so above or below the heatmap.
- If a forward/paper cell contradicts the discovery peak, show that contradiction prominently rather than hiding it in prose.

### Reference heatmap color function

```ts
function signedPerformanceColor(value: number | null): string {
  if (value == null || !Number.isFinite(value)) return "#0d0d0d";
  if (value >= 30) return "#075985";
  if (value >= 15) return "#0284c7";
  if (value > 0) return "#38bdf8";
  if (value > -5) return "#52525b";
  if (value > -25) return "#f97316";
  if (value > -50) return "#ef4444";
  return "#991b1b";
}
```

Use a numeric encoding for the metric even if the renderer’s heatmap API calls the visual channel `color`. Do not accidentally declare a numeric ROI field as nominal/categorical.

## 10. Titles, subtitles, annotations, and reads

### Title pattern

`[Metric] by [comparison dimension(s)]`

Examples:

- `ROI by side rule and entry time`
- `Average net SOL return by model lane and split`
- `Trade count and side mix by frozen rule`
- `Quote disagreement by venue and quote asset`
- `Maximum executable size by price and seconds to close`

### Subtitle pattern

`[Market/instrument] · [time range or snapshot] · [sample/grain] · [cost/fill assumptions] · [evidence level]`

Examples:

```text
SOL 5m Up/Down · Jun 15 replay · 22 resolved markets · $10 VWAP · $0.02/contract fee stress
Binance SOLUSDT 5m · 47,375 rows · 4 bps round trip · directional spot proxy only
Polymarket asks · 100 frozen markets · accepted paper orders · exact fees and official settlement
```

### Annotations

- Use annotations only for a decision-relevant peak, failure, break, outlier, threshold, or benchmark.
- Keep annotation text under roughly two short lines.
- Attach it to the evidence with a quiet neutral connector.
- Do not annotate every bar or point.
- Use exact values in the annotation when the claim depends on magnitude.
- A selected-rule outline is preferable to a starburst, glow, or different color scale.

### “Read” paragraph

Every major chart should be followed by a concise interpretation:

```text
Read: [supported pattern]. [important comparison or instability]. [what this permits or rules out].
```

Good:

> Read: The 180-second spot-trend region is positive across displayed budgets, but the result reuses the same 22 events and the promoted paper slice later lost. Keep it as a frozen hypothesis, not a capital rule.

Bad:

> This amazing chart clearly proves the strategy works.

## 11. Evidence and trading context inside visuals

A visually strong chart is still misleading if it omits trading reality. Include the following in the subtitle, caption, annotation, or adjacent evidence strip as relevant:

- Data source and time range.
- Observation grain.
- Trade count and unique market count.
- Entry rule and side rule.
- Entry timing and quote-age tolerance.
- Selected contract price or full VWAP.
- Budget/size.
- Fees.
- Slippage/price impact.
- Depth assumption.
- Wins and losses.
- PnL and ROI.
- Maximum loss/drawdown.
- Concentration by trade, market, day, side, or regime.
- Evidence level: proxy-only, backtest, paper-traded, fillable, live-filled, or settlement-backed.

Do not put all of this into the visual title. Use the subtitle, tooltip, compact metadata strip, and exact data table.

Recommended evidence badge vocabulary:

```text
PROXY ONLY
BACKTEST — NO DEPTH
EXECUTABLE-DEPTH REPLAY
PAPER — QUOTE OBSERVED
PAPER — ACCEPTED FILL
LIVE FILLED
OFFICIAL SETTLEMENT VERIFIED
```

Status badges describe evidence quality, not whether a chart is profitable.

## 12. Tables and KPI strips adjacent to charts

Use a chart for shape and a table for exact lookup. The underlying chart table should retain more than bare `x`, `y`, and `series` columns when audit context exists.

### KPI strip

Keep KPI strips compact and decision-relevant. Typical fields:

- Unique markets.
- Trades.
- W–L.
- Net PnL.
- ROI.
- Max loss/drawdown.
- Largest-trade/day share.
- Evidence level.

Do not make one KPI card per trivial metric. Four to eight cards is usually enough. Use neutral cards; reserve colored backgrounds for a small status badge.

### Tables

- Full available width, one per row.
- Sticky header for long tables.
- Left-align text; right-align numeric cells.
- Use tabular numerals.
- Preserve units in headers.
- Use subtle row separators, not a heavy border around every cell.
- Freeze important identity columns if horizontal scrolling is necessary.
- Default to a decision-relevant sort and state it.
- Use blue/red text sparingly for signed values; retain the `+`/`−` sign.
- Add the exact source path or dataset identifier near the table.
- Do not dump thousands of raw rows into the main report; provide a filtered table or downloadable local artifact when necessary.

## 13. Interaction

Interaction should improve inspection without becoming required to understand the result.

### Required where feasible

- Hover and keyboard-focus tooltips.
- Click-to-expand chart/heatmap modal.
- Close modal by button, `Escape`, or backdrop click.
- Preserve chart state and return it to the original location when the modal closes.
- Exact-data disclosure or table.
- Visible focus ring.

### Expanded modal

```css
.chart-dialog {
  width: min(96vw, 1800px);
  max-width: none;
  height: min(94vh, 1200px);
  padding: 48px 18px 18px;
  border: 1px solid #555;
  background: #000;
  color: #eee;
}

.chart-dialog::backdrop {
  background: rgba(0, 0, 0, 0.88);
}

.chart-dialog-content {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.chart-dialog-content > *,
.chart-dialog-content svg {
  width: 100% !important;
  max-width: none !important;
  height: auto !important;
}
```

The cursor may be `zoom-in` over an expandable chart. Do not trigger expansion when the user clicks a link, button, table disclosure, or source tooltip inside the panel.

### Avoid

- Animation that delays reading.
- Auto-playing transitions.
- Hover-only essential facts.
- Dragging as the only way to see an axis range.
- Cross-filter systems or dashboard infrastructure for a static research question.
- Remote script dependencies in a portable local HTML report.

## 14. Responsive behavior

- Charts remain one per row at every viewport size.
- At 760–820 px and below, reduce page padding and allow titles to wrap.
- Do not reduce axis labels to unreadable sizes.
- For wide heatmaps, prefer a labeled horizontal scroll container or a deliberate stacked/mobile representation.
- Keep Y-axis labels visible while horizontally scrolling if practical.
- Legends wrap into multiple lines above/below the plot.
- Tooltips portal to a fixed bottom sheet or viewport-safe overlay on touch devices.
- Expanded charts should use the entire available viewport.
- Test at approximately 390 px mobile width, 768 px tablet width, 1440 px laptop width, and a wide desktop.

## 15. Portable artifact chart contract

When a report is built from the repository’s artifact/builder workflow, keep visual intent explicit in the artifact rather than patching arbitrary colors after generation.

Example:

```ts
const chart = {
  id: "signal_entry",
  title: "ROI by side rule and entry time",
  subtitle:
    "SOL 5m · $10 budget · max 10s quote offset · $0.02/contract fee stress · 22 resolved markets",
  type: "heatmap",
  intent: "comparison",
  question: "Which entry-time and side-rule regions retain positive ROI after modeled costs?",
  rationale: "A matrix exposes broad regions and unstable isolated cells better than a ranked table.",
  dataset: "signal_entry",
  sourceId: "depth_grid",
  encodings: {
    x: { field: "entry_seconds", type: "ordinal", label: "Seconds to close" },
    y: { field: "signal_rule", type: "nominal", label: "Side rule" },
    color: { field: "roi_pct", type: "quantitative", label: "ROI", unit: "%" },
  },
  valueFormat: "number",
  unit: "%",
  layout: "full",
  comparisonContext: {
    grain: "entry-time and side-rule parameter cell",
    denominator: "eligible executable-depth replay trades",
    unit: "percent return on modeled spend",
  },
  surface: {
    surface: "card",
    showControls: false,
    viewMode: "visualization",
  },
};
```

Artifact rules:

- Use `layout: "full"` for every report chart.
- Use a numeric/quantitative encoding for numeric color metrics.
- Include `question`, `rationale`, and `comparisonContext` when supported.
- Keep chart datasets rich enough for exact inspection and tooltips.
- Use explicit source metadata and local paths.
- Do not bolt on a second remote chart runtime.
- Package the report so it remains useful offline.
- If final CSS overrides are required, keep them small, named, and idempotent.

## 16. Canonical full-width dark override

For generated portable reports that otherwise inherit narrower defaults, this is the intended override shape:

```css
:root {
  color-scheme: dark !important;
  --portable-canvas: #000 !important;
  --portable-surface: #070707 !important;
  --portable-surface-subtle: #0d0d0d !important;
  --portable-ink: #f2f2f2 !important;
  --portable-muted: #c9c9c9 !important;
  --portable-tertiary: #a9a9a9 !important;
  --portable-table-text: #d2d2d2 !important;
  --portable-border: rgba(255, 255, 255, 0.13) !important;
  --portable-accent: #8ac5ff !important;
}

html,
body {
  background: #000 !important;
  color: #f2f2f2 !important;
}

.portable-fallback,
.portable-block-stack,
.portable-content-card,
.portable-static-chart,
.report-content-grid,
.analytics-layout-canvas {
  width: 100% !important;
  max-width: none !important;
}

.portable-block-stack {
  grid-template-columns: minmax(0, 1fr) !important;
}

.portable-layout-half,
.portable-layout-full {
  grid-column: 1 !important;
}

.portable-static-chart-light {
  display: none !important;
}

.portable-static-chart-dark {
  display: block !important;
}
```

Do not blindly paste this into unrelated third-party documents. It is the repository research-report default.

## 17. Accessibility and perceptual QA

- Text and meaningful labels must meet reasonable contrast on their actual background.
- Every color distinction must have a non-color companion: sign, label, line style, marker shape, ordering, hatch, or outline.
- Keyboard users must reach tooltips, disclosures, and dialog controls.
- Dialogs need an accessible name and must return focus on close.
- Charts need a meaningful accessible label or nearby text summary.
- Exact data should be available as a semantic table when practical.
- Avoid red/green-only distinctions.
- Test heatmap label contrast at every palette step.
- Test grayscale: the takeaway should remain recoverable from labels, signs, and structure.
- Do not encode magnitude with line thickness.
- Keep benchmark and zero lines visible but subordinate to marks.
- Check that labels do not clip at 125–200% browser zoom.

## 18. Final visual QA checklist

Before shipping an HTML report, verify all of the following.

### Analytical integrity

- [ ] Each chart answers a stated analytical question.
- [ ] Chart type matches the comparison.
- [ ] Data source, time range, grain, and filters are correct.
- [ ] Units and denominators are visible.
- [ ] Trade count and unique market count are not conflated.
- [ ] Fees, slippage, price, size, and depth assumptions are stated where relevant.
- [ ] Wins, losses, PnL, ROI, max loss/drawdown, and concentration are available where relevant.
- [ ] Evidence level is explicit.
- [ ] Proxy/backtest output is not described as fillable or live.
- [ ] A parameter search discloses the search count and correlated/reused samples.

### Layout

- [ ] Every chart/image/heatmap is one per row.
- [ ] Every visual uses the full available width with no shrinking max-width cap.
- [ ] No thumbnail gallery or side-by-side visual grid exists.
- [ ] Chart height fits its row count and label density.
- [ ] Prose is readable but does not constrain visual width.
- [ ] Mobile layout stays single-column.

### Color and scales

- [ ] Colors come from an explicit declared palette.
- [ ] The chart uses one root, two roots, or a justified five-root maximum.
- [ ] Same entity keeps the same mapping across the report.
- [ ] Signed performance uses red → grey → blue with a true zero center.
- [ ] Sequential metrics use a sequential scale.
- [ ] Missing, `n=0`, invalid, and real zero are visually distinct.
- [ ] Comparable heatmaps share domains and thresholds.
- [ ] No chart uses a library rainbow default.
- [ ] Color is not the only carrier of meaning.

### Labels and interaction

- [ ] Title is descriptive and non-hyped.
- [ ] Subtitle includes scope, sample, assumptions, and unit.
- [ ] Axis labels, ticks, direct labels, and legends do not collide or clip.
- [ ] Long category labels have enough left margin.
- [ ] Signed bars have a visible zero line and enough space on both sides.
- [ ] Heatmap cells show readable values or inspectable tooltips.
- [ ] Tooltips fit in the viewport and work by keyboard.
- [ ] Click-to-expand works, and the chart returns correctly on close.
- [ ] Exact data/source inspection remains available.

### Final-context inspection

- [ ] Open the actual generated HTML, not only the source spec.
- [ ] Inspect the dark screen version.
- [ ] Inspect the print/light version if the report may be printed or converted.
- [ ] Check approximately 390, 768, 1440, and wide-desktop widths.
- [ ] Check browser zoom and long labels.
- [ ] Check that active 5-minute reporting contains no accidental legacy 15-minute data.
- [ ] Confirm the visual supports the written takeaway and does not hide contradictory evidence.

## 19. Minimal report-design instruction for future work

The following sentence is enough to invoke this standard:

> Follow `report-design.md`: black research theme, single-column full-width charts, explicit palette and scales, thresholded audit-friendly heatmaps, assumptions-rich subtitles, exact evidence context, and click-to-expand visual inspection.

If a future request conflicts with this document, the request wins. Otherwise this document is the default.

## 20. Current repository references

Use these as implementation references, not as permission to copy stale data or legacy strategy logic:

- `apps/research/experiments/solana_alpha_registry/finalize_visual_report.ts` — canonical black, full-width, single-column overrides; heatmap colors; click-to-expand behavior.
- `apps/research/experiments/solana_alpha_registry/build_visual_artifact.ts` — full-width heatmap artifact contracts, titles, subtitles, and evidence framing.
- `apps/research/outputs/alpha_lane_rebuilds/build_report_artifact.ts` — bar/stacked-bar chart contracts, comparison context, and reference lines.
- `apps/research/library/styles.css` — research library dark shell, expanded media treatment, readable tables, and responsive behavior.

The visual rules in this document are stable; the trading conclusions and data inside example reports are not. Always use the newest valid local 5-minute evidence for the actual report.
