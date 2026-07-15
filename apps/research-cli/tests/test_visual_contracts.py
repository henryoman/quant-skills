from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages/python/quant-visuals/src"))

from quant_visuals.frontend.profiles import ReportProfile
from quant_visuals.frontend.report_contract import EvidenceBlock, ReportDocument
from quant_visuals.plotting.diagnostics import conditional_profile_spec, support_heatmap_spec


class VisualContractTests(unittest.TestCase):
    def test_heatmap_requires_support_and_is_valid(self) -> None:
        spec = support_heatmap_spec(
            x_feature="past return",
            y_feature="relative volume",
            outcome="future return",
            unit="bps",
            scope="BTCUSDT, 1m, locked test, n=100,000",
        )
        self.assertEqual(spec.validate(), [])
        self.assertEqual(spec.support_field, "sample_count")
        artifact = spec.as_contract()
        self.assertEqual(artifact["supportField"], "sample_count")
        schema = json.loads(
            (REPO_ROOT / "packages/schemas/json/plot-spec.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(schema["required"]) - set(artifact), set())

    def test_graph_guided_requires_explanatory_claims(self) -> None:
        spec = conditional_profile_spec(
            feature="relative volume",
            target="future return",
            unit="bps",
            scope="BTCUSDT, 1m, test",
        )
        block = EvidenceBlock("volume-profile", "Conditional profile", spec, limitations=("Costs excluded",))
        report = ReportDocument(
            report_id="test-report",
            title="Test",
            decision="Inconclusive",
            classification="inconclusive",
            scope="BTCUSDT",
            profile=ReportProfile.GRAPH_GUIDED,
            evidence=(block,),
            rejected_ideas=("Naive continuation",),
        )
        errors = report.validate()
        self.assertTrue(any("what_it_shows" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
