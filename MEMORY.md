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
- Agentforce overnight builds: ✅ ALLOWED (lifted 2026-03-11). Must `git pull origin main` first. B2B Account Service Agent is PERMANENTLY BANNED — do not recreate under any circumstances.
- `launchctl unload/load` mid-session = gateway goes offline. Warn JT first. Defer to JT-initiated restart if possible.

## Infrastructure (updated 2026-03-15)
- OpenClaw version: 2026.3.13 (updated 2026-03-15)
- bootstrapMaxChars: 32000 (raised from default 20k on 2026-03-17 — gives AGENTS.md ~7k headroom at current 25,197 chars)
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
| Skill | Primary Niche | Secondary Niche | Why |
|-------|--------------|-----------------|-----|
| **Agentforce** | Insurance (COVU anchor) | Mid-large PM/RE (Salesforce shops) | Requires Salesforce — only targets companies already on it |
| **n8n** | Construction + Skilled Trades $5-20M (Aya reference) | Wholesale Distribution (NYC garment/food/hardware) | Stack-agnostic — targets ServiceTitan, Jobber, QuickBooks, NetSuite users |
- Small PM companies (AppFolio/Buildium, not Salesforce) → n8n, not Agentforce
- Upsell path: land construction/wholesale on n8n → as they grow onto Salesforce → sell Agentforce
- **Last fitness review:** not yet run (system launched 2026-03-06) | Next: April 1
- **Signals accumulator:** memory/niche-fitness-signals.md (reset monthly)
- Niches are evaluated monthly against alternatives. If a better fit emerges, Eve advises a pivot.

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
- jtsomwaru.com: live at https://jtsomwaru.com — Next.js on Vercel | Last updated 2026-03-11 (pricing raised, GEO/llms.txt/JSON-LD implemented, nav fixed)
  - B2B Account Service Agent card: PERMANENTLY BANNED — do not re-add under any circumstances
- Dynasty fantasy football: planned

