# REPORT RULES

This file is the complete portable instruction for creating quantitative research reports. Copy this single file into another repository and tell the LLM to follow it. It does not depend on any other design document.

The report has one job: make the evidence easy to inspect and make the next decision hard to misunderstand. It is not a marketing page, a dashboard, a notebook dump, a slide deck, or a collection of bullet points.

## 0. Normative language and authority

The words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are literal requirements.

- **MUST / MUST NOT**: required. A report that violates the rule fails review.
- **SHOULD / SHOULD NOT**: required unless the report documents a concrete reason for an exception.
- **MAY**: optional.

When instructions conflict, use this order:

1. The user's current request and the experiment's frozen research contract.
2. Data integrity, causal timing, validation integrity, and truthful evidence labels.
3. This file.
4. Framework or chart-library defaults.
5. Author preference.

Do not ask the user to choose a style. This file defines the style. Do not invent a second visual system. Do not weaken the evidence requirements to make a prettier report.

---

# PART I — WHAT THE REPORT MUST PROVE

## 1. The report is a decision artifact

Every report MUST support exactly one current decision. For quantitative trading research, use one of these labels:

| Decision | Meaning |
|---|---|
| `reject` | The candidate failed or cannot be distinguished from noise. |
| `diagnostic_only` | The work explains data or behavior but does not justify a trade or promotion. |
| `continue_research` | A bounded question remains worth testing, but the candidate has not earned paper validation. |
| `paper_candidate` | A frozen rule survived meaningful unseen-time and net-cost tests and may begin forward paper validation. |
| `fillable_candidate` | Quotes, depth, latency, partial fills, rejections, fees, and venue constraints support the stated size. |
| `small_live_candidate` | Forward settled results remain acceptable at tiny controlled risk and operational loss controls are ready. |

The report MUST NOT end with several possible decisions. It MUST NOT use phrases such as “promising,” “looks good,” or “potentially profitable” as a substitute for a gate.

The first viewport MUST state:

- the exact research question;
- the one decision label;
- the strongest reason for that decision;
- the achieved evidence level;
- the evaluation period and population;
- the frozen fill and all-in cost assumption;
- the experiment, run, or artifact identifier.

Use a compact header and a dense decision table. Do not use a marketing hero, giant decorative number, row of oversized KPI cards, or bullet-summary opener.

## 2. Profit is not a visual style

A report moves work closer to profit only when it reduces uncertainty about executable net value. A larger backtest number does not satisfy this requirement.

Every profit-oriented report MUST separate this chain:

```text
data
→ observable state
→ prediction or conditional distribution
→ frozen action rule
→ executable order and fill
→ gross outcome
→ costs and operational drag
→ net PnL
→ risk, concentration, and capacity
→ promotion decision
```

The report MUST show where evidence stops. If the data supports prediction but not execution, say so. If it supports a backtest but not fillability, say so. If it supports a paper result but not settled live PnL, say so.

Never promise profit. Never call a strategy proven. Never let visual polish upgrade weak evidence.

## 3. Required evidence contract

Before building the report, create an internal evidence inventory with these fields:

| Dimension | Required information |
|---|---|
| Identity | Experiment ID, run ID, candidate/rule ID, code/config version |
| Population | Asset, venue, market type, eligibility, date range, timezone |
| Support | Raw rows, signals, trades/events, effective count, unique periods/markets/assets |
| Data quality | Missingness, duplicates, gaps, outliers, repairs, structural breaks |
| Information clock | Last feature timestamp, decision timestamp, order timestamp, earliest fill timestamp, exit timestamp |
| Evaluation | Train, validation, purge, embargo, walk-forward folds, test, locked holdout, forward period |
| Selection | Hypothesis timing, variants tried, parameters searched, freeze point, negative results |
| Economics | Price convention, fees, spread, slippage, funding/borrow, impact, latency, safety margin |
| Risk | Drawdown, recovery, tails, worst event, exposure, leverage, concurrency |
| Concentration | Top-N contribution, time/side/asset/regime contribution, leave-one-out behavior |
| Comparators | Unconditional, random, simple rule, prior policy, simple model |
| Operations | Quote/depth source, fill model, rejected/partial fills, size, capacity, venue limits |
| Provenance | Exact source paths, query/code path, hashes if available, output path |

Do not begin layout, prose, or chart styling before this inventory exists. Do not invent a missing field. Mark missing evidence explicitly and downgrade the decision.

## 4. Required report order

Use this order for every serious quantitative report. Do not rearrange it to make a positive result feel stronger.

### 4.1 Decision and evidence scorecard

Open with one compact table:

