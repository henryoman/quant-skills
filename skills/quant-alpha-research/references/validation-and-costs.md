# Validation, Costs, and Promotion Gates

This is the honesty layer. Its job is to turn attractive patterns into either
credible evidence or documented failures.

> **Planned figure:** a purged walk-forward timeline showing training,
> validation, purge, embargo, test, and locked-holdout boundaries.

## 1. Causality audit

For every feature, write its last required timestamp. For every trade, write the
first executable timestamp. The latter must be later.

Common leakage:

- using the current candle high/low/close before it is closed;
- filling at that same close after computing a signal from it;
- centered rolling windows or future-smoothed states;
- full-sample scalers, quantiles, PCA, clusters, imputation, neutral bands, or
  outlier thresholds;
- labels or future PnL used in feature selection outside training/validation;
- revised candles that were not known in real time;
- target construction crossing a split boundary without purge;
- overlapping barrier events double-counted as independent trades;
- using test data to choose the prettiest regime or chart.

## 2. Chronological selection protocol

Minimum:

```text
train -> fit transformations/features/model
validation -> choose a small rule/threshold set
purge/embargo -> remove overlapping information
test -> one untouched report
```

Final standard:

```text
fold 1: train A, validate B, test C
fold 2: train A+B, validate C, test D
fold 3: train A+B+C, validate D, test E
...
```

Rolling windows are also valid when old data is harmful. Compare expanding and
rolling only as a predeclared robustness question.

### Purge

Remove training/validation observations whose label or holding interval overlaps
the next evaluation interval. Account for the largest target/holding horizon.

### Embargo

Leave an additional time buffer after a validation/test block before future
training rows are allowed, especially when features have long lookbacks or data
events cluster.

Persist the actual row/time boundaries and verify zero forbidden overlap—not
just the intended sizes.

## 3. Nested selection

The complete search procedure is what must be validated. If the process tries
50 features, 8 lookbacks, 5 horizons, 6 models, and 10 thresholds, reporting the
single final winner as “one test” is false.

A clean structure:

```text
outer fold test: estimates the research procedure
inner train/validation: selects family, features, parameters, threshold
```

If nested evaluation is too expensive, sharply reduce the search and lock a
final untouched period.

## 4. Multiple-testing control

Record a search ledger:

```text
experiment IDs
features/pairs
lookbacks
horizons
targets
models/hyperparameters
thresholds/gates
cost variants used for selection
all failed and positive results
```

Use appropriate tools depending on the question:

- Benjamini-Hochberg/FDR for a family of model-free hypothesis tests;
- block/permutation max-stat null for “best of search” significance;
- White-style reality check or superior-predictive-ability test for many
  strategy variants;
- deflated Sharpe ratio or probabilistic Sharpe diagnostics when selecting by
  Sharpe;
- probability of backtest overfitting/combinatorial purged CV for large strategy
  searches;
- a final locked holdout and forward paper cohort regardless of p-values.

Statistical correction does not repair bad economics or leakage.

## 5. Dependence-aware uncertainty

IID standard errors are usually wrong for market bars and overlapping labels.
Prefer:

- non-overlapping decisions;
- moving-block or stationary bootstrap;
- HAC/Newey-West-style uncertainty for means/regressions;
- clustering by day/session/event;
- trade-level bootstrap if trades are truly separate;
- fold distribution and worst-fold reporting.

Choose block length using the longest relevant autocorrelation/holding horizon,
then stress nearby block lengths.

## 6. Costs and execution math

For a position `s_t` in `{-1,0,+1}` and executable entry/exit prices:

```text
gross_trade_return = side * (P_exit / P_entry - 1)
net_trade_return = gross_trade_return
                 - entry_fee - exit_fee
                 - spread_cost
                 - slippage_cost
                 - funding_or_carry
                 - other venue costs
```

For continuous rebalanced positions:

```text
gross_bar_pnl = prior_position * next_executable_return
turnover = abs(position_t - position_(t-1))
net_bar_pnl = gross_bar_pnl - turnover * one_way_cost - funding
```

State whether costs are in return units, quote currency, contracts, or basis
points. Do not subtract a percentage fee from a binary-contract dollar payoff or
vice versa without the correct instrument math.

### When only OHLCV exists

You may show a transparent proxy grid:

