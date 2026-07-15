# Code Architecture

## Purpose

The skill specifies how research must be performed; the monorepo packages
implement reusable capabilities. Keep scientific rules, quantitative
computation, orchestration, machine-learning frameworks, artifact contracts,
and presentation independently testable.

## Dependency direction

```text
skills/quant-alpha-research/scripts
  -> apps/research-cli or quant_research.actions
      -> quant_research.routines
          -> quant_core

quant_ml -> quant_core
quant_visuals -> no research workflow dependency

report-studio -> report-ui -> plotting -> contracts

Python producer -> packages/schemas -> TypeScript consumer
```

Quantitative packages never import UI packages. Pure math never imports an
action or routine. PyTorch is loaded only through `quant_ml.torch_adapter` when
explicitly requested.

## Python areas

### `packages/python/quant-core/`

Own dependency-light numerical primitives:

- `math/`: returns, rolling operations, statistics;
- `indicators/`: causal, interpretable market-state transformations;
- `economics/`: costs and trade-level economic metrics;
- `validation/`: information clocks and reusable integrity checks.

An indicator must state its last observable timestamp, normalization, warm-up,
parameters, and invalid-data behavior. This package must remain usable without
Pandas, PyTorch, a CLI, or a frontend.

### `packages/python/quant-research/`

Own the research process:

- `actions/`: one user-triggered operation, argument parsing, file boundaries;
- `routines/`: multi-step workflows expressed with ordinary Python values;
- `core/`: cycle paths and workflow-level contracts;
- `templates/`: registered-cycle artifacts.

Actions may call routines and `quant-core`. Lower layers never call actions.

### `packages/python/quant-ml/`

Own framework-neutral dataset/model protocols and optional framework adapters.
Core alignment, split, and window logic must work without PyTorch. Import
PyTorch lazily and keep it behind an optional dependency group.

### `packages/python/quant-visuals/`

Own renderer-independent plot and report evidence contracts. It may translate
Python values to the shared camelCase artifacts, but it must not recompute an
experiment or define a trading policy.

### `apps/research-cli/`

Own the unified human-facing command. It depends on packages and contains
integration tests; reusable research logic does not live here.

## TypeScript areas

### `packages/typescript/contracts/`

Own TypeScript types and lightweight validation for artifacts defined by
`packages/schemas`. It has no internal workspace dependencies.

### `packages/typescript/plotting/`

Own plot-spec factories and transformations. It consumes contracts and remains
independent of the DOM and any chart renderer.

### `packages/typescript/report-ui/`

Own report components and safe HTML/rendering behavior. It consumes contracts
and plotting but never owns statistical calculations.

### `apps/report-studio/`

Own browser startup, data loading, routing, interactions, and exports. App-only
behavior stays here.

## Cross-language contracts

`packages/schemas/json/` is authoritative at process and language boundaries.
Python serializes an artifact; TypeScript validates and renders it. Do not copy
business logic between languages to make two almost-compatible formats.

## Extension rules

1. Put a pure numerical operation in `quant-core` and test boundary cases.
2. Put model integration in `quant-ml`; keep preprocessing framework-neutral.
3. Compose reusable operations in a `quant-research` routine.
4. Expose a user operation through an action and the unified CLI.
5. Add a thin skill wrapper only when agents need a stable direct entry point.
6. Express graphs as plot specs and interfaces as report UI/app code.
7. Update a shared schema before relying on a new cross-language field.
8. Run Python tests, TypeScript checks, builds, and Turbo boundaries.

Do not create generic `utils.py`, `helpers.ts`, or root scripts. Name a module
after the concept it owns. Do not read archived code to seed a new module.