| Gate | Required evidence | Observed result | Frozen threshold | Status | Main failure risk |
|---|---|---:|---:|---|---|
| Data and timing | Audited data and causal clocks | | | | |
| Conditional information | Effect versus unconditional/simple baseline | | | | |
| Unseen-time survival | Frozen walk-forward/test result | | | | |
| Net economics | Edge after costs, delay, impact, and margin | | | | |
| Stability | Folds, nearby parameters, regimes, sides | | | | |
| Risk and concentration | Drawdown, tails, top-N and bucket ownership | | | | |
| Operational evidence | Fill, latency, capacity, venue constraints | | | | |

Thresholds MUST be frozen before the evaluation they judge. If a threshold was selected after seeing the result, label it exploratory and do not use it to promote the candidate.

### 4.2 Data quality and information boundary

Show what data exists, what is missing, when each field becomes observable, and how a decision could actually be filled. Include a data-coverage graphic and a split/timing diagram.

### 4.3 Unconditional baseline

Show the target distribution and the simplest baseline before showing the candidate. A conditional edge is meaningless without the unconditional distribution it claims to change.

### 4.4 Conditional evidence

Show how the future outcome changes with the observable state. Include uncertainty, support, stability through time, and simple alternative explanations. Separate descriptive association from the trading policy.

### 4.5 Unseen-time validation

Show every meaningful unseen fold. Include failed folds, no-trade folds, worst fold, fixed-simple-baseline performance, and selection-procedure performance. Do not show only the aggregate.

### 4.6 Net economics and execution

Reconcile the economics in one explicit bridge:

```text
gross edge
- entry and exit fees
- spread
- slippage
- funding or borrow
- market impact
- latency or delay loss
- rejected/partial fill effect
- estimation safety margin
= decision-grade net edge
```

Show break-even cost, break-even delay, turnover, exposure, concurrency, capacity, and size sensitivity. Gross results may appear only to explain where edge is consumed.

### 4.7 Robustness, risk, and failure

Show nearby parameters, alternate splits, time/regime/side slices, cost and delay stress, top-N removal, leave-one-bucket-out results, negative controls, drawdown, recovery, tails, and concentration. Failures MUST be as visible as successes.

### 4.8 Decision and next falsification test

End with:

1. one decision label;
2. the evidence that earned it;
3. the evidence blocking the next gate;
4. one bounded next falsification test;
5. frozen success and failure thresholds;
6. required new independent support;
7. the action if the test fails.

“Try more models” is not a falsification test. “Run the frozen rule on the next 20 independent periods using full-depth VWAP and reject if average net return is nonpositive” is a falsification test.

### 4.9 Methods and provenance

List exact source files, queries, code paths, configurations, timestamps, cost assumptions, exclusions, experiment variants, and generated artifacts. Every headline number and every chart MUST trace to a source.

## 5. Short failure report

If the evidence cannot support the full report, do not manufacture length or graphics. Produce a short report with only:

1. the downgraded decision;
2. a blocking-evidence table;
3. the limited conclusions the current data actually supports;
4. one next falsification test.

Do not fill a weak report with generic bullets, speculative recommendations, placeholder charts, or decorative imagery.

---

# PART II — CHARTS AND EXPLANATION

## 6. Visual evidence is mandatory

Every substantive section MUST contain a visual evidence object: a quantitative chart, exact table, timeline, matrix, or causal diagram.

Every material quantitative conclusion MUST have a corresponding chart. A table alone is not enough when the claim concerns shape, time, distribution, interaction, stability, risk, or sensitivity.

Every chart MUST have an exact table, downloadable local data, or inspectable data disclosure. The chart communicates shape; the data communicates exactness.

Do not invent data to satisfy the chart requirement. If no data supports a chart, identify the missing evidence and downgrade the report.

## 7. One chart per row

This is absolute:

- Render one chart, heatmap, diagram, image, or major table per row.
- A chart MUST fill the report column.
- Never use side-by-side chart grids.
- Never use thumbnail galleries, contact sheets, detached chart indexes, or dashboard tile layouts.
- Never put a chart beside a table.
- Never put explanatory prose in a narrow column beside a chart.
- Never stretch the report itself edge-to-edge across an ultrawide display.

The screen report column MUST be centered and approximately `1120–1200px` wide. The chart fills that column. Prose is narrower inside the same column. A click-to-expand chart MAY use approximately `96vw × 94vh` for detailed inspection.

Multiple aligned panels MAY live inside one figure only when they share an x-axis or scale and jointly answer one question. Stack those panels vertically. Examples: equity over drawdown over exposure; outcome heatmap over support heatmap; price over data-quality flags.

## 8. Every chart uses the same explanation contract

Place the following around every major chart, in this exact order.

### 8.1 Decision question

