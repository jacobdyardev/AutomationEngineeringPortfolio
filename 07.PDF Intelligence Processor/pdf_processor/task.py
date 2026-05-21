from pathlib import Path
import json
from automation.core.task_contract import TaskResult  # pyright: ignore[reportMissingImports]
from .loader import load_pdf
from .extractor import extract_text
from .parser import parse_text


TASK_NAME = "pdf_processor"


PARAM_SPEC = {
    "input_path": {
        "required": True,
        "description": "Path to PDF file"
    },
    "mode": {
        "required": False,
        "default": "lines",
        "description": "Parsing mode: text, lines"
    }
}


def run(artifact_dir: Path, params: dict):

    try:
        # ========================
        # PARAM EXTRACTION
        # ========================
        input_path = Path(params["input_path"])
        mode = params.get("mode", "lines")

        if not input_path.exists():
            return TaskResult(
                success=False,
                message=f"File not found: {input_path}"
            )

        print(f"Loading PDF: {input_path}")

        # ========================
        # LOAD + EXTRACT
        # ========================
        pdf = load_pdf(input_path)

        raw_text = extract_text(pdf)

        if not raw_text:
            return TaskResult(
                success=False,
                message="No text extracted from PDF"
            )

        # ========================
        # PARSE
        # ========================
        structured = parse_text(raw_text, mode, source=str(input_path))

        if not structured:
            return TaskResult(
                success=False,
                message="No structured data produced"
            )

        # ========================
        # SAVE OUTPUT
        # ========================
        output_file = artifact_dir / "pdf_output.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured, f, indent=4)

        return TaskResult(
            success=True,
            message=f"Extracted {len(structured)} records from PDF",
            artifacts=[str(output_file)]
        )

    except Exception as e:
        return TaskResult(
            success=False,
            message=str(e)
        )