import json
from pathlib import Path

from automation.core.result import TaskResult


PARAM_SPEC = {
    "path": {
        "required": True,
        "description": "Directory path to scan"
    }
}


def run(artifact_dir, params):

    # --- param validation ---
    if not params or "path" not in params:
        return TaskResult(
            success=False,
            message="Missing required param: path"
        )

    target_path = Path(params["path"])

    if not target_path.exists():
        return TaskResult(
            success=False,
            message=f"Path does not exist: {target_path}"
        )

    # --- scan ---
    total_files = 0
    total_size = 0
    extensions = {}

    for p in target_path.rglob("*"):
        if p.is_file():

            total_files += 1

            try:
                size = p.stat().st_size
                total_size += size
            except Exception:
                # intentionally tolerant
                continue

            ext = p.suffix.lower()

            if not ext:
                ext = "no_extension"

            extensions[ext] = extensions.get(ext, 0) + 1

    # --- artifact write ---
    report = {
        "path": str(target_path),
        "total_files": total_files,
        "total_size_bytes": total_size,
        "extensions": extensions
    }

    output_file = Path(artifact_dir) / "inventory_report.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # --- result ---
    return TaskResult(
        success=True,
        message=f"Scanned {total_files} files",
        artifacts=[str(output_file)]
    )