State the uncertainty the chart is intended to resolve.

Good:

> Does the validation-selected region remain net positive across untouched folds after a one-bar delay?

Bad:

> Performance analysis

### 8.2 Neutral chart title

State what is plotted without claiming the conclusion.

Good:

> Net return by walk-forward fold and entry-delay assumption

Bad:

> The strategy definitely works

### 8.3 Scope subtitle

Use this pattern:

```text
[population] · [UTC range] · [split/fold] · [sample and denominator] · [unit] · [cost/fill assumptions] · [evidence level]
```

The subtitle MUST expose the assumptions needed to interpret the plot. Do not hide them in a distant method section.

### 8.4 How to read this chart

Explain:

- what the x-axis represents;
- what the y-axis represents;
- what color, shape, line style, bands, and annotations mean;
- what the zero, baseline, hurdle, or reference line means;
- how uncertainty and support are encoded;
- whether values are gross or net;
- which split or fold is shown.

Do not assume the reader knows the chart grammar.

### 8.5 The chart

Use the full centered report width. Preserve readable labels and exact units. Do not crop inconvenient data or use a scale that exaggerates the conclusion.

### 8.6 What it shows

Explain the actual evidence in a compact analytical paragraph. Include:

- direction and magnitude;
- uncertainty;
- effective support;
- heterogeneity across time, folds, regimes, sides, or assets;
- whether the effect is broad or concentrated;
- the comparison with the relevant baseline.

Do not write “the chart shows performance varies.” State how much, where, and with what support.

### 8.7 Why it matters

State exactly how the chart changes a decision: promote, reject, size down, gather data, alter execution, or run a specific test.

### 8.8 What it does not prove

State the strongest limitation, missing evidence, alternative explanation, or invalid inference. This is mandatory even when the chart looks favorable.

### 8.9 Evidence footer

Include:

```text
source path · query or generation path · experiment/variant ID · frozen assumptions · generated timestamp
```

## 9. Required chart stack for a serious candidate

Use this sequence. A chart may be omitted only when it is genuinely inapplicable, and the report MUST say why.

| Order | Required chart | Question answered | Required context |
|---:|---|---|---|
| 1 | Data coverage and quality timeline | Is the sample trustworthy? | gaps, repairs, breaks, missingness, split boundaries |
| 2 | Target/unconditional distribution | What must the candidate beat? | tails, base rate, cost hurdle, sample support |
| 3 | Feature distribution over time and by split | Is the input stable and causally constructed? | train-fitted boundaries, drift, missingness |
| 4 | Conditional profile | Does outcome change with observable state? | interval, baseline, support, train/valid/test |
| 5 | Train/validation/test outcome heatmaps | Does the same region survive unseen time? | identical bins, fixed scale, frozen selection |
| 6 | Matched support heatmap | Are favorable cells adequately supported? | raw and effective count, periods, folds |
| 7 | Event path | Is the move observable and fillable after the signal? | matched control, delay, mean/median, interval, MFE/MAE |
| 8 | Parameter-neighborhood surface | Is the chosen point a broad plateau? | selected point, support contours, boundary stress |
| 9 | Fold matrix and fold distribution | Is aggregate performance broadly owned? | counts, worst fold, sides/regimes, fixed baseline |
| 10 | Calibration or prediction-decile chart | Does model score order unseen outcomes? | predicted vs actual, support, simple model, net policy payoff |
| 11 | Net equity path | How does net PnL accumulate? | all costs, fold boundaries, realized/mark-to-market status |
| 12 | Underwater drawdown | What path pain produces the return? | max drawdown, recovery, worst period |
| 13 | Exposure and turnover | How much risk and trading create the result? | leverage, concurrency, holding time |
| 14 | Cost × delay surface | How tolerant is the edge to execution reality? | zero-profit contour, base assumption, size |
| 15 | Trade/outcome distribution | Are mean results hiding tails or skew? | median, quantiles, breakeven, worst loss |
| 16 | Concentration and leave-one-out | Who owns the profit? | top-N, period/side/asset/regime contribution |
| 17 | Negative-control comparison | Could the pipeline manufacture the result? | shuffled/random/simple controls and full search procedure |

Do not create seventeen weak charts to satisfy a count. Each chart must answer its question with real data. A missing required chart is a visible evidence gap, not permission to fabricate one.

## 10. Chart-selection rules

Use the following defaults. Do not choose a chart merely for visual variety.

