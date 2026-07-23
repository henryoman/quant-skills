# OHLCV Feature Math Reference

One asset. Price in USD. One fixed candle interval.

Every feature below states:

- **Input:** numbers used.
- **Math:** exact calculation.
- **Output:** number produced.
- **Scale:** units and normal range.
- **Relative form:** usable across assets, prices, and dates.
- **Log form:** whether log math works and how.

## 0. Symbols

For candle `t`:

| Symbol | Input |
|---|---|
| `O_t` | Open price, USD |
| `H_t` | High price, USD |
| `L_t` | Low price, USD |
| `C_t` | Close price, USD |
| `V_t` | Volume, asset units |
| `n` | Lookback, candles |
| `HH_t(n)` | Highest `H` in the last `n` candles |
| `LL_t(n)` | Lowest `L` in the last `n` candles |
| `mean_n(x)` | Mean of the last `n` values of `x` |
| `median_n(x)` | Median of the last `n` values of `x` |
| `sd_n(x)` | Sample standard deviation of the last `n` values of `x` |
| `ln(x)` | Natural logarithm |
| `eps` | Small positive number used only to prevent division by zero |

Requirements:

- Prices must be positive for log math.
- Candles must use equal time intervals.
- Missing candles must be marked. Do not silently treat missing candles as zero volume and unchanged price.
- Every rolling feature must use only data available at candle `t`. Never use future candles.

## 1. Scale rules

| Form | Example | Output | Cross-asset use |
|---|---|---:|---|
| Dollar | `C_t - C_(t-n)` | USD | Bad |
| Simple relative | `C_t / C_(t-n) - 1` | Decimal return | Good |
| Percent | `100 * relative` | Percent | Good |
| Log relative | `ln(C_t / C_(t-n))` | Log return | Good |
| Standardized | `(x_t - mean) / sd` | Standard deviations | Good |
| Percentile | Historical rank of `x_t` | `0` to `1` | Good |

Use decimal returns inside code. Example: `0.05 = 5%`.

Default rule:

1. Use **log ratios** for price changes, trend slopes, volatility, and additive time aggregation.
2. Use **simple percentages** for reports and direct P&L interpretation.
3. Use **ratios, z-scores, or percentiles** for volume and other positive quantities.
4. Keep raw USD forms only when actual dollar movement matters.

---

# A. Price change and direction

## 2. Dollar change

- **Input:** `C_t`, `C_(t-n)`.
- **Math:** `delta_C = C_t - C_(t-n)`.
- **Output:** signed price change.
- **Scale:** USD; `(-infinity, +infinity)`.
- **Relative form:** `C_t / C_(t-n) - 1`.
- **Log form:** `ln(C_t / C_(t-n))`.
- **Use:** execution dollars only. Prefer return for modeling.

## 3. Simple return

- **Input:** `C_t`, `C_(t-n)`.
- **Math:** `r_t(n) = C_t / C_(t-n) - 1`.
- **Output:** signed decimal return.
- **Scale:** relative; minimum `-1`; no upper limit.
- **Relative form:** already relative.
- **Log form:** `g_t(n) = ln(C_t / C_(t-n))`.
- **Example:** `105 / 100 - 1 = 0.05 = 5%`.

## 4. Log return

- **Input:** `C_t`, `C_(t-n)`.
- **Math:** `g_t(n) = ln(C_t / C_(t-n))`.
- **Output:** signed log return.
- **Scale:** dimensionless; `(-infinity, +infinity)`.
- **Relative form:** already relative.
- **Simple-percent form:** `exp(g_t(n)) - 1`.
- **Key property:** adjacent log returns add.
- **Example:** `ln(105 / 100) = 0.04879`; simple return is `exp(0.04879)-1 = 5%`.

## 5. Momentum

- **Input:** `C_t`, `C_(t-n)`.
- **Math:** use `r_t(n)` or `g_t(n)`.
- **Output:** return over lookback `n`.
- **Scale:** relative.
- **Relative form:** `C_t / C_(t-n) - 1`.
- **Log form:** preferred: `ln(C_t / C_(t-n))`.
- **Note:** momentum is not new math. It is a return with a chosen lookback.

## 6. Acceleration

