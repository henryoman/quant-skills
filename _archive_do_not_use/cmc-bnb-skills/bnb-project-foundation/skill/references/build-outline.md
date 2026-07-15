# Simple Build Outline

## Build one thing

Do not build multiple apps.

Build one Skill with several strategy modes:

```txt
Volatility Regime Strategy Skill
```

## Strategy modes

Start with 3.

```txt
1. volatility_breakout
2. mean_reversion
3. expected_range
```

Add later if time:

```txt
4. binary_probability
5. trend_following
```

## Input

```json
{
  "symbol": "BNB",
  "timeframe": "1h",
  "horizon": "24h",
  "risk": "medium",
  "mode": "hybrid-free"
}
```

## Output

```json
{
  "symbol": "BNB",
  "strategy": "volatility_breakout",
  "regime": "high_volatility_uptrend",
  "entry_rules": [],
  "exit_rules": [],
  "risk_rules": {},
  "backtest_config": {},
  "data_provenance": {}
}
```

## Minimal feature engine

Compute these from candles:

```txt
log returns
realized volatility
ATR percent
EMA 20 / EMA 50
EMA slope
volume z-score
rolling high / rolling low
```

## Simple regime logic

```txt
if trend_up and volatility_expanding and volume_expanding:
  choose volatility_breakout

if trend_flat and price_far_from_mean:
  choose mean_reversion

if volatility_stable and no strong trend:
  choose expected_range
```

## Minimal demo command

```bash
bun run strategy --symbol BNB --timeframe 1h --horizon 24h --mode fixture
```

## Build order

```txt
1. Write SKILL.md
2. Define strategy JSON type
3. Create fixture input/output
4. Implement simple strategy selector
5. Add Binance candle fetcher
6. Add CMC quote/context fetcher
7. Add simple backtest metrics
8. Record demo
9. Submit repo
```
