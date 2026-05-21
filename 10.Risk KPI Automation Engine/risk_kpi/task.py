from pathlib import Path
import json

from automation.core.task_contract import TaskResult  # pyright: ignore
from .loader import load_data
from .evaluator import evaluate_risk


TASK_NAME = "risk_kpi"

PARAM_SPEC = {
    "input_path": {
        "required": True,
        "description": "Path to structured data (mini_etl output)"
    }
}


def run(artifact_dir: Path, params: dict):

    try:
        input_path = Path(params["input_path"])

        data = load_data(input_path)

        results = []

        for record in data:
            risk_result = evaluate_risk(record)
            results.append(risk_result)

        output_file = artifact_dir / "risk_report.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        return TaskResult(
            success=True,
            message=f"Risk analysis completed ({len(results)} records)",
            artifacts=[str(output_file)]
        )

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )