#!/usr/bin/env python3
"""Stable entrypoint for the evaluate-trades action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.evaluate_trades import main


if __name__ == "__main__":
    raise SystemExit(main())
