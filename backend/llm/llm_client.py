# backend/llm/llm_client.py

def call_llm(prompt: str) -> str:
    """
    Mocked LLM call.
    In real systems, this would call OpenAI / Azure / local LLM.
    """
    return f"[LLM RESPONSE]: Processed safely -> {prompt}"
