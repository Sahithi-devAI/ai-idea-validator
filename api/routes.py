import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from main import run_evaluation

load_dotenv()

app = FastAPI(title="AI Idea Validator", version="1.0.0")


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
