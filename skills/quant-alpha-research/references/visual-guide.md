# Visual Guide: What to Plot and How to Read It

Charts are diagnostic instruments, not decoration. Every chart needs a question,
an exact denominator, and a reason it could falsify the idea.

All HTML reports in this repository must render charts **one per row at the full
available width**. Do not use thumbnail galleries, side-by-side plot grids, or
max-width caps that shrink charts. Multi-panel comparisons may be inside one
full-width figure only when axes and color scales are truly shared.

## The minimum chart stack

For a serious candidate, produce these in order:

1. raw/normalized price and data-quality flags;
2. target distribution and unconditional baseline;
3. feature distribution over time and by split;
4. univariate conditional profile with uncertainty and support;
5. train, validation, test conditional heatmaps plus support;
6. event path with block-bootstrap interval;
7. parameter-neighborhood surface;
8. prediction calibration/deciles if a model is used;
9. unseen fold outcomes;
10. net equity, underwater drawdown, trade distribution, exposure and turnover;
11. cost × delay surface;
12. concentration and leave-one-bucket-out result.

## Candle anatomy

> **Planned figure:** candle anatomy labeled with body, upper and lower wick,
> range, close location, and the corresponding normalized geometry.

Interpret candle shape as continuous geometry first:

```text
body fraction + upper wick fraction + lower wick fraction = approximately 1
close position near 1 = close near high
close position near 0 = close near low
```

A “hammer” name is only a thresholded region of this geometry. Before claiming
pattern alpha, show that the named token adds value beyond range, volatility,
prior direction, and the underlying continuous fractions.

## Heatmaps: the right way to find clusters

> **Planned figure:** a synthetic heatmap contrasting a supported cluster, a
> fragile isolated hot pixel, and a broad weak region. It demonstrates how to
> read evidence and does not represent a real signal.

### What each axis should mean

Use causal present-time features on both axes. Usually use train-fitted
equal-count quantile bins so the middle of the distribution is not overfull.

Example:

```text
x = past return quantile, low to high
y = relative volume quantile, low to high
cell value = average future net signed return in bps
```

Every outcome heatmap needs a paired support heatmap with exactly the same axes.
Useful cell values include:

- average/median future return;
- excess over the unconditional mean;
- hit-rate lift over base rate;
- future absolute move/range;
- upper-before-lower probability lift;
- net strategy payoff;
- uncertainty statistic, preferably with dependence-aware intervals.

### Use four maps, not one

For each feature pair and horizon, show one per row:

```text
1. train outcome/lift
2. validation outcome/lift
3. untouched test outcome/lift
4. test support or effective support
```

Use the same bin edges and color scale. If every panel autoscales, noise can
look equally strong everywhere.

### A credible cluster

A candidate cluster should satisfy most of these:

- contiguous cells, not one pixel;
- same economic story across neighboring cells;
- enough raw and effective observations in each cell;
- similar sign in train, validation, test, and several walk-forward folds;
- effect remains when axes shift slightly or bins change from 5 to 10;
- effect remains with a small entry delay and conservative costs;
- cluster boundary can be simplified into a rule without selecting test cells;
- not owned by one day/month/side/regime;
- credible uncertainty after overlap and multiple testing.

### Cluster types and what they suggest

```text
corner cluster     -> joint extremes or interaction
horizontal band    -> y feature dominates; x may be unnecessary
vertical band      -> x feature dominates; y may be unnecessary
diagonal ridge     -> balance/relative relationship between x and y
U-shape             -> both extremes matter; linear model may miss it
center island       -> mid-regime sweet spot; check binning sensitivity
sign flip           -> possible regime routing or side asymmetry
single hot pixel    -> usually sparse noise until proven otherwise
```

### From cluster to rule

Do not trade “whatever cells are green on test.” Instead:

1. discover a family on train;
2. describe a simple contiguous region;
3. choose/freeze boundaries on validation;
4. run the frozen rule once on test;
5. stress neighboring boundaries and folds;
6. include the entire search in the multiple-testing accounting.

### Support standards

There is no universal minimum count, because dependence and payoff variance
matter. Report:

```text
raw cell rows
non-overlapping/effective rows
unique days/sessions/events
number of folds containing the cell
mean, median, dispersion, uncertainty interval
top observation contribution
```

Mask unsupported cells visually, but keep their counts accessible. Never color
missing/underpowered cells as zero or neutral.

## Univariate conditional profile

Use train-fitted bins on the x-axis. A useful full-width figure contains:

- mean or median future outcome;
- uncertainty band;
- unconditional baseline line;
- support bars on a secondary lower panel;
- separate train/valid/test lines using the same bin edges.

Read shapes:

