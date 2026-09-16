from models.evaluation import BuildSignal, EvaluationResult

_MIN_AVG: dict[BuildSignal, float] = {
    BuildSignal.STRONG_YES: 4.0,
    BuildSignal.CAUTIOUS_YES: 3.0,
    BuildSignal.EXPLORE_MORE: 2.0,
    BuildSignal.NOT_RECOMMENDED: 0.0,
}

_MIN_USEFULNESS: dict[BuildSignal, int] = {
    BuildSignal.STRONG_YES: 4,
    BuildSignal.CAUTIOUS_YES: 3,
    BuildSignal.EXPLORE_MORE: 2,
    BuildSignal.NOT_RECOMMENDED: 0,
}

# Upper bounds — catches signals that are too pessimistic relative to scores
_MAX_AVG: dict[BuildSignal, float] = {
    BuildSignal.STRONG_YES: float("inf"),
    BuildSignal.CAUTIOUS_YES: float("inf"),
    BuildSignal.EXPLORE_MORE: float("inf"),
    BuildSignal.NOT_RECOMMENDED: 2.5,
}


def validate_signal(result: EvaluationResult) -> EvaluationResult:
    """
    Sanity-check the build_signal against dimension scores.
    Does NOT override the LLM decision — flags inconsistencies only.
    """
    scored = [d for d in result.dimensions if d.score > 0]
    if not scored:
        return result

    avg = sum(d.score for d in scored) / len(scored)
    usefulness = next(
        (d.score for d in result.dimensions if "Usefulness" in d.name), 0
    )

    min_avg = _MIN_AVG[result.build_signal]
    min_use = _MIN_USEFULNESS[result.build_signal]
    max_avg = _MAX_AVG[result.build_signal]

    if avg < min_avg or usefulness < min_use or avg > max_avg:
        print(
            f"[WARN] Signal '{result.build_signal.value}' may be inconsistent — "
            f"avg score: {avg:.1f}, usefulness: {usefulness}"
        )

    return result
