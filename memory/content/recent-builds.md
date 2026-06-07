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

## Plan Review Pack Skill + Human Signal Workflow - 2026-06-06
**What:** Added `plan-review-pack` plus Client OS, AI Context OS, workflow protocol, proof, product, and video-generation wiring so internal agent plans become human-readable review/proof artifacts.
**For:** internal consulting delivery system
**Outcome:** New skill validated, portable `jt-operating-system` plugin updated/validated with cachebuster `0.2.0+codex.20260606170202`, autoresearch checklist/target added, and Mission Control task `j5728192wnpdjqhzg4bcrryj0x884rm6` created to apply it to the Altmark rent delinquency gate.
**Demonstrates:** agent operating-system design, client proof workflow packaging, human-as-signal delivery loops
**Content angle:** The useful version of human-in-the-loop is not approval on every step; it is a review pack that asks for direction, risk, taste, and acceptance at the exact right point.
**Status:** complete

## Crypto Full Analysis Atomic Pipeline - 2026-06-03
**What:** Added `scripts/run-full-analysis-pipeline.py` and X preflight enforcement inside `generate-full-analysis.py` so the crypto cron runs fetch -> X -> guard -> generate -> validate as one deterministic recovery path.
**For:** internal crypto automation
**Outcome:** Fresh pipeline passed with 25 X entries, X age 0.00h at guard time, validator ok=true for 24 coins and 6 held positions, and `checkpoint: CRYPTO_FULL_ANALYSIS_OK`; cron now calls the pipeline before Telegram delivery.
**Demonstrates:** atomic cron design, stale-evidence prevention, validator-gated delivery
**Content angle:** A deterministic writer is not enough if it trusts stale upstream evidence. The freshness gate belongs inside the writer and the pipeline.
**Status:** complete

## Crypto Full Analysis Deterministic Writer - 2026-06-03
**What:** Added a deterministic writer that converts fresh crypto portfolio, prices, X research, and whale inputs into dated analysis, Telegram summary, history, and allocation artifacts.
**For:** internal crypto automation
**Outcome:** June 3 validator passed for 24 coins, 6 held positions, 25 X entries, and `data/allocation-history/2026-06-03.json`; 6AM cron now calls the writer before Telegram delivery.
**Demonstrates:** cron reliability hardening, validator-gated artifact generation, financial-safety boundaries
**Content angle:** Production agents should not ask a model to remember to write every required artifact when deterministic code can guarantee the handoff.
**Status:** complete

## Altmark Rent Delinquency Testing Pack - 2026-05-27
**What:** Created the rent delinquency acceptance checklist and workflow runbook for sample-report testing, exception routing, human approval, rollback, and production cutover.
**For:** Altmark / client delivery
**Outcome:** Mission Control top task now points to the checklist; Altmark Client OS dashboard, workflow map, weekly update, reusable IP log, and MEMORY.md all reflect the new testing surface.
**Demonstrates:** Paid-client delivery control, property-ops workflow acceptance design, privacy-safe reusable IP capture
**Content angle:** Tenant outreach automation is not a writing problem first. It is a ledger-quality and exception-routing problem.
**Status:** complete


## jtsomwaru.com n8n Automation Service Page — 2026-05-27
**What:** Built `/services/n8n-automation` as a proof-safe n8n automation consulting page with FAQ schema, Service JSON-LD, canonical metadata, sitemap exposure, homepage service links, and llms.txt coverage.
**For:** JT consulting / AI SEO and roundup citation outreach
**Outcome:** Dedicated verifier passed; `npm run build` and `npm run lint` passed; production `/services/n8n-automation` returned HTTP 200 with canonical/schema strings; commits `6243b57` and `7c8c8ec` pushed; updated roundup packet uploaded to Drive.
**Demonstrates:** AI-search/GEO service-page build, proof-safe consulting positioning, Next.js implementation, citation-ready outreach infrastructure
**Content angle:** A service page should be a citation target and sales filter, not a generic list of tools.
**Status:** complete


## App Marketing Share Artifacts Batch 5 — 2026-05-19
**What:** Built Nash Satoshi weekly receipt generator and Glow Index Product Verdict Card MVP as product-led share/acquisition artifacts.
**For:** internal passive-income app marketing
**Outcome:** Nash `/receipts/weekly` added with PNG export and safe caption/source tags; `npm run check` + `npm run build` passed. Glow verdict card embedded on product pages; `npm run build` + `npm run lint` passed with 0 errors and 2 existing image warnings.
**Demonstrates:** product-led growth artifact design, repo-aware AI coding-agent orchestration, claims-safe app marketing implementation
**Content angle:** Cheap app distribution starts with assets users and creators can share, not another generic post.
**Status:** complete


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

