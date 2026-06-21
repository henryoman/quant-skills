import type { StrategyInput, StrategySpec } from "./types";

export function generateStrategy(input: StrategyInput): StrategySpec {
  // Starter shell only.
  // Replace these fixed values with real indicator/regime calculations.

  const strategy = selectStarterStrategy(input);

  return {
    symbol: input.symbol.toUpperCase(),
    cmc_id: input.symbol.toUpperCase() === "BNB" ? 1839 : undefined,
    timeframe: input.timeframe,
    horizon: input.horizon,
    selected_strategy: strategy,
    market_regime: {
      trend: "up",
      volatility: "expanding",
      volume: "expanding",
    },
    entry_rules: [
      "close > rolling_high_20",
      "volume_zscore_20 > 1.25",
      "atr_pct > median_atr_pct_60",
    ],
    exit_rules: [
      "close < ema_20",
      "return_since_entry <= -0.025",
      "return_since_entry >= 0.05",
      "bars_held >= 24",
    ],
    risk_rules: {
      max_position_size_pct: input.risk === "high" ? 15 : input.risk === "low" ? 5 : 10,
      stop_loss_pct: 2.5,
      take_profit_pct: 5.0,
    },
    backtest_config: {
      fee_bps: 10,
      slippage_bps: 5,
      historical_data_source: input.mode === "live-cmc" ? "cmc_or_configured_source" : "binance_public_klines",
      walk_forward: true,
    },
    data_provenance: {
      live_context_source: input.mode === "fixture" ? "fixture" : "coinmarketcap",
      historical_ohlcv_source: input.mode === "fixture" ? "fixture" : "binance_public_klines",
      fixture_mode: input.mode === "fixture",
      synthetic_mode: input.mode === "synthetic",
    },
  };
}

function selectStarterStrategy(input: StrategyInput): string {
  if (input.horizon === "1h") return "binary_probability";
  if (input.risk === "low") return "expected_range";
  return "volatility_breakout";
}

if (import.meta.main) {
  const spec = generateStrategy({
    symbol: "BNB",
    timeframe: "1h",
    horizon: "24h",
    risk: "medium",
    mode: "fixture",
  });

  console.log(JSON.stringify(spec, null, 2));
}
