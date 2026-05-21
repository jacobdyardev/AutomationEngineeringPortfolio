from .rules import check_rules


def evaluate_risk(record):

    score = 0
    reasons = []

    rule_results = check_rules(record)

    for r in rule_results:
        score += r["weight"]

        if r["triggered"]:
            reasons.append(r["reason"])

    # Classification
    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "source": record.get("source"),
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }