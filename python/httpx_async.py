"""Async requests through the proxy, with a limit on how many run at once."""
import asyncio
import os

import httpx

host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"
proxy = f"http://{os.environ['LUDAX_USERNAME']}:{os.environ['LUDAX_PASSWORD']}@{host}"
urls = ["https://api.ludaxproxy.com/whoami"] * 5
limit = asyncio.Semaphore(2)


async def fetch(client, url):
    async with limit:
        response = await client.get(url)
        return response.status_code, response.text


async def main():
    async with httpx.AsyncClient(proxy=proxy, timeout=30) as client:
        for result in await asyncio.gather(*(fetch(client, url) for url in urls)):
            print(*result)


asyncio.run(main())
