# MEMORY.md — Current Operating Context
> Main-session long-term context. Do NOT load in group/shared chats. Full archive: `docs/memory/MEMORY-full.md`; pre-optimization snapshot: `docs/memory/archive/MEMORY-before-optimization-2026-04-26.md`.
> This file is intentionally compact: preserve only durable context, current status, and decisions Eve needs at startup. Historical detail belongs in daily notes or archive.

## Load Order / File Authority
- `AGENTS.md` = operating rules + hard constraints; `TOOLS.md` = commands, paths, API usage; `USER.md` = JT profile; `SOUL.md` = tone/persona; `HEARTBEAT.md` = proactive wake behavior.
- `MEMORY.md` owns current decisions/status. If a fact changes here, update every file that references it.
- Never raise `agents.defaults.bootstrapMaxChars` above 32,000. If bootstrap truncates, optimize files rather than increasing the firehose.

## JT Snapshot
- Jon Trevor Somwaru, “JT”; timezone America/New_York; Telegram primary; direct, low-ceremony, expects Eve to figure things out before asking.
- Background: Business Systems Analyst at Spectrum Enterprise/Charter; strong business-ops + tech translation edge.
- North Star: financial freedom and control over time. Ideal state = multiple high-earning, low-maintenance income streams, ideally managed by specialized AI agents that only escalate urgent decisions; bills paid, no debt spiral, money for nice things for him and family, and freedom to build creative apps/client work with a clear path to success.
- Current priority order: (1) AI implementation consulting, (2) app building + marketing toward eventual passive income, (3) crypto market monitoring/opportunity scanning, (4) health daily as the foundation.
- Income thresholds: safe ≈ $10K/mo, free ≈ $30K/mo, rich ≈ $100K/mo.
- Wants to be known primarily as an AI Implementation Specialist/Consultant and product builder.
- Current focus: AI consulting agency, Aya client work, portfolio credibility, content engine, selective AI implementation/job-market opportunities, crypto as primary income stream.
- Constraints: not positioning as hands-on developer; avoid Apex/SFDX/ML-engineering roles. Job target: AI Solutions Architect / AI Implementation Lead, $150K min, $180–220K ideal, NYC/remote only. Non-negotiables: sleep, health, and staying in NYC/location stability.

## Hard Rules / Security Essentials
- Never modify `openclaw.json` auth, `summaryModel`, `summaryProvider`, primary model, `auth-profiles.json`, or `models.json` without JT approval.
- Never store or paste API keys outside approved auth/env files. Redact secrets in shareable files and Drive uploads.
- Never send messages to third parties on JT’s behalf. Draft, save, and summarize; JT presses send.
- Sacred files are edit-only/append-only: `~/.config/env/global.env`, `~/.openclaw/openclaw.json`, `~/.openclaw/credentials/*`, `memory/content/content-signals.md`.
- Use `trash` over `rm` when removing user/workspace files.

## Consulting Positioning
- Brand: JT Somwaru Consulting / JT Somwaru Consulting direction. Positioning: “practical AI implementation for ops-heavy SMBs” — workflows, dashboards, agents, and integrations that save time or surface revenue.
- Differentiator: JT speaks operations and technology; sells implementation outcomes, not abstract AI strategy.
- Target ICP: NYC/metro SMBs in construction, wholesale distribution, property management, skilled trades; HubSpot is a strong expansion platform due to less Salesforce competition.
- Outreach tiers: T1 custom 2–4/mo; T2 template 8–12/mo; T3 cold hook 50–100/mo, replies promote to T2. JT sends all outreach.
- Preferred stack: n8n over Make.com for client automation; Agentforce when Salesforce/Data Cloud fit the client.

## Active Client: Aya
- Anchor client. Completed: $1,500 dashboard.
- Active: $1,000 StreetEasy scraper.
- Pending: $2,500 co-living dashboard.
- Stalled: acquisitions dashboard.
- Treat Aya as proof-point source when shipped work has concrete outcome; update proof points/recent builds/content angles immediately when completed.

## Pipeline / Business Development
- H.C. Oswald: hold outreach until personal site is polished and demo agents are built.
- Consulting pipeline lives under `~/projects/jt-consulting-pipeline/`; client folders contain research, deck, outreach draft, and pipeline status.
- After deck/outreach stages, sync with `python3 scripts/pipeline_drive_sync.py --slug [slug] --client "[Name]" --stage all` and include Drive links for JT review.
- When JT says outreach was sent, same-turn run `scripts/outreach_update.py` with slug/company/message/channel/date; update daily note.

