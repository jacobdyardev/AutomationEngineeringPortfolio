import csv
import json
from pathlib import Path

from automation.core.result import TaskResult


PARAM_SPEC = {
    "path": {
        "required": True,
        "description": "Path to CSV file to process"
    },
    "limit": {
        "required": False,
        "default": 1000,
        "description": "Optional maximum number of rows to process"
    }
}


def run(artifact_dir, params):

    if not params or "path" not in params:
        return TaskResult(
            success=False,
            message="Missing required param: path"
        )

    csv_path = Path(params["path"])

    if not csv_path.exists():
        return TaskResult(
            success=False,
            message=f"CSV file not found: {csv_path}"
        )

    row_count = 0
    sums = {}
    numeric_counts = {}

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            limit = int(params.get("limit", 0))

            for row in reader:

                if limit and row_count == limit:
                    break

                row_count += 1

                for key, value in row.items():

                    try:
                        num = float(value)

                        sums[key] = sums.get(key, 0) + num
                        numeric_counts[key] = numeric_counts.get(key, 0) + 1

                    except:
                        continue

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )

    averages = {
        k: round(sums[k] / numeric_counts[k], 3)
        for k in sums
    }

    report = {
        "file": str(csv_path),
        "row_count": row_count,
        "sums": sums,
        "averages": averages
    }

    output_file = Path(artifact_dir) / "kpi_report.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return TaskResult(
        success=True,
        message=f"Processed {row_count} rows",
        artifacts=[str(output_file)]
    )