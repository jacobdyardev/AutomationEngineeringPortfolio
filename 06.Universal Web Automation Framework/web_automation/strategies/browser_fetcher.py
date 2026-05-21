from playwright.sync_api import sync_playwright


def fetch_browser(url: str, config: dict = None, context=None) -> str:

    # Use existing browser context (session mode)
    if context:
        page = context.new_page()

        page.goto(url, timeout=30000)

        # Cloudflare challenge handling (SAFE)
        try:
            page.wait_for_function(
                "document.title !== 'Just a moment...'",
                timeout=15000
            )
        except:
            pass

        # Ensure DOM is usable
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            pass

        return page.content()

    # fallback to creating a new browser context if not in session mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        page.goto(url, timeout=30000)

        try:
            page.wait_for_function(
                "document.title !== 'Just a moment...'",
                timeout=15000
            )
        except:
            pass

        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            pass

        html = page.content()

        browser.close()

        return html