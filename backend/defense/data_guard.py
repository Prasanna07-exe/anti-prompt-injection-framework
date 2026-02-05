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
    "password",

    # 🔥 --- Employee / PII data (NEW – IMPORTANT) ---
    "employee personal details",
    "employee personal data",
    "employee details",
    "employee information",
    "employee phone",
    "employee phone number",
    "employee address",
    "employee email",
    "employee salary",
    "employee records",
    "staff personal details",
    "staff personal data",
    "personal details of employees"

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
    if not prompt:
        return False
    
    prompt_lower = prompt.lower()

    # Ignore explicit negation
    if any(neg in prompt_lower for neg in NEGATION_TERMS):
        return False

    return any(term in prompt_lower for term in SENSITIVE_REQUESTS)

