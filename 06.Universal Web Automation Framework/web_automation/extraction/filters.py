def apply_filters(rows: list, filters: list) -> list:
    # Apply config-driven filters to extracted data

    if not filters:
        return rows

    filtered = []

    for row in rows:
        include = True

        for f in filters:
            field = f.get("field")

            if not field:
                continue

            value = row.get(field)

            # --- not_null ---
            if f.get("not_null") and value is None:
                include = False
                break

            # --- contains ---
            if "contains" in f:
                if value is None or f["contains"] not in str(value):
                    include = False
                    break

            # --- not_contains ---
            if "not_contains" in f:
                if value is not None and f["not_contains"] in str(value):
                    include = False
                    break

            # --- equals ---
            if "equals" in f:
                if value != f["equals"]:
                    include = False
                    break
                
        if include:
            filtered.append(row)

    return filtered