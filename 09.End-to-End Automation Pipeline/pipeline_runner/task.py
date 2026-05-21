from pathlib import Path
from automation.core.task_contract import TaskResult  # pyright: ignore[reportMissingImports]
from .pipelines import PIPELINES
from .executor import execute_pipeline


TASK_NAME = "pipeline_runner"


PARAM_SPEC = {
    "pipeline": {
        "required": False,
        "description": "Predefined pipeline name"
    },
    "steps": {
        "required": False,
        "description": "Dynamic pipeline steps separated by |"
    }
}


def run(artifact_dir: Path, params: dict):

    try:
        pipeline_name = params.get("pipeline")
        steps_param = params.get("steps")

        # BUILD PIPELINE
        
        if steps_param:
            steps = [step.strip() for step in steps_param.split("|") if step.strip()]

            if not steps:
                return TaskResult(
                    success=False,
                    message="No valid steps provided"
                )

            pipeline = []

            for i, step in enumerate(steps):
                next_step = steps[i + 1] if i + 1 < len(steps) else None

                step_params = {
                    **params,
                    "pipeline_mode": True,
                    "pipeline_next": next_step
                }

                pipeline.append({
                    "task": step,
                    "params": step_params
                })

        elif pipeline_name:
            if pipeline_name not in PIPELINES:
                return TaskResult(
                    success=False,
                    message=f"Unknown pipeline: {pipeline_name}"
                )

            pipeline = PIPELINES[pipeline_name]

        else:
            return TaskResult(
                success=False,
                message="Either 'pipeline' or 'steps' must be provided"
            )

        _ = artifact_dir

        exit_code = execute_pipeline(pipeline, artifact_dir)

        if exit_code == 0:
            return TaskResult(success=True, message="Pipeline completed")
        else:
            return TaskResult(success=False, message="Pipeline failed")

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )