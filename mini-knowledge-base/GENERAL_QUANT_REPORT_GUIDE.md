# General Quantitative HTML Report Guide

> **Purpose:** a compact, portable instruction for designing clear, auditable
> quantitative research reports from OHLCV and optional derived or auxiliary
> data.
>
> **Scope:** general market research, correlations, conditional analysis,
> statistical models, backtests, risk studies, and negative results. It contains
> no venue-, strategy-, or DLMM-specific rules.
>
> **Use:** copy this file into a project and tell the report author or coding
> agent to follow it. It has no dependency on the repository it came from.

The report is a reading surface with visual evidence. Its job is to make the
question, evidence, uncertainty, limitations, and next decision easy to inspect
and difficult to misread. It is not a dashboard, marketing page, slide deck,
notebook dump, or chart gallery.

The words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are literal. When rules
conflict, follow: the current request and frozen experiment contract; data and
causal integrity; this guide; library defaults; author preference.

## 1. Governing principles

1. **Truth outranks appearance.** Visual polish cannot strengthen evidence.
2. **One report, one job.** State the research question and the decision or
   conclusion it supports.
3. **Show the evidence boundary.** Separate description, prediction, policy,
   execution, and realized outcome. Never imply that one proves the next.
4. **Start with the baseline.** Show the unconditional behavior before a
   conditional result, model, or strategy.
5. **Make failure visible.** Show negative results, weak periods, missing data,
   unstable parameters, contradictory folds, and unsupported regions as clearly
   as favorable evidence.
6. **Report support and uncertainty.** A mean, correlation, Sharpe ratio,
   accuracy, AUC, or p-value is never sufficient alone.
7. **Prefer simple explanations.** Complexity must improve unseen-time evidence
   over a simple baseline.
8. **Do not imply causality from OHLCV association.** A proposed mechanism is a
   hypothesis unless independently identified.
9. **Static first.** The complete argument must remain understandable without
   hover, interaction, JavaScript, or a network connection.
10. **Use the smallest report that supports the conclusion.** Missing evidence
    should shorten and downgrade a report, not produce filler.

### Research breadth and profit discipline

Do not begin with a favorite indicator, strategy, horizon, or model. Search
broadly and shallowly before refining anything. At minimum, consider several
logically distinct families that apply to the available data:

```text
unconditional structure and seasonality
continuation and reversal across coarse horizons
volatility, range, compression, and expansion
candle geometry, path efficiency, and range location
volume and activity states
breakouts, failed breakouts, and boundary behavior
cross-horizon agreement or conflict
regime dependence and long/short asymmetry
conditional tail risk, adverse excursion, and trade avoidance
cross-asset, relative-value, or lead-lag effects when synchronized data exists
```

Do not spend the search budget optimizing the first attractive family. Test
coarse time scales and simple conditional profiles first; examine interactions
only after understanding the components. Register the observable state, future
outcome, expected relationship, mechanism hypothesis, null, confounders,
falsification test, promotion rule, and variant budget before seeing the result.
Keep failed variants in the trial count.

Think beyond direct long/short prediction. Useful information may improve:

- entry or exit timing;
- trade filtering and adverse-selection avoidance;
- volatility or range forecasts for sizing;
- conditional risk forecasts for reducing exposure;
- regime routing, hedging, or choosing among existing strategies.

When profit is in scope, preserve the full chain:

```text
data -> observable state -> prediction -> frozen action rule -> executable fill
-> gross outcome -> costs and delay -> net outcome -> risk and concentration
```

Require a conservative economic margin:

\[
\text{expected gross edge} >
\text{fees} + \text{spread} + \text{slippage} + \text{funding/borrow}
+ \text{impact} + \text{delay loss} + \text{safety margin}
\]

Before calling apparent profit alpha, try to attribute it to drift, market beta,
volatility exposure, leverage, tail-risk selling, selection, or unrealistic
fills. Challenge every candidate with a simple baseline, negative controls,
unseen time, nearby parameters, regimes, sides, delay, higher costs, outlier
removal, and concentration tests. Rank the next experiment by expected
information gain and economic relevance—not by the most attractive possible
backtest.

