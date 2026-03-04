# MEMORY.md — Long-Term Context
> Main session only. Do NOT load in group chats or shared contexts.
> Full history: docs/memory/MEMORY-full.md

## File Architecture
- SOUL.md: personality (Eve can modify) | SECURITY.md: security rules (operator-only)
- AGENTS.md: behavioral rules + all security duplicated for sub-agents
- TOOLS.md: paths/commands (authoritative) | MEMORY.md: context/decisions (authoritative)
- USER.md: JT profile | HEARTBEAT.md: wake behaviors | IDENTITY.md: name/role

## 🚨 Hard Rules
- Gateway restart: ALWAYS use restart script. NEVER raw launchctl/gateway config.patch/apply.
- openclaw.json: NEVER write arbitrary keys — crashes gateway. External keys → TOOLS.md only.

## JT
- Jon Trevor Somwaru | NYC metro | Telegram primary | @jts_14 | @jt__crypto | GitHub: jsomwarux
- BSA background (Spectrum Enterprise 2019–2025): product catalog config, cross-team coordination
- Direct, efficient. Expects Eve to figure things out. Corrects clearly.
- NOT a developer — auto-disqualify roles requiring Apex/SFDX/ML engineering/hands-on coding

## Opticfy Niche-Skill Matrix (locked 2026-03-03)
| Skill | Primary Niche | Secondary Niche | Why |
|-------|--------------|-----------------|-----|
| **Agentforce** | Insurance (COVU anchor) | Mid-large PM/RE (Salesforce shops) | Requires Salesforce — only targets companies already on it |
| **n8n** | Construction + Skilled Trades $5-20M (Aya reference) | Wholesale Distribution (NYC garment/food/hardware) | Stack-agnostic — targets ServiceTitan, Jobber, QuickBooks, NetSuite users |
- Small PM companies (AppFolio/Buildium, not Salesforce) → n8n, not Agentforce
- Upsell path: land construction/wholesale on n8n → as they grow onto Salesforce → sell Agentforce

## Opticfy (AI Consulting)
- Target niches: wholesale distribution, property mgmt, construction, insurance ops, skilled trades (NYC)
- New service (Feb 2026): Cowork Plugin Implementation — custom Claude Cowork plugins + marketplace
- New skill: opticfy-ops — 5 commands (/client-intake, /process-doc, /runbook, /vendor-eval, /anomaly-audit) at skills/opticfy-ops/
- Expansion target: HubSpot (top pick from enterprise platforms research) — SMB CRM, huge NYC presence, lower Salesforce partner competition. Full research: memory/research/enterprise-platforms.md
- Partner pipeline: Avallon (NYC seed startup, no formal program yet) — DM to CEO Cornelius Schramm ready (memory/research/avallon-furtherAI-partner-research-2026-02-28.md). FurtherAI = 6-12 month play.
- ConversationFirst framework built (2026-02-28) — Agentforce UX methodology: persona cards, flow diagrams, 25-pt checklist, 1-page write-up. Ready to share with prospects. Path: memory/drafts/conversationfirst-framework-2026-02-28.md. JT pending: full portfolio card vs. services section callout?

## Aya (Client — Construction/Co-living, NYC)
- Project 1: Construction progress dashboard — $1,500 ✅ complete
- Project 2: StreetEasy scraper → Google Sheet (auto-pulls properties meeting criteria every 2 weeks) — $1,000 ✅ signed
- Project 3 (pending): Co-living dashboard app similar to construction dashboard — quoted $2,500, waiting on final feedback. Contact is a member of Aya's co-living business. Said he's busy with a big project.
- Project 4 (in talks): Dashboard + automations for Head of Acquisitions. Sent NDA to review his spreadsheet — no response after 2 follow-ups. Cold for now.
- Strategy: Aya is becoming an anchor client. Each project extends runway and builds referral credibility within their network. Keep relationship warm.

## Active Apps
- Vista: movie rating app — **LIVE on Apple App Store** (March 2026)
- Nash Satoshi: crypto game theory rankings (4-LLM ensemble) — GitHub jsomwarux/Nash-Satoshi (private)
- Glow Index: skincare rankings on Replit — waiting on n8n workflow + ngrok URL
- jtsomwaru.com: live at https://jtsomwaru.com — Next.js on Vercel | Updated 2026-02-27: custom Framer Motion graphics on all 5 portfolio cards, hero subtitle updated, Zapier removed from About
- Dynasty fantasy football: planned

