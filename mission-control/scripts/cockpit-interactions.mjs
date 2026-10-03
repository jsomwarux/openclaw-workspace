// Browser interaction checks for /cockpit against the in-memory fixture backend (no Convex).
// Same setup as scripts/cockpit-screenshots.mjs. Prints one line per check and exits 1 on any failure.
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE ?? "playwright");
const base = process.env.COCKPIT_URL ?? "http://127.0.0.1:3100";
let failures = 0;

async function check(name, fn) {
  try {
    await fn();
    console.log(`PASS ${name}`);
  } catch (error) {
    failures += 1;
    console.log(`FAIL ${name}: ${error.message.split("\n")[0]}`);
  }
}

const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL ?? "chrome" });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, timezoneId: "UTC", locale: "en-US" });
await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: base });

async function open(scenario) {
  const page = await context.newPage();
  await page.goto(`${base}/cockpit?fixture=${scenario}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(900);
  return page;
}
const header = (page) => page.locator("header").first().innerText();
const text = (page) => page.locator("body").innerText();
const expectText = async (page, needle) => {
  await page.waitForTimeout(150);
  const body = (await text(page)).toLowerCase();
  if (!body.includes(needle.toLowerCase())) throw new Error(`missing "${needle}"`);
};
const expectNoText = async (page, needle) => {
  await page.waitForTimeout(150);
  if ((await text(page)).toLowerCase().includes(needle.toLowerCase())) throw new Error(`unexpected "${needle}"`);
};

await check("J and K move between run positions", async () => {
  const page = await open("active");
  await page.keyboard.press("j");
  if (!(await header(page)).includes("7 of 7")) throw new Error("J did not move to 7 of 7");
  await page.keyboard.press("k");
  if (!(await header(page)).includes("6 of 7")) throw new Error("K did not move back to 6 of 7");
  await page.close();
});

await check("C opens the Complete confirm; Enter confirms; Undo restores", async () => {
  const page = await open("active");
  await page.keyboard.press("c");
  await expectText(page, "Mark this item done?");
  await page.keyboard.press("Enter");
  await expectText(page, "Marked done. Press J for the next item.");
  if (!(await header(page)).includes("6 handled")) throw new Error("handled count did not rise");
  await page.getByRole("button", { name: "Undo", exact: true }).click();
  await expectText(page, "Undone. Status is back to Not started.");
  await page.close();
});

await check("D opens Defer with tomorrow 8am selected; Enter defers", async () => {
  const page = await open("active");
  await page.keyboard.press("d");
  await expectText(page, "Defer this item?");
  if (!(await page.getByLabel(/Tomorrow, 8:00 AM/).isChecked())) throw new Error("tomorrow is not pre-selected");
  await page.keyboard.press("Enter");
  await expectText(page, "Deferred until Sun, Oct 4, 08:00 UTC. It leaves today's run.");
  await page.close();
});

await check("Esc cancels a confirm panel and returns focus", async () => {
  const page = await open("active");
  await page.getByRole("button", { name: "Complete C" }).click().catch(async () => page.getByRole("button", { name: /^Complete/ }).first().click());
  await expectText(page, "Mark this item done?");
  await page.keyboard.press("Escape");
  await expectNoText(page, "Mark this item done?");
  const focused = await page.evaluate(() => document.activeElement?.textContent ?? "");
  if (!focused.startsWith("Complete")) throw new Error(`focus went to "${focused}"`);
  await page.close();
});

await check("Q toggles the queue view; Esc closes it; ? opens the shortcuts overlay", async () => {
  const page = await open("active");
  await page.keyboard.press("q");
  await expectText(page, "Order: Curated order.");
  await page.keyboard.press("Escape");
  await expectNoText(page, "No other order is active.");
  await page.keyboard.press("?");
  await expectText(page, "Keyboard shortcuts");
  await page.keyboard.press("Escape");
  await expectNoText(page, "Keyboard shortcuts");
  await page.close();
});

await check("E with no evidence says so", async () => {
  const page = await open("active");
  await page.keyboard.press("e");
  await expectText(page, "Nothing to open: this item has no evidence links.");
  await page.close();
});

await check("Approve has no single key: letters and Enter do nothing on a P card", async () => {
  const page = await open("p-card");
  for (const key of ["a", "A", "r", "R", "Enter", "Shift+Enter", "c", "Control+Enter"]) await page.keyboard.press(key);
  await expectNoText(page, "Approve this item?");
  await expectNoText(page, "Reject this item?");
  await page.close();
});

await check("Approve by Tab and Enter, then Enter confirms; no Undo afterwards", async () => {
  const page = await open("p-card");
  await page.getByRole("button", { name: "Approve", exact: true }).focus();
  await page.keyboard.press("Enter");
  await expectText(page, "Approve this item?");
  await page.keyboard.press("Enter");
  await expectText(page, "Approved. Press J for the next item.");
  if (await page.getByRole("button", { name: "Undo", exact: true }).count()) throw new Error("Undo offered after Approve");
  await page.close();
});

await check("Q card: Save answer validates, saves, then Complete appears", async () => {
  const page = await open("q-card");
  await page.getByRole("button", { name: "Save answer", exact: true }).click();
  await expectText(page, "Enter an answer before saving.");
  await page.getByLabel("Your answer").fill("Go with the second option.");
  await page.getByRole("button", { name: "Save answer", exact: true }).click();
  if (!(await page.getByText("Your answer · Saved", { exact: true }).count())) throw new Error("saved answer label missing");
  await expectText(page, "Answer: Go with the second option.");
  if (!(await page.getByRole("button", { name: /^Complete/ }).count())) throw new Error("Complete did not appear");
  await page.close();
});

await check("Copy prompt copies the exact stored string", async () => {
  const page = await open("active");
  await page.getByRole("button", { name: "Copy prompt", exact: true }).click();
  await expectText(page, "Copied");
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  if (copied.length !== 10533) throw new Error(`copied ${copied.length} characters, expected 10533`);
  await page.close();
});

await check("A failed write shows the failure panel; Retry completes it", async () => {
  const page = await open("failed");
  await page.getByRole("button", { name: "Start", exact: true }).click();
  await expectText(page, "Could not start this item.");
  await page.getByRole("button", { name: "Retry", exact: true }).click();
  await expectText(page, "Started. Status is now In progress.");
  await page.close();
});

await check("Changed underneath me pauses actions until acknowledged", async () => {
  const page = await open("changed");
  await expectText(page, "Actions are paused until you confirm you have read the new version.");
  if (await page.getByRole("button", { name: "Start", exact: true }).count()) throw new Error("Start offered while paused");
  await page.getByRole("button", { name: "I have read the new version" }).click();
  await expectNoText(page, "Changed while you were looking");
  if (!(await page.getByRole("button", { name: "Start", exact: true }).count())) throw new Error("Start not offered after acknowledge");
  await page.close();
});

await check("Stale data pauses every write action", async () => {
  const page = await open("stale");
  await expectText(page, "Actions are paused until this item refreshes.");
  for (const name of ["Start", "Block"]) if (await page.getByRole("button", { name, exact: true }).count()) throw new Error(`${name} offered while stale`);
  await page.keyboard.press("c");
  await expectNoText(page, "Mark this item done?");
  await page.close();
});

await check("Run start: Enter starts the run at item 1", async () => {
  const page = await open("first-load");
  await page.keyboard.press("Enter");
  if (!(await header(page)).includes("1 of 7")) throw new Error("run did not start at 1 of 7");
  await page.close();
});

await check("Resume: acknowledging shows the item you left", async () => {
  const page = await open("resume");
  await page.getByRole("button", { name: "Acknowledge and resume at 6 of 7" }).click();
  if (!(await header(page)).includes("6 of 7")) throw new Error("did not resume at 6 of 7");
  await page.close();
});

await check("Pause run returns to Resume with nothing changed", async () => {
  const page = await open("active");
  await page.getByRole("button", { name: "Pause run", exact: true }).click();
  await expectText(page, "Nothing changed while you were away.");
  await page.close();
});

await check("Summary: Close the run", async () => {
  const page = await open("summary");
  await page.getByRole("button", { name: "Close the run", exact: true }).click();
  await expectText(page, "Run closed for today. The next run starts when you open Mission Control tomorrow.");
  await page.close();
});

await check("No request reaches /api/tasks in fixture mode", async () => {
  const page = await context.newPage();
  const hits = [];
  page.on("request", (request) => { if (request.url().includes("/api/")) hits.push(request.url()); });
  await page.goto(`${base}/cockpit?fixture=active`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.keyboard.press("c");
  await page.keyboard.press("Enter");
  await page.waitForTimeout(300);
  if (hits.length) throw new Error(`requests: ${hits.join(", ")}`);
  await page.close();
});

const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, timezoneId: "UTC", locale: "en-US" });
async function openPhone(scenario) {
  const page = await phone.newPage();
  await page.goto(`${base}/cockpit?fixture=${scenario}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(900);
  return page;
}

await check("Phone: the queue opens as a bottom sheet and closes", async () => {
  const page = await openPhone("active");
  await page.getByRole("button", { name: "Queue", exact: true }).tap();
  if (!(await page.getByRole("dialog", { name: "Queue" }).count())) throw new Error("queue sheet missing");
  await page.getByRole("button", { name: "Close", exact: true }).tap();
  if (await page.getByRole("dialog", { name: "Queue" }).count()) throw new Error("queue sheet still open");
  await page.close();
});

await check("Phone: Complete confirms in a sheet; the bar then offers Next item", async () => {
  const page = await openPhone("active");
  await page.getByRole("button", { name: "Complete", exact: true }).tap();
  const sheet = page.getByRole("alertdialog", { name: "Confirm complete" });
  await sheet.getByRole("button", { name: "Complete", exact: true }).tap();
  await expectText(page, "Marked done. Press J for the next item.");
  await page.getByRole("button", { name: "Next item →", exact: true }).tap();
  await expectText(page, "7 of 7");
  await page.close();
});

await check("Phone: Defer in a sheet with tomorrow pre-selected", async () => {
  const page = await openPhone("active");
  await page.getByRole("button", { name: "Defer", exact: true }).tap();
  const sheet = page.getByRole("alertdialog", { name: "Confirm defer" });
  await sheet.getByRole("button", { name: "Defer", exact: true }).tap();
  await expectText(page, "Deferred until Sun, Oct 4, 08:00 UTC.");
  await page.close();
});

await browser.close();
console.log(failures === 0 ? "ALL PASS" : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
