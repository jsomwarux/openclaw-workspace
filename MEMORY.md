# MEMORY.md — Current Operating Context
> Main-session long-term context. Do NOT load in group/shared chats. Full archive: `docs/memory/MEMORY-full.md`; snapshot: `docs/memory/archive/MEMORY-before-optimization-2026-04-26.md`.
> Compact file: durable current context only; history belongs in daily notes/archive.

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
- Treat Aya as proof-point source only after accepted proof-safe evidence exists; current gate is `memory/clients/aya/proof-evidence-checklist.md`. Referral/content/proof reuse is blocked until acceptance evidence, value sentence, and anonymization/permission boundary are captured.

## Pipeline / Business Development
- Active client proof pipeline gate lives at `memory/clients/proof-pipeline-gates.md`: acceptance/payment/scope → evidence capture → permission/anonymization → referral ask → distribution. Do not publish, pitch, ask for referrals, or reuse proof when acceptance/screenshots/metrics/permission are unverified.
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
- Glow Index: live skincare rankings app at `https://glowindex.co`; now active for App Marketing OS durable discovery/pSEO planning. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store live at `https://apps.apple.com/us/app/vista-movie-taste-profiles/id6758186885`; durable SEO page live on jtsomwaru.com for 1–100 movie rating positioning.

## Content System
- App Marketing OS is first-class for passive-income apps. Eve owns low-cost user-acquisition strategy, research, hooks, asset maps, scoreboarding, directory/SEO/ASO, Mission Control task generation, and cross-system coordination. Standing directive as of 2026-05-19: continuously improve into JT's best possible app growth advisor using fresh web/X/YouTube research, successful app case studies, platform-native tactics, and App Marketing OS metrics. Revised operating model: `memory/app-marketing/revised-operating-model-2026-05-19.md`. ReelFarm execution/status details live in `memory/reelfarm/*`; Eve owns strategy/feedback, JT laptop/ReelFarm owns slideshow creation/posting.
- Before drafting posts: read `memory/content-voice.md`; no preamble, no em dashes, no “Here’s the thing,” standalone posts 6–15 words when requested.
- Swipe-file rule: content generation must fetch Notion Viral Posts Swipe references first (`python3 scripts/notion-swipe-fetch.py --limit 12 --min-engagement 500`) and include hook mappings in saved weekly/one-off draft files. Priority swipe niches: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
- Sports GM / @dynastyjig Phase 1 is active; current content-system detail archived at `docs/memory/sports-gm-content-system-current.md`. Key rule: daily @dynastyjig drafts are niche-native trust content, not app-centric promo; product names are banned by default. As of 2026-05-12, daily @dynastyjig packs must include `Native pattern teardown` + `Rejected generic patterns`, and drafts must model fresh niche syntax/rhythm before topics. Dynasty reply targets are stricter than posts: targets must be ≤24h old, cached pools are banned, and blocked X/search must return `BLOCKED` instead of stale suggestions.
- Notable completed work triggers: update proof points, recent builds, technical angles if useful, generate content when rubric passes, upload substantive deliverables to Drive.
- Wednesday LinkedIn case studies use `skills/wednesday-linkedin/SKILL.md`.

## Job Market
- Target only AI implementation / AI Solutions Architect / AI Implementation Lead roles that value BSA + ops automation background.
- Strategic posture as of 2026-05-11: consulting-first, employment selective. Treat job discoveries as hiring-budget/pain signals first, applications second. Route each strong discovery as `apply`, `both`, `consulting-outreach`, or `market-intel`.
- Apply only for exceptional strategic fits (generally 22+/25, $150K+, NYC/remote, low misrepresentation risk). For 18–21/25 roles, usually use the JD as market intel or a consulting lead signal instead of spending time on a resume package.
- If a company is hiring full-time for AI implementation, do not assume they lack consulting interest; position consulting as interim de-risking, workflow mapping, pilot governance, or acceleration while the FTE is hired/ramped — never as “hire JT instead.”
- Avoid pure software engineering, ML research, Apex/SFDX-heavy Salesforce developer, relocation, or sub-$150K roles.
- Resume/cover letter packages must use Sonnet model via job-application skill; save local markdown + generate docx + upload to Drive.

