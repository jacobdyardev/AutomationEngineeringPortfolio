import json
from pathlib import Path
from typing import Optional

from automation.utils.paths import ARTIFACT_ROOT


def find_run_dir(task_name: str, run_id: str) -> Optional[Path]:

    run_dir = ARTIFACT_ROOT / task_name / run_id

    if not run_dir.exists() or not run_dir.is_dir():
        return None

    return run_dir


def list_artifact_files(run_dir: Path) -> list[str]:

    return sorted(
        [p.name for p in run_dir.iterdir() if p.is_file()]
    )


def list_all_task_names() -> list[str]:

    if not ARTIFACT_ROOT.exists() or not ARTIFACT_ROOT.is_dir():
        return []

    task_dirs = [p.name for p in ARTIFACT_ROOT.iterdir() if p.is_dir()]
    task_dirs.sort()
    return task_dirs


def list_task_run_dirs(task_name: str) -> list[Path]:

    task_dir = ARTIFACT_ROOT / task_name

    if not task_dir.exists() or not task_dir.is_dir():
        return []

    run_dirs = [p for p in task_dir.iterdir() if p.is_dir()]
    run_dirs.sort(reverse=True)
    return run_dirs


def read_run_metadata(run_dir: Path) -> dict | None:

    metadata_file = run_dir / "run_metadata.json"

    if not metadata_file.exists():
        return None

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None