| Analytical question | Required default | Do not use instead |
|---|---|---|
| Change through time | Line or step chart | unordered bars |
| Net PnL path | Net-equity line plus separate drawdown and exposure panels | equity alone |
| Distribution and tails | Histogram plus ECDF or quantile view | mean-only KPI or pie chart |
| Category ranking | Sorted horizontal bars | donut or vertical labels |
| Estimated effects | Dot-and-whisker plot | bars without intervals |
| Two-variable relationship | Scatter/hexbin with interval or binned profile | trend line without support |
| Two-state interaction | Outcome heatmap plus support heatmap | autoscaled winner heatmap |
| Parameter stability | Complete neighborhood heatmap/surface | best-parameter table |
| Time generalization | Fold matrix plus fold distribution | aggregate Sharpe card |
| Probability quality | Calibration plot and prediction deciles | feature importance |
| Additive change | Waterfall | disconnected KPI cards |
| Concentration | Contribution bars plus cumulative-share/Lorenz curve | top-trade list only |
| Execution quality | Slippage/fill distribution by size and latency | midpoint-fill backtest |
| Exact lookup | Table paired with the relevant shape chart | chart labels for every field |
| Information/execution flow | Simple directed diagram or timeline | decorative flowchart |

## 11. Chart-specific integrity rules

### 11.1 Lines

- Use a `2–2.5px` primary line and a quieter `1–1.5px` comparison line.
- Avoid point markers on dense lines.
- Mark split boundaries, execution events, and structural breaks only when relevant.
- A nonzero y-domain MUST be clearly labeled and analytically justified.
- Never smooth away a failure, drawdown, or regime break.

### 11.2 Bars

- Start quantitative bar axes at zero.
- Sort by value unless time, process, or registered order matters.
- Prefer horizontal bars for long labels.
- Use square corners and minimal outlines.
- Show uncertainty or support when the bar is an estimate.

### 11.3 Scatter and dense relationships

- Use opacity, hexbinning, or density contours when points overlap.
- Show marginal support or binned summaries when density is uneven.
- Label only decision-relevant outliers.
- A fitted line MUST include its uncertainty and out-of-sample status.
- Do not imply causality from association.

### 11.4 Distributions

- Show more than the mean.
- Mark zero, median, cost hurdle, and relevant tails.
- Use the same bins and domain for compared distributions.
- State whether observations are independent.
- Pair mean with median when tails can dominate.

### 11.5 Equity and drawdown

- Always show net equity and underwater drawdown as separate vertically aligned panels.
- Show exposure and turnover when they vary materially.
- Annotate costs, split boundaries, max drawdown, recovery, and position overlap.
- Never show an equity curve without the corresponding risk and concentration views.
- Never construct “equity” by cumulatively summing overlapping labels as if they were executable independent trades.

### 11.6 Heatmaps and parameter surfaces

- Use a heatmap only when both axes are meaningful dimensions.
- Order numeric parameters numerically, not lexicographically.
- Use identical bins, cell geometry, and color domains across train, validation, and test.
- Show an outcome heatmap and a support heatmap.
- Display raw count, effective count, unique periods/events, and fold coverage.
- Mask unsupported cells. Never color missing, invalid, or `n=0` cells as neutral or profitable.
- Use a diverging scale centered at the economic zero/hurdle for signed values.
- Use a sequential scale only when more is unambiguously more of one thing.
- Show the selected parameter inside the complete local neighborhood.
- Treat a single hot cell surrounded by failures as overfit until proven otherwise.
- Do not choose cells from the test heatmap.

### 11.7 Calibration and model charts

- Compare with base rate and a simple baseline.
- Show sample count per bin.
- Use predictions created strictly out of sample.
- Show predicted versus realized values and the net result of the frozen policy.
- Do not use feature importance as proof of edge.

### 11.8 Cost and delay surfaces

- Put all-in cost or size/slippage on one axis and entry delay on the other.
- Use net PnL, return, or average trade as the color value.
- Draw a zero-profit contour.
- Mark the conservative base assumption.
- Include a range extending beyond the favorable assumption.
- An edge that exists only at zero cost and zero delay is not actionable.

## 12. Axes, labels, legends, and annotations

- State units exactly once in an obvious place.
- Use four to six useful ticks by default.
- Use tabular numerals.
- Format precision consistently within a comparison.
- Use a true zero, hurdle, or benchmark line when it matters.
- Directly label series whenever practical.
- Use an unboxed legend above or below the plot only when direct labels would collide.
- Keep category order and color mapping identical across the report.
- Never use a dual y-axis unless no clearer aligned-panel alternative exists.
- Never rotate labels merely to force a cramped chart to fit; increase height or change orientation.
- Annotate only a decision-relevant peak, failure, break, outlier, threshold, or benchmark.
- Never place essential units, caveats, sources, or conclusions only inside hover.

---

# PART III — THE ONE VISUAL DESIGN

## 13. Design character

The report MUST look like a serious black research instrument:

