# Mistakes Log — Recent Entries
> Source: AGENTS.md §Mistakes Log
> Full archive: docs/agents/mistakes-log.md

## Logging Rule
Every entry MUST have six fields: (1) specific failure, (2) root cause one level deeper than "I forgot," (3) concrete guardrail/rule, (4) regression check that would catch recurrence, (5) owner surface updated, (6) verification/date. A mistake entry without a regression check + owner surface is incomplete — finish it before moving on. Reference: `docs/agents/regression-checks.md`.

## Recent Entries (2026-04)

| Date | Mistake | Fix |
|------|---------|-----|
| 2026-04-21 | **TikTok Text Formatting:** Slide captions incorrectly included raw AI instructions like `[Hook — "Text"]` onto the visible slide. | **Root Cause:** Script regex extraction parsed lines starting with `SLIDE X:` instead of stripping and sanitizing bracketed metadata out of the remaining text.<br>**Rule:** Any script that renders LLM-output text into visual formats (video, slides, UI) MUST pass through a dedicated, strict sanitization regex filter (e.g. stripping `[...]`, `CAPTION:`, etc.) before rendering. Never assume LLM output is 100% clean formatting. |
| 2026-04-14 | content-voice.md wiped by LCM compaction — file went from 251 lines (full banned patterns, proof points, voice rules, 6 techniques, audit checklist) to 1 line. Root cause: (1) `freshTailCount: 6` in LCM config kept only 6 lines fresh — rest was summarized. If the model saw only partial context at compaction time, it could summarize from the truncated view. (2) backup.sh backs up from working directory, not git — the wiped version was captured in every backup from March 12 onward, eliminating the recovery path. (3) No integrity monitoring existed for critical memory files. | Rule: **(1) Raise freshTailCount 6→50 in openclaw.json (plugins.entries.lossless-claw.config.freshTailCount). (2) Deploy weekly integrity cron (Sundays 6AM ET, UUID: e7f6e65a) that compares 9 critical files against git references and auto-restores if >50% lost. (3) Never rely on backup.sh for recovery — backup captures working directory state, not git state. (4) Any new critical file (AGENT.md, SKILL.md, content-voice.md) must be added to scripts/critical-files-integrity.py FILE_REFS dict immediately on creation.** |
| 2026-04-14 | content-scheduler: Tuesday X post recycled the same two contrast pairs ("the ones moving fast... / the ones who haven't moved yet," "who owns the deployment") from the LinkedIn Monday post. Both posts went out with identical sharpest lines. Root cause: no rule existed requiring the X version to earn its own framing — the AGENT.md Platform Separation Rules said "never share copy" but didn't define what "copy" means or include a contrast-pair dedup check. | Rule: **Before saving any X post, grep the weekly file for shared contrast pairs or key phrases that appeared in the LinkedIn version. If the same two-part structure appears in both, rewrite the X version to lead with a different observation. The X version must never recycle LinkedIn's sharpest lines verbatim. Rule added to content-scheduler/AGENT.md §Platform Separation Rules + X checklist.** |
| 2026-04-11 | outreach-pipeline: April 1 batch (7 prospects) all had M1 sent correctly but M2 MC tasks were never created. Pipeline logged M2 due dates but no MC task was created → 6 days of silence on 7 warm prospects. Root cause: process logged the due date but skipped the step of creating the actual Mission Control task for M2. | Rule: **Whenever M1 is sent and logged with an M2 due date, immediately create the M2 MC task on that date. Do not defer. Do not batch. The pipeline must never log a follow-up date without also creating the task to send it.** |
| 2026-04-08 | Telegram delivery failures across multiple crons (niche-monitor, Spanish Weekly Eval, crypto morning) — content generated correctly but empty/minimal messages rejected by Telegram. Root cause: crons send "All clear" or zero-content Telegram messages when no findings exist. Each cron fixed individually. | Rule: **All crons that save content + send Telegram: must skip Telegram send if content is empty or "All clear." Add `If no new [findings]: SKIP THE TELEGRAM SEND` to every Telegram-capable cron payload. Already applied: niche-monitor, Spanish Weekly Eval, crypto morning.** |
| 2026-04-15 | Used `Write` tool (full overwrite) on content-signals.md during Monday run, destroying all entries from 2026-03-13 through 2026-04-10 (17,475 bytes reduced to 1,827 bytes). Restored from git backup e0dc797. Root cause: treated content-signals.md as a create-from-scratch file rather than an append-only historical log; `write` overwrites, `edit` appends. | Rule: **content-signals.md is an APPEND-ONLY historical log. Always use `Edit` tool (append new section at end) — never `Write`. Check existing content with `tail` before appending. Verify file size with `wc -c` after any edit.**

