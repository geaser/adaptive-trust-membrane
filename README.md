# Adaptive Trust Membrane

Adaptive Trust Membrane is a Python prototype for trust calibration and context complexity analysis. It provides a membrane-style interface for evaluating contextual trust dynamics, simulating trust evolution, and exposing meta-cognitive hooks for runtime introspection.

## Phase 1 Goals

- Define a modular local architecture for:
  - Trust Calibration Engine
  - Context Complexity Classifier
  - Membrane Interface APIs
- Establish an initial protocol specification
- Add predictive modeling primitives for trust trajectory simulation
- Add meta-cognitive analysis hooks for observability and evaluation
- Provide unit-testable Python modules with robust logging and error handling

## Project Structure

- `src/adaptive_trust_membrane/trust_calibration/engine.py`
  Trust score calculation logic.
- `src/adaptive_trust_membrane/context_complexity/classifier.py`
  Context complexity scoring and classification.
- `src/adaptive_trust_membrane/membrane_interface/api.py`
  Public API surface for the membrane interface.
- `src/adaptive_trust_membrane/predictive/trajectory.py`
  Predictive trust evolution simulation.
- `src/adaptive_trust_membrane/metacognition/hooks.py`
  Meta-cognitive instrumentation hooks.
- `membrane_interface/spec.md`
  API and protocol specification.
- `tests/`
  Initial unit test coverage.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Quick Usage

```python
from adaptive_trust_membrane.membrane_interface.api import (
    calibrate_trust,
    classify_context_complexity,
    simulate_trust_trajectory,
)

context = {
    "source_reliability": 0.82,
    "evidence_quality": 0.74,
    "novelty": 0.35,
    "ambiguity": 0.20,
    "stakes": 0.65,
    "dependencies": ["sensor_a", "sensor_b"],
    "history": {"consistency": 0.88},
}

trust_score = calibrate_trust(context)
complexity_level = classify_context_complexity(context)
trajectory = simulate_trust_trajectory(context, steps=5)

print(trust_score)
print(complexity_level)
print(trajectory)
```

## Design Notes

- Trust scores are normalized to `[0.0, 1.0]`.
- Complexity levels are ordinal:
  - `1` = low
  - `2` = medium
  - `3` = high
- The system is defensive against malformed input and missing values.
- Logging is structured for later integration with observability platforms.

## Security Notes

- Any GitHub PAT used for repo operations should be constrained to the minimum required `repo` scope.
- The prototype does not persist secrets or trust state.
- Runtime hooks are read-only observers and should remain side-effect free by default.

## Status

This is a Phase 1 design/prototyping scaffold, not a production deployment.