# MEMORY.md - Long-Term Memory

## JT
- First contact: 2026-02-21 via Telegram
- Named me Eve
- Direct, efficient, low on ceremony — doesn't want hand-holding
- Timezone: America/New_York
- Background: 6 years as Business Systems Analyst @ Spectrum Enterprise/Charter Communications
  - Specialized: product catalog config, cross-team project coordination, system implementations
  - This is his credibility edge — speaks BOTH business operations AND tech
- Full name: Jon Trevor Somwaru | LinkedIn: https://www.linkedin.com/in/jon-trevor-somwaru/ | X: @jts_14 | GitHub: jsomwarux
- Education: Ithaca College, BS Sport Management, Minor Legal Studies, 2014–2018 | Spectrum: June 2019 – August 2025

## File Architecture
- **SOUL.md** — personality, voice, communication style. Eve CAN self-modify.
- **SECURITY.md** — all security boundaries, financial rules, tool restrictions. Eve CANNOT self-modify. Operator-only (JT approval required for any changes).
- **AGENTS.md** — behavioral rules + ALL security rules duplicated here so sub-agents inherit them (sub-agents never load SECURITY.md).
- **TOOLS.md** — paths, configs, API keys, commands. Authoritative for anything technical.
- **MEMORY.md** — personal context, decisions, project status, lessons.

## 🚨 Hard Rules
- **Gateway restarts** — ALWAYS use `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`. NEVER use raw `launchctl`, `openclaw gateway restart`, OR `gateway config.patch`/`gateway config.apply` — all drop JT's connection silently. For config changes: edit `~/.openclaw/openclaw.json` directly, then use restart script. If `pairing required` loop: `openclaw devices list` → `openclaw devices approve <id>`.
- **NEVER write arbitrary keys to `~/.openclaw/openclaw.json`** — invalid keys crash the gateway. External API keys go in TOOLS.md only.

## JT Somwaru Consulting (AI Consulting Agency)
- Target niches: wholesale distribution, property management, construction, insurance operations, skilled trades — all underserved NYC businesses
- Only client so far: Aya (construction progress dashboard, $1,500)
- Bottleneck: client research/outreach + specialized agent configuration
- Outreach plan: email + LinkedIn | Demo strategy: build agents first, then demo to prospects
- Specialized agents — all at `~/projects/` (paths/repos/commands in TOOLS.md):
  - **Research Agent** — researches prospects, identifies automation use case/pain points, determines n8n vs Agentforce fit. Entry point to 5-stage pipeline.
  - **n8n Agent** — builds production-ready n8n workflows for clients. Core JT Somwaru Consulting delivery mechanism. 4-LLM ensemble support.
  - **Agentforce Agent** — builds Salesforce Agentforce agents for clients on SF. Narrower niche, high-value when it fits.
  - **Crypto Agent** — game-theoretic portfolio analysis 3x daily. Serves JT personally, not clients.
  - **Vibe marketing agent** — content + marketing strategies (location TBC, not yet on this machine)
  - **Data visualization agent** — converts spreadsheets to interactive dashboards (location TBC, not yet on this machine)
- **New service (Feb 24):** Cowork Plugin Implementation — build custom Claude Cowork plugins, launch private marketplace, train teams. Industry-specific plugin suites = potential productized offering. Spectrum is a high-value target (JT knows their workflows; pitch as governed AI).

## Consulting Client Research & Outreach Pipeline
5-stage fully automated: Research → Analysis → n8n Build → Presentation → Outreach → **Drive Sync** → JT presses send.
1. **Research Agent** (`~/projects/research-agent/`) — deep-dives prospect, identifies automation opportunity
2. **Analysis Agent** — maps current processes step-by-step, inventories integrations, outputs brief.json
3. **n8n Agent** (`~/projects/n8n-agent/`) — builds custom workflow from the brief
4. **Presentation Agent** — client-facing deck (Google Slides API or PDF first version)
5. **Outreach Agent** — drafts email with presentation attached
- **Key:** Standardize brief.json schema for all agent handoffs — on task board as HIGH priority
- **Google Drive sync:** After deck-built + outreach-drafted, run `python3 scripts/pipeline_drive_sync.py --slug [slug] --client "[name]" --stage all` → creates `Eve — Drafts / JT Somwaru — Client Pipeline / [Client] / Outreach Draft + Presentation Deck`
- **Status:** Building

## Apps Built
- **Vista** — Movie rating + taste profiles. Pending App Store review. Letterboxd competitor with better UI. Profile shows: all-time highest rated, recent highest rated (30 days), favorite performer.
- **Nash Satoshi** — Crypto game theory rankings. 4-LLM ensemble (GPT-5.2, Opus 4.5, Gemini 3 Pro, Grok 4) → consensus analysis. Rankings leaderboard + individual scorecards. GitHub: `jsomwarux/Nash-Satoshi` (private/404 — grant access for ranking-app-agent to ref source code).
  - **4-LLM methodology expansion planned:** skincare rankings, alcohol quality, baby products, college rankings, neighborhood rankings
- **Dynasty fantasy football app** (planned) — AI correlates advanced stats with fantasy production → overall fantasy scores

