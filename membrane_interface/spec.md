# Membrane Interface Specification

## Purpose

The `membrane_interface` defines a stable protocol for trust calibration and context complexity classification. The interface is designed to be small, auditable, and easy to embed in larger reasoning or orchestration systems.

## Public Functions

### `calibrate_trust(context: dict) -> float`

Returns a normalized trust score in the inclusive range `[0.0, 1.0]`.

#### Expected Input Schema

```python
{
    "risk_level": float,              # 0.0 to 1.0, default 0.5
    "uncertainty": float,             # 0.0 to 1.0, default 0.5
    "evidence_count": int,            # >= 0, default 0
    "source_quality": float,          # 0.0 to 1.0, default 0.5
    "ambiguity_markers": int,         # >= 0, default 0
    "nested_dependencies": int,       # >= 0, default 0
    "historical_reliability": float,  # 0.0 to 1.0, default 0.5
    "novelty": float,                 # 0.0 to 1.0, default 0.5
    "stakes": float,                  # 0.0 to 1.0, default 0.5
    "feedback_signal": float,         # -1.0 to 1.0, default 0.0
}
```

#### Semantics

- Higher `source_quality`, `evidence_count`, and `historical_reliability` increase trust
- Higher `risk_level`, `uncertainty`, `ambiguity_markers`, and `stakes` reduce trust
- `feedback_signal` adjusts trust trajectory using recent performance feedback
- Complexity is incorporated as a damping factor

#### Error Cases

- non-dict `context`
- negative counts
- numeric fields outside accepted ranges
- non-numeric values for numeric fields

### `classify_context_complexity(context: dict) -> int`

Returns an integer complexity level:

- `1`: low
- `2`: medium
- `3`: high

#### Expected Input Schema

The classifier reads the same context schema as `calibrate_trust`, but only requires a subset of fields. Missing fields are defaulted conservatively.

#### Semantics

Complexity increases with:

- ambiguity
- dependency depth
- novelty
- stakes
- uncertainty
- amount of interacting evidence or constraints

## Extended Function

### `simulate_trust_evolution(context: dict, steps: int = 5) -> list[float]`

Returns a projected trust trajectory over `steps` time slices.

#### Semantics

- begins from the current calibrated trust
- applies gradual feedback, novelty decay, and uncertainty adjustment
- returns one score per step, all clamped to `[0.0, 1.0]`

## Meta-Cognitive Hooks

The engine may accept a hook implementing:

- `record_event(event_name: str, payload: dict) -> None`

Typical event names:

- `context_validated`
- `complexity_classified`
- `trust_calibrated`
- `trajectory_simulated`
- `error`

## Usage Examples

### Basic Trust Calibration

```python
score = calibrate_trust({
    "risk_level": 0.3,
    "uncertainty": 0.2,
    "evidence_count": 10,
    "source_quality": 0.9,
    "historical_reliability": 0.8,
})
```

### Complexity Classification

```python
level = classify_context_complexity({
    "uncertainty": 0.8,
    "ambiguity_markers": 4,
    "nested_dependencies": 3,
    "stakes": 0.9,
})
# returns 3
```

### Predictive Modeling

```python
trajectory = simulate_trust_evolution({
    "source_quality": 0.8,
    "uncertainty": 0.4,
    "feedback_signal": 0.2,
}, steps=4)
```

## Edge Cases

- Empty context: valid, defaults applied
- Extremely high evidence with high uncertainty: trust should not saturate to `1.0`
- High source quality with high stakes and high risk: trust should remain damped
- Negative evidence counts or invalid numeric types: reject with validation error
- `steps <= 0` in predictive simulation: reject with validation error

## Stability Notes

Phase 1 guarantees stable function names and return types, but not final weighting constants. Weighting strategy is intentionally provisional and may change in later phases without changing the public function signatures.