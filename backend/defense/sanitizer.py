# backend/defense/sanitizer.py

def sanitize_prompt(prompt: str) -> str:
    blocked_phrases = [
        "ignore previous instructions",
        "reveal system prompt",
        "developer mode"
    ]

    sanitized = prompt
    for phrase in blocked_phrases:
        sanitized = sanitized.replace(phrase, "[REMOVED]")

    return sanitized
