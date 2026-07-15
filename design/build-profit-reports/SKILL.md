---
name: build-profit-reports
description: Build or rewrite dense, decision-ready quantitative research reports that test whether an edge can survive unseen data, costs, delay, concentration, and execution. Use for HTML reports, notebooks, research readouts, backtest reviews, alpha reports, strategy comparisons, parameter studies, trading dashboards converted into durable reports, or any request where weak graphics, bullet-heavy summaries, decorative metrics, or profit claims must be replaced by auditable evidence and one explicit promotion decision.
---

# Build Profit Reports

Produce an evidence instrument, not a presentation. Optimize the report for rejecting false alpha and identifying the next action most likely to improve executable net returns.

## Resolve authority

Treat this skill directory as `<skill-dir>` and resolve all paths from it.

When working in this repository:

1. Read `../../skills/quant-alpha-research/SKILL.md` and its routed active references.
2. Never use `_archive_do_not_use` or historical provenance as active methodology.
3. Use this skill for report selection, evidence density, graphics, and acceptance gates.
4. Use `../report-design.md` for shared implementation details.
5. Use `../report-design-dlmm.md` only for DLMM or execution-specific additions.

This skill overrides softer presentation defaults when they would reduce quantitative evidence density. It never overrides research validity or the frozen experiment contract.

## Load the contracts

Read both references before authoring or materially revising a report:

- [report-contract.md](references/report-contract.md): evidence, structure, writing, promotion, and stop rules.
- [visual-contract.md](references/visual-contract.md): required graphics, chart anatomy, density, and visual QA.

## Start with an evidence inventory

Before writing prose or CSS, identify:

- the decision the report must support;
- the frozen information and execution clocks;
- source artifacts and exact paths;
- train, validation, walk-forward, test, and holdout roles;
- gross and net economics, including every modeled cost;
- effective sample support and dependence;
- experiment count and selection history;
- failure evidence, negative controls, and missing evidence.

Do not invent missing data, charts, thresholds, fills, or conclusions. If required evidence is unavailable, produce the short failure report defined in `report-contract.md`.

## Choose exactly one decision

End with one and only one:

- `reject`
- `diagnostic_only`
- `continue_research`
- `paper_candidate`
- `fillable_candidate`
- `small_live_candidate`

Do not use `paper_candidate` without frozen out-of-sample net evidence. Do not use `fillable_candidate` without quote/depth, latency, fee, rejection, partial-fill, and venue-constraint evidence. Do not use `small_live_candidate` without forward settled results and explicit loss controls.

## Build in this order

1. Freeze the decision question and economic hurdle.
2. Audit sources, clocks, splits, search history, and cost assumptions.
3. Build the evidence tables and graphics before narrative prose.
4. Organize the report around falsification, economics, generalization, and risk.
5. Write interpretations that state what changed, how much, uncertainty, support, decision relevance, and what the evidence does not prove.
6. Remove repeated metrics, generic bullets, decorative cards, and any section that does not change the decision.
7. Render and inspect the actual output at wide, embedded, narrow, and print widths.
8. Reconcile every headline number against its source artifact.
9. Apply the acceptance gate below. Revise until it passes or issue a failure report.

## Enforce the acceptance gate

A report fails if any condition is true:

- The decision is absent, hedged into several options, or unsupported by an explicit gate.
- A profit claim is gross-only, cost-free, in-sample-only, or based on an unrealistic fill clock.
- A chart lacks denominator, sample support, split, unit, cost status, source, or falsification context.
- The report shows only the winning parameter, period, side, asset, regime, or experiment.
- Equity appears without drawdown, exposure, turnover, costs, and concentration.
- Heatmaps omit support, use inconsistent scales across splits, or celebrate isolated hot cells.
- A model appears without baseline, calibration or ranking evidence, unseen-fold behavior, and incremental value.
- Narrative is dominated by bullets, repeated KPI cards, generic observations, or chart descriptions that do not affect a decision.
- Graphics are decorative, fabricated, too small to inspect, or disconnected from source data.
- Negative results, sensitivity failures, or missing evidence are hidden.
- The final recommendation exceeds the achieved evidence gate.

## Keep the output dense and honest

Favor aligned plots, evidence matrices, exact tables, compact captions, and short analytical paragraphs. Do not equate length with rigor. A negative result with insufficient support should be short. A serious candidate should be dense because the evidence battery is dense.

Never promise profit. State whether the evidence moves the candidate closer to or farther from an executable net-profit gate, and name the next falsification test with the highest expected information gain.
