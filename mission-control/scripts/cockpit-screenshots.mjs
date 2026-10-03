// Screenshots of /cockpit against the in-memory fixture backend, at 1440x900 and 390x844.
// Nothing is installed: point PLAYWRIGHT_MODULE at an existing Playwright package and run a
// dev server with NEXT_PUBLIC_COCKPIT_FIXTURES=1, for example:
//   NEXT_PUBLIC_COCKPIT_FIXTURES=1 NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:9 npx next dev -H 127.0.0.1 -p 3100
//   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright COCKPIT_URL=http://127.0.0.1:3100 node scripts/cockpit-screenshots.mjs <outDir>
// Times show in UTC so they line up with the design prototype's fixture times.
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE ?? "playwright");
const base = process.env.COCKPIT_URL ?? "http://127.0.0.1:3100";
const outDir = process.argv[2] ?? "cockpit-screenshots";
mkdirSync(outDir, { recursive: true });

const LAYOUTS = {
  desktop: { viewport: { width: 1440, height: 900 } },
  mobile: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 },
};

const click = (page, name) => page.getByRole("button", { name, exact: true }).first().click();

/** name, fixture scenario, steps to reach the state. */
const SHOTS = [
  ["01-first-load", "first-load", async () => {}],
  ["02-active-run", "active", async () => {}],
  ["03-queue", "active", async (page, layout) => { await click(page, "Queue"); }],
  ["04-q-card-answer-box", "q-card", async (page) => {
    await page.getByLabel("Your answer").fill("Keep the proposed answer. It matches what the client asked for.");
  }],
  ["05-p-card-approve-confirm", "p-card", async (page) => {
    await click(page, "Approve");
    await page.getByLabel("Note (optional)").fill("Approved as recommended.");
  }],
  ["06-parked-item", "item", async (page) => {
    await click(page, "Block");
    await page.getByLabel("Who are you waiting on").fill("Dana at the landlord's office");
    await page.getByLabel("What are you waiting for").fill("the signed renewal");
    await click(page, "Park it");
  }],
  ["07-deferred-item", "item", async (page) => {
    await click(page, "Defer");
    await page.getByRole("alertdialog", { name: "Confirm defer" }).getByRole("button", { name: "Defer", exact: true }).click();
  }],
  ["08-empty-run", "empty", async () => {}],
  ["09-stale-data", "stale", async () => {}],
  ["10-failed-action", "failed", async (page) => { await click(page, "Start"); }],
  ["11-changed-underneath", "changed", async () => {}],
  ["12-invalid-card", "invalid", async () => {}],
  ["13-expired-card", "expired", async () => {}],
  ["14-run-summary", "summary", async () => {}],
  ["15-resume-change-banner", "resume", async () => {}],
  ["16-degraded-connection", "degraded", async () => {}],
  ["17-loading", "loading", async () => {}],
  ["18-defer-choices", "item", async (page) => { await click(page, "Defer"); }],
  ["19-park-form-errors", "item", async (page) => { await click(page, "Block"); await click(page, "Park it"); }],
  ["20-shortcuts-overlay", "active", async (page, layout) => { if (layout === "desktop") await page.keyboard.press("?"); }],
];

const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL ?? "chrome" });
for (const [layout, options] of Object.entries(LAYOUTS)) {
  const context = await browser.newContext({ ...options, timezoneId: "UTC", locale: "en-US" });
  for (const [name, scenario, steps] of SHOTS) {
    if (name === "20-shortcuts-overlay" && layout === "mobile") continue;
    const page = await context.newPage();
    await page.goto(`${base}/cockpit?fixture=${scenario}`, { waitUntil: "networkidle" });
    // Fixture mode only runs on the development server; hide its floating dev badge.
    await page.addStyleTag({ content: "nextjs-portal { display: none !important; }" });
    await page.waitForTimeout(scenario === "loading" ? 400 : 900);
    await steps(page, layout);
    await page.waitForTimeout(250);
    await page.screenshot({ path: join(outDir, `${name}-${layout}.png`) });
    await page.close();
  }
  await context.close();
}
await browser.close();
console.log(`screenshots written to ${outDir}`);
