from enum import Enum
from typing import List
from pydantic import BaseModel


class BuildSignal(str, Enum):
    STRONG_YES = "strong_yes"
    CAUTIOUS_YES = "cautious_yes"
    EXPLORE_MORE = "explore_more"
    NOT_RECOMMENDED = "not_recommended"


class DimensionScore(BaseModel):
    name: str
    score: int  # 1–5, 0 if unparseable
    justification: str


class EvaluationResult(BaseModel):
    idea: str
    dimensions: List[DimensionScore]
    strengths: List[str]
    weaknesses: List[str]
    risks: List[str]
    next_steps: List[str]
    build_signal: BuildSignal
    weakest_dimension: str
    verdict: str
    raw_output: str  # always preserve the original LLM response
