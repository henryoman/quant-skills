# Active Quant Research Framework

This folder contains the active methodology. The framework is a staged funnel:
audit the data, define what is observable, search broadly, promote sparingly,
try to destroy promoted candidates, and evaluate the frozen procedure once.

The governing standard is
[`ADVERSARIAL_QUANT_RESEARCHER.md`](../ADVERSARIAL_QUANT_RESEARCHER.md).

## Recommended reading order

1. [Data and labels](DATA_AND_LABELS.md) — bar semantics, causal
   transformations, targets, overlap, and chronological splits.
2. [Step-by-step workflow](STEP_BY_STEP_WORKFLOW.md) — the complete research
   sequence from question registration through forward evidence.
3. [Experiment template](EXPERIMENT_TEMPLATE.md) — the required contract for
   every test.
4. [Experiment catalog](EXPERIMENT_CATALOG.md) — broad, logically distinct
   hypothesis families and coarse tests.
5. [Feature library](FEATURE_LIBRARY.md) — interpretable feature definitions,
   interactions, redundancy checks, and ablations.
6. [Validation and costs](VALIDATION_AND_COSTS.md) — leakage controls,
   dependence-aware uncertainty, execution costs, robustness, and promotion
   gates.
7. [Visual guide](VISUAL_GUIDE.md) — the evidence plots required to reveal
   support, instability, concentration, and failure.
8. [Asset extensions](ASSET_EXTENSIONS.md) — declarations required when the
   general framework is applied to a venue or instrument.
9. [Glossary](GLOSSARY.md) — plain-language definitions and formula map.

## Operating lifecycle

```text
research question
  -> data audit and information boundary
  -> target matrix and locked split plan
  -> broad, shallow family coverage
  -> registered candidate promotion
  -> focused refinement
  -> adversarial validation and cost stress
  -> one locked evaluation
  -> reject, gather data, investigate, confirm, or paper trade
```

## Non-negotiable gates

A candidate cannot advance unless its record states:

- when every input becomes observable;
- when and how execution occurs;
- which data influenced feature and parameter selection;
- how overlapping targets and serial dependence are handled;
- how many related variants were tried;
- whether the effect survives time, regimes, nearby parameters, delays, and
  realistic costs;
- whether performance is concentrated in a few observations;
- the exact falsification rule and the next research decision.

## Document roles

The framework chapters are normative methodology. External papers belong in
`docs/references/`. Origin-repository notes belong in `docs/provenance/`.
Experiment-specific hypotheses, configurations, outputs, and decisions belong
in `research/`; do not add one-off findings to these general chapters.
