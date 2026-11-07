"""One exit IP for several steps: every request sends the same session token.

On a TLS port (9999 or 8081), add -sameip after the time to keep the exit IP too.
"""
import os
import secrets

import requests

host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"
token = secrets.token_hex(4)
password = f"{os.environ['LUDAX_PASSWORD']}-session-{token}-time-10"
proxy = f"http://{os.environ['LUDAX_USERNAME']}:{password}@{host}"

for _ in range(3):
    response = requests.get("https://api.ludaxproxy.com/whoami",
                            proxies={"http": proxy, "https": proxy}, timeout=30)
    print(response.status_code, response.text)
