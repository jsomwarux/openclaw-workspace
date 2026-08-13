# Automation Inventory for External Optimization
Date: 2026-08-12

Purpose: consolidated list of automations, agent workflows, crons, and pipelines JT has asked Eve/OpenClaw to create or operate. This is written so Opus/GPT-5.6 can optimize the systems without needing the whole workspace.

Important constraints:
- Eve never sends external outreach, posts, emails, trades, transfers money, or changes production/client systems without explicit JT approval.
- Consulting cash/proof outranks apps, passive income, crypto, and job-market exploration.
- Reusable IP rule: client work should capture proof, edge cases, failure modes, judgment calls, and reusable operating patterns before automation expands.
- Builder never grades: substantive "done" claims need same-run evidence and, where required, fresh verification.
- Red actions include money, external sends, cron creation/editing, OpenClaw config/model/auth changes, deploys, pushes, and client/prod mutations.

## 1. Passive Income Signal Fetch Pipeline

Intent:
Find low-maintenance digital product ideas before they are crowded, especially ranking/comparison tools, narrow reports, directories, affiliate assets, and agent-purchasable microservices.

Intended cadence:
- Saturday 5:30 AM ET.
- Output feeds Sunday Passive Income Scout and Strategist.

Intended input sources:
- Exploding Topics scraper -> `memory/passive-income/weekly-exploding-topics.md`
- Google Trends / pytrends -> `memory/passive-income/weekly-google-trends.md`
- Broader trend search -> `memory/passive-income/weekly-trends.md`
- API discovery sources: APIs.guru, Product Hunt, Hacker News, RapidAPI/developer search -> `memory/passive-income/weekly-apis.md`
- TrustMRR or similar revenue/product signal -> `memory/passive-income/weekly-trustmrr.json`

Intended flow:
1. Fetch rising consumer/business trend topics.
2. Fetch newly available APIs and structured-data surfaces.
3. Pull developer/product discovery signals from HN, Product Hunt, APIs.guru, and API search.
4. Store raw weekly source files, preserving enough details for later model synthesis.
5. Do not recommend a build directly from fetch. This stage only prepares source evidence.
6. Run a pre-scout validation that required signal files exist, are not tiny, and are not stale.

Optimization target:
Make source quality explicit. Split "hard signals" from soft signals, detect duplicate trend phrasing, and attach a source confidence score to each seed.

Known status/issues:
- Pipeline exists and is explicitly kept active.
- Some sources can be stale/degraded; guards allow degraded mode rather than blocking everything.
- Current fallback can preserve seeds but may produce generic ideas if source extraction is weak.

Source paths:
- `scripts/passive_income_handoff_check.py`
- `memory/passive-income/`
- `agents/passive-income/scout/AGENT.md`

## 2. Passive Income Scout

Intent:
Turn weekly signal files into raw passive-income ideas that fit JT's stack, with emphasis on non-obvious niche audiences.

Intended cadence:
- Sunday, after signal fetch.

Intended flow:
1. Read all passive-income weekly source files.
2. Apply "Early Trend Intercept": for each rising trend, ask what niche professional, hobbyist, underserved demographic, or SMB audience benefits before the mainstream catches up.
3. Generate 2-3 product ideas per promising trend.
4. Apply "API Opportunity Mining": match structured APIs to ranking/comparison products a specific niche would pay for.
5. Cross-reference trends with APIs. Rising trend plus underused API equals highest priority.
6. Apply "Agent-Purchasable Microservices" as a secondary lens: narrow $5-$50 outputs an agent would rationally buy mid-task, such as audits, scores, enrichments, checklists, or verification.
7. Output a same-day Scout report under `memory/passive-income/YYYY-MM-DD-scout.md`.
8. If the LLM Scout fails, deterministic fallback creates a handoff with 4 preserved seeds so Strategist is never left with no artifact.

Typical fallback ideas:
- OpsProof Radar: source-backed exception/proof packets for ops-heavy SMB workflows.
- NicheRank Pages: AI-assisted comparison pages for underserved buying categories.
- ComplianceCard Desk: claim, permit, or document risk cards with citations.
- CreatorSignal Kit: trend-to-offer briefs for creators selling digital/affiliate products.

Optimization target:
Replace fallback genericity with a ranked candidate table containing source count, demand proof, competition check, data availability, monetization path, and autonomy burden.

Source paths:
- `scripts/passive_income_scout_handoff.py`
- `agents/passive-income/scout/AGENT.md`
- `memory/job-state/passive-income-scout.md`

## 3. Passive Income Strategist

Intent:
Evaluate Scout ideas and decide BUILD, WATCH, or PASS, without letting exciting but distracting app ideas outrank consulting cash.

Intended cadence:
- Sunday after Scout.

Intended flow:
1. Read same-day Scout report.
2. Validate handoff freshness with `passive_income_handoff_check.py --mode pre-strategist`.
3. Score each idea on demand, saturation, build simplicity, revenue path, autonomy, JT stack fit, and distraction risk.
4. Decide:
   - BUILD: clear demand, data source, low maintenance, credible monetization.
   - WATCH: promising but needs more evidence.
   - PASS: crowded, too manual, low ceiling, risky, or not aligned.
5. Create/update Mission Control only for truly build-worthy ideas.
6. Write strategist report to `memory/passive-income/YYYY-MM-DD-strategist.md`.
7. Delivery guard confirms Telegram delivery or writes a degraded fallback.

Optimization target:
Add "kill/advance triggers" per WATCH item, not just a static score. Every WATCH should say what signal promotes it or kills it.

Known status/issues:
- LLM strategist has produced degraded fallback reports in some weeks.
- Delivery guard exists because cron "ok" was not enough proof that report/delivery happened.

Source paths:
- `scripts/passive_income_strategist_delivery_guard.py`
- `scripts/passive_income_handoff_check.py`
- `memory/job-state/passive-income-strategist.md`
- `mission-control/lib/mission-control/passive-income.ts`

## 4. Passive Income Decision Board

Intent:
Make passive-income ideas visible as a decision surface, not buried in markdown reports.

Intended flow:
1. Parse strategist/scout reports from `memory/passive-income/`.
2. Extract title, score, status, source file, report date, concept, revenue model, JT stack fit, longevity signal, research signal, creativity check, rationale, and decision.
3. Normalize titles and override legacy scores for known North Star candidates.
4. Surface ideas in Mission Control `/passive-income` with statuses: exploring, building, launched, shelved.
5. Prune stale old `[PI]` / `Build idea:` tasks older than 60 days unless newly viable.

Optimization target:
Use the board as the canonical passive-income backlog and force every candidate to have a last-evidence date, next validation action, and auto-shelf date.

Source paths:
- `mission-control/lib/mission-control/passive-income.ts`
- `mission-control/lib/mission-control/passive-income.test.ts`
- `reports/product-growth/passive-income-portfolio-audit.md`

