---
name: data-download-clean
description: Use when downloading and cleaning zero-dollar market, derivatives, metadata, and context datasets for alpha generation or backtesting in this quant-skills repo. Covers Binance public klines, futures funding, open interest, long/short ratios, exchange metadata, and optional CoinMarketCap context data when credentials are available.
---

# Data Download Clean Skill

Use this skill after `starter-pack` says the environment is ready for lane C: Binance historical data or local backtesting.

This skill owns the first data layer for alpha-generation work:

```text
source data -> raw local files -> cleaned local files -> downstream backtest/features
```

It does not design strategies or run portfolio analytics. It does generate a static HTML audit report for every download/clean step so the user can see what is right, what needs review, what is wrong, and which files were written.

## What This Skill Downloads And Cleans

Core first-pass datasets:

```text
klines
  Spot and USD-M Futures OHLCV candles from Binance public REST.

funding_rates
  USD-M Futures historical funding rates from Binance public REST.

open_interest
  USD-M Futures open interest history from Binance public REST.

long_short_ratios
  USD-M Futures global account long/short ratio from Binance public REST.

exchange_metadata
  Spot and USD-M Futures exchangeInfo metadata from Binance public REST.
```

Optional context datasets:

```text
cmc_asset_context
  CoinMarketCap ID mapping, metadata, latest quote context, categories, rankings, and market status.
  Use only when a CMC key, CMC MCP, or documented keyless endpoint is available.
```

Not first-pass yet:

```text
Binance bulk archive downloader
DEX/DexScan historical archive normalizer
order book snapshots
trade-by-trade archives
news/social/sentiment feeds
```

If the user asks for those, explain that they are next implementation targets and add a focused script instead of improvising a fragile pipeline.

## Source Rules

Default historical/backtest sources:

```text
Binance public Spot klines
Binance public USD-M Futures klines
Binance public USD-M Futures funding/open-interest/long-short endpoints
Binance public exchangeInfo metadata
```

Allowed context sources:

```text
CoinMarketCap MCP/API for asset identity, current market context, metadata, and sponsor-aligned intelligence
```

Do not use excluded competitor APIs for this project story:

```text
GeckoTerminal, DexScreener, DeFiLlama, CoinGecko, CoinPaprika,
CryptoCompare, Messari, Glassnode, Santiment, TradingView scraping,
random BSC indexers, unofficial scrapers
```

## Required Inputs

Before downloading data, identify:

```text
datasets: klines | funding_rates | open_interest | long_short_ratios | exchange_metadata | all_core
market_type: spot | usd_m_futures
symbols: BTCUSDT, ETHUSDT, BNBUSDT, ...
interval: for klines, e.g. 1h; for derivatives history, e.g. 5m, 15m, 1h, 4h, 1d depending on endpoint
start_date: YYYY-MM-DD, required for historical datasets
end_date: YYYY-MM-DD, required for historical datasets
output_dir: data/market/binance
```

Defaults when the user has not specified values:

```text
symbols: BTCUSDT, ETHUSDT, BNBUSDT
kline interval: 1h
derivatives period: 1h
output_dir: data/market/binance
```

If the user has not specified dates for a historical dataset, ask for the date range. Do not silently download an unbounded range.

## First Two Steps

### Step 1: Plan the dataset

Produce a short dataset plan before running any download:

```text
Dataset plan:
- Source: Binance public <spot|usd_m_futures>
- Datasets: <datasets>
- Symbols: <symbols>
- Kline interval: <interval, if used>
- Derivatives period: <period, if used>
- Date range: <start_date> to <end_date>
- Raw output: <output_dir>/raw/
- Clean output: <output_dir>/clean/
```

### Step 2: Download and clean

Use `download_binance_klines.py` for OHLCV candles:

```bash
python3 alpha-gen-skills/data-download-clean/scripts/download_binance_klines.py \
  --market spot \
  --symbols BTCUSDT ETHUSDT BNBUSDT \
  --interval 1h \
  --start 2024-01-01 \
  --end 2024-03-01 \
  --output-dir data/market/binance
```

Default report:

```text
data/market/binance/reports/binance_klines_report.html
```

Use `download_binance_derivatives.py` for futures funding, open interest, and long/short ratio:

```bash
python3 alpha-gen-skills/data-download-clean/scripts/download_binance_derivatives.py \
  --symbols BTCUSDT ETHUSDT BNBUSDT \
  --datasets funding_rates open_interest long_short_ratios \
  --period 1h \
  --start 2024-01-01 \
  --end 2024-03-01 \
  --output-dir data/market/binance
```

Default report:

```text
data/market/binance/reports/binance_derivatives_report.html
```

Use `download_binance_metadata.py` for exchange metadata:

```bash
python3 alpha-gen-skills/data-download-clean/scripts/download_binance_metadata.py \
  --markets spot usd_m_futures \
  --output-dir data/market/binance
```

Default report:

```text
data/market/binance/reports/binance_metadata_report.html
```

## File Layout

Write raw and clean files under stable paths:

```text
<output_dir>/raw/<market>/<dataset>/<symbol>/<interval-or-period>.csv
<output_dir>/clean/<market>/<dataset>/<symbol>/<interval-or-period>.csv
<output_dir>/raw/<market>/exchange_metadata/exchangeInfo.json
<output_dir>/clean/<market>/exchange_metadata/symbols.csv
<output_dir>/reports/<script-specific-report>.html
```

## Clean Schemas

### klines

```text
symbol,market,interval,open_time,open_time_ms,open,high,low,close,volume,close_time,close_time_ms,quote_volume,trade_count,taker_buy_base_volume,taker_buy_quote_volume,is_closed,source
```

### funding_rates

```text
symbol,market,funding_time,funding_time_ms,funding_rate,mark_price,source
```

### open_interest

```text
symbol,market,period,timestamp,timestamp_ms,sum_open_interest,sum_open_interest_value,source
```

### long_short_ratios

```text
symbol,market,period,timestamp,timestamp_ms,long_short_ratio,long_account,short_account,source
```

### exchange_metadata

```text
symbol,market,status,base_asset,quote_asset,contract_type,onboard_date_ms,delivery_date_ms,permissions,order_types,raw_json,source
```

## Cleaning Rules

Apply these rules to every cleaned dataset:

```text
Timestamps are UTC ISO-8601 strings with Z suffix.
Millisecond epoch columns are preserved.
Numeric fields are decimal strings as returned by the source, not rounded floats.
Rows are sorted by timestamp.
Duplicate timestamp rows are removed per symbol/dataset.
Raw source payloads are kept separately before normalization.
```

For klines:

```text
The final still-open candle is excluded by default.
```

For derivatives history:

```text
Only USD-M Futures is supported in the first pass.
Funding rates do not use --period.
Open interest and long/short ratios require --period.
```

## When To Use Bulk Files Instead

Use Binance public bulk historical files instead of REST pagination when:

```text
The user requests many symbols.
The user requests minute-level data over long ranges.
The request is for a reproducible full historical archive.
REST rate limits become the bottleneck.
```

For this first-pass skill, if bulk files are needed, explain that the next implementation step should add a bulk downloader/unzip/normalize script. Do not improvise a fragile one-off pipeline unless the user explicitly asks.

## CMC Context Data

CMC context is useful for:

```text
symbol-to-CMC-ID mapping
asset metadata
current rank and market cap context
category and sector labels
latest quote sanity checks
```

Use CMC context only after confirming one of these exists:

```text
CMC MCP access
CMC_API_KEY
suitable official keyless/trial endpoint
```

Do not block Binance historical downloads on CMC credentials.

## Output After Completion

After a download/clean task, summarize:

```text
Downloaded:
- <dataset> <symbol> <market> <interval/period/date range>

Wrote:
- raw: <path>
- clean: <path>
- report: <path>

Known limitations:
- Binance public data only unless CMC context was explicitly used
- no delisting survivorship handling unless explicitly added
- no bulk archive pipeline unless explicitly added
```

## Downstream Handoff

After cleaned files exist, hand off to the next skill or task:

```text
feature generation
backtesting
strategy-spec generation
market report
```

Do not move into downstream analysis unless the user asks.
