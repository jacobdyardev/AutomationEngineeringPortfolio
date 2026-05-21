import sys
import typer
from typing import Optional

from automation.core.task_introspection import (
    get_param_spec,
    summarize_params
)
from automation.core.task_runner import run_task
from automation.core.task_registry import TASKS, FAILED_TASKS
from automation.core.param_runtime import (
    print_param_help,
    apply_param_defaults
)
from automation.utils.param_parser import parse_params
from automation.utils.run_history import (
    list_artifact_files,
    list_all_task_names,
    list_task_run_dirs,
    read_run_metadata,
    find_run_dir,    
)

app = typer.Typer()

runs_app = typer.Typer()
app.add_typer(runs_app, name="runs")

tasks_app = typer.Typer()
app.add_typer(tasks_app, name="tasks")

plugin_app = typer.Typer(help="Plugin management commands")
app.add_typer(plugin_app, name="plugin")


@app.command()
def run(
    task: str,
    params: str = typer.Option(
        None,
        "--params",
        "-p",
        help="Optional comma-separated key=value pairs"
    )
):
    """Run an automation task"""

    task_callable = TASKS.get(task)

    if not task_callable:
        print(f"Unknown task: {task}")
        raise typer.Exit(code=1)

    if params is None:
        spec = get_param_spec(task_callable)

        if spec:
            print_param_help(task, spec)
            raise typer.Exit()

    spec = get_param_spec(task_callable)

    parsed = parse_params(params)

    parsed = apply_param_defaults(parsed, spec)

    exit_code = run_task(task, parsed)
    raise typer.Exit(code=exit_code)


@runs_app.command("list")
def runs_list(
    task: Optional[str] = typer.Argument(None)
):
    """List recent task runs"""

    task_names = [task] if task else list_all_task_names()

    if not task_names:
        print("No artifact runs found.")
        return

    for task_name in task_names:
        run_dirs = list_task_run_dirs(task_name)

        if not run_dirs:
            print(f"\nTask: {task_name}")
            print("- No runs found")
            continue

        print(f"\nTask: {task_name}")

        for run_dir in run_dirs:
            metadata = read_run_metadata(run_dir)

            if not metadata:
                print(f"- {run_dir.name} | metadata missing")
                continue

            status = metadata.get("status", "UNKNOWN")

            duration = metadata.get("duration_seconds")
            duration_text = f"{duration}s" if duration is not None else "n/a"

            print(f"- {run_dir.name} | {status} | {duration_text}")


@runs_app.command("show")
def runs_show(
    task: str,
    run_id: str
):
    """Show details of a specific run"""

    run_dir = find_run_dir(task, run_id)

    if not run_dir:
        print(f"Run not found: {task}/{run_id}")
        raise typer.Exit(code=1)

    metadata = read_run_metadata(run_dir)

    print()
    print(f"Task: {task}")
    print(f"Run: {run_id}")
    print()

    if metadata:
        duration = metadata.get("duration_seconds")
        duration_text = f"{duration}s" if duration is not None else "n/a"

        print(f"Status: {metadata.get('status')}")
        print(f"Duration: {duration_text}")
        print(f"Timestamp: {metadata.get('timestamp')}")
        print()

        params = metadata.get("params")

        if params:
            print("Params:")
            for k, v in params.items():
                print(f"- {k} = {v}")
            print()

    print("Artifacts:")

    for file in list_artifact_files(run_dir):
        print(f"- {file}")


@tasks_app.command("describe")
def tasks_describe(task: str):
    """Describe a task's parameters and contract"""

    task_callable = TASKS.get(task)

    if not task_callable:
        print(f"Unknown task: {task}")
        raise typer.Exit(code=1)

    spec = get_param_spec(task_callable)

    print()
    print(f"Task: {task}")
    print()

    if not spec:
        print("No parameters")
        return

    print("Parameters:")
    for name, meta in spec.items():

        required = "required" if meta.get("required") else "optional"
        default = meta.get("default")

        print(f"- {name} ({required})")

        if default is not None:
            print(f"  default = {default}")

        desc = meta.get("description")
        if desc:
            print(f"  {desc}")

    print()


@tasks_app.command("list")
def tasks_list(
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """List available automation tasks"""

    if not TASKS:

        if FAILED_TASKS:
            print("No tasks loaded.\n")

            print("Failed to load:")
            for name in FAILED_TASKS:
                print(f"- {name}")

        else:
            print("No tasks registered.")

        return

    print("\nAvailable tasks:\n")

    for name, task in TASKS.items():

        spec = get_param_spec(task)

        if not verbose:
            summary = summarize_params(spec)
            print(f"{name:<15} | {summary}")
            continue

        # verbose mode
        print(f"Task: {name}")

        if not spec:
            print("No params\n")
            continue

        print("Params:")

        for param, meta in spec.items():
            label = "(required)" if meta.get("required") else "(optional)"
            default = meta.get("default")

            if default is not None:
                print(f"- {param} {label}, default={default}")
            else:
                print(f"- {param} {label}")

        print()

    if FAILED_TASKS:
        print("")

        print("Failed to load:")

        for name in FAILED_TASKS:
            print(f"- {name}")


@plugin_app.command("install")
def plugin_install(package: str):

    import importlib
    from pathlib import Path

    try:
        module = importlib.import_module(package)
    except Exception as e:
        print(f"Failed to import package '{package}': {e}")
        raise typer.Exit(1)

    # Assume standard entrypoint location
    try:
        task_module = importlib.import_module(f"{package}.task")
    except Exception as e:
        print(f"Package '{package}' does not expose a task module: {e}")
        raise typer.Exit(1)

    if not hasattr(task_module, "run"):
        print(f"Package '{package}' does not have a run() function")
        raise typer.Exit(1)

    # Create bridge file
    project_root = Path(__file__).resolve().parents[2]
    bridge_dir = project_root / "automation" / "external_tasks"

    bridge_dir.mkdir(exist_ok=True)

    task_name = getattr(task_module, "TASK_NAME", package)

    bridge_file = bridge_dir / f"{task_name}.py"

    with open(bridge_file, "w") as f:
        f.write(
            f"# Auto-generated plugin bridge\n"
            f"from {package}.task import run\n\n"
            f"# Expose PARAM_SPEC for CLI + validation\n"
            f"PARAM_SPEC = getattr(run, 'PARAM_SPEC', {{}})\n"
        )

    print(f"Plugin '{package}' installed successfully.")


@plugin_app.command("list")
def plugin_list():

    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    bridge_dir = project_root / "automation" / "external_tasks"

    if not bridge_dir.exists():
        print("No plugins installed.")
        return

    plugins = [
        f.stem
        for f in bridge_dir.glob("*.py")
        if f.name != "__init__.py"
    ]

    if not plugins:
        print("No plugins installed.")
        return

    print("Installed plugins:\n")

    for p in sorted(plugins):
        print(f"- {p}")


@plugin_app.command("uninstall")
def plugin_uninstall(name: str):

    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    bridge_dir = project_root / "automation" / "external_tasks"

    bridge_file = bridge_dir / f"{name}.py"

    if not bridge_file.exists():
        print(f"Plugin '{name}' is not installed.")
        raise typer.Exit(1)

    bridge_file.unlink()

    print(f"Plugin '{name}' uninstalled successfully.")


if __name__ == "__main__":
    app()