## Consulting Delivery System — Services-as-Software
- New client rule: when JT mentions a new/active/signed client or real paid/discovery engagement, remind him to document rigorously and initialize the Client OS template in the client folder immediately.
- Services-as-software model adopted 2026-05-01: sell finished outcomes, not tools. Manual delivery collects data/edge cases before automation.
- Every active client gets Client OS (`skills/opticfy-ops/templates/client-os/`): dashboard, weekly updates, decision/workflow/failure/automation/metrics/quarterly files, raw/cleaned inputs, tagged outputs.
- Retention: SaaS-like visibility + weekly cadence + quarterly buyer review. Moat: delivery IP/training data before agents/software.
- Offer filter: outsourced line item, intelligence-heavy, services spend > software spend, manually documentable. Two ghosts = targeting/offer signal. Scale delivery before marketing/sales.

## Consulting Niche-Skill Matrix
- Last reviewed 2026-05-01. Full matrix archived at `docs/memory/consulting-niche-skill-matrix-2026-05-01.md`.
- Current consulting lane remains SMB operational AI implementation: workflow cleanup, dashboards, automation, vendor/tool integration, and reusable delivery IP.

## Current Apps / Products
- `jtsomwaru.com`: portfolio site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push.
- Glow Index: skincare rankings on Replit/GitHub. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store pending.

## Content System
- X is primary growth channel; LinkedIn for case studies/proof; Reddit for project promotion when appropriate.
- Before drafting posts: read `memory/content-voice.md`; no preamble, no em dashes, no “Here’s the thing,” standalone posts 6–15 words when requested.
- Swipe-file rule: content generation must fetch Notion Viral Posts Swipe references first (`python3 scripts/notion-swipe-fetch.py --limit 12 --min-engagement 500`) and include hook mappings in saved weekly/one-off draft files. Priority swipe niches: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
- Sports GM / @dynastyjig Phase 1 is active: source stack + receipts system live in `memory/sports-gm/`, reusable skill at `skills/sports-gm/SKILL.md`, price fetcher `scripts/sports_gm_fetch_prices.py`, report generator `scripts/sports_gm_generate_report.py`, weekly cron Tuesday 9AM (`008a349c-af59-4e6b-88bb-97f65dba61c6`) and Sports GM source model corrected 2026-04-27: primary sources are KTC, FantasyCalc, FantasyPros; DynastyProcess is secondary sanity-check only; never compare raw cross-source values, compare ranks/position ranks/rank deltas. Daily @dynastyjig post-pack cron at 8:30AM (`1e614c8a-adb8-4a02-b35f-3031db55b337`) now generates niche-native traction content, not app-centric promo: 2 dynasty fantasy posts, 2 sports betting posts, and 1 bridge post using Action Arena and Dynasty Simulator only as invisible backdrops. Drafts should earn trust from dynasty managers/bettors through relatable strategy, league psychology, public accountability, timing, regret, risk, and group-chat pressure. Product names are banned by default in daily drafts; mention lane only in internal angle notes. Avoid generic player-eval packs unless the player take supports a sharper niche-native strategy thesis. Drive folder for new packs: `Eve — Drafts / Content/Sports GM/DynastyJig/X/Niche-Growth/YYYY-MM`; existing daily Reddit growth cron `reddit-daily-gen` (`bbe49024-458a-4496-9c7c-7a278615810f`) uses Sports GM rules for dynasty/fantasy Reddit content.
- Notable completed work triggers: update proof points, recent builds, technical angles if useful, generate content when rubric passes, upload substantive deliverables to Drive.
- Wednesday LinkedIn case studies use `skills/wednesday-linkedin/SKILL.md`.

## Job Market
- Target only AI implementation / AI Solutions Architect / AI Implementation Lead roles that value BSA + ops automation background.
- Avoid pure software engineering, ML research, Apex/SFDX-heavy Salesforce developer, relocation, or sub-$150K roles.
- Resume/cover letter packages must use Sonnet model via job-application skill; save local markdown + generate docx + upload to Drive.

## Crypto / Finance
- Crypto is JT’s primary income stream. x402 is a forward bet.
- Financial safety: never trade, transfer, spend, or execute financial transactions. Conway constraints: max $5/action, max 2 VMs, wallet <$10 means do not spend.
- Morning crypto cron and Nash Satoshi ranking content are operationally important; missed critical crons should be detected and fired per HEARTBEAT rules.

