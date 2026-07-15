"""Load Python workspace packages when the skill is used without installation."""

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOTS = (
    REPO_ROOT / "packages/python/quant-core/src",
    REPO_ROOT / "packages/python/quant-research/src",
    REPO_ROOT / "packages/python/quant-visuals/src",
    REPO_ROOT / "packages/python/quant-ml/src",
    REPO_ROOT / "apps/research-cli/src",
)


def load_workspace() -> None:
    for source_root in reversed(SOURCE_ROOTS):
        value = str(source_root)
        if value not in sys.path:
            sys.path.insert(0, value)
