from pathlib import Path
from automation.core.task_contract import TaskResult # pyright: ignore[reportMissingImports]
from .pipeline import PIPELINES
from .worker import run_pipeline


PARAM_SPEC = {
    "pipeline": {
        "required": True,
        "description": "Pipeline name to run"
    }
}

TASK_NAME = "scheduler_worker"


def run(artifact_dir: Path, params: dict):

    pipeline_name = params.get("pipeline")

    if pipeline_name not in PIPELINES:
        return TaskResult(
            success=False,
            message=f"Unknown pipeline: {pipeline_name}"
        )

    exit_code = run_pipeline(PIPELINES[pipeline_name])

    if exit_code == 0:
        return TaskResult(success=True, message="Pipeline completed")
    else:
        return TaskResult(success=False, message="Pipeline failed")