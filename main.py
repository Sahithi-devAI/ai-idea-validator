import os
import sys
import textwrap

from dotenv import load_dotenv

from core.input_handler import validate_idea
from core.llm_client import get_provider
from core.logger import log_evaluation
from core.parser import parse_output
from core.prompt_manager import build_messages
from core.signal_validator import validate_signal
from models.evaluation import EvaluationResult

load_dotenv()

SIGNAL_LABELS = {
    "strong_yes":       "STRONG YES      ✓",
    "cautious_yes":     "CAUTIOUS YES    ~",
    "explore_more":     "EXPLORE MORE    ?",
    "not_recommended":  "NOT RECOMMENDED ✗",
}


def run_evaluation(idea: str, provider: str = "anthropic", prompt_version: str = "v1_5") -> EvaluationResult:
    idea = validate_idea(idea)
    system, messages = build_messages(idea, prompt_version=prompt_version)
    llm = get_provider(provider)
    raw = llm.complete(system=system, messages=messages)
    result = parse_output(raw, idea)
    result = validate_signal(result)
    return result


def print_result(result: EvaluationResult) -> None:
    sep = "=" * 60
    print(f"\n{sep}")
    label = SIGNAL_LABELS.get(result.build_signal.value, result.build_signal.value)
    print(f"  BUILD SIGNAL: {label}")
    print(f"  VERDICT:      {result.verdict}")
    print(f"{sep}\n")

    print("DIMENSION SCORES")
    print("-" * 40)
    for dim in result.dimensions:
        score_display = f"{dim.score}/5" if dim.score else "n/a"
        print(f"  {dim.name:<32} {score_display}")
        if dim.justification:
            for line in textwrap.wrap(dim.justification, width=72):
                print(f"    {line}")
    print()

    if result.strengths:
        print("STRENGTHS")
        for s in result.strengths:
            print(f"  + {s}")
        print()

    if result.weaknesses:
        print("WEAKNESSES")
        for w in result.weaknesses:
            print(f"  - {w}")
        print()

    if result.risks:
        print("TOP RISKS")
        for r in result.risks:
            print(f"  ! {r}")
        print()

    if result.next_steps:
        print("NEXT STEPS")
        for n in result.next_steps:
            print(f"  -> {n}")
        print()

    if result.weakest_dimension:
        print(f"Weakest dimension: {result.weakest_dimension}")
    print()


if __name__ == "__main__":
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    prompt_version = os.getenv("PROMPT_VERSION", "v1_5")
    idea = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your startup idea: ")
    result = run_evaluation(idea, provider=provider, prompt_version=prompt_version)
    print_result(result)
    log_file = log_evaluation(result, provider=provider, prompt_version=prompt_version)
    print(f"Logged to {log_file}")