- pure black canvas;
- near-white text;
- quiet neutral borders and gridlines;
- flat surfaces;
- compact hierarchy;
- generous separation between analytical sections;
- saturated color only in data marks, thresholds, and small status indicators;
- no decorative imagery or marketing styling.

The design should feel calm at first glance and dense during inspection. Density comes from evidence, aligned comparisons, exact labels, and explanation—not smaller type or more cards.

## 14. Canonical tokens

Use these exact defaults unless the user explicitly provides a different brand system:

```css
:root {
  color-scheme: dark;

  --canvas: #000000;
  --surface: #080808;
  --surface-2: #101010;
  --surface-3: #171717;

  --ink: #f2f2f2;
  --ink-muted: #c4c4c4;
  --ink-faint: #929292;

  --line: rgba(255, 255, 255, 0.10);
  --line-strong: rgba(255, 255, 255, 0.20);
  --gridline: rgba(255, 255, 255, 0.09);

  --blue: #38bdf8;
  --blue-dark: #0284c7;
  --red: #ef4444;
  --red-dark: #b91c1c;
  --orange: #f97316;
  --gold: #eab308;
  --green-status: #58c978;
  --neutral: #71717a;
  --neutral-light: #a1a1aa;

  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;

  --report-width: 1180px;
  --prose-width: 78ch;
  --page-pad: clamp(18px, 3vw, 32px);
  --section-gap: 48px;
}
```

Use `Inter` only when locally bundled or installed. Never fetch a remote font merely to render the report.

## 15. Canonical page and figure CSS

Use this as the baseline. Framework-specific code may change class names, but not the behavior.

```css
* { box-sizing: border-box; }

html,
body {
  margin: 0;
  min-height: 100%;
  background: var(--canvas);
  color: var(--ink);
}

body {
  font-family: var(--font-sans);
  font-size: 15px;
  line-height: 1.62;
  text-rendering: optimizeLegibility;
}

.report {
  width: min(calc(100% - (2 * var(--page-pad))), var(--report-width));
  margin-inline: auto;
  padding-block: 28px 72px;
}

.prose,
.chart-read,
.chart-limit {
  max-width: var(--prose-width);
}

.report-section {
  padding-block: 36px;
  border-top: 1px solid var(--line);
}

.evidence-figure {
  width: 100%;
  min-width: 0;
  margin: 28px 0 0;
}

.chart-frame {
  width: 100%;
  min-width: 0;
  min-height: 460px;
  margin-top: 14px;
  background: var(--canvas);
}

.chart-frame.dense { min-height: 600px; }

.chart-frame svg,
.chart-frame canvas,
.chart-frame img {
  display: block;
  width: 100%;
  max-width: none;
  height: auto;
}

.exact-data {
  margin-top: 14px;
  border-top: 1px solid var(--line);
  padding-top: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-variant-numeric: tabular-nums lining-nums;
}

th,
td {
  padding: 9px 12px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

th {
  color: var(--ink-faint);
  font-size: 12px;
  font-weight: 650;
}

td.numeric,
th.numeric { text-align: right; }

@media (max-width: 760px) {
  :root { --page-pad: 16px; }
  .report { padding-block: 22px 48px; }
  .report-section { padding-block: 28px; }
  .chart-frame { min-height: 380px; }
}
```

Forbidden layout code:

```css
/* NEVER use these patterns for report evidence */
.charts { grid-template-columns: repeat(2, 1fr); }
.gallery { display: flex; flex-wrap: wrap; }
.chart { max-width: 640px; }
.report { width: 100vw; }
```

## 16. Typography

Use this hierarchy:

| Role | Size | Weight | Line height |
|---|---:|---:|---:|
| Report title | `clamp(28px, 4vw, 42px)` | `700` | `1.08` |
| Decision sentence | `18–20px` | `500` | `1.45` |
| Major section | `22–26px` | `650` | `1.2` |
| Minor section | `16–18px` | `650` | `1.3` |
| Chart title | `16–18px` | `600` | `1.3` |
| Chart subtitle/body | `13–15px` | `400` | `1.5–1.6` |
| Axis/legend | `11–13px` | `500` | `1.2` |
| Metadata/source | `11–12px` | `450` | `1.45` |

- Never shrink chart text below `11px`.
- Use monospace or tabular numerals for values, timestamps, prices, rates, counts, identifiers, and aligned numeric tables.
- Use sentence case.
- Avoid all-caps except a short status or eyebrow.
- Do not center ordinary paragraphs, chart titles, or tables.
- The report title is the only oversized text.

## 17. Color semantics

Use color consistently:

