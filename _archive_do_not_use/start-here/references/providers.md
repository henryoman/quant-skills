# Provider Reference

Use this file when choosing a data source or explaining key requirements.

## No-key public OHLCV

| Provider | Good for | Key needed | Notes |
| --- | --- | --- | --- |
| Binance Spot public klines | Liquid crypto pairs | No | Best first choice for crypto spot OHLCV when Binance coverage is acceptable. |
| Coinbase Exchange candles | Major crypto USD pairs | No | Max request windows are smaller; script chunks requests. |
| Kraken OHLC | Crypto spot | No | Useful fallback; symbol naming differs from common tickers. |

## Keyed providers

| Provider | Good for | Env vars | Notes |
| --- | --- | --- | --- |
| CoinMarketCap | Crypto metadata, quotes, some historical endpoints depending on plan | `CMC_API_KEY` | Plan access changes; verify endpoint availability before wiring production code. |
| Polygon | US stocks, ETFs, options, crypto, forex depending on plan | `POLYGON_API_KEY` | Good for equities OHLCV; adjusted/unadjusted settings matter. |
| Alpaca | US equities and trading workflows | `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY` | Useful when research may later connect to paper/live execution. |
| Twelve Data | Multi-asset candles | `TWELVE_DATA_API_KEY` | Coverage/rate limits depend on plan. |
| Alpha Vantage | Simple retail market data | `ALPHA_VANTAGE_API_KEY` | Rate limits can be restrictive. |

## Selection rules

- Prefer direct exchange/public historical candles for reproducible crypto OHLCV.
- Prefer paid/keyed vendors for equities if reliability matters.
- Do not use scraped web data unless the user explicitly accepts fragility.
- Keep adjusted and unadjusted equity data clearly labeled.
- Exclude the current partial candle unless the user is doing live monitoring.
- Store normalized research CSVs separately from raw provider payloads.

## Minimum metadata to record

```text
provider
symbol
interval
start
end
download_time_utc
api_key_required
adjusted_prices
known_gaps
rate_limit_notes
```
