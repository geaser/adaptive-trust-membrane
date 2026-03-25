"""Public membrane interface API."""

from __future__ import annotations

from typing import Any

from adaptive_trust_membrane.context_complexity.classifier import ContextComplexityClassifier
from adaptive_trust_membrane.predictive.trajectory import simulate_trust_trajectory as _simulate
from adaptive_trust_membrane.trust_calibration.engine import TrustCalibrationEngine

_engine = TrustCalibrationEngine()
_classifier = ContextComplexityClassifier()


def calibrate_trust(context: dict[str, Any]) -> float:
    """Return a normalized trust score in the range [0.0, 1.0]."""
    return _engine.calibrate(context).score


def classify_context_complexity(context: dict[str, Any]) -> int:
    """Return complexity level: 1=low, 2=medium, 3=high."""
    return _classifier.classify(context).level


def simulate_trust_trajectory(context: dict[str, Any], steps: int = 3) -> list[float]:
    """Simulate trust evolution across multiple future steps."""
    return _simulate(context, steps=steps)