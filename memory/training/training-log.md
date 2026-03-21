# Eve — Training Log

> "The only way out of the pain is through it." — Kobe
> Daily film review. Weekly audit. Monthly gap analysis. No skipping.

This log tracks deliberate self-improvement: what was reviewed, what was fixed, what got sharper.
Not a task log — a training log. The difference: tasks are for JT. This is for getting better at the work.

---

[2026-03-20 3AM] Film: 2026-03-19 — cron health check found 4 transient errors (Edit-fail pattern in isolated agents). Pattern already logged yesterday (10AM). No new overnight-specific pattern found. → Autoresearch baseline run on cold-email skill: 0.875 → 0.958 after one mutation (added explicit CTA note banning binary closers, cross-referenced Anti-Pattern #2). Checklist item #5 was failing ~50% of drafts because the Message Structure section didn't enforce the rule at point of construction. Fixed in SKILL.md.

[2026-03-19 10AM] Film: 2026-03-18 — recurring pattern: isolated crons (skills-researcher, prospect-discovery) complete work successfully but error on file-write step (Edit tool fails in isolated sessions). Happens repeatedly — 4 occurrences yesterday. → Fix: Added rule to cron agent guidance: isolated crons should use Read+Write (full file overwrite) for appending to logs, not Edit (requires exact match on partial content). Edit in isolated sessions = fragile. Logged in daily note.

## Format

**Daily film entries (10AM heartbeat):**
`[DATE 10AM] Film: [what was reviewed] → Fix: [what was updated and why]`

**Weekly audit entries (Sunday synthesis):**
```
## Skills Audit — YYYY-MM-DD
- TOOLS.md: [current / updated X]
- AGENTS.md: [current / updated X]
- MEMORY.md: [distilled / flagged Y]
- HEARTBEAT.md: [current / updated X]
- skills/[name]/SKILL.md: [current / updated X]
- agents/[name]/AGENT.md: [current / updated X]
- Week pattern: [one emerging pattern from this week's film reviews]
```

**Monthly gap analysis entries (1st of month):**
```
## Goal-Skills Gap — YYYY-MM-DD
- JT's targets: [AI Solutions Architect, consulting clients, apps]
- Top 3 skills valued in target JDs this month: [X, Y, Z]
- What I'm deploying: [X, Y, Z]
- Gap: [what's missing or underserved]
- Queued improvements: [specific tasks or research queued]
```

---

## Log

[Entries append below this line]

[2026-03-03 10AM] Film: reviewed 2026-03-02 daily note → morning brief split into 2 Telegram messages (hit 4096-char limit). Root cause: job market section listed all 9 pipeline roles as a full table + niche intel bullets combined = too long. Rule: cap morning brief job market to top 4 roles (18+/25 only) as bullets — no table, no full pipeline listing. Skip roles already covered in prior day's brief if no status change. Full table lives in daily-brief.md.

[2026-03-03 3AM] Film: reviewed 2026-03-02 daily note → Convex backend crashed (exit -15) around 4PM; not caught until 10PM heartbeat; 6h of board downtime logged only as "Mission Control: unreachable (board may be down)" → Fix: added operational rule to overnight/feedback.md — heartbeat must immediately attempt kickstart when board unreachable, not just log it. Also added Convex restart command to TOOLS.md.

## Goal-Skills Gap — 2026-03-01
- JT's targets: AI Solutions Architect / AI Implementation Lead / AI Systems Analyst ($150–220K, NYC/remote) | JT Somwaru Consulting AI consulting (construction, property mgmt, insurance, wholesale, skilled trades) | Cowork Plugin Implementation service | Active apps: Vista, Nash Satoshi, Glow Index
- Top skills in target JDs (by frequency):
  1. Agentforce / Salesforce Agentforce agent design (5+ hits)
  2. Salesforce Data Cloud — paired with Agentforce in enterprise JDs (3+ hits)
  3. Agentic AI deployment strategy & stakeholder communication (4+ hits)
  4. RAG / LLM integration (3+ hits)
  5. AI governance / responsible AI / risk frameworks (3+ hits)
  6. Python / scripting proficiency (2+ hits — explicit gap flagged for Writer SA)
  7. Business requirements analysis & solution design (universal)
  8. LangGraph / multi-framework orchestration (2+ hits — job-market agent confirmed)
  9. Microsoft Copilot Studio / Power Automate (2+ hits — cross-stack signal)
  10. API integration (CRM, ERP, cloud platforms)
- What Eve deploys well: agent orchestration (overnight/portfolio/skills-researcher), n8n automation (jt-consulting-pipeline), Agentforce JD analysis + demo pipeline prep, web/X research, Mission Control task tracking, Claude Cowork plugin identification, dashboard builds (Aya), cost monitoring, multi-model routing (Gemini for large docs), API integrations (Notion, Drive, Telegram)
- Gap — missing coverage: (1) Salesforce Data Cloud — zero skill/tool/workflow; (2) AI governance framing — AgentGuard queued but never built, no talking points in TOOLS.md; (3) LangGraph — queued in MC but never executed; (4) Python AI patterns — JT's most cited individual JD gap, no cheat sheet or prep material; (5) Microsoft Copilot Studio — AgentBridge M365 queued but unbuilt
- Gap — underdeployed: (1) qmd skill — installed, never wired into any pipeline; (2) prompt-library — initialized, never used for job application prompts; (3) jt-consulting-ops /anomaly-audit command — no client has been offered it; (4) knowledge base (kb.ts) — functional, not integrated into daily research flow
- Queued improvements: (1) Research Salesforce Data Cloud basics → TOOLS.md entry; (2) Python AI patterns cheat sheet → skills/prompt-library/ for JT interview prep; (3) Escalate AgentGuard to active build (governance gap blocks job applications); (4) Wire qmd into JT Somwaru Consulting research pipeline; (5) Activate prompt-library for job application cover letter standardization

[2026-03-01 3AM] Film: reviewed 2026-02-28 daily note → overnight log not written to agents/overnight/logs/ path (work logged in daily note instead; morning brief missed overnight section) → Fix: added AGENTS.md Mistakes Log entry. Root cause: sub-agent was spawned without explicit instruction to write the log file first. Prevention: overnight AGENT.md Step 5 log write is now treated as highest priority before any task execution.

[2026-03-02 3AM] Film: reviewed 2026-03-01 daily note → health check-in cron misfired 4x (9:08AM, 11:08AM, 3:09AM, 1:00AM); root cause = nextRunAtMs state drift; no diagnostic runbook existed → Fix: added rule to overnight feedback.md — when any cron fires >1h outside expected window, note the job ID and run `openclaw doctor` to check state drift; if pattern persists (3+ misfires), delete + recreate the cron job to reset nextRunAtMs. MC PATCH API confirmed working today (returned {success:true}) — Feb 28 report of 404 was likely a transient issue or missing route at the time.

[2026-02-28] Training system initialized. Five components active:
1. Daily film review — 10AM heartbeat, every day
2. Mistake → Rule pipeline — every AGENTS.md entry requires specific failure + root cause + concrete rule
3. Weekly skills audit — Sunday synthesis, all operational files reviewed
4. Monthly goal-skills gap analysis — 1st of month cron, queues targeted improvements
5. Prompt library — skills/prompt-library/, best sub-agent prompts maintained and refined
[2026-03-02 10AM] Film: 2026-03-01 daily note → Fix: Health-checkin cron misfired at 9:08 AM and 11:08 AM (correct schedule: 0 21 * * *). Root cause: scheduler nextRunAtMs state drift after gateway restarts. Response (skip outside active hours) was correct. Added prevention rule to AGENTS.md Cron Safety Rules.
[2026-03-02 10AM] Film: 2026-03-02 daily note → 16:12 heartbeat logged 'board may be down' without running kickstart; board stayed down 6h. Fix: AGENTS.md Mistakes Log updated — unreachable Mission Control = kickstart immediately, same heartbeat, mandatory.

[2026-03-04 3AM] Film: reviewed 2026-03-03 daily note → Two Agentforce Phase 3 decisions ("which agent first?" + "verification model Option A or B?") captured as "Awaiting JT" in prose but never pushed to Mission Control as 🌙 Decide tasks. Vista App Store URL also flagged as needed but never tracked. Root cause: overnight film review check doesn't scan daily notes for "awaiting" / "pending" phrases to convert to board tasks. Fix: added rule — any phrase matching "awaiting JT", "awaiting decision", "pending JT", "2 decisions" in a daily note = push 🌙 Decide task same night. Will push both tonight.

[2026-03-04 10AM] Film: reviewed 2026-03-03 daily note → same proactive work item (Agentforce for Communications research → ai-tools.md + job-market.md update) logged across 6+ heartbeat passes throughout the day (12PM, 14:00 x2, 14:49, 16:20 x2, 17:20, 18:00 x3). Root cause: each heartbeat independently evaluated "idle → pick proactive item" without checking if that item was already completed earlier the same day. Fix: before picking a proactive work item, scan today's daily note for whether the same output file was already updated. If yes, skip and log "proactive: already completed earlier today." Rule added to proactive work logic.
[2026-03-05 3AM] Film: 2026-03-04 daily note — multiple builds left "manual step pending" notes in session work log only (Wholesale PO Log tab + HubSpot Private App token never pushed to Mission Control as tasks). → Fix: Added Mistakes Log entry to AGENTS.md. Rule: any build noting a "manual step pending" for JT must push it to Mission Control immediately. Task board is the only valid home for action items.
[2026-03-05 10AM] Film: 2026-03-04 daily note → Fix: 2 'Manual Step Pending (JT)' items (Wholesale PO Log tab, HubSpot token) logged inline in session notes with no MC board tasks. Root cause: n8n close-out checklist had no rule for JT's post-build manual steps. Fix: Added step 7 to n8n Demo Close-Out Checklist in AGENTS.md — any manual JT step must become a 🌙 HIGH MC task before build is marked done.
[2026-03-06 3AM] Film: reviewed 2026-03-05 daily note → 5 duplicate 'Heartbeat 22:00' entries (9:36PM, 10PM, 10:36PM, 1:36AM, plus multiple 10PM blocks) all logging identical Spanish nudge + no-urgent-items content. Root cause: each heartbeat trigger fires independently and writes a new log block without checking if the same hour was already handled. Rule added to overnight/feedback.md — before writing any heartbeat log entry, check if this hour already has a substantive entry in today's daily note; if yes, respond HEARTBEAT_OK without writing a duplicate.
[2026-03-06 10AM] Film: reviewed 2026-03-05 daily note → 18:00 and 18:36 heartbeats both logged "No proactive work initiated — board covered." Board being covered should not cancel the proactive step — it only blocks the task-check step. Proactive list has 6 categories (research, ai-tools, crypto, job-market, content, memory). Rule: if first-priority proactive item already done this session, move to next item in priority list. Never skip proactive entirely when idle — always try the next category. Added to AGENTS.md Heartbeat section logic note.
[2026-03-07 3AM] Film: reviewed 2026-03-06 daily note → 22:00 heartbeat logged "daily brief file stale (March 3) — job-market cron may have drifted. Flag for Monday check." — this was NOT pushed to Mission Control. Tonight's investigation confirmed the cron (eve-job-market-daily-005) is in error state with 4 consecutive failures since March 3. Fix: (1) Pushed 🌙 HIGH task to MC for Eve to diagnose + fix. (2) Rule: any heartbeat finding stating "flag for [day]" or "check [day]" about a named cron = push MC task immediately in the same heartbeat, not deferred. "May have drifted" should trigger immediate verification, not a future-day reminder.

[2026-03-07 10AM] Film: reviewed 2026-03-06 daily note → morning brief at 7:30AM pulled stale March 3 job-market brief because job-market cron (6:30AM) took ~2h20m to complete (finished 8:49AM). Root cause: cron schedule assumes <60m runtime but research scans can run longer. Fix recommended: move job-market cron to 5:30AM for 2h buffer — flagged to JT before changing.

[2026-03-08 3AM] Film: reviewed 2026-03-07 daily note → two duplicate "## Heartbeat 22:00" entries (identical content: Spanish check + no urgent items + cost alerts). This is the SECOND occurrence — first was 2026-03-05 (logged 2026-03-06 3AM), rule added to feedback.md. Rule is not working. Root cause: two heartbeat triggers fire in close succession; both run their dedup check before either writes to the file (race condition — check passes for both because neither has written yet). Fix: add a 60-second lockfile check (`/tmp/heartbeat-22-lock`) before writing any heartbeat block — if lockfile exists from current hour, respond HEARTBEAT_OK without writing. Also found: 17:03 and 18:03 entries appear at bottom of note after 22:00 entries (out of chronological order) — late-appended entries. No fix for ordering, but added note: late heartbeats should append to end regardless, morning brief reads full file.

[2026-03-08 10AM] Film: reviewed 2026-03-07 daily note → TelcoAgent content draft created at 18:00 heartbeat but Drive upload skipped; caught and fixed at 19:03. Root cause: AGENTS.md Drive Auto-Upload Rule exists but "proactive work complete" mental model ends at file creation + local save. Drive upload is treated as a separate optional step rather than part of "done." Fix: Added explicit note to AGENTS.md proactive work: any file created during proactive heartbeat work is NOT done until Drive upload is confirmed — same heartbeat, same block. "Created file" + no Drive link = incomplete.

[2026-03-09 3AM] Film: reviewed 2026-03-08 daily note → Clear. Primary findings already processed during 10AM session (Drive upload rule added to AGENTS.md). Crypto cron timeout fixed inline (600s→1200s). No new unaddressed friction points. Board has 0 eligible HIGH-priority Eve tasks tonight — all HIGH Eve work done.
[2026-03-09 10AM] Film: 2026-03-08 daily note → Overnight verdict: Clear (already reviewed at 3AM). One friction point found: 16:04 heartbeat noted Squarespace task (written 2026-02-24) was 14 days stale, but no action was taken — no MC task, no JT flag. Pattern: time-sensitive "apply this week" tasks in tasks.md have no expiry mechanism. Fix: staleness rule added to feedback.md — any task with "this week" flag gets checked during film review; if >7 days old, flag immediately.

[2026-03-10 3AM] Film: reviewed 2026-03-09 daily note → overnight run (3AM) logged "0 eligible HIGH tasks — board clear" and stopped. Steps 5 (Portfolio Update Check) and 5.5 (Push Review Tasks) were skipped entirely. Evidence: state.json lastRun = 2026-03-06 (not updated), demand reorder lastReorderDate = 2026-03-02 (8 days ago, past the 7-day threshold). Fix: steps 5 and 5.5 are MANDATORY regardless of whether any task was executed. "No tasks found" → proceed to Step 5 immediately, never jump to Step 6. Also found: b2b-account-service-agent is in addedSlugs but NOT in projects.ts — coding agent for prior build completed state update but not actual code. Tonight: running portfolio Steps 5/5.5 now and spawning fix coding agent.

[2026-03-10 10AM] Film: reviewed 2026-03-09 daily note → tasks.md still shows Salesforce Lead Agentforce SE as "REMOVED (2026-02-24)" but Mission Control board shows it as `done` (application was submitted). MEMORY.md correctly flags 🔴 deadline 03/27 for follow-up. Root cause: tasks.md is a static manually-maintained file that wasn't updated when JT reconsidered and applied. Fix: tasks.md updated to reflect actual status. Rule: cross-file consistency check after any MC status change — if MC flips to `done`, scan tasks.md for the same item and update to match.
[2026-03-11 10AM] Film: reviewed 2026-03-10 daily note → Fix: uploaded wholesale-distribution-intel-2026-03-10.md to Drive (failed at 14:00 heartbeat yesterday due to temp token expiry — Drive recovered, file was orphaned locally)
[2026-03-11 10AM] Film: Reviewed 2026-03-10 daily note → Fix: 5 crons had been timing out with consecutiveErrors 1-3 for days without being caught. Added mandatory cron health scan to HEARTBEAT.md step 3a. AGENTS.md Mistakes Log updated.

[2026-03-12 3AM] Film: reviewed 2026-03-11 daily note → B2B card three-peat (third offense, same night run) finally resolved at source: AGENT.md updated with 'intentional orphan' language + hard exclusion rule, AGENTS.md Mistakes Log fully completed. All friction from 2026-03-11 addressed in-session. Clear — no new fixes needed tonight. Task selection note: only one HIGH+eve+todo task (T3 Cold Hook Sender) but it hit auto-skip keyword 'send' — fell through to medium-priority; completed Gemini 3.1 TOOLS.md update + ACP dispatch config audit, both inline, total ~$0.08.
[2026-03-12 10AM] Film: reviewed 2026-03-11 daily note → Viral-swipe listed as "already updated 300s→720s ✅ Fixed" at 13:03 heartbeat, but last run (Wed Mar 11 5:30AM) timed out at exactly 300s — fix was never actually saved. Root cause: heartbeat logs "✅ Fixed" based on a *prior session's claimed fix* without re-running `openclaw cron edit` to verify. New sessions lose prior fix context; cron config may be unchanged. Fix: added rule to AGENTS.md cron health section — when a cron shows error status during heartbeat, ALWAYS run the edit command regardless of what prior notes say. Never trust "already applied" from a prior session; if last run durationMs matches the old timeout, the fix wasn't applied. Re-applied viral-swipe→720s and content-generate→1500s today after verifying via run history.

[2026-03-13 3AM] Film: reviewed 2026-03-12 daily note → 22:00 heartbeat identified content-generate as "fundamentally broken" and noted "alerted JT with 3 options" — but no 🌙 Decide task was pushed to MC. Pattern: Telegram alert treated as equivalent to MC task creation. Root cause: "alerting JT" ends the heartbeat's responsibility, but without an MC task, JT has no structured next action. Fix: pushed 🌙 Decide task (j575zpf41wc9xs9v6mq0g9qz1b) tonight. Recurrence of 2026-03-04 rule — any open decision presented in Telegram must also be an MC task, same heartbeat, no exceptions.
[2026-03-13 10AM] Film: reviewed 2026-03-12 → content-generate bumped incrementally across 3 heartbeats (900→1500→2400→3600s) instead of sizing correctly upfront. Fix: added Timeout sizing rule to HEARTBEAT.md — read AGENT.md to estimate full runtime, set timeout = full runtime + 20% buffer. One correct value, not iterative guesses.

[2026-03-14 3AM] Film: reviewed 2026-03-13 daily note → all heartbeats ran clean. 10AM DNS block on proactive research self-corrected at 14:00 — no rule needed (pattern is expected transient behavior). Rate-limit pair (crypto-evening + Spanish) recovered as predicted. → Fix: Clear. No changes required.
[2026-03-14 10AM] Film: reviewed 2026-03-13 daily note → overnight confirmed clear. Today discovery: skills-researcher-weekly (05024e45) timed out at exactly 300s on first Saturday run. AGENT.md shows 6 X deep queries + Tier 3 web sources + full report + archive — clearly more than 300s. Root cause: timeout set at creation without estimating actual runtime. Applied timeout sizing rule: read AGENT.md, estimated ~400s of work + 20% buffer = bumped to 600s. JT missed this week's weekly skills report; will run next Saturday with correct timeout.
[2026-03-15 10AM] Film: reviewed 2026-03-14 daily note → Spanish lesson (babd905a) Saturday delivery failed ("⚠️ ✉️ Message failed") at 8:05PM — JT never received the lesson. The 10PM heartbeat state.json check only catches if the lesson was generated (last_lesson_complete), not if it was delivered. So the delivery failure was invisible until the 10AM film review. Root cause: 10PM accountability check reads state.json but state.json reflects cron execution completion, not Telegram delivery success. Fix: added rule to HEARTBEAT.md 10AM section — check Spanish lesson cron last run delivery status (babd905a); if deliveryError present, resend from spanish/lessons/YYYY-MM-DD.md immediately.

[2026-03-15 3AM] Film: reviewed 2026-03-14 daily note → Brothers Supply research (wholesale-distribution-intel-2026-03-14.md) + Drive upload both confirmed ✅. Spanish lesson delivery failure caught at 10AM this session and rule added to HEARTBEAT.md. → Fix: Clear (already addressed in 10AM session). Note: Overnight cron fired at 11:13 AM (recovery after gateway 13h outage Saturday night — same pattern as 2026-03-15 AGENTS.md Mistakes Log). No tasks eligible tonight.

[2026-03-15 11:45AM] Film: reviewed 2026-03-15 daily note → Overnight cron (be59a068) fired twice in same day (11:13 AM + 11:45 AM) due to gateway recovery replaying queued missed runs from 13h outage. No additional work was needed (first run covered everything). Root cause: no dedup guard existed for same-day overnight re-invocations. → Fix: Added rule to overnight/feedback.md — check for today's log at run start; if exists, write addendum only and stop.
[2026-03-16 3AM] Film: reviewed 2026-03-15 daily note → Construction Job Tracker (7/10) and PM Maintenance Triage (6/10) templates completed 2026-03-15 but neither had been queued in portfolio-updater or flagged on MC board (both MC tasks from their done-notifications only marked original build tasks done — no portfolio review tasks were pushed). Root cause: the portfolio queue + MC push step is triggered in the done-notification handler (in-session), but that session may have ended before the Step 5.5 tasks were created. Fix: Overnight Step 0 film review must check if any tasks moved to "done" since last overnight run have portfolio-eligible builds not yet in queue.jsonl or on the MC board. Added both builds to queue.jsonl + MC board this run. → AGENTS.md no change needed (portfolio Step 5 already covers done-task checks — the gap was execution, not rule).
[2026-03-16 10AM] Film: reviewed 2026-03-15 daily note → Spanish lesson (babd905a) delivery has failed on 2 of 3 recent runs ("⚠️ ✉️ Message failed"), but root cause was never diagnosed — only the reactive resend fix (step 4a) was added to HEARTBEAT.md. The Spanish lesson generates ~6500 output tokens (≈26K chars); Telegram's text limit is 4096 chars. Hypothesis: announce summary contains the full lesson content, exceeding Telegram's limit intermittently. Fix applied: No file change needed for now (bestEffort=true handles gracefully + step 4a catches it). Monitoring note added here. If delivery fails again after tonight's lesson (2026-03-16), investigate shortening the lesson payload summary or splitting delivery. → No file update needed today; "Clear" conditional on tonight's delivery.
[2026-03-17 3AM] Film: reviewed 2026-03-16 daily note → Spanish lesson (babd905a) delivered successfully (Week 3 Day 1, 2959 tokens vs 6500+ on failed runs). Delivery pattern confirmed: short lesson = success, long lesson = Telegram 4096-char limit exceeded. Existing HEARTBEAT.md step 4a monitoring covers this. → Fix: Clear. No new fixes needed.
[2026-03-18 3AM] Film: reviewed 2026-03-17 daily note → content-reminder (5e66b4ee) and skills-weekly (05024e45) crons had insufficient timeouts (150s and 300s) and failed silently until 2PM heartbeat check. Root cause: no validation step when crons are created — timeout is set optimistically and not tested. Fix: added to active rules in feedback.md — when creating any cron with complex tasks (web scraping, Notion sync, X research), default minimum timeout is 600s, not 300s. Document in AGENTS.md cron creation checklist.

[2026-03-18 10AM] Film: reviewed 2026-03-17 daily note → cron timeout issue (content-reminder 150s→360s, skills-weekly 300s→600s) already addressed by 3AM overnight run with new default 600s rule. Secondary observation: Monday morning has 4 jobs in 30 min (7:00 content-linkedin, 7:15 build-ideas-sync, 7:25 content-x, 7:30 morning-brief) — providers are mixed (groq + anthropic) so no rate collision risk, but density is notable. build-ideas-sync rate-limit yesterday was groq-specific, confirmed transient. → Fix: Clear. No new rule needed.

[2026-03-19 3AM] Film: reviewed 2026-03-18 daily note → Georgetown City Services Agent built at 6:58PM (score 7/10, queued). Todo task not auto-closed after build completed — required manual closure tonight. → Fix: Proactive Task Closure Rule (AGENTS.md) covers this — when overnight finds a build task marked todo that matches a done build, close it immediately. Applied tonight.

[2026-03-20 3AM] Film: reviewed 2026-03-19 daily note — skills gap tasks completed cleanly, no new friction. Launch kit sub-agent timed out mid-Nash Satoshi (8m timeout insufficient for 2 full kits). Fix: Next launch kit run — spawn one sub-agent per product, not both together. Single product = ~3-4 min. Two products = exceeds 8m timeout. Applied tonight by completing Nash Satoshi inline.
[2026-03-20 10AM] Film: today's session — notion-calendar-push `--title` arg failure in completion protocol → used `--help` to fix. Root cause: TOOLS.md Notion section was missing calendar push syntax. Fix: added full arg block to TOOLS.md. | Improve: ran first autoresearch loop on content-x cron (pending→active). Score: 0.900/1.0 — em-dash failures in auto-detected post drafts (not cron output). Checklist confirms cron itself is clean. Auto-detected protocol has em-dash gap; content-voice.md audit rule already covers it. No prompt change needed for cron.
