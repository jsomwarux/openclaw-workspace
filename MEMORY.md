# MEMORY.md - Current Operating Context Index
> Main-session context index. Full detail: `docs/memory/MEMORY-full.md`. Keep compact; warn above 7,000 chars.

## JT Snapshot
- JT Somwaru, America/New_York; Telegram primary; ops-to-AI implementation.
- Active mandate: `memory/operating-mandates/90-day-playbook-2026-08-19.md`, written 2026-08-19 and running through 2026-11-17. It supersedes prior strategy/positioning guidance where conflicts exist.
- Scoreboard through 2026-11-17: cash collected. Nothing else counts as progress. Input metric: 2 priced conversations per week, meaning JT told a real buyer a real number.
- Positioning through 2026-11-17: "You take one messy business process, build a controlled AI system around it, and leave behind proof the business can trust." Say this exact thing; property managers/building owners in NYC/NJ first.
- Frozen through 2026-11-17: niche research system, self-improving cron/agent harness, knowledge ingestion/skill converter work, per-domain lexicons, Mission Control Phase 3, all four app lanes, Guyana, Bustem, $500 website offer, and any new skill outside paid delivery. Re-entry test: produces an invoice inside 90 days.
- Constraints: no relocation, protect sleep/health/NYC stability, avoid developer-only positioning.
- Detail: `docs/memory/MEMORY-full.md#jt-snapshot`.

## Hard Rules / Security Essentials
- No auth/model/OpenClaw/sacred-file/credential changes without explicit approval; never expose keys outside approved auth/env homes.
- Credential/cache artifacts stay outside workspace memory. Never send third-party outreach for JT; draft/sync only.
- Detail: `docs/memory/MEMORY-full.md#hard-rules--security-essentials`.

## Consulting Positioning
- Practical AI implementation for ops-heavy SMBs: one messy business process, controlled AI system, trusted proof.
- Sell in order: Workflow Audit $1,500 flat for one week; Build $6,000-$12,000 fixed with 50% up front and 50% on acceptance; Managed AI Ops $1,500/month after the monthly report exists. Partner Studio is later, not now, except Altmark.
- Do not add "any industry" or explain agents-building-agents in buyer-facing positioning during the 90-day playbook.
- Detail: `docs/memory/MEMORY-full.md#consulting-positioning`.

## Active Clients
- Canonical July 16 state: `memory/canonical/jt-mission-control-state-2026-07-16.md`.
- Altmark top paid/proof lane: rent delinquency gate plus FTE + NewCo negotiation with Yair/Adai. FTE and NewCo separate; JT's existing systems/toolkit/playbook stay personal IP. DHCR routes to Matt.
- MSI / Marketsmith closed accepted: $10,800 fixed-scope Nexus; kickoff $5,400 cleared; all four deliverables accepted after client technical re-verification 2026-08-17. MSI-002 ($5,400) sent 2026-08-18, due 2026-09-02; flag unpaid 2026-09-03. Follow-on through technical lead first; flag before quoting.
- Closed-won/paid: SoberLife-Coach/Karen is paid and referral-ask eligible under the 90 Day Playbook; Gil/Aya construction dashboard is paid and referral-eligible. Maiky is separate live Aya-adjacent opportunity on hold after cost review.
- Detail: `docs/memory/MEMORY-full.md#active-clients`.

## Pipeline / Business Development
- North Star system: `memory/north-star.md`, `memory/pipeline.jsonl`, `memory/send-queue.md`, `scripts/north_star_pipeline.py`.
- Pipeline for 90-day playbook: Ed, Sam, Gil, Karen, Maiky, Yair, Adi, Matt, Ron. Work this list before finding strangers.
- Current asks: Ed follow-on plus 2 intros; Sam referral ask; Gil paperwork-referral ask; Karen referral ask; Maiky restart paused work or ask who else at Aya needs it; Yair/Adi force partnership decision and association intros; Matt asks what is still manual; Ron asks whether jeweler clients need the same thing property managers need.
- Guyana is frozen through 2026-11-17 unless JT explicitly overrides after the freeze prompt.
- Detail: `docs/memory/MEMORY-full.md#pipeline--business-development`.

## Consulting Delivery / Niche Matrix
- Client/discovery work requires Client OS + reusable-IP capture only when tied to paid delivery. Services-as-software = manual proof, edge cases, failures, metrics before automation.
- Delivery focus through 2026-11-17: Tuesday-Thursday paid work only. Do not create research, market discovery, system design, tooling, app, or strategy tasks unless JT explicitly overrides a frozen item or the work produces an invoice inside 90 days.
- Detail: `docs/memory/MEMORY-full.md#consulting-delivery--niche-matrix`.

## Current Apps / Products
- `jtsomwaru.com`: AI ops homepage; `/property` PM Workflow Audit path. All four app lanes are frozen through 2026-11-17 unless JT explicitly overrides after the freeze prompt.
- Detail: `docs/memory/MEMORY-full.md#current-apps--products`.