- **Input:** two adjacent, equal-length returns.
- **Math:** `accel_t(n) = g_t(n) - g_(t-n)(n)`.
- **Output:** change in momentum.
- **Scale:** log-return difference; dimensionless.
- **Relative form:** simple alternative: `r_t(n) - r_(t-n)(n)`.
- **Log form:** preferred formula above.
- **Sign:** positive = latest move is more upward, or less downward.

## 7. Positive-return fraction

- **Input:** one-candle returns `g_i(1)` for last `n` candles.
- **Math:** `up_frac = count(g_i(1) > 0) / n`.
- **Output:** fraction of rising closes.
- **Scale:** relative; `[0, 1]`.
- **Relative form:** already relative.
- **Log form:** use log returns for sign; simple returns give same sign.
- **Companion:** `down_frac = count(g_i(1) < 0) / n`.

## 8. Up/down streak

- **Input:** signs of consecutive one-candle returns.
- **Math:** count consecutive positive or negative returns ending at `t`.
- **Output:** signed integer. Example: `+4` or `-3`.
- **Scale:** candles; not relative.
- **Relative form:** `abs(streak) / n_max` if a bounded value is required.
- **Log form:** not applicable. Log returns may supply the signs.

---

# B. Moving baselines and trend

## 9. Simple moving average: SMA

- **Input:** closes `C_(t-n+1)` through `C_t`.
- **Math:** `SMA_t(n) = mean_n(C)`.
- **Output:** average price.
- **Scale:** USD; not relative.
- **Relative form:** do not compare raw SMA values. Use price distance or SMA slope below.
- **Log form:** geometric mean price: `exp(mean_n(ln(C)))`.
- **Note:** geometric mean is consistent with log returns.

## 10. Exponential moving average: EMA

- **Input:** `C_t`, previous `EMA`, smoothing `alpha`.
- **Math:** `EMA_t = alpha*C_t + (1-alpha)*EMA_(t-1)`.
- **Parameter:** common `alpha = 2/(n+1)`.
- **Output:** smoothed price.
- **Scale:** USD; not relative.
- **Relative form:** use EMA distance or EMA slope.
- **Log form:** run EMA on `ln(C)`, then exponentiate if a USD price is needed.

## 11. Price distance from baseline

- **Input:** `C_t`, baseline `B_t`; `B` may be SMA, EMA, or VWAP.
- **Math, simple:** `dist = C_t / B_t - 1`.
- **Math, log:** `log_dist = ln(C_t / B_t)`.
- **Output:** signed distance from baseline.
- **Scale:** relative.
- **Relative form:** already relative.
- **Log form:** preferred for symmetry and modeling.
- **Example:** `110 / 100 - 1 = 10%`.

## 12. Baseline slope

- **Input:** baseline now `B_t`, baseline `k` candles ago `B_(t-k)`.
- **Math, simple:** `slope = (B_t / B_(t-k) - 1) / k`.
- **Math, log:** `log_slope = ln(B_t / B_(t-k)) / k`.
- **Output:** average baseline change per candle.
- **Scale:** relative per candle.
- **Relative form:** already relative.
- **Log form:** preferred.

## 13. Fast/slow baseline spread

- **Input:** fast baseline `F_t`; slow baseline `S_t`.
- **Math, simple:** `spread = F_t / S_t - 1`.
- **Math, log:** `log_spread = ln(F_t / S_t)`.
- **Output:** signed relative separation.
- **Scale:** relative.
- **Relative form:** already relative.
- **Log form:** preferred.
- **MACD:** raw MACD is `EMA_fast - EMA_slow` in USD. `ln(EMA_fast/EMA_slow)` is the portable version.

## 14. Linear trend slope

- **Input:** `y_i = ln(C_i)` for last `n` candles; time index `x_i = 0,1,...,n-1`.
- **Math:** fit `y_i = a + b*x_i` by ordinary least squares.
- **Output:** coefficient `b`.
- **Scale:** log return per candle.
- **Relative form:** already relative.
- **Log form:** required and preferred.
- **Convert:** expected simple return per candle is `exp(b)-1`.

## 15. Trend fit: R-squared

- **Input:** observed `ln(C_i)` and fitted trend values from Feature 14.
- **Math:** `R2 = 1 - sum((y_i-yhat_i)^2) / sum((y_i-mean(y))^2)`.
- **Output:** straight-line fit quality.
- **Scale:** usually `[0,1]` when an intercept is used.
- **Relative form:** already scale-free.
- **Log form:** calculate on log prices.
- **Meaning:** `1` = exact line; `0` = line explains none of the variation.

