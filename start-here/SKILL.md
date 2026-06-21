---
name: starter-pack
description: Use first when onboarding an agent or user into this quant-skills repo. Sets up the repo workflow, checks required local tools, chooses market-data providers, creates API-key env templates, downloads normalized OHLCV data, and routes into CMC, Binance, market-report, or OHLCV alpha-research skills.
---

# Starter Pack Skill

Use this skill before any other skill in this repository.

This is the bootstrapping layer. Its job is to make sure the model and user have the minimum repo context, local tools, credentials, data-source plan, and normalized OHLCV files needed before moving into CMC, market-report, or alpha-generation work.

## First Rule

Before using another quant skill, check readiness.

If a required skill, tool, credential, or data file is missing, stop and give the smallest concrete command list needed to fix that missing piece. Do not pretend the downstream skill is ready.

## Required Skill Pack

The starter pack expects these local skill folders to exist:

```text
start-here/
cmc-bnb-skills/cmc-mcp/
cmc-bnb-skills/cmc-api-crypto/
cmc-bnb-skills/cmc-api-market/
cmc-bnb-skills/cmc-api-dex/
cmc-bnb-skills/crypto-research/
cmc-bnb-skills/market-report/
alpha-gen-skills/ohlcv-alpha-research/
```

Optional folders:

```text
alpha-gen-skills/<other-skill-name>/
third-party-skills/<skill-name>/
```

Only use optional folders when the user explicitly asks for custom alpha-generation skills or third-party/vendor skills.

## Basic Local Tooling

Before downstream work, make sure the user has the needed basics:

```text
python3
curl
jq
git
```

Recommended but not required:

```text
uv
node
npm
```

Python is required for local OHLCV downloads, normalization, backtests, and alpha research.

## Copy-Paste Readiness Commands

When the user is in the repo root, use these commands for a quick local readiness check:

```bash
pwd
find start-here cmc-bnb-skills alpha-gen-skills -mindepth 1 -maxdepth 2 -name SKILL.md -print | sort
command -v python3
command -v curl
command -v jq
command -v git
```

If the user needs to install this repo's starter pack into Codex-style local skills manually, give commands like this:

```bash
mkdir -p "$HOME/.codex/skills"
rsync -a start-here/ "$HOME/.codex/skills/starter-pack/"
rsync -a cmc-bnb-skills/cmc-mcp/ "$HOME/.codex/skills/cmc-mcp/"
rsync -a cmc-bnb-skills/cmc-api-crypto/ "$HOME/.codex/skills/cmc-api-crypto/"
rsync -a cmc-bnb-skills/cmc-api-market/ "$HOME/.codex/skills/cmc-api-market/"
rsync -a cmc-bnb-skills/cmc-api-dex/ "$HOME/.codex/skills/cmc-api-dex/"
rsync -a cmc-bnb-skills/crypto-research/ "$HOME/.codex/skills/crypto-research/"
rsync -a cmc-bnb-skills/market-report/ "$HOME/.codex/skills/market-report/"
rsync -a alpha-gen-skills/ohlcv-alpha-research/ "$HOME/.codex/skills/ohlcv-alpha-research/"
```

If the user is not in this repository yet, tell them to clone or download the repo first, then run install commands from the repo root.

## First Two Onboarding Steps

### Step 1: Identify the task lane

Ask or infer which lane the user needs:

```text
A. Current market intelligence or thesis research
B. CMC API quotes, listings, metadata, DEX, or market data
C. Download historical OHLCV data and set up API keys
D. Run OHLCV alpha research or local backtesting
E. Market report generation
F. Custom skill work
```

### Step 2: Confirm required readiness

Use this readiness map:

```text
A needs: starter-pack + cmc-mcp + crypto-research
B needs: starter-pack + relevant cmc-api-* skill + curl + jq + optional CMC_API_KEY
C needs: starter-pack + python3 + provider choice + optional provider API keys
D needs: starter-pack + python3 + normalized OHLCV CSV + ohlcv-alpha-research
E needs: starter-pack + market-report + cmc-mcp + relevant cmc-api-* skill
F needs: starter-pack + python3 + project instructions + explicit user scope
```

If anything is missing, provide only the commands needed to fix that missing piece.

## Data and API Setup

The starter pack owns initial data setup.

Default output for research data is OHLCV-only:

```text
timestamp, open, high, low, close, volume
```

Do not mix news, fundamentals, order book data, social data, market identity, derived features, or future targets into the OHLCV file unless the user explicitly changes scope.

Read `references/providers.md` when choosing a source or explaining key requirements.

