from .rules import rule_exists, rule_threshold, rule_contains


def evaluate_rule(data, rule, field=None, value=None, original_data=None, skipped=None):

    if rule == "exists":
        if not field:
            return {
                "message": "Field is required for 'exists' rule",
                "error": True
            }
        return rule_exists(
            data,
            field,
            original_data=original_data,
            skipped=skipped
        )

    elif rule == "threshold":
        if not field or value is None:
            return {
                "message": "Field and value are required for 'threshold' rule",
                "error": True
            }
        return rule_threshold(
            data,
            field,
            value,
            original_data=original_data,
            skipped=skipped
        )

    elif rule == "contains":
        if not field or value is None:
            return {
                "message": "Field and value are required for 'contains' rule",
                "error": True
            }
        return rule_contains(
            data,
            field,
            value,
            original_data=original_data,
            skipped=skipped
        )

    else:
        return {
            "message": f"Unknown rule: {rule}",
            "error": True
        }