import pytest

from core.signal_validator import validate_signal
from models.evaluation import BuildSignal, DimensionScore, EvaluationResult


def _make_result(scores: list[int], signal: BuildSignal) -> EvaluationResult:
    names = [
        "Market Potential",
        "Product Usefulness",
        "Feasibility & Defensibility",
        "Monetization Viability",
    ]
    dims = [DimensionScore(name=n, score=s, justification="") for n, s in zip(names, scores)]
    return EvaluationResult(
        idea="test",
        dimensions=dims,
        strengths=[],
        weaknesses=[],
        risks=[],
        next_steps=[],
        build_signal=signal,
        weakest_dimension="",
        verdict="",
        raw_output="",
    )


def test_consistent_signal_no_warning(capsys):
    result = _make_result([5, 5, 4, 4], BuildSignal.STRONG_YES)
    validate_signal(result)
    assert "WARN" not in capsys.readouterr().out


def test_optimistic_signal_warns(capsys):
    result = _make_result([2, 2, 2, 2], BuildSignal.STRONG_YES)
    validate_signal(result)
    assert "WARN" in capsys.readouterr().out


def test_pessimistic_signal_warns(capsys):
    result = _make_result([5, 5, 5, 5], BuildSignal.NOT_RECOMMENDED)
    validate_signal(result)
    assert "WARN" in capsys.readouterr().out


def test_signal_is_never_overridden():
    result = _make_result([1, 1, 1, 1], BuildSignal.STRONG_YES)
    validated = validate_signal(result)
    assert validated.build_signal == BuildSignal.STRONG_YES


def test_zero_scores_skip_validation(capsys):
    result = _make_result([0, 0, 0, 0], BuildSignal.EXPLORE_MORE)
    validate_signal(result)
    assert "WARN" not in capsys.readouterr().out
