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
- Last reviewed 2026-06-01: `memory/research/niche-fitness-2026-06.md`; prior matrix archived at `docs/memory/consulting-niche-skill-matrix-2026-05-01.md`.
- June effort: property ops first, construction/skilled trades second, wholesale limited-test, Agentforce as strategic proof/readiness unless Salesforce stack + trigger + reply path are confirmed.

## Current Operating Context Relocated From MEMORY.md - 2026-06-11 Phase 6

> Relocated from `MEMORY.md` during Phase 6 bootstrap reduction. No content was deleted; compact bootstrap file now points here.

# MEMORY.md — Current Operating Context
> Main-session long-term context. Do NOT load in group/shared chats. Full archive: `docs/memory/MEMORY-full.md`; snapshot: `docs/memory/archive/MEMORY-before-optimization-2026-04-26.md`.
> Compact file: durable current context only; history belongs in daily notes/archive.

## JT Snapshot
- Jon Trevor Somwaru, “JT”; timezone America/New_York; Telegram primary; direct, low-ceremony, expects Eve to figure things out before asking.
- Background: Business Systems Analyst at Spectrum Enterprise/Charter; strong business-ops + tech translation edge.
- North Star: financial freedom and control over time. Ideal state = multiple high-earning, low-maintenance income streams, ideally managed by specialized AI agents that only escalate urgent decisions; bills paid, no debt spiral, money for nice things for him and family, and freedom to build creative apps/client work with a clear path to success.
- Current priority order: (1) AI implementation consulting, (2) app building + marketing toward eventual passive income, (3) crypto market monitoring/opportunity scanning, (4) health daily as the foundation.
- Income thresholds: safe ≈ $10K/mo, free ≈ $30K/mo, rich ≈ $100K/mo.
- Wants to be known primarily as an AI Implementation Specialist/Consultant and product builder.
- Constraints: not positioning as hands-on developer; avoid Apex/SFDX/ML-engineering roles. Job target: AI Solutions Architect / AI Implementation Lead, $150K min, $180–220K ideal, NYC/remote only. Non-negotiables: sleep, health, and staying in NYC/location stability.

## Hard Rules / Security Essentials
- Never modify `openclaw.json` auth, `summaryModel`, `summaryProvider`, primary model, `auth-profiles.json`, `models.json`, or update OpenClaw without JT approval.
- Never store or paste API keys outside approved auth/env files. Redact secrets in shareable files and Drive uploads.
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
- 2026-06-06 agent-ops positioning: “human-as-signal” is stronger than generic human-in-the-loop. Consulting/AI Context OS should frame agents as volume/execution and JT/client leaders as taste, priority, risk boundary, and react-and-redirect loops. Adopted `plan-review-pack` so internal `plan.md`/raw notes become external proof/review artifacts for clients.
- Target ICP: NYC/metro SMBs in construction, wholesale distribution, property management, skilled trades; HubSpot is a strong expansion platform due to less Salesforce competition.
- Outreach tiers use score gates: T1 80+ proof-led custom; T2 60-79 template/validation; T3 40-59 market-sensing only. JT sends all outreach.
- Preferred stack: n8n over Make.com for client automation; Agentforce when Salesforce/Data Cloud fit the client.

## Active Clients
- **Altmark Group:** priority paid client. Dedicated PC installed in office; insurance expiration workflow is live and final 50% paid. Rent delinquency workflow initial 50% paid and remains the top proof/revenue gate. Synthetic dry-run passed 2026-05-29: 8 rows -> 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 tenant-facing drafts from sensitive/cleanup rows. 2026-05-30 redacted-sample gate: first real-report sample stays review-only; next JT ask is redacted source export, source report path/export process, refresh cadence, reviewer, and exception rules. DHCR Lease Renewal Phase 1 assets sequence after rent delinquency acceptance unless Altmark reprioritizes. Keep proof capture privacy-safe; public naming requires accepted client output plus permission/anonymization.
- **Aya:** anchor client. Completed: $1,500 dashboard. Active: $1,000 StreetEasy scraper. Pending: $2,500 co-living dashboard. Stalled: acquisitions dashboard. Treat Aya as proof-point source only after accepted proof-safe evidence exists; gate: `memory/clients/aya/proof-evidence-checklist.md`.

