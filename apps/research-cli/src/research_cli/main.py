"""Dispatch one stable command surface to modular research actions."""

from __future__ import annotations

import sys
from collections.abc import Callable

from quant_research.actions.audit_ohlcv import main as audit_ohlcv
from quant_research.actions.build_features import main as build_features
from quant_research.actions.create_cycle import main as create_cycle
from quant_research.actions.evaluate_trades import main as evaluate_trades
from quant_research.actions.open_holdout import main as open_holdout
from quant_research.actions.register_experiment import main as register_experiment
from quant_research.actions.validate_cycle import main as validate_cycle


COMMANDS: dict[str, Callable[[], int]] = {
    "audit-ohlcv": audit_ohlcv,
    "build-features": build_features,
    "create-cycle": create_cycle,
    "evaluate-trades": evaluate_trades,
    "open-holdout": open_holdout,
    "register-experiment": register_experiment,
    "validate-cycle": validate_cycle,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print("usage: quant-research <command> [options]")
        print("commands:")
        for command in sorted(COMMANDS):
            print(f"  {command}")
        return 0
    command = sys.argv[1]
    action = COMMANDS.get(command)
    if action is None:
        print(f"error: unknown command '{command}'", file=sys.stderr)
        return 2
    sys.argv = [f"quant-research {command}", *sys.argv[2:]]
    return action()


if __name__ == "__main__":
    raise SystemExit(main())