Use evidence language such as `rejected`, `inconclusive`, `interesting but not
tradable`, `predictive but economically weak`, `conditionally useful`, or
`candidate executable alpha`. Never call a result proven.

## 2. Freeze the analytical contract

Before writing prose, CSS, or charts, record:

| Dimension | Required context |
|---|---|
| Identity | report, experiment, run, model, and configuration identifiers |
| Population | asset, venue if known, interval, UTC range, eligibility, timezone |
| Data | source paths, schema, row count, missingness, duplicates, gaps, outliers, repairs |
| Clock | bar timestamp semantics, feature cutoff, decision time, earliest fill, target start and end |
| Evaluation | train, validation, walk-forward folds, test, holdout, purge, embargo |
| Selection | hypothesis timing, variants tried, parameters searched, freeze point |
| Support | raw rows, effective observations, events/trades, unique periods/assets |
| Uncertainty | interval or test method and treatment of temporal dependence |
| Economics | price convention, fees, spread, slippage, funding/borrow, impact, delay, safety margin |
| Risk | drawdown, tails, exposure, leverage, turnover, concentration |
| Provenance | code/query path, source artifact, generated time, hashes when useful |

Do not invent a missing field. Label it unknown, explain why it matters, and
limit the conclusion accordingly.

For valid OHLCV bars, verify at minimum:

```text
open > 0; high > 0; low > 0; close > 0; volume >= 0
high >= max(open, close); low <= min(open, close); high >= low
timestamps strictly increase after the declared duplicate policy
```

Never forward-fill OHLCV and pretend a trade occurred. Do not silently remove
bad bars. Report counts before and after every repair or exclusion.

### Information-time default

For candle-only research, a conservative convention is:

```text
bar t closes -> features use bars <= t -> decision occurs after close
-> earliest proxy fill is open[t+1] -> future target starts at that fill
```

If another convention is used, explain why the information and price were
available. Fit normalization, bins, feature selection, thresholds, regimes,
models, and calibration on training data only.

## 3. Quantitative notation and math

Define every symbol, index, horizon, unit, and price convention on first use.
Keep formulas close to the claim they support. Prefer normalized, interpretable
features over unexplained indicator names.

For a completed OHLCV bar with open \(O_t\), high \(H_t\), low \(L_t\), close
\(C_t\), volume \(V_t\), lookback \(k\), and small \(\epsilon>0\):

\[
r_t = \log(C_t/C_{t-1}), \qquad
r_{t,k} = \log(C_t/C_{t-k})
\]

\[
\operatorname{range}_t = \frac{H_t-L_t}{C_{t-1}}, \qquad
\operatorname{body}_t = \frac{C_t-O_t}{H_t-L_t+\epsilon}
\]

\[
\operatorname{closePos}_t = \frac{C_t-L_t}{H_t-L_t+\epsilon}, \qquad
\operatorname{relVol}_t =
\frac{V_t}{\operatorname{median}(V_{t-k:t-1})+\epsilon}
\]

For an executable entry proxy \(P_0\) and declared exit price \(P_h\):

\[
R_{t,h}=\frac{P_h}{P_0}-1, \qquad
D_{t,h}=\mathbb{1}(R_{t,h}>0)
\]

The future window MUST begin after the declared decision and entry instant.
For overlapping horizon labels, report raw rows and an effective or
non-overlapping count; use purged chronological splits and dependence-aware
uncertainty.

Math presentation rules:

- Put the economic or analytical meaning before or immediately after a formula.
- State whether returns are simple or log, decimal or percent, gross or net.
- Distinguish percent from percentage points and convert basis points explicitly:
  \(1\text{ bp}=0.01\%=10^{-4}\).
- Use consistent symbols across prose, charts, code, and tables.
- Show assumptions and edge cases, including zero ranges, missing bars, and
  ambiguous intrabar barrier order.
