"""Context complexity classifier."""

from __future__ import annotations

from typing import Any

from adaptive_trust_membrane.logging_config import get_logger
from adaptive_trust_membrane.models import ComplexityResult, MembraneInputError, _coerce_float, clamp

logger = get_logger(__name__)


class ContextComplexityClassifier:
    """Classifies context into low, medium, or high complexity."""

    def classify(self, context: dict[str, Any]) -> ComplexityResult:
        if not isinstance(context, dict):
            raise MembraneInputError("Context must be a dictionary.")

        ambiguity = clamp(_coerce_float(context.get("ambiguity"), 0.0))
        novelty = clamp(_coerce_float(context.get("novelty"), 0.0))
        stakes = clamp(_coerce_float(context.get("stakes"), 0.0))
        dependency_count = len(context.get("dependencies", [])) if isinstance(context.get("dependencies", []), list) else 0
        signal_count = len(context)

        dependency_factor = min(dependency_count / 10.0, 1.0)
        signal_factor = min(signal_count / 20.0, 1.0)

        score = clamp(
            0.35 * ambiguity
            + 0.25 * novelty
            + 0.20 * stakes
            + 0.10 * dependency_factor
            + 0.10 * signal_factor
        )

        if score < 0.34:
            level = 1
        elif score < 0.67:
            level = 2
        else:
            level = 3

        logger.info(
            "Context classified",
            extra={
                "complexity_score": score,
                "complexity_level": level,
            },
        )
        return ComplexityResult(score=score, level=level)