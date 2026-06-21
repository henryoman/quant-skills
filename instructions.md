# Project Instructions

Read this first when working in this repository.

## Root Layout

Keep the root simple:

```text
quant-skills/
  instructions.md
  start-here/
  README.md
  cmc-bnb-skills/
  third-party-skills/
  alpha-gen-skills/
```

Only `instructions.md` and `start-here/` are root-level instruction/bootstrap artifacts. All other skills go in one of the three buckets.

## Buckets

- `cmc-bnb-skills/`: official CoinMarketCap skills plus BNB project foundation material.
- `third-party-skills/`: external/community/vendor skills, mirrors, or imports that are not official CMC and not authored here.
- `alpha-gen-skills/`: skills and packages authored in this workspace for alpha generation, strategy research, data setup, and quant tooling.

## Standalone Skill Install

If someone downloads skills through a skill installer, `start-here/` is the portable instruction package. It is self-contained:

- `start-here/SKILL.md`
- `start-here/references/free-data-manifest.md`
- `start-here/references/track2-architecture.md`
- `start-here/references/source-policy.md`
- `start-here/references/examples.md`
- `start-here/agents/openai.yaml`

The root `instructions.md` is for repository-first onboarding. The `start-here/` folder is for agent/skill-first usage.

Install one concrete skill folder at a time. Do not point an installer at the whole repo or at a bucket folder unless the installer explicitly supports nested skills.

Recommended order:

1. `start-here/`
2. `cmc-bnb-skills/<skill-name>/`
3. `alpha-gen-skills/<skill-name>/`
4. `third-party-skills/<skill-name>/`

Data-source selection, API key setup, and `.env` templates belong in `start-here/`. Repeatable Binance download/clean pipelines live in `alpha-gen-skills/data-download-clean/`. Downstream alpha-generation skills should consume normalized data and focus on research.

## OHLCV-Only Alpha Discovery Framework

### Main Objective

Find whether an event visible in OHLCV data creates statistically different future behavior.

The basic research question is:

```text
When condition C happens at time t, does behavior after t differ from normal behavior?
```

Examples:

- Does an unusually large return continue or reverse?
- Does unusually high volume predict higher future volatility?
- Does a breakout continue or fail?
- Does a failed break below a recent low reverse upward?
- Does volatility compression precede movement expansion?

Useful OHLCV alpha can be:

- `directional`: future returns are biased up or down.
- `volatility`: future movement is larger than usual.
- `path`: price is more likely to hit one side before the other.
- `regime-specific`: the effect only appears in trend, chop, compression, or expansion.

The output should be a ranked set of anomalies with evidence.

### Core Acceptance Rule

Only accept a signal if all of these are true:

- The event is known at time `t`.
- The future outcome is measured after time `t`.
- The event sample is compared against the unconditional baseline.
- The result is checked out of sample using chronological splits.
- The result does not depend on one exact threshold.
- The result survives basic execution and cost assumptions.

## 1. Prepare the OHLCV Data

Allowed inputs:

```text
timestamp
open
high
low
close
volume
```

Do not use news, fundamentals, order book data, market identity, asset-class assumptions, or external context unless a separate task explicitly changes the scope.

Before testing, reject or flag invalid candles:

- `open <= 0`
- `high <= 0`
- `low <= 0`
- `close <= 0`
- `volume < 0`
- `high < low`
- `high < open`
- `high < close`
- `low > open`
- `low > close`
- duplicated timestamps
- unordered timestamps
- missing intervals when candles are expected to be evenly spaced

Compute the base columns:

```text
log_close = ln(close)
log_volume = ln(1 + volume)
r1 = ln(close_t / close_{t-1})
```

The base table must contain:

```text
timestamp, open, high, low, close, volume, log_close, log_volume, r1
```

## 2. Build a Compact Feature Set

Do not create hundreds of indicators. Build only features that answer five questions:

1. Did price move unusually far?
2. Was the candle range unusually large or small?
3. Was volume unusually high or low?
4. Where did the candle close inside its range?
5. Was the recent market trending, choppy, compressed, or expanded?

### Return Features

```text
r1  = ln(close_t / close_{t-1})
r3  = ln(close_t / close_{t-3})
r5  = ln(close_t / close_{t-5})
r10 = ln(close_t / close_{t-10})
r20 = ln(close_t / close_{t-20})
r1_z_100 = rolling_zscore(r1, 100)
```

Candidate events:

- `r1_z_100 > 2`
- `r1_z_100 < -2`
- `abs(r1_z_100) > 2`

