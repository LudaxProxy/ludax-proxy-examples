"""Playwright (Python) through the proxy."""
import os

from playwright.sync_api import sync_playwright

host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"

with sync_playwright() as p:
    browser = p.chromium.launch(proxy={
        "server": f"http://{host}",
        "username": os.environ["LUDAX_USERNAME"],
        "password": os.environ["LUDAX_PASSWORD"],
    })
    page = browser.new_page()
    page.goto("https://api.ludaxproxy.com/whoami", wait_until="domcontentloaded")
    print(page.inner_text("body"))
    browser.close()
