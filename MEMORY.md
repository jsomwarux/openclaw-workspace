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
- bootstrapMaxChars: HARD CAP 32,000. NEVER raise above 32,000. 40,000 caused 2-hour outage 2026-03-31 (long-context billing error blocked all responses).
- openclaw.json: NEVER write arbitrary keys — crashes gateway. External keys → TOOLS.md only.
- Agentforce overnight builds: ✅ ALLOWED (lifted 2026-03-11). Must `git pull origin main` first. B2B Account Service Agent is PERMANENTLY BANNED — do not recreate under any circumstances.
- `launchctl unload/load` mid-session = gateway goes offline. Warn JT first. Defer to JT-initiated restart if possible.

## Infrastructure (updated 2026-04-01)
- OpenClaw version: 2026.3.28 (updated 2026-03-30)
- bootstrapMaxChars: 32000 (HARD CAP — reverted from 40000 on 2026-03-31. Setting to 40000 triggered "Extra usage required for long context" errors blocking ALL responses for ~2h. Never raise above 32000.)
- **Fallback model:** `openrouter/deepseek/deepseek-chat-v3-0324` (deepseek is same OpenRouter provider = fallback actually fires. Groq is NOT used — session profile conflict + 12k TPM too low.)
- **imageMaxDimensionPx:** 512 — cuts image token cost ~85% before context entry
- **auth.cooldowns.failureWindowHours:** 1 — faster cooldown recovery after rate limit clears
- **Root cause of 4 outages (2026-04-01):** Groq fallback never worked (session pinned to openrouter:default, Groq required provider switch). LCM silently failing (Groq 12k TPM < 20k needed). Image floods over context threshold. All three fixed.
- Gateway watchdog: `com.openclaw.gateway-watchdog` (10-min interval) — kills context-mode if RSS >1.5GB, kicks gateway if dead. Script: `scripts/gateway-watchdog.sh`
- context-mode Claude plugin: DISABLED (was causing OOM kills — disabled in `~/.claude/settings.json`)
- LaunchAgent ThrottleInterval: 10s (raised from 1s to prevent rapid crash loop)

## Agentforce Sync (✅ ACTIVE — 2026-03-11)
- JT builds Agentforce agents on personal device using Claude Code/Cursor
- Eve (Mac mini) syncs via GitHub: jsomwarux/agentforce-agent
- Repo path: ~/projects/agentforce-agent (remote: git@github.com:jsomwarux/agentforce-agent.git)
- **Sync rule**: `cd ~/projects/agentforce-agent && git pull origin main` before any Agentforce work. Push after changes.
- Current state: fully synced as of 2026-03-11. Agents in repo: EcommerceServiceAgent (v1–v24), EmployeeAssistant, InsuranceServiceAgent, LendingApplicationAgent, PMOperationsAgent, TenantServiceAgent + all Apex actions and Flows.
- **Overnight builds allowed** (lifted 2026-03-11): overnight agent CAN build Agentforce agents. Must `git pull origin main` first, push after. B2B Account Service Agent is still banned — do not recreate.
- B2B Account Service Agent: decided against building/adding to site (2026-03-06). Do not recreate. Artifact deleted from Mac mini.

## JT
- Jon Trevor Somwaru | NYC metro | Telegram primary | @jts_14 | @jt__crypto | GitHub: jsomwarux
- BSA background (Spectrum Enterprise 2019–2025): product catalog config, cross-team coordination
- Direct, efficient. Expects Eve to figure things out. Corrects clearly.
- NOT a developer — auto-disqualify roles requiring Apex/SFDX/ML engineering/hands-on coding

## Consulting Niche-Skill Matrix (live — reviewed monthly, not locked)
| Skill | Primary Niche | Secondary Niche | Tertiary/Emerging | Last Score | Why |
|-------|--------------|-----------------|-------------------|------------|-----|
| **Agentforce** | Insurance (COVU anchor) — 24/30 ✅ | Financial Services / RIAs — 21/30 🟡 (emerging) | Mid-large PM/RE (Salesforce shops) | 2026-04-01 | Requires Salesforce — only targets companies already on it |
| **n8n** | Construction + Skilled Trades $5-20M (Aya ref) — 23/30 🟡 | Wholesale Distribution (NYC garment/food/hardware) — 22/30 🟡 | Property Management (AppFolio/Buildium) — 22/30 🟡 rising | 2026-04-01 | Stack-agnostic — targets ServiceTitan, Jobber, QuickBooks, NetSuite users |
- Small PM companies (AppFolio/Buildium, not Salesforce) → n8n, not Agentforce
- Upsell path: land construction/wholesale on n8n → as they grow onto Salesforce → sell Agentforce
- **Last fitness review:** 2026-04-01 | Next: May 1
- **Key findings (April 2026):** Insurance = double down (24/30, extraordinary signal density). PM rising fast (adoption tripled YoY). Construction holds but competition increasing (Zero RFI, Trayd). Financial Services RIA emerging for Agentforce (high SF penetration, large deal sizes). Recommended: add PM as co-equal n8n target; begin Financial Services positioning for Agentforce.
- **Signals accumulator:** memory/niche-fitness-signals.md (reset 2026-04-01)
- Niches are evaluated monthly against alternatives. If a better fit emerges, Eve advises a pivot.

