from pathlib import Path
import json

from automation.core.task_contract import TaskResult  # pyright: ignore[reportMissingImports]

from .loader import load_data
from .evaluator import evaluate_rule


TASK_NAME = "data_inspector"


PARAM_SPEC = {
    "input_path": {
        "required": True,
        "description": "Path to JSON data"
    },
    "rule": {
        "required": True,
        "description": "Rule type (exists, threshold, contains)"
    },
    "field": {
        "required": False,
        "description": "Field to evaluate"
    },
    "value": {
        "required": False,
        "description": "Comparison value"
    },
    "ignore_errors": {
        "required": False,
        "default": False,
        "description": "Ignore rows with error field"
    }
}


def run(artifact_dir: Path, params: dict):

    try:
        # ========================
        # PARAM EXTRACTION
        # ========================
        input_path = Path(params["input_path"])
        if not input_path.exists():
            return TaskResult(
                success=False,
                message=f"File not found: {input_path}"
            )
        rule = params["rule"]
        field = params.get("field")
        value = params.get("value")
        original_data = load_data(input_path)
        data = original_data
        ignore_errors = params.get("ignore_errors", False)
        skipped = []        

        print(f"Loading data: {input_path}")

        # ========================
        # LOAD DATA
        # ========================

        if not isinstance(data, list):
            return TaskResult(
                success=False,
                message="Input data must be a list of records"
            )

        if not data:
            return TaskResult(
                success=False,
                message="Input data is empty"
            )
        
        if ignore_errors:
            skipped = [row for row in original_data if "error" in row]
            data = [row for row in original_data if "error" not in row]

        # ========================
        # EVALUATE RULE
        # ========================
        result = evaluate_rule(
            data=data,
            rule=rule,
            field=field,
            value=value,
            original_data=original_data,
            skipped=skipped
        )

        # ========================
        # SAVE OUTPUT
        # ========================
        output_file = artifact_dir / "monitor_output.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        return TaskResult(
            success=True,  # always succeeds unless crash
            message=result.get("message", "Monitoring completed"),
            artifacts=[str(output_file)]
        )
            

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )