# BNB Project Foundation - Track 2 Strategy Skill

This folder is the foundation package for **BNB Hack Track 2: Strategy Skills**.

The goal is **not** to build a live trading bot. The goal is to build a **CoinMarketCap Skill** that turns market data into a **backtestable strategy spec**.

## The simplest winning direction

Build one Skill:

```txt
CMC market data
  -> indicators / regime detection
  -> choose strategy type
  -> output deterministic strategy JSON
  -> optional backtest using free OHLCV
```

Recommended project name:

```txt
Volatility Regime Strategy Skill
```

It should generate strategies like:

- volatility breakout
- mean reversion
- expected range / DLMM-style range
- binary up/down probability

## What to submit

Minimum submission package:

1. Public GitHub/GitLab/Bitbucket repo
2. `skill/SKILL.md`
3. Demo video or demo instructions
4. Example generated strategy specs
5. Clear explanation of what data is real, cached, fixture, or synthetic

## What not to build

For Track 2, do **not** build:

- wallet execution
- private key handling
- Trust Wallet signing
- PancakeSwap swap routing
- BSC live trading bot
- gas optimization
- real-money trading loop

Those are Track 1 concerns.

## Files in this starter

```txt
README.md                                  overview
.env.example                               optional local environment values
package.json                               Bun demo command
skill/SKILL.md                             skill instructions
skill/scripts/generate-strategy.ts         tiny TypeScript strategy shell
skill/scripts/types.ts                     strategy types
skill/examples/bnb-strategy.example.json   sample output
skill/references/build-outline.md          simple build plan
skill/references/contest-parameters.md     exact contest rules / requirements
skill/references/data-options.md           CMC/free/mock data options
skill/references/sources.md                source links checked
```

Run the demo shell with:

```bash
bun run strategy
```
