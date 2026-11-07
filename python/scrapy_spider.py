"""A Scrapy spider through the proxy. Run with: scrapy runspider python/scrapy_spider.py"""
import os
from urllib.parse import quote

import scrapy

HOST = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"
PROXY = (f"http://{quote(os.environ['LUDAX_USERNAME'], safe='')}:"
         f"{quote(os.environ['LUDAX_PASSWORD'], safe='')}@{HOST}")


class WhoamiSpider(scrapy.Spider):
    name = "whoami"

    async def start(self):
        yield scrapy.Request("https://api.ludaxproxy.com/whoami", meta={"proxy": PROXY})

    def start_requests(self):  # for Scrapy older than 2.13
        yield scrapy.Request("https://api.ludaxproxy.com/whoami", meta={"proxy": PROXY})

    def parse(self, response):
        print(response.status, response.text)
