import inspect

from automation.core.task_loader import load_tasks


DISCOVERY = load_tasks()
TASKS = DISCOVERY.tasks
FAILED_TASKS = DISCOVERY.failed