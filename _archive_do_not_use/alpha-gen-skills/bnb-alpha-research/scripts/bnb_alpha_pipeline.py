#!/usr/bin/env python3
"""BNB-specific alpha research pipeline.

Downloads Binance public candles, computes past-only BNB features, scans
anomaly events, writes heatmaps, and emits strategy-candidate JSON.
Uses Binance US spot klines as a fallback when global Binance is unavailable.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

UTC = dt.timezone.utc
SPOT_BASES = ["https://api.binance.com", "https://api.binance.us"]
FUTURES_BASE = "https://fapi.binance.com"
HORIZONS = [1, 3, 6, 12, 24]
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
    "timestamp",
    "open_time_ms",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_volume",
    "trade_count",
    "source",
]
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
}


def parse_date(value: str) -> int:
    parsed = dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(parsed.timestamp() * 1000)


def iso_utc(ms: int) -> str:
    return dt.datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat().replace("+00:00", "Z")


def request_json(url: str, retries: int = 4) -> list[list[object]]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "bnb-alpha-research/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
            data = json.loads(payload)
            if isinstance(data, dict) and "code" in data:
                raise RuntimeError(data)
            return data
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 451:
                raise
            time.sleep(1.5 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed after {retries} attempts: {last_error}")


def endpoints(market: str) -> list[tuple[str, str]]:
    if market == "spot":
        return [(base, "/api/v3/klines") for base in SPOT_BASES]
    if market == "usd_m_futures":
        return [(FUTURES_BASE, "/fapi/v1/klines")]
    raise ValueError(f"unsupported market: {market}")


def fetch_klines(market: str, symbol: str, interval: str, start_ms: int, end_ms: int) -> list[list[object]]:
    if interval not in INTERVAL_MS:
        raise ValueError(f"unsupported interval: {interval}")
    sources = endpoints(market)
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
        batch = None
        errors = []
        for base, path in sources:
            try:
                batch = request_json(f"{base}{path}?{params}")
                break
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{base}: {exc}")
        if batch is None:
            raise RuntimeError("; ".join(errors))
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1][0]) + INTERVAL_MS[interval]
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)
    return rows


def write_raw(path: Path, rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(RAW_COLUMNS)
        writer.writerows(rows)


def clean_rows(rows: list[list[object]], *, symbol: str, market: str, interval: str) -> pd.DataFrame:
    cleaned = []
    seen: set[int] = set()
    for row in rows:
        item = dict(zip(RAW_COLUMNS, row))
        open_ms = int(item["open_time_ms"])
        if open_ms in seen:
            continue
        seen.add(open_ms)
        cleaned.append(
            {
                "symbol": symbol,
                "market": market,
                "interval": interval,
                "timestamp": iso_utc(open_ms),
                "open_time_ms": open_ms,
                "open": item["open"],
                "high": item["high"],
                "low": item["low"],
                "close": item["close"],
                "volume": item["volume"],
                "quote_volume": item["quote_volume"],
                "trade_count": item["trade_count"],
                "source": "binance_public_klines",
            }
        )
    df = pd.DataFrame(cleaned, columns=CLEAN_COLUMNS)
    return df.sort_values("open_time_ms").reset_index(drop=True)


def write_clean(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def generate_example_data(output_dir: Path, market: str, interval: str) -> None:
    rng = np.random.default_rng(7)
    rows = 1200
    timestamps = pd.date_range("2024-01-01", periods=rows, freq="h", tz="UTC")
    base_factors = rng.normal(0.00005, 0.007, rows)
    btc = make_symbol_frame("BTCUSDT", market, interval, timestamps, base_factors, 42000, rng)
    eth = make_symbol_frame("ETHUSDT", market, interval, timestamps, base_factors * 1.1 + rng.normal(0, 0.004, rows), 2200, rng)
    bnb_shocks = base_factors * 0.9 + rng.normal(0.00008, 0.009, rows)
    bnb_shocks[240:250] += 0.025
    bnb_shocks[620:630] -= 0.022
    bnb = make_symbol_frame("BNBUSDT", market, interval, timestamps, bnb_shocks, 310, rng)
    for frame in [bnb, btc, eth]:
        symbol = str(frame["symbol"].iloc[0])
        path = output_dir / "clean" / market / symbol / f"{interval}.csv"
        write_clean(path, frame)


def make_symbol_frame(
    symbol: str,
    market: str,
    interval: str,
    timestamps: pd.DatetimeIndex,
    returns: np.ndarray,
    start_price: float,
    rng: np.random.Generator,
) -> pd.DataFrame:
    close = start_price * np.exp(np.cumsum(returns))
    open_ = np.r_[close[0], close[:-1]] * np.exp(rng.normal(0, 0.0015, len(close)))
    span = np.abs(rng.normal(0.006, 0.0025, len(close)))
    high = np.maximum(open_, close) * np.exp(span)
    low = np.minimum(open_, close) * np.exp(-span)
    volume = rng.lognormal(9.2 if symbol == "BNBUSDT" else 10.5, 0.4, len(close))
    if symbol == "BNBUSDT":
        volume[240:250] *= 4
        volume[620:630] *= 3
    return pd.DataFrame(
        {
            "symbol": symbol,
            "market": market,
            "interval": interval,
            "timestamp": timestamps.astype(str).str.replace("+00:00", "Z", regex=False),
            "open_time_ms": (timestamps.view("int64") // 1_000_000).astype(np.int64),
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "quote_volume": close * volume,
            "trade_count": rng.integers(1000, 7000, len(close)),
            "source": "synthetic_example_not_live_data",
        }
    )


def load_clean(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    for col in ["open", "high", "low", "close", "volume", "quote_volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    valid = (
        df["open"].gt(0)
        & df["high"].gt(0)
        & df["low"].gt(0)
        & df["close"].gt(0)
        & df["volume"].ge(0)
        & df["high"].ge(df[["open", "close", "low"]].max(axis=1))
        & df["low"].le(df[["open", "close", "high"]].min(axis=1))
    )
    return df.loc[valid].reset_index(drop=True)


def rolling_zscore_past(series: pd.Series, window: int) -> pd.Series:
    hist = series.shift(1)
    return (series - hist.rolling(window, min_periods=window).mean()) / hist.rolling(window, min_periods=window).std(ddof=1)


def safe_log_ratio(a: pd.Series, b: pd.Series) -> pd.Series:
    return np.log(np.maximum(a, 1e-12) / np.maximum(b, 1e-12))


def build_features(frames: dict[str, pd.DataFrame], target_symbol: str) -> pd.DataFrame:
    target = frames[target_symbol].copy()
    target = target.rename(columns={"close": "target_close"})
    target["close"] = target["target_close"]
    o, h, low, c, v = target["open"], target["high"], target["low"], target["close"], target["volume"]
    target["r1"] = safe_log_ratio(c, c.shift(1))
    for n in [3, 6, 12, 20, 24, 50, 100]:
        target[f"r{n}"] = safe_log_ratio(c, c.shift(n))
    target["hl_range"] = safe_log_ratio(h, low)
    target["body"] = safe_log_ratio(c, o).abs()
    price_range = (h - low).replace(0, np.nan)
    log_range = target["hl_range"].replace(0, np.nan)
    target["clv"] = ((2 * c - h - low) / price_range).fillna(0)
    target["upper_wick_ratio"] = (safe_log_ratio(h, np.maximum(o, c)).clip(lower=0) / log_range).fillna(0)
    target["lower_wick_ratio"] = (safe_log_ratio(np.minimum(o, c), low).clip(lower=0) / log_range).fillna(0)
    target["log_volume"] = np.log1p(v)
    target["r1_z_100"] = rolling_zscore_past(target["r1"], 100)
    target["range_z_100"] = rolling_zscore_past(target["hl_range"], 100)
    target["volume_z_100"] = rolling_zscore_past(target["log_volume"], 100)
    target["volume_z_200"] = rolling_zscore_past(target["log_volume"], 200)
    tr = np.maximum.reduce(
        [
            safe_log_ratio(h, low),
            safe_log_ratio(h, c.shift(1)).abs(),
            safe_log_ratio(low, c.shift(1)).abs(),
        ]
    )
    target["atr_log_20"] = pd.Series(tr, index=target.index).shift(1).rolling(20, min_periods=20).mean()
    target["atr_log_100"] = pd.Series(tr, index=target.index).shift(1).rolling(100, min_periods=100).mean()
    target["atr_ratio_20_100"] = target["atr_log_20"] / target["atr_log_100"].replace(0, np.nan)
    target["rolling_high_20"] = h.shift(1).rolling(20, min_periods=20).max()
    target["rolling_low_20"] = low.shift(1).rolling(20, min_periods=20).min()
    target["ema_20"] = c.ewm(span=20, adjust=False).mean()
    target["ema_50"] = c.ewm(span=50, adjust=False).mean()
    target["trend_score_20"] = target["r20"] / target["atr_log_20"].replace(0, np.nan)
    target["volatility_regime"] = np.select(
        [target["atr_ratio_20_100"] < 0.75, target["atr_ratio_20_100"] > 1.25],
        ["compression", "expansion"],
        default="normal",
    )
    target["trend_regime"] = np.select(
        [target["trend_score_20"] > 1.0, target["trend_score_20"] < -1.0],
        ["uptrend", "downtrend"],
        default="neutral",
    )
    target["volume_regime"] = np.select(
        [target["volume_z_200"] > 1.0, target["volume_z_200"] < -1.0],
        ["high", "low"],
        default="normal",
    )
    for symbol, frame in frames.items():
        if symbol == target_symbol:
            continue
        context = frame[["timestamp", "close"]].copy()
        prefix = symbol.replace("USDT", "").lower()
        context[f"{prefix}_r20"] = safe_log_ratio(context["close"], context["close"].shift(20))
        context[f"{prefix}_ema50"] = context["close"].ewm(span=50, adjust=False).mean()
        context[f"{prefix}_risk_on"] = context["close"] > context[f"{prefix}_ema50"]
        target = target.merge(context[["timestamp", f"{prefix}_r20", f"{prefix}_risk_on"]], on="timestamp", how="left")
    target["btc_regime"] = np.where(target.get("btc_risk_on", pd.Series(False, index=target.index)).fillna(False), "btc_risk_on", "btc_risk_off")
    for hzn in HORIZONS:
        target[f"fwd_r{hzn}"] = safe_log_ratio(c.shift(-hzn), c)
    target["hour_utc"] = target["timestamp"].dt.hour
    target["day_of_week"] = target["timestamp"].dt.day_name().str[:3]
    return target


EventCondition = Callable[[pd.DataFrame], pd.Series]


def event_definitions() -> dict[str, EventCondition]:
    return {
        "upside_return_shock": lambda d: d["r1_z_100"] > 2.0,
        "downside_return_shock": lambda d: d["r1_z_100"] < -2.0,
        "range_expansion": lambda d: d["range_z_100"] > 2.0,
        "volume_shock": lambda d: d["volume_z_200"] > 2.0,
        "absorption_volume_no_body": lambda d: (d["volume_z_200"] > 1.5) & (d["body"] / d["hl_range"].replace(0, np.nan) < 0.30),
        "close_near_high": lambda d: d["clv"] > 0.80,
        "close_near_low": lambda d: d["clv"] < -0.80,
        "upside_breakout_20": lambda d: d["close"] > d["rolling_high_20"],
        "downside_breakout_20": lambda d: d["close"] < d["rolling_low_20"],
        "atr_compression": lambda d: d["atr_ratio_20_100"] < 0.70,
        "compression_breakout": lambda d: (d["atr_ratio_20_100"] < 0.85) & (d["close"] > d["rolling_high_20"]),
        "btc_risk_on_breakout": lambda d: d["btc_regime"].eq("btc_risk_on") & (d["close"] > d["rolling_high_20"]),
        "btc_risk_off_downshock": lambda d: d["btc_regime"].eq("btc_risk_off") & (d["r1_z_100"] < -1.5),
    }


def dedup_events(flags: pd.Series, cooldown: int) -> np.ndarray:
    arr = flags.fillna(False).to_numpy(dtype=bool)
    selected = []
    next_allowed = 0
    for idx, flag in enumerate(arr):
        if idx < next_allowed:
            continue
        if flag:
            selected.append(idx)
            next_allowed = idx + max(cooldown, 1)
    return np.array(selected, dtype=int)


def profit_factor(values: pd.Series) -> float:
    wins = values[values > 0].sum()
    losses = values[values < 0].sum()
    if losses == 0:
        return float("nan")
    return float(wins / abs(losses))


def run_event_studies(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for event, condition in event_definitions().items():
        flags = condition(features)
        for horizon in HORIZONS:
            target = f"fwd_r{horizon}"
            idx = dedup_events(flags, horizon)
            event_values = features.iloc[idx][target].dropna()
            baseline = features[target].dropna()
            edge = event_values.mean() - baseline.mean()
            std = event_values.std(ddof=1)
            t_stat = event_values.mean() / (std / math.sqrt(len(event_values))) if len(event_values) > 2 and std > 0 else np.nan
            rows.append(
                {
                    "event": event,
                    "horizon": horizon,
                    "n": int(len(event_values)),
                    "event_mean": event_values.mean(),
                    "baseline_mean": baseline.mean(),
                    "edge": edge,
                    "edge_bps": edge * 10000,
                    "median": event_values.median(),
                    "hit_rate": (event_values > 0).mean(),
                    "baseline_hit_rate": (baseline > 0).mean(),
                    "hit_delta": (event_values > 0).mean() - (baseline > 0).mean(),
                    "profit_factor": profit_factor(event_values),
                    "t_stat_simple": t_stat,
                    "break_even_round_trip_bps": max(edge * 10000, 0),
                }
            )
    return pd.DataFrame(rows)


def regime_event_heatmap(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for regime_col in ["volatility_regime", "trend_regime", "volume_regime", "btc_regime"]:
        for regime, subset in features.groupby(regime_col):
            baseline = subset["fwd_r24"].dropna()
            for event, condition in event_definitions().items():
                flags = condition(subset)
                idx = dedup_events(flags, 24)
                vals = subset.iloc[idx]["fwd_r24"].dropna()
                rows.append(
                    {
                        "regime_col": regime_col,
                        "regime": regime,
                        "event": event,
                        "n": int(len(vals)),
                        "edge_bps": (vals.mean() - baseline.mean()) * 10000,
                        "hit_delta": (vals > 0).mean() - (baseline > 0).mean(),
                    }
                )
    return pd.DataFrame(rows)


def calendar_heatmap(features: pd.DataFrame) -> pd.DataFrame:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    grouped = (
        features.dropna(subset=["fwd_r24"])
        .groupby(["day_of_week", "hour_utc"])["fwd_r24"]
        .mean()
        .mul(10000)
        .reset_index(name="fwd_24h_bps")
    )
    grouped["day_of_week"] = pd.Categorical(grouped["day_of_week"], categories=days, ordered=True)
    return grouped.sort_values(["day_of_week", "hour_utc"])


def pivot_heatmap(df: pd.DataFrame, value: str) -> pd.DataFrame:
    return df.pivot_table(index="event", columns="horizon", values=value, aggfunc="mean").reset_index()


def candidate_specs(
    events: pd.DataFrame,
    target_symbol: str,
    market: str,
    interval: str,
    *,
    synthetic_mode: bool,
) -> list[dict[str, object]]:
    ranked = events[(events["n"] >= 20) & events["edge_bps"].abs().ge(5)].copy()
    if ranked.empty:
        ranked = events.sort_values(["n", "edge_bps"], ascending=[False, False]).head(5).copy()
    ranked["score"] = ranked["edge_bps"].abs() * np.sqrt(ranked["n"].clip(lower=1))
    ranked = ranked.sort_values("score", ascending=False).head(5)
    specs = []
    for _, row in ranked.iterrows():
        direction = "long" if row["edge_bps"] >= 0 else "short_or_avoid_long"
        specs.append(
            {
                "strategy_name": f"BNB_{row['event']}_{int(row['horizon'])}h",
                "target_symbol": target_symbol,
                "market": market,
                "timeframe": interval,
                "event": row["event"],
                "direction": direction,
                "entry_rules": [f"event == {row['event']}", "execute on next candle open"],
                "exit_rules": [f"bars_held >= {int(row['horizon'])}", "or stop/take-profit hit first"],
                "risk_rules": {
                    "max_position_size_pct": 10,
                    "stop_loss_atr_multiple": 2.0,
                    "take_profit_atr_multiple": 3.0,
                    "reject_if_expected_edge_bps_below": 10,
                },
                "backtest_config": {
                    "fee_bps": 10,
                    "slippage_bps": 5,
                    "execution": "next_candle_open",
                    "lookahead_bias": "not_allowed",
                },
                "evidence": {
                    "n": int(row["n"]),
                    "edge_bps": float(row["edge_bps"]),
                    "hit_delta": float(row["hit_delta"]) if pd.notna(row["hit_delta"]) else None,
                    "profit_factor": float(row["profit_factor"]) if pd.notna(row["profit_factor"]) else None,
                    "t_stat_simple": float(row["t_stat_simple"]) if pd.notna(row["t_stat_simple"]) else None,
                },
                "data_provenance": {
                    "historical_ohlcv_source": "synthetic_example" if synthetic_mode else "binance_public_klines",
                    "live_context_source": "coinmarketcap_optional_not_required_for_this_backtest",
                    "synthetic_mode": synthetic_mode,
                },
            }
        )
    return specs


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def heat_color(value: float, limit: float) -> str:
    if pd.isna(value):
        return "#f1f3f5"
    clipped = max(min(float(value) / limit, 1), -1)
    if clipped >= 0:
        strength = int(230 - 90 * clipped)
        return f"rgb({strength}, 245, {strength + 10})"
    strength = int(230 - 90 * abs(clipped))
    return f"rgb(250, {strength}, {strength})"


def html_heatmap(df: pd.DataFrame, value_limit: float) -> str:
    if df.empty:
        return "<p>No heatmap rows.</p>"
    cols = [col for col in df.columns if col != "event"]
    header = "<th>event</th>" + "".join(f"<th>{esc(col)}</th>" for col in cols)
    rows = []
    for _, row in df.iterrows():
        cells = [f"<td><code>{esc(row['event'])}</code></td>"]
        for col in cols:
            val = row[col]
            label = "" if pd.isna(val) else f"{float(val):.2f}"
            cells.append(f"<td style=\"background:{heat_color(val, value_limit)}\">{esc(label)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def html_calendar_heatmap(df: pd.DataFrame) -> str:
    if df.empty:
        return "<p>No calendar rows.</p>"
    pivot = df.pivot_table(index="day_of_week", columns="hour_utc", values="fwd_24h_bps", aggfunc="mean")
    header = "<th>day</th>" + "".join(f"<th>{hour}</th>" for hour in pivot.columns)
    rows = []
    for day, row in pivot.iterrows():
        cells = [f"<td><b>{esc(day)}</b></td>"]
        for value in row:
            label = "" if pd.isna(value) else f"{value:.1f}"
            cells.append(f"<td style=\"background:{heat_color(value, 40)}\">{esc(label)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def write_report(
    path: Path,
    *,
    target_symbol: str,
    data_quality: list[dict[str, object]],
    events: pd.DataFrame,
    edge_heatmap: pd.DataFrame,
    hit_heatmap: pd.DataFrame,
    regime_heatmap: pd.DataFrame,
    calendar: pd.DataFrame,
    candidates: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    top = events.sort_values(["n", "edge_bps"], ascending=[False, False]).head(12)
    quality_rows = "".join(
        f"<tr><td>{esc(item['symbol'])}</td><td>{esc(item['rows'])}</td><td>{esc(item['start'])}</td><td>{esc(item['end'])}</td><td>{esc(item['source'])}</td></tr>"
        for item in data_quality
    )
    top_rows = "".join(
        "<tr>"
        f"<td><code>{esc(row.event)}</code></td><td>{int(row.horizon)}</td><td>{int(row.n)}</td>"
        f"<td>{row.edge_bps:.2f}</td><td>{row.hit_delta:.3f}</td><td>{row.profit_factor:.3f}</td>"
        "</tr>"
        for _, row in top.iterrows()
    )
    candidate_items = "".join(
        f"<li><code>{esc(item['strategy_name'])}</code>: {esc(item['event'])}, edge {item['evidence']['edge_bps']:.2f} bps, n={item['evidence']['n']}</li>"
        for item in candidates
    )
    now = dt.datetime.now(UTC).isoformat().replace("+00:00", "Z")
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BNB Alpha Research Report</title>
  <style>
    body {{ margin: 0; background: #f6f7f4; color: #1d242b; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.45; }}
    main {{ width: min(1240px, calc(100% - 32px)); margin: 32px auto 56px; }}
    header, section {{ background: white; border: 1px solid #d9dfd5; border-radius: 8px; padding: 20px; margin-bottom: 16px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; letter-spacing: 0; }}
    p {{ color: #59636d; margin: 0 0 10px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border-top: 1px solid #d9dfd5; padding: 8px 7px; text-align: right; vertical-align: top; }}
    th:first-child, td:first-child {{ text-align: left; }}
    th {{ color: #59636d; font-weight: 650; }}
    code {{ overflow-wrap: anywhere; }}
    ul {{ margin: 0; padding-left: 20px; color: #59636d; }}
    .scroll {{ overflow-x: auto; }}
    @media (max-width: 760px) {{ main {{ width: min(100% - 20px, 1240px); margin-top: 12px; }} header, section {{ padding: 14px; }} }}
  </style>
</head>
<body>
<main>
  <header>
    <h1>BNB Alpha Research Report</h1>
    <p>Target: {esc(target_symbol)}. Generated {now}. Educational research output only; not financial advice.</p>
    <p>Green cells are positive edge; red cells are negative edge. Heatmaps are exploratory and require out-of-sample validation.</p>
  </header>
  <section>
    <h2>Data Quality</h2>
    <table><thead><tr><th>symbol</th><th>rows</th><th>start</th><th>end</th><th>source</th></tr></thead><tbody>{quality_rows}</tbody></table>
  </section>
  <section>
    <h2>Strongest Event Rows</h2>
    <table><thead><tr><th>event</th><th>horizon</th><th>n</th><th>edge bps</th><th>hit delta</th><th>profit factor</th></tr></thead><tbody>{top_rows}</tbody></table>
  </section>
  <section>
    <h2>Edge Heatmap Bps</h2>
    <div class="scroll">{html_heatmap(edge_heatmap, 50)}</div>
  </section>
  <section>
    <h2>Hit Rate Delta Heatmap</h2>
    <div class="scroll">{html_heatmap(hit_heatmap, 0.15)}</div>
  </section>
  <section>
    <h2>Regime Edge Heatmap Bps</h2>
    <p>24-hour forward return edge by BNB regime and event.</p>
    <div class="scroll">{html_heatmap(regime_heatmap, 70)}</div>
  </section>
  <section>
    <h2>Calendar Heatmap</h2>
    <p>Average next-24-hour BNB return in bps by UTC day/hour.</p>
    <div class="scroll">{html_calendar_heatmap(calendar)}</div>
  </section>
  <section>
    <h2>Strategy Candidates</h2>
    <ul>{candidate_items or "<li>No candidates met the minimum evidence threshold.</li>"}</ul>
  </section>
  <section>
    <h2>Next Quant Checks</h2>
    <ul>
      <li>Split chronologically into train, validation, and test windows.</li>
      <li>Run walk-forward parameter selection without reusing future data.</li>
      <li>Stress fee, slippage, missed fills, and delayed entry.</li>
      <li>Promote only candidates that remain stable across regimes and horizons.</li>
    </ul>
  </section>
</main>
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pull BNB data and generate anomaly heatmaps.")
    parser.add_argument("--market", choices=["spot", "usd_m_futures"], default="spot")
    parser.add_argument("--symbols", nargs="+", default=["BNBUSDT", "BTCUSDT", "ETHUSDT"])
    parser.add_argument("--target-symbol", default="BNBUSDT")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--start", default="2024-01-01")
    parser.add_argument("--end", default=dt.datetime.now(UTC).date().isoformat())
    parser.add_argument("--output-dir", default="research/bnb-alpha")
    parser.add_argument("--skip-download", action="store_true", help="Analyze existing clean CSVs under output-dir.")
    parser.add_argument("--make-example", action="store_true", help="Generate synthetic example data locally, then analyze it.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    market = args.market
    interval = args.interval
    symbols = [value.upper() for value in args.symbols]
    target_symbol = args.target_symbol.upper()
    if target_symbol not in symbols:
        symbols.insert(0, target_symbol)

    if args.make_example:
        generate_example_data(output_dir, market, interval)
    elif not args.skip_download:
        start_ms = parse_date(args.start)
        end_ms = parse_date(args.end)
        for symbol in symbols:
            raw = fetch_klines(market, symbol, interval, start_ms, end_ms)
            raw_path = output_dir / "raw" / market / symbol / f"{interval}.csv"
            clean_path = output_dir / "clean" / market / symbol / f"{interval}.csv"
            write_raw(raw_path, raw)
            write_clean(clean_path, clean_rows(raw, symbol=symbol, market=market, interval=interval))
            print(f"{symbol}: raw={raw_path} clean={clean_path} rows={len(raw)}")

    frames = {}
    quality = []
    for symbol in symbols:
        clean_path = output_dir / "clean" / market / symbol / f"{interval}.csv"
        frame = load_clean(clean_path)
        if frame.empty:
            raise SystemExit(f"No clean rows loaded for {symbol}: {clean_path}")
        frames[symbol] = frame
        quality.append(
            {
                "symbol": symbol,
                "rows": len(frame),
                "start": frame["timestamp"].min().isoformat(),
                "end": frame["timestamp"].max().isoformat(),
                "source": frame["source"].iloc[0] if "source" in frame else "unknown",
            }
        )

    features = build_features(frames, target_symbol)
    events = run_event_studies(features)
    edge_heatmap = pivot_heatmap(events, "edge_bps")
    hit_heatmap = pivot_heatmap(events, "hit_delta")
    regimes = regime_event_heatmap(features)
    regime_pivot = (
        regimes.assign(regime_event=regimes["regime_col"] + ":" + regimes["regime"])
        .pivot_table(index="event", columns="regime_event", values="edge_bps", aggfunc="mean")
        .reset_index()
    )
    calendar = calendar_heatmap(features)
    candidates = candidate_specs(events, target_symbol, market, interval, synthetic_mode=args.make_example)

    analysis_dir = output_dir / "analysis"
    reports_dir = output_dir / "reports"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    features.to_csv(analysis_dir / f"features_{target_symbol}.csv", index=False)
    events.to_csv(analysis_dir / "event_studies.csv", index=False)
    edge_heatmap.to_csv(analysis_dir / "heatmap_edge_bps.csv", index=False)
    hit_heatmap.to_csv(analysis_dir / "heatmap_hit_delta.csv", index=False)
    regime_pivot.to_csv(analysis_dir / "heatmap_regime_edge_bps.csv", index=False)
    calendar.to_csv(analysis_dir / "calendar_heatmap_fwd_24h_bps.csv", index=False)
    (analysis_dir / "strategy_candidates.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    latest = features.dropna(subset=["close"]).tail(1).to_dict(orient="records")[0]
    (analysis_dir / "anomaly_latest_snapshot.json").write_text(json.dumps(latest, indent=2, default=str), encoding="utf-8")
    report_path = reports_dir / "bnb_alpha_report.html"
    write_report(
        report_path,
        target_symbol=target_symbol,
        data_quality=quality,
        events=events,
        edge_heatmap=edge_heatmap,
        hit_heatmap=hit_heatmap,
        regime_heatmap=regime_pivot,
        calendar=calendar,
        candidates=candidates,
    )
    print(f"report={report_path}")
    print(f"candidates={analysis_dir / 'strategy_candidates.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