### Range Features

```text
hl_range = ln(high / low)
body = abs(ln(close / open))
body_ratio = body / hl_range
hl_range_z_100 = rolling_zscore(hl_range, 100)
```

If `hl_range = 0`, set `body_ratio = 0`.

Candidate events:

- `hl_range_z_100 > 2`
- `hl_range_z_100 < -1`
- `body_ratio < 0.30`
- `body_ratio > 0.70`

### Wick and Close-Location Features

```text
clv = (2 * close - high - low) / (high - low)
upper_wick = ln(high / max(open, close))
lower_wick = ln(min(open, close) / low)
upper_wick_ratio = upper_wick / hl_range
lower_wick_ratio = lower_wick / hl_range
```

If `high = low`, set `clv = 0`. If `hl_range = 0`, set wick ratios to `0`.

Candidate events:

- `clv > 0.80`
- `clv < -0.80`
- `upper_wick_ratio > 0.60`
- `lower_wick_ratio > 0.60`

### Volume Features

```text
volume_z_100 = rolling_zscore(log_volume, 100)
volume_pct_200 = rolling_percentile(log_volume, 200)
```

Candidate events:

- `volume_z_100 > 2`
- `volume_z_100 < -1`
- `volume_pct_200 > 0.95`

### Volatility State Features

```text
true_range = max(
  ln(high_t / low_t),
  abs(ln(high_t / close_{t-1})),
  abs(ln(low_t / close_{t-1}))
)
atr_20 = rolling_mean(true_range, 20)
atr_100 = rolling_mean(true_range, 100)
atr_ratio = atr_20 / atr_100
```

Regime labels:

- `compression`: `atr_ratio < 0.60`
- `normal`: `0.75 <= atr_ratio <= 1.25`
- `expansion`: `atr_ratio > 1.40`

### Trend and Chop Features

```text
trend_20 = ln(close_t / close_{t-20}) / atr_20
efficiency_20 = abs(sum(r1 over last 20 bars)) / sum(abs(r1) over last 20 bars)
```

Regime labels:

- `uptrend`: `trend_20 > 1.5`
- `downtrend`: `trend_20 < -1.5`
- `neutral`: otherwise
- `choppy`: `efficiency_20 < 0.25`
- `clean trend`: `efficiency_20 > 0.60`

### Rolling High and Low Features

Compute recent highs and lows excluding the current candle:

```text
rolling_high_20 = max(high from t-20 to t-1)
rolling_low_20  = min(low from t-20 to t-1)
```

This exclusion is mandatory. Do not include the current candle when defining the level being broken.

Candidate events:

- `close_t > rolling_high_20`
- `close_t < rolling_low_20`
- `high_t > rolling_high_20 and close_t < rolling_high_20`
- `low_t < rolling_low_20 and close_t > rolling_low_20`

## 3. Build Future Outcome Targets

Keep features and targets separate.

Features use information available at or before time `t`. Targets use information after time `t`.

### Directional Targets

```text
fwd_r1  = ln(close_{t+1} / close_t)
fwd_r3  = ln(close_{t+3} / close_t)
fwd_r5  = ln(close_{t+5} / close_t)
fwd_r10 = ln(close_{t+10} / close_t)
```

### Volatility Targets

```text
fwd_abs_r5 = abs(fwd_r5)
fwd_abs_r10 = abs(fwd_r10)
```

### Path Targets

```text
future_high_10 = max(high from t+1 to t+10)
future_low_10  = min(low from t+1 to t+10)
future_upside_10 = ln(future_high_10 / close_t)
future_downside_10 = ln(close_t / future_low_10)
future_range_10 = future_upside_10 + future_downside_10
```

## 4. Test the Fixed Anomaly Library

Do not freely invent unlimited rules. Test this fixed library first.

