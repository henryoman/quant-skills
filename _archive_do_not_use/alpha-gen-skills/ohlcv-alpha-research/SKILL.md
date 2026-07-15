---
name: ohlcv-alpha-research
description: |
  Build, audit, and interpret instrument-agnostic OHLCV alpha research workflows using only timestamp, open, high, low, close, and volume data. Use for anomaly discovery, past-only feature engineering, event studies, forward targets, MFE/MAE, triple-barrier logic, regime splits, threshold robustness, walk-forward validation, cost stress, and candidate alpha dossiers. Trigger when users ask to research OHLCV alpha, test candle/volume/range anomalies, validate a trading rule, or convert raw OHLCV bars into a disciplined quant research report.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
---

# OHLCV Alpha Research Skill

Use this skill to discover and validate OHLCV-only anomalies without assuming an instrument, venue, session, spread, tick size, borrow cost, leverage rule, fundamentals, macro data, news, options, order book data, or a cross-sectional universe.

## Core Rule

Every feature, threshold, rolling statistic, regime label, signal, and rule must be computable from information available at the end of the current bar. Do not use future values, full-sample normalizers, unshifted breakout levels, or hidden target information.

## Bundled Resources

- Read `references/OHLCV_Alpha_Research_Framework_Beginner_to_Advanced.md` for the full beginner-to-advanced research manual.
- Read `references/first-20-tests.md` when starting an initial event-study scan.
- Read `references/report-template.md` when writing a final anomaly dossier.
- Read `references/checklists.md` before trusting any candidate alpha.
- Use `scripts/ohlcv_research_engine.py` to run a reproducible OHLCV-only scan from a CSV file.
- Use `examples/sample_ohlcv.csv` to verify the script or demonstrate the workflow.

## Standard Workflow

1. Load one time-ordered OHLCV table with `timestamp`, `open`, `high`, `low`, `close`, and `volume`.
2. Clean and validate the bars: strict time order, positive prices, nonnegative volume, OHLC consistency, duplicates, and timestamp gaps.
3. Generate base features using log returns, log ranges, candle structure, volume transforms, path efficiency, rolling highs/lows, and volatility proxies.
4. Generate rolling z-scores, robust z-scores, percentiles, ratios, and regimes using prior bars only.
5. Generate forward targets separately from features: future returns, absolute returns, future range, MFE, MAE, and triple-barrier outcomes.
6. Run event studies with cooldown-based de-duplication.
7. Split results by volatility, trend, efficiency/chop, and volume regimes.
8. Run threshold, horizon, delayed-entry, and cost-stress checks before writing a verdict.
9. Record all trials, including rejected experiments.
10. Assign a conservative verdict: `Reject`, `Watchlist`, `Directional alpha candidate`, `Volatility alpha candidate`, or `Needs more data`.

## Script Usage

```bash
python3 alpha-gen-skills/ohlcv-alpha-research/scripts/ohlcv_research_engine.py \
  --input path/to/ohlcv.csv \
  --output-dir research-output \
  --timestamp-col timestamp
```

If the local Python environment does not already have `pandas` and `numpy`, run it with `uv`:

```bash
uv run --with pandas --with numpy \
  alpha-gen-skills/ohlcv-alpha-research/scripts/ohlcv_research_engine.py \
  --input path/to/ohlcv.csv \
  --output-dir research-output
```

The script writes:

- `cleaned_ohlcv.csv`
- `features_targets.csv`
- `data_quality.json`
- `first_20_event_studies.csv`
- `regime_event_studies.csv`
- `threshold_sweeps.csv`
- `cost_stress.csv`
- `candidate_report.md`
- `candidate_report.html`

Open `candidate_report.html` first. It summarizes what is right, what needs review, generated files, strongest exploratory rows, threshold sweep preview, cost-stress preview, and required next actions.

## Interpretation Rules

- A positive mean with a weak median is fragile until the outlier audit says otherwise.
- A high hit rate with a bad profit factor is not a good directional signal.
- A flat directional result with high future absolute return can still be volatility alpha.
- A signal that fails after cooldown was probably inflated by clustered events.
- A signal that fails after small costs is research-only unless a specific execution context supports it.
- A result that works only at one exact threshold should be rejected or kept exploratory.

## Safety / Honesty Rules

- Never call an anomaly alpha until it survives out-of-sample validation, robustness checks, cost stress, and a final dossier.
- Never claim volume reveals buyer or seller identity; call it participation intensity.
- Never claim wick ordering inside the bar unless lower-timeframe data proves it.
- Handle same-bar triple-barrier hits conservatively or mark them ambiguous.
- Keep OHLCV-derived signals separate from future targets in code and reports.