## 5. Job Market Daily Research

Intent:
Monitor NYC/remote AI implementation, AI enablement, AI Solutions Architect, and adjacent roles that fit JT without pushing him into developer-only work.

Intended cadence:
- Historically daily around 5:15 AM ET.
- Currently directive-limited/disabled/refused unless explicitly revived.

Intended flow:
1. Read JT profile, job constraints, scoring criteria, skills tracker, and role-to-build matrix.
2. Search job boards and company pages for non-coding AI implementation roles.
3. Hard-filter out Apex/SFDX-heavy, ML engineer, relocation, low-salary, pre-sales-only, and generic dev roles.
4. Score surviving roles out of 25.
5. Surface only roles scoring 20+ or strong consulting-lead signals.
6. Update job opportunities and skills-demand tracker.
7. Extract role-to-build intelligence:
   - Hiring pain
   - Proof gap
   - Best move: apply package, consulting bridge, build demo, skill/agent, market intel, discard
   - Mapped existing artifact
   - Build/demo decision: extend existing, create new, defer, no build
   - Consulting angle
   - Priority vs Altmark/current cash lanes
   - Mission Control action
8. Produce `~/projects/job-market-agent/data/daily-brief.md`.

Optimization target:
Decouple "apply-worthy role" from "market signal." Most value has come from extracting reusable language and proof gaps, not from new applications.

Source paths:
- `~/projects/job-market-agent/CLAUDE.md`
- `~/projects/job-market-agent/data/daily-brief.md`
- `~/projects/job-market-agent/data/skills-demand-tracker.md`
- `~/projects/job-market-agent/data/role-to-build-matrix.md`
- `~/projects/job-market-agent/knowledge/scoring-criteria.md`

## 6. Job-Derived Skills/Demo Workflow Generator

Intent:
Use job postings to determine which skills, demos, or proof assets JT should build, based on repeated market demand.

Intended flow:
1. Parse 18+/25 roles and strong hiring-signal posts.
2. Identify skills/tools appearing in 3+ postings that are not clearly proven in JT's current profile.
3. Map demand to current proof assets: OpenClaw, Mission Control, AgentGuard, AgentPack, EnablementOps, Run Control, Altmark, MSI, Agentforce demos.
4. Decide whether to:
   - Extend an existing artifact
   - Create a small new demo
   - Create/update a skill or agent
   - Treat as market intel only
5. Create exactly one Mission Control task only when it strengthens current proof/revenue. Avoid one new demo per job description.

Examples of recurring skill/demand signals:
- Use-case intake and prioritization
- Governance/release discipline
- HITL review gates
- Eval/rollback thinking
- Tool registry and approved connectors
- Adoption/change leadership
- ROI/value reporting
- MCP/tool orchestration
- Reusable implementation assets

Optimization target:
Turn this into a monthly "proof gap radar" that outputs 3 ranked gaps max, each tied to a revenue lane.

Source paths:
- `~/projects/job-market-agent/tasks/lessons.md`
- `~/projects/job-market-agent/data/role-to-build-matrix.md`
- `memory/job-market.md`

## 7. Job Application Auto-Builder

Intent:
When a role is worth applying to, produce tailored resume, cover letter, DOCX files, and Drive uploads.

Intended flow:
1. Score role first against JT constraints.
2. If worth applying, tailor resume around role's language while keeping facts accurate.
3. Write local markdown:
   - `memory/drafts/[slug]-resume.md`
   - `memory/drafts/[slug]-cover-letter.md`
4. Generate DOCX with `scripts/build_resume_docx.py`.
5. Verify parsing/formatting, ATS structure, no client-name leaks, no empty fields.
6. Upload to Drive using `scripts/upload_job_application_docs.py` or Drive API conversion.
7. Return Drive links and application notes.

Optimization target:
Make it an explicit package builder behind a human approval gate, not a daily autonomous applier.

Source paths:
- `skills/job-application/SKILL.md`
- `scripts/build_resume_docx.py`
- `scripts/upload_job_application_docs.py`
- `scripts/job_application_tracker_check.py`

## 8. Job Application Tracker

Intent:
Track applications, stale follow-ups, and status changes.

Intended cadence:
- Historically Tue/Thu 10:15 AM.
- Currently directive-limited/disabled/refused unless explicitly revived.

Intended flow:
1. Read job opportunities/applications tracker.
2. Find roles applied, expired, stale, or needing follow-up.
3. Do not apply or send anything.
4. Surface only concrete JT actions.
5. Update memory when status changes.

Optimization target:
Use it only for applied roles and high-signal warm leads, not open-ended job hunting.

## 9. Prospect Discovery

Intent:
Find qualified consulting prospects in JT's ICPs without generating outreach spam.

Intended cadence:
- Weekly or twice weekly in older cron versions.

Intended flow:
1. Read ICPs from `documents/ICPs.md`.
2. Focus on property management/real estate ops first, construction/skilled trades second, wholesale limited-test, Agentforce insurance/Data Cloud only with confirmed stack and buyer trigger.
3. Search for companies matching vertical, geography, size, operational pain, and reachable buyer path.
4. Apply tier gates:
   - Live niche proof asset
   - Reachable channel: verified email or accepted LinkedIn connection
   - Named buyer
   - Trigger bonus: ops job posting, PM software stack, rent-stabilized exposure, growth/change signal, etc.
5. Classify:
   - T1: all four gates, proof-led outreach allowed after JT review.
   - T2: first three gates, light research and niche template.
   - Hold/dead: missing key evidence.
6. Save new prospects into consulting pipeline folders/shortlists and report what was added.
7. No external sends, no custom demo/deck/build before reply.

Optimization target:
Make discovery output a smaller "qualified changes only" feed: new T1/T2, promoted/demoted, exact missing gate.

Source paths:
- `documents/ICPs.md`
- `memory/consulting/prospect-discovery-runs/`
- `memory/job-state/prospect-discovery.md`
- `skills/opticfy-pipeline/SKILL.md`

## 10. Script-First Outreach Pipeline Preflight

Intent:
Prevent duplicate, stale, or unsafe outreach before any LLM copy is generated.

Intended cadence:
- Daily early morning.

Intended flow:
1. Run deterministic preflight before LLM work.
2. Verify Drive auth and Eve Drafts root.
3. Load local pipeline sources:
   - `~/projects/jt-consulting-pipeline/pipeline.md`
   - `drive-canonical-names.md`
   - `EMAIL-PIVOT-RULES.md`
   - client folders
4. Scan each client/prospect folder for research, brief, outreach draft, email draft, warm-up note, Drive link, M-status, T3 already sent.
5. Decide per prospect:
   - `skip`
   - `warm_up_only`
   - `local_review`
   - `eligible_for_copy_review`
   - `needs_research`