## Job Market
- Target: AI Solutions Architect, AI Implementation Lead, AI Systems Analyst
- $150K min, $180–220K target | NYC metro or remote only
- 🔴 Squarespace People AI SA (19/25, $126–180K hybrid NYC) — apply this week (posted Feb 21, time-sensitive). Docs in Google Drive.
- 🔴 Salesforce Lead Agentforce SE (24/25, $148K–$198K NYC) — DEADLINE 03/27/2026. Perfect fit: leads sandbox-to-production engagements, zero code requirement. → salesforce.com/jobs/jr329627
- 🟠 Salesforce Agentforce/AI Deployment Strategist (20/25, $140K–$185K) — confirmed active at jr305206
- 🟠 Salesforce Sr. Supply Chain Strategist (21/25, $180K–$298K) — vet domain requirement first
- 🟠 Writer SA East (20/25, $207K–$250K hybrid NYC) — Python gap, still worth applying. Docs: memory/drafts/writer-sa-resume.md + writer-sa-cover-letter.md
- Skill gaps (active): AWS Bedrock, LangChain, Copilot Studio, Conversation Design (partially closed — ConversationFirst framework built)

## Setup State
- Model: anthropic/claude-sonnet-4-6 primary | groq/llama-3.3-70b-versatile fallback
- Auth: anthropic:default uses OAuth subscription token (sk-ant-oat01-*) — NOT an API key. All Anthropic usage = $0 real cost, covered by Claude subscription. No usage in Anthropic Console — this is correct and expected. Confirmed working 2026-02-28.
- Compaction: mode=safeguard, reserveTokens=40k, keepRecentTokens=10k, floor=12k (safeguard is correct — preserves cache hits)
- Providers: anthropic:default ✅ (OAuth) | groq:manual ✅ (API key, ~$0) | openrouter:default ✅ (API key, pay-per-use for non-Anthropic models)
- OpenRouter routing: Anthropic models → direct (OAuth, $0). All others → openrouter/ prefix (real cost).
- Brave Search ✅ | Log redaction: tools ✅

## Passive Income System
- **Bucket**: separate from consulting + career — builds that run autonomously, zero upkeep
- **Active properties**: Nash Satoshi (built, stalled, needs monetization), Glow Index (built, stalled, needs n8n + ngrok)
- **Vibe Marketing Agent**: NOT yet built — JT will provide detailed instructions separately
- **Scout agent**: `agents/passive-income-scout/AGENT.md` | state: `agents/passive-income-scout/state.json`
- **2-stage pipeline**: Scout (Sun 6AM) → Strategist (Sun 7:30AM)
- **Scout cron UUID**: `dcdbbef5-2f16-4f3d-81ab-78e1b34f6fd0` | Sun 6AM ET | generates 5 raw ideas → saves report
- **Strategist cron UUID**: `4e19c300-d387-4019-b658-9664f0d665d5` | Sun 7:30AM ET | deep analysis, 8-dimension scoring, pushes 🟢 winners to MC, sends Sunday Telegram digest
- **Scout reports**: `memory/passive-income/YYYY-MM-DD-scout.md` | **Strategist reports**: `memory/passive-income/YYYY-MM-DD-strategist.md`
- **MC project tag**: `passive-income` | Nash Satoshi + Glow Index tasks tagged

## Active Cron Jobs (19) — post-incident schedule (2026-02-26)
- crypto-morning: 6AM daily | main | full portfolio analysis
- job-market: 6:30AM daily | isolated sonnet | → data/daily-brief.md
- morning-brief: 7:30AM daily | main | brief + costs + niche + jobs
- build-ideas-sync: 7:15AM daily | isolated groq | reads agent-ideas.md → pushes new ideas to Mission Control
- niche-monitor: 9AM Mon–Fri only | isolated sonnet | ⚠️ Brave API key not accessible in isolated sessions. Main session runs niche monitor as fallback during heartbeats.
- heartbeat: 10AM,2PM,6PM,10PM EST | main | tasks + cost alerts
- skills-researcher-daily: Mon–Sat 11:30AM | isolated sonnet (fixed 2026-03-01, was gemini-flash — invalid model ID) | X (8 queries) + web scan, alert 🔴/🟠 only
- crypto-midday: 12PM daily | isolated sonnet | pulse (alerts if Δ>±15%)
- pending-tasks: 10:30AM,2:30PM,6:30PM,10:30PM | main | tasks/pending.jsonl
- viral-swipe: Mon/Wed/Fri 5:30AM | isolated sonnet | X research → Notion swipe file
- crypto-evening: 8PM daily | isolated sonnet | EOD pulse (alerts if move >20%)
- health-checkin: 9PM daily | main | ✅ firing correctly (scheduler drift resolved). Eve-health-checkin-003 confirmed `0 21 * * *` America/New_York.
- weekly-synthesis: Sunday 8AM | isolated sonnet | weekly KB + cost review
- health-report: Sunday 9AM | isolated groq | runs health.py --report
- skills-researcher-weekly: Sat 7AM | isolated sonnet | deep X + Tier 3 web + full report
- overnight-autonomy: 3AM daily | isolated sonnet | selects 2 eligible tasks from MC → executes → writes log | UUID: be59a068-eccd-4a7c-964e-946ab40ace7e
- passive-income-scout: Sunday 6AM ET | isolated sonnet | trends → 5 raw ideas → saves report (no MC push, no Telegram) | UUID: dcdbbef5-2f16-4f3d-81ab-78e1b34f6fd0
- passive-income-strategist: Sunday 7:30AM ET | isolated sonnet | reads Scout report → deep 8-dimension analysis → pushes 🟢 winners to MC → sends Sunday digest to Telegram | UUID: 4e19c300-d387-4019-b658-9664f0d665d5
- monthly-goals-gap: 1st of month 8AM | isolated sonnet | job market vs. Eve capabilities audit → MC/Skills queue | UUID: fdc2cf75 (ran 2026-03-01 ✅)
- Daily cap: 20 invocations/weekday ✅

