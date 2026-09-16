import pytest

from core.parser import _extract_build_signal, _extract_score, parse_output
from models.evaluation import BuildSignal

SAMPLE_OUTPUT = """
## Market Potential
Score: 3/5
Limited addressable market due to niche focus. Enterprise segment exists but crowded.

## Product Usefulness
Score: 4/5
Clear pain point for founders. Saves 2–3 hours of research per idea.

## Feasibility & Defensibility
Score: 3/5
Technically simple. Low moat unless network effects are built.

## Monetization Viability
Score: 2/5
Unclear willingness to pay. Similar tools are free or freemium.

## Strengths
- Clear user pain point
- Fast time to value
- Low technical complexity

## Weaknesses
- Low defensibility
- Saturated market
- No data moat

## Top Risks
- Competitors copy quickly
- LLM quality dependency
- User trust in AI evaluations

## Practical Next Steps
- Run 20 user interviews
- Define pricing experiment
- Build waitlist

## Build Signal
cautious_yes

## Weakest Dimension
Monetization Viability

## Verdict
Useful tool for a real pain point, but needs a defensible wedge before scaling.
"""


def test_parse_dimension_count():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert len(result.dimensions) == 4


def test_parse_scores():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    scores = {d.name: d.score for d in result.dimensions}
    assert scores["Market Potential"] == 3
    assert scores["Product Usefulness"] == 4
    assert scores["Feasibility & Defensibility"] == 3
    assert scores["Monetization Viability"] == 2


def test_parse_build_signal():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert result.build_signal == BuildSignal.CAUTIOUS_YES


def test_parse_strengths():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert len(result.strengths) == 3


def test_parse_weaknesses():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert len(result.weaknesses) == 3


def test_parse_risks():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert len(result.risks) == 3


def test_parse_next_steps():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert len(result.next_steps) == 3


def test_parse_weakest_dimension():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert result.weakest_dimension == "Monetization Viability"


def test_parse_verdict():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert "defensible wedge" in result.verdict


def test_raw_output_preserved():
    result = parse_output(SAMPLE_OUTPUT, "test idea")
    assert result.raw_output == SAMPLE_OUTPUT


# --- Unit tests for helper functions ---

@pytest.mark.parametrize("text,expected", [
    ("Score: 3/5", 3),
    ("score: 4/5", 4),
    ("[3/5]", 3),
    ("2/5", 2),
    ("Score: 5 / 5", 5),
    ("no score here", None),
    ("Score: 6/5", None),  # out of range
])
def test_extract_score_variants(text, expected):
    assert _extract_score(text) == expected


@pytest.mark.parametrize("text,expected", [
    ("strong_yes", BuildSignal.STRONG_YES),
    ("Build Signal: not_recommended", BuildSignal.NOT_RECOMMENDED),
    ("The result is cautious_yes based on analysis", BuildSignal.CAUTIOUS_YES),
    ("explore_more", BuildSignal.EXPLORE_MORE),
    ("no signal here", None),
])
def test_extract_build_signal_variants(text, expected):
    assert _extract_build_signal(text) == expected


def test_missing_sections_do_not_crash():
    result = parse_output("Some completely unstructured output.", "test")
    assert result.build_signal == BuildSignal.EXPLORE_MORE  # default
    assert result.dimensions  # still 4 entries
    assert all(d.score == 0 for d in result.dimensions)