## Positioning (decided 2026-03-31 — permanent)
- **Title across all channels: AI Implementation Specialist** (not "AI consultant," not "AI automation consultant")
- **Differentiator: 6 years enterprise operations at Spectrum Enterprise** — large-scale systems integration, cross-functional product rollouts for a national telecom. This is what separates JT from generalist AI consultants.
- Frame: "enterprise operations background" not "telco background" — the ops experience transfers to all niches (construction, PM, insurance, wholesale)
- Applied to: LinkedIn headline, About section, jtsomwaru.com, resume template, cold-email skill, content-voice.md

## JT Somwaru Consulting
- Target niches: wholesale distribution, property mgmt, construction, insurance ops, skilled trades (NYC)
- Active services: n8n Workflow Automation ($3,500), Agentforce Implementation ($6,500), AI App Development ($4,500)
- New skill: jt-consulting-ops — 5 commands (/client-intake, /process-doc, /runbook, /vendor-eval, /anomaly-audit) at skills/jt-consulting-ops/
- Expansion target: HubSpot — SMB CRM, huge NYC presence, lower Salesforce partner competition. Research: memory/research/enterprise-platforms.md
- Cowork Plugin Implementation: CLOSED 2026-03-11 — requires Claude Team ($125-150/mo) before billing. Wrong market for current SMB ICP. Revisit if a client already on Claude Team asks.
- Avallon/FurtherAI partner pipeline: CLOSED 2026-03-11 — no partner infrastructure at seed stage, JT has no insurance relationships yet. Revisit after landing insurance clients organically.
- ConversationFirst framework built (2026-02-28) — Agentforce UX methodology: persona cards, flow diagrams, 25-pt checklist. Path: memory/drafts/conversationfirst-framework-2026-02-28.md.

## Aya (Client — Construction/Co-living, NYC)
- Project 1: Construction progress dashboard — $1,500 ✅ complete
- Project 2: StreetEasy scraper → Google Sheet (auto-pulls properties meeting criteria every 2 weeks) — $1,000 ✅ signed
- Project 3 (pending): Co-living dashboard app similar to construction dashboard — quoted $2,500, waiting on final feedback. Contact is a member of Aya's co-living business. Said he's busy with a big project.
- Project 4 (in talks): Dashboard + automations for Head of Acquisitions. Sent NDA to review his spreadsheet — no response after 2 follow-ups. Cold for now.
- Strategy: Aya is becoming an anchor client. Each project extends runway and builds referral credibility within their network. Keep relationship warm.

## Strategic Recommendations Log
- File: `memory/strategic-recommendations.md` — written by Weekly Intelligence Synthesis every Sunday
- Format: one entry per week with recommendation, trigger, status (open/actioned/deferred)
- Feeds: morning brief "One concrete action" section + MC task board (sortOrder 6, HIGH priority)
- 🔴 skills demand signals also auto-push MC tasks titled `Positioning: [signal]`

