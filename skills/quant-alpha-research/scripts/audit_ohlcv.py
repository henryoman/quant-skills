#!/usr/bin/env python3
"""Stable entrypoint for the audit-OHLCV action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.audit_ohlcv import main


if __name__ == "__main__":
    raise SystemExit(main())
