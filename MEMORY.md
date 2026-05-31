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
- Constraints: not positioning as hands-on developer; avoid Apex/SFDX/ML-engineering roles. Job target: AI Solutions Architect / AI Implementation Lead, $150K min, $180–220K ideal, NYC/remote only. Non-negotiables: sleep, health, and staying in NYC/location stability.

## Hard Rules / Security Essentials
- Never modify `openclaw.json` auth, `summaryModel`, `summaryProvider`, primary model, `auth-profiles.json`, `models.json`, or update OpenClaw without JT approval.
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

## Active Clients
- **Altmark Group:** priority paid client. Dedicated PC installed in office; insurance expiration workflow is live and final 50% paid. Rent delinquency workflow initial 50% paid and remains the top proof/revenue gate. Synthetic dry-run passed 2026-05-29: 8 rows -> 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 tenant-facing drafts from sensitive/cleanup rows. 2026-05-30 redacted-sample gate: first real-report sample stays review-only; next JT ask is redacted source export, source report path/export process, refresh cadence, reviewer, and exception rules. DHCR Lease Renewal Phase 1 assets sequence after rent delinquency acceptance unless Altmark reprioritizes. Keep proof capture privacy-safe; public naming requires accepted client output plus permission/anonymization.
- **Aya:** anchor client. Completed: $1,500 dashboard. Active: $1,000 StreetEasy scraper. Pending: $2,500 co-living dashboard. Stalled: acquisitions dashboard. Treat Aya as proof-point source only after accepted proof-safe evidence exists; gate: `memory/clients/aya/proof-evidence-checklist.md`.

## Pipeline / Business Development
- Active client proof pipeline gate lives at `memory/clients/proof-pipeline-gates.md`: acceptance/payment/scope → evidence capture → permission/anonymization → referral ask → distribution. Do not publish, pitch, ask for referrals, or reuse proof when acceptance/screenshots/metrics/permission are unverified.
- 2026-05-27 outreach strategy reset: LinkedIn warm-up comments are not the default route for new prospects. Use them only for high-fit T1/T2 prospects with recent relevant activity and a concrete M1/follow-up plan within 24-48h. Default prospecting should prioritize proof-led referrals/warm intros, live service pages/citation outreach, buyer-channel validation, and review-only outreach packets.
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
- `jtsomwaru.com`: portfolio site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push. AI SEO/citation path as of 2026-05-27: build n8n service/proof pages first, then directory/entity profiles and roundup outreach; no public submissions before JT approval.
- Glow Index: live skincare rankings app at `https://glowindex.co`; now active for App Marketing OS durable discovery/pSEO planning. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store live at `https://apps.apple.com/us/app/vista-movie-taste-profiles/id6758186885`; durable SEO page live on jtsomwaru.com for 1–100 movie rating positioning. 2026-05-27 app-marketing reset: run a Vista-first, artifact-led growth sprint; use 5-7 total weekly app posts across the portfolio, with Vista getting 60-70%, Nash getting 20-30%, and Glow staying SEO/AI-search first until crawler/claim-safety/measurement gates are healthy.

## Content System
- Before drafting: read `memory/content-voice.md`; no preamble/em dashes/“Here’s the thing”; standalone X posts 6–15 words when requested.
- Recurring content must use platform+niche reference mechanics, not generic swipe claims. New LinkedIn/X queues must save source URL, platform, niche, format, hook mechanic, and JT translation, then pass `content_distribution_guard.py --require-reference-map`.
- App Marketing/ReelFarm reset and Sports GM/@dynastyjig rules live in `docs/memory/current-context-details-2026-05-27.md` and `docs/memory/sports-gm-content-system-current.md`; Wednesday LinkedIn uses `skills/wednesday-linkedin/SKILL.md`.
- Completed work triggers proof points, recent builds, technical angles if useful, content rubric, and Drive upload for substantive deliverables.

## Job Market
- Target only AI implementation / AI Solutions Architect / AI Implementation Lead roles that value BSA + ops automation background.
- Strategic posture as of 2026-05-11: consulting-first, employment selective. Treat job discoveries as hiring-budget/pain signals first, applications second. Route each strong discovery as `apply`, `both`, `consulting-outreach`, or `market-intel`.
- Apply only for exceptional strategic fits (generally 22+/25, $150K+, NYC/remote, low misrepresentation risk). For 18–21/25 roles, usually use the JD as market intel or a consulting lead signal instead of spending time on a resume package.
- If a company is hiring full-time for AI implementation, do not assume they lack consulting interest; position consulting as interim de-risking, workflow mapping, pilot governance, or acceleration while the FTE is hired/ramped — never as “hire JT instead.”
- 2026-05-29 xhigh audit: AI enablement roles now map to AI operating-system proof lanes (intake, connectors/MCP, evals, lineage, governance, adoption, rollback, ROI). `~/projects/job-market-agent/data/role-to-build-matrix.md` is canonical before creating role-derived build/demo tasks; Altmark proof still outranks H.I.G./DealDesk speculation.
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
- Fresh web search: use `scripts/web_search.py` direct Brave API for freshness/date filters; managed `web_search` only for broad non-freshness lookups until proven fixed. Do not configure Brave plugin/provider without approval.
- Gateway restart path: prefer `bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"`; do not raw restart/config patch unless explicitly approved.
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`.
- Critical commands/paths live in `TOOLS.md`; consult it before saying “I can’t.”

## Active Automation / Crons
- Cron volume is guarded by `scripts/cron_volume_guard.py`: ≤35 scheduled invocations/day average and ≤28 agentTurn/day average; >30/day warns. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM ET.
- `critical-files-integrity` (`ee357abb`) runs daily 9AM ET, timeout 180s; run script first, inspect/edit only on non-zero exit.
- Active cron count: 51 enabled / 77 total as of 2026-05-29. Responsibilities: morning brief, job market, niche monitor, crypto, content, App Marketing/ReelFarm, Sports GM, North Star, cost, health, passive-income pipeline. Heartbeat cron `eve-heartbeat-2h-002` disabled 2026-05-17 at JT request.
- 2026-05-27: Outreach pipeline cron is script-first. Cron `outreach-pipeline` now runs `scripts/outreach_pipeline_runner.py --json` before any copy generation; deterministic preflight handles Drive auth, M-status/T3 dedupe, existing draft/doc checks, warm-up holds, and report paths. LLM copy only runs for explicitly eligible copy-review items.
- 2026-05-27: `Overnight Autonomy Agent` moved from 3:00AM to 3:20AM ET to avoid same-minute contention with outreach preflight; prompt is now Mission-Control/North-Star-first, light-context enabled, `thinking=high`, timeout 1800s, and legacy `memory/tasks.md` is fallback only.
- 2026-05-29: `nightly-autonomous-leverage-agent` patched with a material-progress/anti-repeat gate after JT flagged repeated Altmark-adjacent reports. It must compare the last two nightly runs, name a material delta, suppress/rotate after two same-blocker nights without new input/evidence, and avoid creating another adjacent artifact when the existing MC task already captures the blocker.
- 2026-05-28: `Job Application Tracker` cron was hardened after inline Python/heredoc task filtering failed. It now calls `scripts/job_application_tracker_check.py --json`, avoids ad hoc filtering, and only alerts JT when the script returns `flagged_count > 0`. Manual rerun finished ok with no stale or urgent active applications.
- 2026-05-28: `t3-cold-hook` still shows a stale `lastRunStatus=error` from a successful 06:30 batch whose final proof/recap closeout failed. Root cause was patched in `agents/t3-cold-hook/AGENT.md`; do not manually rerun unless duplicate draft/task/Telegram prevention is explicitly handled.
- 2026-05-30: stale cron errors remain known/handled. Job Market Daily is at `consecutiveErrors=2` from a useful-output no-match search failure; hardened to treat `rg ... || true` empty matches as "not found." Skills & API Researcher is at `consecutiveErrors=2` from bare `bun kb.ts`; hardened so KB commands run from `~/.openclaw/workspace/knowledge`. Viral Swipe and `t3-cold-hook` remain one-error stale. Do not rerun any solely to clear status or duplicate output.
- 2026-05-12: Mission Control North Star audit runs in Morning Brief + heartbeat via `scripts/mission_control_north_star_audit.py`.
- 2026-05-13: Spanish Daily Lesson hardened: delivery now fails loudly (`bestEffort=false`), failure alert enabled, cron prompt runs `scripts/spanish_state_check.py`, and HEARTBEAT 10AM/10PM validates Spanish state before resend/reminder.
- 2026-05-26: Spanish lessons paused at JT's request. Disabled `Spanish Daily Lesson` (`babd905a-1098-49dd-8700-772fef14f817`); `Spanish Weekly Evaluation` (`012216b9`) was already disabled. `05024e45` is Skills & API Researcher Weekly Synthesis and remains enabled. Spanish state updated to `paused: true`.
- Passive-income/App Marketing/web metrics/crypto X-research cron details are archived in `docs/memory/current-context-details-2026-05-27.md`.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75; `--check-alerts` includes model-routing guard.
- Kobe Protocol: daily film review at 10AM and weekly skills audit. Mistake entries require failure + root cause + prevention rule.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- Current strategy: contained SMB ops bottleneck audits/prototypes; practical AI implementation for ops-heavy SMBs; prioritize B2B consultable products/client proof over anime/NBA apps; x402 is an operator-builder content/app-readiness pillar, not a generic SMB install offer.
- Deferred/not-needed items: AgentSync unless direct need appears; Zapier MCP and Railway MCP not needed now; Selenium MCP still useful for browser automation.
- Full dated decision detail: `docs/memory/current-context-details-2026-05-27.md` and `docs/memory/MEMORY-full.md`.

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
- Current must-remember items: Altmark rent delinquency deployment is the top consulting/proof lane and the only current high-priority Mission Control item. ReelFarm/TikTok warm-up recovery remains an active app-marketing lane but is not the current high-priority MC blocker. Yair may refer ~15 NYC family offices, but proof/referral use stays anonymized/permission-gated. Marketsmith is warm again after Memorial Day; watch this week, do not chase immediately. CFS role is secondary; App Marketing OS/ReelFarm/Sports GM/North Star crons stay active.
- Guyana strategy reset 2026-05-12: keep Guyana active but narrow the wedge to Local Content Operations Sprint for oil/gas-adjacent Guyanese suppliers/local-content firms. Current artifact is the 30-company prospect map at `memory/research/guyana/guyana-local-content-prospect-map-2026-05-27.md`; first five review-only outreach packets are in `memory/drafts/guyana-first-5-supplier-outreach-packets-2026-05-27.md`. No outreach without JT review/send-path approval. Hidden/noindex `jtsomwaru.com/guyana` remains stale until rewritten around the supplier/local-content wedge.
- Nightly autonomous leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.
