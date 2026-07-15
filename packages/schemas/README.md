# Shared artifact contracts

This directory is the language-neutral boundary between research producers and
report consumers. Python may create these artifacts; TypeScript may validate,
render, or transport them. Neither language package may depend on the other's
implementation.

Active schemas:

- `json/plot-spec.schema.json` — one evidence visualization and its reading aid.
- `json/report-document.schema.json` — a decision report with preserved failures.
- `json/research-cycle.schema.json` — the stable identity and safety fields of a
  registered research cycle. The full cycle validator remains in
  `quant-research` because stage-specific invariants are executable rules.

Schema evolution rules:

1. Add fields compatibly when possible.
2. Change required fields only with a versioned migration.
3. Keep statistical values and provenance as data, never embedded display text.
4. Validate at the artifact boundary, not inside plotting or UI code.
