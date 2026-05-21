PIPELINES = {
    "daily_report": [
        {
            "task": "apiaggregator",
            "params": "retries=3"
        },
        {
            "task": "mini_etl",
            "params": None  # will be injected
        },
        {
            "task": "excel_kpi",
            "params": None  # will be injected
        }
    ]
}