## Infrastructure / OpenClaw State
- 2026-04-26: recovering from April OpenRouter cost crisis ($0 balance/hibernation on Apr 24–25; funded again Apr 26). Operate in conservation mode: avoid unnecessary heavy agents, watch cost alerts, and prefer bounded checks.
- OpenRouter active. Current tiering: MiniMax m2.7 default, Sonnet 4.6 upgrade for complex reasoning/job apps, Opus 4.6 only for high-precision n8n/complex code when ROI justifies it. Use aliases when possible.
- Google Drive OAuth is currently a blocker for outreach uploads; JT needs to run `python3 ~/.openclaw/workspace/scripts/drive_auth.py` before Drive-dependent pipeline work.
- LCM/lossless-claw is active; use `lcm_grep` → `lcm_describe` → `lcm_expand_query` for prior conversation recall before asserting specifics.
- Gateway restart path: prefer `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`; do not raw restart/config patch unless explicitly approved.
- Mission Control dashboard: `http://localhost:3000`; remote tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n remote path `/n8n`.
- Critical workspace commands and paths are in `TOOLS.md`; consult it before saying “I can’t.”

## Active Automation / Crons
- Keep daily cron invocations ≤20. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM EST.
- Morning brief, heartbeat, job-market, niche monitor, crypto morning, content/weekly synthesis, Weekly North Star Review, cost tracking, and health check-ins are active responsibilities.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75.
- Kobe Protocol: daily film review at 10AM and weekly skills audit. Mistake entries require failure + root cause + prevention rule.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- 2026-04-26: consulting acquisition wedge: sell contained 7-day ops bottleneck audits/prototypes, not broad “AI transformation.” First workflows: property maintenance triage, construction field-note→punch-item/customer-update, wholesale stock/ETA/order-status reply drafts with human approval.
- 2026-03-31: consulting positioning is permanent until explicitly changed: practical AI implementation for ops-heavy SMBs.
- 2026-03-23: no anime/NBA apps right now; prioritize B2B consultable products and client-work proof.
- AgentSync concept deferred unless a direct need appears; Mission Control already provides enough orchestration.
- Zapier MCP integration not needed now; n8n MCP + MCP-router covers needs.
- Railway MCP: not needed now; revisit only for multi-service deployments.
- Selenium MCP still needed despite Cloudflare `/crawl` because browser automation remains useful.
- x402 opportunity: Coinbase x402 Bazaar could enable buyer-agent/seller-agent MVP; verify APIs/docs before building.

## Integrity / Fabrication Corrections
- Never claim outreach/messages were sent unless tool/script evidence confirms it.
- Never fabricate URLs, deployment state, GitHub status, Drive links, or task closure. Verify with tools.
- If corrected by JT, immediately update the Mistakes Log/rules before moving on.

## Setup State
- 2026-04-26: Installed `birdclaw` (local X archive workspace) and `gog` (Google Workspace CLI). Workflow rules live in `docs/tools/local-archives-workflows.md`; JT auth/import tasks created before recurring use.

## Automation
- Nightly friction audit cron active: `nightly-friction-audit` at 9:45PM ET. Purpose: choose tomorrow’s top priority, prep one blocker, and ask “Imagine tomorrow succeeds. What friction did we remove tonight?”
- Guyana opportunity monitor active: weekly Monday 12PM ET cron `guyana-economic-opportunity-monitor`; reads existing Guyana research, checks verified live sources, sends concise brief, and creates up to 3 Mission Control tasks only for sourced actionable findings.
- Passive-income pipeline audited 2026-04-27: canonical weekly flow is signal fetch Sat 5:30AM ET → Scout Sun 6AM ET → Strategist Sun 7:30AM ET. Duplicate legacy Scout/Strategist crons disabled. Scout now includes AI vision capability scan as one non-overweighted lens; Strategist validates vision defensibility/cost/risk. Sources include Exploding Topics, Google Trends/pytrends, Brave trend signals, APIs.guru, Product Hunt, HN, and RapidAPI/developer search.

- Weekly North Star Command Center cron active: Sunday 6PM ET (`29772d9b-e007-4f62-9df9-e80b73d0cd21`) scores lanes, revenue path, product portfolio calls, and overinvestment risks against JT’s financial freedom/control-over-time North Star.