## jtsomwaru.com AI Context OS Sprint Service Page — 2026-05-31
- **What:** Added `/services/ai-context-os`, homepage service routing, sitemap/llms/JSON-LD exposure, and an `ai-context-os` delivery skill with reusable sprint template.
- **For:** JT consulting / service packaging.
- **Outcome:** New consulting offer is live at `https://jtsomwaru.com/services/ai-context-os`, packaged as agent-ready operating context plus evals, with one high-priority Mission Control proof task and one completed reusable-template task.
- **Demonstrates:** Offer strategy, AI context engineering, GEO/service-page implementation, reusable consulting IP packaging.
- **Content angle:** The moat is not “knowledge-base cleanup”; it is extracting workflow judgment into context that agents can use and testing whether output quality improves.
- **Status:** complete; build/lint passed; pushed commit `9fc24fd`; production returned HTTP 200.

## AI Ops Teardown Drive Sync — 2026-05-31
- **What:** Added a deterministic Drive sync script for weekly AI Ops Teardown bundles and wired the agent prompt to require Drive links before success.
- **For:** internal consulting proof/content operations.
- **Outcome:** Current lease-renewal teardown and review draft uploaded to organized Drive folders; Mission Control review task now includes both Drive links.
- **Demonstrates:** agent closeout hardening, Drive workflow automation, content-proof organization.
- **Content angle:** A good content agent should leave the review artifact where the human actually reviews it, not buried in local files.
- **Status:** complete; tests passed and proof log recorded.

## jtsomwaru.com Vista 1-100 Movie Rating Landing Page — 2026-06-01
- **What:** Built the exact `/1-100-movie-rating-app` landing page for Vista with direct-answer copy, App Store CTA, iPhone screenshots, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `npm run build`, `npm run lint`, `git diff --check`, local HTTP route check, sitemap check, and llms.txt check passed; commit `f09e09f` pushed to GitHub and production returned HTTP 200 with sitemap/llms.txt updated.
- **Demonstrates:** App Marketing OS durable SEO loop, AI-search/GEO page implementation, product-distribution infrastructure.
- **Content angle:** A winning app-growth artifact should become a crawlable answer page, not just another post.
- **Status:** complete.

## jtsomwaru.com Vista Movie Taste Profile Landing Page — 2026-06-01
- **What:** Built `/movie-taste-profile-app` as Vista's second durable SEO/AI-search landing page with direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `npm run build`, `npm run lint`, `git diff --check`, local rendered route checks, production HTTP 200, production sitemap, production llms.txt, and cross-link checks passed; commit `eb983d3` pushed to GitHub.
- **Demonstrates:** App Marketing OS durable SEO loop, AI-search/GEO product-page compounding, internal-link hygiene.
- **Content angle:** Product SEO compounds when one answer page becomes a cluster, not a standalone orphan.
- **Status:** complete.

## jtsomwaru.com Vista Letterboxd Precise Ratings Landing Page — 2026-06-01
- **What:** Built `/letterboxd-alternative-precise-ratings` as Vista's third durable SEO/AI-search landing page with careful Letterboxd-adjacent positioning, direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `npm run build`, `npm run lint`, `git diff --check`, local rendered route checks, production HTTP 200, production sitemap, production llms.txt, and cross-link checks passed; commits `61ba431` and `6640cbf` pushed to GitHub.
- **Demonstrates:** Guardrailed comparison SEO, AI-search/GEO product-page clustering, product positioning discipline.
- **Content angle:** Competitor-adjacent SEO only works when the page is honest about what the product does and does not do.
- **Status:** complete.

## jtsomwaru.com Vista Private Movie Rating Landing Page — 2026-06-01
- **What:** Built `/private-movie-rating-app` as Vista's fourth durable SEO/AI-search landing page with private personal tracking positioning, direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `npm run lint`, `npm run build`, `git diff --check`, local rendered route checks, production HTTP 200, production sitemap, production llms.txt, and reciprocal cross-link checks passed; commit `f8f8149` pushed to GitHub.
- **Demonstrates:** Privacy-positioned product SEO, AI-search/GEO product-page clustering, unsupported-claim avoidance.
- **Content angle:** Privacy SEO is dangerous if you imply security guarantees; the cleaner wedge is “ratings for yourself before public review pressure.”
- **Status:** complete.

## jtsomwaru.com Vista Rate Movies Out Of 100 Landing Page — 2026-06-01
- **What:** Built `/rate-movies-out-of-100` as Vista's fifth durable SEO/AI-search landing page with 100-point rating-method copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, HowTo schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage.
- **For:** Internal app marketing / Vista durable discovery.
- **Outcome:** `node scripts/verify-vista-rate-movies-page.mjs`, `git diff --check`, `npm run lint`, `npm run build`, production HTTP 200, production sitemap, production llms.txt, and reciprocal Vista cluster-link checks passed; commits `6ff6610`, `5111a61`, and `a24616f` pushed.
- **Demonstrates:** Educational product SEO, AI-search/GEO page clustering, verification hardening after parent review.
- **Content angle:** Method-search pages can convert vague product interest into a specific user action when the page teaches the scoring system before pitching the app.
- **Status:** complete.
