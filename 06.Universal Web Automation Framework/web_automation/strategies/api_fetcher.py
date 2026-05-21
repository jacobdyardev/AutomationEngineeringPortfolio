import requests


def fetch_api(config: dict):
    api_url = config.get("api_url")
    params = config.get("api_params", {})
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9",

        "Referer": "https://www.idealo.co.uk/cat/16073/graphics-cards.html",
        "Origin": "https://www.idealo.co.uk",

        "Connection": "keep-alive",

        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    if not api_url:
        raise ValueError("Missing api_url in config")

    
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(api_url, params=params, timeout=30)

    print(f"API Status: {response.status_code}")

    if response.status_code != 200:
        return None
    print(response.json())
    return response.json()