---
name: quant-skills-instructions
description: First-read routing skill for this quant-skills repository. Use when onboarding into the repo, deciding which quant skill to invoke, installing local skills, or finding the correct path from project instructions to starter-pack to BNB/CMC/alpha research workflows.
---

# Quant Skills Instructions

Use this skill first when it is installed.

It routes the agent into the right local instruction layer without loading every quant reference file.

## Reading Order

1. Read root `instructions.md` for repository layout, source policy, and research standard.
2. Use `start-here/` for readiness checks, provider setup, and lane routing.
3. Choose exactly one specialized skill for the current task.

## Specialized Routing

```text
Need data/API setup:
  start-here/

Need Binance raw and clean data files:
  alpha-gen-skills/data-download-clean/

Need BNB-specific alpha with anomaly heatmaps:
  alpha-gen-skills/bnb-alpha-research/

Need generic OHLCV event-study research:
  alpha-gen-skills/ohlcv-alpha-research/

Need CMC/BNB Track 2 strategy-spec packaging:
  cmc-bnb-skills/bnb-project-foundation/

Need CMC current market context:
  cmc-bnb-skills/cmc-mcp/
```

## Rule

Do not create more role files. Prefer scripts for deterministic data pulls, feature engineering, event studies, heatmaps, and candidate JSON.
