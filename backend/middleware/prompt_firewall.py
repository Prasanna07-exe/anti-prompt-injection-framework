from backend.detection.rule_engine import rule_based_detection
from backend.detection.semantic_detector import semantic_risk_score
from backend.detection.risk_scorer import calculate_risk
from backend.defense.sanitizer import sanitize_prompt
from backend.defense.response_filter import filter_response
from backend.monitoring.metrics import update_metrics
from backend.llm.llm_client import call_llm
from backend.defense.data_guard import check_sensitive_request


def prompt_firewall(prompt: str) -> dict:
    """
    Scalable, risk-based prompt firewall.
    Enforces hard security invariants + confidence-based routing.
    """

    try:
        # ---------- Tier 0: Sensitive Data Guard ----------
        # (Not prompt injection, but must be handled safely)
        if check_sensitive_request(prompt):
            update_metrics("sanitized")
            return {
                "status": "safe_response",
                "response": "I can’t share confidential or private information."
            }

        # ---------- Tier 1: Rule-Based Detection ----------
        rule_result = rule_based_detection(prompt)
        rule_score = rule_result["rule_score"]

        # 🚨 HARD BLOCK: Critical instruction override (NON-NEGOTIABLE)
        if rule_result.get("critical", False):
            update_metrics("blocked")
            return {
                "status": "blocked",
                "reason": "Critical Instruction Override",
                "details": {
                    "rule_score": round(rule_score, 2)
                }
            }

        # 🚀 Fast allow: most benign traffic exits here
        if rule_score < 0.15:
            update_metrics("allowed")
            response = call_llm(prompt)
            return {
                "status": "safe_response",
                "risk": {
                    "risk_score": round(rule_score, 2),
                    "attack_type": "Benign Prompt"
                },
                "response": filter_response(response)
            }

        # ---------- Tier 2: Semantic Intent Analysis ----------
        semantic_score = semantic_risk_score(prompt)

        # ---------- Tier 3: Risk Aggregation ----------
        risk_result = calculate_risk(rule_result, semantic_score)
        final_score = risk_result["risk_score"]

        # ---------- Tier 4: Decision ----------
        if final_score >= 0.6:
            update_metrics("blocked")
            return {
                "status": "blocked",
                "reason": risk_result["attack_type"],
                "details": {
                    "rule_score": round(rule_score, 2),
                    "semantic_score": round(semantic_score, 2)
                }
            }

        if final_score >= 0.35:
            update_metrics("sanitized")
            prompt = sanitize_prompt(prompt)
        else:
            update_metrics("allowed")

        # ---------- Tier 5: Safe LLM Call ----------
        response = call_llm(prompt)

        return {
            "status": "safe_response",
            "risk": risk_result,
            "response": filter_response(response)
        }

    except Exception:
        # ---------- Fail-Safe Default ----------
        update_metrics("sanitized")
        return {
            "status": "safe_response",
            "response": "Request processed safely."
        }