- Do not display decorative algebra that is unused by the analysis.
- In HTML, prefer semantic MathML or locally pre-rendered math. Do not require a
  remote math script; provide a readable text definition or accessible label.

## 4. Correlation and conditional analysis

Correlation is a descriptive statistic, not a trading result or causal claim.

- Correlate stationary or economically meaningful transformations, usually
  returns or changes—not raw price levels with shared trends.
- Name the estimator: Pearson for linear association, Spearman for rank
  association, or another explicitly justified measure.
- Show the observation grain, lag direction, sample, missing-data policy, and
  chronological split.
- Use lagged analysis for prediction: information at or before \(t\) versus an
  outcome after \(t\). Same-time correlation is not lead-lag evidence.
- For cross-asset or cross-venue work, align bar clocks and timestamp semantics,
  disclose asynchronous or missing observations, and separate common-market
  exposure from an alleged leader-follower effect.
- For many features, disclose the number of comparisons and control false
  discovery or clearly label the matrix exploratory.
- Show temporal stability with rolling or fold-wise estimates. A full-sample
  coefficient can hide sign reversals.
- Pair a correlation matrix with support and, when material, uncertainty or
  significance adjusted for dependence and multiple testing.
- Use partial correlation or regression only with a stated conditioning set;
  do not describe statistical control as causal identification.
- Inspect scatter/hexbin or binned conditional profiles. A coefficient can hide
  nonlinearity, tails, regimes, and outliers.

For a conditional research claim, frame the question as:

\[
P(Y_{t,h}\mid X_t) \stackrel{?}{\ne} P(Y_{t,h})
\]

Then report more than the mean: count, effective count, median, quantiles, hit
rate or base-rate lift, tail behavior, interval, time/fold stability, and the
relevant economic hurdle. Use training-defined bins and preserve the same bin
edges across validation and test.

## 5. Report architecture

Use this order unless the report's single job requires a documented change:

1. **Header:** exact subject, research question, scope, evidence status or one
   decision, strongest reason, and primary limitation.
2. **Data and timing:** coverage, quality, transformations, information
   boundary, target, and chronological split.
3. **Unconditional structure:** price/data quality, target distribution, drift,
   dependence, seasonality, and simplest baselines as applicable.
4. **Conditional evidence:** feature distributions, correlations, conditional
   profiles, interactions, models, and uncertainty.
5. **Unseen-time stability:** validation/test/fold results, parameter
   neighborhoods, regime/side/time slices, and negative controls.
6. **Economics and risk, when a policy is tested:** gross-to-net bridge,
   turnover, exposure, drawdown, tails, concentration, cost/delay sensitivity,
   and execution limits.
7. **Conclusion:** supported finding, strongest counterevidence, achieved
   evidence level, and one bounded next falsification test.
8. **Method and provenance:** exact sources, formulas, code/configuration,
   exclusions, variants, generated artifacts, and reproduction steps.

The first viewport should answer: What was tested? On what data? What is the
current conclusion? Why? What is the strongest limitation?

If the evidence is insufficient, use a short failure report: conclusion or
downgraded decision; blocking-evidence table; what can still be concluded; one
next test with frozen pass/fail criteria.

## 6. Figure contract

Every important figure MUST contain these elements in this order:

1. **Question:** the uncertainty or decision the figure addresses.
2. **Neutral title:** what is plotted, without announcing success.
3. **Scope subtitle:** population, UTC range, split/fold, denominator and
   support, unit, transformation, and cost/fill status when relevant.
4. **How to read:** axes, marks, colors, bands, baseline, support, and missing
   values.
5. **Full-width figure:** the actual evidence with readable labels.
6. **What it shows and why it matters:** magnitude, uncertainty, heterogeneity,
   baseline comparison, and decision consequence.
7. **What it does not prove:** strongest limitation or alternative explanation.
8. **Evidence footer:** source path, generation path, variant/configuration,
   frozen assumptions, and generated time.

