# Free CMC + Binance Data Manifest

Use this as the allowed data-source map for BNB Hack/Track 2 strategy skill work.

Last reviewed from local official skill docs and official CMC/Binance docs: 2026-06-21.

## Quick Rule

```text
CMC = official Skill layer, sponsor-aligned intelligence, indicators, regime/sentiment, DEX/BSC data.
Binance = free public raw market data for candles, tickers, order book, trades, futures funding/OI/positioning.
Local Python = backtest engine and final strategy-spec generator.
```

## Zero-Dollar CMC-Owned Sources

| Source | Cost posture | Best Track 2 use | Notes |
| --- | --- | --- | --- |
| CMC Skills framework | Official Track 2 deliverable | Build the strategy-generating skill | Output should be a backtestable strategy spec, not a live execution agent. |
| CMC Agent Hub | Free/key/hackathon access depends on account | Agent workflows and CMC-native routing | Keep it central in the submission story. |
| CMC MCP | Requires CMC MCP API key or hackathon access | Live quotes, technicals, global metrics, news, narratives, derivatives, on-chain metrics | Endpoint: `https://mcp.coinmarketcap.com/mcp`; header: `X-CMC-MCP-API-KEY`. |
| CMC precomputed indicators | Official Track 2 stack where available | RSI, MACD, EMA, ATR, Fear & Greed | Prefer CMC-provided indicators before local fallback calculations. |
| CMC Basic free API key | Free personal-use plan; quotas and endpoint access must be checked | Latest quotes, listings, map IDs, metadata, global metrics, price conversion | Do not rely on Basic for long historical OHLCV backtests. |
| CMC Trial/Keyless API | No key; aggressively rate-limited fixed subset | Prototype response shapes and no-signup demos | Base URL: `https://pro-api.coinmarketcap.com/trial-pro-api`; `GET` only. |
| CMC global metrics | Free via Basic/Trial subset where available | Total market cap, dominance, 24h volume, regime context | Use for market filters. |
| CMC Fear & Greed | Free via Trial subset where available | Current/historical sentiment regime | Use as a regime filter, not as a standalone signal. |
| CMC Altcoin Season Index | Free via Trial subset where available | Risk-on/risk-off altcoin regime | Good market context for BNB/BTC/ETH filters. |
| CMC CMC20/CMC100 indices | Free via Trial subset where available | Broad crypto benchmark context | Useful for regime comparison. |
| CMC DEX API / DexScan data | CMC-owned; free/keyless subset exists | BSC/DEX token price, pools, liquidity, security, holders, transactions, K-lines | Use this instead of GeckoTerminal/DexScreener for DEX-style data. |

## CMC MCP Tool Manifest

| Tool area | Use |
| --- | --- |
| Search Cryptocurrencies | Resolve symbols/names/slugs to stable CMC IDs. |
| Live Quotes | Current price, market cap, volume, percent changes, supply, dominance. |
| Global Market Metrics | Total market cap, 24h volume, Fear & Greed, Altcoin Season, BTC/ETH dominance. |
| Crypto Technical Analysis | MA/SMA, EMA, MACD, RSI, Fibonacci levels, support/resistance. |
| Market Cap Technical Analysis | Technicals on overall crypto market capitalization. |
| Crypto Info | Metadata, logo, description, website, whitepaper, social links. |
| Latest News | Asset-specific recent news. |
| Concept Search | Semantic lookup for crypto concepts, FAQs, definitions. |
| Trending Narratives | Market sectors/narratives and associated tokens. |
| On-Chain Metrics | Holder distribution, whale/retail, holding-time buckets, fees where available. |
| Derivatives Data | Open interest, funding, liquidations, leverage context. |
| Macro Events | Scheduled macro/economic events that can affect markets. |

## CMC Basic / Keyed API Families

| Endpoint family | Example endpoint | Use |
| --- | --- | --- |
| ID mapping | `/v1/cryptocurrency/map` | Stable CMC IDs for BNB/BTC/ETH/etc. |
| Latest quotes | `/v2/cryptocurrency/quotes/latest` or current documented version | Current asset prices and market data. |
| Listings | `/v1/cryptocurrency/listings/latest` or current documented version | Ranked crypto universe. |
| Metadata | `/v2/cryptocurrency/info` | Logos, tags, categories, official links. |
| Market pairs | `/v2/cryptocurrency/market-pairs/latest` | Venue/pair availability. |
| Global metrics | `/v1/global-metrics/quotes/latest` | Total market cap, dominance, volume. |
| Price conversion | `/v2/tools/price-conversion` | Convert crypto/USD/fiat values. |
| Exchange info | exchange endpoint family | Binance-side exchange metadata from CMC. |
| Key info | `/v1/key/info` | Verify current plan, usage, and access. |

## CMC Trial / Keyless API Subset

Base URL:

```text
https://pro-api.coinmarketcap.com/trial-pro-api
```

