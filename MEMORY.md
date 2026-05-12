# MEMORY.md — Current Operating Context
> Main-session long-term context. Do NOT load in group/shared chats. Full archive: `docs/memory/MEMORY-full.md`; snapshot: `docs/memory/archive/MEMORY-before-optimization-2026-04-26.md`.
> Compact file: preserve durable context/current status/decisions only; historical detail belongs in daily notes/archive.

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
- Glow Index: live skincare rankings app at `https://glowindex.co`; now active for App Marketing OS durable discovery/pSEO planning. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store live at `https://apps.apple.com/us/app/vista-movie-taste-profiles/id6758186885`; durable SEO page live on jtsomwaru.com for 1–100 movie rating positioning.

## Content System
- App Marketing OS is first-class for passive-income apps. Eve owns strategy, hooks, asset maps, metrics handoff, scoreboarding, directory/SEO/ASO, and cross-system coordination. JT's laptop/ReelFarm own slideshow creation/posting; Eve must not duplicate runtime. ReelFarm baseline: Growth tier runs native TikTok photo slideshow campaigns for Vista, Nash Satoshi, and Glow Index, with two automations per app: all-lifestyle 2x/week and lifestyle hook + screenshots 1x/week. Current status as of 2026-05-11: all six automations paused; Vista/Nash had 0-view cold-start issues, Vista had silent slideshows, Glow configured but not activated. Recovery: manual TikTok app posts with hand-picked sounds, daily account engagement, restart at 1 post/week/account after warm-up, scale after 2–3 weeks of consistent reach. Screenshots are source of truth for current settings; `memory/reelfarm/reelfarm-strategy-baseline.md`, `memory/reelfarm/apps.md`, and `memory/reelfarm/reelfarm-review-checklist.md` own strategy/status/review logic.
- Before drafting posts: read `memory/content-voice.md`; no preamble, no em dashes, no “Here’s the thing,” standalone posts 6–15 words when requested.
- Swipe-file rule: content generation must fetch Notion Viral Posts Swipe references first (`python3 scripts/notion-swipe-fetch.py --limit 12 --min-engagement 500`) and include hook mappings in saved weekly/one-off draft files. Priority swipe niches: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
- Sports GM / @dynastyjig Phase 1 is active; current content-system detail archived at `docs/memory/sports-gm-content-system-current.md`. Key rule: daily @dynastyjig drafts are niche-native trust content, not app-centric promo; product names are banned by default.
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
- OpenRouter active. Current tiering: MiniMax m2.7 default, Sonnet 4.6 upgrade for complex reasoning/job apps, Opus 4.6 only for high-precision n8n/complex code when ROI justifies it. Use aliases when possible.
- Google Drive OAuth is currently a blocker for outreach uploads; JT needs to run `python3 ~/.openclaw/workspace/scripts/drive_auth.py` before Drive-dependent pipeline work.
- LCM/lossless-claw is active; use `lcm_grep` → `lcm_describe` → `lcm_expand_query` for prior conversation recall before asserting specifics.
- Codex `/goal` evaluated 2026-05-11: useful pattern, not active capability yet. Local `codex` CLI is not installed and OpenClaw does not currently expose `/goal` in the bundled harness docs/source. Do not install/enable/change Codex/OpenClaw config without JT approval. Use current TaskFlow/cron/subagent patterns by default; goal-style work requires one durable objective, verifiable stop condition, checkpoint/progress log, Mission Control visibility, budget/stop rules, and `templates/goal-mode-spec-template.md`.
- Gateway restart path: prefer `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`; do not raw restart/config patch unless explicitly approved.
- Mission Control dashboard: `http://localhost:3000`; remote tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n remote path `/n8n`.
- Critical workspace commands and paths are in `TOOLS.md`; consult it before saying “I can’t.”

## Active Automation / Crons
- Keep daily cron invocations ≤20. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM EST.
- One-shot reminder active: 2026-05-09 9:00AM ET (`e39f312a-d99f-4944-93c2-a0e6a1046fc7`) to re-check OpenClaw Codex harness docs/schema/status and reevaluate whether to enable the codex plugin + `agents.defaults.embeddedHarness.runtime="codex"`; do not touch auth, summaryModel, summaryProvider, or primary model without JT approval.
- `critical-files-integrity` cron (`ee357abb-2b58-44b8-8f03-4c152611117d`) runs daily 9AM ET; timeout increased 60s → 180s on 2026-05-02 after wrapper timed out at 60.018s even though the underlying script completes in ~0.37s. Prompt simplified: run script first, inspect/edit only on non-zero exit.
- Morning brief, heartbeat, job-market, niche monitor, crypto morning, content/weekly synthesis, App Marketing weekly scoreboard, Weekly North Star Review, cost tracking, and health check-ins are active responsibilities.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75.
- Kobe Protocol: daily film review at 10AM and weekly skills audit. Mistake entries require failure + root cause + prevention rule.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- 2026-04-26: consulting acquisition wedge: sell contained 7-day ops bottleneck audits/prototypes, not broad “AI transformation.” First workflows: property maintenance triage, construction field-note→punch-item/customer-update, wholesale stock/ETA/order-status reply drafts with human approval.
- 2026-05-04: synthesized Exception Dashboard positioning for SMB consulting: show AI as an exception layer, not a chatbot — stuck work, owner, changed state, approval need, and audit trail across property management, wholesale, construction, and client intake. Draft saved at `memory/drafts/exception-dashboard-consulting-post-2026-05-04.md`.
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
- 2026-05-11: GBrain consulting recall pilot completed in sandbox. Installed GBrain 0.32.0 at `~/projects/gbrain`, pilot home `~/projects/gbrain-pilot-home`, curated sanitized source `~/projects/gbrain-pilot-source`. Result: entity lookup strong (20/20 vs qmd 13/20), natural-language weak without embeddings (3/20). Use only `scripts/gbrain-consulting-search.sh "Entity"` for consulting/prospect entity lookup. Do not add crons, skillpacks, broad ingestion, or embedding/auth wiring without explicit approval.
- 2026-05-11: Added two reusable workflow skills from Garry Tan/GBrain pattern review: `workflow-skillify` for turning repeated workflows/corrections into durable skills/checklists, and `high-stakes-draft-eval` for checking important outreach/positioning/job-app/site copy before delivery. Also added `consulting/entity-propagation/template.md` for propagating consulting facts across source/prospect/contact/pipeline/daily-note surfaces.
- 2026-04-26: Installed `birdclaw` (local X archive workspace) and `gog` (Google Workspace CLI). Workflow rules live in `docs/tools/local-archives-workflows.md`; JT auth/import tasks created before recurring use.

## Automation / Live Opportunities
- Detailed automation/client/opportunity history archived at `docs/memory/automation-and-live-opportunities-archive-2026-05-10.md`.
- Current must-remember items remain: Altmark is top consulting/proof lane; Yair may refer ~15 NYC family offices; Marketsmith is live warm opportunity at $175/hr or $15k/mo if product team re-engages; CFS luxury construction AI role is secondary/full-time optional; App Marketing OS/ReelFarm/Sports GM/North Star crons are active responsibilities.
- Nightly autonomous leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.

