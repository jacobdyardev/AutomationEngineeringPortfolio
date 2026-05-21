from typing import List, Dict, Any
from bs4 import BeautifulSoup

import time, random

from web_automation.strategies.api_browser_fetcher import fetch_api_browser

from .session_manager import SessionManager
from .strategies.api_fetcher import fetch_api
from .strategies.stealth_fetcher import fetch_stealth
from .strategies.static_fetcher import fetch_static
from .strategies.browser_fetcher import fetch_browser
from .strategies.botasaurus_fetcher import fetch_bota
from .extraction.filters import apply_filters
from .extraction.parser import (
    parse_elements,
    extract_configured
)


def resolve_fetcher(config: dict):

    mode = config.get("mode", "static")

    if mode == "api":
        return fetch_api
    
    if mode == "api_browser":
        return fetch_api_browser

    if mode == "static":
        return fetch_static

    elif mode == "browser":
        return fetch_browser
    
    elif mode == "stealth":
        return fetch_stealth
    
    elif mode == "bota":
        return fetch_bota

    raise RuntimeError(f"Unsupported fetch mode: {mode}")

def fetch_with_fallback(url, config, session=None, session_manager=None):

    # API MODE → just fetch HTML
    if config.get("mode") == "api":
        return fetch_api(config)

    modes = config.get("fallback_modes") or ["static", "browser", "stealth", "bota"]

    last_error = None

    context = None
    if session_manager and any(m in modes for m in ["browser", "stealth", "bota", "api_browser"]):
        context = session_manager.get_browser_context()

    for mode in modes:
        try:
            temp_config = dict(config)
            temp_config["mode"] = mode

            fetcher = resolve_fetcher(temp_config)

            mode = temp_config.get("mode")
            
            if mode == "api":
                data = fetch_api(config)
                return data

            if mode == "static":
                html = fetcher(url, temp_config, session=session)

            elif mode in ["browser", "stealth", "bota"]:
                html = fetcher(url, temp_config, context=context)

            elif mode == "api_browser":
                html = fetcher(url, temp_config, context=context)

            else:
                html = fetcher(url, temp_config)

            if not html:
                continue

            # HANDLE API MODES
            if temp_config.get("mode") in ["api", "api_browser"]:
                return html

            # HTML safety checks
            if isinstance(html, str):
                html_lower = html.lower()

                if "application error" in html_lower:
                    continue

                if "verify you are human" in html_lower:
                    continue

            return html

        except Exception as e:
            last_error = e
            continue

    # All strategies failed
    if last_error:
        raise RuntimeError(f"All fallback modes failed: {last_error}")

    return None

def run_detail_crawl(row: dict, config: dict, session=None, session_manager=None):
    detail_config = config.get("detail")

    if not detail_config or not detail_config.get("enabled"):
        return row

    url_field = detail_config.get("url_field")

    if not url_field or url_field not in row:
        return row

    detail_url = row.get(url_field)

    if not detail_url:
        return row

    html = None

    try:
        # ALWAYS use fallback
        html = fetch_with_fallback(detail_url, config, session=session, session_manager=session_manager)       

        # Final classification
        if html:
            html_lower = html.lower()

            if "application error" in html_lower:
                row["detail_error"] = "client_render_failed"
                return row

            if "verify you are human" in html_lower:
                row["detail_error"] = "captcha_detected"
                return row

    except Exception as e:
        row["detail_error"] = str(e)
        return row  # EXIT EARLY

    # ONLY RUNS IF html IS SAFE
    if not html:
        row["detail_error"] = "no_html_returned"
        return row

    soup = BeautifulSoup(html, "html.parser")
    elements = [soup]

    detail_data = extract_configured(
        elements,
        detail_config.get("fields", []),
        1,
        detail_url
    )

    if detail_data:
        detail_row = dict(detail_data[0])
        detail_row.pop("source", None)
        row.update(detail_row)

    return row


def safe_fetch(fetcher, url, config, session=None):
    for attempt in range(3):
        try:
            return fetcher(url, config, session=session)
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower() or "Too Many Requests" in str(e):
                time.sleep(5 * (attempt + 1))  # backoff
            else:
                raise
    raise RuntimeError("Max retries exceeded")


