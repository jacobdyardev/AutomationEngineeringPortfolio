from pathlib import Path
import json

from automation.core.task_contract import TaskResult # pyright: ignore[reportMissingImports]
from .engine import run_engine
from .config import build_config


TASK_NAME = "web_automation"


PARAM_SPEC = {
    "url": {
        "required": True,
        "description": "Target URL to scrape"
    },
    "selector": {
        "required": True,
        "description": "CSS selector for elements"
    },
    "limit": {
        "required": False,
        "default": 10,
        "description": "Maximum number of elements to extract"
    },
    "fields": {
        "required": True,
        "description": "Field extraction config (e.g. title:text|link:href)"
    },
    "config": {
    "required": False,
    "description": "Path to JSON config file"
    },
    "mode": {
        "required": False,
        "default": "static",
        "description": "Fetch mode (static, browser, etc.)"
    }
}


def run(artifact_dir: Path, params: dict):

    try:
        config = build_config(params)

        data = run_engine(config)

        if not data:
            return TaskResult(
                success=False,
                message="No data extracted"
            )

        output_file = artifact_dir / "scraped_data.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return TaskResult(
            success=True,
            message=f"Extracted {len(data)} items",
            artifacts=[str(output_file)]
        )

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )