#!/usr/bin/env python3
"""Stable entrypoint for the open-holdout action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.open_holdout import main


if __name__ == "__main__":
    raise SystemExit(main())