## Cost Tracking
- Script: scripts/cost-tracker.py | Snapshots: memory/costs/YYYY-MM-DD.json (captured 2AM via backup)
- Auth: Anthropic profile uses OAuth subscription token (sk-ant-oat01-*) — NOT an API key. All Claude/Sonnet/Opus usage is $0 in real API charges, covered by flat Claude subscription. No usage appears in Anthropic Console.
- Real costs: OpenRouter and Groq only (used when explicitly routing to non-Anthropic models)
- Alerts: session >$0.50, daily >$2.00, monthly pace >$15 | Goal: <$10/mo real API spend
- Pre-2026-02-28 snapshots zeroed out — were calculated with wrong Anthropic API pricing (phantom costs)
- 2026-02-27: daily hit $10.79 (over $10 limit) — driven by Writer SA sub-agent (27k tokens) + morning brief + niche monitor. Consider raising daily threshold to $15 or reducing sub-agent token usage.

## Portfolio Auto-Updater
- Repo: ~/projects/jtsomwaru-com/ → Vercel (auto-deploy on main push)
- Agent: agents/portfolio-updater/AGENT.md | Queue: agents/portfolio-updater/queue.jsonl
- Runs: nightly as final step of overnight agent (3 AM)
- Auto-approves score ≥7/10 | Flags 4–6 to JT | Skips <4
- Demand reorder: weekly — featured projects ranked by skills-demand-tracker scores
- Site files: src/data/projects.ts | src/components/project-graphics/index.tsx | src/components/About.tsx
- Triggers: overnight builds, JT says "done/shipped", Opticfy completions, MC tasks flipping to done, in-session builds (via AGENTS.md rule)
- Morning brief: shows 🌐 Site Updated if anything was added overnight

## Spanish Learning System
- Started: 2026-03-02 | Level: A1+ (high beginner, dormant HS Spanish)
- Goal: Casual conversation with girlfriend + her family | Focus: speaking, not writing
- State: `~/.openclaw/workspace/spanish/state.json`
- Curriculum: `~/.openclaw/workspace/spanish/curriculum.md` (4 weeks mapped)
- Lessons: `spanish/lessons/YYYY-MM-DD.md` | Evaluations: `spanish/evaluations/`
- Crons: spanish-lesson (Mon–Sat 8PM ET, UUID: babd905a) | spanish-eval (Sun 8PM ET, UUID: 012216b9)
- Accountability: 10PM heartbeat checks state.json → nudges if lesson not complete
- Voice: JT sends voice message → Groq whisper-large-v3 transcription → Claude evaluates (max 2 corrections per response)
- Real-world challenges unlock weekly (Week 1: say buenos días to someone)

## Automation Infrastructure
- Cleanup: scripts/cleanup-sessions.py | 3AM | Backup: scripts/backup.sh | 2AM | 7-day retention
- Mission Control: http://localhost:3000 + port 3210 (Convex)

## Crypto
- Primary income: crypto | Forward bet: x402 protocol
- Portfolio (7 coins as of 2026-02-26): $MLTL, $KELLYCLAUDE, $FELIX, $NOX, $SELFCLAW, $JUNO, $PRXVT
- Coin intelligence: crypto-agent/data/coin-intelligence/TICKER.md per coin
- $JUNO note: previously EXIT-rated — JT re-entered, agent will re-analyze fresh each morning

## Key Decisions
- **Priority order locked (2026-03-03)**: (1) Polish jtsomwaru.com + build demo agents → (2) Post LinkedIn career update linking to site → (3) Resume job applications + outreach. Nothing in steps 2–3 starts until step 1 is complete.
- **All outreach on hold (2026-03-03)**: No direct outreach until jtsomwaru.com + demo agents are polished. Unlock order: demos built → site updated → outreach resumes. Affected: Avallon DM, Opticfy prospect pipeline, distressed property pitch, Spectrum Cowork pitch, H.C. Oswald outreach, Cowork pitch draft review. All demoted to medium/blocked on MC.
- Aggressive compaction over safeguard — prevents context resets on long builds
- OpenRouter for non-Anthropic models — direct key only if model >$5/mo
- Sonnet default over Opus — caching = 80% as capable at 20% cost
- n8n over Make.com — self-hosted, no per-task pricing at scale
- Training system (Kobe Protocol, 2026-02-28): self-improvement via better SYSTEM (memory, rules, prompts) not model weights. Monthly gap analysis cron is the anchor.
- HubSpot = best Opticfy expansion platform (2026-02-28): SMB CRM, NYC penetration, lower partner competition than Salesforce
