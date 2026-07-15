# Profit-report evidence contract

## Contents

1. Purpose
2. Required report architecture
3. Writing rules
4. Evidence scorecard
5. Economic and statistical gates
6. Short failure report
7. Final acceptance audit

## 1. Purpose

Build the smallest report that exposes all evidence needed to accept, reject, or advance a trading candidate. Information density is decision-relevant evidence per unit of reader attention. It is not more prose, more cards, smaller charts, or more metrics.

Every section must answer at least one question:

- Is the data valid and the information boundary causal?
- Does a conditional distribution differ from its baseline?
- Does the effect survive unseen time and the complete selection procedure?
- Is the effect net positive after conservative execution assumptions?
- Is it stable across nearby choices, regimes, sides, folds, and perturbations?
- Is profit concentrated, capacity-limited, or explained by drift, beta, leverage, volatility, or tail risk?
- What exact decision follows?

Delete a section that answers none of these.

## 2. Required report architecture

### 2.1 Decision header

Open with a compact header, not a marketing hero. Include:

- exact candidate and evaluation period;
- one decision label;
- one-sentence reason;
- achieved promotion gate;
- frozen execution and all-in cost assumption;
- source artifact or cycle identifier.

Do not open with generic bullets or a row of oversized vanity KPIs.

### 2.2 Evidence scorecard

Use one dense table near the top:

| Gate | Required evidence | Observed result | Threshold | Status | Main failure risk |
|---|---|---:|---:|---|---|
| Data and clocks | Audit, causal clock, no forbidden overlap | | | | |
| Conditional information | Effect versus unconditional/simple baseline | | | | |
| Unseen-time survival | Frozen walk-forward/test result | | | | |
| Net economics | Net edge after cost, delay, impact, margin | | | | |
| Stability | Folds, nearby parameters, regimes, sides | | | | |
| Risk and concentration | Drawdown, tails, top-N and bucket share | | | | |
| Operational evidence | Fill, latency, capacity, venue constraints | | | | |

Every threshold must be frozen before the evaluation it judges. If a threshold is unavailable, mark the gate unresolved; do not choose one from the displayed test result.

### 2.3 Data and evaluation contract

State exact paths, hashes when available, UTC range, row/event/trade counts, unique periods or markets, missingness, repairs, timestamp semantics, feature cutoff, decision time, earliest executable fill, exit clock, overlap, splits, purge, embargo, cost units, and holdout status.

Use a compact table. Do not bury these facts in prose.

### 2.4 Conditional information

Show the unconditional baseline before the candidate. Then show the conditional distribution, uncertainty, effective support, and simple alternatives. Separate descriptive association from a trade policy.

State which effect was expected before results, how many related variants were tested, and whether the displayed rule was frozen before the evaluation split.

### 2.5 Unseen-time generalization

Show every meaningful unseen fold, not only the aggregate. Include failed folds, no-trade folds, fixed-baseline performance, and selection-procedure performance. Report worst fold and fold dispersion alongside the average.

### 2.6 Net economics

Lead with net, not gross. Reconcile:

```text
gross edge
- fees
- spread
- slippage
- funding or borrow
- market impact
- latency or delay loss
- estimation safety margin
= decision-grade net edge
```

Show gross only to attribute where the edge is consumed. Report break-even cost, break-even delay, turnover, exposure, concurrency, capacity assumption, and size sensitivity.

### 2.7 Robustness and falsification

Show the complete local parameter neighborhood, time/regime/side slices, cost and delay stresses, top-N removal, leave-one-bucket-out tests, simple baselines, and negative controls. Put failures next to successes.

### 2.8 Risk and concentration

Report maximum drawdown, recovery duration, worst trade/bar/day, expected shortfall or declared tail statistic, MAE/MFE when available, top 1/5/10 trade contribution, period/side/asset/regime contribution, exposure, leverage, and liquidity/capacity limits.

### 2.9 Decision and next falsification test

Close with exactly one decision label. State:

- what evidence earned that label;
- what blocks the next gate;
- one next falsification test;
- its frozen success and failure thresholds;
- required new independent support;
- the action if the test fails.

Rank work by expected information gain and economic relevance, not by the most attractive possible PnL.

