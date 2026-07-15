# Profit-report visual contract

## Contents

1. Visual objective
2. Required figure anatomy
3. High-density chart stack
4. Chart selection
5. Layout and styling
6. Prohibited graphics
7. Render and data QA

## 1. Visual objective

Use graphics to compress decision-relevant evidence while exposing failure. Every graphic must be generated from real source data and answer a falsifiable question. Do not create imagery merely because the report needs to “look designed.”

Default to the quantitative evidence profile in `../../report-design.md` and the explanatory anatomy in `../../report-design-graph-guided.md`. Use the DLMM companion only when its domain applies.

## 2. Required figure anatomy

Every evidence figure must include, in this order:

1. **Question or decision:** the uncertainty the figure resolves.
2. **Neutral title:** what is plotted, without claiming the conclusion.
3. **Scope subtitle:** population, UTC range, split/fold, unit, denominator, cost status, and method.
4. **How to read:** axes, color, baseline, bands, marks, and support encoding.
5. **Full-width graphic:** actual evidence.
6. **What it shows:** magnitude, uncertainty, effective support, and important heterogeneity.
7. **Why it matters:** exact promotion, rejection, sizing, or next-test consequence.
8. **What it does not prove:** strongest limitation or alternate explanation.
9. **Evidence footer:** source path, generation path, variant ID, and frozen assumptions.

Keep these blocks compact. Omit only a redundant block, never its underlying information.

## 3. High-density chart stack

A serious candidate normally requires the following evidence. Omit a figure only when its question is inapplicable or the report downgrades itself for missing evidence.

| Order | Figure | Decision tested | Required overlays or companion data |
|---:|---|---|---|
| 1 | Data coverage and quality timeline | Is the sample trustworthy? | gaps, repairs, structural breaks, split boundaries |
| 2 | Target and unconditional distribution | What must the candidate beat? | tails, base rate, costs or hurdle |
| 3 | Feature distribution by time and split | Is the input stable and causal? | drift, missingness, train-fitted boundaries |
| 4 | Conditional profile | Does outcome move with state? | uncertainty, baseline, effective support |
| 5 | Train/validation/test outcome and support matrices | Does the same region survive unseen time? | identical bins and fixed scale |
| 6 | Event path | Is the move fillable after the signal? | matched control, delay, mean/median, MFE/MAE, interval |
| 7 | Parameter-neighborhood surface | Is the selected point a plateau? | chosen point, support contours, boundary stress |
| 8 | Fold matrix | Is aggregate performance broadly owned? | counts, sides/regimes, worst fold, fixed baseline |
| 9 | Calibration or prediction-decile chart | Does model score order unseen outcomes? | support, actual versus predicted, net policy payoff |
| 10 | Net equity and underwater drawdown | What path risk produces net PnL? | costs, exposure, turnover, fold boundaries |
| 11 | Cost × delay surface | Is the edge economically tolerant? | zero-profit contour and conservative base case |
| 12 | Concentration and leave-one-out view | Who owns the profit? | top-N, periods, sides, assets, regimes |

Do not show twelve weak charts merely to satisfy a count. Combine aligned panels vertically inside one full-width figure when they share an axis and jointly answer one question. Never place unrelated plots side by side.

## 4. Chart selection

Choose graphics by the decision, not by variety.

| Question | Required default | Never substitute |
|---|---|---|
| Net path and pain | aligned net-equity, drawdown, exposure panels | equity alone |
| Distribution and tails | histogram/ECDF plus quantiles and breakeven | average-only KPI |
| Conditional relationship | binned profile with interval and support | scatter cloud with trend line only |
| Two-state interaction | outcome heatmap plus support heatmap | autoscaled winner heatmap |
| Time generalization | fold matrix and fold distribution | aggregate Sharpe card |
| Parameter stability | full neighborhood surface with selected point | best-parameter table |
| Cost tolerance | cost × delay heatmap with zero contour | one cost assumption |
| Prediction quality | calibration/deciles and simple baseline | feature importance |
| Concentration | contribution curve and leave-one-bucket-out | top-trade list only |
| Execution quality | slippage/fill distribution by size and latency | midpoint-fill backtest |

Use tables when exact lookup matters more than shape. Use a diagram only for information flow, execution timing, or experiment architecture. Do not use decorative illustrations in a quantitative evidence report.

## 5. Layout and styling

- Render one evidence figure per row at full available width.
- Use a pure-black canvas, near-white text, quiet borders, and flat surfaces.
- Use blue for favorable magnitude, red for adverse magnitude, orange for fragile or threshold regions, and grey for neutral or unsupported states. Reserve green for a compact pass/status mark.
- Keep a fixed semantic mapping across the entire report.
- Use at least `420px` for a simple primary chart and `560px` for dense multi-series evidence. Derive heatmap height from readable rows.
- Use responsive SVG or a high-resolution canvas/raster with an exact-data table.
- Keep prose constrained; do not constrain plots to prose width.
- Use direct labels, four to six useful ticks, visible zero or hurdle lines, and explicit units.
- Show uncertainty and support in the plot, not only in a footnote.
- Mask unreliable cells distinctly; never map missing or underpowered data to zero.
- Make dense visuals expandable when feasible, but keep the inline report understandable without expansion.
- Use a light print theme with preserved data distinctions.

High density permits aligned layers and panels, not illegible type. Never shrink labels below `11px` to force content into a fixed height.

## 6. Prohibited graphics

Reject the report if it includes any of the following without a documented analytical necessity:

- generic KPI-card dashboards;
- thumbnail chart grids or detached galleries;
- pie, donut, gauge, radar, 3D, decorative Sankey, or word-cloud charts;
- stock images, ornamental illustrations, gradients, glows, glass panels, or fake-terminal effects;
- a price chart with hand-picked winner arrows as evidence;
- price-level correlation matrices presented as predictive evidence;
- feature importance without unseen-time ablation;
- t-SNE or UMAP clusters colored by future labels without original-space confirmation;
- heatmaps without support, fixed cross-split scales, and counts;
- overlapping-label cumulative return presented as executable independent trades;
- candlestick examples showing winners without matched losers and random controls;
- charts generated from invented, placeholder, or silently transformed data;
- bullets or prose where a comparison table or quantitative graphic is required.

## 7. Render and data QA

Before delivery:

1. Recompute or trace every plotted value to a source table.
2. Reconcile chart aggregates with headline and table values.
3. Inspect the rendered report at approximately `1440px`, `768px`, and `390px`, plus the actual embedded viewer width.
4. Inspect print/PDF output using the light theme.
5. Test keyboard focus, tooltip equivalence, chart expansion, disclosures, and reduced motion.
6. Confirm that legends, units, denominators, counts, intervals, caveats, and sources remain readable without hover.
7. Confirm that no crop, scale, color domain, smoothing, or axis choice changes the analytical conclusion.
8. Confirm that the weakest fold, worst loss, unsupported cells, and failed stresses are visually discoverable as quickly as the best result.

If visual inspection reveals crowding, remove redundant labels or split one analytical question across consecutive full-width figures. Do not shrink the evidence into dashboard tiles.
