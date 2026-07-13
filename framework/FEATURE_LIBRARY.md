# OHLCV Feature Library

This is a wide feature checklist, not a request to generate everything at once.
Every feature consumes search budget. Begin with raw, scale-free facts; add a
derived indicator only if it represents a distinct hypothesis or beats its
simpler inputs out of sample.

For every feature version record:

```text
exact formula
lookback in bars and clock time
minimum history
whether current closed bar is included
past/train-only scaling reference
zero/missing behavior
expected target and sign
number of variants tried
```

## 1. Price transformations and returns

| Feature | Formula/meaning | Parameters | Best first plots | Main trap |
|---|---|---|---|---|
| simple return | `C_t/C_(t-k)-1` | lookback `k` | bin profile; lookback × horizon | comparing scales without normalization |
| log return | `ln(C_t/C_(t-k))` | `k` | distribution; lag surface | not a strategy by itself |
| open-close body return | `C_t/O_t-1` | current/lagged bars | geometry × volume heatmap | known only after close |
| close-open gap | `O_t/C_(t-1)-1` | none | gap event path | in 24/7 data may be bar construction |
| cumulative return | sum log returns over `k` | `k` | horizon surface | adjacent rows overlap heavily |
| excess return | asset minus leader/benchmark/rolling-beta component | window, beta | relative bins; event study | beta fitted on future data |
| vol-scaled return | `return/(past_sigma*sqrt(k))` | return/sigma windows | deciles; state table | tiny sigma explosion; floor it |
| percentile return | trailing/train rank | reference window | percentile profile | reference distribution drifts |

Test direction and absolute magnitude separately. A large positive past return
can predict continuation, reversal, or only future volatility.

## 2. Candle geometry

| Feature | Meaning | Parameters | Best first plots | Main trap |
|---|---|---|---|---|
| range percent | `H/L-1` or `(H-L)/prior_close` | none | range bins | bad high/low ticks |
| true range percent | range including prior-close gaps | none | target-range profile | unfinished current range |
| body fraction | `abs(C-O)/(H-L)` | epsilon | body × prior return | zero-range division |
| signed body fraction | direction × body fraction | none | signed body × volume | duplicates body return |
| upper/lower wick fraction | wick divided by range | none | wick × trend/vol | may only encode high vol |
| close position | `(C-L)/(H-L)` | none | close position × prior move | related to body/wicks |
| body location | body low/high inside range | none | taxonomy surface | threshold zoo |
| range/body ratio | range divided by body or inverse | floor/cap | path-quality profile | explodes at doji |
| inside/outside bar | current range inside/outside prior | lag/order | event path | lacks scale context |
| overlap ratio | current/prior range or body overlap | lag/order | coverage × extension | small denominator |

Use lagged geometry sequences and matched volatility/range controls before
calling a named candle pattern predictive.

## 3. Momentum and trend

Raw trend facts:

```text
multi-lookback returns
rolling linear-regression slope
slope / past volatility
fraction of positive bars
up-run/down-run length
higher-high / lower-low counts
distance above prior rolling high/low
path efficiency
```

Classical trend transforms:

| Family | Feature examples | Parameters | Must compare against |
|---|---|---|---|
| SMA/EMA/WMA | close distance, slope, curvature | length, slope lag | raw returns at same clocks |
| moving-average spread | fast/slow ratio scaled by vol | fast/slow pairs | multi-scale returns |
| crossover state | fast above/below slow; time since cross | pairs, confirmation | continuous spread; delayed entry |
| MACD-style | fast EMA − slow EMA; signal difference | fast/slow/signal | EMA spread, acceleration |
| regression trend | slope, residual scale, R² | lookback | return, path efficiency |
| DMI/ADX-style | normalized directional movement/trend strength | lookback | range, return, efficiency |
| Aroon-style | time since rolling high/low | lookback | range position |

Plots: lookback × horizon return, trend-strength × path-efficiency heatmap,
crossing event path, fold stability, and delayed-entry survival.

Traps: moving averages are delayed transforms of price; crossover fills at the
cross price are optimistic; trend strength can predict movement size without
predicting direction.

