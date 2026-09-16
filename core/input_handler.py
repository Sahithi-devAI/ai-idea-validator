MIN_LENGTH = 10
MAX_LENGTH = 2000


def validate_idea(idea: str) -> str:
    idea = idea.strip()
    if len(idea) < MIN_LENGTH:
        raise ValueError(f"Idea too short (min {MIN_LENGTH} chars). Add more detail.")
    if len(idea) > MAX_LENGTH:
        raise ValueError(f"Idea too long (max {MAX_LENGTH} chars). Be more concise.")
    return idea
