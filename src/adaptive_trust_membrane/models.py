"""Core shared models and validation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class MembraneInputError(ValueError):
    """Raised when the membrane interface receives invalid input."""


def _coerce_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        raise MembraneInputError("Boolean values are not valid numeric inputs.")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise MembraneInputError(f"Expected numeric value, got {value!r}") from exc


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


@dataclass(frozen=True)
class ComplexityResult:
    score: float
    level: int


@dataclass(frozen=True)
class TrustResult:
    score: float
    complexity_level: int