## 16. Path efficiency ratio

- **Input:** one-candle log returns over `n` candles.
- **Math:** `ER = abs(sum(g_i(1))) / sum(abs(g_i(1)))`.
- **Output:** direct movement divided by total movement.
- **Scale:** relative; `[0,1]`.
- **Relative form:** already relative.
- **Log form:** preferred formula above.
- **Meaning:** `1` = straight path; `0` = movement canceled itself.

## 17. Return autocorrelation

- **Input:** one-candle log returns over `n` candles and lag `k`.
- **Math:** Pearson correlation between `g_i(1)` and `g_(i-k)(1)`.
- **Output:** serial correlation.
- **Scale:** relative; `[-1,1]`.
- **Relative form:** already relative.
- **Log form:** use log returns.
- **Lag:** `k=1` compares each return with the prior return.

---

# C. Range and volatility

## 18. Candle high-low range

- **Input:** `H_t`, `L_t`.
- **Math, USD:** `range_usd = H_t - L_t`.
- **Math, relative:** `range_rel = (H_t - L_t) / C_(t-1)`.
- **Math, log:** `range_log = ln(H_t / L_t)`.
- **Output:** intrabar price span.
- **Scale:** use relative or log form across assets.
- **Log form:** best portable form when prices are positive.

## 19. True range

- **Input:** `H_t`, `L_t`, `C_(t-1)`.
- **Math, USD:** `TR = max(H_t-L_t, abs(H_t-C_(t-1)), abs(L_t-C_(t-1)))`.
- **Math, relative:** divide each candidate by `C_(t-1)` before taking the maximum.
- **Math, log:** `TR_log = max(ln(H_t/L_t), abs(ln(H_t/C_(t-1))), abs(ln(L_t/C_(t-1))))`.
- **Output:** full candle movement including gaps.
- **Scale:** use relative or log form.
- **Log form:** preferred portable form.

## 20. Average True Range: ATR

- **Input:** true ranges from last `n` candles.
- **Math, USD:** `ATR = mean_n(TR)`.
- **Math, relative:** `ATR_rel = mean_n(TR_rel)`.
- **Math, log:** `ATR_log = mean_n(TR_log)`.
- **Output:** average movement per candle.
- **Scale:** `ATR` is USD; `ATR_rel` and `ATR_log` are portable.
- **Preferred:** average normalized true ranges. Do not normalize only after averaging when price changed greatly inside the window.

## 21. Close-to-close volatility

- **Input:** one-candle log returns `g_i(1)` over last `n` candles.
- **Math:** `vol_t(n) = sd_n(g(1))`.
- **Output:** typical dispersion of one-candle returns.
- **Scale:** log return per candle; nonnegative.
- **Relative form:** already relative.
- **Log form:** required and preferred.
- **Annualization:** multiply by `sqrt(candles_per_year)` only when needed.

## 22. Downside and upside volatility

- **Input:** one-candle log returns over `n` candles.
- **Math:**
  - `down_vol = sqrt(mean(min(g_i,0)^2))`
  - `up_vol = sqrt(mean(max(g_i,0)^2))`
- **Output:** downward and upward semideviation.
- **Scale:** log return per candle; nonnegative.
- **Relative form:** already relative.
- **Log form:** use log returns.
- **Ratio:** `down_vol / (up_vol + eps)`; use `ln((down_vol+eps)/(up_vol+eps))` for a symmetric log ratio.

## 23. Short/long volatility ratio

- **Input:** short volatility `vol_s`; long volatility `vol_l`.
- **Math:** `vol_ratio = vol_s / (vol_l + eps)`.
- **Output:** current volatility relative to baseline volatility.
- **Scale:** positive ratio; `1` = equal.
- **Relative form:** already relative.
- **Log form:** `ln((vol_s+eps)/(vol_l+eps))`; `0` = equal.
- **Works with:** log-return volatility, ATR relative, or log range. Do not mix types.

## 24. Rolling range width

- **Input:** `HH_t(n)`, `LL_t(n)`.
- **Math, simple:** `width = HH_t(n) / LL_t(n) - 1`.
- **Math, log:** `log_width = ln(HH_t(n) / LL_t(n))`.
- **Output:** full high-low width over `n` candles.
- **Scale:** relative; nonnegative.
- **Relative form:** already relative.
- **Log form:** preferred.

