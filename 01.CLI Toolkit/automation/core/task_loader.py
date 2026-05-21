import importlib
import pkgutil
import traceback

from automation.tasks import __path__ as internal_tasks_path
from automation.core.discovery_result import DiscoveryResult
from automation.core.task_validator import validate_task_callable

def load_tasks() -> DiscoveryResult:

    failed = []

    result = DiscoveryResult()

    for module_info in pkgutil.iter_modules(internal_tasks_path):

        module_name = module_info.name

        try:
            module = importlib.import_module(
                f"automation.tasks.{module_name}"
            )
        except Exception as e:
            result.failed[module_name] = str(e)
            continue

        if not hasattr(module, "run"):
            result.failed[module_name] = "Missing required run callable"
            continue

        task_callable = module.run

        try:
            validate_task_callable(module_name, task_callable)
        except Exception as e:
            result.failed[module_name] = str(e)
            continue

        result.tasks[module_name] = task_callable

    try:
        from automation import external_tasks

        external_path = external_tasks.__path__

        for module_info in pkgutil.iter_modules(external_path):

            module_name = module_info.name

            try:
                module = importlib.import_module(
                    f"automation.external_tasks.{module_name}"
                )
            except Exception as e:
                print(f"\n🔥 ERROR loading task: {module_name}")
                traceback.print_exc()
                failed.append(module_name)
                continue

            if not hasattr(module, "run"):
                result.failed[module_name] = "Missing required run callable"
                continue

            task_callable = module.run

            try:
                validate_task_callable(module_name, task_callable)
            except Exception as e:
                result.failed[module_name] = str(e)
                continue

            result.tasks[module_name] = task_callable

    except ImportError as e:
        pass

    return result