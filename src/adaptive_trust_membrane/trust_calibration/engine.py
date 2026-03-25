"""Trust calibration engine."""

from __future__ import annotations

from typing import Any

from adaptive_trust_membrane.logging_config import get_logger
from adaptive_trust_membrane.models import MembraneInputError, TrustResult, _coerce_float, clamp
from adaptive_trust_membrane.context_complexity.classifier import ContextComplexityClassifier

logger = get_logger(__name__)


class TrustCalibrationEngine:
    """Calculates trust scores from contextual features."""

    def __init__(self) -> None:
        self._classifier = ContextComplexityClassifier()

    def calibrate(self, context: dict[str, Any]) -> TrustResult:
        if not isinstance(context, dict):
            raise MembraneInputError("Context must be a dictionary.")

        source_reliability = clamp(_coerce_float(context.get("source_reliability"), 0.5))
        evidence_quality = clamp(_coerce_float(context.get("evidence_quality"), 0.5))
        novelty = clamp(_coerce_float(context.get("novelty"), 0.0))
        ambiguity = clamp(_coerce_float(context.get("ambiguity"), 0.0))
        stakes = clamp(_coerce_float(context.get("stakes"), 0.5))
        consistency = clamp(
            _coerce_float(context.get("history", {}).get("consistency") if isinstance(context.get("history"), dict) else 0.5, 0.5)
        )

        complexity = self._classifier.classify(context)

        base = (
            0.30 * source_reliability
            + 0.25 * evidence_quality
            + 0.20 * consistency
            + 0.10 * (1.0 - novelty)
            + 0.15 * (1.0 - ambiguity)
        )

        complexity_penalty = {1: 0.00, 2: 0.05, 3: 0.12}[complexity.level]
        stakes_penalty = 0.08 * stakes if complexity.level == 3 else 0.04 * stakes
        trust_score = clamp(base - complexity_penalty - stakes_penalty)

        logger.info(
            "Trust calibrated",
            extra={
                "trust_score": trust_score,
                "complexity_level": complexity.level,
            },
        )
        return TrustResult(score=trust_score, complexity_level=complexity.level)