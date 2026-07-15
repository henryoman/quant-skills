# Step-by-Step OHLCV Alpha Workflow

Use this as the literal instruction list. Do not jump to ML or strategy PnL
before the earlier evidence exists. Each step has an output and a stop rule.

## Step 0 — Write one falsifiable question

Good:

```text
Does low 20/240-bar range ratio predict larger next-10-bar total range than the
unconditional baseline, across unseen chronological folds?
```

Bad:

```text
Find the best indicators.
```

Choose exactly one primary label family:

- direction/return;
- absolute move/volatility;
- future high/low/range;
- barrier/time-to-event;
- path efficiency/choppiness/drawdown;
- regime transition;
- net executable payoff.

Output: a filled research-question section from
[experiment-template.md](experiment-template.md), including the failure result
that would make you stop.

Stop if: the future outcome or decision time cannot be written exactly.

## Step 1 — Register the data before touching signals

Record:

```text
asset/instrument
venue/feed
quote asset
UTC range
bar duration/type/phase
timestamp open/close semantics
OHLC price type
volume unit
raw paths and hashes/version
```

Run `E00-E02`:

- contract invariants;
- duplicates and expected interval gaps;
- invalid/stale/flat/outlier bars;
- native versus reconstructed bars if possible;
- sensitivity to bar phase/duration when the hypothesis has no exact clock
  mechanism.

Output:

```text
data_manifest.json
quality_summary.json
gap/outlier charts
explicit cleaning log
```

Stop if: the clock, price, quote, or volume meaning is unknown; the edge period
is mostly corrupt; or cleaning decisions depend on future strategy PnL.

## Step 2 — Freeze the decision clock and labels

Draw the clock:

```text
bars available -> signal compute -> delay -> entry -> future path -> exit
```

Define labels with exact formulas from
[data-and-labels.md](data-and-labels.md). Include:

- price used for entry and exit;
- whether target begins at next open or another executable proxy;
- horizon in bars and clock time;
- neutral band or barrier levels;
- same-bar barrier ambiguity rule;
- overlapping-event policy.

Create at least one magnitude target even when the goal is direction. This tells
whether a directional failure is actually an opportunity/movement signal.

Output: label definitions, label distribution, ambiguous-label counts, raw and
effective sample counts.

Stop if: the label uses prices that occur before a realistic entry, or OHLC
cannot resolve the claimed order of events.

## Step 3 — Split time and lock the final test

Before feature screening:

1. allocate chronological train, validation, and test periods;
2. calculate maximum feature lookback and label/holding horizon;
3. specify purge and embargo;
4. freeze UTC boundaries;
5. reserve a later forward cohort if possible.

Nothing is randomly shuffled across time except inside an explicit null test.

Output: split/fold table and timeline graphic.

Stop if: train labels or position intervals overlap evaluation data after purge,
or the “test” has already been repeatedly used for selection.

## Step 4 — Build small causal feature families

Build raw interpretable facts before indicators:

```text
returns at multiple clock scales
realized volatility / absolute movement / ATR / range
body, wick, close position, true range
relative volume and volume trend
distance to causal rolling mean/high/low
trend slope and path efficiency
time cycles
```

Use [feature-library.md](feature-library.md) for formulas, parameter axes,
interpretation, and traps. It includes classical indicators as derived feature
families, but every one must compete with its simpler underlying inputs.

Rules:

- all rolling reference values use past/training data only;
- preserve raw values beside scaled values;
- fit bins/scalers on train;
- group features by hypothesis;
- do not produce hundreds of near-duplicate indicators without a search budget.

Output: derived Parquet separated from canonical raw data, feature dictionary,
null/missing counts, and feature distribution by split.

Stop if: a feature's last-used timestamp cannot be proved, or features change
meaning across venue/source transitions.

## Step 5 — Establish the null and naive baselines

Run `E03-E05` before looking for winners:

```text
unconditional outcome distribution
majority/mean/median/zero predictor
last-return sign
volatility persistence
always-long / always-short / always-flat
random rule matched on exposure and holding time
block-shuffled or circularly shifted label search
```

Output: one baseline table used by every later experiment.

Stop if: the full search pipeline “finds” similar edge on shuffled labels.

## Step 6 — Run one-feature discovery

Run `E06` for every approved feature × label × horizon:

1. fit 5 or 10 equal-count bin edges on train;
2. apply the same edges to validation/test;
3. calculate count, effective count, mean, median, quantiles, hit rate,
   uncertainty, and net proxy payoff;
4. rank by validation stability, not whole-sample t-stat;
5. retain failures in the search ledger.

Look for:

- monotonic ordering;
- tail effects with enough support;
- U/inverted-U opportunity regimes;
- the same economic sign across time.

Output: profiles, support, ranked feature table, complete trial ledger.

Stop/demote if: only one lucky bin works; validation reverses train; or cost is
larger than the conditional shift.

## Step 7 — Find interactions and heatmap clusters

Run `E07-E10` on a **limited pair list motivated by Step 6**, such as:

```text
past return × relative volume
trend × volatility
compression × range position
wick/close strength × prior move
leader shock × follower lag
model confidence × regime
```

For each pair:

1. use train-fitted bins;
2. show train outcome, validation outcome, test outcome, and support separately;
3. keep identical axes and color scale;
4. identify contiguous candidate regions on train/validation only;
5. simplify to a rule;
6. freeze and test once;
7. shift bin edges and thresholds slightly;
8. count the pair/threshold search in multiple testing.

Read [visual-guide.md](visual-guide.md) for cluster shapes.

