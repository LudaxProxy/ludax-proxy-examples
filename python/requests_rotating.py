"""Rotating exits with Requests: each call opens a new connection, so it can get a new IP."""
import os

import requests

host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"
proxy = f"http://{os.environ['LUDAX_USERNAME']}:{os.environ['LUDAX_PASSWORD']}@{host}"

for _ in range(3):
    # requests.get() does not reuse the connection. A shared requests.Session() does,
    # and then several requests can leave from the same exit.
    response = requests.get("https://api.ludaxproxy.com/whoami",
                            proxies={"http": proxy, "https": proxy}, timeout=30)
    print(response.status_code, response.text)