Pair every nontrivial chart with a nearby exact table, structured text summary,
or stable local data artifact. The chart communicates shape; the table or data
communicates exactness. Essential facts MUST NOT exist only in a tooltip.

## 7. Plot selection and integrity

Choose a plot because it matches the question, not for visual variety.

| Question | Default evidence |
|---|---|
| Change through time | line or step chart; mark gaps and split boundaries |
| OHLC path or events | price/candle panel plus quality/events; examples are not proof |
| Distribution and tails | histogram plus ECDF or quantiles; show median and thresholds |
| Category ranking | sorted horizontal bars starting at zero |
| Estimated effects | dot-and-whisker plot with defined intervals |
| Continuous association | scatter/hexbin plus binned profile and uncertainty |
| Correlation structure | return/change correlation matrix plus support and stability |
| Conditional relationship | training-defined binned profile with interval and support |
| Two-state interaction | outcome heatmap plus matched support heatmap |
| Parameter stability | complete local surface with frozen point marked |
| Time generalization | fold matrix plus fold distribution and counts |
| Prediction quality | calibration and prediction-decile plots plus simple baseline |
| Net path and pain | net equity, underwater drawdown, and exposure/turnover panels |
| Cost tolerance | cost × delay surface with zero-profit contour |
| Concentration | contribution bars/Lorenz curve plus leave-one-bucket-out result |
| Exact lookup | semantic table |
| Clock, process, or causality boundary | simple timeline or directed diagram |

General plot rules:

- Show units and four to six useful ticks. Use consistent precision and tabular
  numerals.
- Show a meaningful zero, unconditional baseline, target, or economic hurdle.
- Start quantitative bar axes at zero. Label any nonzero line-chart domain.
- Use the same bins, axes, domains, category order, and color meaning for direct
  comparisons.
- Do not smooth away extrema, gaps, failures, drawdowns, or regime changes.
- Use opacity, hexbinning, or density contours for overlapping scatter points.
- Show uncertainty for estimates and define the interval method.
- Show support in or directly beside conditional profiles, heatmaps, model
  bins, and subgroup comparisons.
- Mask unsupported, invalid, and missing cells. Distinguish them from real zero
  and from `n=0`.
- Treat an isolated hot heatmap cell or narrow parameter optimum as likely
  overfit until it survives neighboring parameters and unseen time.
- Never select a parameter, cell, regime, or story from the test visualization.
- Never show equity without drawdown, exposure/turnover, costs, and
  concentration. Never cumulate overlapping labels as independent trades.
- Avoid dual axes. Prefer vertically aligned panels with shared time or scale.
- Prefer direct labels; use a small unboxed legend only when necessary.
- Annotate only a decision-relevant threshold, break, failure, outlier, selected
  point, or structural event.

Avoid pie/donut, gauge, radar, 3D, word-cloud, decorative Sankey, hand-picked
winner arrows, feature-importance-as-proof, and label-colored t-SNE/UMAP as
primary evidence.

## 8. Visual system for HTML reports

### Layout

- Use one centered, single-column report flow.
- Report width: approximately `1120–1200px`; prose width: `70–80ch`.
- Every chart, heatmap, diagram, image, and major table gets its own row and
  fills the report column.
- Vertically aligned panels MAY share one figure when they share an axis or
  scale and jointly answer one question.
- Never use dashboard tiles, chart grids, thumbnail galleries, detached chart
  indexes, or side-by-side chart-and-prose layouts.
- Use spacing and thin rules before adding boxes. Do not wrap every section or
  metric in a card.
- Simple charts usually need `420–520px` height; dense charts `560–700px`.
  Increase height before shrinking labels.

### Canonical tokens

```css
:root {
  color-scheme: dark;
  --canvas: #000000;
  --surface: #080808;
  --surface-2: #101010;
  --ink: #f2f2f2;
  --ink-muted: #c4c4c4;
  --ink-faint: #929292;
  --line: rgba(255, 255, 255, 0.10);
  --gridline: rgba(255, 255, 255, 0.09);
  --positive: #38bdf8;
  --negative: #ef4444;
  --warning: #f97316;
  --pass-status: #58c978;
  --neutral: #71717a;
  --report-width: 1180px;
  --prose-width: 78ch;
  --page-pad: clamp(18px, 3vw, 32px);
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
}
```

