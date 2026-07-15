"""Safe cycle-local paths and packaged templates."""

from importlib.resources import files
from pathlib import Path


TEMPLATES_ROOT = files("quant_research.templates")


def resolve_cycle_path(cycle: str | Path, relative_path: str | Path) -> Path:
    """Resolve a cycle-local path and reject traversal outside the cycle."""
    root = Path(cycle).expanduser().resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes cycle directory: {relative_path}") from exc
    return candidate
