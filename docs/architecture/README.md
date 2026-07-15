# Monorepo Architecture

## Non-negotiable boundaries

1. Apps assemble packages; packages never import apps.
2. Workflows use quantitative primitives; primitives never know a workflow.
3. Machine-learning frameworks are adapters, not the foundation of the repo.
4. Plotting describes evidence; it does not calculate research conclusions.
5. UI renders validated artifacts; it does not recompute alpha.
6. Cross-language handoffs use schemas, not implementation imports.
7. Run-specific findings belong in `research/cycles`, never reusable packages.

## Package ownership matrix

| Concern | Owner | May depend on | Must not depend on |
|---|---|---|---|
| Returns, rolling math, indicators | `quant-core` | Python standard library | workflow, ML, UI |
| Costs and integrity checks | `quant-core` | Python standard library | app state, rendering |
| Cycle actions and routines | `quant-research` | `quant-core` | TypeScript/UI |
| Model datasets and adapters | `quant-ml` | `quant-core`, optional framework | actions, UI |
| Python evidence specs | `quant-visuals` | stable data contracts | research actions |
| TS artifact types | `@quant/contracts` | nothing internal | plotting, UI, app |
| TS plot factories | `@quant/plotting` | contracts | UI, app |
| Report components | `@quant/report-ui` | contracts, plotting | app startup |
| Browser application | `@quant/report-studio` | UI and lower TS layers | Python internals |
| Agent research protocol | skill | stable CLI wrappers/references | run findings |

## Add a new capability

### Indicator or mathematical transform

Add it to the relevant `quant_core` concept module, register its observability
metadata when it is a feature, test invalid/warm-up behavior, then compose it in
`quant_research.routines.feature_pipeline` only if it belongs in the baseline.

### Research command

Implement an action with a callable `main`, compose reusable behavior in a
routine, register it in `apps/research-cli`, and add a thin skill wrapper only
if agents need that direct command.

### PyTorch model

Keep chronological splits and window alignment framework-neutral in `quant-ml`.
Put tensor/model/training behavior in a dedicated adapter that calls
`require_torch()`. Tests for the default workspace must not require PyTorch.

### New graph

Define the evidence fields in a plot spec, include support and uncertainty,
implement a renderer-neutral factory, then render it in report UI. If the
artifact crosses languages, update its JSON Schema and both contract tests.

### New frontend surface

Reuse `@quant/report-ui` and plotting contracts. Keep routing, loading, and
browser state in an app. A frontend must display exact scope, costs, support,
uncertainty, and limitations supplied by research artifacts.

## Verification gates

```bash
uv run python -m unittest discover -s apps/research-cli/tests -v
bun run typecheck
bun run test
bun run build
bunx turbo boundaries
```

Turborepo enforces TypeScript package directions. Python import directions are
kept shallow, exercised through package-level tests, and documented here so a
future static dependency checker can be added without reorganizing again.
