import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import run_evaluation

load_dotenv()

app = FastAPI(title="AI Idea Validator", version="1.0.0")

_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in _allowed_origins],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class IdeaRequest(BaseModel):
    idea: str
    provider: str = "anthropic"


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/evaluate")
async def evaluate_idea(request: IdeaRequest):
    try:
        result = run_evaluation(request.idea, provider=request.provider)
        return result.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