## LLM Ensemble Ranking App Agent
- **Workspaces:** `~/projects/ranking-app-agent/` (builder) | `~/projects/ui-ux-agent/` (design — NOT run yet)
- **App 1: Glow Index** (skincare rankings) — **STATUS: ✅ Built + deployed to Replit**
  - URL: Replit | GitHub: `jsomwarux/skincare-rankings` | Admin: `/admin?key=glowindex-admin-2024-secret`
  - 100 products seeded in SQLite DB ✅ | 0 analyzed yet (waiting for n8n workflow)
  - Design: deep burgundy (#3D1F2E) + rose gold (#C4956A) + warm cream; Playfair Display headlines
  - 6 scoring dimensions: Ingredient Efficacy 30, Safety Profile 20, Value 20, Transparency 15, Skin Compatibility 10, Sensory 5
  - Scoring grounded in JAAD 2025 Delphi consensus (23 dermatologist-agreed ingredients)
  - Replit secrets set: ADMIN_KEY, N8N_WEBHOOK_URL (placeholder), N8N_CALLBACK_SECRET
  - **Next steps:** Import n8n workflow JSON → get ngrok URL → update N8N_WEBHOOK_URL in Replit → run 3-5 test analyses from admin. Then run ui-ux-agent AFTER test analyses work.
  - ngrok needed to expose local n8n to Replit: `ngrok authtoken + ngrok http 5678`
- **Stack:** Next.js 15 + Prisma/SQLite + shadcn/ui + Recharts | n8n: Stage 1 (4 LLMs independent) → Stage 2 (cross-check consensus)
- **Planned apps:** Alcohol quality, Baby products, College rankings, Neighborhood rankings (for real estate)
- **Architecture:** Shared base engine (port from Nash Satoshi); each app = thin domain layer on top

## jtsomwaru.com Personal Website
- **STATUS: ✅ LIVE** — deployed Feb 24, 2026 ~5:30 PM EST
- URL: https://jtsomwaru.com | Project: `~/projects/jtsomwaru-com/` | Vercel: jsomwarux-yahoocoms-projects/jtsomwaru-com
- Stack: Next.js 16 + Tailwind + Framer Motion → Vercel (iad1) | DNS via GoDaddy
- Sections: Hero, Work (8 projects), Services (3), About (timeline + skill bars), Contact
- Headshot: `~/projects/jtsomwaru-com/public/jt-headshot.jpg`
- **Next step:** Create GitHub repo `jsomwarux/jtsomwaru-com` → connect to Vercel for auto-deploys

## Content / Audience Building
- Main X: @jts_14 — all projects, learning, progress | Crypto X: @jt__crypto — crypto-specific
- Goals: build audience, make connections with similar builders, establish reputation
- Topics: what he's building, lessons, JT Somwaru Consulting thesis, Nash Satoshi methodology, AI tools

## Google Drive Drafts System
- Google account: openclawagenteve14@gmail.com | Root: "Eve — Drafts" in Drive
- Structure: Eve — Drafts / [Project] / [Content Type] (Vista, Nash Satoshi, JT Somwaru Consulting, _Templates)
- Scripts: `~/.openclaw/workspace/scripts/drive_drafts.py` (main) | Auth token: `~/.openclaw/workspace/config/google-oauth-token.json`
- Apps Script: ONE reusable project "Eve — Drive Scripts" — Cmd+A, paste, select function, run. Never create a new project.
- Local drafts: `~/.openclaw/workspace/memory/drafts/`
- **Fully automated:** drive_drafts.py creates Docs directly — zero JT action needed

## Crypto
- Active trader, on-chain focus | Primary income: crypto investments
- Forward bet: x402 protocol — agentic economy on blockchain + stablecoins. Wants to be early builder.
- Interested in agents that can be hired and paid via x402

## Income / Situation
- Primary income: crypto investments | Consulting: $1,500 (Aya dashboard)
- Goal: expand JT Somwaru Consulting, grow app revenue, stay hireable

## Job Market
- Both staying current AND open to opportunities
- Best-fit roles: AI Solutions Architect, AI Implementation Lead, AI Systems Analyst
- Hire pitch: BSA background + AI builder = rare combo employers need
- **NOT a developer** — roles requiring Apex, SFDX, ML engineering, or hands-on coding are auto-disqualified
- Salary: $150K min, $180-220K target | Location: NYC metro or remote only — no relocation
- **Squarespace People AI SA** (scored 19/25, Feb 21, hybrid NYC, $126-180K): JD literally says "vibe-code" — apply this week. Resume + cover letter in Google Drive (Eve — Drafts / JT Somwaru Consulting). Cover letter hook: "You used 'vibe-code solutions' in a JD — that's my methodology."
  - Resume: https://docs.google.com/document/d/12Uow8QM6w15DxaTGuekoQOIdehO66Th4USrhqwYdEyI/edit
  - Cover letter: https://docs.google.com/document/d/1NZeeO2P4AuySixcKA1b-ACTENNb99rUTuUnMt6I3tAk/edit

## Cost Tracking System
- Script: `~/.openclaw/workspace/scripts/cost-tracker.py`
- Daily snapshots: `~/.openclaw/workspace/memory/costs/YYYY-MM-DD.json` (captured nightly at 2 AM via backup.sh)
- Alert thresholds: session >$2 → alert, daily >$10 → alert, monthly pace >$75 → critical alert, monthly goal: $50
- Runaway loop detection: >10 cron runs in 5 min → critical alert
- Alerts checked every 2h via heartbeat cron, immediately sent via Telegram
- Morning brief: includes yesterday's cost breakdown + monthly pace bar
- Sunday brief: includes weekly optimization review with routing suggestions
- Model routing fixes applied 2026-02-25: all isolated agentTurn cron jobs now have explicit model set; Post-Restart Notify → Groq; health report → Groq; job market/niche/synthesis/crypto → Sonnet; Opus no longer runs automatically anywhere

## Setup State
- **Model:** primary `anthropic/claude-sonnet-4-6`, fallback `groq/llama-3.3-70b-versatile` (auto-routes on rate limit)
- **Brave Search, Groq, QMD skill** → all configured ✅ | `~/.bun/bin` in PATH
- **Compaction:** mode=safeguard, reserveTokens=40000, reserveTokensFloor=12000, keepRecentTokens=10000
- **Model routing rules:** documented in AGENTS.md under "Model Routing Rules". Sonnet=default, Groq=lightweight crons/heartbeats, Opus=JT says "go premium". Prompt caching is automatic (Anthropic handles it).
- **Pending API keys:** Claude Haiku 4.5 (same Anthropic key, just enable model)
- **OpenRouter routing rule:** Anthropic models (Opus/Sonnet/Haiku) → ALWAYS direct Anthropic (prompt caching = 90% savings on cached tokens). Everything else (OpenAI, Grok, Gemini, Kimi, DeepSeek, any new model) → OpenRouter. Model IDs use `openrouter/` prefix. See TOOLS.md for full model list and setup steps.
- **Model experiments:** When testing a new model via OpenRouter, log to `memory/costs/model-experiments.jsonl`. Sunday brief includes OpenRouter efficiency check (flags if any model costs >$5/mo = worth getting direct key).

## Health Tracking System
- SQLite at `~/.openclaw/workspace/health/health.sqlite` | CLI: `python3 health.py` from health/ dir
- 9 PM daily: check-in prompt to JT via Telegram | Sunday 9 AM: weekly report via Telegram
- JT's focus areas: muscle tension (neck, traps, shoulders, lower back, hips) + diet optimization
- Full schema + commands in TOOLS.md

## Cron & Heartbeat System
- Jobs written directly to `~/.openclaw/cron/jobs.json` (CLI can't pair with gateway)
- **Isolated agentTurn sessions load ALL workspace files** — if MEMORY.md+AGENTS.md+TOOLS.md are large, context overflow occurs. Use main session systemEvent for jobs that don't need isolation.

### Active Cron Jobs (11)
1. `eve-morning-brief-001` — 7:30 AM daily | **main session** systemEvent | reads tasks.md + niche-monitor-latest.md + job brief
2. `eve-heartbeat-2h-002` — 8,10,12,14,16,18,20,22 EST | **main session** systemEvent
3. `eve-health-checkin-003` — 9 PM daily | main session | sends check-in prompt to JT
4. `eve-health-report-004` — Sunday 9 AM | isolated | runs health.py --report → Telegram
5. `eve-job-market-daily-005` — 6:30 AM daily | isolated | scans jobs → writes to `~/projects/job-market-agent/data/daily-brief.md`
6. `eve-niche-monitor-006` — 9,11,13,15,17 EST Mon–Fri | isolated | Brave search, severity-filtered → `memory/niche-monitor-latest.md`
7. `eve-weekly-synthesis-007` — Sunday 8 AM | isolated | synthesizes week's KB entries → Telegram report
8. `eve-crypto-morning-008` — 6 AM daily | **main session** systemEvent | full portfolio analysis (converted from isolated 2026-02-25 — same overflow fix as morning brief)
9. `eve-crypto-midday-009` — 12 PM daily | isolated | pulse check, silent unless Δ6h >±15%
10. `eve-crypto-evening-010` — 9 PM daily | isolated | end-of-day pulse, alerts only
11. `f18cace3` (Pending Task Processor) — every 30 min, 8AM–10PM EST | main session | processes tasks/pending.jsonl queue

## Session & Backup Automation
- **Cleanup:** `~/.openclaw/workspace/scripts/cleanup-sessions.py` | LaunchAgent `com.openclaw.cleanup-sessions` | 3 AM daily | keeps main + last 24h sessions, prunes orphans
- **Backup:** `~/.openclaw/workspace/scripts/backup.sh` | LaunchAgent `com.openclaw.backup` | 2 AM daily | 7-day retention | Details in TOOLS.md

## Mission Control Dashboard
- Next.js 15 + local Convex backend | Location: `~/.openclaw/workspace/mission-control/`
- LaunchAgents: `com.openclaw.mission-control-convex` (port 3210) + `com.openclaw.mission-control-next` (port 3000) — auto-start on login
- Pages: Overview, Tasks (Kanban), Schedule, Memory, Agents, Monitor, Costs, Audit Trail
- Eve can create tasks via `POST http://localhost:3000/api/tasks`
- Aesthetic: near-black bg, emerald green accent, JetBrains Mono

## Advanced Research Infrastructure
- **x-research skill:** `~/.openclaw/workspace/skills/x-research/` | Token in `~/.config/env/global.env` as X_BEARER_TOKEN | Cost ~$0.50/100 tweets — on-demand only, NOT mass scanning
- **Severity triage** (all research output): 🔴 Critical=act today, 🟠 High=important today, 🟡 Medium=this week (KB only), 🟢 Low=background (KB only). Morning brief: 🔴🟠 only.
- **Niche monitor** (`eve-niche-monitor-006`): writes 🔴🟠 to `memory/niche-monitor-latest.md`, routes 🟡🟢 to KB. 🔴 triggers immediate Telegram.
- **Knowledge Base:** `~/.openclaw/workspace/knowledge/kb.sqlite` | CLI: `bun kb.ts <cmd>` from knowledge/ dir | Full docs in TOOLS.md

## Workspace Template System
- Base templates: `workspace-templates/base/` (AGENTS.md, SECURITY.md, TOOLS.md, SKILLS.md)
- CLAUDE.md template at `workspace-templates/base/CLAUDE.md` — copy to root of every new project

## Active Agents

### Crypto Research & Analysis Agent
- **Location:** `~/projects/crypto-agent/` | **GitHub:** `jsomwarux/crypto-agent` ✅ live
- **Purpose:** Game-theoretic analysis of 10-coin portfolio. 3x daily. Sends condensed recommendations to Telegram.
- **Portfolio source:** Google Sheet ID `1i4wJQ-bpxo25Y9bT04QhKSw3L8xCF7e9ppsyIgDNMio` (TICKER, CONTRACT ADDRESS, WEBSITE)
- **Price data:** Dexscreener API (`fetch-prices.py`) → `data/prices.json` | All 10 coins resolved ✅
- **Website analysis:** `web_fetch` each coin's site from portfolio.json
- **Fallback:** `config/portfolio-fallback.yaml` — all 10 coins with contract + website
- **Cost:** Full analysis ~$0.30-0.40/day | Daily cost limit: $3.00 | X research runs on ALL 10 coins
- **Portfolio coins:** $KELLYCLAUDE, $FELIX, $MLTL, $A0T, $SELFCLAW, $RADR (Solana), $PRXVT, $ANTIHUNTER, $TRIDENT, $NOX
- **Coin Intelligence System:** `data/coin-intelligence/TICKER.md` per coin — ground truth, prevents repeated mistakes
  - **$MLTL:** NOT Moltbook ecosystem — Moltlaunch is standalone agent marketplace (ETH escrow + ERC-8004 identity). Alpha 7/10. ACCUMULATE small.
  - **$KELLYCLAUDE:** Austen Allred's (@Austen) real AI executive assistant. Stack: Clawdbot + Claude Sonnet 4 + PostgreSQL + vectors. App factory (5-subagent pipelines). Thesis: agent revenue flywheel → token captures value. Chain: Base (ERC-20). Re-analyze with "agent earning real revenue" lens.
- **Allocation history:** `data/allocation-history/YYYY-MM-DD.json` — tomorrow's brief compares vs today with change reasons

### Job Market Research Agent
- **Location:** `~/projects/job-market-agent/` | **GitHub:** `jsomwarux/job-market-agent` (pending push)
- **Purpose:** Monitors AI/Salesforce job market, scores opportunities, tracks in-demand skills, generates build-to-learn ideas. Daily brief feeds morning brief.
- **Cron:** `eve-job-market-daily-005` — 6:30 AM daily, isolated, writes to `data/daily-brief.md`
- **Scoring:** 25-point rubric | Target roles: AI Solutions Architect, AI Implementation Lead, Salesforce Agentforce Specialist, AI Systems Analyst
- **Filters:** $150K min, NYC metro or remote, JT is NOT a developer — auto-disqualify roles requiring Apex/SFDX/ML engineering
- **Profile:** `profile/jt-profile.md` | Cron includes: skill gaps, build-to-learn ideas, portfolio suggestions, pre-screened job scan
- **Status:** Live ✅

### Research Agent
- **Location:** `~/projects/research-agent/` | **GitHub:** `jsomwarux/research-agent` (pending push)
- **Purpose:** Researches prospects in 5 target niches, identifies best automation opportunity, determines n8n vs Agentforce fit, outputs structured briefs.
- **Niches:** Wholesale Distribution, Insurance Operations, Construction/Trades, Real Estate Operations, Logistics/Freight
- **Output:** `clients/[name]/brief.json` + `brief.md` → fed to n8n-agent or agentforce-agent
- **State:** Built, committed, pushed ✅ | Full Agentforce layer added | 10 Tier 1 + 10 Tier 2 Agentforce prospects pre-identified
- **Sales playbook:** `knowledge/agentforce-sales-playbook.md`

### n8n Workflow Builder Agent
- **Location:** `~/projects/n8n-agent/` | **GitHub:** `jsomwarux/n8n-agent` ✅
- **Purpose:** Builds n8n workflows for consulting clients. 4-LLM ensemble support.
- **n8n:** running at `http://localhost:5678` ✅ | All 4 LLM credentials connected (Anthropic, OpenAI, Gemini, xAI) ✅
- **LaunchAgent:** `com.openclaw.n8n` (KeepAlive, auto-starts) | API key in `~/.config/env/global.env` + `~/.zshrc`
- **MCP:** `.mcp.json` wired (n8n-mcp + context7) ✅

### Agentforce Development Agent
- **Location:** `~/projects/agentforce-agent/` | **GitHub:** `jsomwarux/agentforce-agent` ✅
- **Purpose:** Builds Salesforce Agentforce agents for clients (topics, actions, Apex, Flows, deploy).
- **State:** Built. Employee Assistant + Ecommerce Service Agent exist. Deep `lessons.md` from real deployments.
- **Pending:** `sf` CLI not installed on Mac mini — `npm install -g @salesforce/cli`, then `sf org login web --alias [name]`
- **Key lesson:** Many steps require Agent Builder UI (M6 = action re-registration after every topic deploy). Full guide: `docs/manual-intervention-guide.md`

## Notes
- `qmd` binary patched to use `bun src/qmd.ts` instead of `node dist/qmd.js` (tsc build broken — missing @types/node)
- Nash Satoshi GitHub (`jsomwarux/Nash-Satoshi`) — private/404; JT needs to grant access for ranking-app-agent to reference source code
- Nash Satoshi 4-LLM model names as stated by JT: GPT-5.2, Opus 4.5, Gemini 3 Pro, Grok 4 (future/internal designations — use as-is)
- Firecrawl API key stored in TOOLS.md (not openclaw.json)
- Glow Index full architecture in `~/projects/ranking-app-agent/CLAUDE.md`
- Prompting guides at `~/.openclaw/workspace/docs/prompting/` — reference before writing any system prompts, cron payloads, or sub-agent task strings

## 2026-05-04 — Stan $40M ARR Distribution Lesson Integrated
JT asked whether the Stan $40M ARR founder post had takeaways worth integrating into his North Star system. Eve integrated the useful operating principle: growth is a sequence of bottleneck shifts, not just motivation. Early stage requires public visibility, manual customer acquisition, founder-level customer service, and success-story flywheels before compounding distribution can work. Updated `memory/north-star/proof-distribution-engine.md`, `memory/north-star/consulting-sales-engine.md`, `memory/north-star/product-growth-manager.md`, and `memory/north-star/revenue-command-center.md` to force weekly reviews to identify the current bottleneck and recommend unsexy/manual distribution or proof actions before more building.

## 2026-05-04 — Dead SaaS → Agent Company Acquisition Thesis Logged
JT shared an X post arguing that dead SaaS products can be acquired and rebuilt as agent-native workflow companies using old customer data, support tickets, churn reasons, and lookalike distribution. Eve treated it as a useful future signal but not an active priority. Created `memory/opportunities/dead-saas-agent-acquisition.md`, added a future signal, and updated North Star product/opportunity gates. The operating rule: validate and score candidates before buying; require legal/data-transfer clarity, support-ticket workflow evidence, distribution path, low maintenance burden, and ≤$5K first experiment unless JT explicitly approves more. Do not let this distract from Altmark, Marketsmith, and consulting cash flow.

## 2026-05-04 — Dynasty Reply Target Freshness Rule
JT corrected that @dynastyjig reply targets were week-old posts and therefore low-engagement. Eve updated `skills/sports-gm/SKILL.md`: daily Dynasty X Replies now require targets ≤24h old, prefer 6-12h, include a freshness line, and fail closed with `BLOCKED: fresh X reply targets unavailable` if fresh X search/API credits are blocked. Cached viable pools are banned for daily engagement replies.

## 2026-05-04 — Nash Satoshi Daily X + Reddit Content Delivery Fixed
JT asked whether daily Nash Satoshi content was optimally generated for both X and Reddit. Audit found X was included in Morning Brief, but Reddit was not part of the daily generation/delivery path. Eve updated `HEARTBEAT.md` Morning Brief to require both 🐦 Daily Nash Satoshi X Post and 👽 Daily Nash Satoshi Reddit Draft, with Reddit as community-native discussion content rather than an X cross-post. Eve also updated cron `eve-morning-brief-001` to read HEARTBEAT.md fresh and explicitly generate both outputs. Timeout set to 240s.
## Recent Strategy Distillations
- 2026-05-02: Strongest near-term consulting language: **AI Workflow Architect for SMB operations** — audit-first, one bottleneck, one controlled worker, one measurable outcome. Draft: `memory/drafts/ai-workflow-architect-post-2026-05-02.md`.
- 2026-05-04: Integrated Stan $40M ARR lesson into North Star OS: weekly reviews now check the top bottleneck and prioritize manual distribution, first-100 service, proof assets, and success-story flywheels before more building. Details archived in `docs/memory/MEMORY-full.md`.
- 2026-05-04: Dead SaaS acquisition thesis saved validation-only; gates in `memory/opportunities/dead-saas-agent-acquisition.md`.
- 2026-05-04: @dynastyjig reply target rule fixed: daily reply packs require posts ≤24h old, prefer 6-12h, fail closed if fresh X unavailable. Cached pools banned.
- 2026-05-04: Nash daily brief now requires X + Reddit-native drafts.
## Archived From MEMORY.md — 2026-06-11

### Consulting Delivery System — Services-as-Software
- New client rule: when JT mentions a new/active/signed client or real paid/discovery engagement, remind him to document rigorously and initialize the Client OS template in the client folder immediately.
- Services-as-software model adopted 2026-05-01: sell finished outcomes, not tools. Manual delivery collects data/edge cases before automation.
- Every active client gets Client OS (`skills/opticfy-ops/templates/client-os/`): dashboard, weekly updates, decision/workflow/failure/automation/metrics/quarterly files, raw/cleaned inputs, tagged outputs.
- Retention: SaaS-like visibility + weekly cadence + quarterly buyer review. Moat: delivery IP/training data before agents/software.
- Offer filter: outsourced line item, intelligence-heavy, services spend > software spend, manually documentable. Two ghosts = targeting/offer signal. Scale delivery before marketing/sales.

### Consulting Niche-Skill Matrix
- Last reviewed 2026-07-01: `memory/research/niche-fitness-2026-07.md`; prior matrix archived at `docs/memory/consulting-niche-skill-matrix-2026-05-01.md`.
- July scores: Property Management / Real Estate Ops 35 primary; Construction & Skilled Trades 31 adjacent expansion; AI Enablement OS / Enterprise Knowledge + Governance 31 adjacent offer layer; Wholesale Distribution 28 hold/test; Home Services / Field Service Ops 28 hold/test; Agentforce/Data Cloud Readiness + Run Control 30 strategic proof lane; P&C Insurance / MGAs 29 strategic proof lane; Manufacturing / Industrial Service Ops 28 hold/test; B2B Commerce / Procurement Ops 27 hold/test; Financial Services / Wealth Management 23 deprioritize.
- July effort: stay PM-first for active n8n GTM; keep construction as a single proof-led adjacent test; hold wholesale/home services; keep Agentforce/Data Cloud readiness and P&C insurance as strategic proof lanes unless Salesforce stack + trigger + reply path are confirmed.

## Current Operating Context Relocated From MEMORY.md - 2026-06-11 Phase 6

> Relocated from `MEMORY.md` during Phase 6 bootstrap reduction. No content was deleted; compact bootstrap file now points here.

# MEMORY.md — Current Operating Context
> Main-session long-term context. Do NOT load in group/shared chats. Full archive: `docs/memory/MEMORY-full.md`; snapshot: `docs/memory/archive/MEMORY-before-optimization-2026-04-26.md`.
> Compact file: durable current context only; history belongs in daily notes/archive.

## JT Snapshot
- Jon Trevor Somwaru, “JT”; timezone America/New_York; Telegram primary; direct, low-ceremony, expects Eve to figure things out before asking.
- Background: Business Systems Analyst at Spectrum Enterprise/Charter; strong business-ops + tech translation edge.
- North Star: buy back control of time by turning practical AI implementation consulting into dependable cash first, then converting delivery proof into reusable IP, products, and AI-managed income streams. Ideal state = bills paid, no debt spiral, money for nice things for him and family, NYC/location stability, and freedom to choose client work, creative apps, crypto research, or rest without every decision being forced by cash pressure.
- Current priority order: (1) collect consulting cash and proof through real client delivery, (2) use proof to build repeatable AI implementation offers and reusable IP, (3) build and market apps only when distribution/retention evidence exists, (4) monitor crypto as opportunity scan, (5) protect health daily as the foundation.
- Income thresholds: safe ≈ $10K/mo, free ≈ $30K/mo, rich ≈ $100K/mo.
- Wants to be known primarily as an AI Implementation Specialist/Consultant and product builder.
- Constraints: not positioning as hands-on developer; avoid Apex/SFDX/ML-engineering roles. Job target: AI Solutions Architect / AI Implementation Lead, $150K min, $180–220K ideal, NYC/remote only. Non-negotiables: sleep, health, and staying in NYC/location stability.

## Hard Rules / Security Essentials
- Never modify `openclaw.json` auth, `summaryModel`, `summaryProvider`, primary model, `auth-profiles.json`, `models.json`, or update OpenClaw without JT approval.
- Never store or paste API keys outside approved auth/env files. Redact secrets in shareable files and Drive uploads.
- 2026-06-18 security fix: app-marketing GA4 OAuth token cache was moved out of `memory/app-marketing/` to `~/.cache/openclaw/app-marketing/ga4-oauth-token-cache.json`; keep credential/cache artifacts outside workspace memory and broad-readable notes.
- Never send messages to third parties on JT’s behalf. Draft, save, and summarize; JT presses send.
- Sacred files are edit-only/append-only: `~/.config/env/global.env`, `~/.openclaw/openclaw.json`, `~/.openclaw/credentials/*`, `memory/content/content-signals.md`.
- If "Preflight compaction required but failed" appears in any form, report the exact error to JT only; do not modify compaction config, restart the gateway, or delete files.
- Use `trash` over `rm` when removing user/workspace files.

## Consulting Positioning
- Brand: JT Somwaru Consulting. Positioning: “practical AI implementation for ops-heavy SMBs” — workflows, AI context systems, dashboards, agents, and integrations that save time or surface revenue.
- Differentiator: JT speaks operations and technology; sells implementation outcomes, not abstract AI strategy.
- 2026-06-03 positioning refinement: lead with AI operating controls / agent-ready operating models, not generic agent adoption. Buyer pain maps to budget ceilings, owner approvals, sandboxed execution, PII rules, run logs, escalation paths, and human-review boundaries before tools are implemented.
- 2026-06-04 positioning refinement: local-business/property-ops agent offers should sell distribution + governed handoffs, not “AI writes copy.” Durable buyer controls: identity, scoped tool access, approval rules, audit trail, kill switch, cost caps, sandboxing, run logs, source-of-truth ownership, and measured adoption/value reporting.
- 2026-06-05/08 positioning refinement: package frontline AI adoption as an operating-model problem before automation. Durable buyer language: trusted customer/workflow context, approval rules, exception owner, system-of-record writeback, and value/KPI measurement. PM Front Desk + Exception Desk is the current buyer-readable proof path: intake source, system of record, approval owner, exception path, review queue, and audit evidence before autonomous action.
- 2026-06-20 package consolidation: stop creating one-off demos per job description or speculative build signal. The durable proof vehicle is an AI Enablement OS offer that packages intake, governance, human-in-the-loop review, evals, adoption, ROI, exception queues, and control records. Current proof ingredients to align: property-ops workflows, OpenClaw operating system, AgentGuard/tool-call governance, and ROIFlow/measurement.
- 2026-06-22 run-control proof refinement: the strongest Altmark/PM proof is the source-export control record before any resident/ledger/legal-sensitive action moves: source row, payment/context gap, risk flag, proposed next step, reviewer, approve/edit/hold/escalate state, and evidence link. Sell as controlled exception handling, not autonomous collections.
- 2026-06-25 AI enablement refinement: job-market signal now supports buyer/employer language around approved tool stack, function playbooks, use-case priority, review owner, value/adoption metric, and final record path. This reinforces AI Enablement OS as the consulting/employment bridge, not a separate demo lane.
- 2026-06-06 agent-ops positioning: “human-as-signal” is stronger than generic human-in-the-loop. Consulting/AI Context OS should frame agents as volume/execution and JT/client leaders as taste, priority, risk boundary, and react-and-redirect loops. Adopted `plan-review-pack` so internal `plan.md`/raw notes become external proof/review artifacts for clients.
- Target ICP: NYC/metro SMBs in construction, wholesale distribution, property management, skilled trades; HubSpot is a strong expansion platform due to less Salesforce competition.
- Outreach tiers use score gates: T1 80+ proof-led custom; T2 60-79 template/validation; T3 40-59 market-sensing only. JT sends all outreach.
- Preferred stack: n8n over Make.com for client automation; Agentforce when Salesforce/Data Cloud fit the client.

## Active Clients
- 2026-06-11 correction: Altmark insurance final 50% and rent delinquency initial 50% have been collected. Rent delinquency is blocked on Yair sending the needed source/export/reviewer/cadence/exception-rule inputs; without that, JT cannot finish the workflow, invoice the remaining payment, or move to the next Altmark workflows. Aya StreetEasy is cancelled and co-living is dead currently; acquisitions remains stalled only.

- 2026-07-16 canonical alignment: authoritative state lives at `memory/canonical/jt-mission-control-state-2026-07-16.md`. MSI / Marketsmith is SIGNED and ACTIVE DELIVERY: 80-hour fixed-scope Nexus engagement, signed value $10,800, invoicing 50% at kickoff and 50% at completion. MSI displacement rule is in effect; new-logo acquisition shrinks to referral packet v1, Yair referral ask at the gate, and at most three warm Tier B/C asks. Governed AI Ops methodology kit trigger fired; write generic-first and keep MSI-specific configs/deliverables out of JT's reusable repo. SoberLife-Coach/Karen is COMPLETE AND PAID, closed-won, removed from cash pipeline, and Karen referral ask is eligible. Aya dashboard is COMPLETE AND PAID, closed-won, removed from cash pipeline, and Gil referral ask is eligible. Ron/Yair potential business is WATCH ITEM ONLY: no jobs, drafts, or builds until named structure, defined economics, and calendar date exist.

- **Karen Vitale / SoberLife-Coach:** complete and paid as of the 2026-07-16 canonical alignment. Remove from active cash pipeline; closed-won. Karen referral ask (Ask 5) is now eligible; JT sends only.
- **Altmark Group:** priority paid client. Dedicated PC installed in office; insurance expiration workflow is live and final 50% paid. Rent delinquency workflow initial 50% paid and remains the top proof/revenue gate. Synthetic dry-run passed 2026-05-29: 8 rows -> 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 tenant-facing drafts from sensitive/cleanup rows. 2026-07-02 execution path: finish setting up Conductor on Beelink, follow Danny's guide, configure everything else needed for the rent delinquency bot, and use Fable for final playbook review before deploy/payment closeout. Keep proof capture privacy-safe; public naming requires accepted client output plus permission/anonymization.
- 2026-06-22 Altmark action order: send/confirm the redacted source-export ask first; it is still the cleanest move toward cash, proof, remaining rent delinquency invoice, and the next Altmark workflow.
- **Aya:** dashboard complete and paid as of the 2026-07-16 canonical alignment; closed-won and removed from active cash pipeline. Gil referral ask (Ask 2) is now eligible. StreetEasy remains cancelled, co-living dead, and acquisitions stalled unless a fresh trigger appears.
- **MSI / Marketsmith:** signed and active delivery as of 2026-07-16. 80-hour fixed-scope engagement for dashboards + agents inside Nexus. Contact: Sam Foy. Signed value: $10,800, invoicing 50% at kickoff and 50% at completion. Current next action: confirm scope, milestones, and invoicing in writing; start Governed AI Ops methodology kit generic-first. Hard IP boundary: generic methodology is JT's; MSI-specific configs/deliverables are MSI's and must never enter JT's reusable repo. Client OS initialized at `memory/clients/marketsmith/`; discovery prep at `memory/clients/marketsmith/discovery-prep-2026-07-01.md`; meeting notes at `memory/clients/marketsmith/meeting-notes-2026-07-02.md`; SOW review at `memory/clients/marketsmith/sow-review-2026-07-06.md`.

## Pipeline / Business Development
- 2026-07-02: Adopted `JT Outbound Operating System v2` from Fable output. It supersedes prior outreach sequencing/contact-scoring rules where conflicts exist: proof claim in M1, property-management email-primary sequence, reachable channel = verified email OR accepted LinkedIn connection, no custom builds/decks/demos pre-reply, 15 new prospects launched/week target, and weekly review starts with sends vs target. Immediate order: baseline historical send/deliverability audit, permission/referral asks, COI proof pack, 40-PM-firm rebuilt list, first 15 launches.
- Active client proof pipeline gate lives at `memory/clients/proof-pipeline-gates.md`: acceptance/payment/scope → evidence capture → permission/anonymization → referral ask → distribution. Do not publish, pitch, ask for referrals, or reuse proof when acceptance/screenshots/metrics/permission are unverified.
- 2026-05-27 outreach strategy reset: LinkedIn warm-up comments are not the default route for new prospects. Use them only for high-fit T1/T2 prospects with recent relevant activity and a concrete M1/follow-up plan within 24-48h. Default prospecting should prioritize proof-led referrals/warm intros, live service pages/citation outreach, buyer-channel validation, and review-only outreach packets.
- 2026-06-02 contact completeness rule: every prospect that clears outreach threshold must include both LinkedIn profile URL and verified email. LinkedIn-only packets are incomplete; create/return the email-finding next step before treating them as send-ready.
- 2026-06-18 outreach reset: next 30 days of new cold outreach are property-management only and artifact-led. Reusable proof-safe PM artifacts may lead M1 when anonymized/synthetic and useful without custom work. First asset is PM Vendor COI / insurance-expiration tracker; first batch is 20-25 NYC/metro PM prospects; keep tiers as effort throttles, not send throttles; no custom demos/decks/client folders before reply; no fourth touch on silence. Control doc: `memory/consulting/pm-artifact-led-outreach-sprint-2026-06-18.md`.
- 2026-06-19 PM COI execution split: Mission Control should show `PM COI wave one: review/send 8 LinkedIn M1s` as JT-owned high-priority, sourced from `memory/consulting/pm-coi-jt-send-checklist-2026-06-18.md` and the controlled-send packet. Eve may expand the next 12-17 buyer routes only after JT handles or explicitly holds wave one. Petri stays as its own M2 connection request; HPM/Superior follow-ups are bundled separately.
- 2026-06-03 NYCB donor list: pass only as 50-name enrichment seed; fail as direct outreach. Never mention donor/NYCB source; keep only contact-complete operating-business buyers.
- 2026-06-02 prospect re-score/contact execution: `memory/consulting/prospect-tier-action-review-2026-06-02.md`. Petri/HPM/Superior are T2 with contact routes captured and JT-owned M2 follow-ups due Jun 4/5 if no reply; weak/no-email T3s are parked; New Yorker is the only possible wholesale limited-test after proof-led M2 window; Guyana Summit is connector/operator validation, not standard sales outreach.
- H.C. Oswald: hold outreach until personal site is polished and demo agents are built.
- Consulting pipeline lives under `~/projects/jt-consulting-pipeline/`; client folders contain research, deck, outreach draft, and pipeline status.
- After deck/outreach stages, sync with `python3 scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage all` and include Drive links for JT review.
- When JT says outreach was sent, same-turn run `scripts/outreach_update.py` with slug/company/message/channel/date; update daily note.

## Consulting Delivery / Niche Matrix
- New/active/signed client or paid/discovery engagement → document rigorously and initialize Client OS immediately. Services-as-software + July niche matrix details are archived in `docs/memory/MEMORY-full.md`; current live focus remains PM-first n8n GTM, construction as adjacent proof-led test, wholesale/home services hold, and Agentforce/Data Cloud proof/readiness only when Salesforce stack + trigger + reply path are confirmed.

## Current Apps / Products
- `jtsomwaru.com`: portfolio/proof site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push. 2026-07-06 positioning correction: homepage is broad AI operations implementation for ops-heavy teams, with proof across dashboards, automation, websites, and internal tools; `/property` remains the focused PM/family-office referral path and Workflow Audit offer. Keep Production Support off-site and measure property kill-loop signals only after JT confirms timer start. Registered dormant kill loops at `memory/consulting/site-conversion-kill-loops-2026-07-03.jsonl`; start them only when JT confirms the shipped site assets. AI SEO uses source-of-truth audits first: context file, surface mismatch, citations/entity, review language, ready-to-hire intent, proof assets, and monthly operator report. No public submissions before JT approval.
- Glow Index: live skincare rankings app at `https://glowindex.co`; 2026-06-18 reset makes it the only ongoing app bet via SEO/GEO money pages and methodology trust anchor. 2026-06-18 crawler root cause was fixed live after commit `329ed72` and production republish: `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/serum` return 200 and `scripts/glow_crawler_check.py` reports `all_clear=true`. First Glow SEO/GEO deploy batch is now live on production from commit `3c60c25` (includes `2fa05cf`): `/rankings/[id]` has explicit `AI skincare analysis` extraction copy, category internal link, and GA4 `view_product.source_tag=glow_seo_product_analysis_20260618`; `/rankings` has canonical metadata, CollectionPage/ItemList/FAQ JSON-LD, explicit AI skincare rankings extraction copy, source tag `glow_seo_rankings_index_20260618`, and `llms.txt` clarifies rankings as the product-analysis discovery hub. Live verification passed on `/rankings`, one `/rankings/[id]` page, and crawler checks. Baseline artifact: `memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md`. Current blocker: GA4 has page/event data, but `customEvent:source_tag` is not queryable until `source_tag` is registered as an event-scoped custom dimension. Next: register source-tag reporting, then run 72h/7d indexing/GA4 checks before another Replit rebuild or `/categories/serum` batch. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; 2026-06-18 reset caps marketing to one weekly human-reviewed research receipt measured by methodology-page clicks/waitlist signups. Kill daily generic cadence.
- Vista: App Store live; durable SEO page live on jtsomwaru.com. 2026-06-18 reset pauses Vista until proven share-to-install loop or consulting reaches $10K/month.
- Action Arena: 2026-07-16 canonical alignment re-gates this lane on 2026-08-15. Cap remains 10 hr/wk; submit by 2026-08-31 or wait for next season. Apple organization conversion is the blocker to clear now, with D-U-N-S in hand. If Apple org conversion is still unresolved at the 2026-08-15 gate, the gate auto-fails and waits for next season.
- 2026-06-27 strategy correction: app survival hinges on distribution + retention, not just stronger product builds. Any new app loop should include niche-native content research, hook/caption/post-format testing, and retention instrumentation as first-class phases before a build is considered viable.
- 2026-07-02 app execution queue: reach back out to Apple; have Fable review app ideas and rank which are best for UGC/paid onboarding; send ideas to Yair and collect his ideas; build playbooks using Fable; implement selected code with Codex/Opus after playbooks exist.

## Content System
- Before drafting: read content voice/profile/evidence corpus; run `scripts/jt_voice_guard.py`; no preamble/em dashes/“Here’s the thing”; X singles 6–15 words. Stop Slop delta 2026-06-07 catches false agency/narrator-distance/vague/Wh/pull-quote/passive slop. LinkedIn now requires proof density + buyer-readable conversion asset when pipeline-oriented. Current PM proof assets: `memory/content/bank/2026-06-08/pm-front-desk-exception-desk-linkedin.md` and `memory/drafts/pm-front-desk-exception-desk-reply-proof-2026-06-08.md`.
- 2026-06-25 review-ready draft: `memory/drafts/linkedin-ai-enablement-approved-tool-stack-2026-06-25.md` passed `JT_VOICE_GUARD_PASS score=100`; angle is AI enablement as approved tool stack, function playbooks, review owner, metric, and final-record path after a team gets access to AI.
- Content niche/source-map rules live in `memory/content/current-niche-map.md` and `docs/memory/current-context-details-2026-05-27.md`; new queues must pass `content_distribution_guard.py --require-reference-map`.
- AI Ops Teardown purpose reset 2026-06-01: teardowns must examine a current company, funding/product/market signal, regulation, or visible buyer problem in a JT-relevant niche, then show the optimal AI workflow JT would build for that company/problem. Strong default spine: current signal → buyer-recognizable bottleneck → concrete messy input scene → system-of-record need → workflow JT would build → cleaner operating outcome. Generic evergreen approval-queue/workflow advice is not enough.
- AI Ops Teardown weekly bundles must auto-upload to Drive via `scripts/ai_ops_teardown_drive_sync.py --json`; teardown docs go to `Consulting/AI Ops Teardowns/[date]/Teardowns`, content drafts to `Content/AI Ops Teardowns/[date]/Drafts`.
- App Marketing/ReelFarm reset and Sports GM/@dynastyjig rules live in `docs/memory/current-context-details-2026-05-27.md` and `docs/memory/sports-gm-content-system-current.md`; Wednesday LinkedIn uses `skills/wednesday-linkedin/SKILL.md`.
- App content loop priority: for each app, create a separate distribution/retention loop that studies the niche's language, values, proof formats, objections, and share triggers; generates unique Claude Design visual/post concepts; tests X and LinkedIn hooks/captions consistently; and ties each content angle to differentiated app value and observed retention behavior.
- Completed work triggers proof points, recent builds, technical angles if useful, content rubric, and Drive upload for substantive deliverables.

## Job Market
- Target only AI implementation / AI Solutions Architect / AI Implementation Lead roles that value BSA + ops automation background.
- Strategic posture as of 2026-05-11: consulting-first, employment selective. Treat job discoveries as hiring-budget/pain signals first, applications second. Route each strong discovery as `apply`, `both`, `consulting-outreach`, or `market-intel`.
- Apply only for exceptional strategic fits (generally 22+/25, $150K+, NYC/remote, low misrepresentation risk). For 18–21/25 roles, usually use the JD as market intel or a consulting lead signal instead of spending time on a resume package.
- If a company is hiring full-time for AI implementation, do not assume they lack consulting interest; position consulting as interim de-risking, workflow mapping, pilot governance, or acceleration while the FTE is hired/ramped — never as “hire JT instead.”
- 2026-05-29 xhigh audit: AI enablement roles now map to AI operating-system proof lanes (intake, connectors/MCP, evals, lineage, governance, adoption, rollback, ROI). `~/projects/job-market-agent/data/role-to-build-matrix.md` is canonical before creating role-derived build/demo tasks; Altmark proof still outranks H.I.G./DealDesk speculation.
- 2026-06-20 job-market strategy: market signal favors operational AI implementation proof over isolated demos. Prune/consolidate active job-market backlog around the packaged AI Enablement OS proof and align website, resume, and outreach around property-ops, OpenClaw, AgentGuard, and ROIFlow.
- 2026-06-25 job-market pulse: PureSpectrum AI Enablement Manager is the cleanest current signal; route as consulting-bridge/intel, not full application package. Useful vocabulary: AI Academy, approved tool stack, function playbooks, prompt libraries, AI project portfolio, adoption metrics, and ROI.
- 2026-06-02 through 2026-06-08 job-market pulses: no qualifying US/NYC/remote roles cleared filter. Useful positioning signal: AI adoption operating-system / target-operating-model work before implementation: frontline workflow discovery, readiness audits, intake, use-case triage, governance, HITL boundaries, adoption metrics, ROI/KPI dashboards, process ownership, champions, and business-as-usual integration.
- Avoid pure software engineering, ML research, Apex/SFDX-heavy Salesforce developer, relocation, or sub-$150K roles.
- Resume/cover letter packages must use Sonnet model via job-application skill; save local markdown + generate docx + upload to Drive.

## Crypto / Finance
- Crypto is JT’s primary income stream. x402 is a forward bet.
- Financial safety: never trade, transfer, spend, or execute financial transactions. Conway constraints: max $5/action, max 2 VMs, wallet <$10 means do not spend.
- Morning crypto cron and Nash Satoshi ranking content are operationally important; missed critical crons should be detected/fired per HEARTBEAT rules.

## Infrastructure / OpenClaw State
- OpenRouter cost-gated. Main/default routing + all cron payloads use OpenAI OAuth with no non-OpenAI fallbacks; OpenRouter/Opus require named JT approval. Regression guard: `python3 scripts/model_routing_guard.py --include-disabled`.
- Google Drive OAuth may block Drive-dependent pipeline work; if uploads fail, JT needs to run `python3 ~/.openclaw/workspace/scripts/drive_auth.py`.
- LCM/lossless-claw is active; use `lcm_grep` → `lcm_describe` → `lcm_expand_query` for prior conversation recall before asserting specifics.
- Fresh web search: use `scripts/web_search.py` direct Brave API for freshness/date filters; managed `web_search` only for broad non-freshness lookups. Do not configure Brave plugin/provider without approval.
- Gateway restart path: prefer `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`; do not raw restart/config patch unless explicitly approved.
- 2026-06-11 Phase 2A/Finding 1 follow-up: audio input now auto-detects language (`tools.media.audio.language` removed); prior LCM DB backed up at `~/.openclaw/lcm.db.backup-20260611` and live `lcm.db` reset fresh. Moonshot fallback remains unapplied because `openclaw models status` reports `moonshot:default` as `disabled:billing 2h`, and gateway logs show Moonshot 429 insufficient-balance/account-suspended errors. JT-side action: recharge/reactivate Moonshot billing, then rerun one throwaway `moonshot/kimi-k2.6` smoke and apply Phase 2A fallback unchanged. If not using Moonshot, approved alternative is OpenRouter Gemini Flash class after smoke with $5/month fallback cap and $3 alert. Baseline delivery was 48/76 delivered (63.2%); recompute 7 days after fallback lands with `python3 scripts/recompute_delivery_rate.py --days 7 --label fallback-plus-7 --json`.
- 2026-06-11 Follow-up E: initial cron-runtime Sonnet preflight rejected `openrouter/anthropic/claude-sonnet-4-6`; JT pre-approved the exact Hard Rule 1 exception, so only that model was added to `agents.defaults.models` using existing OpenRouter credentials and gateway restarted via `scripts/restart-gateway.sh`. Rerun returned `SONNET_PREFLIGHT_OK`; approved content jobs remain the only Sonnet cron overrides. Moonshot fallback is still not live.
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`. 2026-06-16 Slice 1.1: mobile nav centered/safe-area-aware; `/consulting` is the live Revenue cash-path cockpit backed by North Star, pipeline, and task data; old consulting strategy screen is preserved at `/legacy/consulting`.
- Critical commands/paths: `TOOLS.md`.

## Active Automation / Crons
- 2026-07-08 Phase 4: created `memory/job-state/claims/`, `memory/job-state/archive/`, and 12 survivor job state files from `memory/job-state/TEMPLATE.md`; proof id `13cb69f0`.
- 2026-07-08 migration lane: after JT approval, disabled 33 deprecated cron jobs without deletion; `eve-morning-brief-001` was renamed from Morning Brief to Daily Send Sheet; Friday Scoreboard was created as `18169759-7450-4e06-8db0-e0d14fbc25fd`; live count verified as 12 enabled / 60 disabled / 72 total. Approved jobs now enabled: Daily Send Sheet, Friday Scoreboard, outreach-pipeline, Pending Task Processor, prospect-discovery, Weekly Systems Review, weekly-unemployment-cert, Health Check-in, and four passive-income Engine B Stage 1 jobs. Daily Send Sheet stays `30 7 * * * America/New_York`; Friday Scoreboard runs `0 16 * * 5 America/New_York`; both are isolated, Telegram announce to `6608544825`.
- Cron volume is guarded by `scripts/cron_volume_guard.py`: ≤35 scheduled invocations/day average and ≤28 agentTurn/day average; >30/day warns. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM ET.
- `critical-files-integrity` (`ee357abb`) runs daily 9AM ET, timeout 180s; run script first, inspect/edit only on non-zero exit.
- Active cron count: 44 enabled as of 2026-06-25 after the one-off YouTube TV reminder fired and was confirmed complete by JT. Evening Digest (`evening-digest-001`) runs daily 7PM ET from `memory/digest-queue.md`; 2PM TikTok warm-up queues to digest, redundant 7:45PM TikTok warm-up is disabled, and Morning Brief opens with a capped 3-item SEND QUEUE. Phase 7 disabled the old 9:45PM `nightly-autonomous-leverage-agent` and 3:20AM `Overnight Autonomy Agent`, replacing them with `Night Autonomy Agent` (`f146d8b8-94e0-49ff-8e4a-5050a284e894`) at 11PM ET. Phase 1 removed 12 disabled zombie jobs and saved baseline delivery metric at `docs/audits/baseline-delivery-2026-06-11.md`.
- 2026-06-25 heartbeat state: cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown enabled schedules. Direct cron list remains null-heavy with stale `status:error`/null-metadata rows for `Job Market Daily Research`, `Viral Post Swipe File - X Research`, `Job Application Auto-Builder`, `Niche Intelligence Monitor`, `Daily News Hook`, `prospect-discovery`, `Weekly Systems Review`, and `content-generate-x`; verify run history/artifacts before alerting, editing, or rerunning. Duplicate `lossless-claw` plugin warning persists.
- `critical-files-integrity` now invokes `scripts/cron_snapshot.py`, which snapshots `/Users/jtsomwaru/.openclaw/cron/jobs.json` into `config/cron-snapshots/jobs-YYYY-MM-DD.json` and commits the snapshot when changed.
- Responsibilities: morning brief/send queue, evening digest, job market, niche monitor, crypto, content, App Marketing/ReelFarm, North Star, cost, health, passive-income pipeline. Sports GM/dynasty content automation is disabled as of 2026-06-16 unless JT explicitly re-enables it. Heartbeat cron disabled 2026-05-17 at JT request.
- Recent cron hardening/details live in `docs/memory/current-context-details-2026-05-27.md` plus daily notes. Do not rerun content/reporting crons solely to clear metadata.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- 2026-06-22 health check-in state: fallback-mask recurrence was repaired after JT approved proceeding. Added deterministic helper `scripts/health_checkin_cron.py` plus `scripts/test_health_checkin_cron.py`, converted Health Check-in cron `6be7f564-5cec-47e7-b67c-9b2fcc3ed8de` from isolated `agentTurn` to main-session `systemEvent`, and verified local duplicate-skip for 2026-06-22. The manual system-event test left `runningAtMs` stuck; approved restart path `scripts/restart-gateway.sh "clear stuck Health Check-in cron runningAtMs after cron repair"` cleared live scheduler state. Mission Control task `j572zr0zcfky50mj8cjqg045c5897xhy` closed. Next live verification: 2026-06-23 21:00 ET.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75; `--check-alerts` includes model-routing guard.
- Kobe Protocol: daily film review at 10AM and weekly skills audit.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- Current strategy: contained SMB ops bottleneck audits/prototypes; practical AI implementation for ops-heavy SMBs; prioritize B2B consultable products/client proof. App-growth next moves: Action Arena submission gate, Glow crawler/SEO money pages, Nash weekly receipt cap, Vista hold.

## Integrity / Fabrication Corrections
- Never claim outreach/messages were sent unless tool/script evidence confirms it.
- Never fabricate URLs, deployment state, GitHub status, Drive links, or task closure. Verify with tools.
- If corrected by JT, immediately update the Mistakes Log/rules before moving on.
- External strategy prompts, including Claude Fable prompts, must assume the outside model has zero prior JT-project context. If a prompt asks the model to evaluate a named app, project, client, or proof asset, include a compact primer covering what it is, current status, revenue/proof state, growth hypothesis, constraints, and risk before asking for allocation or sequencing decisions.

## Setup State
- 2026-05-31/06-06: Added AI Context OS/plan-review/proof skills, workflow/product agents, and `~/plugins/jt-operating-system` v0.2.0.
- 2026-05-11: GBrain consulting recall pilot lives at `~/projects/gbrain*`; use only `scripts/gbrain-consulting-search.sh "Entity"` for consulting/prospect entity lookup. No crons/skillpacks/broad ingestion/embeddings without JT approval.

## Automation / Live Opportunities
- Automation/client/opportunity history archived at `docs/memory/automation-and-live-opportunities-archive-2026-05-10.md`.
- Current must-remember: Altmark rent delinquency is the top consulting/proof lane. Internal proof/content tasks stay medium until evidence/send paths are ready. Yair may refer ~15 NYC family offices, proof/referral use gated.
- Guyana wedge: Local Content Operations Sprint for oil/gas-adjacent suppliers. Dad-forward/warm-intro language should emphasize supplier ops/admin drag, vendor records, bid readiness, and local-content evidence. Hidden/noindex `jtsomwaru.com/guyana` remains stale until rewritten.
- Nightly leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.

## 2026-06-26 Heartbeat Memory Maintenance
- 08:13 market lane: added PM/Altmark research addendum translating Salesforce Agentforce Help Agent pay-per-resolution, OpenAI Codex work-data, and Salesforce Open Discovery/ARD into the Altmark resolution-ledger proof frame. Strongest PM proof remains source row/export, allowed data/action scope, context gap, proposed resolution, reviewer, approve/edit/hold/escalate state, evidence link, and outcome event.
- 09:13 AI-tool lane: appended AI Tool Monitoring note. Agent infrastructure signal is moving toward discoverable capability registries plus outcome accounting. Run Control / AI Enablement OS should show registered capability, owner, allowed tools/data, completion definition, escalation state, approval, and replayable proof.
- 10:15 crypto/film lane: 10AM missed-cron gate passed. Crypto Full Analysis, Outreach Pipeline, and Critical-files integrity all had same-day run evidence. Film review added Health Check-in regression guidance: do not accept instruction-payload cron summaries as proof; require deterministic helper status such as `SKIPPED_DUPLICATE_HEALTH_CHECKIN` or `HEALTH_CHECKIN_SENT`.
- 11:34 job-market lane: no new qualifying NYC/remote non-coding AI implementation role. Anthropic Claude Code/Endor Labs signals were developer/partner-integration false positives. Positioning remains business-side AI operating-system proof over developer-advocate proof.
- 12:13 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-property-management-resolution-ledger-2026-06-26.md`; `jt_voice_guard` passed score 100. Angle: property-management AI should get credit only when the approved next step is logged, the exception leaves the queue, and evidence is attached to the source record.
- 13:13 memory lane: compacted `MEMORY.md` under advisory while keeping Jun 26 details here. Current operational baseline: Mission Control 272 total / 261 active / 11 high / 0 overdue; cost alerts empty; Spanish paused; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron scan has no current red rows; stale list-metadata rows are `prospect-discovery`, `Weekly Systems Review`, and `content-generate-x`; duplicate `lossless-claw` warning persists.

## 2026-06-27 Heartbeat Memory Maintenance
- 08:13 market lane: appended PM Exception Desk research addendum. PM AI buyer language keeps converging on permissions, approval rules, audit trails, human overrides, and pre-execution controls for collections/compliance workflows. Altmark proof should lead with a rent-delinquency resolution ledger: source row, allowed scope, context/payment gap, proposed next step, policy/rule applied, reviewer, approve/edit/hold/escalate state, evidence link, and outcome event.
- 09:13 AI-tool lane: appended AI Tool Monitoring note. Governance signal narrowed toward on-behalf-of authorization, gateway allow/reject evidence, identity federation/OBO token propagation/RBAC/audit logs/SSO/SCIM, and enforcement records. Run Control proof should show who/what acted, on whose behalf, requested scope, policy evaluation, allow/reject/approval outcome, replayable log location, owner, budget/rate boundary, delivery proof, and recovery owner.
- 10:13 crypto/film lane: 10AM missed-cron gate passed after retrying Outreach Pipeline with full UUID `651fa1da-84d7-44b3-8e10-6a46e1c05cf6`. Updated heartbeat extended rules, regression checks, and training log so short cron ids do not cause false missed-cron alerts. Crypto monitoring used same-day artifacts only; research/ranking only, no trades/swaps/wallet actions/transfers/payment-MCP/x402 experiments.
- 11:34 job-market lane: no new qualifying role passed filters. Atmosera Principal Consultant AI is market-intel only; it reinforces AI CoE/governance/ROI operating-model proof while failing ML/cloud-architecture hard filters.
- 12:15 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-ai-coe-run-control-2026-06-27.md`; `jt_voice_guard` passed score 100. Angle: AI CoE initiatives need run control before scale: approved path, owner, risk review, evidence, adoption/ROI measurement, and a recovery path when the workflow breaks.
- 12:23 memory lane: compacted `MEMORY.md` under advisory while preserving Jun 27 details here. Current operational baseline: Mission Control 265 total / 263 active / 11 high / 0 overdue; cost alerts empty; Spanish paused; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron scan has no current red rows; stale list-metadata rows are `prospect-discovery`, `Job Application Auto-Builder`, `Weekly Systems Review`, and `content-generate-x`; duplicate `lossless-claw` warning persists.

## 2026-06-28 Heartbeat Memory Maintenance
- 09:12 market lane: corrected `content-generate-x` model routing from invalid `openai-codex/gpt-5.5` to configured `openai/gpt-5.5`, verified model-routing guard/cost alerts clean, and appended PM market addendum. MRI Agora / recurring-consulting signals sharpen Altmark as workflow orchestration with approval evidence, not autonomous collections.
- 10:05 film/systems lane: 10AM missed-cron gate passed. Weekly Systems Review failure was unsafe pseudo-command style; live WSR prompt was patched with command-only execution rules, and the report was manually completed/delivered. Remaining red metadata is owned by natural next runs, not a blind rerun target.
- 11:30 AI-tool lane: appended AI Tool Monitoring note. Agentforce/scriptable-agent signals reinforce Run Control proof as source/input validation, workflow identity, allowed data/tools, deterministic rule/script step, risk threshold, reviewer state, evidence link, outcome event, model route, delivery proof, and recovery path.
- 12:12 crypto lane: used same-day morning artifacts only; research/ranking only, no trades/swaps/wallet/payment-MCP/x402. Future cron scans must inspect `.jobs[].state.lastRunStatus` and `consecutiveErrors` before declaring red metadata clear.
- 13:18 job-market lane: no qualifying NYC/remote non-coding AI implementation role cleared filter. Results reinforce business-side AI enablement language: AI Academy, approved tool stack, playbooks, prompt libraries, project portfolio, adoption metrics, and ROI.
- 14:13 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-local-service-website-operating-record-2026-06-28.md`; `jt_voice_guard` passed score 100. It uses the Natasha/local-studio browser-session signal permission-safely and does not name the business.
- 15:30 memory lane: compacted `MEMORY.md` while preserving Jun 28 details here. Current baseline: Mission Control 267 total / 264 active / 12 high / 0 overdue; cost alerts empty; Spanish paused; digest queue contains only routine TikTok warmup; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata rows remain `content-generate-x` and `Weekly Systems Review`, both already owned by route/prompt fixes and natural next runs; duplicate `lossless-claw` warning persists.

## 2026-06-29 Heartbeat Memory Maintenance
- 08:12 market lane: active-hours checks passed. Prompt-hardened `Job Market Daily Research` after pseudo `fetch ... -> run jq (agent)` failure. Added PM/Altmark market addendum: Salesforce Agentforce commerce/help-agent and AI-ready CRM signals reinforce Altmark as resolution-control proof with trusted source row, allowed action scope, reviewer decision, evidence link, and outcome event. Action order remains Altmark packet first, then Petri M2, then PM COI wave one.
- 09:12 AI-tool lane: appended AI Tool Monitoring note. Salesforce Agentforce/AI-ready CRM signals reinforce business-owned resolution paths, trusted inputs, approved actions, command-safe prompts, and replayable run records.
- 10:17 crypto/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline using full IDs and validated artifacts. Film review added model-route regression: after cron model repair, run `scripts/model_routing_guard.py` and inspect affected payloads for configured model keys such as `openai/gpt-5.5`, not provider/runtime spelling. Crypto monitoring remained research/ranking only with no trades/swaps/wallet/payment-MCP/x402.
- 11:32 job-market lane: CodePath Senior Manager of AI Enablement scored 20/25 but is salary-capped, so route as consulting bridge rather than application priority. Useful positioning language: Claude Enterprise, Claude Code, MCP-assisted agents, eval rubrics, review gates, reusable assets, and outcome reporting. Prompt-hardened `Autoresearch Sweep` after pseudo `print lines ... (agent)` failure.
- 12:12 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-claude-workflow-productionization-2026-06-29.md`; `jt_voice_guard` passed score 100. Angle: AI enablement work is moving from tool access toward workflow productionization with approved paths, reusable agents, eval gates, review queues, delivery proof, and outcome reporting.
- 13:12 memory lane: compacted `MEMORY.md` while preserving Jun 29 details here. Current baseline: Mission Control 274 total / 271 active / 13 audit high / 14 direct-label high / 0 overdue; cost alerts empty; Spanish paused; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata rows are `Job Market Daily Research` and `Autoresearch Sweep` with 1 consecutive error each, both prompt-hardened today, plus `Weekly Systems Review` with 2 consecutive errors already owned by repair/natural next-run path. No blind reruns; duplicate `lossless-claw` warning persists.

## 2026-06-30 Heartbeat Memory Maintenance
- 08:12 market lane: active-hours checks passed. Repaired non-ASCII dash marks in `memory/content/weekly-2026-06-29.md`. Added PM/Altmark market addendum tying Jotform n8n workflows, A.CRE CRE AI coverage, and Highwire/Veriforce construction-inspection AI to run-control proof: source input, allowed action scope, reviewer state, evidence link, and outcome event.
- 09:12 AI-tool lane: patched `eve-niche-monitor-006` with command-safety hardening after pseudo `run bun kb.ts (agent)` failure. Appended AI Tool Monitoring note: enterprise agent stacks are converging on scoped workspace agents, compliance-grade logs, MCP/RBAC gateways, policy enforcement, and replayable evidence.
- 10:12 crypto/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Patched `eve-job-market-daily-005` with a final-response checkpoint after it stopped before confirming completion and left the daily brief stale at 2026-06-29. Added regression/training entries. Crypto monitoring used validated artifacts only; research/ranking only, no trades/swaps/wallet/payment-MCP/x402.
- 11:32 job-market lane: source brief remained stale at 2026-06-29, so the pulse was explicitly positioning-only. Reused CodePath/Claude/MCP workflow-productionization signal; no new application/build task; Altmark packet remains first.
- 12:12 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-workspace-agent-control-record-2026-06-30.md`; final `jt_voice_guard` passed score 100. Angle: workspace agents need scoped app access, reviewer state, allow/block decision, evidence link, and outcome event before automation is trusted.
- 13:18 memory lane: compacted `MEMORY.md` under advisory while preserving Jun 30 details here. Current baseline: Mission Control 275 total / 271 active / 13 high / 0 overdue; cost alerts empty; Spanish paused; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata rows are `Job Market Daily Research` with 2 errors, `Niche Intelligence Monitor` with 1, `Autoresearch Sweep` with 1, and `Weekly Systems Review` with 2; all are prompt-hardened/owned or natural-next-run items. No blind reruns; duplicate `lossless-claw` warning persists.

## 2026-07-01 Heartbeat Memory Maintenance
- 08:13 market lane: Morning Brief delivered with Altmark packet first, Petri M2 second, PM COI wave one third. Added PM/run-control market addendum from AI AGENT Act and Salesforce Help Agent signals: accountable service workflows need traceability, revocation/blocked-action evidence, escalation boundaries, and outcome-tied resolution proof.
- 09:18 AI-tool lane: appended AI Tool Monitoring note. Fresh governance signal moved to device/workspace/MCP/action boundaries and completed-resolution proof: allowed scope, reviewer decision, blocked/allowed state, replayable evidence, and outcome event.
- 10:12 crypto/film lane: missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Film review verified existing pseudo-command and Weekly Systems Review regression coverage. Crypto monitoring used validated artifacts only; research/ranking only, with no trades/swaps/wallet/payment-MCP/x402.
- 11:33 job-market lane: fresh 2026-07-01 job-market brief found no NYC/remote non-coding AI implementation role clearing 18/25. Positioning remains business-side agent operations proof: intake, approved workflows, eval/review gates, rollback or blocked-action evidence, adoption cadence, and outcome reporting.
- 12:12 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-completed-resolution-operating-record-2026-07-01.md`; `jt_voice_guard` passed score 100. Angle: completed-resolution operating records track source read, allowed action, blocked case, reviewer decision, final status, and cash/value event.
- 13:18 memory lane: compacted `MEMORY.md` and preserved Jul 1 details here. Current baseline: Mission Control 279 total / 276 active / 13 high / 0 overdue; cost alerts empty; Spanish paused by fallback state inspection; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata is now only `Autoresearch Sweep` and `Weekly Systems Review`, both with 2 consecutive errors and command-style/natural-next-run repair status. No blind reruns; duplicate `lossless-claw` warning persists.

## 2026-07-02 Heartbeat Memory Maintenance
- 08:13 market lane: active-hours checks passed. `Job Application Auto-Builder` prompt patched after pseudo-command failure, requiring real `rg`/`sed` shell commands and banning `search ... in file (agent)` / `print lines ... (agent)`. Added PM/Run Control market addendum from Microsoft Agent Governance Toolkit and NYC RGB 2026-27 guidance: frame PM proof as permissioned actions, approval gates, evidence logs, rent/regulatory constraints, owner/operator approvals, and measurable resolutions.
- 09:16 AI-tool lane: appended AI Tool Monitoring note from Microsoft Agent Governance/audit docs, OpenAI Compliance Platform and Enterprise/Edu notes, and Anthropic Enterprise notes. Run Control / AI Enablement OS remains an evidence pipeline for model/app/tool scope, approval or block state, append-only logs, delivery proof, and outcome events.
- 10:12 crypto/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Live `Autoresearch Sweep` cron was patched with `LATEST AUTORESEARCH COMMAND PATCH - 2026-07-02`, requiring executable `sed`/`rg`/`test` commands, banning pseudo tool text and prose arrows, and stopping with `AUTORESEARCH_BLOCKED: missing file [path]` for missing inputs. Crypto monitoring used validated artifacts only; research/ranking only, no trades/swaps/wallet/payment-MCP/x402.
- 10:34 project state update: Karen Vitale closeout lane active; Altmark Beelink/Conductor/rent-delinquency/playbook path active; Aya needs full Fable dashboard review, final updates, and Gil review meeting; Marketsmith meeting/proposal path active; app ops are Apple follow-up, Fable UGC/paid onboarding review, Yair idea exchange, then Fable playbooks and Codex/Opus implementation.
- 11:32 job-market lane: fresh daily brief found no qualifying NYC/remote non-coding AI implementation role. INSPYR Charlotte hard-filtered out; Cohere is employer signal only. Job-market energy stays below Karen closeout, Altmark deployment, Aya review, Marketsmith proposal prep, and send queue.
- 12:12 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-operating-sprint-ai-implementation-2026-07-02.md`; `jt_voice_guard` passed score 100. Angle: AI implementation as an operating sprint across closeout, local workflow deployment, dashboard review, proposal/playbook work, and app onboarding/distribution order.
- 13:18 memory lane: refreshed `MEMORY.md` automation baseline and preserved Jul 2 details here. Current baseline: Mission Control 282 total / 280 active / 14 high / 0 overdue; cost alerts empty; Spanish paused by fallback state inspection; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata: `Job Application Auto-Builder` 1, `Autoresearch Sweep` 2, `Weekly Systems Review` 2; all command-style repair/natural-next-run items after today's prompt patches. No blind reruns; duplicate `lossless-claw` warning persists.

## 2026-07-03 Heartbeat Memory Maintenance
- 09:13 market lane: appended PM/Altmark research addendum. Microsoft AI deployment company, Salesforce resolution pricing, and NYC RGB 2026-27 orders support Altmark-first Run Control proof language.
- 10:13 AI-tool/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Added a regression row requiring latest-run timestamp vs repair/nextRunAtMs comparison before another cron patch or blind rerun.
- 11:33 crypto lane: Autoresearch Sweep cleared on natural run with `AUTORESEARCH_OK`; crypto monitoring used validated morning artifacts only and made no trades/swaps/wallet/payment actions.
- 12:29 job-market lane: fresh job-market pulse found no new qualifying role; positioning remains Mission Control/OpenClaw and Run Control proof.
- 12:54 content lane: saved review-only LinkedIn draft `memory/drafts/workflow-audit-property-page-ship-2026-07-03.md`; `jt_voice_guard` passed score 100. No external send or kill-loop activation.
- 13:08 memory lane: refreshed compact automation/site baseline. Current baseline: Mission Control 287 total / 283 active / 15 high / 0 overdue; cost alerts empty; Spanish paused; direct cron scan has one red row, `Weekly Systems Review` with 2 consecutive errors, owned by prior command-style repair and natural next Sunday run. Site verification from the live check: `jtsomwaru.com` and `/property` are committed, pushed, redeployed, and current; Mission Control site ship tasks are done; kill-loop timer task remains waiting for JT confirmation.

## 2026-07-04 Heartbeat Memory Maintenance
- 09:13 market lane: active-hours checks passed. Appended PM/Altmark market addendum reinforcing property-tech exception-desk proof as run control: source ownership, allowed-action scope, reviewer state, and proof of resolved/escalated/held actions. Altmark rent-delinquency packet remains first.
- 10:17 AI-tool/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Verified Jul 3 Crypto Evening manual recovery proof in `crypto-agent/data/evening-log.md` and added regression/training coverage requiring same-day EOD recovery log proof before closing future manual crypto recoveries. Appended AI Tool Monitoring note on enterprise agent identity, approval checkpoints, audit trails, runtime policy enforcement, and outcome evidence.
- 11:32 crypto lane: used validated morning artifacts only; research/ranking only. Monitoring note captured PRXVT 25%, GITLAWB 25%, SURPLUS 25%, DOT 25%, exits NOX/NOOK/SAID; no trades/swaps/wallet/payment actions or extra X pulls.
- 12:37 job-market lane: Noon Crypto Midday Pulse was OK with `NO_ALERT_LOGGED`. Patched `Skills & API Researcher - Daily Scan` cron payload with file-read command hardening after pseudo `print lines ... (agent)` failure; no rerun solely to clear metadata. Job-market pulse found no qualifying NYC/remote non-coding AI implementation role; AIG and ServiceRocket were market-intel only.
- 13:12 content lane: saved review-only LinkedIn draft `memory/drafts/linkedin-ai-roadmap-workflow-audit-2026-07-04.md`; `jt_voice_guard` passed score 100. Angle bridges ServiceRocket/CoE roadmap signal to the live property Workflow Audit offer: source report, blocked row owner, approval state, and outcome evidence before a bigger AI program.
- 14:18 memory lane: refreshed compact memory baseline and preserved Jul 4 details here. Current baseline: Mission Control 288 total / 284 active / 15 high / 0 overdue; cost alerts empty; Spanish paused by fallback state inspection; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Digest queue contains only the routine 2 PM TikTok warmup item for Evening Digest. Direct cron red metadata: `Crypto Evening Pulse` 2 after Jul 3 manual recovery and timeoutSeconds 900, `Weekly Systems Review` 2 awaiting Sunday natural run, and `Skills & API Researcher` 1 with file-read hardening patched for next scheduled run. No blind reruns; duplicate `lossless-claw` warning persists.

## 2026-07-05 Heartbeat Memory Maintenance
- 09:12 recovery lane: Morning Brief failed after a Nash pseudo-command and no delivery. Recovered the brief manually, sent it to Telegram numeric target `6608544825` as message 24793, saved the Nash unavailable marker to `memory/app-marketing/daily-nash/2026-07-05.md`, and patched `eve-morning-brief-001` with command-safety hardening, Nash non-abort skip behavior, final status checkpoint, timeout/failure-alert settings, plus regression/training notes.
- 10:05 systems lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Weekly Systems Review produced/sent its report but ended red on pseudo `run openclaw cron (agent)` text; patched WSR with command-only follow-up hardening and training/regression coverage. Morning Brief, Skills/API Researcher, and WSR red rows were treated as owned/natural-next-run items, not blind rerun targets.
- 11:30 market lane: appended July 5 PM/Altmark addendum. PM maintenance/delinquency triage is mainstreaming; the buyer-safe differentiator remains integration-aware run control with source export, owner/reviewer, escalation state, evidence, and outcome event.
- 12:12 AI-tool lane: appended July 5 AI Tool Monitoring. Governance signal points to reconstructable run-control records, append-only/compliance logs, scoped agent access, authorization layers, deny/allow rules, and no-action guardrails.
- 13:12 crypto lane: appended July 5 crypto monitoring from validated local artifacts only. Research/ranking output: SURPLUS 30%, ODAI 25%, DOT 25%, PRXVT 20%; exits NOX/NOOK/SAID; no trades/swaps/wallet actions/transfers/payment-MCP/x402/personalized advice or extra X pulls.
- 14:17 job-market lane: appended July 5 pulse. Crain Communications Director, Enterprise AI Enablement scored as market intel only; useful language includes Claude rollout, guardrails, micro-learning, adoption measurement, and roadmap ownership, but it stays below Altmark/Yair, Petri M2, and active consulting sends.
- 15:30 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-ai-enablement-operating-record-2026-07-05.md`; `jt_voice_guard` passed score 100. Angle: AI enablement as an operating record, anchored in the rent-delinquency source-export/reviewer/exception-rule scene and the property Workflow Audit path. Not posted or scheduled.
- 16:36 memory lane: refreshed compact baseline. Current baseline: Mission Control 291 total / 287 active / 16 high / 0 overdue; cost alerts empty; Spanish paused by fallback state inspection; digest queue contains only the routine TikTok warmup item for Evening Digest; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata: `Morning Brief` 1, `Skills & API Researcher` 1, and `Weekly Systems Review` 3; prompt hardening markers are present and no blind reruns were performed. Duplicate `lossless-claw` warning persists.

## 2026-07-06 Heartbeat Memory Maintenance
- 08:12 market lane: Morning Brief already completed with `MORNING_BRIEF_SENT_WITH_NASH_SKIP`. Appended PM/Altmark market addendum: enterprise agent governance and Lette-style property-ops signals reinforce Altmark as source-aware run control, not generic automation.
- 09:18 AI-tool lane: appended AI Tool Monitoring note. Enterprise agents are moving into governed workspace products with admin/plugin/action controls, policy checks, scoped approvals, and durable audit/compliance evidence.
- 10:12 crypto/film lane: 10AM missed-cron gate passed for Crypto Full Analysis and Outreach Pipeline. Patched `content-generate-linkedin` with final-status hardening requiring `LINKEDIN_QUEUE_READY`, `LINKEDIN_QUEUE_SKIPPED`, or `LINKEDIN_QUEUE_BLOCKED: [reason]`; updated regression/training coverage. Crypto monitoring used validated morning artifacts only; research/ranking only, no trades/swaps/wallet/payment actions or extra X pulls.
- 11:34 job-market lane: fresh Jul 6 brief had no critical/high flags and no qualifying NYC/remote non-coding AI implementation role. Job-market signal stays positioning input for AI operating-model proof rather than a new application/build task.
- 12:12 content lane: created review-only LinkedIn draft `memory/drafts/linkedin-forwardable-offer-path-2026-07-06.md`; `jt_voice_guard` passed score 100. Angle: a warm referral should not need to translate the offer; one link should name the buyer, first workflow, price/timeline/decision path, and proof checks.
- 13:20 memory lane: refreshed compact baseline. Current baseline: Mission Control 295 total / 291 active / 16 high / 0 overdue; cost alerts empty; Spanish paused by fallback state inspection; digest queue 0; cron volume green at 44 enabled, ~176.46/wk, 25.21/day, 20.21 agentTurn/day, no unknown schedules. Direct cron red metadata: `Weekly Systems Review` 3 and `content-generate-linkedin` 1, both known/patched or command-style natural-run rows. No blind reruns; duplicate `lossless-claw` warning persists.
- 14:38 site-build update: `jtsomwaru.com` build completed and commit `c870c52` was pushed. Homepage broadened from property-first to AI operations implementation for ops-heavy teams; `/property` remains the focused PM path.

## 2026-07-13 Heartbeat Memory Maintenance
- Active-hours baseline through 14:12: Mission Control 283 active / 14 high / 0 overdue / 0 errors; cost alerts empty; enabled cron red rows empty; Spanish paused with `last_lesson_date=2026-05-24`.
- Today completed/handled deduped lanes: client/market research addendum for Altmark send-gate priority, AI-tool monitoring around policy-decision evidence, directive-disabled crypto check, directive-limited job-market pulse, and memory maintenance. Content drafting was not expanded because July directives keep content-generation/marketing rebuild off until JT approval.
- Current directive state: crypto, job-market, and content-generation loops are disabled/refused scope, not missed work. Do not rerun, re-enable, alert, spend X/API, create job/app tasks, or create content batches unless JT explicitly reactivates.
- Passive-income Jul 12 strategist remains DEGRADED FALLBACK: BUILD 0, WATCH 4 only. Jul 13 film review updated existing MC task `[PI] Validate fallback-only Passive Income Strategist weeks` to include `memory/passive-income/2026-07-12-strategist.md`; fallback BUILD 0 must not be treated as a true no-build verdict.
- Compact `MEMORY.md` refreshed under advisory with Jul 13 automation/job/crypto state.

## 2026-07-14 Heartbeat Memory Maintenance
- Morning Daily Send Sheet was already sent at 07:30 with three due sends: Altmark rent delinquency remaining, Petri Plumbing M2, and HPM/Superior M2 follow-ups. Verified cash state remained $0 MTD with 18 days left; no duplicate send was created by heartbeat.
- Active-hours baseline through 14:12: Mission Control audit/API ok at 283 active / 14 high / 0 overdue / 0 errors; cost alerts empty; Spanish paused with `last_lesson_date=2026-05-24`.
- Cron state: 12 enabled / 60 disabled / 72 total. Weekly Systems Review still showed known historical Jul 12 pseudo-command red metadata after useful completion and live-payload patch; no blind rerun was started.
- Today completed/handled deduped lanes: Altmark stale-send research addendum, 10AM missed-cron/film review hardening, AI-tool monitoring, directive-disabled crypto check, directive-limited job-market pulse, and memory maintenance. Content drafting remained constrained by July directives pending marketing rebuild approval.
- Marketsmith Jul 14 pricing note: Karen said $150/hr is above budget and cited $135/hr in office / $100/hr remote; team is still locked in on JT. Tactical recommendation is one $10,800 fixed-fee Ed SOW, 50% kickoff / 50% completion; do not offer a two-option hourly/fixed menu, a lower anchor, or $100 remote.
- Compact `MEMORY.md` refreshed under advisory with Jul 14 automation, job, crypto, and Marketsmith state.

## 2026-07-15 Heartbeat Memory Maintenance
- Active-hours baseline through 14:15: Mission Control audit/API ok at 283 active / 14 high / 0 overdue / 0 errors; cost alerts empty; Spanish paused with `last_lesson_date=2026-05-24`.
- Cron registry remained 12 enabled / 60 disabled / 72 total. The only red enabled row was known Weekly Systems Review `b2ca53ab-0c07-4a22-8424-9d39bf988405` historical pseudo-command metadata; no blind rerun was started. Crypto jobs remained disabled with no next run under July directives.
- Daily Send Sheet had already sent at 07:31 with Altmark rent delinquency, Petri M2, HPM M2, Marketsmith fixed-fee artifact gap, Superior stale follow-up, and $0 MTD cash state; heartbeats did not duplicate the send.
- 10AM film review fixed the Marketsmith artifact gap by creating `memory/clients/marketsmith/fixed-fee-proposal-send-packet-2026-07-15.md`, adding the fixed-fee decision-log row, and adding a Daily Send Sheet artifact-gap regression row. Recommended path remains one $10,800 fixed-fee Ed SOW, 50% kickoff / 50% completion; no hourly menu, lower anchor, or $100 remote.
- Today completed/handled deduped lanes: Marketsmith client/market packet, AI-tool monitoring on authority records, directive-disabled crypto check, directive-limited local job-market pulse, and memory maintenance. Content drafting remained constrained because marketing/content generation jobs are killed pending Marketing Stage 3 rebuild and JT approval.
- Compact `MEMORY.md` refreshed under advisory with Jul 15 automation, job, crypto, and Marketsmith state.

## 2026-07-16 Heartbeat Memory Maintenance
- Active-hours baseline through 14:13: Mission Control audit/API ok at 256 active / 14 high / 0 overdue / 0 errors; cost alerts empty; Spanish paused with `last_lesson_date=2026-05-24`.
- Cron registry remained 12 enabled / 60 disabled / 72 total. The only red enabled row was known Weekly Systems Review `b2ca53ab-0c07-4a22-8424-9d39bf988405` historical pseudo-command metadata; no blind rerun was started.
- Daily Send Sheet sent at 07:31 with Altmark source/export gate, Marketsmith fixed-fee proposal, Petri M2, the closed day-15 cash threshold, stale Altmark/Petri/HPM/Superior threads, and $0 MTD cash. Heartbeats did not duplicate the send.
- 10AM film review found a stale Mission Control pricing anchor after the Marketsmith commercial pivot. Patched task `j5791a894m0meea4y9qjq61bkh87ffc7` to `Marketsmith: send $10,800 fixed-fee Nexus proposal`, added a stale-pricing regression row, and appended the training-log line.
- Later local state showed MSI signed and active delivery: 80-hour fixed-scope Nexus engagement, $10,800 signed value, 50% kickoff / 50% completion. SoberLife/Karen and Aya dashboard are complete/paid; referral asks are now eligible.
- Today completed/handled deduped lanes: PM/Agentforce outcome-pricing client/market addendum, AI-tool monitoring on authorization records, directive-disabled crypto check, directive-limited local job-market pulse, and memory maintenance. Content drafting remained constrained because marketing/content generation jobs are killed pending Marketing Stage 3 rebuild and JT approval.
- Compact `MEMORY.md` refreshed under advisory with Jul 16 client, automation, job, and crypto state.
