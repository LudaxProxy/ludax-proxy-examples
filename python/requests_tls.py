"""A browser TLS profile on a TLS port.

Needs a Residential TLS or Premium TLS plan and the Ludax CA:
curl -O https://ludaxproxy.com/downloads/ludax-ca.crt
"""
import os

import requests

host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '9999')}"
# The username ends with the header mode (AE) and the browser profile.
proxy = f"http://{os.environ['LUDAX_USERNAME']}-AE-chrome154:{os.environ['LUDAX_PASSWORD']}@{host}"

response = requests.get("https://api.ludaxproxy.com/whoami",
                        proxies={"http": proxy, "https": proxy},
                        verify="ludax-ca.crt", timeout=30)
print(response.status_code, response.json()["tls_profile"])
