# Recent Builds Archived Before 2026-05-14

## Content Generation Audit + Freshness Gate — 2026-05-07
**What:** Audited JT's content-generation system after daily posts became stale/repetitive, created `memory/content/current-efforts.md`, and patched six content crons with freshness, trend, anti-repeat, and SKIP_SLOT gates.
**For:** internal content system
**Outcome:** Weekly LinkedIn, X, news hook, swipe research, and Reddit generators now must map output to current efforts, prefer sources from the last 14 days, avoid repeating topics/structures from the last 21 days, and skip when inputs are stale.
**Demonstrates:** content ops QA, freshness gating, cron prompt hardening
**Content angle:** A content engine needs a freshness gate more than it needs another prompt.
**Status:** complete

## jtsomwaru.com AI Operations Diagnostic Reposition — 2026-05-05
**What:** Repositioned personal site around AI Operations Diagnostic, ops-heavy business workflows, who-I-help segments, outcome-led services, and updated AI-search metadata.
**For:** JT consulting / warm lead conversion
**Outcome:** Production site now shows updated hero and diagnostic offer; build + lint passed; commit `2d0bb2a` pushed to GitHub.
**Demonstrates:** Positioning, Next.js site updates, AI-search metadata hygiene
**Content angle:** Stop selling AI tools. Sell the workflow diagnostic that tells the buyer what to build first.
**Status:** complete

## jtsomwaru.com AI Operations Blog Library — 2026-05-05
**What:** Added six buyer-intent / AI-search blog assets: AI Operations Diagnostic, family-office automation, local-first AI automation, exception dashboards, AI Implementation Lead vs Consultant, and Diagnostic vs Automation.
**For:** JT consulting / inbound SEO / AI-search citation surface
**Outcome:** 6 new production blog routes live; build + lint passed; commit `143d839` pushed to GitHub.
**Demonstrates:** GEO strategy, buyer-intent content architecture, consulting positioning
**Content angle:** The best AI consulting content teaches the buyer what to build first, not which tool to buy.
**Status:** complete

## Nash Satoshi Methodology SEO Page — 2026-05-07
**What:** Added a public `/methodology` page explaining Nash Satoshi's 4-model crypto game-theory ranking system, linked it from the homepage, and exposed it through sitemap/robots/llms.txt.
**For:** Nash Satoshi / passive-income app distribution
**Outcome:** Production page live; GitHub synced at commit `5473082`; `npm run check` and `npm run build` passed after preserving upstream Aggregation v2 changes.
**Demonstrates:** AI-search/GEO page strategy, product positioning, React/Express deployment hygiene, safe Git rebase around live app functionality
**Content angle:** The methodology page is not just SEO. It gives the model/ranking system a citation-worthy explanation instead of hiding the trust mechanism inside the app.
**Status:** complete

## jtsomwaru.com Vista 1–100 Movie Rating SEO Page — 2026-05-07
- **What:** Added a durable SEO/AI-search blog page for Vista targeting `1–100 movie rating app` and precise movie rating queries.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `npm run build` and `npm run lint` passed locally; committed and pushed to GitHub as `cd7ab18 Add Vista 100-point movie rating SEO page`. Production deploy pending/propagating at first external check.
- **Demonstrates:** App Marketing OS durable discovery loop: metric-backed content insight → SEO brief → implemented page → sitemap/llms exposure.
- **Content angle:** Social winners should become durable search assets, not just more posts.
- **Status:** complete locally and pushed; verify production after Vercel deploy.

## jtsomwaru.com AI Operations Systems Overview — 2026-05-10
- **What:** Added dense “Systems I Build” capability matrix and compact “AI Ops Teardowns” section to the homepage.
- **For:** JT consulting / portfolio site.
- **Outcome:** Homepage now shows operating range faster without adding more full project cards or turning the site into a tool gallery.
- **Demonstrates:** Buyer-facing positioning, AI ops workflow framing, consulting proof packaging.
- **Content angle:** “Don’t show tools; show the operating surfaces buyers feel.”
- **Status:** complete; pushed to GitHub commit `5c163af`, Vercel deploy should auto-trigger.

## jtsomwaru.com StreetEasy Metric Correction — 2026-05-10
- **What:** Tightened homepage client outcome metric from “10+ hrs/week” to “4 hrs / 2 weeks” to match project detail data.
- **For:** JT consulting / portfolio site.
- **Outcome:** Higher trust; site no longer overclaims StreetEasy scraper impact.
- **Demonstrates:** Proof discipline and buyer-facing credibility.
- **Content angle:** Conservative proof beats inflated metrics.
- **Status:** complete; build/lint passed; pushed commit `a164e4b`.

## PM Maintenance Request Triage (n8n)
- **Date added to site:** 2026-03-22
- **What it is:** n8n workflow — tenant submits maintenance request, Claude classifies urgency + category, routes to right vendor, auto-notifies tenant, escalates if vendor goes quiet
- **Demo value:** "The property manager only gets involved when a vendor goes quiet. Everything else runs without them."
- **Stack:** n8n, Claude API, Google Sheets, Webhook
- **Status:** Configurable template, live on jtsomwaru.com
- **URL:** jtsomwaru.com/work/pm-maintenance-triage
- **Content hook:** Exit condition design — when does automation hand off to a human?
