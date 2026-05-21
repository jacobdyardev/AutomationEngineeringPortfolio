import json
from pathlib import Path


def load_data(path: Path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data