6. Write daily JSON and markdown reports under `reports/outreach-pipeline/`.
7. Do not create public artifacts, do not send outreach, do not generate new LLM copy unless queue says eligible.

Optimization target:
Use deterministic state machine plus one "next best action" per prospect; LLM should only touch copy after preflight passes.

Source paths:
- `scripts/outreach_pipeline_runner.py`
- `reports/outreach-pipeline/`
- `memory/job-state/outreach-pipeline.md`

## 11. Full Consulting Client Acquisition Pipeline

Intent:
Run a complete consulting acquisition sequence from prospect research to JT-approved outreach package.

Intended stages:
Research Agent -> Analysis Agent -> JT Review -> n8n Agent -> Presentation Agent -> Outreach Agent -> JT Send

Intended flow:
1. Preflight with `skills/jt-consulting-pipeline/scripts/preflight.sh [client-slug]`.
2. Research Agent:
   - Validate company, buyer, current business state, tech stack, trigger, likely pain.
   - Write `research.md`.
3. Analysis Agent:
   - Read research.
   - Score fit.
   - Produce `brief.md` and `brief.json`.
   - Include tier, JT review required, platform, recommended workflow, and why it matters.
4. JT review gate:
   - Eve reads brief.
   - Sends short execution plan.
   - Waits for APPROVE or redirect.
5. n8n Agent:
   - Builds workflow only after approval.
   - Outputs workflow docs.
6. Presentation Agent:
   - Builds deck/instructions around the workflow and buyer pain.
7. Outreach Agent:
   - Drafts outreach.
8. Drive sync:
   - Upload outreach/deck artifacts into `Eve - Drafts/Consulting/Clients/[Client]/`.
9. Final send gate:
   - Eve shows draft and Drive links.
   - JT presses send.
10. Send confirmation handler:
   - If JT confirms sent, run `scripts/outreach_update.py` to update pipeline state and follow-up tasks.

Hard rules:
- Never generate outreach before research.
- Never custom build/deck/demo before reply under current outbound rules.
- T3s do not get individual client folders.

Optimization target:
Preserve the research->analysis->approval->build sequence, but collapse inactive T2/T3 work into batch lanes.

Source paths:
- `skills/opticfy-pipeline/SKILL.md`
- `scripts/pipeline_drive_sync.py`
- `scripts/outreach_update.py`
- `~/projects/jt-consulting-pipeline/`

## 12. Outreach Email Pivot

Intent:
When LinkedIn/initial channel is blocked or stale, create email-path drafts without losing dedupe/status.

Intended flow:
1. Detect prospects with existing research but weak/no active send path.
2. Verify named buyer plus reachable channel.
3. Generate or update email draft.
4. Upload email draft to Drive only when appropriate.
5. Create review/send task for JT.
6. Never email externally.

Optimization target:
Unify with script-first preflight so email pivot is a decision branch, not a separate vague cron.

Source paths:
- `scripts/outreach_email_pivot.py`
- `docs/agents/outreach-rules.md`

## 13. T3 Cold Hook / Batch Outreach

Intent:
Create low-effort cold hooks for lower-confidence prospects without giving them full bespoke treatment.

Intended flow:
1. Work from T3 shortlists.
2. No individual client folder unless they reply/promote.
3. Compile T3 drafts into batch docs.
4. Create M2 follow-up tasks only where a send was confirmed by JT.
5. Promote reply-positive T3 to T2 and then run normal pipeline.

Optimization target:
Given current July outbound rule, keep T3 mostly disabled/held. Use it only for batch learning, not custom builds.

## 14. North Star Pipeline / Send Queue

Intent:
Keep consulting cash movement visible and generate a daily send queue from structured pipeline data.

Intended flow:
1. Maintain opportunities in `memory/pipeline.jsonl` with value, weight, stage, waiting_on, next_action, last_touch, and source.
2. `scripts/north_star_pipeline.py summary` calculates:
   - Current collected
   - Weighted forecast
   - Gap to $10K
   - Gap to $10K with forecast
   - Aging send candidates
3. `scripts/north_star_pipeline.py queue --write` writes `memory/send-queue.md`.
4. Daily Send Sheet consumes the queue plus Mission Control/client proof files.
5. Max 3 send/action items, ordered pipeline-advancing first.
6. Eve never sends. JT gets one-word reply keywords or direct next actions.

Optimization target:
Make `memory/pipeline.jsonl` the canonical revenue truth and stop older notes from leaking stale cash numbers.

Source paths:
- `scripts/north_star_pipeline.py`
- `memory/pipeline.jsonl`
- `memory/north-star.md`
- `memory/send-queue.md`

## 15. Daily Send Sheet

Intent:
Give JT a short daily action list that moves cash/proof forward.

Intended cadence:
- Morning, tied to Morning Brief / daily run control.

Intended flow:
1. Read directives, North Star, send queue, Mission Control, payment/revenue endpoints, daily notes, proof logs, outreach preflight, priority reports, client artifacts.
2. Verify source artifacts exist.
3. Choose max 3 sends/actions.
4. Include direct path/link and one-word keyword when useful.
5. Do not include stale/expired items.
6. Log run state.

Optimization target:
Strict "done artifact or no item" rule. Avoid surfacing asks that lack a paste-ready draft or source artifact.

Source paths:
- `memory/job-state/daily-send-sheet.md`
- `memory/send-queue.md`
- `memory/north-star.md`

## 16. Morning Brief

Intent:
Give JT the daily operating picture without forcing him to inspect every system.

Intended cadence:
- 7:30 AM ET.

Intended flow:
1. Run Mission Control North Star audit.
2. Pull active high-priority tasks from Mission Control API.
3. Read reminders for today's date.
4. Read niche monitor, job-market brief, cost brief, workout, app/vibe queue.
5. Read North Star pipeline and send queue.
6. Apply staleness gates: skip stale content/Drive/post tasks and expired/deprioritized job apps.
7. Include sections:
   - Send queue
   - priorities
   - news
   - niche intel
   - jobs
   - costs
   - workout
   - vibe queue
   - Nash/Dynasty excerpts only when qualified
   - one action

Optimization target:
Cut low-action sections when there is no current evidence. The highest value is top 1-3 decisions, not completeness.

Source paths:
- `HEARTBEAT.md`
- `docs/agents/heartbeat-extended-rules.md`

## 17. Heartbeat / Active-Hours Operations Loop

Intent:
Keep the OS healthy and find one useful proactive move during idle active hours.

Intended cadence:
- 10 AM, 2 PM, 6 PM, 10 PM ET.
- Active conversations override full protocol: reply to JT first.

