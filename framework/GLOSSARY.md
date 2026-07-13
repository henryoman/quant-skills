# Plain-Language Glossary and Formula Map

## Core terms

**Feature** — a fact known at the decision time, such as past return, relative
volume, or candle close position.

**Label/target** — a precisely defined future outcome, such as next-10-bar
return, future range, or which barrier was touched first.

**Signal** — a feature or model output used to rank, gate, or choose an action.

**Prediction** — an estimate of a future value/probability. It can be accurate
but too small to trade after costs.

**Edge** — conditional future behavior different enough from the baseline to
create positive expected net payoff.

**Alpha** — edge that survives unseen time, costs, implementation, and plausible
alternative explanations.

**Regime** — a recurring market condition in which distributions or signal
performance differ, such as high volatility or trend/chop.

**State** — a compact discrete description of the current feature values.

**Coverage/exposure** — fraction of eligible time that the signal trades or
holds risk.

**Turnover** — amount the position changes. Higher turnover usually increases
fees and slippage.

**Fillability** — whether the actual quoted book/liquidity could execute the
stated side, size, and timing.

## Return and basis-point formulas

```text
simple return = end / start - 1
log return = ln(end / start)
basis points = return * 10,000
1 bp = 0.01%
100 bps = 1%
```

Log returns add across time. Start-normalized log returns are usually safer than
raw price-level comparisons across feeds with different construction/basis.

## Conditional lift

For a binary outcome:

```text
base probability = P(Y=1)
conditional probability = P(Y=1 | state S)
absolute lift = conditional - base
relative lift = conditional / base - 1
```

For a continuous payoff:

```text
conditional excess = E[Y | S] - E[Y]
```

Use net payoff when judging tradability.

## Expected value

For simple win/loss outcomes:

```text
EV = P(win) * average_win
   - P(loss) * average_loss
   - average_cost
```

The sign of EV, not hit rate alone, determines whether the simplified trade is
attractive.

## Volatility and range

```text
realized volatility = standard deviation of returns over a declared window
absolute movement = abs(return)
range = high - low
true range = max(high-low, abs(high-prior_close), abs(low-prior_close))
ATR = rolling mean of true range
```

Volatility measures dispersion/path variation. Range measures extremes. They
can rank regimes differently.

## Z-score and percentile

```text
z = (current - past_mean) / past_std
percentile = rank of current inside a past/train reference distribution
```

Both depend on the reference window. Fit it using past/training data only.

## Correlation, autocorrelation, and lead-lag

**Correlation** measures co-movement, usually linearly. Same-time correlation
does not imply that one series predicts the other.

**Autocorrelation** measures how a series relates to its own past values.

**Lead-lag** requires information from series A available at `t` to improve a
forecast of series B strictly after `t`, after alignment and latency.

## Entropy and mutual information

**Entropy** measures uncertainty in an outcome distribution. Lower conditional
entropy means outcomes are more concentrated in that state.

```text
information gain = H(Y) - H(Y | X)
```

**Mutual information** can detect nonlinear dependence, but it does not reveal
direction, profitability, or causal order by itself.

## Calibration and ranking

**Ranking/discrimination** asks whether higher scores correspond to more
positive outcomes.

**Calibration** asks whether stated probabilities match frequencies. Among all
`0.60` predictions, about 60% should occur.

Both matter. A model can rank well and be badly calibrated.

## Common metrics

```text
accuracy = correct classes / all classes
precision = true positives / predicted positives
recall = true positives / actual positives
Brier = mean((predicted_probability - outcome)^2)
MAE = mean(abs(prediction - actual))
RMSE = sqrt(mean((prediction - actual)^2))
profit factor = gross wins / abs(gross losses)
max drawdown = largest peak-to-trough equity decline
Sharpe-like = mean return / standard deviation of return
Sortino-like = mean return / downside deviation
```

Annualized metrics require enough time and a disclosed frequency/dependence
assumption.

## Bias and overfitting terms

**Lookahead leakage** — future information enters features or execution.

**Selection bias** — only winners are reported after many trials.

**Survivorship bias** — only assets/venues that survived or are currently
visible are included.

**Data snooping** — repeated analysis makes the “holdout” part of training by
human memory.

**Overfitting** — a rule learns historical noise and fails in future data.

**Purging** — removes training rows whose label/holding intervals overlap an
evaluation interval.

**Embargo** — extra buffer separating evaluation and reusable training data.

**Walk-forward** — repeatedly trains on past data and tests on the next unseen
block.

## Evidence words

Use these literally:

```text
descriptive: pattern observed
proxy_only: candle backtest with assumptions
paper_traded: forward decisions, no capital
fillable: captured quotes/depth support size
settlement_backed: official outcome reconciled
live_small: real small-risk execution
```
