---
name: volatility-regime-strategy
description: Generate deterministic, backtestable crypto trading strategy specs from CoinMarketCap market context and historical OHLCV candles for BNB Hack Track 2 Strategy Skills. Use when asked to create, explain, validate, or demo a CoinMarketCap Strategy Skill, produce strategy JSON, classify market regimes, choose volatility breakout/mean reversion/range strategies, or document data provenance for CMC/free/fixture/synthetic market data.
---

# Volatility Regime Strategy Skill

## Purpose

Generate a deterministic, backtestable crypto trading strategy spec from CoinMarketCap market data and historical candles.

This Skill is for BNB Hack Track 2: Strategy Skills.

It does not execute trades.
It does not sign transactions.
It does not manage wallets.

## Inputs

```json
{
  "symbol": "BNB",
  "timeframe": "1h",
  "horizon": "24h",
  "risk": "medium",
  "mode": "hybrid-free"
}
```

## Modes

```txt
live-cmc:
  Use CoinMarketCap data for current market context.

hybrid-free:
  Use CoinMarketCap for current context and free Binance OHLCV for backtesting.

fixture:
  Use saved local example data for offline demos.

synthetic:
  Use generated candles for tests only. Do not claim performance from synthetic data.
```

## Workflow

1. Resolve the asset to a stable CoinMarketCap ID when CMC is available.
2. Fetch latest market context.
3. Load historical candles.
4. Compute simple technical features:
   - log returns
   - realized volatility
   - ATR percent
   - EMA trend
   - volume z-score
   - rolling high/low
5. Classify the market regime.
6. Select a strategy family.
7. Return a machine-readable strategy spec.
8. Include data provenance.

## Bundled resources

- Run `scripts/generate-strategy.ts` for the local deterministic demo shell.
- Read `examples/bnb-strategy.example.json` when a concrete output example is needed.
- Read `references/data-options.md` when choosing between CMC, Binance public candles, fixtures, and synthetic data.
- Read `references/contest-parameters.md` when checking Track 2 scope, timeline, judging, or submission requirements.
- Read `references/build-outline.md` when implementing the next feature in the strategy engine.
- Read `references/sources.md` only when source links or provenance for the starter package are needed.

## Strategy families

```txt
volatility_breakout:
  use when volatility, volume, and trend are expanding.

mean_reversion:
  use when price is stretched but trend is weak.

expected_range:
  use when the goal is to estimate the likely price range over a horizon.

binary_probability:
  optional; use when output should be p_up / p_down over a fixed horizon.
```

## Output contract

Return JSON with this shape:

```json
{
  "symbol": "BNB",
  "cmc_id": 1839,
  "timeframe": "1h",
  "horizon": "24h",
  "selected_strategy": "volatility_breakout",
  "market_regime": {
    "trend": "up",
    "volatility": "expanding",
    "volume": "expanding"
  },
  "entry_rules": [
    "close > rolling_high_20",
    "volume_zscore_20 > 1.25"
  ],
  "exit_rules": [
    "close < ema_20",
    "return_since_entry <= -0.025",
    "return_since_entry >= 0.05",
    "bars_held >= 24"
  ],
  "risk_rules": {
    "max_position_size_pct": 10,
    "stop_loss_pct": 2.5,
    "take_profit_pct": 5.0
  },
  "backtest_config": {
    "fee_bps": 10,
    "slippage_bps": 5,
    "historical_data_source": "binance_public_klines"
  },
  "data_provenance": {
    "live_context_source": "coinmarketcap",
    "historical_ohlcv_source": "binance_public_klines",
    "fixture_mode": false,
    "synthetic_mode": false
  }
}
```

## Safety / honesty rules

- Never claim fixture or synthetic data is live CMC data.
- Never output vague advice without deterministic rules.
- Never include private keys or wallet actions.
- Always include data provenance.