```text
fees = known schedule or explicit assumption
spread = unavailable -> stress assumptions, never zero by silence
slippage = size-independent proxy grid
latency = one or more delayed-entry bars
depth/fill = unavailable
```

Evidence stays `proxy_only`.

### When quotes/depth exist

Use:

- decision-time bid/ask, not midpoint fills;
- full-depth VWAP for stated size;
- rejected/partial fills;
- quote staleness and request/compute/order latency;
- venue precision, minimum size, and order constraints;
- realized fees and funding;
- official settlement or realized exit.

## 7. Strategy metrics

Always report:

```text
observations, signals, trades, independent events, unique markets/days
gross and net PnL/return
average and median net trade
wins, losses, win rate
average win, average loss, payoff ratio
profit factor
max single loss and worst bar/day
max drawdown and recovery duration
exposure, turnover, average holding time, concurrency
fee/spread/slippage/funding drag
long/short split
top-N and bucket concentration
```

Risk-adjusted metrics may include Sharpe-like, Sortino, Calmar, tail ratio,
expected shortfall, and drawdown-at-risk, but disclose frequency, sample length,
autocorrelation treatment, and any annualization.

Prediction-specific metrics:

```text
classification: base rate, balanced accuracy, precision/recall, ROC-AUC,
                PR-AUC, log loss, Brier, calibration
regression: MAE, RMSE, rank correlation, out-of-sample R²
quantiles: pinball loss, interval coverage and width
volatility/range: QLIKE or declared loss, calibration by predicted bucket
```

Optimize the metric that maps to payoff. Accuracy is usually not enough.

## 8. Robustness battery

Before promotion, test the frozen candidate across:

- neighboring feature lookbacks and forecast/holding horizons;
- neighboring thresholds and neutral bands;
- train/validation boundary changes;
- expanding versus rolling windows if justified;
- one or more bar-phase offsets;
- entry delays;
- 0.5× to 2× costs and realistic size/slippage;
- long and short sides separately;
- volatility, volume, trend/chop, time, and liquidity regimes;
- months/folds and leave-one-period-out;
- top-N trade removal;
- alternate but defensible data source/venue or another asset as replication;
- raw versus robustly flagged data;
- non-overlapping versus overlapping evaluation.

The goal is not to demand every number remain identical. The economic sign and
story should remain coherent.

## 9. Negative controls

At least two should accompany a serious candidate:

- block-shuffled or circularly shifted labels;
- time-reversed feature as an impossibility check;
- random entries matched for count/exposure/holding period;
- random feature with the same search pipeline;
- irrelevant lag or intentionally stale feature;
- alternate bar offsets;
- costless versus costed comparison;
- simpler feature/model ablation;
- venue/feed normalization control;
- future-information trap test in unit tests (pipeline must reject it).

## 10. Promotion gates

### Gate A — Data-valid

- Contract and quality audit pass.
- Decision and label clocks are unambiguous.
- Results are not driven by bad bars/gaps.

### Gate B — Descriptive edge

- Conditional effect differs from unconditional baseline.
- Support and uncertainty are adequate.
- Effect is contiguous/ordered and economically interpretable.

### Gate C — Out-of-sample proxy edge

- Frozen validation-selected rule survives untouched test.
- Beats naive and shuffled-search baselines.
- Net positive under a declared conservative proxy cost.
- Not concentrated in one period/trade/side.

### Gate D — Robust research candidate

- Purged walk-forward evidence across several meaningful folds.
- Parameter plateau and delay/cost tolerance.
- Multiple-testing treatment reported.
- Simpler alternatives compared.

### Gate E — Paper candidate

- Versioned rule produces forward decisions and logs every rejection.
- Probability/outcome and proxy/live price calibration remain acceptable.

### Gate F — Fillable candidate

- Actual quotes/depth support stated size.
- Fees, partial/rejected fills, latency, and venue constraints included.
- Official/realized outcome reconciles.

### Gate G — Small live candidate

- Forward settled net results remain positive at tiny controlled risk.
- Kill switches, max loss, monitoring, and replay are ready.

No gate is skipped because a backtest looks spectacular.

## 11. Decision labels

Every report ends with exactly one:

```text
reject
diagnostic_only
continue_research
paper_candidate
fillable_candidate
small_live_candidate
```

Also state the next falsification test. “Try more models” is not a falsification
test; “run frozen rule on the next 20 independent periods with full-depth VWAP
and fail if net average <= 0” is.