Standard endpoints documented in the keyless subset:

| Endpoint | Use |
| --- | --- |
| `/v1/cryptocurrency/map` | Map symbols to CMC IDs. |
| `/v2/cryptocurrency/info` | Metadata. |
| `/v1/exchange/map` | Exchange ID map. |
| `/v3/cryptocurrency/listings/latest` | Ranked universe. |
| `/v1/cryptocurrency/listings/latest` | Listings latest. |
| `/v3/cryptocurrency/quotes/latest` | Latest quotes. |
| `/v1/global-metrics/quotes/latest` | Market-wide regime. |
| `/v2/tools/price-conversion` | Conversion. |
| `/v1/cryptocurrency/categories` | Category list. |
| `/v1/cryptocurrency/category` | Category details. |
| `/v1/simple/price` | Simple prices. |
| `/v3/fear-and-greed/latest` | Current sentiment. |
| `/v3/fear-and-greed/historical` | Historical sentiment. |
| `/v3/index/cmc100-latest` | CMC100 latest. |
| `/v3/index/cmc100-historical` | CMC100 history. |
| `/v3/index/cmc20-latest` | CMC20 latest. |
| `/v3/index/cmc20-historical` | CMC20 history. |
| `/v1/altcoin-season-index/latest` | Current altcoin-season signal. |
| `/v1/altcoin-season-index/historical` | Historical altcoin-season signal. |

DEX endpoints documented in the keyless subset:

| Endpoint | Use |
| --- | --- |
| `/v4/dex/spot-pairs/latest` | DEX pair listings. |
| `/v4/dex/pairs/quotes/latest` | DEX pair quotes. |
| `/v1/dex/token` | Token detail. |
| `/v1/dex/token/price` | DEX token price. |
| `/v1/dex/token-liquidity/query` | Token liquidity. |
| `/v1/dex/token/pools` | Token pools. |
| `/v1/dex/search` | Search DEX tokens/pairs. |
| `/v1/dex/security/detail` | Token security/risk signal. |
| `/v1/dex/tokens/transactions` | Swap/transaction list. |
| `/v1/dex/liquidity-change/list` | Liquidity change list. |
| `/v1/dex/platform/list` | Supported platforms/networks. |
| `/v1/dex/platform/detail` | Platform details. |
| `/v1/k-line/candles` | DEX K-line candles. |
| `/v1/k-line/points` | DEX K-line points. |
| `/v1/dex/holders/list` | Holder list. |
| `/v1/dex/holders/count` | Holder count. |
| `/v1/dex/holders/detail` | Holder detail. |

## Official But Not Zero-Dollar

| Source | Cost posture | Use only if |
| --- | --- | --- |
| CMC x402 | Pay-per-request; docs list current price as `$0.01 USDC` per request, subject to change | User explicitly accepts payment. Avoid for strict zero-dollar builds. |

## Free Binance Sources

| Source | Base / endpoint family | Best Track 2 use |
| --- | --- | --- |
| Binance Spot REST | `https://api.binance.com` | Historical spot candles, tickers, order book, trades. |
| Spot klines | `/api/v3/klines` | Main free historical OHLCV backtest source for `BNBUSDT`, `BTCUSDT`, etc. |
| Spot ticker price | `/api/v3/ticker/price` | Latest price cross-check. |
| Spot 24h stats | `/api/v3/ticker/24hr` | 24h price/volume/change filters. |
| Spot order book | `/api/v3/depth` | Liquidity/depth proxy. |
| Spot best bid/ask | `/api/v3/ticker/bookTicker` | Spread/execution-cost assumption. |
| Spot aggregate trades | `/api/v3/aggTrades` | Trade-flow/recent activity features. |
| Spot WebSocket streams | Binance Spot WS docs | Live prices/candles for demos. |
| Binance USD-M Futures REST | `https://fapi.binance.com` | Futures OHLCV, funding, OI, positioning. |
| Futures klines | `/fapi/v1/klines` | Perpetual futures candle history. |
| Funding rate history | `/fapi/v1/fundingRate` | Funding/carry/crowding filter. |
| Current open interest | `/fapi/v1/openInterest` | Current leverage/liquidity context. |
| Open interest history | `/futures/data/openInterestHist` | OI regime. |
| Global long/short ratio | `/futures/data/globalLongShortAccountRatio` | Positioning filter. |
| Taker long/short ratio | `/futures/data/takerlongshortRatio` | Aggression/flow factor. |
| Binance public bulk data | `https://data.binance.vision/` | Multi-year reproducible candle/trade datasets without REST loops. |

## Minimal BNB-Focused Universe

Primary target:

```text
BNBUSDT
```

Market filters:

```text
BTCUSDT
ETHUSDT
CMC global metrics
CMC Fear & Greed
CMC Altcoin Season Index
CMC derivatives / Binance funding
```

Optional liquid universe:

```text
BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT
```