def run_single_page(config: dict, fetcher, url: str, source_name: str = None, session=None, session_manager=None):

    html = fetch_with_fallback(url, config, session=session, session_manager=session_manager)

    if config.get("mode") in ["api", "api_browser"]:
        data = html  # already JSON

        if not data:
            print("NO API DATA CAPTURED")
            return []

        print("API KEYS:", list(data.keys()))

        mapping = config.get("api_mapping")
        if not mapping:
            return []

        # navigate to root
        root = mapping.get("root", "")
        items = data

        for key in root.split("."):
            if key:
                items = items.get(key, {})

        if not isinstance(items, list):
            return []

        results = []

        for item in items:
            row = {"source": config.get("name")}

            for field_name, path in mapping.get("fields", {}).items():
                value = item
                for p in path.split("."):
                    if isinstance(value, dict):
                        value = value.get(p)
                    else:
                        value = None
                        break

                row[field_name] = value

            results.append(row)

        return results

    #if isinstance(html, str):
        #print(html[:1000])
   #else:
        #print("=== DEBUG API SAMPLE ===")
        #print(str(html)[:1000])

    #with open("debug.html", "w", encoding="utf-8") as f:
        #if isinstance(html, str):
            #f.write(html)
        #else:
            #f.write(str(html))

    elements = parse_elements(html, config["selector"])

    if not elements:
        return []

    limit = config.get("limit")

    if config.get("pagination"):
        limit = None

    data = extract_configured(
        elements,
        config["fields"],
        limit,
        url
    )

    # DETAIL CRAWLING
    detail_config = config.get("detail")

    if detail_config and detail_config.get("enabled"):
        enriched_data = []

        for row in data:
            enriched_row = run_detail_crawl(row, config, session=session, session_manager=session_manager)
            enriched_data.append(enriched_row)

            time.sleep(random.uniform(0.5, 1.5))

        data = enriched_data

    # Inject source if provided
    if source_name:
        for row in data:
            row["source"] = source_name

    data = apply_filters(data, config.get("filters") or [])

    return data


def run_pagination(config: dict, fetcher, source_name: str = None, session=None, session_manager=None):

    pagination = config.get("pagination")

    if not pagination:
        return None

    p_type = pagination.get("type", "page")

    start = pagination.get("start", 1)
    end = pagination.get("end", 1)

    all_data = []

    for i in range(start, end + 1):

        # PAGE TYPE
        if p_type == "page":
            param = pagination.get("param", "page")

            # Case 1: formatted URL
            if "{page}" in config["url"]:
                url = config["url"].format(page=i)

            # Case 2: query param injection
            elif "?" in config["url"]:
                url = f"{config['url']}&{param}={i}"

            else:
                url = f"{config['url']}?{param}={i}"

        # OFFSET TYPE
        elif p_type == "offset":
            step = pagination.get("step", 10)
            start = pagination.get("start", 0)

            offset = i * step

            if "{offset}" in config["url"]:
                url = config["url"].format(offset=offset)
            elif "?" in config["url"]:
                url = f"{config['url']}&offset={offset}"
            else:
                url = f"{config['url']}?offset={offset}"

        else:
            raise RuntimeError(f"Unsupported pagination type: {p_type}")

        data = run_single_page(config, fetcher, url, source_name, session=session, session_manager=session_manager)

        all_data.extend(data)

        delay = config.get("rate_limit_delay", 2)
        jitter = random.uniform(0.5, 1.5)

        time.sleep(delay + jitter)

    return all_data


# Run a single site (internal helper)
def run_site(config: dict) -> List[Dict[str, Any]]:

    session_manager = SessionManager(config)

    try:
        url = config.get("url")
        selector = config.get("selector")
        fields_config = config.get("fields")

        session = session_manager.get_http_session()

        if config.get("mode") not in ["api", "api_browser"]:
            if not url or not selector or not fields_config:
                raise RuntimeError("Site config must include url, selector, and fields")

            if not isinstance(fields_config, list):
                raise RuntimeError("Fields must be a structured list")

        fetcher = resolve_fetcher(config)
        source_name = config.get("name")

        paginated_data = run_pagination(
            config,
            fetcher,
            source_name,
            session=session,
            session_manager=session_manager
        )

        if paginated_data is not None:
            return paginated_data

        return run_single_page(
            config,
            fetcher,
            url,
            source_name,
            session=session,
            session_manager=session_manager
        )

    finally:
        session_manager.close()
        

def run_engine(config: dict) -> List[Dict[str, Any]]:
    # Core orchestration engine

    # MULTI-SITE MODE
    if "sites" in config:

        all_data = []

        for site in config["sites"]:
            site_name = site.get("name", "unknown")

            print(f"\n--- Running site: {site_name} ---")

            try:
                start_time = time.time()

                site_data = run_site(site)

                duration = round(time.time() - start_time, 2)

                if not site_data:
                    print(f"⚠️ {site_name} returned 0 rows ({duration}s)")
                else:
                    print(f"✔ {site_name} → {len(site_data)} rows ({duration}s)")

                all_data.extend(site_data)

            except Exception as e:
                print(f"❌ {site_name} FAILED: {e}")

        return all_data

    # SINGLE-SITE MODE
    else:
        return run_site(config)