# Data Options — Free, CMC, Fixtures, Synthetic

## Main rule

Use real CoinMarketCap data for the official Skill context when possible.

Use free historical candles for backtesting if the free CMC plan does not provide enough historical data.

Do not fake live data and pretend it came from CMC.

## Best no-money setup

```txt
Current market context:
  CoinMarketCap free API key or CMC MCP

Historical OHLCV/backtesting:
  Binance public klines or Binance Data Vision

Offline/demo mode:
  saved fixtures from real responses

Unit tests:
  synthetic candles
```

## CMC data we care about

Useful CMC / Agent Hub data:

```txt
crypto search / CMC ID resolution
latest quotes
market cap
24h volume
percent changes
metadata
technical analysis if available
global market metrics
fear and greed
trending narratives
news / macro events
derivatives / funding / open interest if exposed
```

## Why CMC ID matters

Do not internally rely only on symbols.

Bad:

```txt
symbol = "BNB"
```

Better:

```txt
search symbol/name
  -> resolve to CMC numeric ID
  -> fetch quotes / metrics using CMC ID
```

This avoids symbol collisions.

## Free CMC limitation

The free CMC Basic plan is good for testing latest market data, rankings, quotes, and current context.

It is not ideal for serious historical backtesting, because historical data is generally not included on the Basic plan.

So the clean architecture is:

```txt
CMC = live/current market context
Binance = free historical OHLCV for backtests
```

## Acceptable fixture/mocking strategy

Allowed and useful:

```txt
fixtures from real API responses
mock objects with the same schema
synthetic candles for tests
cached API responses
fallback to Binance/CoinGecko for free candles
```

Not okay:

```txt
claiming fake data came from CMC
faking backtest results
hiding the data source
bypassing paid API restrictions
scraping protected paid data
```

## Data provenance field

Every output should say where data came from:

```json
{
  "data_provenance": {
    "live_context_source": "coinmarketcap",
    "historical_ohlcv_source": "binance_public_klines",
    "fixture_mode": false,
    "synthetic_mode": false
  }
}
```