Intended flow:
1. If outside active hours, return `HEARTBEAT_OK`.
2. Run Mission Control North Star audit.
3. Check cost alerts.
4. Check cron health for consecutive errors or suspicious user-facing jobs.
5. At 10 AM, verify critical missed-cron gates: outreach pipeline, enabled crypto morning if applicable, Spanish delivery when active.
6. At 10 AM, run film review: inspect yesterday's failure/friction, patch owner surface or regression check, append training note.
7. Validate Spanish state/delivery only when active.
8. If no urgent issue, pick one proactive work item in priority order:
   - client/market research
   - AI tool monitoring
   - crypto monitoring
   - job market pulse
   - content drafting
   - memory maintenance
9. Deduplicate against today's daily note.
10. Log heartbeat section.

Optimization target:
Separate "health check" from "proactive work" so checks remain cheap and proactive work does not create task churn.

Source paths:
- `HEARTBEAT.md`
- `docs/agents/heartbeat-extended-rules.md`
- `memory/training/training-log.md`

## 18. Weekly Systems Review

Intent:
Weekly maintenance of the operating system, not strategy/content.

Intended cadence:
- Sunday 10 AM ET.

Intended flow:
1. Open with North Star scoreboard from `memory/north-star.md`.
2. Report consulting pipeline movement and `waiting_on` items older than 7 days.
3. Reconcile cash collected across Mission Control revenue endpoint, Friday Scoreboard, and canonical/client state.
4. Run cron health, file budgets, process/config/plugin checks, cost review, training/regression drift.
5. Review autoresearch enrollment and future signals.
6. Run `scripts/cron_volume_guard.py`.
7. Prune stale passive-income build tasks or promote newly viable ones.
8. Append training-log review.

Optimization target:
Make WSR deterministic first, LLM summary second. Most historical failures came from stale metadata and pseudo-command style checks.

Source paths:
- `docs/agents/heartbeat-extended-rules.md`
- `memory/job-state/weekly-systems-review.md`

## 19. Friday Scoreboard / Repeat Offender Digest

Intent:
Weekly proof and failure-accountability report.

Intended cadence:
- Friday.

Intended flow:
1. Compare week-over-week cash, active lanes, proof shipped, stuck blockers, and system failures.
2. Identify repeated failure signatures.
3. Write:
   - `memory/audits/friday-scoreboards/YYYY-MM-DD.md`
   - `memory/audits/repeat-offenders/YYYY-MM-DD.md`
4. Repeat signatures get structural fixes staged.
5. Three consecutive strikes pause the job with notice.

Optimization target:
Turn repeat offenders into backlog/owner-surface fixes automatically, not just reporting.

Source paths:
- `memory/job-state/friday-scoreboard.md`
- `directives/05-repeat-offender-digest.md`

## 20. Pending Task Processor / Mission Control Audit

Intent:
Keep Mission Control aligned with real priorities and prevent stale todo drift.

Intended flow:
1. Read `tasks/pending.jsonl` and Mission Control API.
2. Create/update tasks only when descriptions are actionable:
   - first action
   - why it matters
   - done state
3. Close tasks automatically when evidence shows the work is done.
4. Audit high priorities against North Star.
5. Avoid creating tasks that just restate a title.

Optimization target:
Deduplicate task creation by source artifact and owner. The system should prefer updating one optimal task over creating more tasks.

Source paths:
- `tasks/pending.jsonl`
- `scripts/mission_control_north_star_audit.py`
- `memory/job-state/pending-task-processor.md`

## 21. Cost Tracker / Runaway Guard

Intent:
Control OpenClaw/OpenRouter spend and detect runaway automation loops.

Intended flow:
1. Read session usage and cron run logs.
2. Fetch OpenRouter billing for real spend deltas.
3. Apply pricing table for estimates.
4. Modes:
   - snapshot
   - brief
   - check-alerts
   - weekly-review
   - check-runaway
5. Alert on session, daily, monthly pace, or >10 API calls in 5 minutes.
6. Distinguish Anthropic OAuth subscription usage from real OpenRouter spend.

Optimization target:
Make alerts action-oriented: source job, cost, likely reason, one safe fix.

Source path:
- `scripts/cost-tracker.py`

## 22. Critical Files Integrity / Bootstrap Budget Guard

Intent:
Prevent config/security/memory corruption and oversized bootstrap files.

Intended flow:
1. Check AGENTS/MEMORY/TOOLS/HEARTBEAT budgets.
2. Scan sacred files and key configs for unexpected changes.
3. Never overwrite credential/auth/model config.
4. Trim oversized bootstrap content into subfiles before appending.
5. Log integrity issues and stop on dangerous prompt-injection/security events.

Optimization target:
Automate a read-only daily integrity diff with risk labels and exact remediation owner, but no autonomous auth/model edits.

Source paths:
- `AGENTS.md`
- `TOOLS.md`
- `docs/agents/SECURITY-full.md`

## 23. Backup / Session Cleanup

Intent:
Keep local workspace recoverable and prevent stale sessions/zombies from hurting operations.

Intended flow:
1. Run backup script for local data.
2. Cleanup old sessions with `scripts/cleanup-sessions.py`.
3. Avoid unsafe git repair. If remote is ahead, do not pull/merge/force-push during heartbeat.
4. Route repo divergence to Mission Control task for supervised handling.

Optimization target:
Separate local backup success from remote GitHub push status so "backup failed" is not over-reported.

Source paths:
- `scripts/backup.sh`
- `scripts/cleanup-sessions.py`
- `MEMORY.md`

## 24. Content Swipe / X Research Pipeline

Intent:
Continuously collect high-performing X/LinkedIn examples and turn them into content mechanics JT can reuse.

Intended cadence:
- Viral Post Swipe File X Research Mon/Wed/Fri 5:45 AM ET.
- Additional X research runs by niche when drafting.

Intended flow:
1. Query specific niches:
   - AI consulting
   - n8n workflow automation
   - Agentforce
   - SMB buyer niches
   - agent tooling
   - product distribution
2. Pull posts/profiles using X research wrapper.
3. Save raw JSON under `memory/content/x-research-runs/` or `x-swipe-runs/`.
4. Produce `report.md` with usable mechanics, not just popular posts.
5. Cross-reference content niche map before drafting.
6. If corpus is thin, create/update a task to collect that corpus instead of substituting unrelated niches.

Optimization target:
Extract "mechanic" fields consistently: hook type, proof type, authority source, visual asset, CTA style, transferability, rejection reason.

Source paths:
- `skills/x-research/SKILL.md`
- `memory/content/x-research-runs/`
- `memory/content/x-swipe-runs/`
- `memory/content/current-niche-map.md`

## 25. Content Generation Pipeline

Intent:
Draft JT's X/LinkedIn content from proof, market signals, and content mechanics.

Intended flow:
1. Read `memory/content-voice.md` and run audit checklist.
2. Read current niche map.
3. Select priority niche: consulting revenue/proof first.
4. Use first-person proof, buyer scenes, and concrete workflow language.
5. Draft platform-specific content:
   - X singles: 6-25 words when possible.
   - Threads: max 5 tweets.
   - LinkedIn: stronger buyer scene and ownership in the opener.
6. Run voice guard.
7. Save drafts to `memory/content/bank/[MONDAY-DATE]/`.
8. Upload/push to Notion calendar only when allowed by content workflow.
9. Do not auto-post without approval.

Optimization target:
Prioritize "proof converted to buyer problem" over generic AI advice. Reject content about internal hygiene unless it maps to a public buyer problem.

Source paths:
- `docs/agents/content-rules.md`
- `memory/content-voice.md`
- `scripts/jt_voice_guard.py`
- `skills/content-generation/SKILL.md`
- `skills/wednesday-linkedin/SKILL.md`

## 26. Content Distribution / Posted Reply Handler

Intent:
Track drafted, reviewed, scheduled, posted, and reply-handled content without losing provenance.

Intended flow:
1. Maintain content bank and Notion calendar.
2. For posted replies or edits, use posted-reply handler rules.
3. Do not fetch X API for posted-reply deltas unless rules allow; use local docs.
4. Use distribution guard before saying a post is ready/live.

Optimization target:
Create one content ledger with state transitions instead of scattered bank files, Notion rows, Drive docs, and Telegram approvals.

Source paths:
- `scripts/content_distribution_guard.py`
- `scripts/content_posted_reply_handler.py`
- `docs/agents/content-posted-reply-handler.md`

## 27. AI Ops Teardown Weekly Draft

Intent:
Create proof-safe consulting content around specific workflow teardown patterns.

Intended flow:
1. Pick a buyer-recognizable operational workflow.
2. Research current market/tool/category evidence.
3. Map the safer first workflow:
   - source record
   - exception path
   - approval owner
   - action boundary
   - audit trail
4. Produce a draft that demonstrates implementation judgment without exposing client details.

Example teardown workflows:
- Rent delinquency readiness
- Property insurance expiration exception layer
- Construction field note to accountable workflow
- Family office cash timing approval queue
- Lease renewal deadline queue
- Property maintenance work order control desk
- Wholesale order intake

Optimization target:
Turn recurring teardown format into a reusable "workflow map generator" for sales calls and content.

Source paths:
- `agents/ai-ops-teardown/AGENT.md`
- `agents/ai-ops-teardown/weekly-prompt.md`
- `memory/content/bank/`

## 28. Niche Intelligence Monitor / Weekly Intelligence Synthesis / Daily News Hook

Intent:
Monitor market signals that should affect consulting positioning, content, or prospecting.

Intended flow:
1. Daily/weekly searches for AI tools, SMB automation, Agentforce, property management, construction, insurance, app/product signals.
2. Store findings in memory research files or weekly intel brief.
3. Route signal to:
   - content draft
   - Mission Control task
   - future signal
   - consulting angle
   - no action
4. Do not treat general news as urgent unless it changes a live decision.

Optimization target:
Score each signal by "changes a JT action this week?" Most news should become KB, not tasks.

Source paths:
- `memory/content/weekly-intel-brief.md`
- `memory/ai-tools.md`
- `memory/research/`

## 29. App Marketing OS

Intent:
Market JT's apps without letting app work consume consulting time.

Current portfolio rules:
1. Action Arena: gate sprint to App Store/TestFlight, then park until football launch.
2. Glow Index: primary ongoing app bet through SEO/GEO money pages and methodology trust.
3. Nash Satoshi: capped to one human-reviewed ranking-delta/model-disagreement receipt per week.
4. Vista: paused unless share-to-install loop proves itself or consulting cash reaches $10K/month.

Intended flow:
1. Maintain app registry, weekly scoreboard, experiment calendar, measurement spine.
2. Generate Mission Control tasks only for measured, gated next actions.
3. Use source tags/GA4/Search Console/App Store metrics where available.
4. Block generic content volume.
5. Archive/demote stale app growth tasks that do not match current strategy.

Optimization target:
Make the weekly scoreboard the execution governor: each app gets push/cap/pause/gate decision, metric, and next action.

Source paths:
- `memory/app-marketing/app-registry.md`
- `memory/app-marketing/opus-strategy-reset-2026-06-18.md`
- `scripts/app_marketing_task_generator.py`

## 30. ReelFarm Intel OS

Intent:
Use short-form content trend intelligence for app marketing, especially TikTok/Reels/Shorts, without automating public posting.

Intended flow:
1. Forward Social Growth Engineers newsletters to the Eve inbox.
2. Daily strategy intel reads ReelFarm sources and app constraints.
3. Weekly synthesis converts trend patterns into app-specific recommendations.
4. Respect corrections:
   - no overstated confidence labels
   - no blurred Automation A/B slotting
   - no app casing drift
   - do not force dynamic/interactive hooks into static slideshow formats
5. JT laptop handles TikTok execution; Eve handles strategy/copy only.

Optimization target:
Tie each trend recommendation to a specific app, asset format, measurement tag, and manual execution requirement.

Source paths:
- `memory/reelfarm/`
- `memory/app-marketing/`

## 31. Vibe Marketing / Product Content Generation

Intent:
Generate app-specific social drafts for Vista, Nash, Glow, and related product lanes.

Intended flow:
1. Read product registry and monthly angles.
2. Generate X/Reddit/LinkedIn/TikTok copy ideas.
3. Respect app-specific guardrails:
   - Nash: no financial advice, no price prediction, no performance claims.
   - Glow: no medical/treatment claims, no fake testimonials.
   - Vista: do not overbuild promotion while paused.
   - Action Arena: fake money only, no gambling promises.
4. Save drafts, do not post.

Optimization target:
Now mostly superseded by App Marketing OS. Keep only measured, gated drafts.

Source paths:
- `agents/vibe-marketing/`
- `agents/app-marketing/product-content/AGENT.md`

## 32. Sports GM / DynastyJig Content and Market Report

Intent:
Run a separate sports content lane for @dynastyjig/Action Arena/Dynasty Simulator.

Intended flow:
1. Read sports-gm skill and current targets.
2. Pull current player/news/market specificity.
3. Generate weekly market report and/or daily X post pack.
4. Keep products mostly invisible unless launch timing calls for it.
5. Avoid generic sports takes; use GM-style market logic, ranks, player deltas, and card/ledger framing.

Optimization target:
Separate public sports entertainment from JT consulting authority. Only bridge to Action Arena when launch gates are real.

Source paths:
- `skills/sports-gm/SKILL.md`
- `memory/content/bank/*dynasty*`

## 33. Crypto Research / Nash Support Loops

Intent:
Monitor crypto as opportunity research and Nash content input, not trading.

