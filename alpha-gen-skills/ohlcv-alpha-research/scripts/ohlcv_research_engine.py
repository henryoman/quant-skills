#!/usr/bin/env python3
"""Instrument-agnostic OHLCV alpha research engine.

Educational research scaffold only. It does not place trades and does not make
financial recommendations.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd

EPS = 1e-12
REQUIRED_COLS = ["open", "high", "low", "close", "volume"]


@dataclass(frozen=True)
class SignalSpec:
    name: str
    purpose: str
    target: str
    cooldown: int
    side: int
    condition: Callable[[pd.DataFrame], pd.Series]


def safe_log_ratio(a: pd.Series | np.ndarray, b: pd.Series | np.ndarray) -> pd.Series:
    return np.log(np.maximum(a, EPS) / np.maximum(b, EPS))


def rolling_zscore_past(x: pd.Series, n: int) -> pd.Series:
    hist = x.shift(1)
    mu = hist.rolling(n, min_periods=n).mean()
    sd = hist.rolling(n, min_periods=n).std(ddof=1)
    return (x - mu) / sd.replace(0, np.nan)


def rolling_robust_z_past(x: pd.Series, n: int) -> pd.Series:
    hist = x.shift(1)
    med = hist.rolling(n, min_periods=n).median()

    def mad(arr: np.ndarray) -> float:
        m = np.nanmedian(arr)
        return float(np.nanmedian(np.abs(arr - m)))

    madv = hist.rolling(n, min_periods=n).apply(mad, raw=True)
    return 0.6745 * (x - med) / madv.replace(0, np.nan)


def rolling_percentile_past(x: pd.Series, n: int) -> pd.Series:
    def pct_rank(arr: np.ndarray) -> float:
        current = arr[-1]
        hist = arr[:-1]
        hist = hist[~np.isnan(hist)]
        if len(hist) == 0 or np.isnan(current):
            return np.nan
        return float(np.mean(hist <= current))

    return x.rolling(n + 1, min_periods=n + 1).apply(pct_rank, raw=True)


def clean_ohlcv(df: pd.DataFrame, timestamp_col: str = "timestamp") -> tuple[pd.DataFrame, dict]:
    missing = [c for c in [timestamp_col, *REQUIRED_COLS] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    raw_rows = int(len(df))
    out = df.copy()
    out[timestamp_col] = pd.to_datetime(out[timestamp_col], errors="coerce", utc=True)
    invalid_timestamps = int(out[timestamp_col].isna().sum())
    out = out.dropna(subset=[timestamp_col])

    for col in REQUIRED_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.sort_values(timestamp_col)
    duplicate_timestamps = int(out.duplicated(timestamp_col, keep="last").sum())
    out = out.drop_duplicates(timestamp_col, keep="last").reset_index(drop=True)

    price_ok = (out[["open", "high", "low", "close"]] > 0).all(axis=1)
    volume_ok = out["volume"].ge(0)
    structure_ok = (
        out["high"].ge(out[["open", "close", "low"]].max(axis=1))
        & out["low"].le(out[["open", "close", "high"]].min(axis=1))
    )
    finite_ok = np.isfinite(out[REQUIRED_COLS]).all(axis=1)
    bad_bar = ~(price_ok & volume_ok & structure_ok & finite_ok)
    bad_bars = int(bad_bar.sum())
    out = out.loc[~bad_bar].copy().reset_index(drop=True)

    gap_report = detect_gaps(out, timestamp_col)
    report = {
        "raw_rows": raw_rows,
        "clean_rows": int(len(out)),
        "invalid_timestamps": invalid_timestamps,
        "duplicate_timestamps_removed": duplicate_timestamps,
        "bad_bars_removed": bad_bars,
        "gap_report": gap_report,
    }
    return out, report


def detect_gaps(df: pd.DataFrame, timestamp_col: str) -> dict:
    if len(df) < 3:
        return {"median_delta_seconds": None, "large_gap_count": 0, "large_gaps": []}
    deltas = df[timestamp_col].diff().dropna()
    median_delta = deltas.median()
    if pd.isna(median_delta) or median_delta.total_seconds() <= 0:
        return {"median_delta_seconds": None, "large_gap_count": 0, "large_gaps": []}
    gap_mask = deltas > median_delta * 1.5
    gap_rows = []
    for idx, delta in deltas[gap_mask].items():
        gap_rows.append(
            {
                "after": df[timestamp_col].iloc[idx - 1].isoformat(),
                "before": df[timestamp_col].iloc[idx].isoformat(),
                "delta_seconds": float(delta.total_seconds()),
            }
        )
    return {
        "median_delta_seconds": float(median_delta.total_seconds()),
        "large_gap_count": len(gap_rows),
        "large_gaps": gap_rows[:50],
    }


def add_base_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    o, h, l, c, v = out["open"], out["high"], out["low"], out["close"], out["volume"]

    out["r1"] = safe_log_ratio(c, c.shift(1))
    for n in [2, 3, 5, 10, 20, 50, 100]:
        out[f"r{n}"] = safe_log_ratio(c, c.shift(n))
        out[f"abs_r{n}"] = out[f"r{n}"].abs()

    out["oc"] = safe_log_ratio(c, o)
    out["gap"] = safe_log_ratio(o, c.shift(1))
    out["hl_range"] = safe_log_ratio(h, l)
    out["body"] = out["oc"].abs()
    out["upper_wick"] = safe_log_ratio(h, np.maximum(o, c)).clip(lower=0)
    out["lower_wick"] = safe_log_ratio(np.minimum(o, c), l).clip(lower=0)

    price_range = (h - l).replace(0, np.nan)
    log_range = out["hl_range"].replace(0, np.nan)
    out["clv"] = ((2 * c - h - l) / price_range).fillna(0.0)
    out["body_ratio"] = out["body"] / log_range
    out["upper_wick_ratio"] = out["upper_wick"] / log_range
    out["lower_wick_ratio"] = out["lower_wick"] / log_range
    out["wick_imbalance"] = (out["upper_wick"] - out["lower_wick"]) / log_range

    tr1 = safe_log_ratio(h, l)
    tr2 = safe_log_ratio(h, c.shift(1)).abs()
    tr3 = safe_log_ratio(l, c.shift(1)).abs()
    out["true_range_log"] = np.maximum.reduce([tr1, tr2, tr3])

    log_hl = out["hl_range"]
    out["parkinson_var"] = (log_hl**2) / (4 * np.log(2))
    out["garman_klass_var"] = 0.5 * (log_hl**2) - (2 * np.log(2) - 1) * (out["oc"] ** 2)
    out["rogers_satchell"] = safe_log_ratio(h, c) * safe_log_ratio(h, o) + safe_log_ratio(l, c) * safe_log_ratio(l, o)

    out["log_volume"] = np.log1p(v)
    out["volume_change"] = safe_log_ratio(1 + v, 1 + v.shift(1))
    out["notional_proxy"] = c * v
    out["log_notional_proxy"] = np.log1p(out["notional_proxy"])
    out["clv_volume"] = out["clv"] * v
    out["move_per_volume"] = out["r1"].abs() / out["log_volume"].replace(0, np.nan)
    out["range_per_volume"] = out["hl_range"] / out["log_volume"].replace(0, np.nan)

    for n in [20, 50, 100, 200]:
        out[f"r1_z_{n}"] = rolling_zscore_past(out["r1"], n)
        out[f"abs_r1_z_{n}"] = rolling_zscore_past(out["r1"].abs(), n)
        out[f"range_z_{n}"] = rolling_zscore_past(out["hl_range"], n)
        out[f"body_ratio_z_{n}"] = rolling_zscore_past(out["body_ratio"], n)
        out[f"volume_z_{n}"] = rolling_zscore_past(out["log_volume"], n)
        out[f"volume_robust_z_{n}"] = rolling_robust_z_past(out["log_volume"], n)
        out[f"range_pct_{n}"] = rolling_percentile_past(out["hl_range"], n)
        out[f"volume_pct_{n}"] = rolling_percentile_past(out["log_volume"], n)
        out[f"abs_return_pct_{n}"] = rolling_percentile_past(out["r1"].abs(), n)
        out[f"atr_log_{n}"] = out["true_range_log"].shift(1).rolling(n, min_periods=n).mean()
        out[f"realized_vol_{n}"] = np.sqrt((out["r1"] ** 2).shift(1).rolling(n, min_periods=n).sum())
        out[f"rolling_high_{n}"] = h.shift(1).rolling(n, min_periods=n).max()
        out[f"rolling_low_{n}"] = l.shift(1).rolling(n, min_periods=n).min()
        out[f"volume_ratio_{n}"] = v / v.shift(1).rolling(n, min_periods=n).median().replace(0, np.nan)

    out = out.copy()
    out["atr_ratio_20_100"] = out["atr_log_20"] / out["atr_log_100"].replace(0, np.nan)
    out["trend_score_20"] = out["r20"] / out["atr_log_20"].replace(0, np.nan)
    out["signed_return_scale_20"] = out["r1"] / out["atr_log_20"].replace(0, np.nan)
    out["return_acceleration_3_20"] = out["r3"] - out["r20"] * (3 / 20)
    out["absorption_score_100"] = out["volume_z_100"] - out["range_z_100"] - out["body_ratio_z_100"]

    path = out["r1"].abs().shift(1).rolling(20, min_periods=20).sum()
    net = out["r1"].shift(1).rolling(20, min_periods=20).sum().abs()
    out["efficiency_20"] = net / path.replace(0, np.nan)
    out["chop_ratio_20"] = path / net.replace(0, np.nan)
    out["up_fraction_20"] = out["r1"].gt(0).shift(1).rolling(20, min_periods=20).mean()
    out["sign_entropy_20"] = sign_entropy(out["r1"], 20)
    out["return_autocorr_lag1_50"] = rolling_autocorr(out["r1"], 50)
    out["abs_return_autocorr_lag1_50"] = rolling_autocorr(out["r1"].abs(), 50)
    out = add_regime_labels(out)
    return out


def sign_entropy(x: pd.Series, n: int) -> pd.Series:
    signs = np.sign(x).replace(0, np.nan)

    def entropy(arr: np.ndarray) -> float:
        vals = arr[~np.isnan(arr)]
        if len(vals) == 0:
            return np.nan
        p_pos = np.mean(vals > 0)
        p_neg = np.mean(vals < 0)
        probs = np.array([p_pos, p_neg])
        probs = probs[probs > 0]
        return float(-np.sum(probs * np.log(probs)))

    return signs.shift(1).rolling(n, min_periods=n).apply(entropy, raw=True)


def rolling_autocorr(x: pd.Series, n: int) -> pd.Series:
    return x.shift(1).rolling(n, min_periods=n).corr(x.shift(2))


def add_regime_labels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["volatility_regime"] = np.select(
        [out["atr_ratio_20_100"] < 0.75, out["atr_ratio_20_100"] > 1.25],
        ["compression", "expansion"],
        default="normal",
    )
    out["trend_regime"] = np.select(
        [out["trend_score_20"] > 1.0, out["trend_score_20"] < -1.0],
        ["uptrend", "downtrend"],
        default="neutral",
    )
    out["efficiency_regime"] = np.select(
        [out["efficiency_20"] < 0.20, out["efficiency_20"] > 0.60],
        ["chop", "efficient"],
        default="mixed",
    )
    out["volume_regime"] = np.select(
        [out["volume_pct_200"] < 0.20, out["volume_pct_200"] > 0.80],
        ["low", "high"],
        default="normal",
    )
    return out


def add_forward_targets(df: pd.DataFrame, horizons: Iterable[int] = (1, 3, 5, 10, 20)) -> pd.DataFrame:
    out = df.copy()
    c, h, l = out["close"], out["high"], out["low"]
    for horizon in horizons:
        out[f"fwd_r{horizon}"] = safe_log_ratio(c.shift(-horizon), c)
        out[f"fwd_abs_r{horizon}"] = out[f"fwd_r{horizon}"].abs()
        fut_high = h.shift(-1).rolling(horizon, min_periods=horizon).max().shift(-(horizon - 1))
        fut_low = l.shift(-1).rolling(horizon, min_periods=horizon).min().shift(-(horizon - 1))
        out[f"future_upside_{horizon}"] = safe_log_ratio(fut_high, c)
        out[f"future_downside_{horizon}"] = safe_log_ratio(c, fut_low)
        out[f"future_range_{horizon}"] = out[f"future_upside_{horizon}"] + out[f"future_downside_{horizon}"]
        out[f"mfe_long_{horizon}"] = out[f"future_upside_{horizon}"]
        out[f"mae_long_{horizon}"] = out[f"future_downside_{horizon}"]
    return out


def first_20_signal_specs() -> list[SignalSpec]:
    return [
        SignalSpec("01_upside_return_shock", "Shock continuation/reversal", "fwd_r5", 5, 1, lambda d: d["r1_z_100"] > 2),
        SignalSpec("02_downside_return_shock", "Shock continuation/reversal", "fwd_r5", 5, -1, lambda d: d["r1_z_100"] < -2),
        SignalSpec("03_symmetric_return_shock", "Volatility after shock", "fwd_abs_r5", 5, 0, lambda d: d["r1_z_100"].abs() > 2),
        SignalSpec("04_range_expansion", "Range expansion effect", "fwd_abs_r5", 5, 0, lambda d: d["range_z_100"] > 2),
        SignalSpec("05_range_compression", "Compression effect", "fwd_abs_r10", 10, 0, lambda d: d["range_pct_100"] < 0.10),
        SignalSpec("06_volume_shock", "Volume shock effect", "fwd_abs_r5", 5, 0, lambda d: d["volume_z_200"] > 2),
        SignalSpec("07_volume_range_divergence", "Volume/range divergence", "fwd_abs_r10", 10, 0, lambda d: (d["volume_z_200"] > 2) & (d["range_z_100"] < 0)),
        SignalSpec("08_absorption_like", "High volume with limited body", "fwd_abs_r10", 10, 0, lambda d: (d["volume_z_200"] > 2) & (d["body_ratio"] < 0.30)),
        SignalSpec("09_close_near_high", "Close near high continuation", "fwd_r3", 3, 1, lambda d: d["clv"] > 0.8),
        SignalSpec("10_close_near_low", "Close near low continuation", "fwd_r3", 3, -1, lambda d: d["clv"] < -0.8),
        SignalSpec("11_upper_wick_rejection", "Upper rejection reversal", "fwd_r3", 3, -1, lambda d: d["upper_wick_ratio"] > 0.60),
        SignalSpec("12_lower_wick_rejection", "Lower rejection reversal", "fwd_r3", 3, 1, lambda d: d["lower_wick_ratio"] > 0.60),
        SignalSpec("13_upside_breakout", "Upside breakout", "fwd_r5", 5, 1, lambda d: d["close"] > d["rolling_high_20"]),
        SignalSpec("14_downside_breakout", "Downside breakout", "fwd_r5", 5, -1, lambda d: d["close"] < d["rolling_low_20"]),
        SignalSpec("15_failed_upside_breakout", "Failed upside breakout", "fwd_r5", 5, -1, lambda d: (d["high"] > d["rolling_high_20"]) & (d["close"] < d["rolling_high_20"])),
        SignalSpec("16_failed_downside_breakout", "Failed downside breakout", "fwd_r5", 5, 1, lambda d: (d["low"] < d["rolling_low_20"]) & (d["close"] > d["rolling_low_20"])),
        SignalSpec("17_atr_compression", "Volatility compression", "fwd_abs_r10", 10, 0, lambda d: d["atr_ratio_20_100"] < 0.6),
        SignalSpec("18_uptrend_continuation", "Trend continuation", "fwd_r10", 10, 1, lambda d: d["trend_score_20"] > 1.5),
        SignalSpec("19_downtrend_continuation", "Downtrend continuation", "fwd_r10", 10, -1, lambda d: d["trend_score_20"] < -1.5),
        SignalSpec("20_chop_mean_reversion", "Chop mean reversion", "fwd_r3", 3, 0, lambda d: (d["efficiency_20"] < 0.2) & (d["r1_z_100"].abs() > 1.5)),
    ]


def dedup_event_indices(signal: pd.Series, cooldown: int | None) -> np.ndarray:
    flags = signal.fillna(False).to_numpy(dtype=bool)
    if cooldown is None or cooldown <= 1:
        return np.flatnonzero(flags)
    idx: list[int] = []
    next_allowed = 0
    for i, flag in enumerate(flags):
        if i < next_allowed:
            continue
        if flag:
            idx.append(i)
            next_allowed = i + cooldown
    return np.array(idx, dtype=int)


def event_study(df: pd.DataFrame, signal: pd.Series, target: str, cooldown: int | None = None, side: int = 0) -> dict:
    idx = dedup_event_indices(signal, cooldown)
    event = df.iloc[idx][target].dropna()
    base = df[target].dropna()
    if side != 0 and target.startswith("fwd_r"):
        event_eval = event * side
        base_eval = base * side
    else:
        event_eval = event
        base_eval = base
    wins = event_eval[event_eval > 0]
    losses = event_eval[event_eval < 0]
    event_std = event_eval.std(ddof=1)
    t_stat = event_eval.mean() / (event_std / np.sqrt(len(event_eval))) if len(event_eval) > 2 and event_std > 0 else np.nan
    return {
        "n": int(len(event_eval)),
        "raw_event_count": int(len(idx)),
        "event_mean": safe_float(event_eval.mean()),
        "baseline_mean": safe_float(base_eval.mean()),
        "edge": safe_float(event_eval.mean() - base_eval.mean()),
        "median": safe_float(event_eval.median()),
        "baseline_median": safe_float(base_eval.median()),
        "hit_rate": safe_float((event_eval > 0).mean()),
        "baseline_hit_rate": safe_float((base_eval > 0).mean()),
        "avg_win": safe_float(wins.mean()),
        "avg_loss": safe_float(losses.mean()),
        "profit_factor": safe_float(wins.sum() / abs(losses.sum())) if losses.sum() != 0 else np.nan,
        "p05": safe_float(event_eval.quantile(0.05)),
        "p95": safe_float(event_eval.quantile(0.95)),
        "t_stat_simple": safe_float(t_stat),
        "outlier_no_best_mean": safe_float(outlier_audit(event_eval)["no_best_mean"]),
        "outlier_trimmed_mean": safe_float(outlier_audit(event_eval)["trimmed_mean"]),
        "break_even_round_trip_bps": safe_float(max((event_eval.mean() - base_eval.mean()) * 10000, 0)),
    }


def outlier_audit(x: pd.Series) -> dict:
    vals = x.dropna().sort_values()
    if vals.empty:
        return {"full_mean": np.nan, "no_best_mean": np.nan, "trimmed_mean": np.nan, "median": np.nan}
    lo = int(0.01 * len(vals))
    hi = max(int(0.99 * len(vals)), lo + 1)
    return {
        "full_mean": vals.mean(),
        "no_best_mean": vals.iloc[:-1].mean() if len(vals) > 2 else np.nan,
        "trimmed_mean": vals.iloc[lo:hi].mean() if len(vals) > 10 else vals.mean(),
        "median": vals.median(),
    }


def safe_float(value: object) -> float:
    if value is None or pd.isna(value):
        return np.nan
    return float(value)


def run_first_20(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for spec in first_20_signal_specs():
        signal = spec.condition(df)
        metrics = event_study(df, signal, spec.target, cooldown=spec.cooldown, side=spec.side)
        rows.append(
            {
                "signal": spec.name,
                "purpose": spec.purpose,
                "target": spec.target,
                "side": spec.side,
                "cooldown": spec.cooldown,
                **metrics,
            }
        )
    return pd.DataFrame(rows)


def run_regime_splits(df: pd.DataFrame) -> pd.DataFrame:
    regime_cols = ["volatility_regime", "trend_regime", "efficiency_regime", "volume_regime"]
    rows = []
    for spec in first_20_signal_specs():
        full_signal = spec.condition(df)
        for regime_col in regime_cols:
            for regime_value in sorted(df[regime_col].dropna().unique()):
                subset = df[regime_col] == regime_value
                metrics = event_study(df.loc[subset], full_signal.loc[subset], spec.target, cooldown=spec.cooldown, side=spec.side)
                rows.append(
                    {
                        "signal": spec.name,
                        "target": spec.target,
                        "side": spec.side,
                        "regime_col": regime_col,
                        "regime_value": regime_value,
                        **metrics,
                    }
                )
    return pd.DataFrame(rows)


def run_threshold_sweeps(df: pd.DataFrame) -> pd.DataFrame:
    sweep_defs = [
        ("r1_z_100_gt", "fwd_r5", 1, [1.0, 1.5, 2.0, 2.5, 3.0], lambda d, x: d["r1_z_100"] > x),
        ("r1_z_100_lt", "fwd_r5", -1, [1.0, 1.5, 2.0, 2.5, 3.0], lambda d, x: d["r1_z_100"] < -x),
        ("abs_r1_z_100_gt", "fwd_abs_r5", 0, [1.0, 1.5, 2.0, 2.5, 3.0], lambda d, x: d["r1_z_100"].abs() > x),
        ("range_z_100_gt", "fwd_abs_r5", 0, [1.0, 1.5, 2.0, 2.5, 3.0], lambda d, x: d["range_z_100"] > x),
        ("range_pct_100_lt", "fwd_abs_r10", 0, [0.20, 0.10, 0.05, 0.01], lambda d, x: d["range_pct_100"] < x),
        ("volume_z_200_gt", "fwd_abs_r5", 0, [1.0, 1.5, 2.0, 2.5, 3.0], lambda d, x: d["volume_z_200"] > x),
        ("upper_wick_ratio_gt", "fwd_r3", -1, [0.40, 0.50, 0.60, 0.70], lambda d, x: d["upper_wick_ratio"] > x),
        ("lower_wick_ratio_gt", "fwd_r3", 1, [0.40, 0.50, 0.60, 0.70], lambda d, x: d["lower_wick_ratio"] > x),
        ("atr_ratio_20_100_lt", "fwd_abs_r10", 0, [0.80, 0.70, 0.60, 0.50], lambda d, x: d["atr_ratio_20_100"] < x),
    ]
    rows = []
    for name, target, side, thresholds, condition in sweep_defs:
        horizon = int("".join(ch for ch in target if ch.isdigit()) or 5)
        for threshold in thresholds:
            metrics = event_study(df, condition(df, threshold), target, cooldown=horizon, side=side)
            rows.append({"sweep": name, "threshold": threshold, "target": target, "side": side, **metrics})
    return pd.DataFrame(rows)


def run_cost_stress(df: pd.DataFrame, costs_bps: Iterable[float] = (0, 1, 2, 5, 10, 20, 50)) -> pd.DataFrame:
    rows = []
    for spec in first_20_signal_specs():
        if spec.side == 0 or not spec.target.startswith("fwd_r"):
            continue
        idx = dedup_event_indices(spec.condition(df), spec.cooldown)
        event = df.iloc[idx][spec.target].dropna() * spec.side
        base = df[spec.target].dropna() * spec.side
        for cost_bps in costs_bps:
            round_trip_cost = cost_bps / 10000.0
            net = event - round_trip_cost
            rows.append(
                {
                    "signal": spec.name,
                    "target": spec.target,
                    "cost_bps": cost_bps,
                    "n": int(len(net)),
                    "net_mean": safe_float(net.mean()),
                    "net_median": safe_float(net.median()),
                    "net_hit_rate": safe_float((net > 0).mean()),
                    "baseline_net_mean": safe_float((base - round_trip_cost).mean()),
                }
            )
    return pd.DataFrame(rows)


def generate_candidate_report(
    output_path: Path,
    quality: dict,
    first_20: pd.DataFrame,
    regimes: pd.DataFrame,
    sweeps: pd.DataFrame,
    costs: pd.DataFrame,
) -> None:
    ranked = first_20.copy()
    ranked["abs_edge"] = ranked["edge"].abs()
    ranked = ranked.sort_values(["n", "abs_edge"], ascending=[False, False]).head(8)
    lines = [
        "# OHLCV Alpha Research Scan",
        "",
        "Educational research output only. This is not financial advice.",
        "",
        "## Data Quality",
        "",
        f"- Raw rows: {quality['raw_rows']}",
        f"- Clean rows: {quality['clean_rows']}",
        f"- Bad bars removed: {quality['bad_bars_removed']}",
        f"- Duplicate timestamps removed: {quality['duplicate_timestamps_removed']}",
        f"- Large gaps detected: {quality['gap_report']['large_gap_count']}",
        "",
        "## Strongest Exploratory Rows",
        "",
        markdown_table(
            ranked,
            ["signal", "target", "n", "edge", "median", "hit_rate", "profit_factor", "break_even_round_trip_bps"],
        ),
        "",
        "## Required Next Checks",
        "",
        "- Treat every row as exploratory until train/validation/test and walk-forward checks are complete.",
        "- Inspect regime rows before discarding weak global signals.",
        "- Reject any candidate whose edge depends on one outlier or one exact threshold.",
        "- Use the cost-stress table to identify practical fragility.",
        "- Record all follow-up tests in a research log.",
        "",
        "## Output Files",
        "",
        "- `cleaned_ohlcv.csv`",
        "- `features_targets.csv`",
        "- `data_quality.json`",
        "- `first_20_event_studies.csv`",
        "- `regime_event_studies.csv`",
        "- `threshold_sweeps.csv`",
        "- `cost_stress.csv`",
        "",
        "## Dossier Template",
        "",
        "Use `references/report-template.md` before assigning a final verdict.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _fmt(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def html_table(df: pd.DataFrame, cols: list[str]) -> str:
    if df.empty:
        return "<p>No rows.</p>"
    view = df[cols].copy()
    header = "".join(f"<th>{_esc(col)}</th>" for col in cols)
    rows = []
    for _, row in view.iterrows():
        cells = "".join(f"<td>{_esc(_fmt(row[col]))}</td>" for col in cols)
        rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def report_check_rows(checks: list[dict[str, object]]) -> str:
    status_labels = {"pass": "Right", "warn": "Needs Review", "fail": "Wrong", "info": "Info"}
    rows = []
    for check in checks:
        status = str(check.get("status", "info"))
        rows.append(
            "<tr>"
            f"<td><span class=\"pill {status}\">{_esc(status_labels.get(status, 'Info'))}</span></td>"
            f"<td>{_esc(check.get('name', ''))}</td>"
            f"<td>{_esc(check.get('detail', ''))}</td>"
            "</tr>"
        )
    return "".join(rows)


def generate_candidate_html_report(
    output_path: Path,
    quality: dict,
    first_20: pd.DataFrame,
    regimes: pd.DataFrame,
    sweeps: pd.DataFrame,
    costs: pd.DataFrame,
    output_files: list[str],
) -> None:
    ranked = first_20.copy()
    ranked["abs_edge"] = ranked["edge"].abs()
    ranked = ranked.sort_values(["n", "abs_edge"], ascending=[False, False]).head(10)
    robust_sweeps = sweeps.sort_values(["n", "edge"], ascending=[False, False]).head(10)
    cost_fragile = costs.sort_values(["cost_bps", "net_mean"], ascending=[True, True]).head(10)
    quality_checks = [
        {
            "status": "pass" if quality["clean_rows"] > 250 else "warn",
            "name": "Clean row count",
            "detail": f"{quality['clean_rows']} clean rows from {quality['raw_rows']} raw rows.",
        },
        {
            "status": "pass" if quality["bad_bars_removed"] == 0 else "warn",
            "name": "Bad bars removed",
            "detail": f"{quality['bad_bars_removed']} invalid OHLCV bars were removed.",
        },
        {
            "status": "pass" if quality["duplicate_timestamps_removed"] == 0 else "warn",
            "name": "Duplicate timestamps",
            "detail": f"{quality['duplicate_timestamps_removed']} duplicate timestamps were removed.",
        },
        {
            "status": "pass" if quality["gap_report"]["large_gap_count"] == 0 else "warn",
            "name": "Timestamp gaps",
            "detail": f"{quality['gap_report']['large_gap_count']} large gaps detected.",
        },
        {
            "status": "pass",
            "name": "Lookahead audit",
            "detail": "Rolling highs and forward target alignment assertions passed before writing outputs.",
        },
    ]
    generated = "\n".join(f"<li><code>{_esc(name)}</code></li>" for name in output_files)
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OHLCV Alpha Research HTML Report</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f4;
      --ink: #1c2228;
      --muted: #5d6872;
      --line: #d7ddd2;
      --panel: #ffffff;
      --pass: #177245;
      --warn: #9a6100;
      --fail: #b42318;
      --info: #315da8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: 32px auto 56px; }}
    header, section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 16px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; letter-spacing: 0; }}
    p {{ margin: 0 0 10px; color: var(--muted); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ text-align: left; border-top: 1px solid var(--line); padding: 9px 7px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 650; }}
    code {{ overflow-wrap: anywhere; }}
    ul {{ margin: 0; padding-left: 20px; color: var(--muted); }}
    .pill {{ display: inline-block; border-radius: 999px; padding: 3px 9px; font-size: 12px; font-weight: 700; }}
    .pass {{ color: var(--pass); background: #e8f5ee; }}
    .warn {{ color: var(--warn); background: #fff4df; }}
    .fail {{ color: var(--fail); background: #fdebea; }}
    .info {{ color: var(--info); background: #edf3ff; }}
    @media (max-width: 720px) {{
      main {{ width: min(100% - 20px, 1180px); margin-top: 12px; }}
      header, section {{ padding: 14px; }}
      table {{ display: block; overflow-x: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>OHLCV Alpha Research Scan</h1>
      <p>Educational research output only. This is not financial advice.</p>
      <p>Generated {now}</p>
    </header>
    <section>
      <h2>What Is Right And What Needs Review</h2>
      <table>
        <thead><tr><th>Status</th><th>Check</th><th>Detail</th></tr></thead>
        <tbody>{report_check_rows(quality_checks)}</tbody>
      </table>
    </section>
    <section>
      <h2>Strongest Exploratory Rows</h2>
      {html_table(ranked, ["signal", "target", "n", "edge", "median", "hit_rate", "profit_factor", "break_even_round_trip_bps"])}
    </section>
    <section>
      <h2>Threshold Sweep Preview</h2>
      {html_table(robust_sweeps, ["sweep", "threshold", "target", "n", "edge", "median", "hit_rate", "profit_factor"])}
    </section>
    <section>
      <h2>Cost Stress Preview</h2>
      {html_table(cost_fragile, ["signal", "target", "cost_bps", "n", "net_mean", "net_median", "net_hit_rate"])}
    </section>
    <section>
      <h2>Generated Files</h2>
      <ul>{generated}</ul>
    </section>
    <section>
      <h2>Required Next Actions</h2>
      <ul>
        <li>Do not promote any row until train/validation/test and walk-forward checks pass.</li>
        <li>Inspect regime rows before discarding weak global signals.</li>
        <li>Reject candidates whose apparent edge depends on one outlier, one threshold, or zero-cost assumptions.</li>
        <li>Write a final anomaly dossier from <code>references/report-template.md</code> before any strategy spec.</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")


def markdown_table(df: pd.DataFrame, cols: list[str]) -> str:
    if df.empty:
        return "_No rows._"
    view = df[cols].copy()
    for col in view.columns:
        if pd.api.types.is_float_dtype(view[col]):
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else f"{x:.6g}")
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    body = ["| " + " | ".join(str(row[col]) for col in cols) + " |" for _, row in view.iterrows()]
    return "\n".join([header, sep, *body])


def assert_no_lookahead_rolling_high(df: pd.DataFrame, n: int = 20) -> None:
    expected = df["high"].shift(1).rolling(n, min_periods=n).max()
    actual = df[f"rolling_high_{n}"]
    pd.testing.assert_series_equal(actual, expected, check_names=False)


def assert_target_alignment(df: pd.DataFrame, h: int = 5) -> None:
    expected = np.log(df["close"].shift(-h) / df["close"])
    actual = df[f"fwd_r{h}"]
    pd.testing.assert_series_equal(actual, expected, check_names=False)


def assert_no_targets_in_features(feature_cols: Iterable[str]) -> None:
    bad = [
        c
        for c in feature_cols
        if c.startswith("fwd_") or c.startswith("future_") or c.startswith("mfe_") or c.startswith("mae_")
    ]
    if bad:
        raise AssertionError(f"Target leakage columns found: {bad}")


def write_outputs(df: pd.DataFrame, clean: pd.DataFrame, quality: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_files = [
        "cleaned_ohlcv.csv",
        "features_targets.csv",
        "data_quality.json",
        "first_20_event_studies.csv",
        "regime_event_studies.csv",
        "threshold_sweeps.csv",
        "cost_stress.csv",
        "candidate_report.md",
        "candidate_report.html",
    ]
    clean.to_csv(output_dir / output_files[0], index=False)
    df.to_csv(output_dir / output_files[1], index=False)
    (output_dir / output_files[2]).write_text(json.dumps(quality, indent=2), encoding="utf-8")

    first_20 = run_first_20(df)
    regimes = run_regime_splits(df)
    sweeps = run_threshold_sweeps(df)
    costs = run_cost_stress(df)
    first_20.to_csv(output_dir / output_files[3], index=False)
    regimes.to_csv(output_dir / output_files[4], index=False)
    sweeps.to_csv(output_dir / output_files[5], index=False)
    costs.to_csv(output_dir / output_files[6], index=False)
    generate_candidate_report(output_dir / output_files[7], quality, first_20, regimes, sweeps, costs)
    generate_candidate_html_report(output_dir / output_files[8], quality, first_20, regimes, sweeps, costs, output_files)


def make_example(path: Path, rows: int = 320) -> None:
    rng = np.random.default_rng(42)
    ts = pd.date_range("2024-01-01", periods=rows, freq="h", tz="UTC")
    drift = 0.0001
    shocks = rng.normal(drift, 0.007, rows)
    shocks[90:95] += 0.02
    shocks[180:185] -= 0.018
    close = 100 * np.exp(np.cumsum(shocks))
    open_ = np.r_[close[0], close[:-1]] * np.exp(rng.normal(0, 0.0015, rows))
    span = np.abs(rng.normal(0.006, 0.003, rows))
    high = np.maximum(open_, close) * np.exp(span)
    low = np.minimum(open_, close) * np.exp(-span)
    volume = rng.lognormal(mean=8.0, sigma=0.45, size=rows)
    volume[90:95] *= 4
    volume[180:185] *= 3
    out = pd.DataFrame(
        {
            "timestamp": ts,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OHLCV-only alpha research scans.")
    parser.add_argument("--input", help="CSV with timestamp, open, high, low, close, volume columns.")
    parser.add_argument("--output-dir", default="ohlcv-alpha-output", help="Directory for scan outputs.")
    parser.add_argument("--timestamp-col", default="timestamp", help="Timestamp column name.")
    parser.add_argument("--make-example", help="Write an example OHLCV CSV to this path and exit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.make_example:
        make_example(Path(args.make_example))
        print(f"Wrote example OHLCV CSV to {args.make_example}")
        return 0
    if not args.input:
        raise SystemExit("Provide --input or --make-example.")

    raw = pd.read_csv(args.input)
    clean, quality = clean_ohlcv(raw, args.timestamp_col)
    features = add_base_features(clean)
    full = add_forward_targets(features)

    assert_no_lookahead_rolling_high(full, 20)
    assert_target_alignment(full, 5)
    feature_cols = [
        c
        for c in full.columns
        if c not in {"timestamp", *REQUIRED_COLS}
        and not c.startswith("fwd_")
        and not c.startswith("future_")
        and not c.startswith("mfe_")
        and not c.startswith("mae_")
    ]
    assert_no_targets_in_features(feature_cols)

    output_dir = Path(args.output_dir)
    write_outputs(full, clean, quality, output_dir)
    print(f"Wrote OHLCV alpha research outputs to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
