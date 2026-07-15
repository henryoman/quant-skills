"""Research-stage state machine and artifact requirements."""

from __future__ import annotations

from enum import Enum


class ResearchStage(str, Enum):
    DATA_AUDIT = "data_audit"
    STRUCTURAL_PROFILING = "structural_profiling"
    BROAD_SEARCH = "broad_search"
    CANDIDATE_REFINEMENT = "candidate_refinement"
    ADVERSARIAL_VALIDATION = "adversarial_validation"
    LOCKED_EVALUATION = "locked_evaluation"
    PAPER_TRADING = "paper_trading"
    COMPLETE = "complete"


ORDER = tuple(ResearchStage)


REQUIRED_ARTIFACTS: dict[ResearchStage, tuple[str, ...]] = {
    ResearchStage.DATA_AUDIT: ("cycle.json", "DATA_CARD.md", "results/data-audit/DATA_AUDIT.json"),
    ResearchStage.STRUCTURAL_PROFILING: ("TARGET_MATRIX.csv", "results/structural-profile"),
    ResearchStage.BROAD_SEARCH: ("HYPOTHESIS_LEDGER.csv", "EXPERIMENT_LEDGER.csv", "BROAD_EXPERIMENT_MATRIX.csv"),
    ResearchStage.CANDIDATE_REFINEMENT: ("BROAD_EXPERIMENT_MATRIX.csv", "experiments"),
    ResearchStage.ADVERSARIAL_VALIDATION: ("EXPERIMENT_LEDGER.csv", "results"),
    ResearchStage.LOCKED_EVALUATION: ("FROZEN_PROCEDURE.json",),
    ResearchStage.PAPER_TRADING: ("DECISION.md",),
    ResearchStage.COMPLETE: ("DECISION.md",),
}


def may_transition(current: ResearchStage, proposed: ResearchStage) -> bool:
    """Allow staying put or advancing exactly one stage; never skip evidence levels."""
    current_index = ORDER.index(current)
    proposed_index = ORDER.index(proposed)
    return proposed_index in {current_index, current_index + 1}


def requirements_for(stage: ResearchStage) -> tuple[str, ...]:
    return REQUIRED_ARTIFACTS[stage]
