from pathlib import Path
from automation.core.task_contract import TaskResult # pyright: ignore[reportMissingImports]

from .pipeline import run_pipeline


PARAM_SPEC = {
    "input_path": {
        "required": True,
        "description": "Path to input JSON file"
    },
    "output_format": {
        "required": False,
        "default": "json",
        "description": "json, csv, or excel"
    },
    "fields": {
        "required": False,
        "description": "Comma-separated fields to keep"
    },
    "rename": {
        "required": False,
        "description": "Mapping old:new,old:new"
    },
    "metrics": {
        "required": False,
        "description": "Comma-separated metrics (sum,count)"
    },
    "mapping_file": {
        "required": False,
        "description": "Path to TOML extraction mapping"
    },
    "output_mode": {
        "required": False,
        "default": "wide",
        "description": "wide, grouped, or sheets (excel only)"
    },
    "mapping_key": {
        "required": False,
        "description": "Explicit mapping section to use"
    }
}


TASK_NAME = "mini_etl"


def run(artifact_dir: Path, params: dict):

    try:
        transformed, metrics, data_file, metrics_file = run_pipeline(
            artifact_dir,
            params
        )

        message = f"Processed {len(transformed)} records."

        artifacts = [str(data_file)]

        if metrics:
            artifacts.append(str(metrics_file))

        return TaskResult(
            success=True,
            message=message,
            artifacts=artifacts
        )

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )