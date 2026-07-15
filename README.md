# Quant Research Monorepo

An adversarial research workspace for testing whether market data contains
stable, executable information. The repository separates scientific rules,
reusable computation, workflow orchestration, machine learning, visualization,
and report applications so each can evolve without becoming one giant script.

It is designed to reject false alpha aggressively. It does not promise profit.

## Where to start

| Goal | Start here |
|---|---|
| Understand the research standard | [`skills/quant-alpha-research/SKILL.md`](skills/quant-alpha-research/SKILL.md) |
| Run or continue empirical work | [`research/README.md`](research/README.md) |
| Add math, indicators, costs, or validation | [`packages/python/quant-core`](packages/python/quant-core) |
| Add research actions or multi-step routines | [`packages/python/quant-research`](packages/python/quant-research) |
| Add PyTorch or another model adapter | [`packages/python/quant-ml`](packages/python/quant-ml) |
| Add renderer-neutral plot contracts | [`packages/python/quant-visuals`](packages/python/quant-visuals) or [`packages/typescript/plotting`](packages/typescript/plotting) |
| Add report components | [`packages/typescript/report-ui`](packages/typescript/report-ui) |
| Build the report application | [`apps/report-studio`](apps/report-studio) |
| Change a cross-language artifact | [`packages/schemas`](packages/schemas) |
| Compare report styles | [`design/OPTIONS.md`](design/OPTIONS.md) |
| Understand all dependency rules | [`docs/architecture/README.md`](docs/architecture/README.md) |

## Repository map

```text
quant-skills/
├── apps/
│   ├── research-cli/        Python command application
│   └── report-studio/       TypeScript/Bun report application
├── packages/
│   ├── python/
│   │   ├── quant-core/      Pure math, indicators, costs, integrity checks
│   │   ├── quant-research/  Actions, routines, cycle state, templates
│   │   ├── quant-ml/        Framework-neutral datasets + optional PyTorch
│   │   └── quant-visuals/   Renderer-neutral evidence/report contracts
│   ├── typescript/
│   │   ├── contracts/       Runtime-facing TypeScript artifact contracts
│   │   ├── plotting/        Plot-spec factories and transformations
│   │   └── report-ui/       Pure report rendering components
│   └── schemas/             Language-neutral JSON Schemas
├── skills/
│   └── quant-alpha-research/ Scientific method, references, thin wrappers
├── research/                Run-specific cycles and empirical artifacts
├── design/                  Current, mellow, and graph-guided comparisons
├── standards/               Reusable reporting standards
├── docs/                    Architecture and provenance documentation
├── tooling/                 Shared compiler/tool configuration
└── _archive_do_not_use/     Frozen history; excluded from active work
```

## Dependency direction

```text
Python
research-cli -> quant-research -> quant-core
             -> quant-visuals
quant-ml     -> quant-core       (PyTorch is an optional extra)

TypeScript
report-studio -> report-ui -> plotting -> contracts
              -> plotting  -> contracts

Cross-language
Python artifact producer -> JSON Schema <- TypeScript artifact consumer
```

Lower layers never import applications, UIs, or workflow actions. Research
results cross language boundaries as validated data, not by importing Python
from TypeScript or TypeScript from Python.

## Setup and verification

The workspace uses Bun/Turborepo for TypeScript and uv workspaces for Python.

```bash
bun install
uv sync --all-packages
bun run check
bun run build
bunx turbo boundaries
```

Install PyTorch only for an experiment that needs it:

```bash
uv sync --extra torch --package quant-ml
```

The default environment intentionally stays light and does not install
PyTorch.

## Run the research CLI

```bash
uv run --package quant-research-cli quant-research --help
uv run --package quant-research-cli quant-research create-cycle --help
```

Skill wrappers remain stable entry points for agents:

```bash
python3 skills/quant-alpha-research/scripts/new_cycle.py --help
python3 skills/quant-alpha-research/scripts/validate_cycle.py --help
```

Create empirical work under `research/cycles/`; never hard-code a cycle path in
a package. Preserve every failed experiment in its ledger.

## Placement rule

Put code in the lowest reusable layer that owns the concept:

- one numerical transformation: `quant-core`;
- one model/framework adapter: `quant-ml`;
- one user-triggered operation: a `quant-research` action;
- a multi-step workflow: a `quant-research` routine;
- a graph description: plotting;
- HTML/components/interactions: report UI or an app;
- a stable data handoff: schemas and contracts;
- scientific instructions for agents: the skill.

Do not add a catch-all `scripts/` directory at the root. A script is either a
thin skill entry point, an app command, or reusable package code.

## Back burner

`_archive_do_not_use/` is intentionally frozen. Active code, documentation,
tests, imports, and research must not read from or depend on it.
