# Crosswalk to Existing Repository Work

> **Status: provenance only.** This document describes the repository in which
> the framework was originally synthesized. Its paths and scope constraints may
> not exist here. Do not use it as active methodology or current empirical
> evidence.

The new framework is a synthesis layer, not a replacement for existing
experiments. Executable code and run artifacts remain under
`apps/research/experiments/`; this folder explains how to design and judge the
next experiment consistently.

The review covered the active research hub and notebook findings, continuous
candle dataset/taxonomy/Markov work, state-table families and candle-pattern
states, sticky EMA labels/features, univariate scans, indicator-classifier
history, volatility/volume regime scout, BTC→SOL lead-lag and walk-forward
reports, current alpha status/playbook, pricing/feed normalization findings,
math/strategy documentation, and archived baseline/mining/model families. Large
generated datasets and chart binaries were inventoried through their manifests
and reports rather than treated as independent research ideas.

## Existing family → framework lesson

| Existing work | What it contributes here | Framework destination |
|---|---|---|
| [5m alpha primer](../apps/research/reports/5m-alpha-research-primer.md) | targets beyond direction, causal features, range/volatility first, calibration, full pipeline | data/labels, E06-E48 |
| [Univariate state testing](../apps/research/experiments/univariate_state_testing/README.md) | one-feature equal-count bins, split stability, model-free discovery | E06 and heatmap guide |
| [Continuous experiment](../apps/research/experiments/continuous/) | modular OHLCV feature groups, candle geometry/tokens, lag sequences, Markov k2/k3 | E11-E12, E37-E39 |
| [State tables](../apps/research/experiments/state_tables/README.md) | compact interpretable conditional probabilities, smoothing/support, test survival | E13, E17, E37-E38 |
| [Sticky experiment](../apps/research/experiments/sticky/README.md) | long-memory features and direction/power/choppiness labels; prediction does not equal strategy | label library, E19, E44-E45 |
| [Indicator classification](../apps/research/experiments/indicator_classification/ALPHA_README.md) | chronological selection, neutral bands, cost-aware non-overlapping trades, longer horizons, model comparison | E44-E48, validation |
| [Vol/volume regime scout](../apps/research/experiments/vol_volume_regime_scout/FINDINGS.md) | volume/volatility can identify opportunity magnitude while failing as direction | E27-E30, gating logic |
| [BTC→SOL experiment guide](../apps/research/experiments/solbtccorrelation/btc_sol_30s_predictive_power_experiment.md) | leader features must precede follower outcomes; same-time correlation is insufficient | E49-E51 |
| [BTC→SOL walk-forward report](../apps/research/experiments/solbtccorrelation/outputs/walkforward_backtest/walkforward_backtest_report.md) | expanding train/valid/test folds, fixed versus adaptive regime rules, equity/drawdown/fold charts | E40, E54, visuals |
| [Adaptive/pruned report](../apps/research/experiments/solbtccorrelation/outputs/adaptive_pruned/adaptive_pruned_report.md) | prune weak families, compare adaptive selector to simple fixed anchor | E48, E54, selection controls |
| [Current alpha findings](../apps/research/reports/alpha-findings.md) | prioritize broad interpretable and selective cost-aware lanes; next work is honest validation | promotion gates |
| [Current alpha status](../ALPHA_STATUS_CURRENT.md) | raw cross-feed price gaps shrink after start-normalized returns; distinguish diagnostics from tradable evidence | E52, evidence ladder |
| [Up/Down playbook](../UP_DOWN_STRATEGY_PLAYBOOK.md) | proxy price history cannot prove executable depth; log exact entry, size, fees, skips, and settlement | E53-E59 |
| [Math package](../packages/math/src/) | explicit expected-value, probability, volatility scaling, and binary pricing functions | glossary and instrument extensions |

## Lessons carried forward, including failures

### 1. Interpretable state spaces work only while supported

The repo explored 9-, 27-, 32/128-, 81-, and 125-style state tables, as well as
doji and engulfing states. Their reusable lesson is not that one magic number of
states wins. It is:

```text
compact causal state -> train-only counts/probabilities -> smoothing/support ->
unchanged out-of-sample lookup -> survival report
```