| Anomaly | Condition | Primary Targets |
| --- | --- | --- |
| Positive return shock | `r1_z_100 > 2` | `fwd_r1`, `fwd_r3`, `fwd_r5`, `fwd_r10`, `fwd_abs_r5` |
| Negative return shock | `r1_z_100 < -2` | `fwd_r1`, `fwd_r3`, `fwd_r5`, `fwd_r10`, `fwd_abs_r5` |
| Absolute return shock | `abs(r1_z_100) > 2` | `fwd_abs_r5`, `fwd_abs_r10` |
| Range expansion | `hl_range_z_100 > 2` | `fwd_r3`, `fwd_r5`, `fwd_r10`, `fwd_abs_r5`, `fwd_abs_r10` |
| Range compression | `atr_ratio < 0.60` | `fwd_abs_r5`, `fwd_abs_r10`, `future_upside_10`, `future_downside_10`, `future_range_10` |
| Volume shock | `volume_z_100 > 2` | `fwd_r3`, `fwd_r5`, `fwd_abs_r5`, `fwd_abs_r10` |
| High-volume small-range | `volume_z_100 > 2 and hl_range_z_100 < 0 and body_ratio < 0.30` | `fwd_abs_r5`, `fwd_abs_r10`, `future_upside_10`, `future_downside_10` |
| Close near high | `clv > 0.80` | `fwd_r1`, `fwd_r3`, `fwd_r5` |
| Close near low | `clv < -0.80` | `fwd_r1`, `fwd_r3`, `fwd_r5` |
| Upper wick rejection | `upper_wick_ratio > 0.60` | `fwd_r1`, `fwd_r3`, `fwd_r5` |
| Lower wick rejection | `lower_wick_ratio > 0.60` | `fwd_r1`, `fwd_r3`, `fwd_r5` |
| Upside breakout | `close_t > rolling_high_20` | `fwd_r3`, `fwd_r5`, `fwd_r10` |
| Downside breakout | `close_t < rolling_low_20` | `fwd_r3`, `fwd_r5`, `fwd_r10` |
| Failed upside breakout | `high_t > rolling_high_20 and close_t < rolling_high_20` | `fwd_r3`, `fwd_r5`, `fwd_r10` |
| Failed downside breakout | `low_t < rolling_low_20 and close_t > rolling_low_20` | `fwd_r3`, `fwd_r5`, `fwd_r10` |
| Uptrend pullback | `trend_20 > 1.5 and r1_z_100 < -1` | `fwd_r3`, `fwd_r5`, `fwd_r10` |
| Downtrend pullback | `trend_20 < -1.5 and r1_z_100 > 1` | `fwd_r3`, `fwd_r5`, `fwd_r10` |

The expected output is not a guaranteed trading signal. It is an event-study result.

## 5. Compare Every Anomaly to the Baseline

Never report only the average future return after a signal.

For every target horizon:

```text
baseline_mean = mean(target over all valid rows)
event_mean = mean(target when anomaly occurs)
edge = event_mean - baseline_mean
short_edge = baseline_mean - event_mean
volatility_lift = mean(event future absolute return) / mean(baseline future absolute return)
```

Compute these metrics for every anomaly and horizon:

- event count
- baseline mean
- event mean
- edge
- event median
- hit rate
- average win
- average loss
- profit factor
- t-stat
- 5th percentile outcome
- 95th percentile outcome
- volatility lift

Interpretation rules:

- Too few events means the result is unreliable.
- Mean and median should both be checked because outliers can dominate.
- Hit rate is not enough without win/loss size.
- Profit factor below `1.0` is losing before costs.
- Profit factor from `1.0` to `1.2` is weak.
- Profit factor from `1.2` to `1.5` is potentially interesting.
- Profit factor above `1.5` is strong but must be verified carefully.
- T-stat is only a rough strength measure because financial returns are not independent and normally distributed.

## 6. Avoid Duplicate Event Distortion

If testing a 10-bar outcome and a signal fires on five consecutive candles, the forward windows overlap heavily.

Use a cooldown rule:

```text
If an event is recorded at time t, ignore new events of the same anomaly until t + horizon.
```

Report both:

- raw event result
- deduplicated event result

If a signal works only in the raw version and disappears after deduplication, be skeptical.

## 7. Run Three Robustness Checks

### Chronological Time Split

Split rows in order:

- first `60%`: research
- next `20%`: validation
- last `20%`: final test

Do not shuffle time-series rows.

Report:

```text
anomaly
horizon
research edge
validation edge
test edge
research profit factor
validation profit factor
test profit factor
verdict
```

### Threshold Stability

Test nearby thresholds. Examples:

- return shock: `abs(r1_z_100) > 1.5`, `2.0`, `2.5`
- volume shock: `volume_z_100 > 1.5`, `2.0`, `2.5`
- compression: `atr_ratio < 0.70`, `0.60`, `0.50`
- close location: `clv > 0.70`, `0.80`, `0.90`

A believable effect should be reasonably smooth. If it works only at one exact value, reject or downgrade it.

### Regime Split

Use only simple regimes:

