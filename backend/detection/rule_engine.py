# backend/detection/rule_engine.py

import re

# Regex patterns for known injection styles
INJECTION_PATTERNS = [
    r"ignore (all|previous) instructions",
    r"override (system|safety|previous) (rules|instructions)",
    r"you are no longer bound by (previous )?instructions",
    r"forget (all )?(safety|previous) rules",
    r"follow only my commands",
    r"(enter|enable) developer mode",
    r"(bypass|disable) (all )?(safeguards|restrictions|policies)",
]

CRITICAL_OVERRIDE_PATTERNS = [
    # -------- Instruction override --------
    "ignore all previous instructions",
    "ignore previous instructions",
    "do whatever i say",
    "override system rules",
    "you are no longer bound by",
    "forget all safety rules",
    "follow only my commands",

    # -------- Role / authority hijacking --------
    "you are now the system",
    "you are the system",
    "act as the system",
    "assume system role",
    "execute internal instructions",
    "act as system prompt",

    # -------- Internal system disclosure (NEW) --------
    "reveal internal system",
    "reveal system settings",
    "reveal system prompt",
    "show internal configuration",
    "expose internal configuration",
    "expose hidden policies",
    "show hidden policies",
    "internal system settings"

   
]



# Softer heuristic keywords (signal only, not absolute)
KEYWORDS = [
    "ignore",
    "override",
    "developer mode",
    "system prompt",
    "hidden policies",
    "bypass",
    "disable safeguards"
]


def rule_based_detection(prompt: str) -> dict:
    prompt_lower = prompt.lower()

    matched_patterns = []
    matched_keywords = []

    # ---------- HARD BLOCK CHECK ----------
    for phrase in CRITICAL_OVERRIDE_PATTERNS:
        if phrase in prompt_lower:
            return {
                "matched_patterns": [phrase],
                "matched_keywords": [],
                "rule_score": 1.0,
                "critical": True
            }

    # ---------- REGEX PATTERN MATCHING ----------
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt_lower):
            matched_patterns.append(pattern)

    # ---------- KEYWORD HEURISTICS ----------
    for keyword in KEYWORDS:
        if keyword in prompt_lower:
            matched_keywords.append(keyword)

    # ---------- SCORING ----------
    # Patterns are stronger than keywords
    score = 0.0
    score += 0.25 * len(matched_keywords)
    score += 0.6 * len(matched_patterns)

    return {
        "matched_patterns": matched_patterns,
        "matched_keywords": matched_keywords,
        "rule_score": min(score, 1.0),
        "critical": False
    }
