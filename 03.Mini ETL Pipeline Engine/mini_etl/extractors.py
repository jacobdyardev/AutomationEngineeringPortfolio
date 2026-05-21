import json
from pathlib import Path


def extract_json(input_path: Path):

    if not input_path.exists():
        raise RuntimeError(f"Input file not found: {input_path}")

    with open(input_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [
            {"source": key, **value}
            for key, value in data.items()
            if isinstance(value, dict)
        ]

    if not isinstance(data, list):
        raise RuntimeError("Input JSON must be a list of objects")

    return data