Use `Inter` only if locally bundled or installed; never fetch a remote font just
for the report.

### Color

- Blue: favorable or positive quantitative magnitude.
- Red: adverse or negative magnitude.
- Orange: warning, fragility, or near-threshold values.
- Grey or labeled pattern: neutral, missing, unsupported, or unavailable.
- Green: compact pass-status marks only, not the positive data scale.
- Never rely on color alone; pair it with sign, label, position, shape, line
  style, outline, or pattern.
- Use one non-neutral root plus greys for ordinary charts, two for signed/focal
  comparisons, and at most five only when category identity is the question.
- Never use rainbow palettes or automatic chart-library colors.

### Typography and surfaces

- Report title: `28–42px`; section heading: `22–26px`; body: `15–16px` at
  `1.55–1.65`; chart title: `16–18px`; axes/legends: `11–13px`; metadata:
  `11–12px`.
- The report title is the only oversized text. Use sentence case and
  left-aligned prose.
- Use tabular numerals or monospace for values, timestamps, identifiers, paths,
  prices, rates, and aligned numeric tables.
- Use flat black plots, quiet gridlines and borders, square or nearly square
  chart corners, and little or no shadow.
- Do not use decorative gradients, glows, glass effects, textures, fake
  terminals, stock imagery, ornamental illustrations, or white notebook plots.

## 9. Writing and explanation

Write in short analytical paragraphs. Use tables for comparisons and lists only
for genuinely parallel items or procedures. Do not open with a bullet dump or a
wall of KPI cards.

An important paragraph should contain:

```text
claim -> magnitude -> uncertainty and support -> decision meaning
-> limitation or alternative explanation
```

Replace words such as *strong*, *robust*, *significant*, *profitable*,
*optimal*, *promising*, and *clear edge* with exact magnitude, interval,
support, split, costs, and stability. Do not say a chart speaks for itself.

- Use specific titles and question/finding section headings, not `Overview`,
  `Results`, `Analysis`, or `Chart 3`.
- Keep chart titles neutral. Put interpretation in the reading paragraph.
- Distinguish observation from interpretation and mechanism from evidence.
- State denominators. A percentage without its count can mislead.
- Report mean and median when tails matter; report long and short or relevant
  subgroups separately when asymmetry matters.
- Preserve failed hypotheses, folds, regimes, controls, parameter regions, and
  missing evidence in the main argument rather than hiding them in an appendix.
- Do not repeat the same number in a title, card, paragraph, annotation, and
  table.

## 10. Tables, interaction, and implementation

Tables MUST use semantic headers, units in headers or captions, right-aligned
numeric columns, tabular numerals, consistent precision, quiet row rules, and a
declared sort order. Long tables should disclose shown versus total rows and use
a contained, keyboard-accessible scroller.

For portable HTML:

- Use semantic HTML: one `<main>`, one `<h1>`, nested headings, `<section>`,
  `<figure>`, `<figcaption>`, semantic `<table>`, and native controls.
- Prefer inline CSS and build-time inline SVG for static charts. An existing
  chart library MAY be used, but its defaults must not override this guide.
- Avoid remote scripts, fonts, CDNs, iframes, and network calls.
- Keep conclusions, units, caveats, sources, and essential labels visible when
  JavaScript fails.
- Tooltips may add exact values but must work by keyboard and cannot contain the
  only important information.
- Dense charts SHOULD expand into a near-full-screen view with a visible close
  button, `Escape` support, focus management, and the same data and caveats.
- Do not animate charts on load. Respect reduced-motion preferences.
- Escape inserted text, serialize embedded data safely, and never embed secrets.

## 11. Responsive, accessible, and print behavior