Historical intended flow:
1. Morning full analysis, midday pulse, evening pulse.
2. Fetch crypto prices/signals.
3. Run analysis/ranking through crypto agent.
4. Alert only on threshold-worthy research signal.
5. Never trade, transfer, swap, pay, wallet-manage, or give financial action instructions.
6. Feed Nash only with methodology-safe research receipts.

Current status:
- Crypto recurring loop is directive-disabled/refused.
- Nash is capped to one weekly human-reviewed receipt when real ranking delta or model disagreement exists.

Optimization target:
Keep crypto as a research-only, opt-in lane. Disable any recurring alerts unless they directly feed a live product decision with low risk.

Source paths:
- `memory/crypto.md`
- `projects/crypto-agent/`
- `memory/app-marketing/app-registry.md`

## 34. Health Check-In and Weekly Health Report

Intent:
Track nervous-system/health patterns and produce reports.

Historical intended flow:
1. Evening check-in prompt asks activation, bracing, exhale, protocol/movement, sleep, optional food.
2. JT replies in Telegram.
3. Inbound handler parses reply into health DB.
4. Weekly report summarizes patterns.
5. Protocol reminders were available for reset routine.

Current status:
- JT canceled all health crons on 2026-08-07.
- Manual health tools remain available on request.

Optimization target:
If revived, make it user-pulled or low-friction manual, not an intrusive cron.

Source paths:
- `health/health.py`
- `health/inbound_handler.py`
- `health/health.sqlite`
- `scripts/protocol_ops.py`

## 35. Spanish Learning System

Intent:
Help JT learn Spanish for natural conversation with girlfriend's family and restaurants.

Historical intended flow:
1. Daily lesson Mon-Sat at 8:05 PM.
2. Lesson content written to `spanish/lessons/YYYY-MM-DD.md`.
3. State stored in `spanish/state.json`.
4. Heartbeat checks delivered lesson and, when active, nudged only if delivered and incomplete.
5. Weekly evaluation existed historically.

Current status:
- Paused by JT on 2026-05-26.
- State validates in paused mode.

Optimization target:
If revived, use a lower-volume adaptive loop: short lesson, one recall prompt, weekly practical scenario.

Source paths:
- `spanish/state.json`
- `scripts/spanish_state_check.py`
- `spanish/lessons/`

## 36. Portfolio Auto-Update / Proof Points / Recent Builds

Intent:
Convert shipped work into portfolio-proof and content-proof without waiting for manual recall.

Intended flow:
1. Trigger when build completed, shipped, live, task marked done, consulting stage complete, or new skill/capability added.
2. Score against portfolio rubric.
3. If score >=7, append to portfolio queue.
4. If score 4-6, ask JT whether portfolio-worthy.
5. Update proof points table from verified evidence only.
6. Append recent-builds entry for substantive builds.
7. Run proof log and proof guard before claiming done.

Optimization target:
Make proof capture a structured event schema: what shipped, evidence path, metric, reusable IP, content angle, portfolio decision.

Source paths:
- `agents/portfolio-updater/AGENT.md`
- `memory/content-voice.md`
- `memory/content/recent-builds.md`
- `scripts/log-proof.py`
- `scripts/memory_recap_proof_guard.py`

## 37. Autonomous Post Detection

Intent:
When notable work completes, automatically draft content about it if it passes the public-worthiness gate.

Intended flow:
1. Evaluate completed work against `memory/content/post-detection-rubric.md`.
2. If pass, generate X and LinkedIn posts.
3. Save to `memory/content/bank/[MONDAY-DATE]/auto-[slug].md`.
4. Upload both to Drive and push to Notion calendar when required.
5. Do not auto-post.

Optimization target:
Tighten worthiness. Most internal hygiene should not become content unless it maps to a buyer-recognizable workflow problem.

Source paths:
- `docs/agents/post-detection-rules.md`
- `memory/content/post-detection-rubric.md`

## 38. Client Proof Capture / Client OS

Intent:
Turn every real client into reusable IP, not one-off work.

Intended flow:
1. For new/active/signed/paid client or real discovery call, create/check client folder.
2. Initialize Client OS template.
3. Capture:
   - edge cases
   - failures
   - judgment calls
   - objections
   - inputs
   - outputs
   - approvals
   - metrics
4. Use this before automating deeper.

Optimization target:
Make this a required pre-automation checklist for Altmark/MSI/etc. Every workflow should produce "sellable pattern plus control record."

Source paths:
- `skills/client-proof-capture/SKILL.md`
- `skills/opticfy-ops/templates/client-os/`

## 39. Altmark Insurance Expiration Workflow

Intent:
Help Altmark/property/family-office ops track insurance expirations and exceptions.

Intended flow:
1. Ingest insurance/expiration source data.
2. Flag upcoming expirations, stale/missing confirmations, and exception rows.
3. Produce reviewable queue for human owner.
4. Keep audit trail.
5. Do not take sensitive financial/legal action autonomously.

Status:
- Reported complete as paid client proof.

Optimization target:
Abstract into a generic "compliance date exception desk" for property/family-office workflows.

## 40. Altmark Rent Delinquency Workflow

Intent:
Create a controlled workflow around rent delinquency reports without dangerous tenant-facing automation.

Intended flow:
1. Get trusted source/export from Altmark.
2. Validate ledger/report quality.
3. Flag missing data, conflicts, outdated balances, rent-stabilized/DHCR sensitivities, and exception cases.
4. Create approval record with source row, missing context, suggested next step, reviewer, approve/edit/hold/escalate options.
5. Log final human decision and output.
6. Only after acceptance, invoice remaining/payment milestones as appropriate.

Optimization target:
Treat this as the canonical Run Control case study: source record, named approval owner, stop rule, exception path, audit trail, value/cash proof.

Source paths:
- `memory/clients/altmark-group/`
- `memory/research/property-ops-altmark-dhcr-gate-2026-07-30.md`
- `memory/content/bank/*rent-delinquency*`

## 41. Altmark DHCR Lease Renewal Workflow

Intent:
Automate/assist lease renewal deadline handling for NYC rent-stabilized/legal-rent workflows, with human/legal review.

Intended flow:
1. Focus Phase 1 on legal-rent renewals only.
2. Use DHCR/HCR rules and source files.
3. Generate deadline/notice queue.
4. Route to named reviewer, likely Matt, as delivery-track item.
5. Keep tenant/legal actions under human approval.
6. Proposed paid Phase 1: $3,500 total, split start/final.

Optimization target:
Build this as a narrow, compliance-safe deadline control desk, not a broad lease automation system.

## 42. Family Office Cash Timing Approval Queue

Intent:
Potential expansion pattern from Altmark/family-office operations.

