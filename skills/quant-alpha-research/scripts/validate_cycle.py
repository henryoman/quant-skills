#!/usr/bin/env python3
"""Stable entrypoint for the validate-cycle action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.validate_cycle import main


if __name__ == "__main__":
    raise SystemExit(main())
