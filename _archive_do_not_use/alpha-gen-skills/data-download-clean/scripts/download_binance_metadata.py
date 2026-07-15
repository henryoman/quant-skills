#!/usr/bin/env python3
"""Download Binance public exchange metadata and normalize symbol records."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from pathlib import Path

from reporting import write_html_report

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


def write_outputs(output_dir: Path, market: str, payload: dict[str, object]) -> tuple[Path, Path, list[dict[str, object]]]:
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
    return raw_path, clean_path, rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Binance public exchange metadata.")
    parser.add_argument("--markets", nargs="+", choices=sorted(MARKETS), required=True)
    parser.add_argument("--output-dir", default="data/market/binance")
    parser.add_argument("--report", help="Output HTML report path. Defaults to <output-dir>/reports/binance_metadata_report.html.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    report_path = Path(args.report) if args.report else output_dir / "reports" / "binance_metadata_report.html"
    checks: list[dict[str, object]] = []
    outputs: list[dict[str, object]] = []
    for market in args.markets:
        payload = request_json(MARKETS[market])
        raw_path, clean_path, rows = write_outputs(output_dir, market, payload)
        trading_count = sum(1 for row in rows if row["status"] == "TRADING")
        checks.extend(
            [
                {
                    "status": "pass" if rows else "fail",
                    "name": f"{market} symbol metadata",
                    "detail": f"{len(rows)} symbols normalized.",
                },
                {
                    "status": "pass" if trading_count else "warn",
                    "name": f"{market} tradable symbols",
                    "detail": f"{trading_count} symbols currently marked TRADING.",
                },
            ]
        )
        outputs.extend(
            [
                {"name": f"{market} raw exchangeInfo", "path": raw_path, "detail": "Raw Binance exchangeInfo payload."},
                {"name": f"{market} clean symbols", "path": clean_path, "detail": f"{len(rows)} normalized symbol rows."},
            ]
        )
    outputs.append({"name": "HTML report", "path": report_path, "detail": "Static Binance metadata audit."})
    write_html_report(
        report_path,
        title="Binance Metadata Download Report",
        summary=f"Exchange metadata for {', '.join(args.markets)}.",
        checks=checks,
        outputs=outputs,
        notes=[
            "Use clean symbol metadata to validate universe construction before downloading candles.",
            "Filter to TRADING symbols unless a delisted-history study explicitly needs inactive markets.",
        ],
    )
    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
