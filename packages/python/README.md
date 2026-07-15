# Python packages

Dependency direction:

```text
quant-research -> quant-core
quant-ml       -> quant-core
quant-visuals  -> renderer-neutral contracts only
```

- `quant-core`: lightweight math, indicators, economics, and validation.
- `quant-research`: actions, routines, cycle paths, and artifact templates.
- `quant-ml`: framework-neutral model interfaces plus optional adapters.
- `quant-visuals`: Python plot/report contracts and artifact serialization.

Keep PyTorch optional. Keep actions out of numerical packages. Keep empirical
results under `research/`, not package source trees.