| Meaning | Color |
|---|---|
| Favorable or positive quantitative magnitude | Blue |
| Adverse, loss, or negative quantitative magnitude | Red |
| Marginal, fragile, warning, or near-threshold | Orange |
| Neutral, near-zero, benchmark, missing, unsupported | Distinct greys/patterns |
| Pass status badge only | Green |
| Selection, link, focus | Blue |

Do not use green as the default positive quantitative scale. Do not use red versus green as the primary chart encoding. Never rely on color alone; pair it with sign, label, position, marker, line style, or pattern.

Use one non-neutral root plus neutrals for a simple chart. Use at most two non-neutral roots for signed or focal comparisons. Use at most five roots only when category identity is the actual analytical question. Never use rainbow palettes or chart-library defaults.

## 18. Surfaces, cards, and decoration

- Use spacing and thin rules before adding a box.
- Do not wrap every section in a card.
- Do not make one KPI card per metric.
- A compact evidence scorecard table is preferred to metric tiles.
- A bounded surface is allowed for code, a warning, an exact-data disclosure, or a selected state.
- Use little or no shadow.
- Charts are flat and rectangular.
- Do not use gradients, glassmorphism, glows, 3D, textures, fake scanlines, fake command prompts, ornamental illustrations, or stock images.
- Do not import a white notebook theme into a black report.
- Do not leave white plot backgrounds, white raster margins, or default chart-library chrome inside the black page.

## 19. Spacing and density

Use a consistent `4, 8, 12, 16, 24, 32, 48, 64px` spacing scale.

- `4–8px`: label to value or related metadata.
- `12–16px`: chart title/subtitle to plot.
- `16–24px`: plot to interpretation.
- `24–32px`: related subsections.
- `40–56px`: major evidence sections.
- `64px`: rare chapter-scale separation.

Density means more useful evidence in a coherent view. It does not mean tiny type, cramped axes, stacked card grids, repeated labels, or a wall of prose.

---

# PART IV — WRITING RULES

## 20. Do not write a bullet-point report

The lists in this instruction file are rules, not a template for the report.

The report MUST use analytical paragraphs, evidence tables, and chart explanations as its primary language.

- Never use bullets for the executive conclusion.
- Never create a “Key takeaways” bullet dump.
- Use a list only for a genuinely parallel set or a procedural checklist.
- Limit an ordinary list to five items.
- Convert larger comparisons into a table, matrix, or chart.
- Do not repeat the same number in a title, KPI card, paragraph, chart annotation, and table.
- Do not use a bullet when a complete causal explanation is required.

## 21. Required analytical paragraph

Every important paragraph should contain:

```text
claim
→ exact evidence and magnitude
→ uncertainty and support
→ economic or decision meaning
→ limitation or alternative explanation
```

Bad:

> Performance was strong across most periods. Risk should be monitored.

Good:

> The frozen rule produced positive net expectancy in 4 of 6 unseen folds, but the aggregate was owned by one high-volatility month: removing that month reduced net expectancy from +3.8 bps to +0.6 bps per trade, with the dependence-aware interval crossing zero. The result remains `continue_research`, not a paper candidate, until an independent period shows positive net expectancy without that regime.

## 22. Prohibited language

Do not use these words without immediate quantitative support and scope:

- strong;
- robust;
- significant;
- profitable;
- optimal;
- proven;
- reliable;
- compelling;
- promising;
- clear edge.

Replace them with magnitude, interval, support, split, costs, stability, and achieved gate.

Do not say “the chart speaks for itself.” Explain it.

## 23. Titles and section headings

- Report titles identify the exact subject, evaluation, and decision context.
- Section headings state a question or evidence claim.
- Chart titles remain neutral and descriptive.
- Do not use headings such as `Overview`, `Results`, `Analysis`, or `Chart 3` when a specific heading is possible.
- Do not use a clever headline that overstates the result.

## 24. Negative results

Negative evidence is a required output. Preserve:

- failed hypotheses;
- failed folds;
- failed parameter regions;
- adverse regimes;
- negative controls;
- cost/delay failures;
- model reversals;
- missing evidence;
- non-fillable assumptions.

Do not hide failures in an appendix while successes appear in the main body. The report must make the weakest evidence discoverable as quickly as the strongest evidence.

---

# PART V — IMPLEMENTATION, ACCESSIBILITY, AND PORTABILITY

## 25. Portable HTML contract

When the deliverable is HTML, it MUST be self-contained and independently readable.

- Use inline CSS.
- Use inline SVG for charts when practical.
- Embed required local raster images or keep them beside the report with stable relative paths when embedding is impractical.
- Do not require remote fonts, remote scripts, CDNs, network calls, or a separate development server.
- Do not bolt on a second chart runtime when static SVG is enough.
- Do not ship raw notebook HTML as the final report.
- Code MAY be collapsible; conclusions, tables, and charts MUST be visible without executing code.
- The complete argument MUST remain understandable if JavaScript fails.
- Every report MUST open directly to its actual contents, not a gallery or wrapper page.

