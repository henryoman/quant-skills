# OHLCV Alpha Research Checklists

## Before Trusting Any Candidate

- Did every feature use only current or past OHLCV data?
- Were rolling highs/lows shifted so breakout levels exclude the current bar?
- Were z-scores and percentiles computed from prior values only?
- Were future targets kept separate from features?
- Were repeated adjacent signals de-duplicated?
- Was the baseline computed globally and inside the relevant regime?
- Did the result survive train, validation, and test periods?
- Did the result survive reasonable threshold changes?
- Did the result survive cost and delayed-entry stress?
- Were ambiguous same-bar barrier hits handled conservatively?
- Was the number of tested ideas recorded?
- Is the final rule simple enough to explain without hindsight?

## Reject Immediately

- Any signal using future data, full-sample normalization, or unshifted breakout levels.
- Any result with too few events unless it is explicitly labeled exploratory.
- Any rule that only works at one exact threshold.
- Any edge caused by one or two outlier trades.
- Any rule that is great in-sample and dead out-of-sample.
- Any strategy whose average edge is smaller than minimal plausible transaction costs.
- Any path test that assumes favorable same-bar barrier ordering without proof.
- Any result found after many hidden trials without adjustment or skepticism.

## Implementation QA

| Test | Assertion |
| --- | --- |
| OHLC consistency | `high >= open`, `high >= close`, `high >= low`, `low <= open`, `low <= close` |
| Positive prices | `open`, `high`, `low`, `close` are all positive |
| Volume nonnegative | `volume >= 0` |
| Timestamp monotonicity | timestamps are strictly increasing after deduplication |
| No future in rolling high | `rolling_high_n` at `t` equals `max(high[t-n:t-1])` |
| No future in z-score | z-score denominator uses indices `< t` |
| Target alignment | `fwd_r_h` at `t` equals `ln(close[t+h] / close[t])` |
| Feature-target separation | No target column appears in feature list |
| Cooldown logic | Consecutive event indices are `>= cooldown` apart |
| Barrier ambiguity | Events with both barriers in one bar are flagged |
| Split integrity | `max(train_time) < min(test_time)` after gap/embargo |
| Cost grid | Net returns decrease monotonically as cost increases |