## 25. Compression or expansion ratio

- **Input:** short-window width or volatility `X_s`; long-window value `X_l`.
- **Math:** `ratio = X_s / (X_l + eps)`.
- **Output:** recent activity divided by normal activity.
- **Scale:** positive ratio.
- **Relative form:** already relative.
- **Log form:** `ln((X_s+eps)/(X_l+eps))`.
- **Meaning:** below `1` = compression; above `1` = expansion.

---

# D. Range position, breakouts, and loss from peak

## 26. Position inside rolling range

- **Input:** `C_t`, `HH_t(n)`, `LL_t(n)`.
- **Math:** `pos = (C_t - LL_t(n)) / (HH_t(n) - LL_t(n))`.
- **Output:** close location inside rolling high-low range.
- **Scale:** normally `[0,1]`.
- **Relative form:** already relative.
- **Log form:** optional: `(ln(C_t)-ln(LL))/(ln(HH)-ln(LL))`.
- **Zero-width rule:** output missing if `HH = LL`.
- **Stochastic:** this is the core Stochastic `%K` calculation.

## 27. Breakout distance

- **Input:** `C_t`; prior rolling high `HH_(t-1)(n)` or low `LL_(t-1)(n)`.
- **Math, upper:** `upper_break = C_t / HH_(t-1)(n) - 1`.
- **Math, lower:** `lower_break = C_t / LL_(t-1)(n) - 1`.
- **Output:** signed distance from the old boundary.
- **Scale:** relative.
- **Relative form:** already relative.
- **Log form:** `ln(C_t/HH_prior)` or `ln(C_t/LL_prior)`.
- **Important:** exclude candle `t` from the boundary. Otherwise the feature leaks its own high/low into the test.

## 28. Drawdown from rolling peak

- **Input:** `C_t`, prior or current rolling peak `P_t = max(C)` over chosen history.
- **Math, simple:** `DD = C_t / P_t - 1`.
- **Math, log:** `DD_log = ln(C_t / P_t)`.
- **Output:** loss from peak.
- **Scale:** simple drawdown `[-1,0]`; log drawdown `(-infinity,0]`.
- **Relative form:** already relative.
- **Log form:** preferred for modeling.

## 29. Recovery from rolling trough

- **Input:** `C_t`, trough `T_t = min(C)` since a chosen start or peak.
- **Math, simple:** `recovery = C_t / T_t - 1`.
- **Math, log:** `recovery_log = ln(C_t / T_t)`.
- **Output:** gain from trough.
- **Scale:** nonnegative when current close is above trough.
- **Relative form:** already relative.
- **Log form:** preferred.

## 30. Time since high or low

- **Input:** locations of `HH_t(n)` and `LL_t(n)`.
- **Math:** `age_high = t - argmax(H)`; `age_low = t - argmin(L)`.
- **Output:** candle count.
- **Scale:** integer; `[0,n-1]`.
- **Relative form:** divide by `n-1` to obtain `[0,1]`.
- **Log form:** not needed.

---

# E. Single-candle shape

## 31. Signed candle body

- **Input:** `O_t`, `C_t`.
- **Math, USD:** `body = C_t - O_t`.
- **Math, relative:** `body_rel = C_t / O_t - 1`.
- **Math, log:** `body_log = ln(C_t / O_t)`.
- **Output:** open-to-close movement.
- **Scale:** use relative or log form across assets.
- **Log form:** preferred.

## 32. Body fraction of candle range

- **Input:** `O_t`, `H_t`, `L_t`, `C_t`.
- **Math:** `body_frac = abs(C_t-O_t) / (H_t-L_t)`.
- **Output:** fraction of candle range occupied by body.
- **Scale:** `[0,1]` for valid OHLC data.
- **Relative form:** already relative.
- **Log form:** optional log-price version: `abs(ln(C/O)) / ln(H/L)`.
- **Zero-range rule:** output missing when `H = L`.

## 33. Upper and lower wick fractions

- **Input:** `O_t`, `H_t`, `L_t`, `C_t`.
- **Math:**
  - `upper = H_t - max(O_t,C_t)`
  - `lower = min(O_t,C_t) - L_t`
  - `upper_frac = upper / (H_t-L_t)`
  - `lower_frac = lower / (H_t-L_t)`
