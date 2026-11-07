// Node.js fetch through the proxy. Node's built-in fetch needs undici's ProxyAgent for this.
import { ProxyAgent, fetch } from "undici";

const host = `${process.env.LUDAX_HOST ?? "gw.ludaxproxy.com"}:${process.env.LUDAX_PORT ?? "7777"}`;
const token = Buffer.from(`${process.env.LUDAX_USERNAME}:${process.env.LUDAX_PASSWORD}`).toString("base64");
const dispatcher = new ProxyAgent({ uri: `http://${host}`, token: `Basic ${token}` });

const response = await fetch("https://api.ludaxproxy.com/whoami", { dispatcher });
console.log(response.status, await response.text());
await dispatcher.close();