State spaces explode exponentially. This framework therefore requires support,
effective counts, smoothing, coverage, and order-comparison plots in E37-E38.

### 2. Continuous geometry should precede folklore labels

The continuous taxonomy encodes body fraction, wick fractions, close position,
range, activity, and lags before named candle classes. Pattern experiments then
make engulf coverage, extension, body ratio, and close strength numeric. This is
why E11 and E15 ask whether a named token adds value beyond its raw geometry.

### 3. Neutral/no-trade states are structural

The state/classifier work showed why forcing every bar into up/down can create
low-quality coverage. Neutral bands, confidence thresholds, and skip rules are
valid—but their thresholds belong to training/validation, and the final test
must report both quality and lost coverage.

### 4. Longer horizons can reveal weak structure, but overlap is dangerous

Current findings surfaced stronger selective classifier lanes at longer
horizons. Those labels overlap heavily if evaluated every bar. The framework
therefore requires non-overlapping decision logic or dependence-aware
uncertainty, purge/embargo, and actual holding/concurrency simulation.

### 5. Volume is often an opportunity filter, not a direction oracle

The volatility/volume scout found larger future absolute moves in high relative
volume and expansion regimes while naive current-bar continuation remained
negative after its cost hurdle. This directly motivates separate magnitude and
direction targets in E29-E30.

### 6. Adaptive selection must beat a simple fixed anchor

The cross-asset reports compare broad/adaptive/pruned selectors with a raw model
and fixed regime rules. This avoids celebrating complex selection that merely
chases validation noise. E48 and E54 require that same comparison and fold-by-
fold visibility.

### 7. Same-time co-movement is not predictive lead-lag

The BTC→SOL work explicitly separates correlation now from BTC information now
predicting SOL later. E49 requires a B-only baseline, timestamp alignment, lag ×
horizon surface, and delay stress.

### 8. Raw feed level differences are not automatically alpha

The current pricing/feed work found large raw-level discrepancies that mostly
collapsed after each source was normalized from its own start. Quote asset,
venue, age, raw payload, target construction, and settlement source must remain
visible. E52 treats feed disagreement as diagnostic until it survives those
checks and maps to an executable payoff.

### 9. Backtests are evidence, not fills

The Up/Down work separates proxy price histories, paper decisions, executable
depth, and settlement. The evidence ladder and E59 generalize that distinction.
Missing depth does not mean infinite capacity; missing spread does not mean zero
cost.

### 10. Charts need to reveal failure, not only winners

Existing rebuilt notebooks and reports show state support, split performance,
equity, drawdown, rules, and fold outcomes. This framework standardizes the
full-width one-chart-per-row rule and adds paired support, cost/delay, parameter
plateau, and concentration visuals.

## Existing concepts intentionally not promoted as universal truths

- A custom sticky EMA is a feature family to compare, not a privileged market
  law.
- RSI, Bollinger, moving averages, named candles, HMMs, trees, or deep sequence
  models are competing representations, not schools to believe in.
- A positive state/classifier result in one file is a research lead, not a
  reusable parameter for every asset/timeframe.
- High volume does not automatically tell direction.
- Cross-asset correlation does not automatically identify a leader.
- Raw venue/price basis does not automatically identify arbitrage.
- Historical OHLCV cannot establish historical fill depth.

## Where new work should go

```text
quant-skill/
  instructions, experiment definitions, templates, graphics

apps/research/experiments/<existing-or-new-family>/
  offline code, configs, derived datasets, run artifacts

packages/data/
  raw and canonical source-of-truth data

apps/exec/
  TypeScript polling, paper-live, order decisioning, execution
```

Before creating any executable family, check the existing experiment map above.
For example, univariate bins belong with `univariate_state_testing`, candle
sequences with `continuous`/`state_tables`, rich tabular models with
`indicator_classification`, and cross-asset lead-lag with `solbtccorrelation`
unless the new logic is materially different.

## Current-scope guard

This general instruction set does not run or optimize any market. In the active
repository workflow, SOL Up/Down research is 5-minute only. Historical
15-minute artifacts are legacy and were not used as active strategy guidance in
this framework.
