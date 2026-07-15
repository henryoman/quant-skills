#!/usr/bin/env python3
"""Audit an OHLCV CSV without silently repairing it."""

from __future__ import annotations

import argparse
import csv
import hashlib
import heapq
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


INTERVAL_PATTERN = re.compile(r"^(\d+)(s|m|h|d)$")
REQUIRED = ("timestamp", "open", "high", "low", "close", "volume")


def parse_interval(value: str) -> timedelta:
    match = INTERVAL_PATTERN.fullmatch(value)
    if not match:
        raise argparse.ArgumentTypeError("interval must look like 30s, 1m, 5m, 1h, or 1d")
    number = int(match.group(1))
    unit = match.group(2)
    seconds = number * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
    return timedelta(seconds=seconds)


def parse_timestamp(value: str) -> tuple[datetime, bool]:
    value = value.strip()
    try:
        numeric = float(value)
    except ValueError:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        naive = parsed.tzinfo is None
        if naive:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc), naive
    magnitude = abs(numeric)
    if magnitude >= 1e15:
        numeric /= 1_000_000
    elif magnitude >= 1e12:
        numeric /= 1_000
    return datetime.fromtimestamp(numeric, timezone.utc), False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample(samples: dict[str, list[dict[str, Any]]], key: str, row: int, detail: str) -> None:
    bucket = samples.setdefault(key, [])
    if len(bucket) < 20:
        bucket.append({"row": row, "detail": detail})


