RENAME_MAP = {
    "current_weather_temperature": "temperature",
    "current_weather_time": "time",
}


def normalize_rows(data, exclude_errors=False, columns=None):

    if exclude_errors:
        data = [row for row in data if "error" not in row]

    flattened_data = []

    for row in data:
        if not isinstance(row, dict):
            continue

        flattened_data.append(flatten_row(row))

    # Ensure status exists
    for row in flattened_data:
        if "status" not in row:
            if "error" in row and row["error"]:
                row["status"] = "FAILURE"
            else:
                row["status"] = "SUCCESS"

    normalized = []

    for row in flattened_data:

        if not isinstance(row, dict):
            continue

        source = row.get("source")

        if not source:
            continue

        status = row.get("status")

        if not status:
            if row.get("error"):
                status = "FAILURE"
            else:
                status = "SUCCESS"

        clean_row = {}

        # Preserve original order from ETL
        for key, value in row.items():

            if key == "source":
                clean_row[key] = source
                continue

            if key == "status":
                clean_row[key] = status
                continue

            if value not in (None, "", [], {}):
                clean_row[key] = value

        normalized.append(clean_row)

    # headers are now dynamic per row (not global)
    return normalized


def flatten_row(row, parent_key="", sep="_"):

    items = {}

    for k, v in row.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.update(flatten_row(v, new_key, sep=sep))

        elif isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                # Flatten first item of list
                items.update(flatten_row(v[0], new_key, sep=sep))
            else:
                # Store as string to avoid crashes
                items[new_key] = str(v)

        else:
            final_key = RENAME_MAP.get(new_key, new_key)
            items[final_key] = v

    return items