- **Output:** two wick fractions.
- **Scale:** each `[0,1]`.
- **Relative form:** already relative after division by range.
- **Log form:** optional; calculate all distances in log-price space.
- **Zero-range rule:** output missing when `H = L`.

## 34. Close location inside candle

- **Input:** `C_t`, `H_t`, `L_t`.
- **Math:** `CLV = (C_t-L_t) / (H_t-L_t)`.
- **Output:** close position within the candle.
- **Scale:** `[0,1]`.
- **Relative form:** already relative.
- **Log form:** optional: `(ln(C)-ln(L)) / (ln(H)-ln(L))`.
- **Zero-range rule:** output missing when `H = L`.

## 35. Opening gap

- **Input:** `O_t`, `C_(t-1)`.
- **Math, simple:** `gap = O_t / C_(t-1) - 1`.
- **Math, log:** `gap_log = ln(O_t / C_(t-1))`.
- **Output:** signed gap from prior close.
- **Scale:** relative.
- **Relative form:** already relative.
- **Log form:** preferred.

---

# F. Volume and OHLCV liquidity proxies

## 36. Volume change

- **Input:** `V_t`, `V_(t-n)`.
- **Math, ratio:** `vol_change = V_t / V_(t-n) - 1`.
- **Math, log:** `vol_log_change = ln((V_t+eps)/(V_(t-n)+eps))`.
- **Output:** volume growth.
- **Scale:** relative.
- **Relative form:** ratio is relative.
- **Log form:** preferred when volume is highly skewed; `eps` rule must be fixed globally.

## 37. Relative volume

- **Input:** `V_t`; prior rolling mean or median volume `B_V`.
- **Math:** `RVOL = V_t / (B_V + eps)`.
- **Output:** current volume divided by normal volume.
- **Scale:** positive ratio; `1` = normal.
- **Relative form:** already relative.
- **Log form:** `ln((V_t+eps)/(B_V+eps))`; `0` = normal.
- **Leak rule:** build `B_V` from candles ending at `t-1` if the current candle is being tested against prior normal.
- **Robust option:** use median because volume spikes distort the mean.

## 38. Approximate dollar volume

- **Input:** asset-unit volume `V_t`; representative price `P_t`.
- **Math:** `DV_t = V_t * P_t`.
- **Price choice:** `P_t = (H_t+L_t+C_t)/3` or `(O_t+H_t+L_t+C_t)/4`.
- **Output:** approximate USD traded.
- **Scale:** USD; not relative.
- **Relative form:** `DV_t / median_prior_n(DV)`.
- **Log form:** `ln(DV_t+eps)` or log relative dollar volume.
- **Warning:** exact dollar volume needs individual trades. Candle OHLCV gives an approximation.

## 39. Price movement per dollar volume: illiquidity proxy

- **Input:** absolute log return `abs(g_t(1))`; dollar volume `DV_t`.
- **Math:** `ILLIQ_t = abs(g_t(1)) / (DV_t + eps)`.
- **Output:** price movement per USD traded.
- **Scale:** inverse USD; positive; raw values are tiny.
- **Relative form:** divide by its rolling median, take a z-score, or take a percentile rank.
- **Log form:** `ln(abs(g_t(1))+eps) - ln(DV_t+eps)`.
- **Warning:** proxy only. Not actual order-book depth or trade impact.

## 40. Signed-volume balance

- **Input:** one-candle return signs and volume over `n` candles.
- **Math:** `balance = sum(sign(g_i(1))*V_i) / sum(V_i)`.
- **Output:** volume-weighted direction balance.
- **Scale:** relative; `[-1,1]`.
- **Relative form:** already relative.
- **Log form:** not needed.
- **OBV relation:** raw OBV cumulatively adds signed volume. This normalized form is portable and bounded.

## 41. Up-volume/down-volume ratio

- **Input:** volumes labeled by one-candle return sign over `n` candles.
- **Math:**
  - `UV = sum(V_i where g_i > 0)`
  - `DV = sum(V_i where g_i < 0)`
  - `ratio = (UV+eps)/(DV+eps)`
- **Output:** positive-volume participation divided by negative-volume participation.
- **Scale:** positive ratio; `1` = equal.
- **Relative form:** already relative.
- **Log form:** `ln((UV+eps)/(DV+eps))`; `0` = equal.
- **Warning:** not true buyer and seller volume. OHLCV lacks trade aggressor labels.

