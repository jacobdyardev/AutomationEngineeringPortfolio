import json
from pathlib import Path


def load_data(input_path: Path):

    if not input_path.exists():
        raise RuntimeError(f"Input file not found: {input_path}")

    with open(input_path, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise RuntimeError("Input must be a list of objects")

    return data