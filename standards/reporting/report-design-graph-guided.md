# Graph-Guided Research Report Design

> **Version:** explanatory, evidence-first reporting profile  
> **Use when:** readers need help understanding graphs, statistical evidence,
> or trading relevance  
> **Relationship:** this profile keeps the current quantitative visual language
> but adds a structured explanation around every important graph.

## 1. Design idea

Treat every graph as a small guided argument. The reader should never have to
guess what the axes mean, which comparison matters, whether the effect is large,
or what the graph fails to establish.

This version is more explanatory than the current unified style, but it must
not become louder or more decorative. It uses the same disciplined dark
research aesthetic, full-width evidence, restrained color, visible support,
and static-first interaction.

## 2. Best uses

Choose the graph-guided profile for:

- alpha-research reports shared beyond the immediate researcher;
- reviews containing unfamiliar chart types;
- parameter and regime heatmaps;
- walk-forward validation reports;
- model calibration and prediction-decile reports;
- cost, delay, turnover, MFE, MAE, and drawdown analysis;
- reports where a statistically significant result may still be economically
  weak or non-executable.

## 3. Page structure

Use this sequence:

1. Research question and frozen scope.
2. Decision and confidence level.
3. A short “What was tested” explanation.
4. Baseline and unconditional structure.
5. Guided evidence figures in argumentative order.
6. Robustness, costs, and failure evidence.
7. Rejected explanations and limitations.
8. Final classification and next falsification test.
9. Method, experiment ledger, and sources.

Do not begin with performance metrics before explaining the target, baseline,
and information boundary.

## 4. Required graph block

Every major graph must use the following structure.

### Question

Phrase the exact question the graph answers.

> Does future one-minute return change as current relative volume increases?

### Neutral chart title

State what is plotted without announcing the conclusion.

> Mean next-minute return by training-defined relative-volume decile

### Scope subtitle

Include asset, venue, interval, period, split, unit, sample size, and important
method detail.

> BTC-USDT · Binance spot · 1-minute bars · locked test · Jan–Mar 2026 · bps ·
> 126,412 observations · HAC 95% confidence intervals

### How to read this graph

Explain, in plain language:

- what the horizontal axis represents;
- what the vertical axis represents;
- what each mark, line, color, or cell represents;
- which baseline or threshold matters;
- whether higher, lower, flatter, or more monotonic is meaningful.

Keep this to two to five sentences. It should teach the chart, not repeat the
method section.

### Graph

Give the graph the full available evidence width. Preserve readable axes,
units, support, uncertainty, and direct labels.

### What it shows

State the numerical observation before interpreting it.

> Deciles 1–9 remain between -0.08 and 0.06 bps. Decile 10 reaches 0.21 bps,
> with a 95% interval of -0.04 to 0.46 bps.

### Why it matters

Connect the observation to the hypothesis, decision, or economic hurdle.

> The extreme-volume bucket may change the outcome distribution, but its point
> estimate is smaller than the assumed 1.2 bps round-trip cost.

### What it does not prove

Name the strongest limitation or alternative explanation.

> This does not establish directional alpha. The bucket may only identify
> higher future volatility, and the interval still includes zero.

### Evidence footer

Show support, uncertainty method, data source, transformation version, figure
generation ID, and any exclusions close to the graph.

## 5. Visual hierarchy

- Main container: full available report width, with prose capped near `760px`.
- Charts and major tables: one per row and uncapped within the report frame.
- Graph block spacing: `72–104px` between major figures.
- Explanatory copy: visibly grouped with its graph, never detached into a
  distant methods section.
- Chart height: begin at `460–640px`; use more height for dense labels or
  heatmaps.

Use a quiet border or background shift to bind one graph block together. Do
not turn each block into a floating dashboard card.

## 6. Color tokens

```css
:root {
  --page: #090b0d;
  --surface: #11151a;
  --surface-soft: #171c22;
  --text: #eef2f5;
  --muted: #a3adb7;
  --faint: #69747f;
  --rule: #2b333c;
  --focus: #65a7ff;
  --positive: #66a9ff;
  --negative: #ef767a;
  --warning: #e4a85b;
  --support: #98a5b3;
  --interval: rgba(101, 167, 255, 0.20);
}
```

Blue represents favorable or positive quantitative magnitude, red represents
adverse or negative magnitude, orange represents fragility or warning, and
grey represents neutral or unavailable values. Green may be used for a small
pass-status mark, not as the default positive data scale.

## 7. Graph grammar

Every graph must make these elements explicit where applicable:

- population and denominator;
- unit and transformation;
- chronological split;
- zero, unconditional, random, or cost baseline;
- sample support;
- uncertainty;
- missing or excluded values;
- selected versus merely displayed parameters;
- gross versus net outcomes;
- long versus short direction.

Use visual emphasis in this order:

1. the actual evidence;
2. the comparison or baseline;
3. uncertainty and support;
4. annotation;
5. grid and frame.

