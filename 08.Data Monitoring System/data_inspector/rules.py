def get_nested_value(row, field):

    keys = field.split(".")

    value = row

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None

    return value


def rule_exists(data, field, original_data=None, skipped=None):

    do_contain = []
    dont_contain = []

    for row in original_data:
        val = get_nested_value(row, field)

        if val is None:
            dont_contain.append(row)
        else:
            do_contain.append(row)

    total = len(original_data)
    valid = len(do_contain)

    return {
        "message": f"{valid}/{total} records contain '{field}'",
        "do_contain": [r.get("source", "unknown") for r in do_contain],
        "dont_contain": [r.get("source", "unknown") for r in dont_contain],
        "checked": data,
        "skipped": skipped or []
    }


def rule_threshold(data, field, value, original_data=None, skipped=None):

    try:
        value = float(value)
    except:
        return {
            "message": "Invalid threshold value",
            "do_contain": [],
            "dont_contain": [r.get("source", "unknown") for r in data],
            "checked": data,
            "skipped": skipped or []
        }

    failed = []

    for row in data:
        try:
            val = get_nested_value(row, field)

            if val is None or float(val) < value:
                failed.append(row)
        except:
            failed.append(row)

    passed = [r for r in data if r not in failed]

    return {
        "message": f"{len(passed)}/{len(data)} records meet threshold for '{field}'",
        "do_contain": [r.get("source", "unknown") for r in passed],
        "dont_contain": [r.get("source", "unknown") for r in failed],
        "checked": data,
        "skipped": skipped or []
    }


def rule_contains(data, field, value, original_data=None, skipped=None):

    failed = []

    for row in data:
        content = str(get_nested_value(row, field) or "")

        if value not in content:
            failed.append(row)

    passed = [r for r in data if r not in failed]

    return {
        "message": f"{len(passed)}/{len(data)} records contain '{value}' in '{field}'",
        "do_contain": [r.get("source", "unknown") for r in passed],
        "dont_contain": [r.get("source", "unknown") for r in failed],
        "checked": data,
        "skipped": skipped or []
    }