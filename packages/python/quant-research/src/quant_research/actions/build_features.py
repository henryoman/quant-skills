#!/usr/bin/env python3
"""Build a causal, interpretable feature matrix from an audited OHLCV CSV."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import deque
from pathlib import Path

from ..routines.feature_pipeline import build_feature_row


def parse_lookbacks(value: str) -> list[int]:
    try:
        lookbacks = sorted({int(item.strip()) for item in value.split(",") if item.strip()})
    except ValueError as exc:
        raise argparse.ArgumentTypeError("lookbacks must be comma-separated integers") from exc
    if not lookbacks or any(item < 1 for item in lookbacks):
        raise argparse.ArgumentTypeError("lookbacks must be positive")
    return lookbacks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ohlcv_csv")
    parser.add_argument("--output", required=True)
    parser.add_argument("--lookbacks", type=parse_lookbacks, default=parse_lookbacks("5,15,60"))
    parser.add_argument("--timestamp-col", default="timestamp")
    args = parser.parse_args()

    source = Path(args.ohlcv_csv).expanduser().resolve()
    destination = Path(args.output).expanduser().resolve()
    if not source.is_file():
        print(f"error: file not found: {source}", file=sys.stderr)
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)

    max_history = max(args.lookbacks) + 1
    history: deque[dict[str, str]] = deque(maxlen=max_history)
    output_rows = 0
    writer: csv.DictWriter | None = None
    with source.open("r", newline="", encoding="utf-8-sig") as input_handle, destination.open(
        "w", newline="", encoding="utf-8"
    ) as output_handle:
        reader = csv.DictReader(input_handle)
        headers = reader.fieldnames or []
        lower = {item.lower(): item for item in headers}
        required = {name: lower.get(name) for name in ("open", "high", "low", "close", "volume")}
        missing = [name for name, actual in required.items() if actual is None]
        timestamp_actual = args.timestamp_col if args.timestamp_col in headers else lower.get(args.timestamp_col.lower())
        if missing or not timestamp_actual:
            print(f"error: missing required columns: {', '.join(missing + ([] if timestamp_actual else [args.timestamp_col]))}", file=sys.stderr)
            return 1

        for source_row, raw in enumerate(reader, start=2):
            bar = {name: raw[actual] for name, actual in required.items() if actual is not None}
            try:
                valid_numeric = all(math.isfinite(float(value)) for value in bar.values())
            except ValueError:
                valid_numeric = False
            if not valid_numeric:
                print(f"error: invalid numeric OHLCV value on row {source_row}", file=sys.stderr)
                return 1
            history.append(bar)
            if len(history) < max_history:
                continue
            try:
                features = build_feature_row(list(history), args.lookbacks)
            except ValueError as exc:
                print(f"error: row {source_row}: {exc}", file=sys.stderr)
                return 1
            output = {
                "source_row": source_row,
                "timestamp": raw[timestamp_actual],
                "feature_cutoff": "bar_t_close",
                **features,
            }
            if writer is None:
                writer = csv.DictWriter(output_handle, fieldnames=list(output))
                writer.writeheader()
            writer.writerow(output)
            output_rows += 1

    if output_rows == 0:
        print("error: no feature rows produced; dataset is shorter than the maximum lookback", file=sys.stderr)
        return 1
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