## Content System (updated 2026-03-16)
- Voice rules: `memory/content-voice.md` — **load before every draft.** Platform-specific: LinkedIn = case studies + expertise, X = compression + hot takes. Wednesday LinkedIn is most important post of the week.
- Proof Points inventory + Credibility Test in content-voice.md — every post must pass before publishing
- **LinkedIn: 6 posts/week** (Mon/Tue/Wed/Thu/Fri/Sun) | **X: 7 posts/week + 5-6 banked** (3 technical angles + 2-3 build showcases)
- Pillars: Mon Short Take | Tue Industry Observation | Wed Case Study | Thu Agentforce Proof Point | Fri Tactical Insight | Sat Eve Ops (X only) | Sun Behind the Build
- Content crons: content-generate-linkedin (Mon 7AM, 6 posts) | content-generate-x (Mon 7:25AM, 3 passes: 7 calendar + 3 technical + 2-3 build showcase) | content-reminder (Tue-Sat 8AM, LinkedIn on Tue/Wed/Thu/Fri + X daily) | content-sunday (Sun 9AM, Sun LinkedIn + X + engagement check) | content-monday-send (Mon 7:55AM, surfaces bank posts to JT)
- Content sources: recent-builds.md | technical-angles.md (30+ angles) | consulting-observations.md (nightly from outreach-pipeline) | job-market-observations.md (daily from job-market cron) | content-voice.md Proof Points | Notion swipe file
- Bank: memory/content/bank/[MONDAY-DATE]/ — technical + build showcase posts generated weekly, surfaced to JT Monday morning via content-monday-send
- Swipe file: Notion DB (viral X posts) | Format signals: memory/content/content-signals.md | Technical angles: memory/content/technical-angles.md

## Critic Agent (built 2026-03-07)
- Agent: `agents/critic/AGENT.md` — 4-step strategic critique framework
- Triggers: on-demand `/critic`, soft-signal flag (single line), Sunday 6PM weekly gut-check cron (UUID: d5290646)
- Registered in agents.json ✅
- SOUL.md updated: critic mode activated on /critic or soft-signal detection

## Active Apps
- AgentGuard: AI governance layer — **LIVE at https://agentguard-delta.vercel.app** (March 2026). Confidence scoring + human-in-the-loop + audit log + explainability report. Insurance claims triage demo. **Portfolio card on jtsomwaru.com ✅ (confirmed live 2026-03-22).**
- Vista: movie rating app — **LIVE on Apple App Store** (March 2026)
- Nash Satoshi: crypto game theory rankings (4-LLM ensemble) — GitHub jsomwarux/Nash-Satoshi (private). **Analysis pipeline: PERMANENTLY on Gumloop. Do NOT touch Nash Satoshi n8n workflow or routes.ts unless JT explicitly says so.**
- Glow Index: skincare rankings on Replit — waiting on n8n workflow + ngrok URL
- jtsomwaru.com: live at https://jtsomwaru.com — Next.js on Vercel | Last updated 2026-03-31 (AI Implementation Specialist positioning live; prior: pricing raised, GEO/llms.txt/JSON-LD implemented, nav fixed 2026-03-11)
  - B2B Account Service Agent card: PERMANENTLY BANNED — do not re-add under any circumstances
- Dynasty fantasy football: planned

## Job Market
- Target: AI Solutions Architect, AI Implementation Lead, AI Systems Analyst
- $150K min, $180–220K target | NYC metro or remote only
- ⚠️ Squarespace People AI SA (19/25) — verify still posted before applying.
- Hard rule: do not recommend roles requiring explaining/defending Agentforce internals to technical audiences.
- **Hard rule — application tracking:** IMMEDIATELY after every job application, update `~/projects/job-market-agent/data/job-opportunities.md` — change `Status: new` to `Status: applied | Applied: YYYY-MM-DD`. The morning brief reads from this file and will re-surface applied roles if status isn't updated. No exceptions.
- Skill gaps: AWS Bedrock, LangChain, Copilot Studio.

## Setup State
- Model: anthropic/claude-sonnet-4-6 primary | openrouter/openai/gpt-4o-mini fallback (functional — same OpenRouter provider)
- Auth: anthropic:default uses OAuth subscription token — all Anthropic usage = $0, covered by Claude subscription.
- Compaction: mode=safeguard, reserveTokens=40k, keepRecentTokens=10k, floor=12k
- Providers: anthropic:default ✅ (OAuth) | openrouter:default ✅ (API key, pay-per-use)
- OpenRouter routing: Anthropic → direct (OAuth, $0). All others → openrouter/ prefix.
- Brave Search ✅ | Log redaction: tools ✅

## Passive Income System
- **Bucket**: separate from consulting + career — builds that run autonomously, zero upkeep
- **Active properties**: Nash Satoshi (built, stalled, needs monetization), Glow Index (built, active — analyses running, 4-LLM ensemble live, Tailscale Funnel + n8n wired)

