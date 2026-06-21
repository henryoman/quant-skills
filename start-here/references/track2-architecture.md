# Track 2 Architecture And Data Routing

Use this file when designing the strategy skill, data manifest, or backtest story.

## Correct Deliverable

Track 2 should produce a CMC Skill that generates a backtestable trading strategy spec. It should not be framed as:

- live execution bot
- private-key signer
- wallet/trade router
- PancakeSwap execution engine
- gas optimizer
- real-money trading loop

## Data Layer Split

```text
User prompt
  -> CMC Skill
  -> CMC intelligence layer
  -> Binance historical/raw market data layer
  -> local backtest engine
  -> deterministic strategy JSON/spec
```

## Recommended Routing

| Job | Use |
| --- | --- |
| Sponsor-required intelligence | CMC MCP / Agent Hub |
| Official Track 2 Skill output | CMC Skills framework |
| Latest prices | CMC quotes/latest plus Binance ticker cross-check |
| Current global regime | CMC global metrics, Fear & Greed, Altcoin Season, CMC indices |
| Historical spot candles | Binance Spot `/api/v3/klines` or Binance public bulk data |
| Historical futures candles | Binance Futures `/fapi/v1/klines` |
| Funding rate | Binance Futures `/fapi/v1/fundingRate` plus CMC MCP derivatives if available |
| Open interest / leverage | Binance Futures plus CMC MCP derivatives |
| Technical indicators | CMC precomputed RSI/MACD/EMA/ATR first; local fallback second |
| BSC/DEX token info | CMC DEX API / DexScan only |
| DEX K-lines | CMC `/v1/k-line/candles` or `/v1/k-line/points` |
| News / narratives | CMC MCP latest news / trending narratives |
| Backtest result | Local Python |

## Minimal Working Data Plan

CMC calls:

1. `quotes/latest` for BNB, BTC, ETH.
2. `global-metrics/quotes/latest`.
3. `fear-and-greed/latest`.
4. `altcoin-season-index/latest`.
5. CMC MCP technical analysis for BNB.
6. CMC MCP derivatives/funding/liquidation context.
7. CMC MCP news/narratives when requested or useful.

Binance calls:

1. Spot `/api/v3/klines` for `BNBUSDT` at `1h`, `4h`, `1d`.
2. Spot `/api/v3/ticker/24hr` for volume/momentum.
3. Spot `/api/v3/ticker/bookTicker` for spread.
4. Futures `/fapi/v1/fundingRate` for perp funding.
5. Futures `/futures/data/globalLongShortAccountRatio` for positioning.

## Historical Backtest Rule

Do not pretend CMC Basic free API supplies all historical OHLCV needed for a long backtest. For strict zero-dollar historical candles:

1. Use Binance REST klines for small/medium samples.
2. Use Binance public bulk files for larger multi-year samples.
3. Use CMC for current market context, CMC-native indicators, regime filters, and sponsor-aligned intelligence.

## Recommended Local Dataset Layout

```text
data/
  binance/
    spot/
      BNBUSDT/
        1h.parquet
        4h.parquet
        1d.parquet
    futures/
      BNBUSDT/
        1h.parquet
        funding.parquet
        open_interest.parquet
        long_short_ratio.parquet
  cmc/
    snapshots/
      quotes_latest.json
      global_metrics_latest.json
      fear_greed_latest.json
```

## Required Backtest Assumptions

Every strategy spec should state:

- execution timing, usually next candle open or next candle close
- fees and slippage assumptions
- candle source and timeframe
- CMC-derived regime/indicator sources
- whether data is live, cached, fixture, synthetic, or bulk historical
- no lookahead bias
- live trading disabled unless explicitly outside Track 2

## Strategy Spec Source Manifest Shape

```json
{
  "data_sources": {
    "official_intelligence": [
      "CMC Skill",
      "CMC MCP",
      "CMC precomputed RSI/MACD/EMA/ATR/Fear & Greed"
    ],
    "current_market_data": [
      "CMC quotes/latest",
      "CMC global metrics",
      "CMC Fear & Greed",
      "CMC Altcoin Season Index"
    ],
    "historical_backtest_data": [
      "Binance Spot /api/v3/klines",
      "Binance public historical data files"
    ],
    "derivatives_features": [
      "Binance /fapi/v1/fundingRate",
      "Binance /futures/data/globalLongShortAccountRatio",
      "CMC MCP derivatives data"
    ],
    "dex_or_bsc_data": [
      "CMC DEX API / DexScan only, if needed"
    ],
    "excluded_sources": [
      "GeckoTerminal",
      "DexScreener",
      "DeFiLlama",
      "CoinGecko",
      "TradingView scraping"
    ]
  }
}
```
