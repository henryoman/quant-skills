# Data Contract, Transformations, and Labels

This file defines the shared ground beneath every experiment. Most false alpha
starts here: a shifted timestamp, a future-filled gap, an unadjusted venue
change, a target that includes the entry bar, or a normalization fitted on the
entire sample.

## 1. Freeze the bar semantics

For each dataset record:

```text
asset_id
venue
quote_asset
bar_duration
timestamp_timezone = UTC
timestamp_semantics = bar_open | bar_close
open, high, low, close
volume
volume_unit = base | quote | contracts | unknown
bar_source = native | locally_aggregated
```

Minimum columns:

| Column | Contract |
|---|---|
| `timestamp` | timezone-aware UTC instant with declared open/close semantics |
| `open` | first valid trade/mark in the interval |
| `high` | maximum valid trade/mark in the interval |
| `low` | minimum valid trade/mark in the interval |
| `close` | last valid trade/mark in the interval |
| `volume` | nonnegative, with unit and venue declared |

Useful optional raw fields must stay labeled, not merged into anonymous
“volume”: quote volume, trade count, taker-buy volume, VWAP, spread, bid/ask,
depth, open interest, funding, index price, mark price, venue status, and raw
payload pointer.

## 2. Invariants that must pass

For valid normal bars:

```text
open > 0, high > 0, low > 0, close > 0
high >= max(open, close)
low <= min(open, close)
high >= low
volume >= 0
timestamps strictly increasing after duplicate policy
```

Report counts before and after every cleaning operation. Never silently delete
the bars that make a strategy look bad.

Audit:

- duplicate timestamps, including conflicting duplicates;
- missing expected bars and gap-length distribution;
- irregular intervals and daylight-saving mistakes;
- zero/negative prices and impossible OHLC relations;
- zero volume versus genuinely missing volume;
- isolated return/range/volume outliers;
- long flatlines and stale-feed repeats;
- symbol, venue, contract, quote, or price-scale changes;
- partial first/last bars;
- bar revisions if the source republishes history;
- whether native candles and locally aggregated candles match.

### Missing bars

Never forward-fill OHLCV and pretend a trade occurred. Choose and declare one:

1. break all rolling/sequence features across the gap;
2. insert an explicit missing-state row that cannot be traded;
3. exclude windows crossing the gap;
4. rebuild bars from raw trades when available.

## 3. Decision-time convention

Use one explicit convention per experiment. A safe close-decision example:

```text
bar t closes at T
features use bars <= t
signal becomes known after T + compute_delay
entry occurs at first executable price after T + total_delay
target starts at entry, not before it
```

With candle-only data, a conservative proxy is often:

```text
signal from closed bar t
entry at open[t+1]
exit at open[t+1+h] or close[t+h], declared in advance
```

Using `close[t]` both to create the signal and as a guaranteed fill is optimistic
unless the workflow proves the decision and fill were available before that
close.

## 4. Canonical past-only transformations

Let `C_t`, `O_t`, `H_t`, and `L_t` be the current closed candle.

### Returns

```text
simple_return(k) = C_t / C_(t-k) - 1
log_return(k)    = ln(C_t) - ln(C_(t-k))
body_return      = C_t / O_t - 1
range_pct        = H_t / L_t - 1
```

Use log returns for additive comparisons and cross-feed normalization. Preserve
raw prices and quote labels alongside normalized returns.

### Candle geometry

```text
range       = H_t - L_t
body        = abs(C_t - O_t)
upper_wick  = H_t - max(O_t, C_t)
lower_wick  = min(O_t, C_t) - L_t
body_frac   = body / max(range, epsilon)
upper_frac  = upper_wick / max(range, epsilon)
lower_frac  = lower_wick / max(range, epsilon)
close_pos   = (C_t - L_t) / max(range, epsilon)
```

For near-zero range, use an explicit flat/doji state. Do not let division noise
create giant ratios.

### Rolling scale

Fit only on bars available before or at the decision time:

```text
past_sigma(w) = std(r_(t-w) ... r_(t-1))
z_t           = (x_t - past_mean_w) / max(past_std_w, epsilon)
percentile_t  = rank x_t against a trailing or train-only reference window
```

Shift rolling estimates when their implementation would otherwise include the
current value in a way inconsistent with the decision clock.

### Volatility and path

Test several objects; they are not interchangeable:

```text
realized_vol(w) = std(past one-bar returns)
mean_abs_move(w) = mean(abs(past returns))
ATR_pct(w) = mean(true_range / prior_close)
Parkinson-like range variance = mean((ln(H/L))^2) / (4 ln 2)
path_efficiency(w) = abs(C_t - C_(t-w)) / sum(abs(C_i - C_(i-1)))
choppiness_proxy = 1 - path_efficiency
```

### Volume

Keep both raw and normalized versions:

```text
log_volume
volume / trailing_median_volume
volume_z
quote_volume
dollar_or_quote_volume_z
short_volume_mean / long_volume_mean
```

Cross-venue raw volume is usually not directly comparable. A venue-relative
percentile or z-score can be comparable only after checking how each venue
defines volume.

