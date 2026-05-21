import asyncio
import aiohttp
import json
from pathlib import Path
from automation.core.task_contract import TaskResult # type: ignore

TASK_NAME = "api_aggregator"

DEFAULT_APIS = {
    "bitcoin": "https://api.coindesk.com/v1/bpi/currentprice.json",
    "weather": "https://api.open-meteo.com/v1/forecast?latitude=33.75&longitude=-84.39&current_weather=true"
}

PARAM_SPEC = {
    "retries": {
        "required": False,
        "default": 3,
        "description": "Retry attempts per API request"
    },
    "apis": {
        "required": False,
        "description": "Inline API definitions (name:url,name:url)"
    },
    "apis_file": {
        "required": False,
        "description": "Path to JSON file containing API definitions"
    }
}


# // Parse inline API string → dict
def parse_inline_apis(raw: str) -> dict:
    result = {}

    pairs = raw.split(",")

    for pair in pairs:
        name, url = pair.split(":", 1)
        result[name.strip()] = url.strip()

    return result


# // Load APIs from JSON file
def load_apis_from_file(path: str) -> dict:
    with open(path, "r") as f:
        raw = json.load(f)

    # normalize structure
    result = {}

    for name, value in raw.items():
        if isinstance(value, str):
            result[name] = value
        else:
            result[name] = value.get("url")

    return result


# // Resolve API source (priority-based)
def resolve_apis(params: dict) -> dict:

    if "apis" in params:
        print("Using inline APIs")
        return parse_inline_apis(params["apis"])

    if "apis_file" in params:
        print(f"Loading APIs from file: {params['apis_file']}")
        from automation.utils.path_resolver import resolve_path # pyright: ignore[reportMissingImports]

        resolved_path = resolve_path(params["apis_file"], "apis")
        return load_apis_from_file(str(resolved_path))

    print("Using DEFAULT_APIS")
    return DEFAULT_APIS


async def fetch(session, name, url, retries: int):

    for attempt in range(1, retries + 1):

        try:
            print(f"[{name}] attempt {attempt}")

            async with session.get(url, timeout=10) as response:
                data = await response.json()

                print(f"[{name}] success")

                return name, data

        except Exception as e:
            print(f"[{name}] failed attempt {attempt}: {e}")

            if attempt == retries:
                print(f"[{name}] giving up")
                return name, {"error": str(e)}

            await asyncio.sleep(1)


async def run_async(artifact_dir: Path, params: dict):

    results = {}

    retries = int(params.get("retries", 3))

    apis = resolve_apis(params)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch(session, name, url, retries)
            for name, url in apis.items()
        ]

        responses = await asyncio.gather(*tasks)

        for name, data in responses:
            results[name] = data

    output_file = artifact_dir / "aggregated_data.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    success_count = sum(
        1 for r in results.values()
        if "error" not in r
    )

    failure_count = len(results) - success_count

    message = f"{success_count} succeeded, {failure_count} failed."

    if success_count > 0:
        return TaskResult(
            success=True,
            partial=(failure_count > 0),
            message=message
        )
    else:
        return TaskResult(
            success=False,
            message=message
        )


def run(artifact_dir: Path, params: dict):
    return asyncio.run(run_async(artifact_dir, params))