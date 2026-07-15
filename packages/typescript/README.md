# TypeScript packages

Dependency direction, enforced by `turbo boundaries`:

```text
report-ui -> plotting -> contracts
```

- `contracts`: artifact types and lightweight boundary validation.
- `plotting`: renderer-neutral diagnostic plot specifications.
- `report-ui`: safe report rendering and reusable presentation components.

Browser lifecycle and data loading belong in `apps/report-studio`, not these
packages. Statistical conclusions arrive as validated artifacts; UI code does
not recalculate them.
