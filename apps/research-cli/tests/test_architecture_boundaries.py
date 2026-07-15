from __future__ import annotations

import ast
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

PACKAGE_RULES = {
    "packages/python/quant-core/src": {
        "quant_research",
        "quant_ml",
        "quant_visuals",
        "research_cli",
    },
    "packages/python/quant-research/src": {
        "quant_ml",
        "quant_visuals",
        "research_cli",
    },
    "packages/python/quant-ml/src": {
        "quant_research",
        "quant_visuals",
        "research_cli",
    },
    "packages/python/quant-visuals/src": {
        "quant_core",
        "quant_research",
        "quant_ml",
        "research_cli",
    },
}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_python_dependency_direction(self) -> None:
        violations: list[str] = []
        for relative_root, forbidden in PACKAGE_RULES.items():
            for path in sorted((REPO_ROOT / relative_root).rglob("*.py")):
                invalid = imported_roots(path) & forbidden
                if invalid:
                    violations.append(f"{path.relative_to(REPO_ROOT)} imports {sorted(invalid)}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