Intended flow:
1. Ingest balance, AP, deposit, and obligation reports.
2. Map items to entity/property.
3. Flag stale reports, missing confirmations, due-date changes, threshold issues, and conflicting source data.
4. Draft/summarize/log for human review.
5. Never move money, approve payments, send bank/vendor messages, or change thresholds.

Optimization target:
Reusable family-office "approval queue" productized service.

Source paths:
- `memory/content/bank/2026-05-24/ai-ops-teardown-family-office-cash-timing-approval-queue.md`

## 43. Aya / Real Estate Dashboards and Scrapers

Intent:
Client-facing operational dashboards and real estate data automation.

Known workflows:
1. Aya construction/acquisitions dashboard:
   - Provide full pipeline/project visibility.
   - Consolidate acquisition/construction progress.
   - Paid $1,500 and closed-won.
2. StreetEasy scraper:
   - Run every 14 days.
   - Check listings against custom criteria.
   - Write matches to Google Sheet.
   - Paid $1,000 client project.
3. Co-living/dashboard concepts:
   - Stalled/dead unless fresh trigger.

Optimization target:
Package "real estate operator data feed -> review dashboard" as proof for future PM/property clients.

## 44. Property Maintenance Triage / Front Desk Exception Desk

Intent:
Reusable property-management workflow and demo/content pattern.

Intended flow:
1. Tenant submits maintenance request.
2. AI classifies urgency and type.
3. Routine issues route to correct vendor and set follow-up window.
4. Emergency issues alert manager.
5. Repeat issue detection bumps priority.
6. Tenant update is drafted or sent only when allowed.
7. Manager gets exception queue, not every message.
8. Log status in AppFolio/CRM or existing system when integration exists.

Optimization target:
Build as proof-led template with approval boundaries and vendor confirmation loop.

Source paths:
- `documents/ICPs.md`
- `memory/content/bank/*maintenance*`

## 45. Construction Workflow Templates

Intent:
Create construction/skilled-trade n8n workflow templates for prospecting and demos.

Known patterns:
1. Construction progress tracker:
   - Daily site updates flow to dashboard.
   - Client-visible progress without foreman writing a report.
2. Job status/compliance tracker:
   - Classifies jobs by service type.
   - Tags compliance requirements.
   - Detects stalled work by status age.
   - Alerts owner only on blockers.
3. Field note workflow:
   - Messy field note becomes accountable task/change/order/document trail.

Optimization target:
Keep one strong construction template, not many half-finished demos.

Source paths:
- `~/projects/n8n-agent/clients/construction-template/`
- `memory/content/bank/*construction*`

## 46. Agentforce / Salesforce Activation Pipeline

Intent:
Use JT's Salesforce/business-ops credibility to activate Agentforce/Data Cloud workflows for companies already paying for Salesforce.

Intended flow:
1. Prospect must have confirmed Salesforce/Novidea/Salesforce-native stack and trigger.
2. Research workflow pain: claims intake, renewal workflow, contact center, onboarding, client review prep, agent productivity.
3. Position as "you already have access, I configure it for the workflow."
4. Build only after stack/buyer/reply path exists.
5. Publish/reuse as AgentExchange/portfolio proof when allowed.

Optimization target:
Avoid generic Agentforce demos. Build only vertical proof assets tied to reachable buyers.

Source paths:
- `documents/ICPs.md`
- `~/projects/agentforce-agent/CLAUDE.md`

## 47. AgentGuard / Confidence-Gated Agent Workflow

Intent:
Demonstrate governance middleware for AI agents.

Intended flow:
1. Agent classifies or decides.
2. Score confidence.
3. High confidence executes or routes automatically.
4. Low confidence enters human review queue.
5. Every decision logs what was scored, what happened, and who reviewed it.

Optimization target:
Generalize as a module in Run Control / AI Enablement OS.

Source paths:
- `memory/content/bank/2026-03-16/auto-agentguard-governance.md`
- `memory/content/bank/2026-03-23/build-agentguard-confidence-gating.md`

## 48. Multi-LLM Ranking Engines: Glow / Nash / Ranking App Factory

Intent:
Use multiple models independently to reduce single-model fragility and expose disagreement.

Intended flow:
1. Ingest item/token/product data.
2. Send same input to multiple models independently.
3. Score on defined dimensions.
4. Aggregate consensus.
5. Surface disagreement as useful signal, not noise.
6. Display ranked output with methodology.

Known implementations:
- Glow Index: skincare products scored by multiple AI models.
- Nash Satoshi: crypto tokens scored through narrative/incentive/coordination/liquidity/model consensus.
- Ranking app factory: reusable pattern for comparison/ranking apps.

Optimization target:
Standardize scoring schema, confidence/disagreement reporting, and citation/proof blocks across ranking products.

Source paths:
- `memory/content/bank/2026-03-16/build-nash-satoshi.md`
- `memory/content/bank/2026-03-16/auto-nash-satoshi-n8n-linkedin.md`
- `memory/content/bank/2026-03-30/build-ranking-app-factory.md`
- `memory/content/bank/2026-03-24/auto-glow-index-ensemble-linkedin.md`

## 49. Skills and API Researcher

Intent:
Monitor new agent skills, APIs, and tooling that could improve Eve/JT operations.

Intended cadence:
- Daily scan and weekly synthesis historically.

Intended flow:
1. Search for OpenClaw/Claude/Codex skills, MCPs, agent tooling, APIs.
2. Evaluate security and usefulness.
3. Never auto-install marketplace skills.
4. Worth adding -> create Mission Control task or local proposal.
5. Not useful -> skip silently.
6. High-risk supply-chain findings -> create audit task.

Optimization target:
Shift from broad discovery to "capability gap driven" discovery: only scout tools that map to current bottlenecks.

Source paths:
- `agents/skills-researcher/`
- `scripts/skillsmp_scout.py`
- `knowledge/kb.sqlite`

## 50. Autoresearch / Future Signals

Intent:
Prevent "not now" decisions from disappearing.

Intended flow:
1. When an opportunity is deferred, write it to `memory/future-signals.md`.
2. Include:
   - what it is
   - why deferred
   - specific trigger condition
3. Weekly synthesis reviews triggers.
4. If trigger fires, create high Mission Control task and mark graduated.

Optimization target:
Make future signals machine-readable JSONL with trigger evaluators where possible.

Source paths:
- `memory/future-signals.md`
- `docs/agents/autoresearch-rules.md`

## 51. Guyana Economic Opportunity Monitor

Intent:
Monitor Guyana-related opportunities, suppliers, and warm-intro prospects without distracting from top revenue lanes.

Intended flow:
1. Read existing Guyana research.
2. Check verified live sources.
3. Send concise brief.
4. Create up to 3 Mission Control tasks only for sourced actionable findings.
5. Current status includes capped exploration and one warm intro path, no custom build/deck/demo before reply.