## Pipeline / Business Development
- Active client proof pipeline gate lives at `memory/clients/proof-pipeline-gates.md`: acceptance/payment/scope → evidence capture → permission/anonymization → referral ask → distribution. Do not publish, pitch, ask for referrals, or reuse proof when acceptance/screenshots/metrics/permission are unverified.
- 2026-05-27 outreach strategy reset: LinkedIn warm-up comments are not the default route for new prospects. Use them only for high-fit T1/T2 prospects with recent relevant activity and a concrete M1/follow-up plan within 24-48h. Default prospecting should prioritize proof-led referrals/warm intros, live service pages/citation outreach, buyer-channel validation, and review-only outreach packets.
- 2026-06-02 contact completeness rule: every prospect that clears outreach threshold must include both LinkedIn profile URL and verified email. LinkedIn-only packets are incomplete; create/return the email-finding next step before treating them as send-ready.
- 2026-06-03 NYCB donor list: pass only as 50-name enrichment seed; fail as direct outreach. Never mention donor/NYCB source; keep only contact-complete operating-business buyers.
- 2026-06-02 prospect re-score/contact execution: `memory/consulting/prospect-tier-action-review-2026-06-02.md`. Petri/HPM/Superior are T2 with contact routes captured and JT-owned M2 follow-ups due Jun 4/5 if no reply; weak/no-email T3s are parked; New Yorker is the only possible wholesale limited-test after proof-led M2 window; Guyana Summit is connector/operator validation, not standard sales outreach.
- H.C. Oswald: hold outreach until personal site is polished and demo agents are built.
- Consulting pipeline lives under `~/projects/jt-consulting-pipeline/`; client folders contain research, deck, outreach draft, and pipeline status.
- After deck/outreach stages, sync with `python3 scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage all` and include Drive links for JT review.
- When JT says outreach was sent, same-turn run `scripts/outreach_update.py` with slug/company/message/channel/date; update daily note.

## Consulting Delivery / Niche Matrix
- New/active/signed client or paid/discovery engagement → document rigorously and initialize Client OS immediately. Services-as-software + June niche matrix details are archived in `docs/memory/MEMORY-full.md`; current live focus remains property ops first, construction/skilled trades second, with Agentforce as proof/readiness when Salesforce stack + trigger + reply path are confirmed.

## Current Apps / Products
- `jtsomwaru.com`: portfolio site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push. AI SEO now uses source-of-truth audits first: context file, surface mismatch, citations/entity, review language, ready-to-hire intent, proof assets, and monthly operator report. No public submissions before JT approval.
- Glow Index: live skincare rankings app at `https://glowindex.co`; now active for App Marketing OS durable discovery/pSEO planning. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store live; durable SEO page live on jtsomwaru.com. Current Vista-first app-marketing split/details live in `docs/memory/current-context-details-2026-05-27.md`.

## Content System
- Before drafting: read content voice/profile/evidence corpus; run `scripts/jt_voice_guard.py`; no preamble/em dashes/“Here’s the thing”; X singles 6–15 words. Stop Slop delta 2026-06-07 catches false agency/narrator-distance/vague/Wh/pull-quote/passive slop. LinkedIn now requires proof density + buyer-readable conversion asset when pipeline-oriented. Current PM proof assets: `memory/content/bank/2026-06-08/pm-front-desk-exception-desk-linkedin.md` and `memory/drafts/pm-front-desk-exception-desk-reply-proof-2026-06-08.md`.
- Content niche/source-map rules live in `memory/content/current-niche-map.md` and `docs/memory/current-context-details-2026-05-27.md`; new queues must pass `content_distribution_guard.py --require-reference-map`.
- AI Ops Teardown purpose reset 2026-06-01: teardowns must examine a current company, funding/product/market signal, regulation, or visible buyer problem in a JT-relevant niche, then show the optimal AI workflow JT would build for that company/problem. Strong default spine: current signal → buyer-recognizable bottleneck → concrete messy input scene → system-of-record need → workflow JT would build → cleaner operating outcome. Generic evergreen approval-queue/workflow advice is not enough.
- AI Ops Teardown weekly bundles must auto-upload to Drive via `scripts/ai_ops_teardown_drive_sync.py --json`; teardown docs go to `Consulting/AI Ops Teardowns/[date]/Teardowns`, content drafts to `Content/AI Ops Teardowns/[date]/Drafts`.
- App Marketing/ReelFarm reset and Sports GM/@dynastyjig rules live in `docs/memory/current-context-details-2026-05-27.md` and `docs/memory/sports-gm-content-system-current.md`; Wednesday LinkedIn uses `skills/wednesday-linkedin/SKILL.md`.
- Completed work triggers proof points, recent builds, technical angles if useful, content rubric, and Drive upload for substantive deliverables.