2026-04-05 | Bootstrap files exceeded safe limits (AGENTS.md 32,311 / MEMORY.md 24,116 / TOOLS.md 19,030). Groq fallback never worked. LCM compaction failing silently. Retry loops burning rate limit. Root cause: no pre-append size check enforced, Groq free tier TPM too low for compaction, fallback model same provider as primary. | Rule: **Check `wc -c` before every append. Use openrouter/gpt-4o-mini as fallback (same provider as primary). LCM summaryModel must be Gemini Flash-Lite via openrouter. Max 3 retries with exponential backoff then stop + alert.** |
| 2026-04-02 | Resume and cover letter generated with em dashes throughout. Root cause: wrote files directly without loading job-application/SKILL.md first. | Rule: **Load job-application/SKILL.md before writing a single word of any application package.** |
| 2026-03-25 | Cover letter uploaded blank — body missing. Root cause: `parse_cover_letter_md()` requires exactly two `---` separators; had only one. | Rule: **Cover letter markdown must have two `---` separators. Always run `parse_cover_letter_md()` verification before uploading.** |

## Outreach MC Task Staleness (fixed 2026-04-15)
**Specific failure:** Multiple "Review + Send" MC tasks showed "(outreach drafted but M1 never sent)" even after M1 was sent. Examples: FCMRE, ProRealty USA, Atlas NYC, Citadel, BJD, Wynne — all had M1 sent in March, MC tasks still showing stale "never sent" descriptions in April.
**Root cause:** Eve creates the "Review + Send" MC task after the Outreach Agent finishes, then JT sends the message — but Eve had no mechanism to learn about the send. The outreach-draft.md correctly tracked "M1 SENT [date]" in its header, but this status never propagated to MC. The pipeline was a one-way street: draft → task → send → no feedback.
**Prevention rule:** `scripts/outreach_update.py` automates the full post-send update (outreach-draft.md status, pipeline.md, MC task close, M2/M3 task creation). AGENTS.md "Outreach Send Confirmation Handler" triggers it automatically when JT confirms a send. SKILL.md Step 8 now tells JT exactly what to reply ("sent M1 via LinkedIn"). Never create an outreach task without a send-confirmation mechanism.

## Missing Autonomous Validation (2026-04-20)
| Failure: | JT had to discover three critical bugs today: (1) 6 cron jobs were failing silently, (2) the crypto agent hallucinated an $87K BTC price because it didn't have live data, and (3) the TikTok pipeline posted duplicate slideshows due to a JSON parsing failure. |
| Root Cause: | I am operating reactively on "happy paths." I run scripts assuming they work perfectly and output correctly. I am not aggressively validating the integrity of the data *before* using it, nor am I verifying the output state (e.g., checking if the queue was actually updated). |
| Prevention Rule: | **Trust Nothing, Verify Everything.** 1) All data ingestion scripts must include a timestamp freshness check. If data is stale > 6 hours, throw an error, do not hallucinate. 2) Output must be verified. If a script updates a queue, read the queue immediately after execution to confirm the state change. 3) Proactive Heartbeat checks must include a scan of system log errors, not just successful completions.

## Cron Payload API Field Validation (2026-04-20)
| Failure: | The synthesis agent passed a "notes" field via POST to the Mission Control Tasks API, leading to a 500 error instead of a graceful skip. |
| Root Cause: | Subagents assume generic API payloads instead of reading the TS schema. |
| Prevention Rule: | Never pass undocumented fields to custom APIs. Subagents MUST verify the schema in  before attempting bulk mutation operations. |

## Cron Payload API Field Validation (2026-04-20)
| Failure: | The synthesis agent passed a "notes" field via POST to the Mission Control Tasks API, leading to a 500 error instead of a graceful skip. |
| Root Cause: | Subagents assume generic API payloads instead of reading the TS schema. |
| Prevention Rule: | Never pass undocumented fields to custom APIs. Subagents MUST verify the schema in `convex/tasks.ts` before attempting bulk mutation operations. |

## Nested Git Repository Corruption (2026-04-20)
| Failure: | The agent ran `git init` inside of `skills/` while inside the existing `openclaw-workspace` repository, corrupting the commit tree and preventing GitHub syncs. |
| Root Cause: | Blind assumption of directory state. Did not execute `git status` before initializing version control. |
| Prevention Rule: | Always run `git status` to verify if a working directory is already under version control before running `git init` or proposing repository creation. |

## Outreach - Bypassing Research Validation
- **Failure:** Drafted cold outreach for a company that had been bankrupt/liquidated for nearly two years (Common Living), and used obsolete CTO contacts for three others. 
- **Root Cause:** Fast-tracked straight to the "Outreach" stage of the pipeline based on old Mission Control database tags, bypassing the mandatory `research-agent` stage which would have caught the bankruptcy and role changes. I prioritized execution speed over data integrity.
- **Rule:** Never generate outreach drafts without validating the company's current status and the prospect's current role via live web search. If asked to "skip to outreach" or "fast track," refuse and run a lightweight validation first.

