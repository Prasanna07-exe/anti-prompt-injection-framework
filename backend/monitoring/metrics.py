# backend/monitoring/metrics.py

metrics = {
    "total_prompts": 0,
    "blocked": 0,
    "sanitized": 0,
    "allowed": 0
}

def update_metrics(status: str):
    metrics["total_prompts"] += 1

    if status == "blocked":
        metrics["blocked"] += 1
    elif status == "sanitized":
        metrics["sanitized"] += 1
    else:
        metrics["allowed"] += 1

def get_metrics():
    return metrics