```text
Volatility:
  low: atr_ratio < 0.75
  normal: 0.75 <= atr_ratio <= 1.25
  high: atr_ratio > 1.25

Trend:
  uptrend: trend_20 > 1.5
  downtrend: trend_20 < -1.5
  neutral: otherwise

Chop:
  choppy: efficiency_20 < 0.25
  clean directional: efficiency_20 > 0.60
  middle: otherwise
```

Report:

```text
anomaly
regime
event count
edge
hit rate
profit factor
volatility lift
```

The goal is not to force every anomaly to work everywhere. The goal is to identify where it actually works.

## 8. Test Execution Realism

If an anomaly is known only after candle `t` closes, the realistic entry is:

```text
entry = open_{t+1}
```

The informative but less conservative version is:

```text
entry = close_t
```

Report both and label them clearly.

Directional execution targets:

```text
long_realistic_return = ln(close_{t+h} / open_{t+1})
short_realistic_return = ln(open_{t+1} / close_{t+h})
```

If the edge disappears using next-bar open, the signal may not be executable.

## 9. Stress Test Costs

Test a cost range:

```text
0 bps, 1 bps, 2 bps, 5 bps, 10 bps, 20 bps, 50 bps
```

For a round trip:

```text
net_return = gross_return - 2 * cost_bps / 10000
break_even_round_trip_bps = gross_edge * 10000
```

Report:

```text
anomaly
gross edge
net edge at 1 bps
net edge at 5 bps
net edge at 10 bps
break-even cost
verdict
```

## 10. Rank Anomalies

Rank candidates by:

- event count
- edge versus baseline
- profit factor
- out-of-sample consistency
- threshold stability
- regime clarity
- cost tolerance
- realistic execution survival

Final ranking table:

```text
rank
anomaly
type
horizon
events
edge
hit rate
profit factor
volatility lift
validation result
test result
cost tolerance
verdict
```

Actual values must come from the data.

## 11. Create Alpha Cards for Survivors

Every surviving anomaly gets one concise alpha card:

```text
Name:
Data used: OHLCV only
Signal definition:
Signal timing:
Entry assumption:
Exit rule:
Alpha type: directional, volatility, path, or regime-specific
Main result:
Sample size:
Validation:
Robustness:
Failure modes:
Verdict:
```

### Verdict Rules

Use conservative labels.

`Reject` if:

- event count is too small
- edge only appears in research
- validation and test fail
- threshold result is unstable
- edge disappears with realistic entry
- costs eliminate the effect
- result depends on one or two outliers

`Watchlist` if:

- the effect is interesting but weak
- sample size is limited
- result is plausibly regime-specific
- validation is mixed
- volatility lift exists but direction is unclear

`Candidate` if:

- edge is positive versus baseline
- validation and test are directionally consistent
- threshold behavior is not fragile
- event count is reasonable
- realistic entry still works
- cost sensitivity is acceptable

`Strong candidate` only if:

- result survives research, validation, and final test
- nearby thresholds also work
- deduplicated event count is sufficient
- regime behavior is clear
- realistic execution works
- cost stress is acceptable
- result does not depend on outliers

Most anomalies should be rejected or placed on watchlist.

## Required LLM Instruction

When asked to run OHLCV alpha research, follow this instruction:

```text
You are given only OHLCV data.

Do not assume the instrument type.
Do not use external data.
Do not invent unlimited indicators.

Build the required OHLCV features.
Build future return, volatility, and path targets.
Test the fixed anomaly library.
Compare every event sample against the unconditional baseline.
Use chronological research, validation, and test splits.
Check threshold stability.
Check volatility, trend, and chop regimes.
Use deduplicated events to avoid overlapping-sample distortion.
Test realistic next-bar execution.
Stress test transaction costs.

Return:
  data quality summary
  anomaly ranking table
  robustness table
  regime table
  cost sensitivity table
  alpha cards for survivors
  rejected anomaly list
  final verdict
```

## Final Report Format

The final report must be short and structured with only these sections:

1. Data quality summary
2. Feature summary
3. Baseline future-return statistics
4. Anomaly ranking table
5. Robustness summary
6. Regime summary
7. Cost sensitivity summary
8. Alpha cards for surviving anomalies
9. Rejected anomalies and why
10. Final conclusion

## Why This Framework Exists

This framework does one thing: test whether OHLCV-visible anomalies change future behavior.

It avoids the main research mistakes:

- lookahead bias
- overfitting
- random pattern mining
- ignoring baselines
- ignoring regimes
- ignoring transaction costs
- using impossible entries
- counting overlapping events as independent
- treating every visual pattern as alpha

The framework does not say a pattern should work. It says: define the event, measure what happens next, compare it to normal, validate it, and then decide.
