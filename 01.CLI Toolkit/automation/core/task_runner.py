import time
from automation.core.task_registry import TASKS
from automation.utils.paths import create_run_artifact_dir
from automation.utils.run_metadata import write_run_metadata
from automation.utils.param_parser import parse_params
from automation.core.task_contract import TaskResult


def run_task(task_name: str, params: str | None = None) -> int:

    task = TASKS.get(task_name)

    if not task:
        print(f"Unknown task: {task_name}")
        return 1

    if isinstance(params, dict):
        parsed_params = params
    else:
        parsed_params = parse_params(params)

    spec = getattr(task, "PARAM_SPEC", {})

    from automation.core.param_runtime import (
        validate_required_params,
        apply_param_defaults,
    )

    parsed_params = apply_param_defaults(parsed_params, spec)

    try:
        validate_required_params(parsed_params, spec)
    except RuntimeError as e:
        print(f"Runtime error: {e}")
        return 1
    
    print(f"Running task: {task_name}")

    if parsed_params:
        print(f"Params → {parsed_params}")

    artifact_dir = create_run_artifact_dir(task_name)

    print(f"Artifacts → {artifact_dir}")

    write_run_metadata(
        artifact_dir,
        task_name,
        status="STARTED",
        params=parsed_params
    )

    start_time = time.time()

    try:

        result = task(artifact_dir, parsed_params)

        if not isinstance(result, TaskResult):
            raise RuntimeError(
                f"Task '{task_name}' returned invalid result type: {type(result)}"
            )

        duration = round(time.time() - start_time, 3)

        if result.partial:
            final_status = "PARTIAL"
            exit_code = 2
        elif result.success:
            final_status = "SUCCESS"
            exit_code = 0
        else:
            final_status = "FAILED"
            exit_code = 1

        write_run_metadata(
            artifact_dir,
            task_name,
            status=final_status,
            message=result.message,
            params=parsed_params,
            duration_seconds=duration
        )

        print(f"Status: {final_status}")
        print(f"Duration: {duration}s")

        if result.message:
            print(result.message)

        return exit_code

    except Exception as e:

        duration = round(time.time() - start_time, 3)

        write_run_metadata(
            artifact_dir,
            task_name,
            status="FAILED",
            message=str(e),
            params=parsed_params,
            duration_seconds=duration
        )

        print("Task crashed:")
        print(e)
        print(f"Duration: {duration}s")

        return 1