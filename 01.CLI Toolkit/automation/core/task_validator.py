import inspect


def validate_task_callable(name: str, task_callable):

    if not callable(task_callable):
        raise RuntimeError(
            f"Task '{name}' is not callable"
        )

    sig = inspect.signature(task_callable)

    if len(sig.parameters) < 2:
        raise RuntimeError(
            f"Task '{name}' must accept (artifact_dir, params)"
        )