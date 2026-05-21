import json
from pathlib import Path


def load_config_file(path: str) -> dict:

    from automation.utils.path_resolver import resolve_path # pyright: ignore[reportMissingImports]
    config_path = resolve_path(path, subdir="web")

    if not config_path.exists():
        raise RuntimeError(f"Config file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def parse_fields_string(fields_str: str) -> list:

    fields = []

    for part in fields_str.split("|"):
        pieces = part.split(":")

        if len(pieces) == 2:
            name, attr = pieces
            fields.append({
                "name": name,
                "selector": None,
                "attribute": attr
            })

        elif len(pieces) == 3:
            name, selector, attr = pieces
            fields.append({
                "name": name,
                "selector": selector,
                "attribute": attr
            })

    return fields


def build_config(params: dict) -> dict:

    config_file = params.get("config")

    if config_file:
        return load_config_file(config_file)

    raw_fields = params.get("fields")

    if isinstance(raw_fields, str):
        fields = parse_fields_string(raw_fields)
    else:
        fields = raw_fields

    return {
        "url": params.get("url"),
        "selector": params.get("selector"),
        "fields": fields,
        "limit": int(params.get("limit", 10)),
        "mode": params.get("mode", "static"),
        "filters": params.get("filters")
    }