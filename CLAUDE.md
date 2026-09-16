# AI Idea Validator — Project Context

## What this is
An AI-powered startup idea evaluator that answers one question: **"Is this idea worth building?"**

This is NOT a scoring tool. It is an expert evaluator with decision-first output — opinionated, skeptical, specific.

Target users: indie hackers, founders, PMs, hackathon builders. Future: VCs, AI coding platforms (Lovable, Claude Code, Emergent).

---

## Build Signal (core output concept)
Replaces the confidence score, which was removed for being fake precision.

| Signal | Meaning |
|---|---|
| `strong_yes` | Strong opportunity |
| `cautious_yes` | Worth building, but execution/competition risks |
| `explore_more` | Needs validation / unclear wedge |
| `not_recommended` | Fundamentally weak |

**Never reintroduce a confidence score.**

---

## Evaluation dimensions (in priority order)
1. **Product Usefulness** — MOST IMPORTANT
2. Market Potential
3. Feasibility & Defensibility
4. Monetization Viability

---

## Key architecture decisions

| Decision | Choice | Reason |
|---|---|---|
| Output format | Semi-structured text | Strict JSON breaks reasoning and slows iteration |
| Signal logic | Heuristic reasoning | Hard "if X then Y" rules kill nuance |
| Agent architecture | Single-agent (V1) | Multi-agent is V2 |
| Parsing | Post-generation parser in `core/parser.py` | Parses section headers from LLM output |

---

## Project structure
```
core/
  input_handler.py     — validates and cleans idea input
  prompt_manager.py    — loads prompt by version from prompts/
  llm_client.py        — provider-abstracted LLM calls (Anthropic now, open-source in V2)
  parser.py            — parses semi-structured LLM output into EvaluationResult
  signal_validator.py  — sanity-checks signal vs scores, never overrides LLM
models/
  evaluation.py        — Pydantic models: BuildSignal, DimensionScore, EvaluationResult
prompts/
  v1_5.txt             — current locked prompt (do not edit without intention)
api/
  routes.py            — FastAPI: POST /evaluate, GET /health
main.py                — CLI entry point
tests/
  test_parser.py
  test_signal_validator.py
  stress/ideas.py      — stress test cases across idea quality spectrum
logs/                  — JSONL evaluation run logs
```

---

## Prompt versioning
- Prompts live in `prompts/` as versioned `.txt` files
- Current default: `v1_5`
- Change prompt version via `PROMPT_VERSION` env var or `prompt_version` arg in `run_evaluation()`
- Never hardcode prompts in Python files

---

## Running the project
```bash
# Install
pip install -r requirements.txt

# Copy and fill in API key
cp .env.example .env

# Single evaluation (CLI)
python main.py "your idea here"

# API server
uvicorn api.routes:app --reload

# Unit tests (no API key needed)
pytest tests/

# Stress test (calls live API)
python tests/stress/ideas.py
```

---

## What NOT to do
- Do not reintroduce a confidence score
- Do not switch to strict JSON output — it degrades reasoning quality
- Do not add hard scoring rules ("if score < X then signal = Y")
- Do not over-engineer V1 — keep it single-agent
- Do not make outputs generic or optimistic — the evaluator persona is skeptical and sharp

---

## V2 intentions (do not build yet)
- Multi-agent split (market research agent, product usefulness agent, etc.)
- Open-source LLM support — `llm_client.py` is already provider-abstracted for this
- Real market signals via external APIs
- Historical evaluation memory