## Crypto / Finance
- Crypto is JT’s primary income stream. x402 is a forward bet.
- Financial safety: never trade, transfer, spend, or execute financial transactions. Conway constraints: max $5/action, max 2 VMs, wallet <$10 means do not spend.
- Morning crypto cron and Nash Satoshi ranking content are operationally important; missed critical crons should be detected and fired per HEARTBEAT rules.

## Infrastructure / OpenClaw State
- OpenRouter active. Use Sonnet for complex reasoning/job apps; Opus only when JT explicitly approves premium/high-precision work. Use aliases when possible.
- Google Drive OAuth may block Drive-dependent pipeline work; if uploads fail, JT needs to run `python3 ~/.openclaw/workspace/scripts/drive_auth.py`.
- LCM/lossless-claw is active; use `lcm_grep` → `lcm_describe` → `lcm_expand_query` for prior conversation recall before asserting specifics.
- Fresh web search: use `scripts/web_search.py` direct Brave API for freshness/date filters; managed `web_search` only for broad non-freshness lookups until proven fixed. Do not configure Brave plugin/provider without approval.
- Gateway restart path: prefer `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`; do not raw restart/config patch unless explicitly approved.
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`.
- Critical commands/paths live in `TOOLS.md`; consult it before saying “I can’t.”

## Active Automation / Crons
- Keep daily cron invocations ≤20. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM ET.
- One-shot reminder active: 2026-05-15 3PM ET (`0f4d8f45`) to check after Yair/Matt Thu/Fri rent-delinquency discussion; suggest light follow-up only if no update.
- `critical-files-integrity` (`ee357abb`) runs daily 9AM ET, timeout 180s; run script first, inspect/edit only on non-zero exit.
- Active cron count: 53 as of 2026-05-24 after adding a temporary reddit rerun check plus passive-income strategist delivery guard. Active cron responsibilities: morning brief, job market, niche monitor, crypto, content, App Marketing/ReelFarm, Sports GM, North Star, cost, health, passive-income pipeline. Heartbeat cron `eve-heartbeat-2h-002` disabled 2026-05-17 at JT request.
- 2026-05-24: Passive-income strategist hardened after silent miss. Guard cron `e7d45070` runs Sundays 3:20PM ET and executes `scripts/passive_income_strategist_delivery_guard.py --send` to verify report + Telegram delivery, resend digest, or alert.
- 2026-05-12: Mission Control North Star audit runs in Morning Brief + heartbeat via `scripts/mission_control_north_star_audit.py`.
- 2026-05-13: App Marketing OS gained autonomous MC task generation via `scripts/app_marketing_task_generator.py`; weekly reviews must read self-improvement rules, assign states, and rerun generator after metrics refresh.
- 2026-05-14: App Marketing OS web analytics integrated with GA4/Search Console OAuth via `scripts/app_marketing_connectors/web_metrics.py`. Nash + Glow GA4/Search Console are live; jtsomwaru.com GA4/Search Console live. Ref: `memory/app-marketing/ga4-integration-reference.md`.
- 2026-05-19: App Marketing OS xhigh review sharpened strategy: prioritize niche-specific acquisition loops, product-led share artifacts, measurement spine, competitor/review mining, and borrowed-audience lists. Operating model: `memory/app-marketing/revised-operating-model-2026-05-19.md`.
- 2026-05-13: Spanish Daily Lesson hardened: delivery now fails loudly (`bestEffort=false`), failure alert enabled, cron prompt runs `scripts/spanish_state_check.py`, and HEARTBEAT 10AM/10PM validates Spanish state before resend/reminder.
- 2026-05-12: Autoresearch Sweep (`ec9f36d3`) Mon/Wed/Fri 11:15AM ET; AI Ops Teardown Weekly Draft (`f96cc24f`) Sundays 7:15PM ET.
- 2026-05-12/13: Selective routing + xhigh audit fixed content seed/Drive loop, outreach preflights/buffer, passive-income decrowding, Weekly Intelligence/System Review split, stale cron descriptions, and disabled obsolete `content-monday-send`.
- 2026-05-14: Crypto Morning (`eve-crypto-morning-008`) now hard-requires fresh full-universe X API research before allocation delivery. Added `scripts/run-x-research.py` + `scripts/x-research-guard.py`; cron timeout is 1200s and must block/send incomplete warning if X guard fails.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75.
- Kobe Protocol: daily film review at 10AM and weekly skills audit. Mistake entries require failure + root cause + prevention rule.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- 2026-04-26: consulting acquisition wedge: sell contained 7-day ops bottleneck audits/prototypes, not broad “AI transformation.” First workflows: property maintenance triage, construction field-note→punch-item/customer-update, wholesale stock/ETA/order-status reply drafts with human approval.
- 2026-05-04: Exception Dashboard positioning: AI as exception layer, not chatbot — stuck work, owner, changed state, approval need, audit trail across PM/wholesale/construction/client intake. Draft: `memory/drafts/exception-dashboard-consulting-post-2026-05-04.md`.
- 2026-03-31: consulting positioning is permanent until explicitly changed: practical AI implementation for ops-heavy SMBs.
- 2026-03-23: no anime/NBA apps right now; prioritize B2B consultable products and client-work proof.
- AgentSync concept deferred unless a direct need appears; Mission Control already provides enough orchestration.
- Zapier MCP integration not needed now; n8n MCP + MCP-router covers needs.
- Railway MCP: not needed now; revisit only for multi-service deployments.
- Selenium MCP still needed despite Cloudflare `/crawl` because browser automation remains useful.
- x402 / agentic commerce: active content pillar and passive-income/app-readiness lens as of 2026-05-10. Post 1–2x/week max from operator-builder POV. Do not sell generic “x402 installation” to SMBs; if tested, frame as Agent-Ready Revenue Layer / x402 Readiness Sprint for API/data/product companies with agent-readable outputs, pricing, receipts, spend controls, and docs. Source: `memory/consulting/agent-ready-revenue-layer/positioning.md`.

## Integrity / Fabrication Corrections
- Never claim outreach/messages were sent unless tool/script evidence confirms it.
- Never fabricate URLs, deployment state, GitHub status, Drive links, or task closure. Verify with tools.
- If corrected by JT, immediately update the Mistakes Log/rules before moving on.

## Setup State
- 2026-05-11: GBrain consulting recall pilot lives at `~/projects/gbrain*`; use only `scripts/gbrain-consulting-search.sh "Entity"` for consulting/prospect entity lookup. No crons/skillpacks/broad ingestion/embeddings without JT approval.
- 2026-05-11: Added `workflow-skillify` and `high-stakes-draft-eval`; added `consulting/entity-propagation/template.md`.
- 2026-04-26: Installed `birdclaw` (local X archive workspace) and `gog` (Google Workspace CLI). Workflow rules live in `docs/tools/local-archives-workflows.md`; JT auth/import tasks created before recurring use.

## Automation / Live Opportunities
- Automation/client/opportunity history archived at `docs/memory/automation-and-live-opportunities-archive-2026-05-10.md`.
- Current must-remember items remain: Altmark is top consulting/proof lane; on 2026-05-19 JT installed the dedicated local automation PC at Altmark's office. Public proof/content should stay anonymized unless naming permission exists; next gate is handoff/access confirmation, acceptance wording, open issues, and payment/deposit clarity. Earlier context: Yair may refer ~15 NYC family offices; Marketsmith is live warm opportunity at $175/hr or $15k/mo if product team re-engages; CFS luxury construction AI role is secondary/full-time optional; App Marketing OS/ReelFarm/Sports GM/North Star crons are active responsibilities.
- Guyana strategy reset 2026-05-12: keep Guyana active but narrow the wedge. Primary path is Local Content Operations Sprint for oil/gas-adjacent Guyanese suppliers/local-content firms (compliance docs, procurement/admin workflows, bid readiness, vendor docs, tender tracking), using JT’s Guyanese-American/family-network edge as trust bridge. Government digitization/city-services demos are secondary and should only move through warm intros/local partners; stop broad “AI transformation for Guyana” framing. Files: `memory/research/guyana/2026-05-12-strategy-reset.md`, `local-content-ops-sprint.md`, `supplier-prospect-seed-list.md`. Current hidden/noindex `jtsomwaru.com/guyana` page is stale/government-infrastructure biased; do not use in supplier outreach until rewritten around Local Content Ops Sprint. MC tasks added for dad/family intro ask, capability brief, 30 supplier prospects, Richard Leo/AmCham re-engagement, hidden page rewrite, and mock demo scoping.
- Nightly autonomous leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.

