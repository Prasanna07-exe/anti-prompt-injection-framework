# backend/defense/data_guard.py

# Sensitive business, internal, or credential information
SENSITIVE_REQUESTS = [
    # Business / organizational
    "company secrets",
    "confidential information",
    "internal data",
    "private data",
    "trade secrets",
    "company strategy",
    "business strategy",
    "company plans",
    "internal roadmap",
    "internal policies",

    # 🔧 Development / engineering (NEW)
    "development information",
    "internal development",
    "engineering details",
    "internal architecture",
    "development details",
    "internal implementation",

    # Credentials / secrets
    "api key",
    "secret key",
    "access token",
    "authentication token",
    "private key",
    "credentials",
    "password"

    "how the system decides what to block",
    "how blocking works",
    "decision logic of the system",
    "internal decision process"

]

NEGATION_TERMS = [
    "do not",
    "don't",
    "dont",
    "never",
    "no need",
    "not required",
    "without"
]


def check_sensitive_request(prompt: str) -> bool:
    """
    Detects genuine requests for sensitive internal,
    business, development, or credential information.
    """
    prompt_lower = prompt.lower()

    # Ignore explicit negation
    if any(neg in prompt_lower for neg in NEGATION_TERMS):
        return False

    return any(term in prompt_lower for term in SENSITIVE_REQUESTS)
