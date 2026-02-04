# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from backend.middleware.prompt_firewall import prompt_firewall
from backend.monitoring.metrics import get_metrics

app = FastAPI(title="Anti Prompt Injection Framework")


class PromptRequest(BaseModel):
    prompt: str


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    result = prompt_firewall(request.prompt)
    return result

@app.get("/metrics")
def metrics():
    return get_metrics()