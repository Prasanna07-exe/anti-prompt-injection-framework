# backend/detection/risk_scorer.py

def calculate_risk(rule_result: dict, semantic_score: float) -> dict:
    # Weighted hybrid score
    final_score = (
        0.6 * rule_result["rule_score"] +
        0.4 * semantic_score
    )

    if final_score >= 0.6:
        attack_type = "Prompt Injection Attempt"
    elif final_score >= 0.35:
        attack_type = "Suspicious Prompt"
    else:
        attack_type = "Benign Prompt"

    return {
        "risk_score": round(final_score, 2),
        "attack_type": attack_type
    }