## 5. Label library

All future windows start after the chosen entry instant. Let `P_0` be the proxy
entry price and horizon `h` contain future bars `1..h`.

### L01: close-to-close or entry-to-exit return

```text
future_return_h = P_exit / P_0 - 1
```

Use for directional payoff, regression, and signed strategy return. Declare
whether `P_exit` is a future open, close, VWAP, bid, or ask.

### L02: direction with a deadband

```text
up      if future_return_h > +band_t
neutral if abs(future_return_h) <= band_t
down    if future_return_h < -band_t
```

Candidate bands:

- fixed basis points;
- a multiple of past-only volatility times `sqrt(h)`;
- estimated round-trip costs plus a safety margin;
- train-only quantiles.

The band is a parameter and must be trained/frozen, not chosen from test.

### L03: future absolute move and realized volatility

```text
future_abs_return_h = abs(future_return_h)
future_realized_vol_h = std(future one-bar returns 1..h)
future_quadratic_variation_h = sum(future log_return_i^2)
```

These answer whether the market will move, not which direction.

### L04: maximum favorable/adverse excursion

For a long orientation:

```text
MFE_h = max(H_1..H_h) / P_0 - 1
MAE_h = min(L_1..L_h) / P_0 - 1
```

For a short, reverse signs consistently. MFE/MAE exposes path risk hidden by the
final close.

### L05: future range and directional range

```text
upside_h   = max(H_1..H_h) / P_0 - 1
downside_h = min(L_1..L_h) / P_0 - 1
total_range_h = upside_h - downside_h
```

This supports breakout, stop/target, liquidity-range, and volatility studies.

### L06: barrier and triple-barrier outcome

With upper `+u`, lower `-d`, and time horizon `h`:

```text
+1 = upper touched first
-1 = lower touched first
 0 = neither before the time barrier
```

If both are inside the same candle, OHLC cannot tell which occurred first. Mark
it `ambiguous`, use lower-timeframe data, or apply a declared conservative rule.
Do not choose the favorable order.

### L07: time to event

```text
bars_to_upper
bars_to_lower
bars_to_exit_range
bars_to_recover_drawdown
```

Right-censor events that do not happen inside the observation window. Survival
analysis is more honest than assigning a fake time.

### L08: path efficiency and choppiness

```text
future_efficiency_h = abs(P_h - P_0) / sum(abs(P_i - P_(i-1)))
future_choppiness_h = 1 - future_efficiency_h
```

Useful for trend-following viability, stop placement, and deciding whether a
directional prediction is likely to arrive cleanly.

### L09: drawdown and run-up

```text
future_max_drawdown_h = minimum peak-to-trough return in path 0..h
future_max_runup_h = maximum trough-to-peak return in path 0..h
```

These are closer to risk than terminal return.

### L10: distribution/quantile label

Predict conditional quantiles of future return, upside, downside, or range:

```text
Q05, Q25, Q50, Q75, Q95
```

Quantiles are more useful than a single mean when tails and asymmetry matter.

### L11: regime label

Examples: future volatility bucket, trend/chop bucket, or latent state. Fit
bucket cutoffs or clustering on training only. Use regime labels mainly to
route/gate strategies; do not assume a cluster is tradable by itself.

### L12: cross-asset/venue response

For a leader `A` and traded asset `B`:

```text
feature = A information at or before t
label   = B return/range/volatility after t
```

Same-time correlation is not lead-lag evidence. Align timestamps, bar clocks,
quote assets, venue latency, and missing bars before testing.

## 6. Overlap and effective sample size

If a new signal appears every bar but each label spans `h` bars, adjacent labels
share future prices. Treating them as independent inflates significance.

Use one or more:

- non-overlapping decision rows (`every h bars`);
- event-based sampling;
- purged splits and embargo;
- heteroskedasticity/autocorrelation-consistent uncertainty;
- moving-block or stationary bootstrap;
- cluster uncertainty by day/session/event.

Always report both raw row count and effective/non-overlapping count.

## 7. Split contract

Minimum chronological partition:

```text
train: fit transformations, bins, features, models
validation: choose a small number of thresholds/rules
test: report once, never retune
```

Preferred final check: rolling or expanding walk-forward folds with purge and
embargo sized to the maximum lookback, forecast horizon, and holding period.

Freeze and persist:

- UTC boundaries;
- row counts;
- maximum feature lookback;
- maximum label horizon;
- purge and embargo lengths;
- all train-fitted statistics;
- any rows removed and why.

## 8. Dataset outputs

A derived research dataset should be replayable without contaminating canonical
raw data. Recommended logical groups:

```text
keys: timestamp, asset_id, venue, quote_asset, row_id
base: OHLCV and bar metadata
quality: gap/outlier/staleness flags
features: causal numeric values
states: train-fitted bins/tokens/clusters
labels: future outcomes and ambiguity flags
splits: train/valid/test/fold assignments
```

Use Parquet for repeated scans, JSON for manifests/configs/summaries, JSONL for
append-only live observations, and CSV only for quick inspection/export.