```text
monotonic slope -> threshold/ranking candidate
tail-only effect -> selective event candidate
U-shape -> magnitude/regime candidate
inverted U -> middle-regime sweet spot
random sawtooth -> likely noise or bins too fine
train slope, test flat -> overfit/nonstationary
```

## Event-study path

At event time `0`, normalize price or cumulative return to zero. Plot forward
median and mean because tails can pull them apart. Add block-bootstrap bands and
a matched-control path. Include MFE, MAE, and event counts.

Red flags:

- move happens before event time (leakage or late event definition);
- all profit is in the first unfillable instant;
- mean works but median does not because one event dominates;
- events overlap so heavily that one episode is counted many times;
- post-event path reverses before realistic entry delay.

## Horizon and lookback surfaces

Axes:

```text
x = past feature lookback in clock time
y = future forecast/holding horizon in clock time
color = net effect or predictive score
contours/text = effective trade count
```

Look for a broad time-scale region. An isolated `lookback=17, horizon=43` winner
is not a discovery unless market mechanics explain those exact clocks.

## Parameter plateau surface

Plot the validation-selected point inside the complete local neighborhood. Use
the same surface on untouched test without moving the marker.

Good:

```text
neighboring thresholds/lookbacks remain positive
support changes smoothly
selected point is not on an extreme boundary
```

Bad:

```text
one cell is bright and every neighbor is negative
best point sits at the far edge of searched values
profit rises only as trade count collapses
```

## Prediction-decile plot

Sort out-of-sample predictions into train-fitted or equal-count deciles. Plot:

- actual future outcome by prediction decile;
- predicted probability/value;
- support;
- net payoff after the frozen decision rule.

The desired shape is ordered. A model can have modest AUC but useful extreme
deciles; it can also have good average accuracy but no net-payoff ordering.

## Calibration/reliability plot

For probability forecasts:

```text
x = predicted probability
y = observed frequency
diagonal = perfect calibration
```

Add sample count per bin and Brier/log loss. Calibrate only using training/
validation. A model saying `0.70` and realizing `0.54` is dangerous even if its
ranking is decent.

## Fold matrix

Rows are unseen walk-forward folds; columns are strategy variants, sides, or
regimes. Color net return/PnL and print trade count. This exposes whether the
aggregate is one lucky window.

Prefer:

- many small positive/near-zero folds;
- limited downside in bad folds;
- similar behavior across sides/regimes;
- stable trade availability.

Distrust:

- one giant green fold surrounded by losses;
- no trades in most folds;
- rules/thresholds jumping wildly every fold;
- selection that is worse than a fixed simple baseline.

## Equity and drawdown

Always show net equity and underwater drawdown as separate full-width charts.
Equity alone hides path risk.

Annotate:

- fees/spread/slippage/funding assumption;
- trade/exposure count;
- training/validation/test or fold boundaries;
- maximum drawdown and recovery length;
- whether returns are mark-to-market or realized;
- whether positions overlap.

Do not annualize a short sample without making the extrapolation obvious.

## Cost × delay heatmap

Axes:

```text
x = all-in round-trip cost or size/slippage assumption
y = entry delay
color = net PnL/return/average trade
```

Add a zero-profit contour and mark the conservative base assumption. Alpha that
exists only at zero delay and zero cost is not actionable.

## MFE/MAE plot

Useful views:

- scatter `MAE` versus `MFE`, colored by final outcome;
- marginal distributions;
- excursion by signal score/regime;
- time to MFE/MAE.

This tells whether entries are directionally right but poorly timed, whether
stops cut eventual winners, and whether tail losses dominate.

## Concentration visuals

Plot PnL by:

```text
day/week/month
hour/session
side
volatility/volume regime
asset/venue
signal score decile
holding time
top-N trades
```

Add a contribution Lorenz curve or cumulative share. Then rerun the headline
metric leaving out each major bucket and removing the top 1/5/10 trades.

## Charts that often mislead

- Price with hand-drawn arrows: useful for examples, not evidence.
- Correlation matrix on price levels: shared trends can make nonsense look
  strong; use returns and lagged prediction.
- Feature importance without out-of-sample ablation: not proof of edge.
- t-SNE/UMAP clusters colored by future return: label leakage and projection
  artifacts are easy; confirm clusters in original features and future time.
- Backtest equity without drawdown, exposure, turnover, and costs.
- Heatmap without support or with individually autoscaled splits.
- Cumulative return made from overlapping horizon labels as if trades were
  independently executable.
- Candlestick gallery of winners only; always show matched losers and random
  examples.

## Figure caption contract

Every figure caption should answer:

```text
what data and UTC range?
what is known at decision time?
what exactly are x, y, color, and denominator?
gross or net of which costs?
which split/fold?
raw rows or independent events?
what would falsify the reading?
```
