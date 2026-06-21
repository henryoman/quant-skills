#!/usr/bin/env python3
"""Download Binance public klines and write raw + cleaned CSV files.

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

SPOT_BASE = "https://api.binance.com"
USD_M_FUTURES_BASE = "https://fapi.binance.com"

INTERVAL_MS = {
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

RAW_COLUMNS = [
    "open_time_ms",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time_ms",
    "quote_volume",
    "trade_count",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "ignore",
]

CLEAN_COLUMNS = [
    "symbol",
    "market",
    "interval",
    "open_time",
    "open_time_ms",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "close_time_ms",
    "quote_volume",
    "trade_count",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "is_closed",
    "source",
]


def parse_date(value: str) -> int:
    parsed = dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    return int(parsed.timestamp() * 1000)


def iso_utc(ms: int) -> str:
    return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")


def endpoint_for(market: str) -> tuple[str, str]:
    if market == "spot":
        return SPOT_BASE, "/api/v3/klines"
    if market == "usd_m_futures":
        return USD_M_FUTURES_BASE, "/fapi/v1/klines"
    raise ValueError(f"unsupported market: {market}")


def request_json(url: str, retries: int = 4) -> list[list[object]]:
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


def fetch_klines(market: str, symbol: str, interval: str, start_ms: int, end_ms: int) -> list[list[object]]:
    base, path = endpoint_for(market)
    rows: list[list[object]] = []
    cursor = start_ms

    while cursor < end_ms:
        params = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "interval": interval,
                "startTime": cursor,
                "endTime": end_ms - 1,
                "limit": 1000,
            }
        )
        url = f"{base}{path}?{params}"
        batch = request_json(url)
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1][0]) + interval_to_ms(interval)
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)

    return rows


def interval_to_ms(interval: str) -> int:
    if interval == "1M":
        raise ValueError("1M interval is calendar-based and is not supported by this first-pass script")
    if interval not in INTERVAL_MS:
        raise ValueError(f"unsupported interval: {interval}")
    return INTERVAL_MS[interval]


def write_raw(path: Path, rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(RAW_COLUMNS)
        writer.writerows(rows)


def clean_rows(
    rows: list[list[object]],
    *,
    symbol: str,
    market: str,
    interval: str,
    end_ms: int,
    include_open_candle: bool,
) -> list[dict[str, object]]:
    cleaned_by_open: dict[int, dict[str, object]] = {}
    now_ms = int(time.time() * 1000)

    for row in rows:
        item = dict(zip(RAW_COLUMNS, row))
        open_ms = int(item["open_time_ms"])
        close_ms = int(item["close_time_ms"])
        is_closed = close_ms < now_ms and close_ms < end_ms
        if not include_open_candle and not is_closed:
            continue
        cleaned_by_open[open_ms] = {
            "symbol": symbol,
            "market": market,
            "interval": interval,
            "open_time": iso_utc(open_ms),
            "open_time_ms": open_ms,
            "open": item["open"],
            "high": item["high"],
            "low": item["low"],
            "close": item["close"],
            "volume": item["volume"],
            "close_time": iso_utc(close_ms),
            "close_time_ms": close_ms,
            "quote_volume": item["quote_volume"],
            "trade_count": item["trade_count"],
            "taker_buy_base_volume": item["taker_buy_base_volume"],
            "taker_buy_quote_volume": item["taker_buy_quote_volume"],
            "is_closed": str(is_closed).lower(),
            "source": "binance_public_klines",
        }

    return [cleaned_by_open[key] for key in sorted(cleaned_by_open)]


def write_clean(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CLEAN_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Binance public klines and write raw + clean CSV files.")
    parser.add_argument("--market", choices=["spot", "usd_m_futures"], required=True)
    parser.add_argument("--symbols", nargs="+", required=True, help="Symbols like BTCUSDT ETHUSDT BNBUSDT")
    parser.add_argument("--interval", required=True, help="Binance interval, e.g. 1h, 15m, 1d")
    parser.add_argument("--start", required=True, help="UTC start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="UTC end date YYYY-MM-DD, exclusive")
    parser.add_argument("--output-dir", default="data/market/binance")
    parser.add_argument("--include-open-candle", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start_ms = parse_date(args.start)
    end_ms = parse_date(args.end)
    if end_ms <= start_ms:
        print("--end must be after --start", file=sys.stderr)
        return 2
    interval_to_ms(args.interval)

    output_dir = Path(args.output_dir)
    for symbol in [value.upper() for value in args.symbols]:
        rows = fetch_klines(args.market, symbol, args.interval, start_ms, end_ms)
        raw_path = output_dir / "raw" / args.market / symbol / f"{args.interval}.csv"
        clean_path = output_dir / "clean" / args.market / symbol / f"{args.interval}.csv"
        write_raw(raw_path, rows)
        cleaned = clean_rows(
            rows,
            symbol=symbol,
            market=args.market,
            interval=args.interval,
            end_ms=end_ms,
            include_open_candle=args.include_open_candle,
        )
        write_clean(clean_path, cleaned)
        print(f"{symbol}: raw={raw_path} clean={clean_path} rows={len(cleaned)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
