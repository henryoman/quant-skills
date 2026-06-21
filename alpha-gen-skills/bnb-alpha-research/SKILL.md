---
name: bnb-alpha-research
description: Pull real Binance BNB market data and run BNB-specific quantitative anomaly research with event studies, regime splits, heatmaps, and backtestable strategy-candidate JSON. Use when asked to derive BNB alpha, analyze BNBUSDT, produce anomaly heatmaps, test BNB breakout/mean-reversion/volatility patterns, or prepare a CMC/BNB Track 2 strategy spec from real free market data.
---

# BNB Alpha Research Skill

Use this skill after `starter-pack` confirms Python is available and the source policy is CMC/Binance only.

This is the BNB-specific quant lab. It is not a role file and it is not a market-commentary prompt. It owns one measurable workflow:

```text
pull BNB/BTC/ETH candles -> clean candles -> compute past-only features
-> scan BNB anomaly events -> build heatmaps -> emit candidate strategy specs
```

## Source Scope

Allowed:

```text
Binance public spot or USD-M futures klines for historical candles
Binance US public spot klines as a fallback when global Binance returns HTTP 451
CMC MCP/API for current context, provenance, and sponsor-aligned market intelligence
```

Do not use competitor APIs or unofficial scrapers for this project.

## First Command

For a real BNB pull:

```bash
uv run --with pandas --with numpy \
  alpha-gen-skills/bnb-alpha-research/scripts/bnb_alpha_pipeline.py \
  --market spot \
  --symbols BNBUSDT BTCUSDT ETHUSDT \
  --target-symbol BNBUSDT \
  --interval 1h \
  --start 2024-01-01 \
  --end 2024-06-01 \
  --output-dir research/bnb-alpha
```

For offline verification without network:

```bash
uv run --with pandas --with numpy \
  alpha-gen-skills/bnb-alpha-research/scripts/bnb_alpha_pipeline.py \
  --make-example \
  --output-dir /tmp/bnb-alpha-example
```

## Output Contract

The pipeline writes:

```text
raw/<market>/<symbol>/<interval>.csv
clean/<market>/<symbol>/<interval>.csv
analysis/features_BNBUSDT.csv
analysis/event_studies.csv
analysis/heatmap_edge_bps.csv
analysis/heatmap_hit_delta.csv
analysis/heatmap_regime_edge_bps.csv
analysis/calendar_heatmap_fwd_24h_bps.csv
analysis/anomaly_latest_snapshot.json
analysis/strategy_candidates.json
reports/bnb_alpha_report.html
```

Open `reports/bnb_alpha_report.html` first. It shows data quality, strongest events, edge heatmaps, hit-rate heatmaps, regime heatmaps, calendar heatmaps, and generated strategy candidates.

## Quant Rules

- Every feature must be known at the close of the current bar.
- Every target must be measured after the current bar.
- Compare event rows to unconditional baseline rows at the same horizon.
- Treat heatmaps as exploratory evidence, not proof.
- Reject events with tiny samples, one-threshold dependence, or cost-fragile edges.
- Strategy candidates must include deterministic entry, exit, risk, backtest, and provenance fields.

## Handoff

After this skill produces `strategy_candidates.json`, hand off to:

```text
cmc-bnb-skills/bnb-project-foundation/
```

Use the candidate JSON as the quantitative evidence layer for a CMC Track 2 backtestable strategy spec.
