# OHLCV Anomaly Report Template

```text
Anomaly name:
Signal formula:
Feature definitions:
Lookbacks:
Thresholds tested:
Target horizons tested:
Event de-duplication rule:
Sample period:
Train/validation/test split:

Global event results:
    n, mean edge, median edge, hit rate, profit factor, p05, p95

Regime results:
    volatility regimes
    trend regimes
    efficiency/chop regimes
    volume regimes

Path results:
    MFE, MAE, barrier-first probabilities, ambiguous-bar rate

Robustness:
    nearby thresholds
    nearby lookbacks
    alternative horizons
    delayed entry
    cost grid

Multiple-testing note:
    number of related trials attempted
    adjustment or conservative criteria used

Verdict:
    Reject / Watchlist / Directional alpha candidate / Volatility alpha candidate / Needs more data

Reasoning:
    Why the result may exist, why it may fail, and what would invalidate it.
```

## Verdict Standards

`Reject`: leakage, too few events, one-threshold behavior, outlier-dominated mean, dead validation, or cost fragility.

`Watchlist`: plausible pattern with incomplete sample size, weak validation, or missing path/cost checks.

`Directional alpha candidate`: direction target improves out of sample, median/hit/path metrics support the mean, and cost stress is plausible.

`Volatility alpha candidate`: future absolute return or future range lift is stable, even if directional return is flat.

`Needs more data`: concept is coherent but event count or regime coverage is insufficient.
