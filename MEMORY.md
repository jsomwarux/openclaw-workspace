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
- 2026-06-05 positioning refinement: package frontline AI adoption as an operating-model problem before automation. Durable buyer language: trusted customer/workflow context, approval rules, exception owner, system-of-record writeback, and value/KPI measurement. Use AI Context OS / Altmark-style workflow readiness as the proof path, not generic agent builds.
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

## Consulting Delivery System — Services-as-Software
- New client rule: when JT mentions a new/active/signed client or real paid/discovery engagement, remind him to document rigorously and initialize the Client OS template in the client folder immediately.
- Services-as-software model adopted 2026-05-01: sell finished outcomes, not tools. Manual delivery collects data/edge cases before automation.
- Every active client gets Client OS (`skills/opticfy-ops/templates/client-os/`): dashboard, weekly updates, decision/workflow/failure/automation/metrics/quarterly files, raw/cleaned inputs, tagged outputs.
- Retention: SaaS-like visibility + weekly cadence + quarterly buyer review. Moat: delivery IP/training data before agents/software.
- Offer filter: outsourced line item, intelligence-heavy, services spend > software spend, manually documentable. Two ghosts = targeting/offer signal. Scale delivery before marketing/sales.

## Consulting Niche-Skill Matrix
- Last reviewed 2026-06-01: `memory/research/niche-fitness-2026-06.md`; prior matrix archived at `docs/memory/consulting-niche-skill-matrix-2026-05-01.md`.
- June effort: property ops first, construction/skilled trades second, wholesale limited-test, Agentforce as strategic proof/readiness unless Salesforce stack + trigger + reply path are confirmed.

## Current Apps / Products
- `jtsomwaru.com`: portfolio site at `~/projects/jtsomwaru-com/`, deployed via Vercel. Portfolio cards require coding-agent/build/test/push. AI SEO/citation path as of 2026-05-27: build n8n service/proof pages first, then directory/entity profiles and roundup outreach; no public submissions before JT approval.
- Glow Index: live skincare rankings app at `https://glowindex.co`; now active for App Marketing OS durable discovery/pSEO planning. Replit deploy requires fresh build, not just redeploy. Engine OpenRouter key lives in LaunchAgent plist, not `global.env`. Marketing guardrails: no medical/dermatology claims, diagnosis/treatment language, fake testimonials, or fake before/after claims.
- Nash Satoshi: crypto ranking app, private repo `jsomwarux/Nash-Satoshi`; morning brief drafts daily X post from live rankings.
- Vista: App Store live; durable SEO page live on jtsomwaru.com. Current Vista-first app-marketing split/details live in `docs/memory/current-context-details-2026-05-27.md`.

## Content System
- Before drafting: read `memory/content-voice.md`; no preamble/em dashes/“Here’s the thing”; standalone X posts 6–15 words when requested.
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
- 2026-06-02/03/04/05 job-market pulses: no qualifying US/NYC/remote roles cleared filter. Useful positioning signal: AI adoption operating-system / target-operating-model work before implementation: frontline workflow discovery, intake, use-case triage, governance, HITL boundaries, adoption metrics, ROI reporting, KPIs, process ownership, champions, and business-as-usual integration.
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
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`.
- Critical commands/paths: `TOOLS.md`.

## Active Automation / Crons
- Cron volume is guarded by `scripts/cron_volume_guard.py`: ≤35 scheduled invocations/day average and ≤28 agentTurn/day average; >30/day warns. Do not create `deleteAfterRun: true` jobs.
- Task queue: `tasks/pending.jsonl`; cron every 2h 8AM–10PM ET.
- `critical-files-integrity` (`ee357abb`) runs daily 9AM ET, timeout 180s; run script first, inspect/edit only on non-zero exit.
- Active cron count: 52 enabled / 78 total as of 2026-06-05 after adding one June 25 YouTube TV midday reminder. Responsibilities: morning brief, job market, niche monitor, crypto, content, App Marketing/ReelFarm, Sports GM, North Star, cost, health, passive-income pipeline. Heartbeat cron disabled 2026-05-17 at JT request.
- Recent cron hardening/details live in `docs/memory/current-context-details-2026-05-27.md` plus daily notes. As of 2026-06-05 active cron count is 52 jobs with red states only for `prospect-discovery` and `Weekly Systems Review`; both are covered. Crypto Full Analysis content is validating/sending, but delivery metadata still needs reconciliation. Do not rerun content/reporting crons solely to clear metadata.
- 2026-06-03 Crypto Full Analysis recovery: added deterministic `scripts/generate-full-analysis.py`, validated June 3 artifacts, and patched cron `eve-crypto-morning-008` to require deterministic artifact writing plus `CRYPTO_FULL_ANALYSIS_OK`.
- 2026-05-12: Mission Control North Star audit runs in Morning Brief + heartbeat via `scripts/mission_control_north_star_audit.py`.
- Spanish lessons paused 2026-05-26; Daily Lesson and Weekly Evaluation are disabled. `05024e45` is Skills & API Researcher Weekly Synthesis and remains enabled.
- Passive-income/App Marketing/web metrics/crypto X-research cron details are archived in `docs/memory/current-context-details-2026-05-27.md`.
- Cron count/status changes must update this file same turn. Diagnose any cron with consecutive errors ≥2; timeout fixes should be sized from actual expected runtime.

## Health / Training / Quality Loops
- Health DB: `health/health.sqlite`; daily check-in 9PM; Sunday report.
- Cost tracker: `scripts/cost-tracker.py`; alert thresholds session >$2, daily >$10, monthly pace >$75; `--check-alerts` includes model-routing guard.
- Kobe Protocol: daily film review at 10AM and weekly skills audit.
- Lessons auto-write: capture non-obvious solved problems in the relevant lessons/skill/rules file immediately.

## Strategic Decisions Log
- Current strategy: contained SMB ops bottleneck audits/prototypes; practical AI implementation for ops-heavy SMBs; prioritize B2B consultable products/client proof. x402 is an operator-builder content/app-readiness pillar, not a generic SMB install offer. Full dated decisions/deferred items: `docs/memory/current-context-details-2026-05-27.md` and `docs/memory/MEMORY-full.md`.

## Integrity / Fabrication Corrections
- Never claim outreach/messages were sent unless tool/script evidence confirms it.
- Never fabricate URLs, deployment state, GitHub status, Drive links, or task closure. Verify with tools.
- If corrected by JT, immediately update the Mistakes Log/rules before moving on.

## Setup State
- 2026-05-31/06-02: Added AI Context OS Sprint, capability-routing map, proof/corpus skills, workflow/product agents, and portable Codex plugin `~/plugins/jt-operating-system` v0.2.0. Details: `docs/agents/jt-toolkit-synthesis-2026-06-02.md`.
- 2026-05-11: GBrain consulting recall pilot lives at `~/projects/gbrain*`; use only `scripts/gbrain-consulting-search.sh "Entity"` for consulting/prospect entity lookup. No crons/skillpacks/broad ingestion/embeddings without JT approval.
- Prior setup details are archived in `docs/memory/MEMORY-full.md`; tool commands live in `TOOLS.md`.

## Automation / Live Opportunities
- Automation/client/opportunity history archived at `docs/memory/automation-and-live-opportunities-archive-2026-05-10.md`.
- Current must-remember: Altmark rent delinquency is the top consulting/proof lane. Internal proof/content tasks stay medium until evidence/send paths are ready. Yair may refer ~15 NYC family offices, proof/referral use gated.
- Guyana wedge: Local Content Operations Sprint for oil/gas-adjacent suppliers. As of 2026-06-03, Dad-forward and warm-intro language should emphasize supplier ops/admin drag across logistics, construction, transportation, warehousing, professional services, ICT, vendor records, bid readiness, and local-content evidence. Artifacts/Drive IDs live in `docs/memory/current-context-details-2026-05-27.md`; hidden/noindex `jtsomwaru.com/guyana` remains stale until rewritten.
- Nightly leverage, Guyana monitor, passive-income pipeline, North Star review, App Marketing scoreboard, ReelFarm Intel, and related automation are active unless cron list says otherwise.
