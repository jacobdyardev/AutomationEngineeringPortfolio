PIPELINES = {
    "daily_report": [
        {
            "task": "apiaggregator",
            "params": "retries=3"
        },
        {
            "task": "mini_etl",
            "params": None
        },
        {
            "task": "risk_kpi",
            "params": None
        },
        {
            "task": "excel_kpi",
            "params": None
        }
    ]
}