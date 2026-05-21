import json
from datetime import datetime
from pathlib import Path


def write_run_metadata(
    artifact_dir,
    task_name,
    status,
    message=None,
    params=None,
    duration_seconds=None,
):

    metadata = {
        "task": task_name,
        "status": status,
        "message": message,
        "params": params or {},
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration_seconds,
    }

    with open(artifact_dir / "run_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)