## 42. Rolling candle VWAP approximation

- **Input:** representative price `P_i` and volume `V_i` over `n` candles.
- **Math:** `VWAP = sum(P_i*V_i) / sum(V_i)`.
- **Output:** volume-weighted average price.
- **Scale:** USD; not relative.
- **Relative form:** `C_t/VWAP - 1`.
- **Log form:** `ln(C_t/VWAP)`.
- **Warning:** candle VWAP is approximate. Exact VWAP needs trade-level price and size.

## 43. Price-volume correlation

- **Input:** log returns `g_i(1)` and transformed volume `u_i = ln(V_i+eps)` over `n` candles.
- **Math:** Pearson correlation `corr(g,u)`.
- **Output:** signed return-volume relationship.
- **Scale:** relative; `[-1,1]`.
- **Relative form:** already relative.
- **Log form:** use log return and log volume.
- **Second version:** `corr(abs(g),u)` measures movement-size versus volume, ignoring direction.

---

# G. Standardization and bounded oscillators

## 44. Rolling z-score

- **Input:** current feature `x_t`; prior mean `mu`; prior standard deviation `s` over `n` candles.
- **Math:** `z = (x_t-mu)/(s+eps)`.
- **Output:** distance from normal in standard deviations.
- **Scale:** standardized; unbounded.
- **Relative form:** already scale-free.
- **Log form:** if `x` is positive and skewed, first use `ln(x+eps)`, then z-score it.
- **Good inputs:** log price distance, log return, log volume, log range, relative ATR.
- **Leak rule:** use prior window ending at `t-1` when testing whether `x_t` is unusual.

## 45. Rolling percentile rank

- **Input:** `x_t` and prior `n` observations.
- **Math:** `pct_rank = count(x_i <= x_t) / n`.
- **Output:** historical rank.
- **Scale:** relative; `[0,1]`.
- **Relative form:** already scale-free.
- **Log form:** unnecessary because monotonic log transforms preserve rank.
- **Benefit:** stable with skewed data and extreme outliers.

## 46. RSI using relative returns

- **Input:** one-candle log returns `g_i` over `n` candles.
- **Math:**
  - `gain_i = max(g_i,0)`
  - `loss_i = max(-g_i,0)`
  - `AG = mean_n(gain)`
  - `AL = mean_n(loss)`
  - `RS = AG/(AL+eps)`
  - `RSI = 100 - 100/(1+RS)`
- **Output:** upward movement share.
- **Scale:** `[0,100]`.
- **Relative form:** already relative when built from returns.
- **Log form:** use log returns as inputs.
- **Zero-loss rule:** if `AL=0` and `AG>0`, RSI is `100`; if both are zero, output missing or `50` by fixed policy.

## 47. Bollinger position and width

- **Input:** log prices `p_i = ln(C_i)` over `n` candles.
- **Math:**
  - `mu = mean_n(p)`
  - `s = sd_n(p)`
  - `z_price = (p_t-mu)/(s+eps)`
  - `band_width_log = 2*k*s`
- **Output:** standardized price position and log band width.
- **Scale:** `z_price` is standard deviations; width is log-price units.
- **Relative form:** both are portable.
- **Log form:** preferred construction above.
- **Note:** Bollinger position is a price z-score. Do not duplicate it as a separate feature if `z_price` already exists.

---

# H. Regime, time, and multiple resolutions

## 48. Time bucket

- **Input:** candle timestamp.
- **Math:** map timestamp to hour, minute block, weekday, or weekend flag.
- **Output:** category or cyclic number.
- **Scale:** not price-relative.
- **Relative form:** not applicable.
- **Log form:** not applicable.
- **Cyclic encoding:** `sin(2*pi*hour/24)` and `cos(2*pi*hour/24)` prevent hour `23` and hour `0` from appearing far apart.

## 49. Multi-timeframe feature

- **Input:** same base OHLCV aggregated into larger fixed intervals.
- **Math:** calculate the same relative feature at each interval.
- **Example:** `g_1m(20)`, `g_5m(20)`, `g_1h(20)`.
- **Output:** one value per timeframe.
- **Scale:** use log returns, ratios, or standardized values.
- **Relative form:** yes, if the underlying feature is relative.
- **Log form:** preferred for price features.
- **Rule:** never compare raw dollar slopes from different timeframes. Convert to return per unit time.