## Job Market
- Target only AI implementation / AI Solutions Architect / AI Implementation Lead roles that value BSA + ops automation background.
- Strategic posture as of 2026-05-11: consulting-first, employment selective. Treat job discoveries as hiring-budget/pain signals first, applications second. Route each strong discovery as `apply`, `both`, `consulting-outreach`, or `market-intel`.
- Apply only for exceptional strategic fits (generally 22+/25, $150K+, NYC/remote, low misrepresentation risk). For 18–21/25 roles, usually use the JD as market intel or a consulting lead signal instead of spending time on a resume package.
- If a company is hiring full-time for AI implementation, do not assume they lack consulting interest; position consulting as interim de-risking, workflow mapping, pilot governance, or acceleration while the FTE is hired/ramped — never as “hire JT instead.”
- 2026-05-29 xhigh audit: AI enablement roles now map to AI operating-system proof lanes (intake, connectors/MCP, evals, lineage, governance, adoption, rollback, ROI). `~/projects/job-market-agent/data/role-to-build-matrix.md` is canonical before creating role-derived build/demo tasks; Altmark proof still outranks H.I.G./DealDesk speculation.
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
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`.
- Critical commands/paths: `TOOLS.md`.

## Active Automation / Crons
- Cron volume is guarded by `scripts/cron_volume_guard.py`: ≤35 scheduled invocations/day average and ≤28 agentTurn/day average; >30/day warns. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM ET.
- `critical-files-integrity` (`ee357abb`) runs daily 9AM ET, timeout 180s; run script first, inspect/edit only on non-zero exit.
- Active cron count: 53 enabled / 70 total as of 2026-06-11 Phase 7. Evening Digest (`evening-digest-001`) runs daily 7PM ET from `memory/digest-queue.md`; 2PM TikTok warm-up queues to digest, redundant 7:45PM TikTok warm-up is disabled, and Morning Brief opens with a capped 3-item SEND QUEUE. Phase 7 disabled the old 9:45PM `nightly-autonomous-leverage-agent` and 3:20AM `Overnight Autonomy Agent`, replacing them with `Night Autonomy Agent` (`f146d8b8-94e0-49ff-8e4a-5050a284e894`) at 11PM ET. Phase 1 removed 12 disabled zombie jobs and saved baseline delivery metric at `docs/audits/baseline-delivery-2026-06-11.md`.
- `critical-files-integrity` now invokes `scripts/cron_snapshot.py`, which snapshots `/Users/jtsomwaru/.openclaw/cron/jobs.json` into `config/cron-snapshots/jobs-YYYY-MM-DD.json` and commits the snapshot when changed.
- Responsibilities: morning brief/send queue, evening digest, job market, niche monitor, crypto, content, App Marketing/ReelFarm, Sports GM, North Star, cost, health, passive-income pipeline. Heartbeat cron disabled 2026-05-17 at JT request.
- Recent cron hardening/details live in `docs/memory/current-context-details-2026-05-27.md` plus daily notes. Do not rerun content/reporting crons solely to clear metadata.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75; `--check-alerts` includes model-routing guard.
- Kobe Protocol: daily film review at 10AM and weekly skills audit.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- Current strategy: contained SMB ops bottleneck audits/prototypes; practical AI implementation for ops-heavy SMBs; prioritize B2B consultable products/client proof. App-growth next moves: `ChargeTrip Fit` spec-first MVP, Nash Satoshi conversion patch, Vista measurement/distribution loop.

## Integrity / Fabrication Corrections
- Never claim outreach/messages were sent unless tool/script evidence confirms it.
- Never fabricate URLs, deployment state, GitHub status, Drive links, or task closure. Verify with tools.
- If corrected by JT, immediately update the Mistakes Log/rules before moving on.

## Setup State
- 2026-05-31/06-06: Added AI Context OS/plan-review/proof skills, workflow/product agents, and `~/plugins/jt-operating-system` v0.2.0.
- 2026-05-11: GBrain consulting recall pilot lives at `~/projects/gbrain*`; use only `scripts/gbrain-consulting-search.sh "Entity"` for consulting/prospect entity lookup. No crons/skillpacks/broad ingestion/embeddings without JT approval.

## Automation / Live Opportunities
- Automation/client/opportunity history archived at `docs/memory/automation-and-live-opportunities-archive-2026-05-10.md`.
- Current must-remember: Altmark rent delinquency is the top consulting/proof lane. Internal proof/content tasks stay medium until evidence/send paths are ready. Yair may refer ~15 NYC family offices, proof/referral use gated.
- Guyana wedge: Local Content Operations Sprint for oil/gas-adjacent suppliers. Dad-forward/warm-intro language should emphasize supplier ops/admin drag, vendor records, bid readiness, and local-content evidence. Hidden/noindex `jtsomwaru.com/guyana` remains stale until rewritten.
- Nightly leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.