## 4. Mean reversion and oscillator families

| Family | Feature examples | Parameters | Simpler control |
|---|---|---|---|
| distance to mean | `(C-mean)/past_scale` | mean type/length, scale | raw return |
| Bollinger-style | z-score, band width, `%B` | length, band multiple | distance + volatility |
| RSI-style | smoothed positive-move share | lookback, smoothing | signed/absolute returns |
| stochastic-style | close position in prior high-low | range lookback, smoothing | causal range position |
| CCI-style | typical-price deviation from mean deviation | lookback | price z-score |
| Williams `%R`-style | inverted range position | lookback | stochastic/range position |
| detrended-price style | price minus a causal mean | lookback | mean distance |
| residual reversion | asset minus fitted leader/beta component | beta/z windows | relative return |

Test extreme score against return toward center, continued breakout, time to
mean, MFE/MAE before touch, and trend/volatility/volume regimes. The indicator
name is not a mechanism; E21 requires incremental value beyond raw inputs.

## 5. Breakout, range, and compression

| Feature | Meaning | Parameters | Plot |
|---|---|---|---|
| prior range position | close inside prior high-low | lookback | position × horizon |
| Donchian-style distance | distance beyond prior high/low | lookback | break-strength path |
| breakout retention | close location after crossing | threshold/confirm | break × retention |
| time since high/low | recency of boundary | lookback | recency bins |
| rolling range width | `(prior_high-prior_low)/close` | lookback | width vs future range |
| ATR ratio | short ATR / long ATR | short/long | compression profile |
| Bollinger bandwidth | rolling price std / mean | window | bandwidth profile |
| Keltner-style position | price relative to EMA ± ATR multiple | windows/multiple | position × vol |
| squeeze ratio | dispersion-band width / ATR-channel width | windows | squeeze × volume |
| false-break state | break then close back inside | thresholds/delay | event path |

All rolling boundaries exclude information not available at signal time.

## 6. Volatility and tail-state features

| Family | Examples | Parameters | Evaluation target |
|---|---|---|---|
| close-return vol | std, EWMA, mean/median absolute return | window/decay | future vol/range |
| range estimators | ATR, Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang-style | window | future range/vol |
| vol term structure | short/medium/long ratios | window tuples | future vol/regime |
| vol-of-vol | variability/change of volatility | outer window | shock persistence |
| jump/shock | absolute return/range z-score or tail rank | reference/threshold | future tails/decay |
| semivolatility | separate negative/positive variation | window | asymmetric risk |
| trailing skew/tails | robust higher moments/exceedance rates | window | future barrier/tails |
| drawdown state | peak loss, duration, recovery | peak window | rebound/risk |
| range efficiency | net move / path length | window | trend/chop |

Range estimators make different assumptions. Compare them; bad high/low prints
can dominate all range-based measures.

Plots: past-vol bucket versus future quantiles, predicted/realized calibration,
term-structure × volume heatmap, shock decay, and tail exceedance.

## 7. Volume and price-volume interaction

Preserve venue units. Build raw and normalized fields:

```text
raw base volume
quote/dollar volume if supplied or defensibly computed
log volume
volume / past median
volume z-score
short/long volume ratio
volume trend and acceleration
```

| Family | Meaning | Main control/trap |
|---|---|---|
| signed-volume proxy | candle sign × volume | not true aggressor side |
| OBV-style | cumulative signed volume | nonstationary; use changes/slopes |
| MFI-style | typical-price direction weighted by volume | redundant transform |
| price-volume trend | price change × volume accumulation | venue/scale dependence |
| ease-of-movement style | price movement relative to range/volume | unstable in thin bars |
| price-volume correlation | rolling return/volume-change relation | nonlinear/regime effects |
| volume concentration | recent share of trailing volume | overlapping events |
| activity intensity | volume/range, volume/vol, trades/bar | not liquidity without depth |

Test volume against future magnitude first, then direction. High volume can mean
continuation, exhaustion, churn, or merely more opportunity.

## 8. Path, serial structure, and market states

