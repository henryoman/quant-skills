#!/usr/bin/env python3
"""Create a local .env template for alpha data providers."""

from __future__ import annotations

import argparse
from pathlib import Path

from reporting import write_html_report

PROVIDER_VARS = {
    "binance": [],
    "coinbase": [],
    "kraken": [],
    "cmc": ["CMC_API_KEY"],
    "polygon": ["POLYGON_API_KEY"],
    "alpaca": ["ALPACA_API_KEY_ID", "ALPACA_API_SECRET_KEY"],
    "twelvedata": ["TWELVE_DATA_API_KEY"],
    "alpha_vantage": ["ALPHA_VANTAGE_API_KEY"],
}

HEADER = """# Alpha data provider environment
# Fill only the keys you need. Do not commit real secrets.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a .env template for alpha data providers.")
    parser.add_argument("--providers", nargs="+", default=["binance", "coinbase", "kraken"], help="Providers to include.")
    parser.add_argument("--output", default=".env.alpha", help="Output env file path.")
    parser.add_argument("--report", help="Output HTML report path. Defaults to <output>.report.html.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing output file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    report_path = Path(args.report) if args.report else output.with_name(output.name + ".report.html")
    if output.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite {output}. Pass --overwrite to replace it.")

    lines = [HEADER.rstrip(), ""]
    unknown = []
    known = []
    vars_written = []
    for provider in args.providers:
        key = provider.lower().replace("-", "_")
        if key not in PROVIDER_VARS:
            unknown.append(provider)
            continue
        known.append(key)
        vars_for_provider = PROVIDER_VARS[key]
        lines.append(f"# {provider}")
        if not vars_for_provider:
            lines.append(f"# No API key required for basic {provider} public OHLCV downloads.")
        for var in vars_for_provider:
            vars_written.append(var)
            lines.append(f"{var}=")
        lines.append("")

    if unknown:
        lines.append("# Unknown providers requested: " + ", ".join(unknown))
        lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    write_html_report(
        report_path,
        title="Environment Template Setup Report",
        summary="Checks for the generated local provider environment template.",
        checks=[
            {
                "status": "pass" if known else "fail",
                "name": "Known providers",
                "detail": ", ".join(known) if known else "No recognized providers were requested.",
            },
            {
                "status": "warn" if unknown else "pass",
                "name": "Unknown providers",
                "detail": ", ".join(unknown) if unknown else "Every requested provider is recognized.",
            },
            {
                "status": "pass",
                "name": "Secret safety",
                "detail": "The file contains blank placeholders only; no real secrets were written.",
            },
            {
                "status": "pass" if output.exists() else "fail",
                "name": "Output file",
                "detail": f"Template written to {output}.",
            },
        ],
        outputs=[
            {"name": "Env template", "path": output, "detail": f"{len(vars_written)} keyed variables plus public-provider notes."},
            {"name": "HTML report", "path": report_path, "detail": "Static setup audit report."},
        ],
        notes=[
            "Fill only the keys required for the providers you will actually use.",
            "Load the file with set -a; source .env.alpha; set +a before keyed downloads.",
            "Do not commit real .env files.",
        ],
    )
    print(f"Wrote {output}")
    print(f"Wrote report {report_path}")
    if unknown:
        print("Unknown providers were noted in the file: " + ", ".join(unknown))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
