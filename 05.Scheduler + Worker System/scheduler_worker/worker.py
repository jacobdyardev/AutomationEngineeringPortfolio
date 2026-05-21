from pathlib import Path


def get_latest_artifact(task_name: str) -> str:

    from automation.utils.paths import get_artifacts_base # pyright: ignore[reportMissingImports]

    base = get_artifacts_base() / task_name

    runs = sorted(base.iterdir(), reverse=True)

    latest = runs[0]

    # Find JSON inside
    for f in latest.iterdir():
        if f.suffix == ".json":
            return str(f)

    return str(latest)


def run_pipeline(pipeline_steps):

    from automation.core.task_runner import run_task # pyright: ignore[reportMissingImports]

    last_output_path = None

    for step in pipeline_steps:

        task_name = step["task"]
        params = step["params"]

        # Inject previous output into ETL + Excel
        if task_name == "mini_etl" and last_output_path:
            params = f"input_path={last_output_path}"

        if task_name == "excel_kpi" and last_output_path:
            params = f"input_path={last_output_path},exclude_errors=true,columns=source|temperature|time"

        print(f"\n--- Running: {task_name} ---")

        exit_code = run_task(task_name, params)

        if exit_code == 1:
            print(f"Pipeline failed at {task_name}")
            return 1

        if exit_code == 2:
            print(f"Warning: {task_name} partially succeeded, continuing...")

        # Get latest artifact path
        last_output_path = get_latest_artifact(task_name)

    print("\nPipeline completed successfully")
    return 0