Use these bundled scripts:

```text
start-here/scripts/setup_env.py
start-here/scripts/download_ohlcv.py
```

Both scripts write a static HTML report by default:

```text
<output>.report.html
```

Open that report first. It shows what is right, what needs review, what is wrong, written files, and next actions.

### Provider routing

Use this default routing:

```text
Crypto spot, no key:
  Binance public klines first.
  Coinbase Exchange public candles second.
  Kraken public OHLC third.

Crypto market metadata or CMC-specific work:
  CoinMarketCap APIs or CMC MCP, usually with CMC_API_KEY.

US equities / ETFs:
  Polygon or Alpaca when API keys are available.
  Yahoo-style data only if the user accepts unofficial/free-source fragility.

User already has CSV:
  Normalize and validate the CSV instead of downloading again.
```

### Credential rules

Never ask the user to paste secrets into chat if a local env file is enough.

Use local env vars:

```text
CMC_API_KEY
POLYGON_API_KEY
ALPACA_API_KEY_ID
ALPACA_API_SECRET_KEY
TWELVE_DATA_API_KEY
ALPHA_VANTAGE_API_KEY
```

Public Binance, Coinbase Exchange, and Kraken OHLCV endpoints do not need API keys for basic historical candles.

If credentials are missing, create a placeholder `.env` template and tell the user which keys are optional versus required.

### Env setup command

```bash
python3 start-here/scripts/setup_env.py \
  --providers binance coinbase kraken polygon alpaca cmc \
  --output .env.alpha
```

This also writes `.env.alpha.report.html`.

Then load it as needed:

```bash
set -a
source .env.alpha
set +a
```

Do not commit real `.env` files.

### Download commands

Binance public candles:

```bash
python3 start-here/scripts/download_ohlcv.py \
  --provider binance \
  --symbol BTCUSDT \
  --interval 1h \
  --start 2024-01-01 \
  --end 2024-06-01 \
  --output data/BTCUSDT_1h.csv
```

Coinbase public candles:

```bash
python3 start-here/scripts/download_ohlcv.py \
  --provider coinbase \
  --symbol BTC-USD \
  --interval 3600 \
  --start 2024-01-01 \
  --end 2024-06-01 \
  --output data/BTC-USD_1h.csv
```

Kraken public candles:

```bash
python3 start-here/scripts/download_ohlcv.py \
  --provider kraken \
  --symbol XBTUSD \
  --interval 60 \
  --start 2024-01-01 \
  --output data/XBTUSD_1h.csv
```

Polygon keyed aggregates:

```bash
POLYGON_API_KEY=... python3 start-here/scripts/download_ohlcv.py \
  --provider polygon \
  --symbol AAPL \
  --interval 1d \
  --start 2024-01-01 \
  --end 2024-06-01 \
  --output data/AAPL_1d.csv
```

Every successful download should produce exactly:

```text
timestamp,open,high,low,close,volume
```

Every successful download also writes `<output>.report.html` with row count, timestamp order, duplicate checks, OHLCV-structure checks, output path, and next actions.

Store provider metadata separately from the research CSV.

## Routing After Readiness

Once ready, route like this:

```text
Current CMC intelligence, Agent Hub, MCP tools:
  cmc-bnb-skills/cmc-mcp/

Crypto assets, quotes, listings, metadata, key info:
  cmc-bnb-skills/cmc-api-crypto/

Global metrics, Fear and Greed, Altcoin Season, indices, market context:
  cmc-bnb-skills/cmc-api-market/

DEX, DexScan, BSC token/pair/liquidity/security/holder context:
  cmc-bnb-skills/cmc-api-dex/

Research narrative, token thesis, strategy ideation:
  cmc-bnb-skills/crypto-research/

Report generation and sponsor-aligned summaries:
  cmc-bnb-skills/market-report/

OHLCV-only event studies, anomaly ranking, robustness, and alpha cards:
  alpha-gen-skills/ohlcv-alpha-research/
```

## Handoff to OHLCV Alpha Research

After data setup, route to `ohlcv-alpha-research` with:

```text
input_csv:
provider:
symbol:
interval:
start:
end:
known_limitations:
```

Report limitations plainly: missing candles, API caps, adjusted versus unadjusted prices, rate limits, partial current candle, or provider-specific symbol mapping.

## Source Scope

For default OHLCV alpha work, use only:

```text
timestamp
open
high
low
close
volume
```

CMC and other metadata sources may be used for setup, symbol discovery, or reporting only when the task asks for them. They should not be silently merged into OHLCV alpha features.
