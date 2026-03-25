"""Meta-cognitive analysis hooks for membrane evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetaCognitiveObserver:
    """Collects runtime observations for evaluation and debugging."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append(
            {
                "event_type": event_type,
                "payload": payload,
            }
        )

    def summarize(self) -> dict[str, Any]:
        return {
            "event_count": len(self.events),
            "event_types": sorted({event["event_type"] for event in self.events}),
        }