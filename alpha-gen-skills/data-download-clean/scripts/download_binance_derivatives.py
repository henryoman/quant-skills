#!/usr/bin/env python3
"""Download Binance USD-M Futures public derivatives datasets.

Datasets:
- funding_rates: /fapi/v1/fundingRate
- open_interest: /futures/data/openInterestHist
- long_short_ratios: /futures/data/globalLongShortAccountRatio

No API key required. Uses only Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://fapi.binance.com"
MARKET = "usd_m_futures"

DATASETS = {"funding_rates", "open_interest", "long_short_ratios"}

FUNDING_COLUMNS = [
    "symbol",
    "market",
    "funding_time",
    "funding_time_ms",
    "funding_rate",
    "mark_price",
    "source",
]

OPEN_INTEREST_COLUMNS = [
    "symbol",
    "market",
    "period",
    "timestamp",
    "timestamp_ms",
    "sum_open_interest",
    "sum_open_interest_value",
    "source",
]

LONG_SHORT_COLUMNS = [
    "symbol",
    "market",
    "period",
    "timestamp",
    "timestamp_ms",
    "long_short_ratio",
    "long_account",
    "short_account",
    "source",
]


def parse_date(value: str) -> int:
    parsed = dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    return int(parsed.timestamp() * 1000)


def iso_utc(ms: int) -> str:
    return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")


def request_json(path: str, params: dict[str, object], retries: int = 4) -> list[dict[str, object]]:
    query = urllib.parse.urlencode(params)
    url = f"{BASE}{path}?{query}"
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = response.read().decode("utf-8")
            data = json.loads(payload)
            if isinstance(data, dict) and "code" in data:
                raise RuntimeError(data)
            return data
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed after {retries} attempts: {last_error}")


def fetch_funding(symbol: str, start_ms: int, end_ms: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cursor = start_ms
    while cursor < end_ms:
        batch = request_json(
            "/fapi/v1/fundingRate",
            {"symbol": symbol, "startTime": cursor, "endTime": end_ms - 1, "limit": 1000},
        )
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1]["fundingTime"]) + 1
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)
    return rows


def fetch_windowed(path: str, symbol: str, period: str, start_ms: int, end_ms: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cursor = start_ms
    while cursor < end_ms:
        batch = request_json(
            path,
            {"symbol": symbol, "period": period, "startTime": cursor, "endTime": end_ms - 1, "limit": 500},
        )
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1]["timestamp"]) + 1
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)
    return rows


def write_raw_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as file:
        for row in rows:
            file.write(json.dumps(row, separators=(",", ":")) + "\n")


def write_csv(path: Path, columns: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def clean_funding(symbol: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[int, dict[str, object]] = {}
    for row in rows:
        ms = int(row["fundingTime"])
        deduped[ms] = {
            "symbol": symbol,
            "market": MARKET,
            "funding_time": iso_utc(ms),
            "funding_time_ms": ms,
            "funding_rate": row.get("fundingRate", ""),
            "mark_price": row.get("markPrice", ""),
            "source": "binance_public_funding_rate",
        }
    return [deduped[key] for key in sorted(deduped)]


def clean_open_interest(symbol: str, period: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[int, dict[str, object]] = {}
    for row in rows:
        ms = int(row["timestamp"])
        deduped[ms] = {
            "symbol": symbol,
            "market": MARKET,
            "period": period,
            "timestamp": iso_utc(ms),
            "timestamp_ms": ms,
            "sum_open_interest": row.get("sumOpenInterest", ""),
            "sum_open_interest_value": row.get("sumOpenInterestValue", ""),
            "source": "binance_public_open_interest_hist",
        }
    return [deduped[key] for key in sorted(deduped)]


def clean_long_short(symbol: str, period: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[int, dict[str, object]] = {}
    for row in rows:
        ms = int(row["timestamp"])
        deduped[ms] = {
            "symbol": symbol,
            "market": MARKET,
            "period": period,
            "timestamp": iso_utc(ms),
            "timestamp_ms": ms,
            "long_short_ratio": row.get("longShortRatio", ""),
            "long_account": row.get("longAccount", ""),
            "short_account": row.get("shortAccount", ""),
            "source": "binance_public_global_long_short_account_ratio",
        }
    return [deduped[key] for key in sorted(deduped)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Binance USD-M Futures derivatives data.")
    parser.add_argument("--symbols", nargs="+", required=True)
    parser.add_argument("--datasets", nargs="+", choices=sorted(DATASETS), required=True)
    parser.add_argument("--period", default="1h", help="Period for open_interest and long_short_ratios")
    parser.add_argument("--start", required=True, help="UTC start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="UTC end date YYYY-MM-DD, exclusive")
    parser.add_argument("--output-dir", default="data/market/binance")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start_ms = parse_date(args.start)
    end_ms = parse_date(args.end)
    if end_ms <= start_ms:
        print("--end must be after --start", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir)
    for symbol in [value.upper() for value in args.symbols]:
        if "funding_rates" in args.datasets:
            raw = fetch_funding(symbol, start_ms, end_ms)
            clean = clean_funding(symbol, raw)
            raw_path = output_dir / "raw" / MARKET / "funding_rates" / symbol / "funding_rates.jsonl"
            clean_path = output_dir / "clean" / MARKET / "funding_rates" / symbol / "funding_rates.csv"
            write_raw_jsonl(raw_path, raw)
            write_csv(clean_path, FUNDING_COLUMNS, clean)
            print(f"{symbol} funding_rates: raw={raw_path} clean={clean_path} rows={len(clean)}")

        if "open_interest" in args.datasets:
            raw = fetch_windowed("/futures/data/openInterestHist", symbol, args.period, start_ms, end_ms)
            clean = clean_open_interest(symbol, args.period, raw)
            raw_path = output_dir / "raw" / MARKET / "open_interest" / symbol / f"{args.period}.jsonl"
            clean_path = output_dir / "clean" / MARKET / "open_interest" / symbol / f"{args.period}.csv"
            write_raw_jsonl(raw_path, raw)
            write_csv(clean_path, OPEN_INTEREST_COLUMNS, clean)
            print(f"{symbol} open_interest: raw={raw_path} clean={clean_path} rows={len(clean)}")

        if "long_short_ratios" in args.datasets:
            raw = fetch_windowed("/futures/data/globalLongShortAccountRatio", symbol, args.period, start_ms, end_ms)
            clean = clean_long_short(symbol, args.period, raw)
            raw_path = output_dir / "raw" / MARKET / "long_short_ratios" / symbol / f"{args.period}.jsonl"
            clean_path = output_dir / "clean" / MARKET / "long_short_ratios" / symbol / f"{args.period}.csv"
            write_raw_jsonl(raw_path, raw)
            write_csv(clean_path, LONG_SHORT_COLUMNS, clean)
            print(f"{symbol} long_short_ratios: raw={raw_path} clean={clean_path} rows={len(clean)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
