#!/usr/bin/env python3
"""Stable entrypoint for the register-experiment action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.register_experiment import main


if __name__ == "__main__":
    raise SystemExit(main())
