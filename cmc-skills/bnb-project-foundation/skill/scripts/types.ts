export type Mode = "live-cmc" | "hybrid-free" | "fixture" | "synthetic";
export type Timeframe = "5m" | "15m" | "1h" | "4h" | "1d";
export type Horizon = "1h" | "4h" | "24h" | "7d";

export type StrategyInput = {
  symbol: string;
  timeframe: Timeframe;
  horizon: Horizon;
  risk: "low" | "medium" | "high";
  mode: Mode;
};

export type StrategySpec = {
  symbol: string;
  cmc_id?: number;
  timeframe: Timeframe;
  horizon: Horizon;
  selected_strategy: string;
  market_regime: {
    trend: "up" | "down" | "flat";
    volatility: "expanding" | "contracting" | "stable";
    volume: "expanding" | "contracting" | "normal";
  };
  entry_rules: string[];
  exit_rules: string[];
  risk_rules: Record<string, number | string>;
  backtest_config: Record<string, number | string | boolean>;
  data_provenance: {
    live_context_source: string;
    historical_ohlcv_source: string;
    fixture_mode: boolean;
    synthetic_mode: boolean;
  };
};