## 26. Exact-data disclosure

Every nontrivial chart SHOULD include a nearby disclosure:

```html
<details class="exact-data">
  <summary>Inspect exact chart data and assumptions</summary>
  <div class="table-scroll">
    <!-- exact table used to generate the chart -->
  </div>
</details>
```

The table MUST preserve identifiers, support, split, units, costs, and relevant context—not only generic `x`, `y`, and `series` columns.

## 27. Chart expansion

Dense charts and heatmaps SHOULD open into a near-full-screen black modal.

Requirements:

- Open by click or keyboard action.
- Use approximately `min(96vw, 1800px)` by `min(94vh, 1200px)`.
- Close by visible button and `Escape`; backdrop close MAY also be supported.
- Preserve the chart state and return focus to the original figure.
- Do not intercept clicks on links, disclosures, or source controls.
- Use a visible focus ring.
- The inline chart must remain complete enough to understand without expansion.

## 28. Accessibility

Every report MUST include:

- semantic headings in order;
- `<main>`, `<section>`, `<figure>`, `<figcaption>`, and semantic tables;
- descriptive chart title and text alternative;
- keyboard-accessible interaction;
- visible focus states;
- sufficient contrast;
- color-independent meaning;
- reduced-motion support;
- readable content without hover;
- minimum `40×40px` interactive targets on touch devices.

For SVG:

```html
<svg role="img" aria-labelledby="chart-title chart-desc" viewBox="0 0 1100 520">
  <title id="chart-title">Neutral chart title</title>
  <desc id="chart-desc">Concise summary of the chart's main relationship and scope.</desc>
  <!-- marks -->
</svg>
```

## 29. Responsive behavior

Test the actual report at approximately:

- `1440px` browser width;
- the real embedded viewer width, often `700–1000px`;
- `768px` tablet width;
- `390px` mobile width.

Rules:

- Keep one chart per row at every width.
- Collapse auxiliary layouts; do not shrink the whole page.
- Reduce tick count before rotating labels.
- Increase chart height when labels need space.
- Put wide tables and matrices in contained horizontal scrollers.
- Prevent page-level horizontal overflow.
- Keep axis text at least `11px` when possible and never below `10px`.
- Preserve the same data, conclusion, and caveats across responsive variants.

## 30. Print and PDF

The screen artifact is black. A print stylesheet MAY switch to a true light theme for legibility and ink use unless the user explicitly requests a black PDF.

Do not screenshot the dark report and paste it into a PDF. Render a real print variant with readable labels, preserved semantic colors or patterns, repeated table headers, and figures kept with their captions.

---

# PART VI — LLM WORKFLOW

## 31. Required workflow for the LLM

Follow these steps in order. Do not skip directly to HTML.

### Step 1 — Read before writing

Inspect repository instructions, the frozen experiment contract, source datasets, result tables, existing reports for the same experiment, and current decision records. Do not use an old report as empirical truth when the underlying data is available.

### Step 2 — Freeze the decision

Write one sentence naming the decision the report must support. Freeze the evidence label and the economic hurdle before visual design.

### Step 3 — Build the evidence inventory

Fill the contract in Section 3. Identify missing evidence immediately.

### Step 4 — Reconcile the numbers

Recompute or trace headline metrics from source artifacts. Verify denominators, signs, units, fees, timestamps, splits, and trade counts. Do not trust a prior summary without reconciliation.

### Step 5 — Create a chart plan

Before charting, make an internal table:

| Section | Decision question | Source data | Chart type | Required support/uncertainty | Failure exposed |
|---|---|---|---|---|---|

Every material claim must map to a chart. Every chart must map to a source and a decision.

### Step 6 — Build charts before narrative

Generate the full evidence stack. Use fixed scales across comparisons. Preserve failures. Attach exact data and provenance.

### Step 7 — Write explanations

Use the nine-part explanation contract in Section 8. Do not write generic chart descriptions.

### Step 8 — Assemble the report

Use the exact order in Section 4 and the one visual system in Part III. Do not introduce a second layout, palette, card style, or chart grammar.

### Step 9 — Inspect the rendered result

Open the actual report in a browser. Inspect wide, embedded, tablet, mobile, and print widths. Do not claim completion from source code alone.

### Step 10 — Reconcile again

Compare every headline, chart label, annotation, and exact-data table with the source artifacts. Confirm that visual transforms did not change the conclusion.

### Step 11 — Remove slop

Delete:

- generic bullets;
- repeated metrics;
- decorative cards;
- empty introductions;
- chart titles that merely name a chart type;
- prose that describes geometry without decision meaning;
- unsupported positive language;
- redundant charts;
- hidden or detached failure evidence.

### Step 12 — Apply the delivery gate

Do not deliver until all applicable checks in Section 33 pass. If a check cannot pass because evidence is missing, downgrade the decision and use the short failure-report format.

## 32. What the LLM must never do

- Never fabricate a chart, value, source, sample size, cost, or fill assumption.
- Never optimize the report around the prettiest result.
- Never select parameters, regimes, or cells from the test visualization.
- Never hide failed experiments or report only the winner.
- Never mix incompatible markets, horizons, populations, or evidence levels in one headline.
- Never use future data in features, normalization, thresholds, or selection.
- Never present gross PnL as decision-grade profit.
- Never assume midpoint, close, high, low, or zero-delay fills without an executable mechanism.
- Never show equity without drawdown, exposure, turnover, costs, and concentration.
- Never show a heatmap without support and a fixed comparison scale.
- Never use a raw white notebook export as the final black report.
- Never use side-by-side charts, chart thumbnails, or a detached gallery.
- Never use decorative imagery in place of evidence.
- Never let a chart library's default theme override this file.
- Never say the report is finished without inspecting the rendered artifact.

## 33. Final delivery checklist

The report is complete only if every applicable answer is **yes**.

### Decision and evidence

- [ ] The first viewport states one decision, achieved evidence level, cost basis, and primary reason.
- [ ] The research question, rule, population, period, and experiment ID are exact.
- [ ] Data quality and information/execution clocks are explicit.
- [ ] Train, validation, test, folds, purge, embargo, holdout, and selection timing are explicit where applicable.
- [ ] Gross and net economics reconcile exactly.
- [ ] Effective support, uncertainty, search size, and comparators are visible.
- [ ] Failed folds, nearby parameters, adverse regimes, higher costs, delays, and negative controls are visible.
- [ ] Drawdown, tails, exposure, turnover, capacity, and concentration are visible.
- [ ] The recommendation is no stronger than the achieved gate.
- [ ] The report ends with one bounded falsification test and frozen pass/fail criteria.

### Charts

- [ ] Every material quantitative conclusion has a chart.
- [ ] Every substantive section has a visual evidence object.
- [ ] Charts appear one per row and fill the centered report column.
- [ ] No chart grid, thumbnail gallery, contact sheet, or detached chart index exists.
- [ ] Every chart has the nine-part explanation contract.
- [ ] Every chart has units, denominator, population, period, split, costs, support, uncertainty, and provenance as applicable.
- [ ] Every chart has exact inspectable data or a local data artifact.
- [ ] Comparable charts use the same bins, scales, domains, colors, and category order.
- [ ] Missing and unsupported values are visibly distinct from zero.
- [ ] Failures are as easy to find as favorable results.

### Design

- [ ] The screen canvas and plot backgrounds are pure black.
- [ ] The report is centered at approximately `1120–1200px`, not stretched across the viewport.
- [ ] Prose remains near `78ch`; charts fill the report column.
- [ ] Body, axis, legend, and cell labels remain readable.
- [ ] Color follows the fixed blue/red/orange/grey semantics and never carries meaning alone.
- [ ] No generic KPI-card dashboard, gradient, glow, glass effect, 3D mark, stock image, or white notebook theme remains.
- [ ] Spacing and hierarchy explain grouping without boxing every section.

### Implementation and QA

- [ ] The report is self-contained and works without network access.
- [ ] It remains understandable without JavaScript or hover.
- [ ] Keyboard, focus, contrast, reduced-motion, and text alternatives work.
- [ ] Wide, embedded, tablet, mobile, expanded-chart, and print views were inspected.
- [ ] No page-level horizontal overflow, clipped label, unreadable legend, or broken source path remains.
- [ ] Every number and chart was reconciled against its source after rendering.

Any unchecked item is a blocker. Fix it or explicitly downgrade the report.

## 34. Minimal invocation for another LLM

Use this exact instruction when copying this file into another repository:

> Read `report-rules.md` completely before touching report code. Treat every MUST and MUST NOT as an acceptance requirement. Inspect the underlying data and existing experiment evidence first. Build the charts and exact evidence tables before writing prose. Use the single black, centered, one-chart-per-row design defined in the file. Explain every chart using the required question, neutral title, scope, how-to-read, what-it-shows, why-it-matters, what-it-does-not-prove, and provenance blocks. Render and visually inspect the final artifact at wide, embedded, mobile, expanded, and print sizes. Do not deliver until the final checklist passes or the report is explicitly downgraded for missing evidence.