## 2026-04-27 — Sports GM raw value comparability error
- **Failure:** Treated KTC, FantasyCalc, and DynastyProcess raw trade values as directly comparable in @dynastyjig player-evaluation drafts, producing misleading statements like Kendre Miller KTC 2552 vs FantasyCalc 233 vs DynastyProcess 37.
- **Root cause:** The Sports GM fetcher normalized field names but did not preserve source semantics; downstream report generation compared `value` fields across sources without verifying whether each source shared the same scale. I optimized for automation speed before validating the measurement model.
- **Guardrail/rule:** Sports GM analysis must compare only comparable fields: overall rank, positional rank, percentiles/rank deltas, trends, and source direction. Raw values are source-local metadata. KTC and FantasyCalc values are not rank. DynastyProcess is secondary sanity-check only unless its source model is explicitly validated.
- **Regression check:** Before any player-specific Sports GM post is delivered, verify the draft includes at least two primary comparable rank references and contains no cross-source raw-value comparison phrased as a disagreement. Search generated drafts for `KTC:` / `FantasyCalc:` / `DynastyProcess:` and ensure adjacent numbers are labeled `rank`, `pos rank`, or explicitly `source-local value`.
- **Owner surface updated:** `scripts/sports_gm_fetch_prices.py`, `scripts/sports_gm_generate_report.py`, `skills/sports-gm/SKILL.md` pending, daily @dynastyjig cron prompt, `memory/content/bank/2026-04-27/dynasty-gm-player-evals.md` invalidated.
- **Verification/date:** 2026-04-27 — audited Kendre Miller raw source schema: KTC value 2552 but rank 257/RB69; FantasyCalc value 233 but rank 366/RB90; FantasyPros rank 341/RB91; DynastyProcess value 37 but rank ~240/RB~68. Rebuilt generator to use rank deltas and added FantasyPros.

## 2026-04-27 — Misinterpreted passive-income tab as task-pruning board
- **Failure:** Treated Mission Control's passive-income tab like a normal priority execution board and closed/pruned speculative passive-income ideas, when JT clarified the tab is intended to display all passive income ideas generated by the passive income agent, scored and ordered.
- **Root cause:** I applied generic task-board hygiene rules instead of preserving the domain-specific purpose of this tab as an idea portfolio. I optimized for focus but violated the product surface's purpose.
- **Guardrail/rule:** Passive-income tab = idea portfolio, not cleanup queue. Do not close/prune generated passive-income ideas just because they are low priority or stale. Keep ideas visible, assign score/order/status language, and separate active ideas from parked ideas via sortOrder/title/description.
- **Regression check:** Before patching Mission Control tasks in project `passive-income`, verify whether each task is an idea vs. one-off execution chore. Ideas must remain visible unless JT explicitly says remove/close.
- **Owner surface updated:** Mistakes log updated; passive-income Mission Control tasks to be corrected same turn.
- **Verification/date:** 2026-04-27 — correction triggered by JT clarification in Telegram.

## 2026-04-27 — Misclassified regular Glow Index execution tasks as Passive $ ideas
- **Failure:** Put Glow Index TikTok warm-up and Glow Index SEO/image deployment tasks on the Passive $ tab, even though JT clarified Passive $ is for passive-income ideas generated by the passive income agent, not regular execution tasks.
- **Root cause:** I conflated tasks that support a passive-income project with passive-income ideas themselves. I used project relevance instead of surface purpose as the classification rule.
- **Guardrail/rule:** Passive $ tab contains ideas/mechanisms/business concepts only. Execution chores for existing products go on the regular Tasks tab unless they are themselves the generated passive-income idea record.
- **Regression check:** Before assigning `project='passive-income'`, ask: “Is this an idea/mechanism to evaluate, or an execution step for an existing project?” Execution step → Tasks tab.
- **Owner surface updated:** Mission Control project fields corrected; mistakes log updated.
- **Verification/date:** 2026-04-27 — moved Glow TikTok and Glow deploy tasks out of Passive $, kept Glow programmatic SEO pipeline as actual Passive $ idea.