- Consulting Sales Engine state file: `memory/north-star/consulting-sales-engine.md`; integrated into Weekly North Star Command Center to track pipeline health, follow-ups, stale prospects, and fastest next consulting dollar.

- North Star OS layers implemented under `memory/north-star/`: revenue command center, consulting sales engine, proof/distribution, product growth, opportunity intake gate, health constraint layer, and weekly rubric; all integrated into Weekly North Star Command Center cron.
## Active Client — Altmark Group
- Status: Active AI implementation client as of 2026-04-30. Yair, CFO, reached out to JT on Twitter; JT met him at Altmark's Bronx office, scoped automation systems, created revised proposal, and has started delivery.
- Proposal: AI Operations Build for Altmark Group, revised April 2026. Total proposed buildout: $34,750 + $1,500/month support, 3-month minimum after buildout. Foundation setup listed at $4,000; six use cases over ~8–10 weeks, with foundation + first use case live within ~2 weeks of Navid infrastructure session.
- Current progress: insurance expiration workflow finished; dedicated PC set up and planned for delivery to Altmark office next week; rent delinquency workflow pending 50% deposit before work begins.
- Positioning proof: local-first/self-hosted operations automation for property/ops team; QuickBooks Desktop/server environment; audit trails; human-in-the-loop financial actions; no SaaS/vendor lock-in.
- Client status file: `memory/clients/altmark-group/status.md`; proposal extraction: `reports/clients/altmark-group/proposal-extracted.txt`.
## Altmark / Family Office Expansion Strategy
- Yair, Altmark Group CFO, mentioned he may be able to connect JT to ~15 other NYC-area family offices likely interested in similar automation systems.
- Strategic goal: finish Altmark systems, convert Altmark into monthly support/maintenance retainer, continue building additional Altmark automations, then use Yair as referral channel/case-study wedge into other NYC family offices.
- This makes Altmark the top consulting revenue/proof lane and a potential repeatable offer for local family offices/property/financial operations teams.
## Live Opportunity — Marketsmith
- Status as of 2026-04-30: live consulting/freelance opportunity. Marketsmith chief of strategy is a family friend and reached out about new product initiatives. JT met with head of talent acquisition on 2026-04-29; she said they are very open to consulting/freelance work and mentioned MSIGenerate + `msitheagency.com`.
- JT quoted $175/hr or $15k/month, 15 available hours/week, deliverables-focused rather than fixed hours.
- Next step: head of talent acquisition will talk with product team about fit and follow up. No response yet as of 2026-04-30 8:04 PM.
- Strategic fit: high-value consulting/product opportunity aligned with AI Implementation Specialist + product builder positioning; avoid being converted into generic employment-style role unless explicitly desired.
- Status file: `memory/opportunities/marketsmith/status.md`.
## Product Portfolio Update — 2026-04-30
- Apps/products: Action Arena and Dynasty Fantasy Football Simulator remain important sports/product lanes. Vista has launched and has ~10 active users. Automated TikTok slideshow organic growth loops are currently running for both Nash Satoshi and Vista.
- JT wants to build many stored passive-income ideas and run automated organic marketing strategies for them to maximize probability of passive/semi-passive income streams. Guardrail: many bets are acceptable only when maintenance is low, distribution loop exists, metric is tracked, and kill/pause threshold is explicit.

## Consulting Acquisition Update — 2026-04-30
- JT reported no responses to cold outreach sent so far. Treat as data: acquisition strategy needs review, not just more cold volume. Prioritize warm/referral lanes (Altmark/Yair family-office intros, Marketsmith family-friend/product lane), proof-led LinkedIn, local NYC relationship channels, and trigger-based outreach backed by proof.
## North Star Strategy Synthesis — 2026-04-30
- Altmark + Marketsmith now dominate near-term North Star strategy. Altmark is active $34,750 buildout + $1,500/mo support potential + Yair referral channel into ~15 family offices. Marketsmith is live consulting/freelance opportunity already anchored at $175/hr or $15k/mo.
- Consulting acquisition priority should shift from generic cold outreach to warm/referral/proof-led channels: Altmark delivery → Yair referrals, Marketsmith product-team fit, proof-led LinkedIn, local NYC partner/referral sources, then redesigned trigger-based cold outreach.
- Apps remain important for passive-income upside, but should run as constrained experiments: low-maintenance MVP, automated distribution from day one, weekly metric, kill/pause threshold, no interference with consulting delivery. Vista has ~10 active users; Nash Satoshi + Vista automated TikTok slideshow loops are running.