## Ensemble Rankings Strategy (decided 2026-03-24)
- **Model**: individual niche domains (glowindex.com, etc.) — NOT one URL with tabs
- **Platform directory trigger**: build only after 3+ niches have 1k+ monthly visitors each
- **Hard rule**: every new niche gets its own domain deployed via `new-niche.sh` → Vercel. Never add as a tab/sub-path.
- **Glow Index exception**: lives on Replit (legacy). All future niche apps → Vercel.
- **Build system**: `~/projects/ranking-app-agent/` | new-niche.sh scaffolds standalone per niche
- **Vibe Marketing**: ✅ BUILT — agent: `agents/vibe-marketing/AGENT.md` | cron: Mon 4:45AM ET (UUID: 870bf3ff) | active products: Nash Satoshi + Vista
- **Nash Satoshi**: permanently on Gumloop. DO NOT touch Nash Satoshi n8n workflow or routes.ts unless JT explicitly requests.

## Lesson Files (operational, per-system)
Lessons are stored WITH the system they document — not in one central file. This is the canonical reference:
- `docs/agents/ensemble-build-lessons.md` — Python/FastAPI ensemble ranking engine builds only (Nash Satoshi, Glow Index, future niches). NOT for vibe marketing.
- `agents/vibe-marketing/lessons.md` — TikTok slideshow pipeline, Reelfarm API, content generation, Replit deployment. (Created 2026-04-06)
- `projects/n8n-agent/tasks/lessons.md` — n8n workflow patterns and mistakes.
- `spanish/lessons/YYYY-MM-DD.md` — Spanish lesson content.
- Any project with a `lessons.md` or `CLAUDE.md` must be read before touching that project.
- **TikTok routing rule**: niche-specific products → dedicated account. Builder/dev/AI products → @jts_14
- **Passive income scout/strategist**: `dcdbbef5` (Sun 6:30AM) → `4e19c300` (Sun 8:30AM) | reports: `memory/passive-income/`
## Active Cron Jobs (43 total)
> Full list: run `cron list`. Do NOT maintain a manual copy here.

**Key job IDs:** `eve-crypto-morning-008` (6AM daily) | `651fa1da` outreach-pipeline (2AM) | `ebb843af` prospect-discovery (Sun+Wed 1AM) | `be59a068` overnight-autonomy (3AM) | `eve-morning-brief-001` (7:30AM) | `eve-heartbeat-2h-002` (10/14/18/22 ET) | `fe984519` content-linkedin (Mon 6:45AM) | `cb8f29dd` content-x (Mon 7:25AM) | `babd905a` spanish-lesson (Mon-Sat 8:05PM) | `870bf3ff` vibe-generate (Mon 4:45AM) | `b2357bd5` job-app-auto (6:15AM) | `f368e18b` passive-signals (Sat 5:30AM)

**Cap:** 20 invocations/weekday. Groq for midday/evening. Staggered 5-8AM Mondays.
## Cost Tracking
- Script: scripts/cost-tracker.py | Snapshots: memory/costs/YYYY-MM-DD.json (captured 2AM via backup)
- Auth: Anthropic profile uses OAuth subscription token (sk-ant-oat01-*) — NOT an API key. All Claude/Sonnet/Opus usage is $0 in real API charges, covered by flat Claude subscription. No usage appears in Anthropic Console.
- Real costs: OpenRouter and Groq only (used when explicitly routing to non-Anthropic models)
- Alerts: session >$1.50, daily >$15.00, monthly pace >$50 | Goal: <$50/mo real API spend
- Pre-2026-02-28 snapshots zeroed out — were calculated with wrong Anthropic API pricing (phantom costs)
- 2026-02-27: daily hit $10.79 (over $10 limit) — driven by Writer SA sub-agent (27k tokens) + morning brief + niche monitor. Consider raising daily threshold to $15 or reducing sub-agent token usage.

## Portfolio Auto-Updater
- Repo: ~/projects/jtsomwaru-com/ → Vercel (auto-deploy on main push)
- Agent: agents/portfolio-updater/AGENT.md | Queue: agents/portfolio-updater/queue.jsonl
- Runs: nightly as final step of overnight agent (3 AM)
- Auto-approves score ≥7/10 | Flags 4–6 to JT | Skips <4
- Demand reorder: weekly — featured projects ranked by skills-demand-tracker scores
- Site files: src/data/projects.ts | src/components/project-graphics/index.tsx | src/components/About.tsx
- Triggers: overnight builds, JT says "done/shipped", consulting completions, MC tasks flipping to done, in-session builds (via AGENTS.md rule)
- Morning brief: shows 🌐 Site Updated if anything was added overnight

