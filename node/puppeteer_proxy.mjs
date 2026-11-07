// Puppeteer through the proxy: the server is a Chrome flag, the login goes through authenticate().
import puppeteer from "puppeteer";

const host = `${process.env.LUDAX_HOST ?? "gw.ludaxproxy.com"}:${process.env.LUDAX_PORT ?? "7777"}`;
const browser = await puppeteer.launch({ args: [`--proxy-server=http://${host}`] });
const page = await browser.newPage();
await page.authenticate({
  username: process.env.LUDAX_USERNAME,
  password: process.env.LUDAX_PASSWORD,
});
await page.goto("https://api.ludaxproxy.com/whoami", { waitUntil: "domcontentloaded" });
console.log(await page.$eval("body", (body) => body.innerText));
await browser.close();
