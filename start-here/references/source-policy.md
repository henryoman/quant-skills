# Source Policy

Use this file to decide whether a data source belongs in the Track 2 stack.

## Allow

Allow these by default:

- CMC Skills framework
- CMC Agent Hub
- CMC MCP
- CMC Basic/keyed API where the user's plan allows it
- CMC Trial/Keyless API
- CMC precomputed indicators
- CMC global metrics
- CMC Fear & Greed
- CMC Altcoin Season Index
- CMC CMC20/CMC100 indices
- CMC DEX API / DexScan data
- Binance Spot public REST market-data endpoints
- Binance Spot public WebSocket streams
- Binance USD-M Futures public REST market-data endpoints
- Binance Futures public WebSocket streams
- Binance public historical data files
- Local Python/Pandas/Polars/vectorized backtesting code

## Allow With Caveats

| Source | Caveat |
| --- | --- |
| CMC Basic free API | Personal/free quotas and endpoint access can change. Verify with current plan docs and `/v1/key/info`. Avoid assuming long historical OHLCV. |
| CMC Trial/Keyless API | Good for prototypes and demos; aggressively rate-limited and fixed subset only. |
| CMC MCP | Requires API key/hackathon access. If tools fail, ask user to configure `X-CMC-MCP-API-KEY`. |
| Binance REST loops | Fine for small/medium datasets; prefer bulk files for large backtests. |
| CMC DEX K-lines | Check exact required params before wiring. |
| Local indicator fallback | Only use when CMC precomputed indicators are unavailable; disclose fallback. |

## Official But Paid

CMC x402 is official but not zero-dollar. It is pay-per-request using USDC on Base. Do not use it for strict no-payment builds.

## Exclude For This Submission

Exclude these even if free, because they weaken the sponsor-aligned Track 2 story:

- GeckoTerminal
- DexScreener
- DeFiLlama
- CoinGecko
- CoinPaprika
- CryptoCompare
- Messari
- Glassnode
- Santiment
- TradingView scraping
- Random BSC indexers
- Unofficial CMC scrapers
- Unofficial Binance scrapers when official public endpoints or bulk files exist

## Language Rules

Use precise source language:

- Say `CMC-owned DEX data`, not `DexScreener`.
- Say `Binance public OHLCV`, not `exchange data from a third-party aggregator`.
- Say `participation/volume`, not `institutional buying`.
- Say `CMC MCP derivatives context`, not `proprietary derivatives feed`, unless the exact feed is documented.
- Say `free/keyless/prototyping endpoint`, not `production unlimited free API`.

## Rejection Rule

Reject a proposed source if any answer is "yes":

1. Is it a competitor or non-sponsor crypto data API?
2. Does it require scraping a UI instead of using official APIs?
3. Does it make the strategy non-reproducible for a zero-dollar reviewer?
4. Does it add a data dependency not needed for a backtestable strategy spec?
5. Does it make the sponsor story weaker than CMC + Binance?
