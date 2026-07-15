# Experiment Specification and Report Template

Copy this file into the executable experiment's existing folder. Fill it before
opening the final holdout. The objective is to make every choice, fixed control,
and rejection condition visible.

## A. Identity

```text
experiment_id:
title:
owner:
created_utc:
status: planned | running | complete | rejected | promoted
parent_experiment_ids:
code_commit_or_worktree_state:
evidence_level: descriptive | proxy_only | paper_traded | fillable |
                settlement_backed | live_small
```

## B. Research question

```text
hypothesis:
economic_mechanism:
future_outcome_being_predicted:
why_ohlcv_could_contain_this_information:
what_result_would_falsify_it:
```

Write the core mapping in one line:

```text
[features known by time t] -> [outcome strictly after t]
```

## C. Data contract

| Field | Declared value |
|---|---|
| Asset/instrument | |
| Venue/feed | |
| Quote asset | |
| UTC start/end | |
| Bar duration/type/phase | |
| Timestamp is bar open or close | |
| Raw file(s) | |
| Row count before/after cleaning | |
| Volume unit | |
| Missing-bar policy | |
| Duplicate policy | |
| Outlier policy | |
| Known source/venue changes | |

## D. Decision and label clocks

```text
feature_cutoff:
signal_available_at:
assumed_compute_delay:
assumed_order_or_entry_delay:
entry_price_definition:
target_start:
target_formula:
forecast_horizon:
exit_price_definition:
same_bar_barrier_policy:
overlap_policy:
```

## E. Variables and controls

### Independent variables deliberately varied

| Variable | Values/range | Why these values | Selected using |
|---|---|---|---|
| | | | train / validation only |

### Fixed variables

| Variable | Fixed value | Why held fixed |
|---|---|---|
| Data source | | |
| Target/horizon | | |
| Entry/exit convention | | |
| Position/side rule | | |
| Cost model | | |
| Split/folds | | |
| Metrics | | |
| Plot set | | |

### Nuisance/confounding variables to stratify or match

```text
volatility:
volume/liquidity:
trend/chop:
time/session:
side:
venue/feed age:
other:
```

## F. Feature definitions

For every feature:

| Feature | Exact formula | Lookback | Last timestamp used | Scaling fitted on | Expected relation |
|---|---|---:|---|---|---|
| | | | | train/past only | |

## G. Search budget

```text
feature_count:
feature_pairs_count:
lookbacks_count:
horizons_count:
targets_count:
model_variants_count:
thresholds_count:
cost_variants_used_for_selection:
total_candidate_combinations:
multiple_testing_method:
negative_controls:
```

## H. Splits and leakage protection

| Fold/split | Train UTC | Validation UTC | Test UTC | Purge | Embargo |
|---|---|---|---|---:|---:|
| | | | | | |

```text
maximum_feature_lookback:
maximum_label_or_holding_horizon:
train_fitted_objects: scalers, bins, thresholds, PCA, clusters, model, etc.
test_lock_date:
```

## I. Baselines and negative controls

```text
unconditional baseline:
naive prediction baseline:
equal-exposure random baseline:
shuffled/circular-shift baseline:
simpler model/rule baseline:
```

## J. Strategy translation

Leave blank for descriptive experiments; do not invent trades prematurely.

```text
eligible_signal:
long_rule:
short_rule:
flat_or_skip_rule:
confidence_threshold:
sizing:
maximum_concurrent_positions:
position_netting:
entry:
exit:
stop_or_target:
reentry/cooldown:
every_rejection_reason_logged:
```

## K. Cost and fill assumptions

| Component | Base | Stress values | Source/evidence |
|---|---:|---|---|
| Entry fee | | | |
| Exit fee | | | |
| Spread | | | |
| Slippage at size | | | |
| Latency/delay | | | |
| Funding/carry | | | |
| Depth/partial fills | available/unavailable | | |

If unavailable, write `unavailable`; do not write zero.

## L. Predeclared pass/reject criteria

```text
minimum independent test events/trades:
minimum unique periods/markets:
minimum net average trade or EV:
maximum acceptable drawdown/loss:
minimum positive fold share:
maximum top-N concentration:
required parameter plateau:
required cost/delay survival:
required baseline improvement:
failure conditions:
```

## M. Required plots

Use one plot per full-width row.

```text
[ ] data/gap audit
[ ] unconditional target distribution
[ ] feature distribution by split
[ ] univariate profile + support
[ ] train/valid/test conditional heatmaps + support
[ ] event path + uncertainty
[ ] parameter neighborhood
[ ] prediction deciles/calibration, if modeled
[ ] fold matrix and split map
[ ] net equity
[ ] underwater drawdown
[ ] trade PnL and MFE/MAE
[ ] cost x delay surface
[ ] concentration/leave-one-out
```

## N. Result table

| Metric | Train | Validation | Test | Walk-forward unseen aggregate |
|---|---:|---:|---:|---:|
| Rows | | | | |
| Independent events/trades | | | | |
| Wins / losses | | | | |
| Hit rate | | | | |
| Gross PnL/return | | | | |
| Net PnL/return | | | | |
| Avg/median net trade | | | | |
| Profit factor | | | | |
| Max loss | | | | |
| Max drawdown | | | | |
| Turnover/exposure | | | | |

Add target-specific prediction metrics and uncertainty intervals.

## O. Stability and concentration

```text
positive/total unseen folds:
worst unseen fold:
long vs short:
top 1/5/10 trade contribution:
top day/week/month contribution:
worst cost/delay still positive:
neighbor parameter sign consistency:
regimes where it works:
regimes where it fails:
```

## P. Conclusion

```text
decision: reject | diagnostic_only | continue_research | paper_candidate |
          fillable_candidate | small_live_candidate
what_is_actually_proven:
what_is_not_proven:
largest_failure_mode:
next_single_falsification_test:
```

## Compact machine-readable configuration example

This is illustrative. Keep the actual file next to experiment code only if it is
used; do not build configuration infrastructure just to mirror this template.

```yaml
experiment_id: E29-sol-example-v1
data:
  asset: ASSET
  venue: VENUE
  quote_asset: QUOTE
  bar_duration: 5m
  timestamp_semantics: bar_open
  start_utc: YYYY-MM-DDTHH:MM:SSZ
  end_utc: YYYY-MM-DDTHH:MM:SSZ
decision:
  feature_cutoff: closed_bar_t
  entry: open_t_plus_1
  delay_bars: 1
label:
  name: future_abs_return
  horizons_bars: [1, 2, 5, 10]
features:
  relative_volume_windows: [20, 60, 240]
  volatility_windows: [20, 60, 240]
fixed:
  quantile_bins: 5
  sides: [long, short]
  overlap_policy: non_overlapping
validation:
  scheme: purged_walk_forward
  purge_bars: 10
  embargo_bars: 10
costs_bps:
  base_round_trip: null  # unavailable until sourced; never silently zero
  stress: [2, 4, 8, 12]
```
