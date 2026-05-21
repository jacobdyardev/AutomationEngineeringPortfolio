def clean_price(value):
    if not value:
        return None

    cleaned = (
        str(value)
        .replace("$", "")
        .replace(",", "")
        .replace("–", "")
        .replace("-", "")
        .strip()
    )

    try:
        return float(cleaned)
    except:
        return None


def parse_list(value: str | None):
    if not value:
        return None
    return [v.strip() for v in value.split(",")]


def parse_mapping(value: str | None):
    if not value:
        return {}

    mapping = {}
    for pair in value.split(","):
        old, new = pair.split(":")
        mapping[old.strip()] = new.strip()

    return mapping


def apply_transforms(data, fields, rename_map, mapping_config=None):

    transformed = []

    for row in data:

        # Remove error BEFORE processing
        row = dict(row)
        error = row.pop("error", None)

        new_row = {}

        # ========================
        # FIELD SELECTION
        # ========================
        if fields:
            for f in fields:
                if f in row:
                    new_row[f] = row[f]
        else:
            new_row = dict(row)

        # ========================
        # RENAME
        # ========================
        for old, new in rename_map.items():
            if old in new_row:
                new_row[new] = new_row.pop(old)

        # ========================
        # STATUS HANDLING (FIXED)
        # ========================
        status = "SUCCESS"

        if error:
            status = "FAILURE"
        elif not new_row or len(new_row) == 1:  # only "source"
            status = "FAILURE"

        # ========================
        # BUILD FINAL ROW
        # ========================
        final_row = {}

        source_val = new_row.pop("source", "unknown")
        final_row["source"] = source_val
        final_row["status"] = status

        # ----------------------------------------
        # 🔥 ORDER ENFORCEMENT (TOML-driven)
        # ----------------------------------------

        ordered_keys = []

        if mapping_config:

            source = final_row["source"].lower()

            mapping = mapping_config.get(source, {})

            # fallback: try alias match
            if not mapping:
                for key, value in mapping_config.items():
                    aliases = value.get("aliases", [])
                    if source in [a.lower() for a in aliases]:
                        mapping = value
                        break

            ordered_keys = [
                k for k in mapping.keys()
                if k != "aliases"
            ]

        # Always include dynamic fields after
        dynamic_keys = [
            k for k in new_row.keys()
            if k not in ordered_keys
        ]

        final_order = ordered_keys + dynamic_keys

        for key in final_order:

            value = new_row.get(key)

            if "price" in key.lower():
                value = clean_price(value)

            final_row[key] = value

        transformed.append(final_row)

    return transformed


def compute_metrics(data, metrics):

    result = {}

    if not data:
        return result

    numeric_fields = [
        k for k, v in data[0].items()
        if isinstance(v, (int, float))
    ]

    for m in metrics or []:

        if m == "count":
            result["count"] = len(data)

        elif m == "sum":
            for f in numeric_fields:
                result[f"sum_{f}"] = sum(
                    row.get(f, 0) for row in data
                )

    return result