from concurrent.futures import ThreadPoolExecutor

from adaptive_trust_membrane.membrane_interface.api import calibrate_trust


CONTEXT = {
    "risk_level": 0.35,
    "uncertainty": 0.25,
    "evidence_count": 12,
    "source_quality": 0.8,
    "ambiguity_markers": 1,
    "nested_dependencies": 2,
    "historical_reliability": 0.9,
    "novelty": 0.4,
    "stakes": 0.6,
    "feedback_signal": 0.1,
}


def task(_: int) -> float:
    return calibrate_trust(CONTEXT)


def main() -> None:
    runs = 1000
    workers = 16
    with ThreadPoolExecutor(max_workers=workers) as executor:
        scores = list(executor.map(task, range(runs)))
    print(
        {
            "runs": runs,
            "workers": workers,
            "min_score": min(scores),
            "max_score": max(scores),
            "avg_score": sum(scores) / len(scores),
        }
    )


if __name__ == "__main__":
    main()