## Job Market
- Target: AI Solutions Architect, AI Implementation Lead, AI Systems Analyst
- $150K min, $180–220K target | NYC metro or remote only
- ⚠️ Squarespace People AI SA (19/25, $126–180K hybrid NYC) — posted Feb 21, likely expired. Verify before applying.
- ~~Salesforce Lead Agentforce SE~~ — PASSED 2026-03-18. Role required deep technical Agentforce conversations JT isn't comfortable with yet. His Agentforce capability is agent-configured, not hands-on. **Hard rule going forward: do not recommend roles where core responsibility is explaining or defending Agentforce internals to technical audiences.**
- ~~🟠 Salesforce Agentforce/AI Deployment Strategist (20/25, $140K–$185K)~~ — EXPIRED/REMOVED 2026-03-19. JR305206 returns 404 on both Salesforce Careers and Workday. Do not resurface.
- ~~Salesforce Sr. Supply Chain Strategist~~ — REMOVED 2026-03-22. Domain requirement is a hard disqualifier (requires actual supply chain ops expertise, not just Agentforce). Score corrected to 11/25.
- ~~Writer SA East (20/25, $207K–$250K hybrid NYC)~~ — TAKEN DOWN 2026-03-22. Do not resurface.
- ⛔ OpenAI AI Deployment Engineer (18/25, NYC hybrid) — evaluated 2026-03-18, skipped. Python/JS proficiency + infra ownership required explicitly. Below 24+ threshold.
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
- **Vibe Marketing System**: ✅ BUILT 2026-03-12 — weekly content generation for passive income products
  - Agent: `agents/vibe-marketing/AGENT.md` | Registry: `agents/vibe-marketing/product-registry.json`
  - Queue: `agents/vibe-marketing/queue.jsonl` | State: `agents/vibe-marketing/state.json`
  - Cron: Monday 4:45AM ET (UUID: 870bf3ff-55c9-49c0-9970-361c81a0920b) | isolated sonnet | 720s
  - Active products: Nash Satoshi + Vista (Glow Index pending n8n/ngrok)
  - Nash Satoshi: nashsatoshi.com | X: @NashSatoshi | TikTok: @NashSatoshi (created 2026-03-20, warmup in progress — first post eligible after Monday 4:45AM vibe marketing cron) | Reddit: community account (needs karma build) | **Analysis pipeline: PERMANENTLY on Gumloop (hard rule — no n8n changes unless JT explicitly requests)**
  - Vista: App Store | X: @jts_14 | TikTok: @jts_14 | Reddit: JT's personal account (needs karma build)
  - Glow Index: TikTok dedicated account required when activated (skincare niche ≠ JT's audience)
  - TikTok routing rule: niche-specific products (crypto, skincare, etc.) → dedicated account. Builder/dev/AI products → @jts_14
  - Platforms: X (weekly) + TikTok (weekly) + Reddit (weekly, alternating subreddits) + LinkedIn (monthly, 1st Monday)
  - JT always approves before posting — manual for first 1–2 weeks, then PostBridge auto-scheduling
  - Add new product: one entry in product-registry.json with status:active → picked up next Monday
- **Vibe Marketing Agent**: NOT yet built — JT will provide detailed instructions separately
- **Scout agent**: `agents/passive-income-scout/AGENT.md` | state: `agents/passive-income-scout/state.json`
- **2-stage pipeline**: Scout (Sun 6AM) → Strategist (Sun 7:30AM)
- **Scout cron UUID**: `dcdbbef5-2f16-4f3d-81ab-78e1b34f6fd0` | Sun 6AM ET | generates 5 raw ideas → saves report
- **Strategist cron UUID**: `4e19c300-d387-4019-b658-9664f0d665d5` | Sun 7:30AM ET | deep analysis, 8-dimension scoring, pushes 🟢 winners to MC, sends Sunday Telegram digest
- **Scout reports**: `memory/passive-income/YYYY-MM-DD-scout.md` | **Strategist reports**: `memory/passive-income/YYYY-MM-DD-strategist.md`
- **MC project tag**: `passive-income` | Nash Satoshi + Glow Index tasks tagged

## Active Cron Jobs (24) — post-incident schedule (2026-02-26)
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
- outreach-pipeline: 2AM daily | isolated sonnet | T2: 3/night (was 2) research→brief→DM→Drive; **Salesforce verification pass** (3 insurance T3s/night checked, auto-upgrades to T2 when confirmed); T3 cold hook batch (10/night); **template gate**: construction + PM T2s blocked until templates built | UUID: 651fa1da-84d7-44b3-8e10-6a46e1c05cf6
- prospect-discovery: **Sun + Wed 1AM** | isolated sonnet | Sunday = all 4 niches (20-30 prospects); Wednesday = Agentforce/insurance focused (15-20 prospects, Salesforce confirmation attempts) → Telegram summary | UUID: ebb843af-e752-4c65-923d-540d5ff5ad3f
- passive-income-scout: Sunday **6:30AM** ET | isolated sonnet | trends → 5 raw ideas → saves report (no MC push, no Telegram) | UUID: dcdbbef5-2f16-4f3d-81ab-78e1b34f6fd0 (rescheduled 2026-03-15 from 6AM)
- passive-income-strategist: Sunday **8:30AM** ET | isolated sonnet | reads Scout report → deep 8-dimension analysis → pushes 🟢 winners to MC → sends Sunday digest to Telegram | UUID: 4e19c300-d387-4019-b658-9664f0d665d5 (rescheduled 2026-03-15 from 7:30AM)
- monthly-goals-gap: 1st of month 8AM | isolated sonnet | job market vs. Eve capabilities audit → MC/Skills queue | UUID: fdc2cf75 (ran 2026-03-01 ✅)
- monthly-niche-fitness: 1st of month 9:30AM | isolated sonnet | scores current niches vs. alternatives, advises pivot/shift/stay | UUID: 1e2cf966
- content-generate-linkedin: Monday 7:00AM ET | isolated sonnet | generates 4 LinkedIn posts → saves weekly file → uploads to Content/LinkedIn | UUID: fe984519
- content-generate-x: Monday 7:25AM ET | isolated sonnet | generates 7 X posts → appends to weekly file → uploads to Content/X | UUID: cb8f29dd
- content-generate (DISABLED): UUID 98fda582 — was timing out at 40+ min, replaced by above split crons
- content-monday-send: Monday 7:55AM ET | isolated sonnet | sends Monday LinkedIn + X to JT | UUID: d4dedeb1 (bumped from 7:45AM)
- content-reminder: Tue–Sat 8AM ET | isolated sonnet | sends that day's post (LinkedIn on Wed/Fri) | UUID: 5e66b4ee
- content-sunday: Sunday 9AM ET | isolated sonnet | sends Sun LinkedIn + X + engagement check | UUID: d918122d
- t3-cold-hook: Tue/Thu 6AM ET | isolated sonnet | reads T3 shortlists → drafts 8-10 cold hook DMs → uploads batch to Drive (Consulting/Clients/T3 Batches/Outreach/LinkedIn) → Telegrams JT with Drive link for review | UUID: 3ed01a8a-c3fb-4673-9ae0-993611e94c5a | **JT always sends — agent drafts only**
- weekly-systems-review: Sunday 10AM ET | isolated sonnet | cron health + file budgets + process health + config drift + version check → Telegram report | UUID: b2ca53ab-0c07-4a22-8424-9d39bf988405
- **NOTE (2026-03-15):** weekly-synthesis payload updated to include Future Signals Review + content signal → MC push (was logging signals but not converting them to tasks)
- **NOTE (2026-03-15):** construction-trades.md + property-management.md shortlists created (prospect-discovery was writing to non-existent files)
- **NOTE (2026-03-20 — self-improvement audit):** Full audit of all self-improvement systems. Fixes applied: (1) PostBridge → HIGH sortOrder 45 — unblocks entire content feedback flywheel; (2) weekly-synthesis timeout 300s→720s; (3) daily-news-hook staggered to 9:30AM (was 9:15AM, rate-limit collision with niche monitor); (4) prospect-discovery switched from Edit tool to shell append — fixes file-size write failures; (5) HEARTBEAT.md: added autoresearch enrollment check (step 9) + idea queue pruning (step 10) + content→consulting niche feedback rule to weekly synthesis; (6) overnight agent: explicit autoresearch volume trigger check added (Step 1.6) — runs cold-email loop if >14 days since last run; (7) autoresearch AGENT.md: volume trigger documented. Key finding: vibe marketing performance-log.jsonl has 0 entries — entire feedback flywheel blocked on PostBridge activation.
- reddit-karma-daily-reminder: 8PM daily | isolated groq | sends daily Reddit karma habit reminder to JT | UUID: fe575759-c8b1-4715-ae5a-0dbe034b3c9b
- job-app-auto-builder: 6AM daily | isolated sonnet | checks job-opportunities.md for status:new 20+/25 roles → builds resume + cover letter .docx → uploads to Drive → pushes "Review + Submit" HIGH MC task to JT | UUID: b2357bd5-651d-4151-80df-49e4a928826f | silent if no qualifying roles
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
- Portfolio (7 coins as of 2026-02-26): $MLTL, $KELLYCLAUDE, $FELIX, $NOX, $SELFCLAW, $JUNO, $PRXVT
- Coin intelligence: crypto-agent/data/coin-intelligence/TICKER.md per coin
- $JUNO note: previously EXIT-rated — JT re-entered, agent will re-analyze fresh each morning

## Financial Situation (updated 2026-03-23)
- Monthly burn: $2,174/month (rent $1,050 + expenses $550 + subscriptions $574 after SuperGrok cancellation)
- Subscriptions breakdown: Claude $200 | Gumloop $194 (105k credits, Nash Satoshi 680/run) | LinkedIn $65 | X $40 | Replit $25 | Supabase $25 (DB for Nash Satoshi/Vista/Glow Index) | Gsuite $14 | Higgsfield $9 (locked yearly until Jan 2027 — do not renew)
- SuperGrok cancelled 2026-03-23 (was $30/mo — Grok now via OpenRouter if needed)
- Crypto: ~$10K, DECLINING. Market down, withdrawing to cover burn.
- Income: $30/mo net (Aya scraper $75/mo, ~$45 costs). 
- No savings buffer. Zero.
- Aya $1,000 scraper: paid out.
- **Unemployment (filed, backpay to December):** NY max is $869/wk (raised Oct 2025). JT estimate ~$500/wk. Backpay ~17 weeks = ~$8,500 lump sum incoming within weeks. BUT those weeks count against 26-week max, so only ~9 weeks of ongoing weekly payments (~$4,500) remain after lump sum hits.
- **Total UI benefit: ~$13,000**
- **Updated runway: ~$23K total ($10K crypto + $8.5K lump sum + $4.5K ongoing UI) = ~11 months at $2,040/mo burn.** After UI exhausts (~9 weeks), back to burning crypto unless income lands.
- North Star: financial independence, multiple passive income streams, controlled work hours, luxury travel, nice house near major city, take care of parents.
- **Implication: runway is real but has a cliff. UI weekly payments end in ~9 weeks post-lump sum. Job landing in 60-90 days is still the priority — it solves burn permanently.**

## Key Decisions
- **Priority order (updated 2026-03-23 — RUNWAY CRITICAL)**: Job applications are now PRIMARY, not a hedge. With ~4-5 months runway and declining crypto, a $150K+ role closing in 60-90 days is the most reliable lifeline. Volume must go up — not 2-3/week, but every qualified role (20+/25, passes hard filters) gets an application. Consulting runs in parallel but cannot be treated as the primary income plan on this timeline. Threshold: score **20+/25** with hard filters still in place (no hands-on coding primary, no technical pre-sales SE, no explicit Python/JS proficiency as hard requirement). Only active application: OpenAI AI Deployment Manager (applied 2026-03-18).
- **Agentforce job filter (added 2026-03-18)**: Do not recommend roles where a core responsibility is explaining, defending, or technically advising on Agentforce internals. JT's Agentforce capability is agent-configured. He can build and deploy agents but is not comfortable in deep technical Agentforce conversations with clients or SE/sales engineering contexts.
- **Outreach active as of 2026-03-09**: freeze lifted. T1: H.C. Oswald — outreach sent 2026-03-11 (LinkedIn DM + subject "After-hours coverage for your catalog"). Awaiting response. T2: Brothers Supply + Independent Pipe (overnight eligible). T3: cold batch (sender build pending).
- **Outreach tier system**: T1 Custom (2–4/mo, full pipeline, JT reviews), T2 Template (8–12/mo, niche demo configured per prospect, overnight can run), T3 Cold Hook (50–100/mo, no demo upfront, replies promote to T2). Niche templates: wholesale (convert existing demo — still needed), **construction job-tracker ✅ BUILT 2026-03-15** (`~/projects/n8n-agent/clients/construction-template/`), **PM maintenance triage ✅ BUILT 2026-03-15** (`~/projects/n8n-agent/clients/pm-maintenance-template/`). Tier 3 send scheduler: still needed.
- Aggressive compaction over safeguard — prevents context resets on long builds
- OpenRouter for non-Anthropic models — direct key only if model >$5/mo
- Sonnet default over Opus — caching = 80% as capable at 20% cost
- n8n over Make.com — self-hosted, no per-task pricing at scale
- Training system (Kobe Protocol, 2026-02-28): self-improvement via better SYSTEM (memory, rules, prompts) not model weights. Monthly gap analysis cron is the anchor.
- HubSpot = best JT Somwaru Consulting expansion platform (2026-02-28): SMB CRM, NYC penetration, lower partner competition than Salesforce
