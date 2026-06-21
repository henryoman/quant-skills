# First 20 OHLCV Event Studies

Use these as the initial scan. They are hypothesis tests, not trading rules.

| # | Condition | Targets | Purpose |
| --- | --- | --- | --- |
| 1 | `r1_z_100 > 2` | `fwd_r1`, `fwd_r3`, `fwd_r5` | Shock continuation/reversal |
| 2 | `r1_z_100 < -2` | `fwd_r1`, `fwd_r3`, `fwd_r5` | Shock continuation/reversal |
| 3 | `abs(r1_z_100) > 2` | `fwd_abs_r5` | Volatility after shock |
| 4 | `range_z_100 > 2` | `fwd_abs_r5`, `fwd_r5` | Range expansion effect |
| 5 | `range_pct_100 < 0.10` | `fwd_abs_r10` | Compression effect |
| 6 | `volume_z_200 > 2` | `fwd_r5`, `fwd_abs_r5` | Volume shock effect |
| 7 | `volume_z_200 > 2 and range_z_100 < 0` | `fwd_abs_r10` | Volume/range divergence |
| 8 | `volume_z_200 > 2 and body_ratio < 0.30` | `fwd_abs_r10` | Absorption-like behavior |
| 9 | `clv > 0.8` | `fwd_r3` | Close near high continuation |
| 10 | `clv < -0.8` | `fwd_r3` | Close near low continuation |
| 11 | `upper_wick_ratio > 0.60` | `fwd_r3` | Upper rejection reversal |
| 12 | `lower_wick_ratio > 0.60` | `fwd_r3` | Lower rejection reversal |
| 13 | `close > rolling_high_20` | `fwd_r5` | Upside breakout |
| 14 | `close < rolling_low_20` | `fwd_r5` | Downside breakout |
| 15 | `high > rolling_high_20 and close < rolling_high_20` | `fwd_r5` | Failed upside breakout |
| 16 | `low < rolling_low_20 and close > rolling_low_20` | `fwd_r5` | Failed downside breakout |
| 17 | `atr_ratio_20_100 < 0.6` | `fwd_abs_r10` | Volatility compression |
| 18 | `trend_score_20 > 1.5` | `fwd_r10` | Trend continuation |
| 19 | `trend_score_20 < -1.5` | `fwd_r10` | Downtrend continuation |
| 20 | `efficiency_20 < 0.2 and abs(r1_z_100) > 1.5` | `fwd_r3` | Chop mean reversion |

Required discipline:

1. Run with cooldown at least equal to the target horizon.
2. Compare each result to its baseline target distribution.
3. Run regime splits before treating a weak global result as useless.
4. Count all 20 tests in the multiple-testing burden.
5. Keep rejected tests in the research log.
