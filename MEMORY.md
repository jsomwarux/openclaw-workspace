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
- Current focus: AI consulting agency, Aya client work, portfolio credibility, content engine, selective AI implementation/job-market opportunities, crypto as primary income stream.
- Constraints: not positioning as hands-on developer; avoid Apex/SFDX/ML-engineering roles. Job target: AI Solutions Architect / AI Implementation Lead, $150K min, $180–220K ideal, NYC/remote only.

## Hard Rules / Security Essentials
- Never modify `openclaw.json` auth, `summaryModel`, `summaryProvider`, primary model, `auth-profiles.json`, or `models.json` without JT approval.
- Never store or paste API keys outside approved auth/env files. Redact secrets in shareable files and Drive uploads.
- Never send messages to third parties on JT’s behalf. Draft, save, and summarize; JT presses send.
- Sacred files are edit-only/append-only: `~/.config/env/global.env`, `~/.openclaw/openclaw.json`, `~/.openclaw/credentials/*`, `memory/content/content-signals.md`.
- Use `trash` over `rm` when removing user/workspace files.

## Consulting Positioning
- Brand: JT Somwaru Consulting / Opticfy direction. Positioning: “practical AI implementation for ops-heavy SMBs” — workflows, dashboards, agents, and integrations that save time or surface revenue.
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

## Current Apps / Products
- `jtsomwaru.com`: portfolio site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push.
- Glow Index: skincare rankings on Replit/GitHub. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store pending.

## Content System
- X is primary growth channel; LinkedIn for case studies/proof; Reddit for project promotion when appropriate.
- Before drafting posts: read `memory/content-voice.md`; no preamble, no em dashes, no “Here’s the thing,” standalone posts 6–15 words when requested.
- Swipe-file rule: content generation must fetch Notion Viral Posts Swipe references first (`python3 scripts/notion-swipe-fetch.py --limit 12 --min-engagement 500`) and include hook mappings in saved weekly/one-off draft files. Priority swipe niches: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
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
- Morning brief, heartbeat, job-market, niche monitor, crypto morning, content/weekly synthesis, cost tracking, and health check-ins are active responsibilities.
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
