# automation/tasks/web_automation/session_manager.py

import requests


class SessionManager:

    def __init__(self, config):
        self.config = config
        self.http_session = None
        self.context = None
        self.browser = None
        self.playwright = None

    # ------------------------
    # HTTP SESSION (existing behavior)
    # ------------------------
    def get_http_session(self):

        if self.http_session:
            return self.http_session

        session_config = self.config.get("session")

        if not session_config or not session_config.get("enabled"):
            return None

        self.http_session = requests.Session()

        headers = session_config.get("headers", {})
        if headers:
            self.http_session.headers.update(headers)

        login = session_config.get("login")

        if login:
            url = login.get("url")
            method = login.get("method", "POST").upper()
            payload = login.get("payload", {})

            if method == "POST":
                res = self.http_session.post(url, data=payload)
            else:
                res = self.http_session.get(url, params=payload)

            if res.status_code != 200:
                raise RuntimeError(f"Login failed: {res.status_code}")

        return self.http_session

    # ------------------------
    # BROWSER SESSION (NEW)
    # ------------------------
    def get_browser_context(self):

        if self.context:
            return self.context

        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright()
        self._playwright_context = self.playwright.__enter__()

        self.browser = self._playwright_context.chromium.launch(headless=True)

        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US"
        )

        return self.context
    

    def close(self):
        if self.browser:
            self.browser.close()
            self.browser = None

        if self.playwright:
            self.playwright.__exit__(None, None, None)
            self.playwright = None