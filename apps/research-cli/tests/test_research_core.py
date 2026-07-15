from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
for source_root in (
    REPO_ROOT / "packages/python/quant-core/src",
    REPO_ROOT / "packages/python/quant-research/src",
    REPO_ROOT / "packages/python/quant-ml/src",
):
    sys.path.insert(0, str(source_root))

from quant_core.economics.costs import CostModel
from quant_core.economics.trades import concentration, trade_metrics
from quant_core.indicators.candle import candle_geometry
from quant_core.indicators.momentum import path_efficiency, trailing_log_return
from quant_core.indicators.range_location import range_position
from quant_core.indicators.registry import INDICATORS, indicator_names
from quant_core.indicators.volatility import realized_volatility
from quant_core.indicators.volume import relative_volume
from quant_core.math.returns import forward_log_returns, log_return, simple_return, to_basis_points
from quant_core.math.rolling import rolling_mean
from quant_core.math.statistics import block_bootstrap_mean
from quant_core.validation.clocks import InformationClock, validate_information_clock
from quant_ml.dataset import WindowSpec, build_supervised_windows
from quant_research.core.paths import resolve_cycle_path
from quant_research.routines.feature_pipeline import build_feature_row
from quant_research.routines.stages import ResearchStage, may_transition


class ReturnMathTests(unittest.TestCase):
    def test_return_math(self) -> None:
        self.assertAlmostEqual(simple_return(100, 101), 0.01)
        self.assertAlmostEqual(log_return(100, 101), math.log(1.01))
        self.assertAlmostEqual(to_basis_points(0.01), 100)
        self.assertEqual(forward_log_returns([100, 101, 102], 1)[-1], None)

    def test_rolling_alignment(self) -> None:
        self.assertEqual(rolling_mean([1, 2, 3], 2), [None, 1.5, 2.5])
        self.assertEqual(rolling_mean([1, 2, 3], 2, include_current=False), [None, None, 1.5])

    def test_block_bootstrap_is_reproducible(self) -> None:
        first = block_bootstrap_mean([1, 2, 3, 4], 2, 200, 17)
        second = block_bootstrap_mean([1, 2, 3, 4], 2, 200, 17)
        self.assertEqual(first, second)


class IndicatorTests(unittest.TestCase):
    def test_candle_geometry(self) -> None:
        geometry = candle_geometry(100, 104, 98, 103, previous_close=99)
        total = geometry.absolute_body_fraction + geometry.upper_wick_fraction + geometry.lower_wick_fraction
        self.assertAlmostEqual(total, 1.0)
        self.assertAlmostEqual(geometry.close_location, 5 / 6)

    def test_interpretable_indicators(self) -> None:
        closes = [100, 101, 102, 101, 103]
        self.assertGreater(trailing_log_return(closes, 2), 0)
        self.assertGreaterEqual(path_efficiency(closes, 4), 0)
        self.assertLessEqual(path_efficiency(closes, 4), 1)
        self.assertGreater(realized_volatility(closes, 4), 0)
        self.assertAlmostEqual(relative_volume([10, 10, 20], 2), 2.0, places=10)
        self.assertAlmostEqual(range_position([102, 103], [98, 99], 102, 2), 0.8)

    def test_feature_pipeline(self) -> None:
        bars = [
            {"open": 100 + i, "high": 102 + i, "low": 99 + i, "close": 101 + i, "volume": 10 + i}
            for i in range(5)
        ]
        features = build_feature_row(bars, [2, 4])
        self.assertIn("signed_body_fraction", features)
        self.assertIn("trailing_log_return_4", features)
        self.assertIn("realized_volatility_2", features)
        self.assertNotIn("future_return", features)

    def test_indicator_registry_has_unique_causal_entries(self) -> None:
        names = indicator_names()
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(item.last_observable == "bar_t_close" for item in INDICATORS))


class EconomicsAndIntegrityTests(unittest.TestCase):
    def test_cost_model_and_metrics(self) -> None:
        model = CostModel(1.0, 0.5, 0.5, impact_bps_per_trade=0.2, safety_margin_bps=0.5)
        self.assertAlmostEqual(model.round_trip_bps, 3.7)
        self.assertAlmostEqual(model.net_return_bps(5.0), 1.3)
        metrics = trade_metrics([2.0, -1.0, 3.0])
        self.assertEqual(metrics["count"], 3)
        self.assertGreater(metrics["profit_factor"], 1)
        self.assertGreater(concentration([2.0, -1.0, 3.0])["top_5_absolute_share"], 0.99)

    def test_information_clock(self) -> None:
        valid = InformationClock(10, 10, 10, 11, 15)
        self.assertEqual(validate_information_clock(valid), [])
        leaking = InformationClock(12, 10, 10, 11, 15)
        self.assertIn("feature uses information after the decision bar", validate_information_clock(leaking))

    def test_stage_machine_prevents_skips(self) -> None:
        self.assertTrue(may_transition(ResearchStage.DATA_AUDIT, ResearchStage.STRUCTURAL_PROFILING))
        self.assertFalse(may_transition(ResearchStage.DATA_AUDIT, ResearchStage.BROAD_SEARCH))

    def test_cycle_path_cannot_escape(self) -> None:
        with self.assertRaises(ValueError):
            resolve_cycle_path("/tmp/cycle", "../outside")

    def test_ml_windows_preserve_target_alignment(self) -> None:
        self.assertNotIn("torch", sys.modules)
        windows, labels, indices = build_supervised_windows(
            [[1.0], [2.0], [3.0], [4.0]],
            [10.0, 20.0, 30.0, 40.0],
            WindowSpec(lookback_rows=2, forecast_gap_rows=1),
        )
        self.assertEqual(windows, [[[1.0], [2.0]], [[2.0], [3.0]]])
        self.assertEqual(labels, [30.0, 40.0])
        self.assertEqual(indices, [2, 3])


if __name__ == "__main__":
    unittest.main()
