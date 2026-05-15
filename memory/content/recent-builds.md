# Recent Builds Log

*Updated automatically when builds complete — by overnight agent (Step 5b) and by Eve in-session when JT confirms a build is done.*
*Read by content-generate as the primary source for Wednesday case studies and build-in-public posts.*
*Entries expire after 30 days — remove stale entries during weekly synthesis.*

## Format

```
## [Build Name] — [YYYY-MM-DD]
**What:** [1-sentence description of what was built]
**For:** [client name, or "internal" for Eve/personal builds]
**Outcome:** [metric, result, or capability unlocked — be specific: "$1,000 project", "runs every 14 days", "replaced 18 hrs/week"]
**Demonstrates:** [skill or capability this proves — e.g., "n8n workflow automation", "Agentforce multi-topic routing", "RAG over external catalog"]
**Content angle:** [suggested post angle for Wednesday LinkedIn or build-in-public X — 1 sentence]
**Status:** [complete | in-progress | review-needed]
```

---

<!-- Entries appended below — most recent first -->


## jtsomwaru.com Public Proof Privacy Pass — 2026-05-14
**What:** Anonymized public client proof copy and removed exact proposal/deal amounts from site proof surfaces while keeping role/city/workflow specificity.
**For:** JT consulting / public credibility + client privacy
**Outcome:** Build + lint passed; pushed commit `11439c7`; production homepage, family-office detail route, and `/llms.txt` verified with no Aya/Altmark/Lady D/exact amount hits.
**Demonstrates:** Public proof hygiene, privacy-safe case-study packaging, attribution correction
**Content angle:** Strong proof does not require naming the client. It requires the workflow, the buyer type, and the operating result.
**Status:** complete


## jtsomwaru.com Client Outcome Attribution Fix — 2026-05-14
**What:** Corrected the site so Aya owns the construction dashboard and StreetEasy pipeline, added Altmark local-first family-office automation as its own client outcome/detail page, and restored Adversight AI under Apps.
**For:** JT consulting / proof accuracy
**Outcome:** Build + lint passed; pushed commit `25b9563`; production `/` and `/work/altmark-local-automation` verified with HTTP 200 and expected content strings.
**Demonstrates:** Proof attribution discipline, client-work packaging, portfolio inventory preservation
**Content angle:** Proof only works if the attribution is precise. Generic labels can hide the actual client story.
**Status:** complete


## jtsomwaru.com Positioning + Roles Update — 2026-05-14
**What:** Reworked the personal site around consulting-first positioning with balanced Work buckets, updated Who I Help niches, cleaner About/tools language, a new `/roles` recruiter path, footer links, and AI-search metadata updates.
**For:** JT consulting / selective recruiting upside
**Outcome:** `npm run build` and `npm run lint` passed; pushed to GitHub commit `fce1480`; production checks returned HTTP 200 for `/` and `/roles` on Vercel.
**Demonstrates:** Consulting positioning, proof-tier hygiene, Next.js implementation, recruiter/buyer path separation, GEO metadata maintenance
**Content angle:** A portfolio site should separate client outcomes, demos, internal systems, and apps without making the real client work look scarce.
**Status:** complete


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

