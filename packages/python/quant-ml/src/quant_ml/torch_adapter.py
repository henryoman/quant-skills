"""Lazy PyTorch capability boundary."""

from __future__ import annotations

import importlib
from typing import Any


class TorchUnavailableError(RuntimeError):
    pass


def require_torch() -> Any:
    """Import PyTorch only when a torch-backed routine is explicitly requested."""
    try:
        return importlib.import_module("torch")
    except ModuleNotFoundError as exc:
        raise TorchUnavailableError(
            "PyTorch is optional. Install the quant-ml 'torch' extra in a dedicated environment."
        ) from exc


def seed_torch(seed: int, *, deterministic: bool = True) -> None:
    torch = require_torch()
    torch.manual_seed(seed)
    if hasattr(torch, "cuda") and torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic and hasattr(torch, "use_deterministic_algorithms"):
        torch.use_deterministic_algorithms(True)
