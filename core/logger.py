import json
from datetime import datetime, timezone
from pathlib import Path

from models.evaluation import EvaluationResult

LOGS_DIR = Path(__file__).parent.parent / "logs"


def log_evaluation(result: EvaluationResult, provider: str, prompt_version: str) -> Path:
    LOGS_DIR.mkdir(exist_ok=True)
    log_file = LOGS_DIR / "evaluations.jsonl"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "prompt_version": prompt_version,
        "idea": result.idea,
        "build_signal": result.build_signal.value,
        "verdict": result.verdict,
        "weakest_dimension": result.weakest_dimension,
        "dimensions": [d.model_dump() for d in result.dimensions],
        "strengths": result.strengths,
        "weaknesses": result.weaknesses,
        "risks": result.risks,
        "next_steps": result.next_steps,
    }

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return log_file
