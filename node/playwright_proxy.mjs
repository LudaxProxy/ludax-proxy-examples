// Playwright (Node.js) through the proxy.
import { chromium } from "playwright";

const host = `${process.env.LUDAX_HOST ?? "gw.ludaxproxy.com"}:${process.env.LUDAX_PORT ?? "7777"}`;
const browser = await chromium.launch({
  proxy: {
    server: `http://${host}`,
    username: process.env.LUDAX_USERNAME,
    password: process.env.LUDAX_PASSWORD,
  },
});
const page = await browser.newPage();
await page.goto("https://api.ludaxproxy.com/whoami", { waitUntil: "domcontentloaded" });
console.log(await page.innerText("body"));
await browser.close();
