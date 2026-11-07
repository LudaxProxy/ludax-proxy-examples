"""Selenium with Chrome through the proxy.

Chrome cannot take a proxy username and password on the command line, so this
answers the login through Selenium's DevTools connection.
"""
import os

import trio  # installed with selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


def with_proxy_login(driver, username, password, work):
    """Runs work(driver) while Chrome's proxy login is answered."""

    async def main():
        async with driver.bidi_connection() as connection:
            session, devtools = connection.session, connection.devtools
            await session.execute(devtools.fetch.enable(handle_auth_requests=True))

            async def answer_login():
                async for event in session.listen(devtools.fetch.AuthRequired):
                    await session.execute(devtools.fetch.continue_with_auth(
                        event.request_id,
                        devtools.fetch.AuthChallengeResponse("ProvideCredentials", username, password)))

            async def resume_requests():
                async for event in session.listen(devtools.fetch.RequestPaused):
                    await session.execute(devtools.fetch.continue_request(event.request_id))

            async with trio.open_nursery() as nursery:
                nursery.start_soon(answer_login)
                nursery.start_soon(resume_requests)
                result = await trio.to_thread.run_sync(work, driver)
                nursery.cancel_scope.cancel()
        return result

    return trio.run(main)


def work(driver):
    driver.get("https://api.ludaxproxy.com/whoami")
    print(driver.find_element(By.TAG_NAME, "body").text)


host = f"{os.getenv('LUDAX_HOST', 'gw.ludaxproxy.com')}:{os.getenv('LUDAX_PORT', '7777')}"
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument(f"--proxy-server=http://{host}")
driver = webdriver.Chrome(options=options)
try:
    with_proxy_login(driver, os.environ["LUDAX_USERNAME"], os.environ["LUDAX_PASSWORD"], work)
finally:
    driver.quit()
