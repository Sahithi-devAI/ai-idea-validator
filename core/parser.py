import re
from typing import Optional

from models.evaluation import BuildSignal, DimensionScore, EvaluationResult

DIMENSION_NAMES = [
    "Market Potential",
    "Product Usefulness",
    "Feasibility & Defensibility",
    "Monetization Viability",
]

_SIGNAL_MAP: dict[str, BuildSignal] = {
    "strong_yes": BuildSignal.STRONG_YES,
    "cautious_yes": BuildSignal.CAUTIOUS_YES,
    "explore_more": BuildSignal.EXPLORE_MORE,
    "not_recommended": BuildSignal.NOT_RECOMMENDED,
}


def _extract_section(text: str, header: str) -> Optional[str]:
    """Pull content between a section header and the next ## header."""
    escaped = re.escape(header)
    # Use string concat to avoid f-string interpreting {1,3} as an expression
    pattern = r"#{1,3}\s*" + escaped + r"[^\n]*\n(.*?)(?=\n#{1,3}\s|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def _extract_score(text: str) -> Optional[int]:
    """Find the first score in patterns like Score: 3/5, 3/5, [3/5]."""
    patterns = [
        r"[Ss]core[:\s]+(\d)\s*/?\s*5",
        r"\[(\d)/5\]",
        r"\b(\d)/5\b",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 5:
                return val
    return None


def _extract_list_items(text: str) -> list[str]:
    """Extract bullet/numbered list items from a block of text."""
    items = []
    for line in text.splitlines():
        line = line.strip()
        cleaned = re.sub(r"^[-*•]|\d+\.\s*", "", line).strip()
        if cleaned and re.match(r"^[-*•]|\d+\.", line):
            items.append(cleaned)
    return items


def _extract_build_signal(text: str) -> Optional[BuildSignal]:
    """Find the first valid build signal token in the text."""
    for token, signal in _SIGNAL_MAP.items():
        if re.search(rf"\b{re.escape(token)}\b", text, re.IGNORECASE):
            return signal
    return None


def parse_output(raw: str, idea: str) -> EvaluationResult:
    dimensions: list[DimensionScore] = []
    for name in DIMENSION_NAMES:
        section = _extract_section(raw, name)
        if section:
            score = _extract_score(section)
            # Remove score line including any surrounding markdown bold markers
            justification = re.sub(r"\*{0,2}[Ss]core[:\s]+\d\s*/?\s*5\*{0,2}", "", section)
            # Remove any leftover lines that are only asterisks/whitespace
            justification = re.sub(r"^\s*\*+\s*$", "", justification, flags=re.MULTILINE)
            justification = justification.strip()
        else:
            score = None
            justification = ""
        dimensions.append(
            DimensionScore(name=name, score=score or 0, justification=justification)
        )

    strengths = _extract_list_items(_extract_section(raw, "Strengths") or "")
    weaknesses = _extract_list_items(_extract_section(raw, "Weaknesses") or "")

    risks_raw = _extract_section(raw, "Top Risks") or _extract_section(raw, "Risks") or ""
    risks = _extract_list_items(risks_raw)

    steps_raw = (
        _extract_section(raw, "Practical Next Steps")
        or _extract_section(raw, "Next Steps")
        or ""
    )
    next_steps = _extract_list_items(steps_raw)

    signal_section = _extract_section(raw, "Build Signal") or ""
    build_signal = _extract_build_signal(signal_section) or _extract_build_signal(raw) or BuildSignal.EXPLORE_MORE

    weakest_raw = _extract_section(raw, "Weakest Dimension") or ""
    weakest_dimension = weakest_raw.splitlines()[0].strip() if weakest_raw else ""

    verdict_raw = _extract_section(raw, "Verdict") or ""
    verdict = verdict_raw.splitlines()[0].strip() if verdict_raw else ""

    return EvaluationResult(
        idea=idea,
        dimensions=dimensions,
        strengths=strengths,
        weaknesses=weaknesses,
        risks=risks,
        next_steps=next_steps,
        build_signal=build_signal,
        weakest_dimension=weakest_dimension,
        verdict=verdict,
        raw_output=raw,
    )
