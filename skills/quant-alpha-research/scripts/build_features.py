#!/usr/bin/env python3
"""Stable entrypoint for the build-features action."""

from _bootstrap import load_workspace

load_workspace()

from quant_research.actions.build_features import main


if __name__ == "__main__":
    raise SystemExit(main())
