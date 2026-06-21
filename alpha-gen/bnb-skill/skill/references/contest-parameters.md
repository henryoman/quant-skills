# Contest Parameters — Track 2 Only

## Competition

BNB Hack: AI Trading Agent Edition is run by BNB Chain, CoinMarketCap, and Trust Wallet.

There are two tracks, but this project targets **Track 2 only**.

## Track 2: Strategy Skills

Track 2 requirement:

```txt
Build a CoinMarketCap Skill that generates backtestable trading strategies from market data.
```

Important meaning:

```txt
Required:
  market data input
  strategy logic
  backtestable strategy output
  repo + demo

Not required:
  live trading
  wallet signing
  BSC execution
  real money
```

## Prize structure

Track 2 prize pool:

```txt
1st: $3,000
2nd: $2,000
3rd: $1,000
Total: $6,000
```

There are also special prizes, but for this package we only care about the one that is naturally aligned with Track 2:

```txt
Best use of CoinMarketCap Data & Signal: $2,000
```

## Judging

Track 2 is judged by a panel. It is not scored by live PnL.

Judging factors:

```txt
technical execution
originality
real-world relevance
demo / presentation quality
```

So the project should look real and deterministic, not vague.

Bad output:

```txt
BNB looks bullish. You should buy.
```

Good output:

```json
{
  "strategy": "volatility_breakout",
  "timeframe": "1h",
  "entry_rules": [
    "close > rolling_high_20",
    "volume_zscore_20 > 1.25",
    "atr_pct > median_atr_pct_60"
  ],
  "exit_rules": [
    "close < ema_20",
    "return_since_entry <= -0.025",
    "return_since_entry >= 0.05",
    "bars_held >= 24"
  ]
}
```

## Timeline

Key dates from the hackathon FAQ / official pages:

```txt
Build window: June 3–21, 2026
Track 2 submission due: June 21, 2026
Track 1 live trading: June 22–28, 2026
Judging: June 29–July 5, 2026
Winners: week of July 6, 2026
```

## Submission checklist

```txt
[ ] Public repo
[ ] SKILL.md
[ ] README explaining Track 2 purpose
[ ] Example strategy outputs
[ ] Demo command or demo video
[ ] Data-source explanation
[ ] Backtestable JSON spec
[ ] No private keys committed
[ ] No fake live-data claims
```

## What a backtestable strategy spec must include

A strategy is backtestable when another program can replay it over historical candles.

Minimum fields:

```txt
asset
source
timeframe
horizon
strategy name
features used
entry rules
exit rules
risk rules
fee assumption
slippage assumption
position sizing rule
```

Optional but good:

```txt
market regime
confidence score
expected move
strategy alternatives
human explanation
backtest results
walk-forward settings
```