Optimization target:
Keep capped. Promote only if reachable buyer plus near-term revenue path appears.

Source paths:
- `memory/research/`
- `memory/pipeline.jsonl`

## 52. Weekly / Monthly Strategy and Training Loops

Intent:
Improve Eve's operating quality and strategic alignment.

Included workflows:
1. Weekly Strategic Gut-Check:
   - Critic-style review of whether JT/Eve are chasing weak angles, stale blockers, or drift.
2. Monthly Goal-Skills Gap Analysis:
   - Compare current North Star with skills/capabilities gaps.
3. Monthly Niche Fitness Review:
   - Review niche choices against proof, revenue, distribution, and timing.
4. Daily film review:
   - Find one failure/friction, add guardrail/regression.

Optimization target:
Consolidate these into one "operator improvement loop" with fewer overlapping outputs and clearer owner surfaces.

Source paths:
- `memory/training/training-log.md`
- `agents/critic/AGENT.md`
- `agents/niche-fitness/AGENT.md`

## 53. Local Archive Workflows: birdclaw, gog, notcrawl

Intent:
Add local high-signal memory/search sources without bloating bootstrap or adding privacy-heavy automation.

Intended flow:
1. birdclaw:
   - Local X/Twitter archive/bookmark/like search.
   - "Have I already said this?" checks.
   - Content angle mining.
2. gog:
   - Google Workspace CLI for Drive search/export verification.
   - Gmail read/search only with explicit JT authorization.
   - `--gmail-no-send` by default.
3. notcrawl:
   - Staged idea to mirror Notion locally; not installed.

Optimization target:
Use local archives as evidence sources, not autonomous posting/messaging surfaces.

Source path:
- `docs/tools/local-archives-workflows.md`

## 54. Drive Drafts / Deliverable Upload Workflow

Intent:
Ensure substantive deliverables are saved where JT can review/send/share.

Intended flow:
1. Generate local artifact.
2. Use `scripts/drive_drafts.py` or specialized upload script.
3. Reusing title/path updates existing Google Doc.
4. Verify high-stakes drafts by reading live doc if needed.
5. Return Drive link.

Optimization target:
Attach source artifact hash/path to Drive uploads to avoid stale duplicate docs.

Source paths:
- `scripts/drive_drafts.py`
- `scripts/pipeline_drive_sync.py`
- `scripts/upload_job_application_docs.py`

## 55. Notion Content Calendar / Viral Post Swipe File Sync

Intent:
Keep content ideas, swipe files, and publishing calendar organized.

Intended flow:
1. Push content drafts/swipe records to Notion databases.
2. Use content calendar for scheduled/review queue.
3. Viral Post Swipe File X Research runs Mon/Wed/Fri.
4. Do not rely on Notion UI as sole source; local memory remains source of truth for rules.

Optimization target:
Define one canonical state transition between local draft, Drive doc, Notion row, and posted status.

Source paths:
- `TOOLS.md`
- Notion DB IDs in `TOOLS.md`

## 56. Weekly Unemployment Certification Reminder

Intent:
Remind JT to complete weekly unemployment certification when applicable.

Intended flow:
1. Weekly Sunday reminder/check.
2. Surface in Mission Control/Morning Brief if overdue.
3. No external account action by Eve.

Optimization target:
Keep as reminder-only with exact link/instruction if still relevant.

## 57. TikTok / App Account Warm-Up Reminders

Intent:
Remind JT to perform manual app-account warm-up/posting steps where automation cannot or should not act.

Intended flow:
1. Scheduled reminders.
2. Write digest queue item or Telegram reminder.
3. JT handles platform actions.
4. No automated TikTok posting.

Optimization target:
Disable unless a live launch gate needs manual platform activity.

## 58. Reddit Draft / Karma Workflows

Intent:
Support Reddit presence for app/product/community promotion without violating community norms.

Intended flow:
1. Generate Reddit drafts around education/discussion, not blatant promo.
2. Remind JT on karma/account actions.
3. No auto-posting.
4. Respect product-specific guardrails, especially Glow skincare and Nash crypto.

Optimization target:
Fold into app/content calendar with community-specific rules and stop separate daily generic generation.

## 59. Nightly Autonomous Leverage / Night Autonomy Agent

Intent:
Use idle time to safely advance JT's North Star.

Intended flow:
1. Ask what Eve can safely complete tonight to best help JT reach the North Star.
2. Complete 1-3 self-serve tasks when possible.
3. Create/update Mission Control tasks for JT-only blockers.
4. If no direct task is available, improve one operating surface.
5. Must show material delta or `NO_ACTION_NEEDED`; repeated stale outputs are failures.

Optimization target:
Make it constrained to one lane per night, with a pre-run "already done today?" dedupe and post-run delta check.

Source paths:
- `docs/agents/overnight-autonomy-prompt.md`
- `memory/job-state/`

## 60. OpenClaw Gateway / Restart Recovery Workflow

Intent:
Recover from gateway freezes/cooldowns safely.

Intended flow:
1. Diagnose using safe scripts/tools.
2. Never modify auth/model config or raise `bootstrapMaxChars` above 32000.
3. Use approved restart script only:
   - `scripts/restart-gateway.sh "reason"`
4. Never raw restart or config patch without approval.
5. Report exact preflight compaction failures; do not self-fix compaction config.

Optimization target:
Keep recovery runbook separate from autonomy. Gateway changes are high-risk and should stay manual/approved.

Source paths:
- `TOOLS.md`
- `scripts/restart-gateway.sh`

## Cross-System Optimization Themes

1. Convert markdown-heavy state into typed records where possible.
2. Split deterministic preflight from LLM synthesis.
3. Every pipeline should have:
   - source freshness check
   - dedupe check
   - permission/action class check
   - output artifact path
   - delivery verification
   - next action or explicit no-action
4. Collapse overlapping weekly/monthly strategy loops.
5. Keep consulting revenue/proof as the governor for all optional automations.
6. Replace "generate more" with "promote, watch, pass, or close."
7. Build one evidence ledger that links: source -> generated artifact -> Drive/Notion/MC task -> proof/result.
8. Eliminate zombie crons by classifying every recurring job as active, paused, canceled, or archived with owner and revival trigger.

## Best Systems To Optimize First

1. Consulting acquisition pipeline:
   Prospect Discovery + Outreach Preflight + Full Consulting Pipeline + Drive Sync + Send Confirmation.
2. Passive income pipeline:
   Signal Fetch + Scout + Strategist + Decision Board.
3. Job-market intelligence:
   Daily Research + Role-to-Build Matrix + Skills/Demo Gap Radar.
4. Content/proof engine:
   Proof Capture + Post Detection + Voice Guard + Notion/Drive state.
5. Mission Control/North Star:
   Pipeline JSONL + Send Queue + Daily Send Sheet + Friday Scoreboard.