## Spanish Learning System
- Started: 2026-03-02 | Level: A1+ (high beginner, dormant HS Spanish)
- Goal: Casual conversation with girlfriend + her family | Focus: speaking, not writing
- State: `~/.openclaw/workspace/spanish/state.json`
- Curriculum: `~/.openclaw/workspace/spanish/curriculum.md` (4 weeks mapped)
- Lessons: `spanish/lessons/YYYY-MM-DD.md` | Evaluations: `spanish/evaluations/`
- Crons: spanish-lesson (Mon–Sat **8:05PM ET**, UUID: babd905a — staggered from 8PM 2026-03-12 to avoid crypto-evening rate-limit collision) | spanish-eval (Sun 8PM ET, UUID: 012216b9)
- Accountability: 10PM heartbeat checks state.json → nudges if lesson not complete
- Voice: JT sends voice message → Groq whisper-large-v3 transcription → Claude evaluates (max 2 corrections per response)
- Real-world challenges unlock weekly (Week 1: say buenos días to someone)

## Automation Infrastructure
- Cleanup: scripts/cleanup-sessions.py | 3AM | Backup: scripts/backup.sh | 2AM | 7-day retention
- Mission Control: http://localhost:3000 + port 3210 (Convex)

## Crypto
- Primary income: crypto | Forward bet: x402 protocol
- Portfolio (21 coins as of 2026-03-24 — pulled live from Google Sheet each run): $KELLYCLAUDE, $FELIX, $A0T, $PRXVT, $NOX, $JUNO, $ODAI, $PERKOS, $MOLTEN, $FDRY, $NOOK, $CLAWNCH, $CLAWD, $DREAMS, $ZAUTH, $DEXTER, $TAKEOVER, $ROBOTMONEY, $SERV, $WORK, $BOTCOIN
- Coin intelligence: crypto-agent/data/coin-intelligence/TICKER.md per coin
- $JUNO note: previously EXIT-rated — JT re-entered, agent will re-analyze fresh each morning

## Financial Situation (updated 2026-03-23)
- Monthly burn: $2,174 (rent $1,050 + expenses $550 + subs $574). Subscriptions: Claude $200 | Gumloop $194 | LinkedIn $65 | X $40 | Replit $25 | Supabase $25 | Gsuite $14 | Higgsfield $9 (locked until Jan 2027).
- Crypto: ~$10K, declining. Income: $30/mo net (Aya scraper). No savings buffer.
- UI: ~$500/wk est. Backpay ~17 weeks = ~$8,500 lump sum incoming. ~9 weeks ongoing after (~$4,500). Total ~$13,000.
- Runway: ~$23K total, ~11 months at current burn. UI cliff in ~9 weeks post-lump sum — job in 60-90 days solves burn permanently.
- North Star: financial independence, passive income streams, luxury travel.

## Key Decisions
- **Priority order (updated 2026-03-23 — RUNWAY CRITICAL)**: Job applications PRIMARY. Every qualified role (20+/25, hard filters) gets an application. Threshold: 20+/25, no hands-on coding primary, no SE/technical pre-sales. Active: Impulse Latam (3-31), Arya Health (4-01), ~~Lightstone $175-300K~~ ✅ APPLIED 4-09, Ramp (18/25 — vibe coder/Gumloop fit), Qvest $140-170K (4-02), Gong $148-225K (4-02), Tenex 23/25 (4-02), ~~Zoom AI Transformation~~ ✅ APPLIED 4-06, ~~Morgan Stanley GenAI Change Management~~ ✅ APPLIED 4-06, ~~Axios $130-165K~~ ✅ APPLIED 4-09. ~~OpenAI AI Deployment Manager~~ REJECTED.
- **Agentforce job filter**: Do not recommend roles requiring explaining/defending Agentforce internals. JT builds/deploys agents but not comfortable in SE/technical pre-sales Agentforce contexts.
- **Outreach**: T1: H.C. Oswald (sent 2026-03-11, awaiting). T2: Brothers Supply + Independent Pipe. T3: cold batch (sender build pending). Templates: construction ✅ + PM maintenance ✅. Tier 3 scheduler: still needed.
- Outreach tiers: T1 Custom (2-4/mo) | T2 Template (8-12/mo) | T3 Cold Hook (50-100/mo, replies promote to T2).
- n8n over Make.com. Model tiering: MiniMax m2.7 as default (cheapest, handles most work), Sonnet 4 upgrade when needed, Opus 4 for n8n workflow generation and complex multi-file Python (quality × no-rework ROI). HubSpot = best consulting expansion platform (lower SF competition). Training system: Kobe Protocol — self-improvement via SYSTEM not model weights.
