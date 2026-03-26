# Recent Builds Log

*Updated automatically when builds complete — by overnight agent (Step 5b) and by Eve in-session when JT confirms a build is done.*
*Read by content-generate as the primary source for Wednesday case studies and build-in-public posts.*
*Entries expire after 30 days — remove stale entries during weekly synthesis.*

---

## Ensemble Ranking App Factory — 2026-03-23
**What:** Config-driven factory that generates a full multi-LLM ranking app for any niche from a single JSON schema file
**For:** internal / passive income products
**Outcome:** 3 niches (crypto, skincare, colleges) deployed from 1 config schema; new niche scaffolded in minutes
**Demonstrates:** architectural systems thinking, multi-LLM orchestration, passive income product building
**Content angle:** Wednesday LinkedIn — "How I built a product factory so the second niche takes minutes, not weeks"
**Status:** complete
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

## AgentGuard — AI Governance Layer — 2026-03-17
**What:** Production governance middleware for AI agents — confidence scoring routes decisions automatically (≥70%) or to human review (<70%), with full audit trail, override logging, and governance reports. Live demo: HR candidate screening.
**For:** internal (portfolio build — demonstrates enterprise AI governance patterns)
**Outcome:** Live at agentguard-delta.vercel.app, portfolio card on jtsomwaru.com. Demonstrates the trust layer missing from most AI agent deployments.
**Demonstrates:** enterprise AI governance, human-in-the-loop design, confidence-based routing, audit trail architecture, responsible AI deployment patterns
**Content angle:** "Every AI demo shows what it does when it's right. AgentGuard shows what happens when the agent isn't sure — and why that's the thing that decides whether AI goes to production."
**Status:** complete

## Construction Job Tracker — n8n T2 Template — 2026-03-15
**What:** n8n workflow for contractors — foreman sends one WhatsApp/SMS update, Claude classifies job status, client gets auto-notification, owner gets alerted only on blockers
**For:** internal (T2 reusable template for construction/trades prospects)
**Outcome:** Reusable template configurable per prospect in ~2 hours — targets NYC GCs, HVAC, plumbing, electrical. Unlocks T2 pipeline for 5 waiting construction prospects.
**Demonstrates:** n8n workflow automation, Claude AI classification, construction/trades vertical expertise
**Content angle:** "Contractors waste 30-60 min/day calling foremen for status updates. Built a workflow where one WhatsApp message does it all — classification, client update, blocker alert."
**Status:** complete

## PM Maintenance Request Triage — n8n T2 Template — 2026-03-15
**What:** n8n automation for property managers — tenant submits maintenance request, Claude classifies urgency + category, routes to right vendor, sends tenant confirmation, logs everything, escalates no-shows
**For:** internal (T2 reusable template for NYC property management prospects)
**Outcome:** Reusable template for AppFolio/Buildium-using PMs — automates the maintenance triage loop (intake → classify → dispatch → confirm → log → escalate)
**Demonstrates:** n8n workflow automation, Claude AI classification, property management vertical expertise
**Content angle:** "Property managers spend 40% of their day routing maintenance requests. Built a workflow where the tenant submits once and the vendor is dispatched automatically."
**Status:** complete

## StreetEasy Property Scraper — 2026-03-01
**What:** n8n workflow that automatically pulls StreetEasy listings matching custom criteria into a Google Sheet every 14 days
**For:** Aya (NYC real estate firm)
**Outcome:** $1,000 project — replaced a manual biweekly research process
**Demonstrates:** n8n workflow automation, data extraction, scheduled pipelines
**Content angle:** "Real estate firm was spending 3+ hours every two weeks manually pulling listings. Now it runs on a schedule with zero human input."
**Status:** complete

## Construction Progress Tracker — 2026-01-15
**What:** Interactive web app tracking construction progress of a NYC hotel build with milestone logging, photo upload, and stakeholder dashboard
**For:** Aya (NYC real estate firm)
**Outcome:** $1,500 project — replaced manual status update emails and spreadsheet reporting
**Demonstrates:** AI-powered web app development, client-facing dashboards, real estate tech
**Content angle:** "Construction firm was sending weekly status update emails with attached spreadsheets. Replaced that with a live dashboard stakeholders check themselves."
**Status:** complete

