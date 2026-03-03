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

## Opticfy (AI Consulting Agency)
- Target niches: wholesale distribution, property management, construction, insurance operations, skilled trades — all underserved NYC businesses
- Only client so far: Aya (construction progress dashboard, $1,500)
- Bottleneck: client research/outreach + specialized agent configuration
- Outreach plan: email + LinkedIn | Demo strategy: build agents first, then demo to prospects
- Specialized agents — all at `~/projects/` (paths/repos/commands in TOOLS.md):
  - **Research Agent** — researches prospects, identifies automation use case/pain points, determines n8n vs Agentforce fit. Entry point to 5-stage pipeline.
  - **n8n Agent** — builds production-ready n8n workflows for clients. Core Opticfy delivery mechanism. 4-LLM ensemble support.
  - **Agentforce Agent** — builds Salesforce Agentforce agents for clients on SF. Narrower niche, high-value when it fits.
  - **Crypto Agent** — game-theoretic portfolio analysis 3x daily. Serves JT personally, not clients.
  - **Vibe marketing agent** — content + marketing strategies (location TBC, not yet on this machine)
  - **Data visualization agent** — converts spreadsheets to interactive dashboards (location TBC, not yet on this machine)
- **New service (Feb 24):** Cowork Plugin Implementation — build custom Claude Cowork plugins, launch private marketplace, train teams. Industry-specific plugin suites = potential productized offering. Spectrum is a high-value target (JT knows their workflows; pitch as governed AI).

## Opticfy Client Research & Outreach Pipeline
5-stage fully automated: Research → Analysis → n8n Build → Presentation → Outreach → **Drive Sync** → JT presses send.
1. **Research Agent** (`~/projects/research-agent/`) — deep-dives prospect, identifies automation opportunity
2. **Analysis Agent** — maps current processes step-by-step, inventories integrations, outputs brief.json
3. **n8n Agent** (`~/projects/n8n-agent/`) — builds custom workflow from the brief
4. **Presentation Agent** — client-facing deck (Google Slides API or PDF first version)
5. **Outreach Agent** — drafts email with presentation attached
- **Key:** Standardize brief.json schema for all agent handoffs — on task board as HIGH priority
- **Google Drive sync:** After deck-built + outreach-drafted, run `python3 scripts/pipeline_drive_sync.py --slug [slug] --client "[name]" --stage all` → creates `Eve — Drafts / Opticfy — Client Pipeline / [Client] / Outreach Draft + Presentation Deck`
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
- Topics: what he's building, lessons, Opticfy thesis, Nash Satoshi methodology, AI tools

## Google Drive Drafts System
- Google account: openclawagenteve14@gmail.com | Root: "Eve — Drafts" in Drive
- Structure: Eve — Drafts / [Project] / [Content Type] (Vista, Nash Satoshi, Opticfy, _Templates)
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
- Goal: expand Opticfy, grow app revenue, stay hireable

## Job Market
- Both staying current AND open to opportunities
- Best-fit roles: AI Solutions Architect, AI Implementation Lead, AI Systems Analyst
- Hire pitch: BSA background + AI builder = rare combo employers need
- **NOT a developer** — roles requiring Apex, SFDX, ML engineering, or hands-on coding are auto-disqualified
- Salary: $150K min, $180-220K target | Location: NYC metro or remote only — no relocation
- **Squarespace People AI SA** (scored 19/25, Feb 21, hybrid NYC, $126-180K): JD literally says "vibe-code" — apply this week. Resume + cover letter in Google Drive (Eve — Drafts / Opticfy). Cover letter hook: "You used 'vibe-code solutions' in a JD — that's my methodology."
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
- **Purpose:** Builds n8n workflows for Opticfy clients. 4-LLM ensemble support.
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