## 50. Timeframe agreement

- **Input:** signs of the same feature at `m` timeframes.
- **Math:** `agreement = sum(sign(x_j)) / m`.
- **Output:** direction agreement.
- **Scale:** `[-1,1]`.
- **Relative form:** already relative.
- **Log form:** use log-derived inputs; agreement itself needs no log.
- **Example:** three positive timeframes gives `1`; two positive and one negative gives `1/3`.

---

# I. Minimal implementation set

Calculate each marked base feature over several lookbacks. Do not begin with every named indicator.

| Group | Feature | Preferred form |
|---|---|---|
| Return | 1-candle and `n`-candle movement | Log return |
| Change of return | Acceleration | Difference of equal-horizon log returns |
| Direction count | Positive-return fraction | `[0,1]` |
| Baseline | EMA or SMA distance | `ln(C/B)` |
| Trend | Linear slope | OLS slope of `ln(C)` |
| Trend quality | `R2` | `[0,1]` |
| Path quality | Efficiency ratio | Absolute net log return / gross absolute log return |
| Serial behavior | Return autocorrelation | Correlation of log returns |
| Intrabar range | High-low range | `ln(H/L)` |
| Full range | True range | Log true range |
| Volatility | Close-to-close volatility | SD of log returns |
| Volatility regime | Short/long ratio | Log ratio |
| Rolling location | Range position | `[0,1]` |
| Boundary | Breakout distance | Log distance |
| Peak loss | Drawdown | Log drawdown |
| Candle | Body and wick fractions | `[0,1]` plus signed log body |
| Volume regime | Relative volume | Log ratio to prior median |
| Traded value | Approximate dollar volume | USD plus percentile |
| Liquidity proxy | Absolute return / dollar volume | Log value or percentile |
| Volume direction | Signed-volume balance | `[-1,1]` |
| Price by volume | VWAP distance | `ln(C/VWAP)` |
| Unusualness | Z-score | Standardized transformed feature |
| Robust unusualness | Percentile rank | `[0,1]` |
| Time | Hour/weekday | Cyclic or category |
| Resolution | Same feature at several candle sizes | Same relative form |

Suggested lookbacks are not laws. Test a grid tied to time:

- Very short
- Short
- Medium
- Long

Example for one-minute candles: `3, 5, 10, 20, 60, 240`. For other candle sizes, choose lookbacks representing the same real durations.

---

# J. Named-indicator map

Many named indicators repeat the same core math.

| Name | Core math |
|---|---|
| Momentum / ROC | Return over lookback |
| MACD | Fast/slow EMA spread plus smoothing |
| Bollinger `%B` | Position around a moving mean and standard deviation |
| Bollinger bandwidth | Rolling volatility or dispersion width |
| Stochastic `%K` | Position inside rolling high-low range |
| Williams `%R` | Inverted rolling range position |
| ATR | Mean true range |
| RSI | Smoothed positive returns versus negative returns |
| OBV | Cumulative signed volume |
| VWAP | Volume-weighted price |
| Donchian channel | Rolling high and rolling low |
| Z-score | Distance from rolling mean divided by rolling SD |

Do not store both the named indicator and identical underlying math unless smoothing or parameterization differs.

---

# K. Required output columns for every experiment

For every feature variant, store:

| Field | Example |
|---|---|
| `feature_name` | `volatility_ratio` |
| `price_form` | `log` |
| `lookback` | `20` |
| `secondary_lookback` | `100` |
| `timeframe` | `1m` |
| `value` | `0.182` |
| `available_at` | candle close timestamp |
| `is_missing` | `false` |

Never replace missing values with zero unless zero has the correct mathematical meaning.

---

# L. Core safety rules

1. Build boundaries and baselines from prior candles when testing the current candle.
2. Fit scalers on training data only.
3. Use log returns, not raw price differences, for portable models.
4. Use log ratios, z-scores, or percentiles for volume.
5. Keep candle interval fixed inside each calculation.
6. Compare like with like: volatility ratio to volatility; range ratio to range.
7. Record every lookback and smoothing rule.
8. Include fees, slippage, and decision delay when testing edge.
9. An indicator is an input. Edge exists only if future net returns change out of sample.