## Glow Index Ensemble Engine Rebuild — 2026-03-21
**What:** Rebuilt Glow Index (skincare product rankings app) backend with Python FastAPI + real Brave Search data collection replacing placeholder data. Built 4-LLM ensemble analysis pipeline with verdict banner, key findings panel, model name normalization, and analysis status page. Frontend polished and pushed.
**For:** Glow Index (JT's passive income app — Replit)
**Outcome:** Engine ready for n8n workflow import + ngrok activation — last step before fully live
**Demonstrates:** FastAPI backend, multi-LLM ensemble architecture, real-time data collection pipeline, full-stack web app
**Content angle:** "Rebuilt a skincare rankings app to pull real product data and run it through 4 different AI models simultaneously. Each model scores independently — the verdict is the consensus."
**Status:** complete (n8n import + ngrok pending)

## PM Maintenance Request Triage (n8n)
- **Date added to site:** 2026-03-22
- **What it is:** n8n workflow — tenant submits maintenance request, Claude classifies urgency + category, routes to right vendor, auto-notifies tenant, escalates if vendor goes quiet
- **Demo value:** "The property manager only gets involved when a vendor goes quiet. Everything else runs without them."
- **Stack:** n8n, Claude API, Google Sheets, Webhook
- **Status:** Configurable template, live on jtsomwaru.com
- **URL:** jtsomwaru.com/work/pm-maintenance-triage
- **Content hook:** Exit condition design — when does automation hand off to a human?

## Mission Control Systems Tab — 2026-03-22
**What:** New Systems tab in Mission Control dashboard (localhost:3000/systems) with 8 flow diagrams and dark/light mode toggle
**For:** Internal ops tooling (Mission Control dashboard)
**Outcome:** Visual architecture overview of Eve's 8 core operational systems — accessible at /systems
**Demonstrates:** Next.js dashboard development, flow diagram rendering, dark/light theming
**Status:** complete (internal build — no demo value, skip portfolio)

## Glow Index Engine + Reusable Ensemble Template (2026-03-23)
**What:** FastAPI backend running 4-LLM ensemble (OpenAI o3, Gemini 2.5 Pro, Claude Sonnet 4.6, Grok 4) scoring skincare products simultaneously. Reusable ensemble template extracted from Nash Satoshi architecture — second build took 20% of the time.
**For:** Glow Index (passive income app — skincare rankings)
**Outcome:** Engine complete. Template extracted and reusable across any rankings domain. Pending: n8n import + ngrok activation for live demo.
**Stack:** FastAPI, Python, OpenRouter (4 models), asyncio, structured output schema, n8n HTTP callback
**Content angle:** "Built the same 4-LLM ensemble twice. Second one took 20% of the time — because I extracted the template after the first."
**Status:** engine complete, activation pending (n8n + ngrok step remaining)

## Ensemble Ranking App Factory (2026-03-23)
**What:** Niche config schema, parameterized Next.js template, prompt generator, and new-niche.sh orchestration script. Full factory for spinning up multi-LLM ranking apps in any niche from a single config.
**Tested with:** Colleges config (working frontend in minutes)
**Powers:** Nash Satoshi, Glow Index, and any future ranking product
**Stack:** Next.js (parameterized template), JSON config schema, prompt generator, bash orchestration, OpenRouter (4 models)
**Content angle:** "Stopped building ranking apps. Built the machine that builds them. Third one is almost free."
**Status:** complete

## UI/UX Pipeline Added to Ranking App Factory (2026-03-23)
**What:** uiux-review.sh integrated into new-niche.sh — every new niche now gets an automated UI/UX review pass as part of the generation pipeline. Glow Index improvements backported to template-app.
**Impact:** All future ranking apps inherit the polished Glow Index design system out of the box. Review is mandatory, not optional.
**Status:** complete — factory pipeline now: config → generate → build → uiux-review → verify
