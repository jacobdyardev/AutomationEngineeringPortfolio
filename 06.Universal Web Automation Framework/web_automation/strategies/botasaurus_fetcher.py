from __future__ import annotations
from typing import Any
from botasaurus.browser import browser


@browser(
    headless=False,
    block_images=False,
)
def _run_botasaurus_fetch(driver: Any, data: dict[str, Any]) -> dict[str, Any]:
    # Navigate to the target URL using Botasaurus' browser driver.
    url = data["url"]
    driver.get(url)

    # Wait for a selector when the config provides one.
    render_wait = data.get("render_wait")
    if render_wait:
        driver.wait_for_element(render_wait, timeout=data.get("timeout", 30))

    # Extract rendered HTML.
    # Botasaurus driver APIs can vary slightly by version, so this keeps the
    # fetcher isolated behind one helper.
    html = driver.page_html

    # Extract the title if available.
    title = None
    try:
        title = driver.get_text("title")
    except Exception:
        title = None

    return {
        "url": driver.current_url,
        "html": html,
        "title": title,
    }


# Context intentionally unused.
# Botasaurus should always launch a fresh isolated browser session
# so it never reuses personal cookies or logged-in account state.

def fetch_bota(
    url: str,
    config: dict[str, Any],
    context: Any = None,
) -> str:
    # Validate required input before starting an expensive browser scrape.
    if not url:
        raise ValueError("fetch_bota requires a URL.")

    payload = {
        "url": url,
        "render_wait": config.get("render_wait"),
        "timeout": config.get("timeout", 30),
    }

    raw_result = _run_botasaurus_fetch(payload)

    html = raw_result.get("html", "")

    if not html:
        raise RuntimeError("Botasaurus returned empty HTML.")

    return html