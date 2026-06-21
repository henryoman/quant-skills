# Quant Skills

Read `instructions.md` first. The repo bootstrap and portable instruction skill lives in `start-here/`.

This workspace is organized into three top-level buckets plus the root instruction artifacts:

- `cmc-bnb-skills/`: official native CoinMarketCap skills and BNB project foundation material.
- `third-party-skills/`: imported skills from outside vendors, community repos, mirrors, or other external authors.
- `alpha-gen-skills/`: skills and research packages authored in this workspace for alpha generation, strategy research, data setup, and contest work.

Keep new skill folders inside one of these buckets unless the folder is the root `start-here/`.

Initial data-source selection and API key setup belong in `start-here/`. Repeatable Binance download/clean pipelines live in `alpha-gen-skills/data-download-clean/`.

Runnable setup, download, and research steps should emit a static HTML report next to their outputs. Treat that report as the first user-facing audit: it should show what is right, what needs review, what is wrong, which files were written, and the next action.

For skill installers, install one skill folder at a time:

1. `start-here/`
2. `cmc-bnb-skills/<skill-name>/`
3. `alpha-gen-skills/<skill-name>/`
4. `third-party-skills/<skill-name>/`

## Default Research Standard

Unless a skill says otherwise, alpha research in this repo should follow the OHLCV-only framework in `instructions.md`.

Core rule:

```text
Use only timestamp, open, high, low, close, and volume.
Define events using information known at or before time t.
Measure outcomes only after time t.
Compare every event against the unconditional baseline.
Validate chronologically out of sample.
Reject signals that depend on one magic threshold, impossible execution, or unrealistic costs.
```

The expected output is a short ranked report:

1. Data quality summary
2. Feature summary
3. Baseline future-return statistics
4. Anomaly ranking table
5. Robustness summary
6. Regime summary
7. Cost sensitivity summary
8. Alpha cards for surviving anomalies
9. Rejected anomalies and why
10. Final conclusion

For executable workflows, include `candidate_report.html` or the relevant `*.report.html` file with the machine-readable CSV/JSON outputs.