## 2026-04-29 — Dynasty X reply target over-repetition
- **Failure:** Daily Dynasty X reply suggestions repeatedly targeted the same two accounts (`@DynastyDwarf` and `@DFF_Dynasty`), making @dynastyjig engagement look narrow and repetitive.
- **Root cause:** Cron prompt used a narrow `from:` search seeded with a few known high-signal accounts and only required two unique accounts, so the ranking step optimized for familiar handles instead of audience/network diversity.
- **Guardrail/rule:** Reply-target generation must build a candidate pool from varied topical searches, require at least 10 candidates from 7 unique accounts, select 3 different accounts, and cap repeat-heavy accounts to at most one target total.
- **Regression check:** Before delivering any reply pack, verify `Account diversity: 3/3 unique accounts` and list skipped repeat-heavy accounts; if fewer than 3 unique accounts are found, return fewer targets rather than repeating.
- **Owner surface updated:** Cron `dynasty-replies-gen` (`8b968751-6e59-42e5-b2ce-09f57d36176c`) prompt updated with anti-repeat requirements, topical search expansion, and output diversity check.
- **Verification/date:** 2026-04-29 — cron payload patched and returned updated prompt; next run scheduled for 2026-04-30 11:00 ET.

## 2026-04-30 — Duplicate heartbeat daily-note entries
- **Failure:** April 29/30 heartbeat reminders fired close together and produced duplicate `## Heartbeat HH:MM` sections with substantially identical cost/cron/task status.
- **Root cause:** HEARTBEAT.md had proactive-work deduping, but no explicit idempotency rule for heartbeat daily-note logging.
- **Guardrail:** Added a Heartbeat Log Idempotency Rule requiring a check for the exact `## Heartbeat HH:MM` section before appending and suppression of duplicate reminders within 5 minutes unless state changed.
- **Regression check:** 10AM film review scans yesterday's daily note for duplicate heartbeat headings; every heartbeat must check the daily note before appending.
- **Owner surface updated:** `HEARTBEAT.md` and `docs/agents/regression-checks.md`.
- **Verification/date:** 2026-04-30 — owner files patched and active regression row added.

## 2026-05-01 — Resurfaced abandoned legacy consulting brand name
- **Failure:** Used the abandoned legacy consulting brand name in the monthly skills audit even though JT had previously instructed it be eliminated.
- **Root cause:** Stale historical memory/docs still contained the old brand name, so synthesis pulled from archived wording instead of canonical current naming.
- **Guardrail/rule:** Treat the old consulting brand string as a banned legacy name; use “JT Somwaru Consulting” or “consulting pipeline” instead. Before sending consulting/business-audit summaries, grep drafted text for the banned term.
- **Regression check:** Run the banned-term grep across bootstrap/docs/memory/skills/agents; it should return no user-facing references except unavoidable filesystem compatibility paths if any remain.
- **Owner surface updated:** Replaced legacy references across workspace text files; logged this correction in `docs/agents/mistakes-log-recent.md`.
- **Verification/date:** 2026-05-01; follow-up grep run after replacement.

## 2026-05-04 — Stale Dynasty X Reply Targets Suggested
- **Failure:** Suggested @dynastyjig reply targets from week-old X posts, which are unlikely to be seen or engaged with.
- **Root cause:** The sports-gm reply workflow allowed a "cached viable pool" fallback when fresh X API search was blocked, optimizing for producing an output instead of preserving engagement quality.
- **Guardrail/rule:** Daily reply target generation must fail closed when fresh X/search is unavailable. Every target must be ≤24h old, preferably 6-12h. Cached/old pools are banned for daily engagement replies.
- **Regression check:** `skills/sports-gm/SKILL.md` now requires `Freshness: all targets ≤24h old` in the final output and `BLOCKED: fresh X reply targets unavailable` when fresh search is blocked.
- **Owner surface updated:** `skills/sports-gm/SKILL.md` → Workflow: Dynasty X Replies.
- **Verification/date:** 2026-05-04 verified by editing the sports-gm skill and checking the replacement succeeded.

## 2026-05-04 — Nash Satoshi Daily Reddit Draft Missing
- **Failure:** Daily Nash Satoshi content generation covered an X post in the morning brief but did not require a Reddit-native draft, despite JT wanting daily content for both X and Reddit.
- **Root cause:** The Morning Brief spec only named `Daily Nash Satoshi X Post`; Reddit strategy existed elsewhere but was not wired into the daily delivery path. The cron payload also did not explicitly require rereading the latest HEARTBEAT.md section.
- **Guardrail/rule:** Daily Nash Satoshi content must include two separate platform-native outputs: one X post and one Reddit discussion draft. Reddit must not be a cross-post; it needs subreddit, title, body, fit rationale, and promo-risk note.
- **Regression check:** `HEARTBEAT.md` now requires 🐦 Daily Nash Satoshi X Post and 👽 Daily Nash Satoshi Reddit Draft. Cron `eve-morning-brief-001` payload now explicitly tells the agent to read HEARTBEAT.md fresh and generate both.
- **Owner surface updated:** `HEARTBEAT.md`; cron `eve-morning-brief-001`; `docs/agents/mistakes-log-recent.md`.
- **Verification/date:** 2026-05-04 verified via cron update output showing new payload and 240s timeout.
