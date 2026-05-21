from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import random
import json
import os
from urllib.parse import urlparse


DEFAULT_WAIT_SELECTOR = "[class*='snize-product']"


def _apply_stealth(page):
    # Apply stealth behavior to the page
    stealth_sync(page)


def _warmup_navigation(page):
    # Simulate a more natural entry path before visiting the target page
    page.goto("https://www.drifthq.com/", timeout=30000)
    
    # extra buffer for JS injection
    page.wait_for_timeout(2000)


def _get_proxy(config):
    if not config:
        return None

    proxies = config.get("proxies")
    if not proxies:
        return None

    if config.get("proxy_rotation") == "random":
        return random.choice(proxies)

    return proxies[0]


def _parse_proxy(proxy_value):
    # Supports:
    # http://ip:port
    # http://user:pass@ip:port
    # https://ip:port
    # https://user:pass@ip:port
    if not proxy_value:
        return None

    parsed = urlparse(proxy_value)

    if not parsed.scheme or not parsed.hostname or not parsed.port:
        return None

    proxy_config = {
        "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
    }

    if parsed.username:
        proxy_config["username"] = parsed.username

    if parsed.password:
        proxy_config["password"] = parsed.password

    return proxy_config


def _get_fingerprint():
    # Use real-looking user agents, not placeholder strings
    user_agents = [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    ]

    viewports = [
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 1536, "height": 864},
    ]

    return {
        "user_agent": random.choice(user_agents),
        "viewport": random.choice(viewports),
    }


def _load_cookies(context, config):
    if not config:
        return

    cookies_file = config.get("cookies_file")
    if not cookies_file:
        return

    if not os.path.exists(cookies_file):
        print(f"⚠️ Cookies file not found: {cookies_file}")
        return

    try:
        with open(cookies_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        if isinstance(cookies, list) and cookies:
            context.add_cookies(cookies)
        else:
            print(f"⚠️ Cookies file is empty or invalid: {cookies_file}")

    except Exception as e:
        print(f"⚠️ Failed to load cookies: {e}")


def _wait_for_content(page, config):
    wait_selector = DEFAULT_WAIT_SELECTOR

    if config and config.get("render_wait"):
        wait_selector = config["render_wait"]

    page.wait_for_selector(wait_selector, timeout=15000)


def _simulate_user(page, config):
    if config and config.get("simulate_user", True):
        page.mouse.move(
            random.randint(100, 500),
            random.randint(100, 500),
        )


def _is_blocked(html: str) -> bool:
    html_lower = html.lower()
    return (
        "verify you are human" in html_lower or
        "application error" in html_lower
    )


def _extract_html(page):
    return page.content()


def _run_page_flow(page, url, config):
    _apply_stealth(page)
    _warmup_navigation(page)

    page.goto(url, timeout=30000)

    # initial buffer
    page.wait_for_timeout(2000)

    # trigger Searchanise FIRST
    page.mouse.wheel(0, 3000)
    page.wait_for_timeout(2000)

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    # then wait for products
    _wait_for_content(page, config)

    page.wait_for_function(
        "() => document.querySelectorAll('[class*=\"snize-product\"]').length > 0",
        timeout=15000
    )

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)

    # now wait for products AFTER trigger
    _wait_for_content(page, config)

    _simulate_user(page, config)

    page.wait_for_function(
        "() => document.querySelectorAll('[class*=\"snize-product\"]').length > 0",
        timeout=15000
    )

    return _extract_html(page)


def fetch_stealth(url: str, config: dict = None, context=None) -> str:
    # Session mode: reuse provided browser context
    if context:
        page = context.new_page()
        html = _run_page_flow(page, url, config)

        if _is_blocked(html):
            return html

        return html

    # Standalone mode
    with sync_playwright() as p:
        headless = True
        if config:
            headless = config.get("headless", True)

        proxy_value = _get_proxy(config)
        proxy_config = _parse_proxy(proxy_value)

        launch_args = {}
        if proxy_config:
            launch_args["proxy"] = proxy_config

        browser = p.chromium.launch(
            headless=headless,
            **launch_args
        )

        try:
            fp = _get_fingerprint()

            browser_context = browser.new_context(
                user_agent=fp["user_agent"],
                viewport=fp["viewport"],
                locale="en-US",
                extra_http_headers={
                    "Referer": "https://www.drifthq.com/"
                }
            )

            _load_cookies(browser_context, config)

            page = browser_context.new_page()
            html = _run_page_flow(page, url, config)

            if _is_blocked(html):
                return html

            return html

        finally:
            browser.close()