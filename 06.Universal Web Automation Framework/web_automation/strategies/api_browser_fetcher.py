def fetch_api_browser(url, config, context=None):
    page = context.new_page()

    captured = {}

    def handle_response(response):
        if "searchResult" in response.url:
            try:
                text = response.text()
                import json
                captured["data"] = json.loads(text)
            except Exception as e:
                print("CAPTURE ERROR:", e)

    page.on("response", handle_response)

    page.goto("https://www.idealo.co.uk/cat/16073/graphics-cards.html")
    page.wait_for_timeout(3000)

    # 🔥 Try multiple triggers
    try:
        # Scroll (often triggers lazy load APIs)
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(2000)

        # Try clicking page 2 directly
        page.click("a[href*='pageIndex=1'], button:has-text('2')")
        page.wait_for_event("response", timeout=10000)

    except:
        pass

    page.close()

    return captured.get("data") or {}