---
name: quant-alpha-research
description: Run adversarial, leakage-safe quantitative alpha research on OHLCV or related market data. Use when creating a research cycle, auditing price data, defining causal features and targets, registering hypotheses, testing predictive information, validating a trading candidate chronologically, modeling fees and execution, preserving failed experiments, or deciding whether an effect is rejected, informative, paper-tradeable, or a candidate executable alpha.
---

# Quant Alpha Research

Find conditional information that can survive unseen time and realistic
execution. Do not promise profit or optimize toward a pretty backtest. Make
economic usability a hard gate: an effect must survive costs, delay, uncertainty,
concentration, and alternative explanations.

## Resolve paths safely

Treat the directory containing this `SKILL.md` as `<skill-dir>`. Resolve every
script, asset, and reference relative to `<skill-dir>`, never relative to the
user's current working directory. Store paths inside cycle manifests relative to
the cycle directory. Reject references to `_archive_do_not_use`.

Read [code-architecture.md](references/code-architecture.md) before adding or
changing code. Put CLI parsing in actions, orchestration in routines,
quantitative computation in `quant-core`, optional frameworks in `quant-ml`,
chart contracts in plotting packages, and report behavior in UI/app packages.

## Begin every task

1. Read [research-mandate.md](references/research-mandate.md).
2. Read [data-and-labels.md](references/data-and-labels.md) before touching data,
   features, targets, splits, or execution clocks.
3. Read [workflow.md](references/workflow.md) before creating or continuing a
   full research cycle.
4. State the current stage, frozen information boundary, and next falsifiable
   decision.

Do not begin alpha testing before a documented data audit. Do not open a locked
holdout before freezing the full selection and execution procedure.

## Create a registered research cycle

Run:

```text
python3 <skill-dir>/scripts/new_cycle.py \
  --cycle-id 20260713-btcusdt-1m-conditional-alpha \
  --asset BTCUSDT \
  --venue binance-spot \
  --interval 1m \
  --objective "Test whether causal OHLCV states change executable future outcomes" \
  --data-path data/btcusdt-1m.csv \
  --fee-bps-per-side 1.0 \
  --spread-bps-round-trip 0.5 \
  --slippage-bps-round-trip 0.5
```

The tool creates a manifest, data card, target matrix, hypothesis and experiment
ledgers, broad experiment matrix, decision record, sealed-holdout marker, and
separate experiment/result directories. It predeclares return, direction,
future-range, and adverse-excursion targets across coarse horizons.

Treat generated placeholders as unresolved research obligations, not boilerplate
to ignore.

## Audit OHLCV data

Run:

```text
python3 <skill-dir>/scripts/audit_ohlcv.py <csv-path> \
  --interval 1m \
  --interval-label 1m \
  --timestamp-semantics open_time \
  --cycle <cycle-dir> \
  --output-dir <cycle-dir>/results/data-audit
```

Use the generated JSON and Markdown to fill `DATA_CARD.md`. The optional cycle
argument verifies the audited path, records its hash and audit status, and does
not approve or repair it. Document every repair proposal, affected row count,
and possible research impact. Do not let a script silently mutate source data.

Build the initial past-only feature matrix after accepting the audit:

```text
python3 <skill-dir>/scripts/build_features.py <audited-ohlcv.csv> \
  --output <experiment-dir>/results/features.csv \
  --lookbacks 5,15,60
```

Use the output as a causal baseline feature set: normalized candle geometry,
trailing return, path efficiency, relative volume, range position, and realized
volatility. Add new features through the modular indicator layer, not inside the
CLI.

## Freeze the economic and information contracts

Before feature testing, fill `cycle.json` with:

- bar timestamp semantics and feature cutoff;
- decision, order, execution, and exit clocks;
- chronological train, validation, walk-forward, purge, embargo, and locked
  holdout boundaries;
- fee, spread, slippage, funding, borrow, impact, and estimation-margin inputs;
- target horizons and overlap structure;
- total variant cap, per-family cap, and applicable hypothesis families.

Use a conservative default: observe completed bar `t`, decide afterward, and
execute no earlier than bar `t+1` open. If using another convention, prove it is
executable.

## Register hypotheses before results

Read [experiment-catalog.md](references/experiment-catalog.md) to cover broad,
logically distinct families. Read [feature-library.md](references/feature-library.md)
only after selecting a family.

Register each hypothesis with:

```text
python3 <skill-dir>/scripts/new_experiment.py \
  --cycle <cycle-dir> \
  --id B01-momentum-coarse \
  --name "Coarse continuation" \
  --observable-state "Past-only return over 5, 15, and 60 bars" \
  --future-outcome "Executable log return at registered horizons" \
  --expected-relationship "Larger positive formation return shifts future return upward" \
  --falsification-test "Reject if signs reverse across ordinary folds or net effect is below costs" \
  --promotion-criteria "Same sign in at least 70% of test folds, smooth neighboring horizons, adequate support, and net-positive lower confidence bound" \
  --variant-cap 12
```

Keep every run in `EXPERIMENT_LEDGER.csv`, including failed variants. Never
replace a registered hypothesis with the explanation suggested by its result.

## Search broadly before refining

Use model-free conditional profiles first:

1. Establish unconditional drift, distribution, dependence, seasonality, and
   volatility structure.
2. Use training-defined bins to measure count, mean, median, quantiles, hit rate,
   tails, uncertainty, and turnover implications.
3. Cover every applicable family without giving any family more than 20% of the
   initial variant budget.
4. Compare every candidate with unconditional, random, drift, previous-sign,
   simple threshold, and simple linear baselines.
5. Promote only broad, stable regions with adequate support and economically
   meaningful effect size.

Read [experiment-template.md](references/experiment-template.md) for the full
experiment contract.

## Translate information into executable value

Separate four possible products:

- directional entry or exit information;
- trade filtering and adverse-selection avoidance;
- volatility/range forecasts for sizing;
- conditional risk forecasts for exposure reduction.

Estimate conditional outcome distributions before defining a strategy. Require:

```text
expected gross edge > fee + spread + slippage + funding/borrow + impact + safety margin
```

Attribute apparent profit to drift, beta, volatility exposure, leverage, tail
risk, and selection before calling it alpha. Report gross and net effects, long
and short results, exposure, turnover, capacity assumptions, adverse excursion,
and concentration.

For a trade-level CSV containing `gross_return_bps` and `side`, run:

```text
python3 <skill-dir>/scripts/evaluate_trades.py <trades.csv> \
  --output-dir <experiment-dir>/results/trade-evaluation \
  --fee-bps-per-side 1.0 \
  --spread-bps-round-trip 0.5 \
  --slippage-bps-round-trip 0.5 \
  --impact-bps-per-trade 0.2 \
  --safety-margin-bps 0.5
```

Use its gross/net expectancy, dependence-aware interval, long/short split,
drawdown, concentration, break-even cost capacity, and cost stress as economic
evidence. Do not let trade-level profitability bypass selection or leakage
validation.

## Validate adversarially

Read [validation-and-costs.md](references/validation-and-costs.md). Apply:

- chronological walk-forward selection;
- purge and embargo for overlapping labels;
- train-only normalization, feature selection, thresholds, regimes, and models;
- dependence-aware intervals and effective observation counts;
- explicit multiple-testing correction against the complete ledger;
- nearby-parameter, time, regime, direction, delay, cost, outlier, and
  leave-one-period-out stress tests;
- simple-baseline and negative-control comparisons.

Use [visual-guide.md](references/visual-guide.md) to show support, uncertainty,
parameter plateaus, fold dispersion, cost-delay sensitivity, drawdown, and
concentration. A graph must expose how a candidate fails, not only how its best
region performs.

Validate the cycle at any point:

```text
python3 <skill-dir>/scripts/validate_cycle.py <cycle-dir>
python3 <skill-dir>/scripts/validate_cycle.py <cycle-dir> --strict
```

The validator checks required artifacts, relative paths, costs, target diversity,
purge/embargo, sealed-holdout integrity, family coverage, variant budgets,
registered experiments, archive contamination, and the single-decision rule.

## Open the holdout once

Open the locked holdout only after:

- data transformations, features, targets, parameters, policy, costs, and
  reporting are frozen;
- ledgers match all work performed;
- promotion criteria are already written;
- the cycle validator has no errors.

Set `cycle.json` status to `frozen`, set `search_budget.stage` to
`locked_evaluation`, and run:

```text
python3 <skill-dir>/scripts/open_holdout.py <cycle-dir> --procedure-frozen
```

The command refuses incomplete cycles, hashes the frozen procedure, records the
opening event, and removes the sealed marker. If the holdout fails, record
failure. Do not tune on it or quietly create a new test from the remaining tail.

## Close the cycle

Produce the mandate's data card, information boundary, target matrix, hypothesis
ledger, broad experiment matrix, candidate cards, rejected ideas, and ranked
next tests. Select exactly one decision in `DECISION.md`:

- stop;
- gather more data;
- change target or horizon;
- investigate one candidate;
- run a locked confirmation;
- begin paper trading.

Use only these evidence classifications: rejected, inconclusive, interesting but
not tradable, predictive but economically weak, conditionally useful, or
candidate executable alpha. Never call an effect proven.

## Load references only when needed

- Use [asset-extensions.md](references/asset-extensions.md) for venue,
  instrument, derivative, or cross-asset additions.
- Use [glossary.md](references/glossary.md) for formulas and evidence terms.
- Use [btc-1m-sources.md](references/btc-1m-sources.md) for BTC one-minute
  literature and implementations.
- Use [foundational-ohlcv-sources.md](references/foundational-ohlcv-sources.md)
  for broader OHLCV methods and scientific tools.

External sources generate tests; they do not transfer empirical validity to the
current asset, venue, period, or execution model.
