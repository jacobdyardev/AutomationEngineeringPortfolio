def get_nested_value(data, path):
    keys = path.split(".")
    value = data

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None

    return value

def check_rules(record):

    results = []

    # Rule 1: Failure status
    if record.get("status") == "FAILURE":
        results.append({
            "triggered": True,
            "weight": 50,
            "reason": "Source failed"
        })

    # Rule 2: High temperature
    temp = get_nested_value(record, "current_weather.temperature")

    if temp and temp > 30:
        results.append({
            "triggered": True,
            "weight": 30,
            "reason": "High temperature"
        })

    # Rule 3: Missing data
    if not temp:
        results.append({
            "triggered": True,
            "weight": 20,
            "reason": "Missing temperature"
        })

    return results