### 2.10 Reproducibility and provenance

List source files, experiment and variant IDs, code paths, configuration, timestamps, cost assumptions, exclusions, and output artifacts. Every headline number and chart must trace to a source.

## 3. Writing rules

Use analytical prose, exact tables, and figure captions. Do not produce a bullet-summary report.

- Never use bullets for the executive conclusion.
- Use a list only for a genuinely parallel set or a procedural checklist.
- Limit an ordinary list to five items; move larger comparisons into a table.
- Do not repeat the same number in a card, paragraph, chart title, and table.
- Do not write generic observations such as “performance varies,” “results are promising,” or “risk should be monitored.” Quantify the variation, evidence, and decision effect.
- Do not narrate chart geometry without interpretation. State magnitude, uncertainty, support, economic relevance, and limitation.
- Use short paragraphs with one claim each.
- Use declarative section headings tied to decisions or falsification questions.
- Replace “strong,” “robust,” “significant,” and “profitable” with measured evidence and the achieved gate.
- Preserve negative results and conflicting evidence at equal visual prominence.

## 4. Evidence scorecard rules

Every headline result must disclose:

| Dimension | Required disclosure |
|---|---|
| Population | Asset, venue, period, timezone, eligibility |
| Support | Raw rows, trades/events, effective count, unique periods/markets |
| Split | Train, validation, fold, untouched test, locked holdout, or forward |
| Selection | Hypothesis timing, variants tried, rule-freeze point |
| Economics | Gross/net, cost components, delay, size, safety margin |
| Uncertainty | Method, interval, dependence treatment |
| Concentration | Top-N, worst bucket, leave-one-out behavior |
| Comparators | Unconditional, random, simple, prior policy |
| Falsification | Observation that would reject or downgrade the claim |
| Provenance | Exact source artifact and generation path |

If the report cannot fill these fields, it cannot present the result as decision-grade.

## 5. Economic and statistical gates

### Reject or downgrade immediately when

- test selection contaminated the evaluation;
- fill timing uses information unavailable at order time;
- net edge is nonpositive under the conservative base case;
- a small cost or delay change destroys the effect;
- profit is owned by a few observations or one regime;
- neighboring parameters reverse sign;
- effective support is inadequate;
- unseen folds conflict materially;
- multiple-testing treatment makes evidence inconclusive;
- the result does not beat a simpler baseline;
- execution, capacity, or fill evidence is absent for the claimed gate.

### Do not let one metric dominate

Sharpe, total PnL, win rate, accuracy, AUC, and a p-value are never sufficient alone. Pair performance with net expectancy, uncertainty, drawdown, tails, support, fold behavior, concentration, costs, and implementation constraints.

### Scope language to the evidence

Use only the active framework’s evidence classifications. Never call a strategy proven. Never convert a backtest directly into a live recommendation.

## 6. Short failure report

When the inputs cannot support a serious report, stop instead of manufacturing density. Produce at most four sections:

1. **Decision:** `reject`, `diagnostic_only`, or `continue_research`.
2. **Blocking evidence table:** missing or invalid item, why it matters, and exact remedy.
3. **What can still be concluded:** only claims supported by current evidence.
4. **Next falsification test:** one bounded test with frozen pass/fail criteria.

Do not add filler charts, speculative recommendations, generic bullet lists, or decorative design.

## 7. Final acceptance audit

Before delivery, answer yes to every applicable item:

- Does the first viewport state one decision, achieved gate, cost basis, and primary reason?
- Can every number and visual be traced to a source artifact?
- Are clocks, splits, overlap, purge, embargo, and holdout status explicit?
- Are gross and net economics reconciled?
- Are uncertainty, effective support, and search size visible?
- Are all folds, nearby parameters, costs, delays, sides, regimes, and concentration risks shown?
- Are failures and negative controls as visible as successes?
- Does every graphic change or test a decision?
- Is narrative mostly paragraphs, tables, and captions rather than bullets?
- Is the recommendation no stronger than the achieved gate?
- Does the report end with one falsifiable next action?

Any “no” is a delivery blocker unless the report explicitly downgrades itself and explains the missing evidence.
