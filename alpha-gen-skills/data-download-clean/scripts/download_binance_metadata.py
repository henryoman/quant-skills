#!/usr/bin/env python3
"""Download Binance public exchange metadata and normalize symbol records."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from pathlib import Path

MARKETS = {
    "spot": "https://api.binance.com/api/v3/exchangeInfo",
    "usd_m_futures": "https://fapi.binance.com/fapi/v1/exchangeInfo",
}

COLUMNS = [
    "symbol",
    "market",
    "status",
    "base_asset",
    "quote_asset",
    "contract_type",
    "onboard_date_ms",
    "delivery_date_ms",
    "permissions",
    "order_types",
    "raw_json",
    "source",
]


def request_json(url: str) -> dict[str, object]:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_symbol(market: str, row: dict[str, object]) -> dict[str, object]:
    return {
        "symbol": row.get("symbol", ""),
        "market": market,
        "status": row.get("status", ""),
        "base_asset": row.get("baseAsset", ""),
        "quote_asset": row.get("quoteAsset", ""),
        "contract_type": row.get("contractType", ""),
        "onboard_date_ms": row.get("onboardDate", ""),
        "delivery_date_ms": row.get("deliveryDate", ""),
        "permissions": "|".join(row.get("permissions", []) or []),
        "order_types": "|".join(row.get("orderTypes", []) or []),
        "raw_json": json.dumps(row, separators=(",", ":"), sort_keys=True),
        "source": "binance_public_exchange_info",
    }


def write_outputs(output_dir: Path, market: str, payload: dict[str, object]) -> None:
    raw_path = output_dir / "raw" / market / "exchange_metadata" / "exchangeInfo.json"
    clean_path = output_dir / "clean" / market / "exchange_metadata" / "symbols.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path.parent.mkdir(parents=True, exist_ok=True)

    raw_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    rows = [normalize_symbol(market, item) for item in payload.get("symbols", [])]
    rows.sort(key=lambda item: str(item["symbol"]))
    with clean_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{market}: raw={raw_path} clean={clean_path} rows={len(rows)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Binance public exchange metadata.")
    parser.add_argument("--markets", nargs="+", choices=sorted(MARKETS), required=True)
    parser.add_argument("--output-dir", default="data/market/binance")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    for market in args.markets:
        payload = request_json(MARKETS[market])
        write_outputs(output_dir, market, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
