# backend/defense/meta_guard.py

def check_meta_policy_request(prompt: str) -> bool:
    """
    Detects meta / control-plane introspection queries.
    These should NOT reach the LLM.
    """
    if not prompt:
        return False

    p = prompt.lower()

    return (
        "how the system decides" in p
        or "decides what to block" in p
        or "what the system blocks" in p
        or "how blocking works" in p
        or "decision logic" in p
        or "internal decision process" in p
        or "how are prompts blocked" in p
        or "why this was blocked" in p
    )