## Content System
- Read JT voice/corpus before drafting; first-person proof beats generic advice.
- Review drafts remain review-only; do not auto-post/schedule/send/upload unless explicitly approved.
- Detail: `docs/memory/MEMORY-full.md#content-system`.

## Job Market
- 2026-08-22: JT approved reactivating the weekday job pipeline as a controlled income hedge while consulting remains primary and the 2-priced-conversations/week input metric stays intact.
- Search responsibilities before titles. Primary targets: Senior/Lead BSA (AI/automation), AI Operations Program Manager, Intelligent Automation/Workflow Transformation Lead, AI Adoption & Enablement Manager, AI Governance/Quality Operations Manager, and AI Implementation Program Manager. Solutions Architect is selective only when post-sale/configuration/implementation-focused, never pre-sales/cloud/coding-heavy.
- Application gate: direct evidence for at least 80% of must-haves; top 3 responsibilities map to paid work or Spectrum; no critical credential/seniority/coding/quota/architecture gap; $150K+ NYC/remote; live posting verified.
- GPT-5.6 Sol via OAuth is the default application-package model. Sonnet is explicit comparison/escalation only. Legacy research/build-idea modules are preserved in `config/cron-snapshots/job-pipeline-legacy-before-reactivation-2026-08-22.json`.
- Avoid Apex/SFDX-heavy dev, pure ML/research, relocation, low salary. Anonymize client proof unless JT approves.
- Detail: `docs/memory/MEMORY-full.md#job-market`.

## Crypto / Finance
- Crypto is research/ranking/threshold-awareness only. Never trade, transfer, swap, spend, or run payment-MCP/x402 experiments without JT approval.
- Crypto loop remains directive-disabled; avoid X pulls unless JT reactivates/asks.
- Detail: `docs/memory/MEMORY-full.md#crypto--finance`.

## Infrastructure / OpenClaw State
- Default route is OpenAI OAuth; non-default/premium model use needs named approval except approved content jobs. OpenClaw checks require Node 26 path; cost alerts clean.
- Mission Control: `http://localhost:3000`; tailnet `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n `/n8n`. Normalize MC API with `(.tasks // .items // .)`. Write contract now blocks Strategy/Positioning, research, market discovery, system design, and tooling tasks during the 90-day playbook unless tied to an invoice inside 90 days.
- Backup regression: local backup succeeds but `n8n-agent` GitHub push remains remote-ahead `main -> main (fetch first)`. Heartbeats must not run git pull/merge/force-push; routed via MC task `j57cc0zrdhrxkkazwkd2hpmqn58bz4ff`.
- Detail: `docs/memory/MEMORY-full.md#infrastructure--openclaw-state`.

## Active Automation / Crons
- 2026-08-24: JT overrode the freeze and approved the non-Grok agent-operating-system implementation. The independently confirmed Nightly Validation Controller is live at 11:15 PM ET as cron `e3156dad-ddc4-4b74-b019-727b23dc72e0`; 11 jobs are enabled, 59 estimated weekly invocations, and the empty-queue smoke run succeeded silently. It admits one lane and up to three read-only packets, requires fresh independent verification, and upserts at most one gated Mission Control task. JT will create the separate Grok Signal Lab. Source: `deliverables/agent-operating-system-redesign-2026-08-24.md`.
- 2026-08-24: JT approved the non-Grok implementation. `Daily Workout Card` remains active as a one-way 05:00 ET training card outside the canceled health-automation lane. It reads JT's pointer, sends exact workout text silently, never asks for health/feeling/completion data, and never advances state.
- Aug 12 heartbeat baseline: cost clean; MC 66 active/10 high/4 overdue high; 12 enabled crons/0 unhealthy; refused-scope jobs absent; Spanish paused. Daily Delta must use numeric Telegram destination `6608544825`; stale `@heartbeat` attempts are recurrence evidence.
- Aug 7 JT canceled all health crons. Do not re-enable Health/Protocol Ops without explicit JT instruction; manual health helpers remain available only on request.
- Detail: `docs/memory/MEMORY-full.md#active-automation--crons`.

## Health / Training / Quality Loops
- Health files/tools remain available, but automated health prompts/reports are canceled as of Aug 7. Cost tracker, proof guard, film review, and skills audit remain active.
- Daily Workout Card is training delivery only, not health tracking or a revival of canceled health check-ins.
- Detail: `docs/memory/MEMORY-full.md#health--training--quality-loops`.

## Integrity / Fabrication Corrections
- Never fabricate; verify outreach, URLs, deployments, Drive links, task closure, and delivery with tool/script evidence.
- JT corrections require Mistakes Log/rule updates with regression checks. Use lossless-claw recall before exact compacted-history claims: start with `lcm_grep`, inspect with `lcm_describe`, use `lcm_expand_query` when exact evidence is needed.
- External strategy prompts need no-prior-context primer.
- Detail: `docs/memory/MEMORY-full.md#integrity--fabrication-corrections`.

## Setup State / Live Opportunities
- JT OS plugin/skills live in TOOLS. Altmark is top proof/revenue lane; PM proof review and Run Control sales asset are next.
- Detail: `docs/memory/MEMORY-full.md#setup-state`.
