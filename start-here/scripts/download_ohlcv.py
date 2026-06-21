#!/usr/bin/env python3
"""Download normalized OHLCV CSVs from simple public/keyed providers.

Output columns are always:

timestamp,open,high,low,close,volume
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable

UTC = dt.timezone.utc

BINANCE_INTERVAL_MS = {
    "1m": 60_000,
    "3m": 180_000,
    "5m": 300_000,
    "15m": 900_000,
    "30m": 1_800_000,
    "1h": 3_600_000,
    "2h": 7_200_000,
    "4h": 14_400_000,
    "6h": 21_600_000,
    "8h": 28_800_000,
    "12h": 43_200_000,
    "1d": 86_400_000,
    "3d": 259_200_000,
    "1w": 604_800_000,
}

POLYGON_INTERVALS = {
    "1m": (1, "minute"),
    "5m": (5, "minute"),
    "15m": (15, "minute"),
    "30m": (30, "minute"),
    "1h": (1, "hour"),
    "1d": (1, "day"),
}


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    if len(text) == 10:
        return dt.datetime.fromisoformat(text).replace(tzinfo=UTC)
    parsed = dt.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def iso_from_ms(ms: int) -> str:
    return dt.datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat().replace("+00:00", "Z")


def iso_from_seconds(seconds: int) -> str:
    return dt.datetime.fromtimestamp(seconds, tz=UTC).isoformat().replace("+00:00", "Z")


def request_json(url: str, headers: dict[str, str] | None = None) -> object:
    request = urllib.request.Request(url, headers=headers or {"User-Agent": "alpha-data-setup/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download_binance(symbol: str, interval: str, start: dt.datetime | None, end: dt.datetime | None) -> list[dict[str, object]]:
    if interval not in BINANCE_INTERVAL_MS:
        raise SystemExit(f"Unsupported Binance interval: {interval}")
    rows: list[dict[str, object]] = []
    start_ms = int((start or dt.datetime(2017, 1, 1, tzinfo=UTC)).timestamp() * 1000)
    end_ms = int((end or dt.datetime.now(UTC)).timestamp() * 1000)
    step = BINANCE_INTERVAL_MS[interval]

    while start_ms < end_ms:
        params = urllib.parse.urlencode({
            "symbol": symbol.upper(),
            "interval": interval,
            "startTime": start_ms,
            "endTime": end_ms,
            "limit": 1000,
        })
        data = request_json(f"https://api.binance.com/api/v3/klines?{params}")
        if not data:
            break
        for item in data:
            open_time = int(item[0])
            if open_time >= end_ms:
                continue
            rows.append({
                "timestamp": iso_from_ms(open_time),
                "open": item[1],
                "high": item[2],
                "low": item[3],
                "close": item[4],
                "volume": item[5],
            })
        next_ms = int(data[-1][0]) + step
        if next_ms <= start_ms:
            break
        start_ms = next_ms
        time.sleep(0.15)
    return rows


def download_coinbase(symbol: str, interval: str, start: dt.datetime | None, end: dt.datetime | None) -> list[dict[str, object]]:
    granularity = int(interval)
    if granularity not in {60, 300, 900, 3600, 21600, 86400}:
        raise SystemExit("Coinbase interval must be one of: 60, 300, 900, 3600, 21600, 86400")
    rows: list[dict[str, object]] = []
    cursor = start or (dt.datetime.now(UTC) - dt.timedelta(days=30))
    finish = end or dt.datetime.now(UTC)
    max_span = dt.timedelta(seconds=granularity * 300)

    while cursor < finish:
        chunk_end = min(cursor + max_span, finish)
        params = urllib.parse.urlencode({
            "start": cursor.isoformat().replace("+00:00", "Z"),
            "end": chunk_end.isoformat().replace("+00:00", "Z"),
            "granularity": granularity,
        })
        data = request_json(f"https://api.exchange.coinbase.com/products/{symbol}/candles?{params}")
        for item in data:
            rows.append({
                "timestamp": iso_from_seconds(int(item[0])),
                "open": item[3],
                "high": item[2],
                "low": item[1],
                "close": item[4],
                "volume": item[5],
            })
        cursor = chunk_end
        time.sleep(0.2)
    return sorted(unique_rows(rows), key=lambda row: row["timestamp"])


def download_kraken(symbol: str, interval: str, start: dt.datetime | None, end: dt.datetime | None) -> list[dict[str, object]]:
    since = int((start or (dt.datetime.now(UTC) - dt.timedelta(days=30))).timestamp())
    end_ts = int((end or dt.datetime.now(UTC)).timestamp())
    params = urllib.parse.urlencode({"pair": symbol, "interval": int(interval), "since": since})
    payload = request_json(f"https://api.kraken.com/0/public/OHLC?{params}")
    if payload.get("error"):
        raise SystemExit("Kraken error: " + "; ".join(payload["error"]))
    result = payload.get("result", {})
    pair_keys = [key for key in result.keys() if key != "last"]
    if not pair_keys:
        return []
    rows = []
    for item in result[pair_keys[0]]:
        ts = int(float(item[0]))
        if ts >= end_ts:
            continue
        rows.append({
            "timestamp": iso_from_seconds(ts),
            "open": item[1],
            "high": item[2],
            "low": item[3],
            "close": item[4],
            "volume": item[6],
        })
    return rows


def download_polygon(symbol: str, interval: str, start: dt.datetime | None, end: dt.datetime | None) -> list[dict[str, object]]:
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        raise SystemExit("POLYGON_API_KEY is required for provider=polygon")
    if interval not in POLYGON_INTERVALS:
        raise SystemExit(f"Unsupported Polygon interval: {interval}")
    if not start or not end:
        raise SystemExit("Polygon downloads require --start and --end")
    multiplier, timespan = POLYGON_INTERVALS[interval]
    start_s = start.date().isoformat()
    end_s = end.date().isoformat()
    params = urllib.parse.urlencode({"adjusted": "true", "sort": "asc", "limit": 50000, "apiKey": api_key})
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start_s}/{end_s}?{params}"
    payload = request_json(url)
    if payload.get("status") not in {"OK", "DELAYED"}:
        raise SystemExit("Polygon error: " + json.dumps(payload)[:500])
    return [{
        "timestamp": iso_from_ms(int(item["t"])),
        "open": item["o"],
        "high": item["h"],
        "low": item["l"],
        "close": item["c"],
        "volume": item["v"],
    } for item in payload.get("results", [])]


def unique_rows(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    seen = set()
    output = []
    for row in rows:
        ts = row["timestamp"]
        if ts in seen:
            continue
        seen.add(ts)
        output.append(row)
    return output


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download normalized OHLCV CSV data.")
    parser.add_argument("--provider", required=True, choices=["binance", "coinbase", "kraken", "polygon"])
    parser.add_argument("--symbol", required=True, help="Provider-specific symbol, e.g. BTCUSDT, BTC-USD, XBTUSD, AAPL.")
    parser.add_argument("--interval", required=True, help="Provider interval, e.g. 1h for Binance/Polygon, 3600 for Coinbase, 60 for Kraken.")
    parser.add_argument("--start", help="UTC start date/time, e.g. 2024-01-01 or 2024-01-01T00:00:00Z.")
    parser.add_argument("--end", help="UTC end date/time. Defaults to now for public providers.")
    parser.add_argument("--output", required=True, help="Output CSV path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = parse_time(args.start)
    end = parse_time(args.end)

    if args.provider == "binance":
        rows = download_binance(args.symbol, args.interval, start, end)
    elif args.provider == "coinbase":
        rows = download_coinbase(args.symbol, args.interval, start, end)
    elif args.provider == "kraken":
        rows = download_kraken(args.symbol, args.interval, start, end)
    elif args.provider == "polygon":
        rows = download_polygon(args.symbol, args.interval, start, end)
    else:
        raise SystemExit(f"Unsupported provider: {args.provider}")

    rows = sorted(unique_rows(rows), key=lambda row: row["timestamp"])
    write_csv(rows, Path(args.output))
    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