The frame must never be more visually prominent than the data.

## 8. Explanations by graph type

### Line or event-path chart

Explain the starting point, time direction, unit, and whether paths overlap.
Show a zero or unconditional path and a dependence-aware interval. State
whether the endpoint or the path shape is the actual test.

### Histogram or distribution

Explain bin width, normalization, tails, and the difference between frequency
and probability. Show median and relevant tail thresholds. Do not summarize a
heavy-tailed distribution with only its mean.

### Bar or conditional-profile chart

Explain how categories or bins were defined and whether boundaries came only
from training data. Show support and intervals. Make the unconditional mean and
economic hurdle visible.

### Scatterplot

Explain what one point represents. Show density or transparency when points
overlap. Report whether any fitted line is descriptive, trained, or evaluated
out of sample. Do not let a few extreme points determine the apparent slope.

### Heatmap

Explain both axes, cell statistic, color midpoint, clipping, and blank-cell
meaning. Pair the outcome heatmap with a support heatmap. Mark the selected
region without hiding nearby parameters, and distinguish a broad cluster from
an isolated hot pixel.

### Parameter surface

Explain which parameters were selected before the test and which are shown only
for sensitivity. The visual question is whether a plateau exists, not where the
single maximum sits. Mark the selected point and the viable neighborhood.

### Calibration or prediction-decile chart

Explain the ideal diagonal or monotonic relationship, class balance, coverage,
and threshold selection. Report probability calibration separately from
trading profitability.

### Equity and drawdown

State starting capital, compounding convention, exposure, leverage, fees,
funding, concurrency, and whether the curve is gross or net. Always pair equity
with underwater drawdown and show inactive periods honestly.

### Cost × delay chart

Explain the assumed base execution point and what each delay means in real
time. Mark the plausible operating region. A candidate that survives only at
zero delay and zero cost should be labeled fragile.

### MFE and MAE chart

Define the observation window, entry price, direction convention, and intrabar
ambiguity. Explain that favorable excursion does not imply an executable exit
at the observed extreme.

## 9. Annotation rules

Annotations should answer one of four questions:

- What changed?
- Where is the relevant threshold?
- Which region was selected before evaluation?
- What data or market event may explain an anomaly?

Use direct, factual language. Prefer:

> Net expectancy crosses below zero at 0.8 bps cost.

Avoid:

> The strategy falls apart here!

Do not annotate every point. Use one to three annotations per graph unless the
figure is explicitly an event chronology.

## 10. Plain-language statistical terms

Define unfamiliar terms next to their first important use:

- **Confidence interval:** a range showing estimation uncertainty under the
  stated method; it is not the range of future outcomes.
- **Support:** the number of observations behind a mark or cell.
- **Baseline:** the result a feature or model must improve upon.
- **Holdout:** data kept untouched until the procedure is frozen.
- **Drawdown:** the decline from a prior portfolio peak.
- **Turnover:** how much position changes and therefore creates trading cost.
- **Calibration:** whether predicted probabilities match observed frequencies.

Use the repository glossary for the full definition. Do not make a tooltip the
only place a term is explained.

## 11. Tables beside graph explanations

Add a small exact-value table when the graph requires precise comparison. The
table should contain only the values needed to verify the visual claim:

| State | Support | Effect | 95% interval | Net of cost | Decision |
|---|---:|---:|---:|---:|---|
| Low | 12,640 | -0.03 bps | [-0.18, 0.12] | -1.23 bps | Reject |
| High | 12,641 | 0.21 bps | [-0.04, 0.46] | -0.99 bps | Inconclusive |

The table supplements the graph; it must not introduce a different population,
unit, or filter without saying so.

## 12. Interaction

The report must remain complete without interaction. Useful enhancements are:

- keyboard-accessible exact-value tooltips;
- click-to-expand for dense figures;
- a “show data” table;
- a “show method” disclosure;
- synchronized highlight between a plotted region and its table row.

Do not hide the conclusion, caveat, unit, source, or support behind hover.

## 13. Accessibility

- Never rely on color alone.
- Use patterns, direct labels, signs, or shapes for important distinctions.
- Maintain readable contrast for text and axes.
- Give every graph a concise text alternative.
- Make explanation and data tables available in reading order.
- Preserve visible keyboard focus.
- Respect reduced-motion preferences.
- Use semantic headings and table markup.

## 14. Guided graph acceptance checklist

For every important graph, confirm:

- Can a non-specialist identify both axes and their units?
- Is it clear what one mark or cell represents?
- Is the relevant baseline visible and explained?
- Are support and uncertainty shown?
- Does the text distinguish observation from interpretation?
- Is economic magnitude separated from statistical evidence?
- Is the strongest limitation stated beside the graph?
- Can the claim be checked against exact values?
- Does the graph reveal failure and instability, not only the best result?
- Would the reader reach the same conclusion without a tooltip?

The guided version succeeds when it improves understanding without changing the
strength of the underlying claim.