Output: outcome/support heatmaps, cluster definition, stability matrix, event
study, and plateau surface.

Stop if: the cluster is one sparse pixel, disappears with minor bin changes, or
is owned by one episode.

## Step 8 — Cover the different schools of thought

Do not assume one family explains markets. Give each family a fair, bounded
model-free test from [experiment-catalog.md](experiment-catalog.md):

| Family | Core tests |
|---|---|
| Candle geometry/patterns | E11-E15 |
| Trend/momentum/clean path | E16-E19 |
| Mean reversion/exhaustion | E20-E22 |
| Breakout/range/compression | E23-E26 |
| Volatility/range/volume | E27-E30 |
| Calendar/event cycles | E31-E32 |
| Autocorrelation/variance/long memory/cycles | E33-E36 |
| State tables/Markov/information | E37-E39 |
| Rule/latent/change regimes | E40-E43 |
| Supervised/distribution/sequence/ensemble | E44-E48 |
| Cross-asset/cross-venue | E49-E52 |
| Strategy/execution | E53-E59 |

This coverage prevents school-of-thought tunnel vision. It does not authorize an
unlimited grid. Predeclare at least one or two sensible tests per relevant
family, record the failures, then allocate more effort only where evidence
survives.

Output: family scorecard with `reject`, `diagnostic`, or `candidate` for each.

## Step 9 — Add models only where model-free structure exists

Order:

```text
regularized linear/logistic
small tree/boosting models
quantile/distribution model if tails/range matter
clustering/HMM for routing if regimes matter
sequence model only if lag order adds value
```

For every complex model, compare:

- naive baseline;
- best one-feature/profile rule;
- transparent linear model;
- same model with each feature family removed;
- calibration and prediction-decile ordering;
- performance after costs and non-overlap.

Output: out-of-fold predictions, locked test predictions, calibration, deciles,
fold metrics, feature-family ablations, model card/config.

Stop if: complexity does not add stable unseen net value or probability
calibration is unusable.

## Step 10 — Translate prediction into one exact decision rule

Freeze:

```text
eligibility
long/short/skip mapping
confidence threshold
entry and delay
exit/holding period
position size
concurrency/netting
cooldown/re-entry
fees/spread/slippage/funding
rejection reasons
```

Do not use the future label return directly as an executable PnL stream. Build a
chronological position/trade ledger so overlap, turnover, and capital are real.

Output: trade ledger with signal time, entry/exit, gross/net PnL, costs, MFE,
MAE, regime, fold, and rejection context.

Stop if: trades cannot be reconstructed one by one.

## Step 11 — Run the honesty battery

Run `E53-E58` and [validation-and-costs.md](validation-and-costs.md):

- purged walk-forward of the whole selection procedure;
- search-aware null/multiple-testing controls;
- local parameter plateau;
- bar offset and entry delay;
- cost, spread, slippage, size, and optional funding stress;
- long/short and regime decomposition;
- leave-one-month/day/side/regime out;
- remove top 1/5/10 trades;
- compare rolling versus expanding only if predeclared;
- alternate venue/asset replication where appropriate.

Output: unseen fold matrix, stitched unseen equity, drawdown, cost × delay
surface, concentration report, pass/reject gates.

Stop if: one fold/trade owns PnL, conservative cost/delay removes it, or only an
isolated parameter survives.

## Step 12 — State what is proven

End with:

```text
data and UTC range
trade/independent event/unique market counts
exact entry, side, size, and exit
all costs and unavailable execution fields
wins/losses/PnL/ROI/drawdown/max loss/concentration
validation and multiple-testing method
evidence level
decision label
next falsification test
```

Allowed decision labels:

```text
reject
diagnostic_only
continue_research
paper_candidate
fillable_candidate
small_live_candidate
```

## Step 13 — Forward evidence

For a paper candidate, freeze a version and log forward in real time:

```text
raw source payload pointer
feature snapshot
model/rule version
decision and rejected-signal reason
entry quote and full-depth VWAP when available
latency, fee, slippage, partial/rejected fill
exit and official outcome/settlement
predicted versus realized distribution
```

Do not change the frozen cohort mid-run. New changes create a new version and a
new cohort.

Output: replayable JSONL/Parquet and a forward report.

Stop if: the backtest proxy is systematically unavailable, stale, unfillable,
or misaligned with the actual payoff.

## Step 14 — Promote tiny or retire cleanly

Only after fillable/settlement-backed forward evidence:

- declare max per-trade/day loss and total exposure;
- implement kill switches for data age, spread/depth, venue/API health,
  drawdown, and feature drift;
- start at tiny size;
- compare live slippage/rejection/PnL with paper expectations;
- define automatic demotion criteria.

If retired, preserve the config, data range, results, and failure reason. A
graveyard of clear failures is more valuable than a folder of ambiguous charts.

## Final checklist

```text
[ ] Question and falsification rule written first
[ ] OHLCV source/clock/quote/volume semantics audited
[ ] Decision precedes target and executable entry
[ ] Chronological split, purge, embargo, final lock
[ ] Train-only transforms/bins/states/clusters
[ ] Unconditional, naive, random, and shuffled baselines
[ ] Model-free bins and supported heatmaps
[ ] Multiple schools tested with bounded search
[ ] Complex model beats transparent baseline
[ ] Exact chronological position/trade simulation
[ ] Fees, spread, slippage, delay, size, funding declared
[ ] Walk-forward, parameter plateau, concentration, multiple-testing controls
[ ] Evidence level and decision label stated honestly
[ ] Forward fillability/settlement before meaningful capital
```
