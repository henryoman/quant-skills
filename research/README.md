# Research Workspace

This is the active workspace for applying the framework. Keep reusable
methodology in `framework/`; keep empirical claims and run-specific artifacts
here.

## Structure

Create folders only when work begins:

```text
research/
├── cycles/<cycle-id>/
│   ├── DATA_CARD.md
│   ├── TARGET_MATRIX.md
│   ├── HYPOTHESIS_LEDGER.csv
│   ├── DECISION.md
│   └── experiments/<experiment-id>/
│       ├── HYPOTHESIS.md
│       ├── config.yaml
│       ├── src/
│       ├── results/
│       └── REPORT.md
└── README.md
```

Use `YYYYMMDD-asset-interval-question` for a cycle ID and a stable family code
plus a short name for an experiment ID, for example `B01-momentum-coarse`.

## Cycle contract

Before signal testing, a cycle must freeze:

- asset, venue, bar semantics, date range, and input fields;
- data-quality findings and documented repairs;
- observation, decision, order, and execution times;
- target definitions and overlap structure;
- training, validation, walk-forward, and locked-holdout boundaries;
- initial hypothesis-family search budget;
- cost and execution assumptions;
- promotion, rejection, and stop rules.

## Experiment contract

Every experiment must begin with the hypothesis card defined by the research
mandate and a configuration recording all variants. Results must include failed
variants, uncertainty, support, time/regime breakdowns, cost relevance, and the
decision reached. Never overwrite an earlier result to make a later run look
like the original test.

## Cycle completion

Close every cycle with the required data card, target matrix, hypothesis
ledger, broad experiment matrix, candidate cards, rejected ideas, exactly one
research decision, and next experiments ranked by expected information gain.
