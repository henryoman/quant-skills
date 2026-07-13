# Quant Research Framework

This repository is an active framework for adversarial, reproducible alpha
research. Its purpose is to determine whether market data contains stable,
economically usable information—not to optimize until a backtest looks good.

## Start here

Read the active material in this order:

1. [Research mandate](ADVERSARIAL_QUANT_RESEARCHER.md) — the governing
   epistemic rules and acceptance standard.
2. [Framework guide](framework/README.md) — the research lifecycle and the
   order in which to use the framework chapters.
3. [Research workspace](research/README.md) — where cycles, registered
   experiments, results, and decisions belong.
4. [Source library](docs/README.md) — external references and historical
   provenance.
5. [Reporting standards](standards/reporting/README.md) — how durable evidence
   should be presented.

## Active repository map

```text
.
├── ADVERSARIAL_QUANT_RESEARCHER.md  Governing research mandate
├── framework/                       Methodology, features, validation, templates
├── research/                        New cycles and experiment records
├── docs/                            References and provenance
├── standards/                       Reporting and artifact standards
├── support-skills/                  Optional supporting capabilities
└── _archive_do_not_use/             Frozen legacy material; excluded from use
```

## Authority

When active documents overlap, use this order:

1. The current research question and its frozen data/execution contract.
2. `ADVERSARIAL_QUANT_RESEARCHER.md`.
3. The chapters under `framework/`.
4. Domain-specific extensions.
5. Reporting and visual standards.

Historical provenance records and archived material are not active authority.

## What exists now

- A complete adversarial research mandate.
- Data, labeling, feature, experiment, validation, cost, visualization, and
  asset-extension guidance.
- A broad experiment catalog covering distinct hypothesis families.
- A reusable experiment specification and report template.
- A foundational source list for one-minute BTC OHLCV research.
- A unified reporting design system and domain-specific companions.

## What is not built yet

- A canonical executable research engine.
- A dataset registry and immutable data manifests.
- A machine-readable experiment ledger shared across research cycles.
- A first end-to-end research cycle using the framework.
- Automated leakage, cost, and promotion-gate checks.

Those are implementation tasks, not missing principles. New work should enter
through `research/` so that hypotheses, failed tests, and decisions remain
auditable.

## Archive policy

`_archive_do_not_use/` is retained only to avoid losing earlier work. Do not
search it, cite it, import from it, copy patterns from it, or treat it as current
guidance unless a user explicitly asks for archival review.
