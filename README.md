# Ludax Proxy examples

Working setup code for [Ludax Proxy](https://ludaxproxy.com) in curl, Python, Node.js, Playwright, Selenium, Puppeteer and Scrapy. Each file stands alone, so you can copy just the one you need.

There is no SDK and no API key. Everything goes through one connection string:

```text
http://USERNAME:PASSWORD@gw.ludaxproxy.com:PORT
```

## Quick start

Get your username and plan password from the [dashboard](https://ludaxproxy.com/dashboard), under **Generate**. Then set them as environment variables:

```bash
export LUDAX_USERNAME="resi-YOUR_ACCOUNT_NAME"
export LUDAX_PASSWORD="YOUR_PLAN_PASSWORD"
```

```powershell
$env:LUDAX_USERNAME = "resi-YOUR_ACCOUNT_NAME"
$env:LUDAX_PASSWORD = "YOUR_PLAN_PASSWORD"
```

Check the connection:

```bash
bash curl/whoami.sh
```

## Examples

| Tool | File | Shows |
| --- | --- | --- |
| curl | [curl/whoami.sh](curl/whoami.sh) | Rotating and sticky requests |
| Requests | [python/requests_rotating.py](python/requests_rotating.py) | A new connection per request |
| Requests | [python/requests_sticky.py](python/requests_sticky.py) | One exit IP for a whole session |
| Requests | [python/requests_tls.py](python/requests_tls.py) | A browser TLS profile on a TLS port |
| HTTPX | [python/httpx_async.py](python/httpx_async.py) | Async requests with limited concurrency |
| Playwright | [python/playwright_proxy.py](python/playwright_proxy.py) | Browser through the proxy |
| Selenium | [python/selenium_proxy.py](python/selenium_proxy.py) | Answering Chrome's proxy login |
| Scrapy | [python/scrapy_spider.py](python/scrapy_spider.py) | A spider with the proxy on each request |
| fetch | [node/fetch_undici.mjs](node/fetch_undici.mjs) | Node.js `fetch` through the proxy |
| Playwright | [node/playwright_proxy.mjs](node/playwright_proxy.mjs) | Browser through the proxy |
| Puppeteer | [node/puppeteer_proxy.mjs](node/puppeteer_proxy.mjs) | Browser through the proxy |

```bash
pip install -r python/requirements.txt
python -m playwright install chromium
python python/requests_rotating.py

cd node && npm install && npx playwright install chromium
node fetch_undici.mjs
```

## Products and ports

The port picks the product. A plan's password works only on its own product's gateway.

| Product | Username prefix | HTTP and HTTPS | SOCKS5 | Browser TLS |
| --- | --- | --- | --- | --- |
| [Residential](https://ludaxproxy.com/products/residential-proxies) | `resi-` | `7777` | `7575` | No |
| [Residential TLS](https://ludaxproxy.com/products/residential-tls-proxies) | `resi-` | `9999` | none | Yes |
| [Residential Premium](https://ludaxproxy.com/products/residential-premium-proxies) | `premi-` | `8080` | `1080` | No |
| [Residential Premium TLS](https://ludaxproxy.com/products/residential-premium-tls-proxies) | `premi-` | `8081` | none | Yes |

The examples default to port `7777`. To use another product, set `LUDAX_PORT`.

## Password options

Routing options go in the password, in this order: session, then location.

```text
YOUR_PLAN_PASSWORD-country-us
YOUR_PLAN_PASSWORD-session-abc123-time-10-country-de
YOUR_PLAN_PASSWORD-session-abc123-time-30-country-us-state-il-city-chicago
```

| Option | Values | Notes |
| --- | --- | --- |
| `-session-<token>` | 3 to 24 characters | Keeps the same exit IP. Leave it out to get a new IP on each connection. |
| `-time-<minutes>` | 1 to 1000 (Premium: at least 3) | Session lifetime. Without it, a session lasts 1 minute. |
| `-sameip` | flag | TLS ports only, right after `-time-`. Keeps the exit IP as well as the browser profile. |
| `-country-<iso2>` | `us`, `de`, `jp` | 137 countries on Residential, 219 on Premium. |
| `-state-<code>`, `-city-<name>` | `il`, `chicago` | Falls back to the country when no exit is free there. |
| `-asn-<number>`, `-os-<device>` | `2516`, `android` | Premium only. |

Full reference: [proxy authentication guide](https://ludaxproxy.com/docs/proxy-authentication).

## TLS ports

On ports `9999` and `8081`, three things differ:

- **Username:** add the header mode and browser profile, such as `resi-YOUR_ACCOUNT_NAME-AE-chrome154`. Use `-AE-auto` to let the gateway pick a profile.
- **Sticky sessions:** add `-sameip` after `-time-`. Without it, the session keeps the browser profile, but the exit IP can change.
- **HTTPS clients:** trust the Ludax CA. Download [`ludax-ca.crt`](https://ludaxproxy.com/downloads/ludax-ca.crt), then set the variable for your client:

| Client | How to trust the CA |
| --- | --- |
| Requests | `REQUESTS_CA_BUNDLE=ludax-ca.crt`, or `verify="ludax-ca.crt"` |
| HTTPX | `SSL_CERT_FILE=ludax-ca.crt` |
| curl | `CURL_CA_BUNDLE=ludax-ca.crt` |
| Node.js fetch | `NODE_EXTRA_CA_CERTS=ludax-ca.crt` |

## Common errors

| Error | Likely cause | What to do |
| --- | --- | --- |
| `407` | Wrong login, or the plan's data is used up or expired | Check the credentials. Do not retry in a loop: 30 failed logins in 5 minutes block your IP for 10 minutes. |
| `502` | The exit dropped or could not reach the site | Retry. Without a session token, the retry gets a new IP. |
| Certificate error on a TLS port | The client does not trust the Ludax CA | Download [`ludax-ca.crt`](https://ludaxproxy.com/downloads/ludax-ca.crt) and pass it to the client. |

More: [Python proxy errors: 407, 403, 429 and 502](https://ludaxproxy.com/blog/python-proxy-errors-407-403-429-502).

## Use it responsibly

Follow each website's terms and our Acceptable Use Policy, linked in the footer of [ludaxproxy.com](https://ludaxproxy.com).

## License

[MIT](LICENSE)
