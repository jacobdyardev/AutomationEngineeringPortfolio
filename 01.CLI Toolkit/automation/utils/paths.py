from pathlib import Path
from datetime import datetime
import shutil


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"


from pathlib import Path

def get_artifacts_base() -> Path:
    return Path(__file__).resolve().parents[2] / "artifacts"


def create_run_artifact_dir(task_name: str) -> Path:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = ARTIFACT_ROOT / task_name / timestamp

    run_dir.mkdir(parents=True, exist_ok=True)

    enforce_retention(task_name)

    return run_dir


def enforce_retention(task_name: str, keep_last: int = 10):

    task_dir = ARTIFACT_ROOT / task_name

    if not task_dir.exists():
        return

    runs = sorted(
        [p for p in task_dir.iterdir() if p.is_dir()],
        reverse=True
    )

    for old_run in runs[keep_last:]:
        shutil.rmtree(old_run, ignore_errors=True)