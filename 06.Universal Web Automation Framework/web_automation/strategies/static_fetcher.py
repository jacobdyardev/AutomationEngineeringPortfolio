import requests
import random


# ----------------------------------------
# USER AGENT POOL
# ----------------------------------------

USER_AGENTS = [
    # Chrome (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Firefox (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) "
    "Gecko/20100101 Firefox/121.0",

    # Safari (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]


# ----------------------------------------
# SESSION FACTORY
# ----------------------------------------

def create_session():
    session = requests.Session()

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    session.headers.update(headers)

    return session


# ----------------------------------------
# FETCHER
# ----------------------------------------

def fetch_static(url: str, config: dict = None, session=None) -> str:

    if session:
        response = session.get(url, timeout=10)
    else:
        session = create_session()
        response = session.get(url, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch page (status {response.status_code})")

    return response.text