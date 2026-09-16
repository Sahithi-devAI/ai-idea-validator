from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(version: str = "v1_6") -> str:
    path = PROMPTS_DIR / f"{version}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_messages(idea: str, prompt_version: str = "v1_6") -> tuple[str, list]:
    system = load_prompt(prompt_version)
    messages = [{"role": "user", "content": f"Evaluate this idea:\n\n{idea}"}]
    return system, messages
