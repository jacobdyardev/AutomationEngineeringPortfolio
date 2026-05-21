from pathlib import Path
from automation.utils.debug_logger import DebugLogger  # pyright: ignore[reportMissingImports]


def get_latest_artifact(task_name: str) -> str:
    from automation.utils.paths import get_artifacts_base  # pyright: ignore[reportMissingImports]

    base = get_artifacts_base() / task_name

    if not base.exists():
        raise RuntimeError(f"No artifacts found for task: {task_name}")

    runs = sorted(base.iterdir(), reverse=True)

    if not runs:
        raise RuntimeError(f"No runs found for task: {task_name}")

    latest = runs[0]

    files = list(latest.iterdir())

    # ----------------------------------------
    # 1. Prefer actual data files (NOT metadata)
    # ----------------------------------------
    for f in files:
        if f.name != "run_metadata.json" and f.suffix in [".json", ".csv", ".xlsx"]:
            return str(f)

    # ----------------------------------------
    # 2. Fallback (if only metadata exists)
    # ----------------------------------------
    for f in files:
        if f.suffix in [".json", ".csv", ".xlsx"]:
            return str(f)

    # ----------------------------------------
    # 3. Final fallback
    # ----------------------------------------
    return str(latest)


def execute_pipeline(pipeline_steps, artifact_dir: Path):

    from automation.core.task_runner import run_task  # pyright: ignore[reportMissingImports]

    logger = DebugLogger(artifact_dir)

    last_output = None

    for step in pipeline_steps:

        task_name = step["task"]
        params = step["params"]

        # ========================
        # PARAM INJECTION
        # ========================
        if last_output:
            if isinstance(params, dict):
                params = {
                    **params,
                    "input_path": last_output,
                    "pipeline_mode": True
                }
            elif params:
                params = f"{params},input_path={last_output},pipeline_mode=true"
            else:
                params = {
                    "input_path": last_output,
                    "pipeline_mode": True
                }
        else:
            if isinstance(params, dict):
                params = {**params, "pipeline_mode": True}
            elif params:
                params = f"{params},pipeline_mode=true"
            else:
                params = {"pipeline_mode": True}

        print(f"\n--- Running: {task_name} ({params}) ---")

        logger.log_step_start(task_name, params)

        try:
            exit_code = run_task(task_name, params)

            # 🔥 FIX: Proper artifact selection
            output_path = get_latest_artifact(task_name)

            if exit_code == 0:
                logger.log_step_end("SUCCESS", output_path)
            elif exit_code == 2:
                logger.log_step_end("PARTIAL", output_path)
            elif exit_code == 1:
                logger.log_step_end("FAILED", output_path)
            else:
                logger.log_step_end("UNKNOWN", output_path)

        except Exception as e:
            logger.log_error(e)
            logger.save()
            raise

        # ========================
        # EXIT HANDLING
        # ========================
        if exit_code == 1:
            print(f"Pipeline failed at {task_name}")
            logger.save()
            return 1

        elif exit_code == 2:
            print(f"Warning: {task_name} partially succeeded, continuing...")

        elif exit_code != 0:
            print(f"Warning: {task_name} returned unknown exit code ({exit_code}), continuing...")

        last_output = output_path

    logger.save()

    print("\nPipeline completed successfully")
    return 0