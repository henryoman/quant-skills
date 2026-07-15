---
name: bnb-project-foundation
description: CMC/BNB Track 2 foundation skill for turning BNB quantitative evidence into a sponsor-aligned, backtestable strategy spec. Use after bnb-alpha-research generates anomaly heatmaps and strategy_candidates.json, or when packaging CoinMarketCap/BNB source policy, provenance, and submission-ready strategy JSON.
---

# BNB Project Foundation

Use this after quantitative evidence exists.

This skill packages BNB alpha evidence into a CMC Track 2 strategy-skill deliverable. It does not discover anomalies itself. For discovery, use:

```text
alpha-gen-skills/bnb-alpha-research/
```

## Inputs

Expected evidence files:

```text
analysis/event_studies.csv
analysis/heatmap_edge_bps.csv
analysis/heatmap_hit_delta.csv
analysis/heatmap_regime_edge_bps.csv
analysis/strategy_candidates.json
reports/bnb_alpha_report.html
```

## Workflow

1. Read `analysis/strategy_candidates.json`.
2. Select only candidates with enough sample size, nontrivial edge, and clear provenance.
3. Convert the candidate into deterministic strategy JSON.
4. Add CMC/Binance source provenance.
5. State that this is a backtestable strategy spec, not a live execution agent.

## Bundled Starter

The original Track 2 starter implementation is under:

```text
skill/
```

Read `skill/SKILL.md` only when you need the TypeScript demo shell or original contest packaging notes.
