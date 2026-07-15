# Applications

Applications are deployable or human-facing entry points. They assemble
workspace packages but do not own reusable math or research logic.

- `research-cli/` — unified Python command interface and integration tests.
- `report-studio/` — Bun/TypeScript browser surface for validated reports.

If code could be reused by a second app, move it to the narrowest package.