Test the actual artifact near `1440px`, the real embedded width, `768px`, and
`390px`, plus browser zoom and print/PDF.

- Keep one figure per row at every width; collapse auxiliary layouts instead of
  shrinking the whole page.
- Reduce tick count before rotating labels. Increase height before reducing
  type. Keep axis text at least `11px` when practical and never below `10px`.
- Contain wide tables and matrices; never create page-level horizontal overflow.
- Preserve the same data, conclusion, and caveats across responsive variants.
- Provide visible focus, keyboard operation, meaningful document order, chart
  names/descriptions, exact data or structured summaries, and color-independent
  meaning.
- Target at least `4.5:1` contrast for normal text and `3:1` for large text and
  essential marks.
- Use a true light print stylesheet with repeated table headers and figures kept
  with captions. Do not paste screenshots of the dark page into a PDF.

## 12. Build and review workflow

1. Read the experiment contract and underlying data, not only a prior summary.
2. Freeze the report's question, evidence status, and decision threshold.
3. Complete the analytical contract in Section 2 and mark missing evidence.
4. Recompute or trace headline metrics; verify signs, units, timestamps,
   denominators, splits, costs, and counts.
5. Make a figure plan mapping each claim to its question, source, plot,
   uncertainty/support, and failure mode.
6. Build evidence tables and figures before narrative prose.
7. Assemble the report in the order in Section 5.
8. Inspect the rendered HTML at wide, embedded, mobile, expanded, and print
   sizes. Source review alone is insufficient.
9. Reconcile every headline, label, annotation, table, and plotted value against
   its source after rendering.
10. Remove repeated metrics, generic bullets, decorative cards, redundant
    charts, unsupported praise, and hidden failure evidence.

## 13. Delivery checklist

- [ ] The first viewport states the question, scope, conclusion/status, strongest
      reason, and strongest limitation.
- [ ] Data quality, bar semantics, information boundary, target, and
      chronological evaluation are explicit.
- [ ] Every claim is no stronger than its evidence and every value traces to a
      source.
- [ ] Baselines, uncertainty, raw and effective support, search size, and
      negative evidence are visible where applicable.
- [ ] Correlations use appropriate transformations, lags, support, and cautious
      language.
- [ ] Broad, logically distinct hypothesis families were considered before
      fine tuning, and the search size includes rejected variants.
- [ ] Gross and net economics reconcile when a trading policy is evaluated.
- [ ] Apparent profit was challenged as drift, beta, volatility, leverage, tail
      risk, selection, or unrealistic execution before being called alpha.
- [ ] Risk, drawdown, tails, exposure, turnover, and concentration are shown
      when applicable.
- [ ] Every important figure follows the figure contract, fills its row, and has
      exact inspectable evidence.
- [ ] Comparable plots share bins, scales, domains, ordering, and semantics;
      missing and unsupported values differ from zero.
- [ ] No chart grid, KPI-card dashboard, white notebook plot, decorative graphic,
      or default library styling remains.
- [ ] The report works without network access, hover, or JavaScript and remains
      keyboard accessible.
- [ ] Wide, embedded, tablet, mobile, expanded, zoomed, and print views were
      inspected.
- [ ] The conclusion includes the main limitation and one bounded next
      falsification test when further research is warranted.

Any unchecked applicable item is a blocker. Fix it or explicitly downgrade the
report.

## Minimal invocation

> Follow `GENERAL_QUANT_REPORT_GUIDE.md` completely. Treat every MUST and MUST
> NOT as an acceptance rule. Start from the experiment contract and source data;
> use a black, centered, single-column HTML report with one full-width figure per
> row; explain every figure with its question, neutral title, scope, reading,
> evidence, limitation, and provenance; show baselines, uncertainty, support,
> time splits, negative results, and costs when applicable; search across
> distinct information families before tuning and consider filters, sizing,
> risk, and execution—not only direction; render and inspect the final artifact
> at wide, embedded, mobile, expanded, and print sizes before delivery.
