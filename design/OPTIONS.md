# Design options

Use `build-profit-reports` as the strict default for quantitative, alpha, strategy, and trading reports. The other options remain available for different communication jobs.

| Option | Use it for | Density | Key behavior |
|---|---|---:|---|
| `build-profit-reports/` | Profit-oriented quant research and strategy decisions | Very high | Enforces causal evidence, costs, unseen-time validation, failure graphics, and one promotion decision |
| `report-design.md` | Canonical mixed-audience research reports | Medium–high | Unified LIQ and ML system with explicit profiles |
| `report-design-graph-guided.md` | Complex charts that readers may misinterpret | Medium–high | Requires how-to-read, observation, relevance, and limitation blocks |
| `report-design-mellow.md` | Short notes, negative results, and low-visual reports | Low | Calm, minimal, and intentionally restrained |
| `report-design-liq.md` | General editorial and technical reports | Medium | Structured reading surface, caption rails, accessibility, portable HTML |
| `report-design-ml.md` | Dense quantitative evidence reports | High | Full-width single-column charts, heatmaps, exact context, inspection tools |
| `report-design-dlmm.md` | DLMM, execution, and strategy-specific reports | High | Domain companion for liquidity and trading mechanics |
| `frontend-design/` | Product interfaces and non-report UI | Varies | Distinctive visual direction, typography, layout, and interaction |

Selection order:

1. Quantitative profit decision: `build-profit-reports/`.
2. General research artifact: `report-design.md`.
3. Reader needs explicit chart guidance: add `report-design-graph-guided.md`.
4. DLMM or execution domain: add `report-design-dlmm.md`.
5. Short or negative result with little evidence: use `report-design-mellow.md`.
6. Product UI rather than a report: use `frontend-design/`.

Visual polish never upgrades weak research evidence. The active quantitative research framework and frozen experiment contract remain authoritative.
