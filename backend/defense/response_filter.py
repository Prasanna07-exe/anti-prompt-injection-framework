# backend/defense/response_filter.py

SENSITIVE_TERMS = [
    "system prompt",
    "confidential",
    "internal instructions"
]


def filter_response(response: str) -> str:
    filtered = response
    for term in SENSITIVE_TERMS:
        if term in filtered.lower():
            filtered = filtered.replace(term, "[REDACTED]")
    return filtered
