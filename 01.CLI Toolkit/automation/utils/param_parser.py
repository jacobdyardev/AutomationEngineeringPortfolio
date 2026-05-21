def parse_params(params: str | None) -> dict:

    if not params:
        return {}

    parsed = {}

    pairs = [part.strip() for part in params.split(",") if part.strip()]

    for pair in pairs:
        if "=" not in pair:
            continue

        key, value = pair.split("=", 1)

        parsed[key.strip()] = value.strip()

    return parsed