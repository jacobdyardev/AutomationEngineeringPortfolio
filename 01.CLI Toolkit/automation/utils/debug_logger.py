import json
import time
from pathlib import Path


class DebugLogger:

    def __init__(self, artifact_dir: Path):
        self.artifact_dir = artifact_dir
        self.start_time = time.time()
        self.steps = []

    def log_step_start(self, name, params):
        self.steps.append({
            "task": name,
            "params": params,
            "start": time.time(),
            "status": "RUNNING"
        })

    def log_step_end(self, status, output=None):
        step = self.steps[-1]
        step["end"] = time.time()
        step["duration"] = round(step["end"] - step["start"], 3)
        step["status"] = status

        if output:
            step["output"] = str(output)

    def log_error(self, error):
        step = self.steps[-1]
        step["status"] = "FAILED"
        step["error"] = str(error)

    def save(self):
        trace = {
            "total_duration": round(time.time() - self.start_time, 3),
            "steps": self.steps
        }

        path = self.artifact_dir / "pipeline_trace.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(trace, f, indent=2)