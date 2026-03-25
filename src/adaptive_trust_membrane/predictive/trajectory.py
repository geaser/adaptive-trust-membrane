"""Predictive modeling for trust trajectory evolution."""

from __future__ import annotations

from typing import Any

from adaptive_trust_membrane.models import MembraneInputError, clamp
from adaptive_trust_membrane.trust_calibration.engine import TrustCalibrationEngine


def simulate_trust_trajectory(context: dict[str, Any], steps: int = 3) -> list[float]:
    if not isinstance(context, dict):
        raise MembraneInputError("Context must be a dictionary.")
    if steps < 1:
        raise MembraneInputError("Steps must be >= 1.")

    engine = TrustCalibrationEngine()
    working_context = dict(context)
    trajectory: list[float] = []

    for _ in range(steps):
        result = engine.calibrate(working_context)
        trajectory.append(result.score)

        current_history = working_context.get("history", {})
        if not isinstance(current_history, dict):
            current_history = {}

        consistency = clamp(float(current_history.get("consistency", 0.5)) + 0.03)
        ambiguity = clamp(float(working_context.get("ambiguity", 0.0)) * 0.95)

        working_context["history"] = {**current_history, "consistency": consistency}
        working_context["ambiguity"] = ambiguity

    return trajectory