# Examples

Use these examples when writing docs, code comments, strategy specs, or setup instructions.

## CMC MCP Configuration

```json
{
  "mcpServers": {
    "cmc-mcp": {
      "url": "https://mcp.coinmarketcap.com/mcp",
      "headers": {
        "X-CMC-MCP-API-KEY": "your-api-key"
      }
    }
  }
}
```

## CMC Trial / Keyless Calls

Latest quotes:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v3/cryptocurrency/quotes/latest?symbol=BNB,BTC,ETH'
```

Fear & Greed:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v3/fear-and-greed/latest'
```

Global metrics:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v1/global-metrics/quotes/latest'
```

Listings:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v3/cryptocurrency/listings/latest?start=1&limit=20'
```

DEX token price:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v1/dex/token/price?contract_address=TOKEN_CONTRACT_ADDRESS'
```

DEX K-line endpoint placeholder:

```bash
curl 'https://pro-api.coinmarketcap.com/trial-pro-api/v1/k-line/candles'
```

Check exact required query parameters in CMC docs before wiring DEX K-lines.

## Binance Spot Calls

BNB/USDT 1h candles:

```bash
curl 'https://api.binance.com/api/v3/klines?symbol=BNBUSDT&interval=1h&limit=1000'
```

Latest BNB/USDT price:

```bash
curl 'https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT'
```

24h BNB/USDT stats:

```bash
curl 'https://api.binance.com/api/v3/ticker/24hr?symbol=BNBUSDT'
```

Best bid/ask:

```bash
curl 'https://api.binance.com/api/v3/ticker/bookTicker?symbol=BNBUSDT'
```

Order book:

```bash
curl 'https://api.binance.com/api/v3/depth?symbol=BNBUSDT&limit=100'
```

## Binance Futures Calls

BNBUSDT perpetual candles:

```bash
curl 'https://fapi.binance.com/fapi/v1/klines?symbol=BNBUSDT&interval=1h&limit=1500'
```

BNBUSDT funding:

```bash
curl 'https://fapi.binance.com/fapi/v1/fundingRate?symbol=BNBUSDT&limit=1000'
```

BNBUSDT global long/short ratio:

```bash
curl 'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BNBUSDT&period=1h&limit=500'
```

## Example Strategy Spec

```json
{
  "strategy_name": "CMC_BNB_Regime_Momentum_Skill",
  "track": "Track 2 - Strategy Skills",
  "official_stack": [
    "CMC Skill",
    "CMC MCP",
    "CMC precomputed RSI/MACD/EMA/ATR/Fear & Greed",
    "Binance public OHLCV for backtest"
  ],
  "target_asset": "BNBUSDT",
  "timeframe": "1h",
  "data_sources": {
    "current_market_data": [
      "CMC quotes/latest",
      "CMC global metrics",
      "CMC Fear & Greed",
      "CMC MCP technical analysis",
      "CMC MCP derivatives data",
      "CMC MCP news/narratives"
    ],
    "historical_backtest_data": [
      "Binance Spot /api/v3/klines",
      "Binance public historical data files"
    ],
    "derivatives_features": [
      "Binance /fapi/v1/fundingRate",
      "Binance globalLongShortAccountRatio",
      "CMC MCP derivatives data"
    ],
    "excluded_sources": [
      "GeckoTerminal",
      "DexScreener",
      "DeFiLlama",
      "CoinGecko",
      "TradingView scraping"
    ]
  },
  "features": [
    "ema_20",
    "ema_50",
    "rsi_14",
    "macd",
    "atr_14",
    "volume_zscore_24h",
    "cmc_fear_greed",
    "cmc_altcoin_season",
    "funding_rate",
    "long_short_ratio",
    "btc_trend_filter"
  ],
  "entry_rules": [
    "BNBUSDT close > EMA_20",
    "EMA_20 > EMA_50",
    "RSI_14 >= 50 and RSI_14 <= 70",
    "MACD histogram > 0",
    "BTCUSDT close > BTC EMA_50",
    "CMC Fear & Greed >= 35",
    "funding_rate < 0.0005"
  ],
  "exit_rules": [
    "BNBUSDT close < EMA_20",
    "EMA_20 < EMA_50",
    "RSI_14 < 45",
    "close < entry_price - 2 * ATR_14"
  ],
  "risk_management": {
    "position_size": "max 20% portfolio",
    "stop_loss": "2 * ATR_14",
    "take_profit": "3 * ATR_14",
    "max_drawdown_cutoff": "15%",
    "fees": "0.10%",
    "slippage": "0.05%"
  },
  "backtest_assumptions": {
    "execution": "next candle open",
    "lookahead_bias": "not allowed",
    "data_frequency": "1h",
    "live_trading": false
  }
}
```

## Source Links

- CMC docs index: `https://pro.coinmarketcap.com/llms.txt`
- CMC MCP: `https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/mcp.md`
- CMC Trial Pro API: `https://pro.coinmarketcap.com/api/documentation/pro-api-reference/trial-pro-api.md`
- CMC x402: `https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/x402.md`
- Binance Spot market data: `https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints`
- Binance USD-M Futures market data: `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api`
- Binance public historical data: `https://data.binance.vision/`
