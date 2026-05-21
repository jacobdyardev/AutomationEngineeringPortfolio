import time
from datetime import datetime
from .pipeline import PIPELINES
from .worker import run_pipeline


def run_scheduler(pipeline_name: str, interval_seconds: int = 60):
    print(f"Scheduler started for pipeline: {pipeline_name}")

    if pipeline_name not in PIPELINES:
        print(f"Unknown pipeline: {pipeline_name}")
        return

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{now}] Running pipeline...")

        exit_code = run_pipeline(PIPELINES[pipeline_name])

        if exit_code == 0:
            print("Pipeline run successful")
        else:
            print("Pipeline run failed")

        print(f"Sleeping for {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)