```text
positive/negative run length
sign alternation and flat-bar rate
rolling autocorrelation of returns/signs/absolute returns
variance ratio
path efficiency and choppiness
maximum drawdown/run-up and duration
time since shock, break, high, or low
rolling entropy of signs/tokens
train-fitted transition probability
state dwell time and transition surprise
change-point score
```

Plots: transition/support matrix, run-length curves, ACF/PACF by regime, entropy
× volatility, dwell times, and change score against future signal performance.

## 9. Time and recurring cycles

Use continuous encodings plus readable buckets:

```text
hour_sin, hour_cos
minute_or_bar_phase_sin, minute_or_bar_phase_cos
day_of_week
weekend flag
time since/to a scheduled venue event
month/quarter only with enough multi-year evidence
```

Known-in-advance funding, settlement, maintenance, emissions/unlocks, auctions,
or protocol events belong in asset/venue extensions.

Plot hour × weekday heatmaps for return, volatility, volume, cost when available,
and strategy net payoff. Repeat by month/fold.

## 10. Multi-timeframe representations

Do not merge a partially formed higher-timeframe bar. Use only completed bars or
trailing clock windows ending at the decision instant.

```text
short/medium/long return alignment
short/long volatility and volume ratios
lower-timeframe efficiency inside a higher-timeframe move
position within the prior higher-timeframe range
lower-timeframe shock relative to higher context
bar-phase sensitivity
```

Plot alignment state tables and short-scale × long-scale heatmaps with support.

## 11. Cross-asset and cross-venue features

After exact timestamp and quote alignment:

```text
leader returns, range, volatility, and volume shocks at t/prior lags
relative return = A return - beta * B return
relative volatility/shock
rolling beta/correlation/residual scale
raw venue basis
start-normalized log-return disagreement
feed age × disagreement
dispersion across feeds
```

Required controls: B-only features/model, same-time versus lagged information,
realistic delays, raw versus normalized basis, quote/venue/price type, official
payoff source, and missing/stale-feed behavior.

## 12. Statistical and information representations

These are diagnostics/features, not direct rules:

```text
rolling correlation/beta
ACF/PACF and variance ratio
Hurst/DFA with null calibration
spectral/wavelet power and phase stability
entropy/conditional entropy
mutual information against permutation null
train-fitted PCA/factor scores
cluster distance/probability
HMM filtered state probability
change-point likelihood/score
```

Fit dimensionality reduction, clusters, and latent states on train. Assign future
rows without future smoothing.

## 13. Sequence representations

Start simple:

```text
lagged numeric features
sign/quantile/candle-geometry tokens
n-grams and Markov orders 1, 2, 3
run-length encoding
state transition surprise
fixed-length numeric windows
```

Only then try a small CNN/RNN/transformer benchmark. Compare against aggregate
returns, state tables, and boosted trees. Report sequence length, parameter
count, training stability, and compute cost.

## 14. Feature interaction shortlist

| Pair | Question |
|---|---|
| past return × path efficiency | clean trend or noisy displacement? |
| past return × relative volume | confirmation, exhaustion, or magnitude only? |
| trend × volatility | continuation in calm versus shock? |
| mean distance × trend strength | reversion or breakout? |
| compression × range position | where might expansion leave? |
| wick/close position × prior move | rejection or random high vol? |
| short/long volatility × volume trend | opportunity expanding or dying? |
| leader move × follower lag | catch-up or divergence? |
| model score × regime | does confidence mean the same everywhere? |
| signal × cost/liquidity proxy | paper or actionable edge? |

Avoid all-pairs heatmaps without correction. A limited hypothesis-driven list is
easier to validate than thousands of accidental patterns.

## 15. Redundancy and ablation checklist

```text
[ ] Adds beyond its raw input
[ ] Not a near-copy of another lookback/indicator
[ ] Univariate shape survives time splits
[ ] Drop-family/permutation ablation shows incremental value
[ ] Effect direction and scale are stable across folds
[ ] Causal at the entry time
[ ] Survives delayed entry and costs
[ ] Can be computed and logged live if promoted
```

Prefer the smallest family that preserves most out-of-sample edge.