def markdown_report(audit: dict[str, Any]) -> str:
    checks = audit["checks"]
    lines = [
        "# OHLCV Data Audit",
        "",
        "## Data identity",
        "",
        f"- File: `{audit['file']}`",
        f"- SHA-256: `{audit['sha256']}`",
        f"- Rows read: {audit['rows']:,}",
        f"- Valid numeric bars: {audit['valid_numeric_bars']:,}",
        f"- Date range: {audit['date_range']['start']} to {audit['date_range']['end']}",
        f"- Expected interval: {audit['expected_interval']}",
        f"- Timestamp semantics assumed: {audit['timestamp_semantics']}",
        "",
        "## Checks",
        "",
        "| Check | Count | Interpretation |",
        "|---|---:|---|",
        f"| Timestamp parse failures | {checks['timestamp_parse_failures']:,} | Rows whose time could not be interpreted |",
        f"| Naive timestamps | {checks['naive_timestamps']:,} | Parsed as UTC but timezone was absent |",
        f"| Out-of-order timestamps | {checks['out_of_order_timestamps']:,} | Time decreased relative to the prior row |",
        f"| Duplicate timestamps | {checks['duplicate_timestamps']:,} | Repeated timestamp values |",
        f"| Irregular intervals | {checks['irregular_intervals']:,} | Delta differs from the declared bar interval |",
        f"| Gap events | {checks['gap_events']:,} | Delta exceeds the declared bar interval |",
        f"| Estimated missing bars | {checks['estimated_missing_bars']:,} | Approximate missing slots inside positive gaps |",
        f"| Numeric parse failures | {checks['numeric_parse_failures']:,} | OHLCV values that could not be parsed |",
        f"| Nonpositive prices | {checks['nonpositive_prices']:,} | Open/high/low/close at or below zero |",
        f"| Negative volume | {checks['negative_volume']:,} | Invalid under ordinary volume semantics |",
        f"| Zero volume | {checks['zero_volume']:,} | May be valid or may indicate inactive/missing bars |",
        f"| Impossible OHLC bars | {checks['impossible_ohlc']:,} | High/low invariants failed |",
        f"| Stale close transitions | {checks['stale_close_transitions']:,} | Consecutive bars with identical close |",
        f"| Longest stale-close run | {checks['longest_stale_close_run']:,} | Consecutive equal-close transitions |",
        "",
        "## Largest absolute close-to-close returns",
        "",
        "These are review candidates, not automatically bad rows.",
        "",
        "| Row | Timestamp | Return (bps) |",
        "|---:|---|---:|",
    ]
    for item in audit["largest_absolute_returns"]:
        lines.append(f"| {item['row']} | {item['timestamp']} | {item['return_bps']:.3f} |")
    lines.extend(
        [
            "",
            "## Final-bar assessment",
            "",
            audit["final_bar_assessment"],
            "",
            "## Issue samples",
            "",
        ]
    )
    if not audit["samples"]:
        lines.append("No sampled issues.")
    for key, items in audit["samples"].items():
        lines.append(f"### {key}")
        lines.append("")
        for item in items:
            lines.append(f"- Row {item['row']}: {item['detail']}")
        lines.append("")
    lines.extend(
        [
            "## Research decision",
            "",
            "This audit does not repair data or approve it for alpha testing. Record each",
            "material issue and any proposed repair in `DATA_CARD.md`, including affected",
            "rows and whether the repair could change results.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--interval", required=True, type=parse_interval)
    parser.add_argument("--interval-label", default="", help="Optional display label such as 1m")
    parser.add_argument("--timestamp-semantics", choices=["open_time", "close_time", "unknown"], default="unknown")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--cycle", default="", help="Optional cycle directory whose manifest should record this audit")
    parser.add_argument("--timestamp-col", default="timestamp")
    parser.add_argument("--open-col", default="open")
    parser.add_argument("--high-col", default="high")
    parser.add_argument("--low-col", default="low")
    parser.add_argument("--close-col", default="close")
    parser.add_argument("--volume-col", default="volume")
    args = parser.parse_args()

    source = Path(args.csv_file).expanduser().resolve()
    if not source.is_file():
        print(f"error: file not found: {source}", file=sys.stderr)
        return 1
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cycle_path: Path | None = None
    cycle_manifest: dict[str, Any] | None = None
    if args.cycle:
        cycle_path = Path(args.cycle).expanduser().resolve()
        try:
            output_dir.relative_to(cycle_path)
        except ValueError:
            print("error: when --cycle is used, --output-dir must be inside the cycle directory", file=sys.stderr)
            return 1
        manifest_path = cycle_path / "cycle.json"
        try:
            cycle_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: cannot read cycle manifest: {exc}", file=sys.stderr)
            return 1
        declared = cycle_manifest.get("scope", {}).get("data_path", "")
        if not declared:
            print("error: cycle manifest has no scope.data_path", file=sys.stderr)
            return 1
        declared_path = (cycle_path / declared).resolve()
        if declared_path != source:
            print(f"error: audited file {source} does not match declared cycle data {declared_path}", file=sys.stderr)
            return 1

    requested = {
        "timestamp": args.timestamp_col,
        "open": args.open_col,
        "high": args.high_col,
        "low": args.low_col,
        "close": args.close_col,
        "volume": args.volume_col,
    }
    counts: Counter[str] = Counter()
    samples: dict[str, list[dict[str, Any]]] = {}
    timestamps: set[datetime] = set()
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    previous_timestamp: datetime | None = None
    previous_close: float | None = None
    stale_run = 0
    longest_stale_run = 0
    largest_returns: list[tuple[float, int, str, float]] = []
    rows = 0
    valid_numeric = 0

    with source.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        lower_map = {item.lower(): item for item in headers}
        columns: dict[str, str] = {}
        for canonical, requested_name in requested.items():
            actual = requested_name if requested_name in headers else lower_map.get(requested_name.lower())
            if not actual:
                print(f"error: missing column '{requested_name}' for {canonical}; found {headers}", file=sys.stderr)
                return 1
            columns[canonical] = actual

        for row_number, row in enumerate(reader, start=2):
            rows += 1
            timestamp: datetime | None = None
            try:
                timestamp, naive = parse_timestamp(row[columns["timestamp"]])
                if naive:
                    counts["naive_timestamps"] += 1
                    sample(samples, "naive_timestamps", row_number, row[columns["timestamp"]])
            except (ValueError, OverflowError, OSError) as exc:
                counts["timestamp_parse_failures"] += 1
                sample(samples, "timestamp_parse_failures", row_number, str(exc))

            if timestamp is not None:
                if first_timestamp is None or timestamp < first_timestamp:
                    first_timestamp = timestamp
                if last_timestamp is None or timestamp > last_timestamp:
                    last_timestamp = timestamp
                if timestamp in timestamps:
                    counts["duplicate_timestamps"] += 1
                    sample(samples, "duplicate_timestamps", row_number, timestamp.isoformat())
                timestamps.add(timestamp)
                if previous_timestamp is not None:
                    delta = timestamp - previous_timestamp
                    if delta < timedelta(0):
                        counts["out_of_order_timestamps"] += 1
                        sample(samples, "out_of_order_timestamps", row_number, f"delta={delta}")
                    if delta != args.interval:
                        counts["irregular_intervals"] += 1
                        sample(samples, "irregular_intervals", row_number, f"delta={delta}")
                    if delta > args.interval:
                        counts["gap_events"] += 1
                        missing = max(0, math.floor(delta / args.interval) - 1)
                        counts["estimated_missing_bars"] += missing
                previous_timestamp = timestamp

            try:
                open_price = float(row[columns["open"]])
                high = float(row[columns["high"]])
                low = float(row[columns["low"]])
                close = float(row[columns["close"]])
                volume = float(row[columns["volume"]])
                values = [open_price, high, low, close, volume]
                if not all(math.isfinite(item) for item in values):
                    raise ValueError("non-finite OHLCV value")
                valid_numeric += 1
            except (TypeError, ValueError) as exc:
                counts["numeric_parse_failures"] += 1
                sample(samples, "numeric_parse_failures", row_number, str(exc))
                continue

            if min(open_price, high, low, close) <= 0:
                counts["nonpositive_prices"] += 1
                sample(samples, "nonpositive_prices", row_number, f"O={open_price} H={high} L={low} C={close}")
            if volume < 0:
                counts["negative_volume"] += 1
                sample(samples, "negative_volume", row_number, str(volume))
            elif volume == 0:
                counts["zero_volume"] += 1
            if high < max(open_price, close) or low > min(open_price, close) or high < low:
                counts["impossible_ohlc"] += 1
                sample(samples, "impossible_ohlc", row_number, f"O={open_price} H={high} L={low} C={close}")

            if previous_close is not None and previous_close > 0 and close > 0:
                if close == previous_close:
                    stale_run += 1
                    counts["stale_close_transitions"] += 1
                    longest_stale_run = max(longest_stale_run, stale_run)
                else:
                    stale_run = 0
                return_bps = math.log(close / previous_close) * 10_000
                item = (abs(return_bps), row_number, timestamp.isoformat() if timestamp else "", return_bps)
                if len(largest_returns) < 20:
                    heapq.heappush(largest_returns, item)
                elif item[0] > largest_returns[0][0]:
                    heapq.heapreplace(largest_returns, item)
            previous_close = close

    counts["longest_stale_close_run"] = longest_stale_run
    interval_label = args.interval_label or str(args.interval)
    if last_timestamp is None:
        final_assessment = "No valid final timestamp was available."
    elif args.timestamp_semantics == "open_time":
        bar_end = last_timestamp + args.interval
        if datetime.now(timezone.utc) < bar_end:
            final_assessment = (
                f"Potentially incomplete: treating timestamps as bar opens, the final bar ends at "
                f"{bar_end.isoformat()}. Remove or quarantine it until complete."
            )
        else:
            final_assessment = "The final bar is in the past under the declared open-time convention; completeness still depends on the source."
    else:
        final_assessment = "Cannot determine mechanically because timestamp semantics are not declared as open_time."

    critical = (
        counts["timestamp_parse_failures"]
        + counts["numeric_parse_failures"]
        + counts["nonpositive_prices"]
        + counts["impossible_ohlc"]
    )
    review_issues = (
        counts["duplicate_timestamps"]
        + counts["irregular_intervals"]
        + counts["negative_volume"]
        + counts["zero_volume"]
    )
    audit_status = "blocked" if critical else ("review_required" if review_issues else "passed")
    source_hash = sha256(source)
    audit = {
        "file": str(source),
        "sha256": source_hash,
        "status": audit_status,
        "rows": rows,
        "valid_numeric_bars": valid_numeric,
        "columns": requested,
        "expected_interval": interval_label,
        "timestamp_semantics": args.timestamp_semantics,
        "date_range": {
            "start": first_timestamp.isoformat() if first_timestamp else None,
            "end": last_timestamp.isoformat() if last_timestamp else None,
        },
        "checks": {key: int(counts[key]) for key in [
            "timestamp_parse_failures",
            "naive_timestamps",
            "out_of_order_timestamps",
            "duplicate_timestamps",
            "irregular_intervals",
            "gap_events",
            "estimated_missing_bars",
            "numeric_parse_failures",
            "nonpositive_prices",
            "negative_volume",
            "zero_volume",
            "impossible_ohlc",
            "stale_close_transitions",
            "longest_stale_close_run",
        ]},
        "largest_absolute_returns": [
            {"row": row, "timestamp": ts, "return_bps": ret}
            for _, row, ts, ret in sorted(largest_returns, reverse=True)
        ],
        "final_bar_assessment": final_assessment,
        "samples": samples,
    }
    (output_dir / "DATA_AUDIT.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    (output_dir / "DATA_AUDIT.md").write_text(markdown_report(audit), encoding="utf-8")
    if cycle_path is not None and cycle_manifest is not None:
        scope = cycle_manifest.setdefault("scope", {})
        scope["data_hash"] = f"sha256:{source_hash}"
        scope["audited_date_range"] = audit["date_range"]
        scope["data_audit"] = {
            "status": audit_status,
            "json_path": str((output_dir / "DATA_AUDIT.json").relative_to(cycle_path)),
            "markdown_path": str((output_dir / "DATA_AUDIT.md").relative_to(cycle_path)),
        }
        (cycle_path / "cycle.json").write_text(json.dumps(cycle_manifest, indent=2) + "\n", encoding="utf-8")
    print(output_dir / "DATA_AUDIT.md")
    return 2 if critical else 0


if __name__ == "__main__":
    raise SystemExit(main())
