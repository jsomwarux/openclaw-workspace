# Mistakes Log — Recent Entries
> Source: AGENTS.md §Mistakes Log
> Full archive: docs/agents/mistakes-log.md

## Logging Rule
Every entry MUST have six fields: (1) specific failure, (2) root cause one level deeper than "I forgot," (3) concrete guardrail/rule, (4) regression check that would catch recurrence, (5) owner surface updated, (6) verification/date. A mistake entry without a regression check + owner surface is incomplete — finish it before moving on. Reference: `docs/agents/regression-checks.md`.

## 2026-06-18 — Glow measurement update stalled after status promises
- **Failure:** JT had to ask "Update?" repeatedly during the Glow post-deploy measurement step because I twice said I was finishing the baseline note, then did not produce the artifact or proactively close the loop.
- **Root cause:** I treated the active-conversation status reply as progress instead of anchoring the work to an artifact gate. The task was no longer code-heavy, so I let measurement-note writing drift behind repeated observational checks.
- **Guardrail/rule:** For measurement or research tasks, every "working on it" status must name the current artifact gate: no artifact yet, artifact drafted, artifact verified, Mission Control updated, or blocker logged. If an update says "finishing the note," the next user-visible update must include the file path and task state, not another intent statement.
- **Regression check:** Before answering any future "Update?" on measurement work, run `test -f memory/app-marketing/[dated-measurement-note].md && rg -n "Decision|Next check|Source-tag" memory/app-marketing/[dated-measurement-note].md`; if the file does not exist, create it before replying unless there is a real blocker.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; current Glow measurement workflow.
- **Verification/date:** 2026-06-18 — logged the mistake before continuing, created `memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md`, updated stale crawler/serum guidance, and verified syntax/whitespace checks.

## 2026-06-16 — App Marketing prompt stalled after status replies
- **Failure:** JT had to ask for repeated updates on the Claude Fable App Marketing Strategy + Automation prompt because I sent status/context messages but did not create the local draft before pausing or getting interrupted.
- **Root cause:** I let the active-conversation update rule dominate the execution loop. I reported intent and gathered enough context, but did not anchor the work to the first irreversible artifact gate: local file exists.
- **Guardrail/rule:** For prompt-package work after scope is clear, create the local draft before any nonessential status update. Status replies must say which artifact gate has been reached: no file, local file, Drive URL, live verification, or recap.
- **Regression check:** Before answering "update?" on a prompt-package task, run `test -f memory/drafts/[slug].md && wc -c memory/drafts/[slug].md` or state "no local file yet"; completion requires local draft, Drive URL, live Google Docs verification, and weekly recap entry.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; current Claude Fable prompt-package operating behavior.
- **Verification/date:** 2026-06-16 — App Marketing Strategy + Automation prompt completed with local draft, Drive upload, live Google Docs verification `missing=[]`, and weekly recap entry.

## 2026-06-16 — Fable prompt referenced apps by name without project primers
- **Failure:** Prompt 1 asked Claude Fable 5 to decide whether Vista, Nash Satoshi, and Glow Index should receive time in the next 30 days without explaining what the apps are, and omitted Action Arena.
- **Root cause:** I wrote the prompt from workspace memory instead of from the external model's viewpoint. I treated project names as shared context even though Fable 5 would only see the pasted prompt.
- **Guardrail/rule:** External strategy prompts must include compact self-contained primers for every named app/project/client/agent being evaluated: what it is, current status, revenue/proof state, best growth hypothesis, constraints, and risks.
- **Regression check:** Before uploading any future Fable/external strategy prompt, scan for named project/app/client references and confirm each has a primer or is irrelevant to the requested decision.
- **Owner surface updated:** `memory/drafts/claude-fable-north-star-revenue-architecture-prompt-2026-06-16.md`, `skills/prompt-library/SKILL.md`, `AGENTS.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-16; Prompt 1 updated to include Vista, Nash Satoshi, Glow Index, and Action Arena project context plus an explicit no-prior-knowledge instruction.

## 2026-06-13 — Phase 2 site work stalled between short bursts
- **Failure:** During JT's approved Phase 2 jtsomwaru.com work, I repeatedly worked for a short burst, stopped at a partial state, and forced JT to ask "Update?" multiple times instead of carrying the task through implementation and verification.
- **Root cause:** I treated interim status replies as a substitute for continuous execution. The active-conversation update rules were followed superficially, but the task loop was not anchored to a completion gate like "new pages written, lint/build passed, screenshots captured, evidence report saved."
- **Guardrail/rule:** For approved multi-step work, define the next verification gate and keep executing until that gate is reached or a real blocker appears. Send proactive progress updates, but do not pause the work just because an update was sent.
- **Regression check:** On the next active multi-step coding task, verify there is no gap where JT has to ask for status before the current verification gate is attempted; final report must include the exact lint/build/test/evidence commands run.
- **Owner surface updated:** `AGENTS.md` rule 9c; this Mistakes Log entry.
- **Verification/date:** 2026-06-13 — continued Phase 2 after correction, completed the two offer pages, reran lint/build, captured Playwright screenshots, and saved the evidence report.

## 2026-06-12 — Fable closeout left deferred lanes in high priority
- **Failure:** After reporting the Fable North Star closeout as finished, live Mission Control still had Guyana validation tasks and a duplicate Glow metrics task in/near the high-priority layer, contradicting Fable's instruction to keep Guyana validation-only and freeze app/product work except gated Action Arena.
- **Root cause:** I verified the created artifacts and archive counts, but did not run a final Fable-specific priority-layer checklist against the live Mission Control high-priority set after the North Star audit script re-promoted stale tasks.
- **Guardrail/rule:** Any Fable/North Star closeout must verify the live high-priority layer contains only Altmark cash, active consulting sends, proof, or urgent ops; Guyana, app-marketing, passive-income, and product tasks must be medium/low/archived unless a trigger is explicitly documented.
- **Regression check:** Run `python3 scripts/mission_control_north_star_audit.py --dry-run` and a live `/api/tasks` high-priority query; dry run must show `changes=0/errors=0`, and the high todo/in-progress set must not include Guyana, generic app marketing, duplicate Glow metrics, or ungated Action Arena launch work.
- **Owner surface updated:** `scripts/mission_control_north_star_audit.py`, `reports/evidence/2026-06-12-fable-north-star-closeout.md`, `memory/2026-06-12.md`, `memory/weekly-recaps/current-week.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-12 — patched the audit script, reran it, verified follow-up dry run `changes=0/errors=0`, live Mission Control showed 260 active tasks, 5 high todo/in-progress tasks, and 0 overdue; duplicate Glow metrics task was archived while one low-priority Glow metrics task stayed active.

## Recent Entries (2026-04)

| Date | Mistake | Fix |
|------|---------|-----|

## 2026-06-07 — GA4 OAuth token cache was tracked in the workspace repo
- **Failure:** `memory/app-marketing/.ga4-oauth-token-cache.json` was already tracked by git and showed a refreshed OAuth access token in the working diff during the GitHub update pass.
- **Root cause:** The app-marketing runtime cache lived under a tracked memory path, and `.gitignore` blocked several OAuth/token patterns but did not include this exact cache file. Because the file was already tracked, normal ignore rules would not protect future diffs.
- **Guardrail/rule:** OAuth/token caches must stay local only. Remove tracked cache files from git with `git rm --cached`, add exact ignore rules, and scan staged changes for token patterns before any push.
- **Regression check:** After the cleanup commit, `git ls-files memory/app-marketing/.ga4-oauth-token-cache.json` must return no rows. During the cleanup commit only, `git diff --cached --name-status -- memory/app-marketing/.ga4-oauth-token-cache.json` may show a staged `D`; future pushes must not stage token-cache additions or modifications.
- **Owner surface updated:** `.gitignore`, git index, this Mistakes Log entry.
- **Verification/date:** 2026-06-07 — removed the GA4 token cache from git tracking with `git rm --cached`, added the exact `.gitignore` rule, and will run staged secret/name scans before push.

## 2026-06-07 — @jts_14 X research references were real but not packaged as a first-class ledger
- **Failure:** When JT asked what X posts were scraped, stored, analyzed, and applied for his main @jts_14 content, the answer made the evidence look mostly dynasty/betting because @jts_14 references were scattered across weekly content, viral swipe reports, raw JSON, and Notion pushes instead of one inspectable map.
- **Root cause:** The content system tracked platform reference mechanics and raw X research artifacts, but it did not force a source-to-draft ledger for @jts_14 separating topic selection from structure, credibility/proof, niche-signal-only inputs, and rejected sources. That let real research become operationally hard to audit.
- **Guardrail/rule:** Weekly @jts_14 X content must maintain `memory/content/jts14-x-reference-ledger-[MONDAY].md` with source URL, canonical lane, why selected, analyzed mechanic, influence type, draft touched, and rejection/constraint status. Do not claim @jts_14 X research is optimal unless the ledger exists and passes its guard.
- **Regression check:** `python3 scripts/jts14_x_reference_ledger_guard.py memory/content/jts14-x-reference-ledger-2026-06-01.md` must return `JTS14_X_REFERENCE_LEDGER_GUARD_PASS`.
- **Owner surface updated:** `memory/content/jts14-x-reference-ledger-2026-06-01.md`, `scripts/jts14_x_reference_ledger_guard.py`, `docs/agents/content-rules.md`, `skills/content-generation/SKILL.md`, `skills/x-research/SKILL.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-07 - guard added and run against the new ledger; weekly content guard remains the companion check for platform reference mechanics.

### 2026-06-15 addendum — ledger contract needed a deterministic builder
- **Failure:** The 2026-06-15 viral swipe/X research run saved useful artifacts and pushed examples, but `memory/content/jts14-x-reference-ledger-2026-06-15.md` was missing, so the swipe-to-draft path was still not inspectable even though the older ledger rule existed.
- **Root cause:** The rule depended on an agent or cron prompt remembering to package saved research into the ledger. There was a guard for validating an existing ledger, but no deterministic local builder and no weekly guard flag that required the ledger as part of delivery verification.
- **Guardrail/rule:** After weekly @jts_14 X artifacts exist, build the ledger with `scripts/build_jts14_x_reference_ledger.py` from the saved report, reply targets, and weekly content artifact. Weekly delivery checks should use `--require-jts14-ledger` when validating Monday X/LinkedIn recovery or generation.
- **Regression check:** `PYTHONPATH=scripts python3 -m unittest scripts/test_jts14_x_reference_ledger.py`; `python3 scripts/jts14_x_reference_ledger_guard.py memory/content/jts14-x-reference-ledger-2026-06-15.md`; `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-06-15.md --require-reference-map linkedin --require-reference-map x --require-jts14-ledger memory/content/jts14-x-reference-ledger-2026-06-15.md`.
- **Owner surface updated:** `scripts/build_jts14_x_reference_ledger.py`, `scripts/test_jts14_x_reference_ledger.py`, `scripts/content_distribution_guard.py`, `memory/content/jts14-x-reference-ledger-2026-06-15.md`, `skills/content-generation/SKILL.md`, `skills/x-research/SKILL.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-15 — generated the 2026-06-15 ledger with 21 rows; unit tests, py_compile, ledger guard, content distribution guard with required ledger, and scoped `git diff --check` all passed.

## 2026-06-07 — Low-value public-proof privacy cleanup post reached JT
- **Failure:** Delivered a Sunday LinkedIn recommendation about removing client names from JT's website / public proof privacy cleanup, which JT correctly rejected as not valuable, not worth posting, and not improving his positioning.
- **Root cause:** The content guard blocked internal content-system transparency but did not treat adjacent proof-hygiene/process-meta work as a low-value standalone angle. The generator optimized for "true and trust-related" instead of "buyer/recruiter/builder value that benefits JT."
- **Guardrail/rule:** Client-name removal, public proof cleanup, private-detail hiding, attribution cleanup, and "proof needs privacy" cannot be delivered as the main post. They can only support a real buyer pain, shipped outcome, current signal teardown, or permission-safe case study.
- **Regression check:** `python3 scripts/content_distribution_guard.py --linkedin-draft /tmp/bad_public_proof_privacy.md` must fail; `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-06-01.md` must pass after rejected Sunday LinkedIn/X entries are replaced.
- **Owner surface updated:** `AGENTS.md`, `skills/content-generation/SKILL.md`, `agents/autoresearch/checklists/content-generation.md`, `scripts/content_distribution_guard.py`, `memory/content-voice.md`, `memory/content/jt-voice-profile.md`, `docs/agents/content-rules.md`, `memory/FEEDBACK-LOG.md`, `memory/content/weekly-2026-06-01.md`, `memory/content/pending-posted-reply.json`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-07 — bad draft `/tmp/bad_public_proof_privacy.md` fails with `CONTENT_DISTRIBUTION_GUARD_FAIL`; corrected `memory/content/weekly-2026-06-01.md` passes `CONTENT_DISTRIBUTION_GUARD_PASS`; `python3 scripts/content_calendar_audit.py --week 2026-06-01` passes weekly/posted-log/crons; `posted-log.jsonl` and `pending-posted-reply.json` validate as JSON; existing Drive docs were reused/body-updated and live Google Docs API read confirmed old phrase absent and replacement phrase present.

## 2026-06-03 — Drive draft sync reused stale Google Doc body
- **Failure:** Told JT the Guyana Local Content Summit Drive draft contained the Guyanese-American line after checking the local markdown, but the live Google Doc still showed the older Kathy/GCCI body without that line.
- **Root cause:** `scripts/drive_drafts.py` was idempotent by title/folder and returned an existing Google Doc URL without replacing the document body, so rerunning the sync looked successful while leaving stale Drive content in place.
- **Guardrail/rule:** Corrected high-stakes drafts are not verified until the live Google Doc text is checked after sync. Existing title/path reuse must update the Google Doc body, not just return the URL.
- **Regression check:** After a corrected draft reuses an existing Drive doc, read/export the live Google Doc and verify the corrected phrase is present before sending the link.
- **Owner surface updated:** `scripts/drive_drafts.py`, `scripts/test_drive_drafts.py`, `TOOLS.md` Drive Drafts section, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-03 — `drive_drafts.py` now reports "Existing doc reused and body updated"; regression test `python3 -m unittest scripts/test_drive_drafts.py` passes for existing text docs and DOCX uploads; live Google Docs API read confirmed `Guyanese-American count: 6` and Kathy/GCCI contains the corrected personal-context line.

## 2026-05-29 — Nightly Leverage overfit to same Altmark blocker
- **Failure:** Nightly Leverage reports were not exact duplicates, but recent runs repeatedly treated adjacent Altmark prep artifacts/task repoints as fresh nightly wins while the real blocker still required JT/client input.
- **Root cause:** The cron prompt prioritized active revenue/client delivery but did not define material progress, compare the last two nightly runs, enforce a same-blocker cooldown, or rotate to self-serve work when the top blocker was unchanged.
- **Guardrail/rule:** Nightly Leverage must scan the last 7 days of nightly outputs, compare the last two runs, name a `Material delta`, and suppress/rotate when the same client/project/blocker appears twice without new external input or verification evidence.
- **Regression check:** After any Nightly Leverage report, 10AM film review checks that the report includes a material delta versus the last two nightly runs; if not, patch the cron and log the repeated blocker instead of accepting the report as progress.
- **Owner surface updated:** Live cron `003191af-45a7-4e3b-a824-f7a6cd52f8c7` / `nightly-autonomous-leverage-agent`, `docs/agents/regression-checks.md`, `memory/audits/xhigh-systems/2026-05-29-nightly-leverage-anti-repeat-audit.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-05-29 — prompt file created with anti-repeat/material-progress gate; live cron patch and verification performed same turn.

## 2026-05-27 — Paused Spanish lessons still triggered stale-state heartbeat failure
- **Failure:** The 10AM heartbeat Spanish state check failed with `FAIL: last lesson is stale: 2026-05-24 (3 days ago)` even though Spanish lessons were intentionally paused on 2026-05-26.
- **Root cause:** `spanish_state_check.py` validated freshness before accounting for the explicit `"paused": true` state, so a deliberate pause looked like a stale/broken lesson pipeline.
- **Guardrail/rule:** Paused Spanish state must still validate required fields and date sanity, then return `ok` with `paused:true` without requiring `last_lesson_date` to equal today or fall inside the freshness window.
- **Regression check:** `python3 scripts/spanish_state_check.py --max-age-days 2` and `python3 scripts/spanish_state_check.py --date 2026-05-27 --require-today` must pass while `spanish/state.json` has `"paused": true`.
- **Owner surface updated:** `scripts/spanish_state_check.py`, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-05-27 — paused-state validation added and verified during the 10AM heartbeat film review.

## 2026-05-27 — Repeated-noun contrarian pattern escaped LinkedIn content guard
- **Failure:** Delivered Wednesday LinkedIn scheduled content containing “The risk is not that nobody cares about cash. The risk is that timing decisions get assembled manually...” despite JT repeatedly banning the “X is not / it’s Y” contrarian reveal pattern.
- **Root cause:** The content voice rule was clear, but the executable guard only caught pronoun/comma variants like “it is not X, it is Y” and “X is not just Y. It is Z.” It missed the repeated-noun two-sentence variant because the second sentence reused “risk” instead of “it.”
- **Guardrail/rule:** Repeated-noun reveals like “The risk is not X. The risk is Y.” are banned as the same stale contrarian pattern. Rewrite to lead with the concrete failure moment, workflow, owner, number, or business constraint.
- **Regression check:** `python3 scripts/content_distribution_guard.py --linkedin-draft /tmp/bad_linkedin_risk.md` must fail on the repeated-noun reveal, and `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-05-25.md` must pass after the corrected draft.
- **Owner surface updated:** `scripts/content_distribution_guard.py`, `memory/content-voice.md`, `memory/FEEDBACK-LOG.md`, `memory/content/weekly-2026-05-25.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-05-27 — `/tmp/bad_linkedin_risk.md` and `/tmp/bad_linkedin_pronoun.md` both failed with `CONTENT_DISTRIBUTION_GUARD_FAIL`; corrected `memory/content/weekly-2026-05-25.md` passed `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-05-25.md`.

## 2026-05-27 — AI Ops Teardown Drive folder mixed source docs, support bundles, and stale weekly copies
- **Failure:** The AI Ops Teardown Drive folder did not contain the current cash-timing LinkedIn post, while old property-management chatbot opener copy appeared across multiple visible docs. Correcting the local weekly file did not update the already-uploaded Drive docs.
- **Root cause:** The Drive upload flow treated weekly batches, bank docs, prep packs, and source teardowns as equivalent content artifacts. `drive_drafts.py` is idempotent by title/folder, so rerunning an upload reused existing docs without replacing stale body text, and old support bundles stayed in the active AI Ops folder beside canonical source teardowns.
- **Guardrail/rule:** AI Ops Teardown Drive folder top level must contain one canonical document per teardown plus `Archive/`. Prep packs, delivery bundles, superseded drafts, and weekly batches belong in `Archive/` or `Content/Weekly`, not beside canonical teardowns. When local content is corrected after Drive upload, update the existing Google Doc body or create a new canonical doc and archive stale duplicates.
- **Regression check:** After any AI Ops Teardown correction/upload, list `Eve — Drafts / Content / LinkedIn / AI Ops Teardowns` and verify the expected teardown doc exists at top level, support bundles are under `Archive/`, and exported Drive docs do not contain the corrected banned/stale text.
- **Owner surface updated:** Google Drive folder structure, `memory/content/bank/2026-05-24/ai-ops-teardown-family-office-cash-timing-approval-queue.md`, weekly Drive docs `Weekly Content - 2026-05-25` and `LinkedIn Weekly Queue - 2026-05-25`, this Mistakes Log entry.
- **Verification/date:** 2026-05-27 — exported Drive docs show `old_bad=False` for “The risk is not that nobody cares about cash” and `new=True` for “The fragile moment is the manual assembly”; AI Ops Teardown folder top level now includes `AI Ops Teardown - Family Office Cash Timing Approval Queue - 2026-05-24` plus canonical teardown docs and `Archive/`.

## 2026-05-14 — Search Console verification status carried forward without API validation
- **Failure:** Reported Nash Search Console as pending DNS verification after JT later clarified it was already verified, then initially mapped `https://nashsatoshi.com/` as a URL-prefix property instead of checking the actual verified property list.
- **Root cause:** I treated a human briefing line as source-of-truth infrastructure state and only tested GA4, not the Search Console `sites.list` endpoint, before finalizing App Marketing OS status.
- **Guardrail/rule:** Before reporting Search Console status or writing account-map entries, run the Search Console sites list API with the active OAuth token and use the returned `siteUrl` exactly (`sc-domain:...` vs URL-prefix). Do not infer property type from domain names.
- **Regression check:** App Marketing web analytics integration is not done until `scripts/app_marketing_connectors/web_metrics.py` returns `search_console_ok` for every mapped verified Search Console property or records the exact HTTP error/property mismatch.
- **Owner surface updated:** `memory/app-marketing/account-map.json`, `scripts/app_marketing_connectors/web_metrics.py`, `scripts/app_marketing_collect_metrics.py`, `memory/app-marketing/metrics-automation-plan.md`, `MEMORY.md`, daily note, and Mistakes Log.
- **Verification/date:** 2026-05-14 — `sites.list` returned `sc-domain:nashsatoshi.com` and `sc-domain:glowindex.co` with `siteOwner`; both `searchAnalytics.query` calls returned `search_console_ok`; stale `pending_dns` references cleared from App Marketing files.

| 2026-05-06 | **Action Arena / Dynasty Simulator Conflation:** Described Action Arena as if it were the dynasty fantasy football simulator. | **Root Cause:** I relied on a compressed memory phrase “sports/product lane” and generalized from Sports GM context instead of verifying the product positioning in `skills/sports-gm/SKILL.md`, where Action Arena and Dynasty Simulator are explicitly separate lanes. **Rule:** Before giving strategy for any sports app, read `skills/sports-gm/SKILL.md` Product Positioning sections and distinguish Action Arena (fake-budget betting strategy leagues, no real money) from Dynasty Fantasy Football Simulator (persistent dynasty simulation). **Regression check:** Any future answer mentioning Action Arena must include “fake budget/no real money” or “league betting-strategy game,” and must not describe dynasty roster simulation mechanics unless separately discussing Dynasty Simulator. **Owner surface updated:** `MEMORY.md` corrected; Mistakes Log updated. **Verification/date:** 2026-05-06 — corrected after JT explicitly clarified the app definition. |
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
## 2026-05-05 — Stale source framed as this-week content intel
- **Failure:** Tuesday LinkedIn content claimed "one property management report this week" showed a 60%+ AI adoption gap. The cited Building Engines/JLL/BOMA report was from January, not this week, so the content laundered an old source as fresh market intel.
- **Root cause:** Weekly intel synthesis stored a dated source without preserving/validating the publication date, then the content generator converted it into freshness language. There was no source-date gate for phrases like "this week" or for market-stat claims.
- **Guardrail/rule:** Any content draft that says "this week," "today," "new," "fresh," or uses a market stat must verify source date within 14 days, or explicitly label older context with date. Unknown source date means cut the stat and use an operator-observation angle instead.
- **Regression check:** Before content delivery, scan drafts for freshness words and numeric/stat claims; each must have a dated source within 14 days or an explicit older-context label. Check `memory/content/weekly-intel-brief.md` entries include source name + source date.
- **Owner surface updated:** `docs/agents/content-rules.md`, `docs/agents/regression-checks.md`, `memory/content/weekly-intel-brief.md`, `memory/content/weekly-2026-05-04.md`.
- **Verification/date:** 2026-05-05 — removed stale PM stat from weekly intel, rewrote Tuesday LinkedIn draft without the January-source claim, added Source Freshness Gate and regression check.


## 2026-05-05 — Incorrect site contact email changed to Yahoo
- **Failure:** Updated jtsomwaru.com contact metadata to `jsomwarux@yahoo.com` even though JT's site contact should always be `jtsomwaru@gmail.com`.
- **Root cause:** Treated stale project docs/llms metadata as authoritative instead of preserving the existing live contact convention and confirming against current site usage.
- **Guardrail/rule:** For personal website contact info, `jtsomwaru@gmail.com` is canonical. Do not change site contact email unless JT explicitly says the new address.
- **Regression check:** Before any future site contact/metadata deploy, grep `src public CLAUDE.md README.md documents` for email addresses and verify only the canonical site contact appears.
- **Owner surface updated:** Site repo `CLAUDE.md`, `public/llms.txt`, and `src/components/Contact.tsx` corrected; this mistakes log now records the canonical rule.
- **Verification/date:** 2026-05-05 — grep confirmed `jtsomwaru@gmail.com` in Contact/Guyana/llms/CLAUDE and no `jsomwarux@yahoo.com` in checked site paths; build + lint passed.

## 2026-05-09 — @dynastyjig stale/recycled content pack
- **Failure:** Delivered an @dynastyjig post pack that reused stale pattern inputs, included a player JT had already posted (Demond Claiborne), and leaned on outdated/generic betting angles.
- **Root cause:** The Sports GM drafting path treated old swipe mechanics as acceptable content inputs and did not enforce a same-day freshness/no-repeat gate before finalizing drafts.
- **Guardrail/rule:** @dynastyjig packs must run a preflight: fresh market snapshot from today, no player/topic already posted by JT when known from context, no slate/team odds unless verified current, and every draft must pass the current content-voice X checklist.
- **Regression check:** Before sending any @dynastyjig pack, verify the output file includes a `Quality gate applied` section listing freshness source, repeat exclusions, and why the recommended first post is not stale/generic.
- **Owner surface updated:** `skills/sports-gm/SKILL.md` and `memory/content/bank/2026-05-09/dynastyjig-niche-growth-post-pack.md`.
- **Verification/date:** 2026-05-09 — stale pack replaced with revised pack using 2026-05-09 Sports GM data and Demond Claiborne excluded.

## 2026-05-10 — Passive-income concepts did not populate Passive $ correctly
- **Failure:** New passive-income 🟢 concepts appeared incomplete/misrouted on Mission Control Passive $: PDRN Decoder and CollectionProof had blank concept fields, while RouteShade inherited PDRN blueprint text.
- **Root cause:** Mission Control `/api/passive-income` split strategist reports only on `##` headings, so top scorecard sections swallowed later `# 🟢 Blueprint:` content. The parser did not merge blueprint sections back into matching idea cards and did not fail closed on `ALREADY QUEUED` sections.
- **Guardrail/rule:** Passive-income parser now splits on level-1/2 headings, skips `# 🟢 Blueprint:` as standalone cards, skips `ALREADY QUEUED` idea cards, and merges blueprint concept/revenue/stack/marketing/automation details into the matching idea.
- **Regression check:** After strategist runs, verify `/api/passive-income` shows every 🟢 idea with non-empty `concept`, no `ALREADY QUEUED` duplicate cards, and exactly one active `[PI] Build:` task under `project=passive-income` for each 🟢 idea.
- **Owner surface updated:** `mission-control/app/api/passive-income/route.ts`, `agents/autoresearch/checklists/passive-income-strategist.md`, and `docs/agents/regression-checks.md`.
- **Verification/date:** 2026-05-10 — `bunx tsc --noEmit` passed; `/api/passive-income` returns PDRN Decoder concept_len 518, CollectionProof concept_len 498, RouteShade count 0; MC tasks show active `[PI] Build:` tasks for both PDRN Decoder and CollectionProof in `project=passive-income`.

## 2026-05-11 — Stale job posting surfaced as apply
- **Failure:** Told JT the one `apply` role was Ridgeline AI Enablement Lead even though the visible BuiltIn UI showed the role had been removed on 2026-04-14.
- **Root cause:** I trusted the local opportunity log and cached/HTTP-200 aggregator JD text instead of verifying current live posting status/application availability before recommending action.
- **Guardrail/rule:** Before routing any job as `apply` or `both`, verify live UI/application availability and check for removed/closed/expired language. Cached JD text from BuiltIn/aggregators is market intel only if UI status conflicts.
- **Regression check:** Search `data/job-opportunities.md` for `Route: apply` or `Route: both`; each must have active-posting verification or be downgraded before surfacing.
- **Owner surface updated:** `~/projects/job-market-agent/CLAUDE.md`, `knowledge/scoring-criteria.md`, `tasks/lessons.md`, `data/job-opportunities.md`, Mission Control task status.
- **Verification/date:** 2026-05-11 — Ridgeline set to `Status: expired | Route: market-intel`; MC apply task marked done.

## 2026-05-11 — Reddit daily generator repeated stale evergreen frames
- **Failure:** `reddit-daily-gen` sent stale Reddit content repeating the same crypto narrative/protocol-durability frame and fantasy roster-window/calculator frame that had already been delivered multiple times in prior days.
- **Root cause:** The anti-repeat rules existed in `memory/content/reddit-strategy.md`, but the active cron prompt still allowed broad fallback categories (“incentive alignment,” “protocol durability,” “roster construction,” “trade calculators as sentiment tools”) and did not hard-fail when outputs matched recent frames. The cron optimized for filling both slots instead of freshness.
- **Guardrail/rule:** Reddit cron now has a hard anti-repeat gate banning the repeated frames unless tied to a fresh named event/thread from the last 48 hours. It must output `SKIP_SLOT` instead of padding with evergreen theory.
- **Regression check:** Inspect the next 3 `reddit-daily-gen` runs. Fail if any crypto slot uses generic narrative/mechanism/protocol durability/stakeholder alignment framing without a fresh 48h signal, or if fantasy slot uses generic roster-window/value/liquidity/calculator advice without a concrete thread type.
- **Owner surface updated:** `reddit-daily-gen` cron payload (`bbe49024-458a-4496-9c7c-7a278615810f`), `memory/content/reddit/2026-05-11-replacement-growth-drop.md`, `memory/content/reddit-draft-log.jsonl`.
- **Verification/date:** 2026-05-11 — cron update returned persisted payload with hard anti-repeat gate and timeout 420; replacement drop skips crypto due stale source and uses Sports GM 2026-05-09 report for fantasy.

2026-05-11 | Crypto morning cron appeared delivered but JT did not receive/notice actual portfolio recommendation for two days. Root cause: cron generated correct files and cron run history marked `deliveryStatus=delivered`, but delivery relied on cron announce/fallback summary rather than an explicit Telegram send of `data/telegram-summary.txt`; heartbeat checks trusted delivery metadata instead of verifying user-facing payload. | Guardrail: critical crons that generate local output and need Telegram must explicitly send the intended summary via message tool after file generation, and final run summary must include `telegram_message_sent=true` plus exact summary text. | Regression check: 10AM heartbeat must inspect latest crypto run for explicit summary text/message send, not just `lastRunStatus`/`deliveryStatus`; if missing, resend `telegram-summary.txt` manually and patch cron. | Owner surface updated: cron `eve-crypto-morning-008` payload patched to read crypto-agent CLAUDE.md, generate files, read `telegram-summary.txt`, and explicitly send via Telegram; this mistakes log. | Verification: 2026-05-11 cron patch returned JSON with updated payload and delivery mode none; manual Telegram resend succeeded messageId 18371.

## 2026-05-12 — @dynastyjig content modeled topics instead of native post construction
- **Failure:** Reassured JT that the @dynastyjig Niche-Growth pack was optimal even though the drafts still sounded assistant-generated: polished aphorisms, repeated constructions like “the real question is” / “question worth asking,” and insufficient modeling of actual dynasty/betting sentence rhythm.
- **Root cause:** The pipeline extracted topics and broad hook mechanics from swipe/current examples but did not force a teardown of native sentence construction, nouns, rhythm, and tension before drafting. “Specific player/rank gap” became a proxy for niche-native voice, which is not enough.
- **Guardrail/rule:** Sports GM daily packs must create a `Native pattern teardown` before drafting: opening syntax, native nouns, sentence rhythm, tension type, and what not to copy. Drafts must map to a specific syntax/rhythm mechanic, not just a topic or player.
- **Regression check:** Sports GM autoresearch checklist now asks whether the pack includes native pattern teardown, avoids assistant-y phrases, and maps each draft to a fresh native syntax/rhythm mechanic. Any pack missing this fails review.
- **Owner surface updated:** `skills/sports-gm/SKILL.md`, `agents/autoresearch/checklists/sports-gm.md`, daily @dynastyjig cron prompt patched and verified.
- **Verification/date:** 2026-05-12 — live X samples showed native patterns around final roster spots, post-rookie-draft timing, productive vets, 1.08/WR2 decisions, cards/units/round robins/last legs; prior pack did not model those patterns tightly enough.

## 2026-05-12 — Dynasty reply cron still allowed stale cached targets
- **Failure:** `dynasty-replies-gen` produced reply suggestions from cached/stale tweets after X API credits/search were blocked, despite the Sports GM skill requiring fresh reply targets.
- **Root cause:** The skill had the right fail-closed rule, but the active cron prompt still used `--since 7d` examples and did not include a hard `BLOCKED` output contract. The generator optimized for filling the reply pack rather than preserving engagement freshness.
- **Guardrail/rule:** Reply targets are different from standalone posts: every final target must be ≤24h old, preferably ≤12h. Cached viable pools, prior-day pools, saved links, and older high-quality posts are banned. If fresh search is unavailable, output exactly `BLOCKED: fresh X reply targets unavailable — [reason]` and stop.
- **Regression check:** Active cron prompt now includes `FRESHNESS HARD STOP`, `Freshness: all targets ≤24h old`, `Cached pool used: no`, and `BLOCKED: fresh X reply targets unavailable`; Sports GM autoresearch checklist now checks cached-pool failure.
- **Owner surface updated:** `dynasty-replies-gen` cron (`8b968751-6e59-42e5-b2ce-09f57d36176c`), `skills/sports-gm/SKILL.md`, `agents/autoresearch/checklists/sports-gm.md`, this mistakes log.
- **Verification/date:** 2026-05-12 — cron show verified hard-stop markers present, `--since 1d` present, timeout increased to 360s.

## 2026-05-12 — Dynasty reply search query allowed non-fantasy noise
- **Failure:** Fresh X search worked, but the first validation query used broad terms like `trade value`, pulling real estate, DeFi, stocks, and generic sports noise instead of dynasty fantasy reply targets.
- **Root cause:** The cron had freshness rules but not query-hygiene rules. It assumed `dynasty fantasy OR trade value` would constrain results, but X search interpreted `trade value` broadly.
- **Guardrail/rule:** Dynasty reply searches must include fantasy-football qualifiers and exclude obvious non-fantasy noise (`-crypto -defi -stock -real estate -multifamily`). If a search returns mostly non-fantasy results, discard it and rerun narrower before output.
- **Regression check:** Sports GM autoresearch checklist now checks query hygiene and noisy result discard before Dynasty X Replies are accepted.
- **Owner surface updated:** `dynasty-replies-gen` cron prompt, `skills/sports-gm/SKILL.md`, `agents/autoresearch/checklists/sports-gm.md`, this mistakes log.
- **Verification/date:** 2026-05-12 — narrowed approved-account and fantasy-specific searches returned fresh usable targets from DynastyDadFF, EthanKreagerFF, JoeOrrico, and DLFootball.

## 2026-05-13 — LinkedIn content foregrounded credibility repair instead of buyer authority
- **Failure:** Suggested a Wednesday LinkedIn post about reducing an overstated 10-hour claim to 4 hours every 2 weeks, making the public story about JT correcting a weak claim instead of demonstrating buyer-facing implementation value.
- **Root cause:** Content quality gates checked honesty, specificity, and style but did not include a strategic-fit test for whether the post increases buyer/hiring-manager confidence. The advisory board accepted “trust in proof” as a theme without penalizing self-undermining framing.
- **Guardrail/rule:** Wednesday LinkedIn and all LinkedIn delivery must block drafts that foreground a mistake, inflated claim, correction, apology, weak metric, or credibility repair unless JT explicitly requests a postmortem; accurate numbers stay, but the story must lead with buyer pain, proof, and implementation authority.
- **Regression check:** Before any Wednesday LinkedIn approval or content-reminder send, scan for correction/self-undermining terms (mistake, inflated, corrected, apology, overclaimed, weak claim, changed the metric, 10 hours) and require an explicit buyer-authority justification or regenerate.
- **Owner surface updated:** skills/wednesday-linkedin/SKILL.md, memory/content-voice.md audit checklist, content-reminder cron, content-generate-linkedin cron, memory/content/weekly-2026-05-11.md, memory/content/bank/2026-05-13/wednesday-linkedin.md.
- **Verification/date:** 2026-05-13 — bad post replaced with buyer-facing StreetEasy scraper case study; guardrail added to skill/checklist/crons; grep confirmed bad phrase locations were addressed in active content files.

## 2026-05-13 — Dynasty reply generator repeated stale/generic targets while claiming optimality
- **Failure:** Dynasty X Replies Crown repeated the same target/reply set from yesterday and delivered generic replies, while I had previously certified the output as optimal.
- **Root cause:** The freshness gate checked tweet age but not durable target/reply dedupe. The isolated cron did not have reliable access to yesterday's delivered pack, and query hygiene allowed loose terms like SF/TEP that can pull non-fantasy garbage. Quality gates accepted replies that could fit many tweets.
- **Guardrail/rule:** Dynasty reply generation must read/write `memory/sports-gm/dynasty-replies-ledger.jsonl`, reject URLs/status IDs used in the last 14 days, reject same accounts for 48 hours unless justified, ban loose SF/TEP-only query terms, and block generic reply shapes unless tied to a specific original-tweet angle.
- **Regression check:** Before any Dynasty X Replies delivery, verify final output includes `Ledger check: passed`; grep the ledger for each selected status ID; verify each query includes unmistakable fantasy-football qualifiers and excludes real estate/finance noise; reject replies that could fit 20 different tweets.
- **Owner surface updated:** `skills/sports-gm/SKILL.md`, `dynasty-replies-gen` cron payload, `memory/sports-gm/dynasty-replies-ledger.jsonl`.
- **Verification/date:** 2026-05-13 — bad targets and replacement targets appended to ledger; cron contains HARD ANTI-REPEAT LEDGER, REPLY QUALITY GATE, and loose SF/TEP ban.

## 2026-05-14 — Crypto allocation skipped mandatory X research
- **Failure:** The 2026-05-14 Crypto Morning full-analysis delivered allocation recommendations even though fresh X research was skipped; `data/cost-log.md` said “X searches: skipped in this pass to preserve cost,” while the latest X evidence file was stale from May 5.
- **Root cause:** X research existed as a prompt instruction but not as an executable preflight gate. The cron allowed the agent to trade off real-time social/coordination evidence for cost control, so allocation could still be delivered without the signal most relevant to microcap narrative rotation.
- **Guardrail/rule:** Full-analysis allocation must run `scripts/run-x-research.py --since 1d --limit 5`, then `scripts/x-research-guard.py --max-age-hours 3`, before scoring or sending. Cost discipline can reduce depth, not eliminate X. If X fails/stales/misses coverage, send a blocker instead of allocation.
- **Regression check:** Before Crypto Morning delivery, `x-research-guard.py` must pass with fresh `data/x-research-latest.json` coverage for every Google Sheet coin plus `__NARRATIVE__`; cron final response must include `x_research_guard_passed` and `x_research_entries`.
- **Owner surface updated:** `/Users/jtsomwaru/projects/crypto-agent/CLAUDE.md`, `config/settings.yaml`, `scripts/run-x-research.py`, `scripts/x-research-guard.py`, and cron `eve-crypto-morning-008` payload/timeout.
- **Verification/date:** 2026-05-14 — full X pass attempted 20 searches, succeeded 20, `x-research-guard.py` returned `OK: fresh X research verified — entries=20, age_hours=0.00, portfolio_covered=20/20`; cron timeout increased to 1200s and payload now hard-blocks allocation if X guard fails.

## 2026-05-14 — Repeated LinkedIn Agentforce boundary post recommended
- **Failure:** Content reminder recommended a LinkedIn Agentforce boundary/escalation post that JT had already posted roughly a month earlier; the same angle had also been recycled across March/April/May weekly files.
- **Root cause:** The content guard checked formatting, placeholders, Notion script hygiene, and same-slot duplicates, but it did not enforce semantic topic cooldown against recent content themes. The posted log also had many manually posted rows still marked `posted=false`, so relying only on posted status hid repeat risk.
- **Guardrail/rule:** Content delivery must block semantic topic clusters, not just exact text. Agentforce boundary/escalation is now a cooldown cluster; content guard scans current/future weekly sections against recent LinkedIn log rows regardless of posted flag.
- **Regression check:** `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-05-11.md --check-notion-script` fails on the repeated Agentforce boundary section, then passes after replacement. Future repeats in active/future sections should fail with `topic cooldown breach`.
- **Owner surface updated:** `scripts/content_distribution_guard.py`, `memory/content/weekly-2026-05-11.md`, `memory/content/posted-log.jsonl`, Mistakes Log, regression checks.
- **Verification/date:** 2026-05-14 — guard failed on `agentforce-boundary-escalation`, Thursday slot replaced with fresh content-system failure post, guard passed, and `scripts/content_calendar_audit.py --week 2026-05-11` passed.

## 2026-05-14 — Morning Brief truncated Nash X/Reddit drafts
- **Failure:** Morning Brief delivered only a save path plus short teaser for Nash X + Reddit instead of full post drafts, forcing JT to ask for the actual copy.
- **Root cause:** HEARTBEAT and the morning-brief cron required generating/saving Nash X+Reddit, but did not explicitly require full inline delivery. The agent optimized for briefness and summarized the drafts.
- **Guardrail/rule:** Morning Brief must include full Daily X Post and full Daily Reddit Draft inline whenever Nash content is generated; preserve full drafts before lower-priority news/detail if Telegram length is a concern.
- **Regression check:** Morning Brief cron payload must contain `NASH DELIVERY CONTRACT`; HEARTBEAT Morning Brief section must say full X + full Reddit draft inline, not path/teaser only.
- **Owner surface updated:** `HEARTBEAT.md`, cron `eve-morning-brief-001`, Mistakes Log.
- **Verification/date:** 2026-05-14 — patched HEARTBEAT + cron payload; cron update output shows NASH DELIVERY CONTRACT and full draft requirements.

## 2026-05-14 — Site Work buckets hid expected Altmark/Adversight proof
- **Failure:** After deploying the jtsomwaru.com positioning update, JT asked why Altmark work was not visible under Client Outcomes and why Adversight AI disappeared from Apps.
- **Root cause:** I followed the safety brief too literally and optimized proof-tier hygiene without preserving JT's expected portfolio inventory. Altmark work was anonymized as generic construction/real-estate client cards without making the mapping obvious, while Adversight was removed from the first visible Apps list because I treated “avoid first visible Apps view” as a removal instruction instead of asking/flagging the tradeoff.
- **Guardrail/rule:** Portfolio updates must preserve all already-live proof assets unless explicitly approved for removal. If a client name is unsafe publicly, keep the work visible with an anonymized label and map it internally for JT review. Product/app removals require explicit JT approval.
- **Regression check:** Before any future portfolio deploy, run a pre-deploy inventory diff: previous visible Work/App cards vs proposed visible cards, with every removed/renamed item labeled `approved`, `anonymized`, or `blocked`.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; regression check to be added to portfolio-card/site-update workflow before next deploy.
- **Verification/date:** Logged immediately on 2026-05-14 after JT flagged the issue.

## 2026-05-14 — Misattributed Aya work as Altmark during site QA
- **Failure:** I told JT the Construction Progress Tracker and Property Intelligence Scraper were Altmark work. They were Aya work: Aya is the client behind the Lady D hotel dashboard and StreetEasy scraper.
- **Root cause:** I inferred client ownership from generic anonymized card labels instead of checking the authoritative client status/proposal files before answering. I also failed the inventory-diff guardrail immediately after adding it.
- **Guardrail/rule:** For public proof/client-work claims, verify client ownership against `MEMORY.md`, `memory/clients/*/status.md`, proposal extracts, or project source data before answering or editing. Never infer client attribution from generic card labels.
- **Regression check:** Before any portfolio deploy or client-work answer, run a client attribution check for each client outcome: slug → client → source file → allowed public label. Any uncertain mapping is `blocked` until verified.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; `docs/agents/regression-checks.md` updated with portfolio inventory diff and client attribution check.
- **Verification/date:** Logged 2026-05-14 after JT corrected the attribution.

## 2026-05-14 — Public site exposed client names and exact Altmark proposal amounts
- **Failure:** I deployed site copy that publicly named real clients (Aya/Altmark) and displayed exact Altmark proposal amounts after JT had repeatedly set a client-name/privacy boundary.
- **Root cause:** I optimized for proof specificity without re-running the public-proof privacy gate. I treated proposal facts as usable proof instead of separating internal deal context from externally safe copy.
- **Guardrail/rule:** Public site, LinkedIn, outreach, and portfolio copy must default to anonymized client descriptors unless JT explicitly approves naming. Proposal/deal amounts stay internal unless JT explicitly approves publishing them.
- **Regression check:** Before deploy, grep public source for real client names and exact proposal amounts; fail the deploy if any appear in public copy without an approval note.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; `docs/agents/regression-checks.md` gets public proof privacy grep check.
- **Verification/date:** Logged 2026-05-14 before privacy redeploy.

## 2026-05-17 — Missed cron cancellation instruction
- **Failure:** JT said “Let’s cancel this cron for now going forward” in reply to the heartbeat cron, but I treated it as an active-conversation heartbeat and replied `HEARTBEAT_OK` instead of disabling the cron.
- **Root cause:** The active-conversation heartbeat shortcut overrode an explicit operational command because I did not inspect reply context before applying the heartbeat stop rule.
- **Guardrail/rule:** If a message contains an explicit command like cancel/disable/stop/pause/resume/update a cron, execute that command even if it arrives in heartbeat context; heartbeat shortcut applies only to actual heartbeat polls or no-op checks.
- **Regression check:** On any heartbeat-adjacent user message, check for operational verbs (`cancel`, `disable`, `stop`, `pause`, `resume`, `update`, `remove`) before returning `HEARTBEAT_OK`.
- **Owner surface updated:** Mistakes log + MEMORY.md cron status + daily note.
- **Verification/date:** 2026-05-17 — cron `eve-heartbeat-2h-002` updated to `enabled=false`; tool result confirmed disabled.

## 2026-06-01 — LinkedIn queue shipped generic repeats and exposed internal content ops
- **Failure:** The 2026-06-01 LinkedIn queue reached JT with a generic Monday "best first AI project / least glamorous" opener he had already posted, a Wednesday post repeating last week's "gets risky / lives in multiple places" structure, a Friday post overusing "exception layer," and a Sunday post about internal content automation that should not be public.
- **Root cause:** The generator optimized for guard compliance and schedule completion instead of strategic novelty. The deterministic guard checked banned copy patterns and reference mechanics, but did not block semantic repeats, overused JT phrases, or content that reveals internal publishing machinery.
- **Guardrail/rule:** LinkedIn weekly generation must pass a 45-day semantic originality check and a strategic-fit check before delivery. Current hard blockers: "best first AI project / least glamorous," "gets risky when...live in different places," "exception layer," and public discussion of JT's content-generation/publishing machinery unless JT explicitly asks for it.
- **Regression check:** `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-2026-06-01.md --require-reference-map linkedin --require-reference-map x --check-notion-script` must fail drafts containing those patterns and pass the revised queue. Future weekly LinkedIn queues must also compare against `memory/content/posted-log.jsonl` before delivery.
- **Owner surface updated:** `scripts/content_distribution_guard.py`, `memory/content-voice.md`, `docs/agents/content-rules.md`, `skills/content-generation/SKILL.md`, `memory/content/weekly-2026-06-01.md`, `memory/content/posted-log.jsonl`, `memory/FEEDBACK-LOG.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-01 — revised queue passed `content_distribution_guard.py`, `content_calendar_audit.py --week 2026-06-01`, and `py_compile`; Drive doc and 4 Notion LinkedIn slots were updated.

## 2026-05-21 — Not-Y-X reveal pattern escaped content guard
- **Failure:** A LinkedIn content reminder delivered “A methodology page is not just documentation. It is trust infrastructure.” after JT had explicitly banned the “Not Y, X” / contrast-reveal pattern.
- **Root cause:** The prior fix banned only narrow “not X, it is Y / not X but Y” variants and scoped the rule mostly to client-proof posts. The deterministic guard did not include the semantically identical two-sentence “X is not just Y. It is Z.” construction, so the content system could pass a stale AI-copy pattern while technically satisfying the old regex.
- **Guardrail/rule:** The ban is now global across JT content and includes “not X, it’s Y,” “not X but Y,” and “X is not just Y. It is Z.” variants. Drafts must state the positive claim directly instead of using contrast-reveal framing.
- **Regression check:** `python3 scripts/content_distribution_guard.py --linkedin-draft [draft-file]` must fail any LinkedIn draft containing the two-sentence “X is not just Y. It is Z.” variant before delivery.
- **Owner surface updated:** `scripts/content_distribution_guard.py`, `memory/content-voice.md`, `docs/agents/content-rules.md`, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-05-21 — verified with `/tmp/bad_linkedin_not_just.md`; guard returned `CONTENT_DISTRIBUTION_GUARD_FAIL` for `banned Not-Y-X variant: 'X is not just Y. It is Z.'`.

## 2026-05-24 — Passive-income strategist cron silently missed report + Telegram delivery
- **Failure:** The Sunday 3PM passive-income strategist cron showed `status=ok`, but JT did not receive the digest, `deliveryStatus=not-delivered`, and `memory/passive-income/2026-05-24-strategist.md` was never created.
- **Root cause:** The cron treated the isolated LLM turn completing as success while relying on the same LLM turn to create the artifact and send Telegram. No deterministic post-run check enforced the required report file or message-tool delivery marker, so scheduler success could mask missing output.
- **Guardrail/rule:** User-facing crons with required artifacts must have a deterministic post-run verifier independent of the LLM final answer. For passive-income strategist, cron fallback delivery is not sufficient; report creation plus explicit Telegram delivery marker must be verified.
- **Regression check:** Sundays after 3PM, `scripts/passive_income_strategist_delivery_guard.py --send` must return `ok: true`; if report is missing or delivery is unconfirmed, it must resend the digest from the report or send a failure alert. The `passive-income-strategist-delivery-guard` cron runs Sundays 3:20PM ET.
- **Owner surface updated:** `scripts/passive_income_strategist_delivery_guard.py`, passive-income strategist cron delivery mode/payload, new `passive-income-strategist-delivery-guard` cron (`e7d45070`), `MEMORY.md`, daily note, and proof log.
- **Verification/date:** 2026-05-24 — recovered report exists at `memory/passive-income/2026-05-24-strategist.md` (26,524 bytes); guard returned `ok: true` with message-tool delivery marker and no problems; proof guard returned `ok: true`.

## 2026-05-27 — Misattributed OpenRouter spike and disabled wrong cron
- **Failure:** I attributed the OpenRouter spike to Glow Index without proving request-level usage, missed that Gemini 3 Flash Preview was the dominant billed model, and during the prior Spanish pause task disabled `05024e45`, which is Skills & API Researcher Weekly Synthesis, not Spanish Weekly Evaluation.
- **Root cause:** I trusted a plausible local-engine hypothesis and stale memory mapping instead of reconciling OpenRouter dashboard model attribution with trajectory-level model usage and live cron job names. The Gemini main-session fallback/tool-loop evidence was available in trajectory logs but not checked before the first answer.
- **Guardrail/rule:** Cost investigations must start from provider dashboard attribution, then reconcile to trajectory/session usage by model, hour, sessionKey, and cron ID before naming a root cause. Cron disable actions must verify live `openclaw cron show <id>` name before changing `enabled`. Main/default routing and enabled cron fallbacks must not include OpenRouter/Moonshot/Anthropic unless JT explicitly approves the exception and cost cap.
- **Regression check:** For any OpenRouter spike, run trajectory aggregation for OpenRouter model usage by hour and sessionKey, then compare against `memory/costs/openrouter-billing.jsonl` and dashboard model totals. For any cron pause/disable, capture `id`, `name`, `enabled`, and `schedule` from `openclaw cron show --json` before and after. After model-routing edits, run `jq empty` on config files and scan enabled cron payloads for non-OpenAI models/fallbacks.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`, `MEMORY.md`, `AGENTS.md`, daily note, `~/.openclaw/openclaw.json`, `~/.openclaw/cron/jobs.json`; restored `05024e45` to enabled.
- **Verification/date:** 2026-05-27 — trajectory aggregation identified `agent:main:telegram:direct:6608544825` on `openrouter/google/gemini-3-flash-preview` as the spike source; `openclaw cron show 05024e45...` confirms Skills & API Researcher Weekly Synthesis is enabled; `jq empty` passes for OpenClaw config/cron JSON and enabled cron scan returns no non-OpenAI models/fallbacks.

## 2026-05-27 — ReelFarm Intel overstated confidence and blurred A/B slots
- **Failure:** ReelFarm Intel recommendations labeled thin new-account TikTok signals as "High confidence," blurred Automation A lifestyle hooks with Automation B screenshot-demo hooks, used improper all-caps app casing, recommended trend-locked/interactive hooks that do not transfer to static slideshows, and underweighted cross-source convergence.
- **Root cause:** The analysis treated low-volume/throttled view counts as optimization data instead of noisy cold-start data, and the review checklist lacked deterministic gates for confidence labels, Automation B slotting, brand casing, trend-transferability, and declarative hook preference.
- **Guardrail/rule:** Until each account has 20+ posts with normal, non-throttled distribution, every ReelFarm recommendation is capped at `Medium - hypothesis` and must be framed as a test. Automation B is screenshot-demo only; if the hook does not promise product screenshots/walkthrough in following slides, assign it to Automation A. Use proper app casing and prefer declarative, slideshow-native hooks.
- **Regression check:** Before future ReelFarm recommendations, read `memory/reelfarm/calibration-2026-05-27.md` and verify: confidence cap, A/B slotting test, proper app casing, no trend-locked or viewer-interactive hook, declarative-over-question preference, and explicit cross-source convergence when present.
- **Owner surface updated:** `memory/reelfarm/calibration-2026-05-27.md`, `memory/reelfarm/reelfarm-review-checklist.md`, `memory/reelfarm/reelfarm-strategy-baseline.md`, `memory/app-marketing/optimization-rules.md`, `memory/app-marketing/current-status-2026-05-26.md`, `MEMORY.md`, and regression checks.
- **Verification/date:** 2026-05-27 — calibration file created, checklist/baseline/optimization rules patched, and `rg` verification confirms the new confidence cap and Automation B slotting test are present.

## 2026-05-27 — Active Telegram replies stalled behind maintenance work
- **Failure:** JT sent repeated "are you there?" messages and saw typing indicators, but I delayed the visible reply while running heartbeat/context-maintenance, file-budget checks, and tool chains.
- **Root cause:** I let injected heartbeat/background context and bootstrap pressure compete with an active human conversation, then violated the reply-first rule by doing multi-step tool work before sending a visible ack. LCM compaction/tool-result repair made the delay worse.
- **Guardrail/rule:** Active Telegram messages win over heartbeat/proactive work. For "are you there?", live status checks, or live ops/debug questions, send a visible ack before any tool calls; keep active-conversation work to <=4 tool calls between visible updates.
- **Regression check:** `docs/agents/regression-checks.md` now has an active check for Telegram stalls behind maintenance/tool chains; daily film review must flag any active Telegram turn with more than four tool calls and no visible reply.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`, `docs/agents/regression-checks.md`, and `TOOLS.md` bootstrap pressure was reduced so the hot tool file is not sitting at 99% budget.
- **Verification/date:** 2026-05-27 — sent immediate visible ack to JT, added regression check, trimmed `TOOLS.md`, and redacted stale secrets from tool docs.

## 2026-05-28 — LinkedIn weekly queue skipped posted-log tracking
- **Failure:** Thursday content reminder sent only X, and this week's LinkedIn slots were absent from `memory/content/posted-log.jsonl` even though the LinkedIn generator claimed the queue was ready and pushed Notion.
- **Root cause:** The `content-generate-linkedin` cron prompt required writing the weekly file, running the guard, Drive upload, and review packet, but did not explicitly require local `posted-log.jsonl` rows before success. The 8AM reminder and pending posted-reply state depend on `posted-log`, so Notion scheduling alone was not enough.
- **Guardrail/rule:** Weekly LinkedIn generation must append one `posted-log.jsonl` row per LinkedIn slot before announcing success. A ready queue without local tracking rows is a blocker, not success.
- **Regression check:** After every LinkedIn generator run, verify `posted-log.jsonl` contains `platform=linkedin` rows whose `source_weekly` matches the current weekly file. Friday 2026-05-29 pending-state dry run must return both X and LinkedIn entries.
- **Owner surface updated:** `content-generate-linkedin` cron payload, `memory/content/posted-log.jsonl`, Mistakes Log.
- **Verification/date:** 2026-05-28 — added 4 missing LinkedIn rows for week of 2026-05-25; `content_pending_reply_state.py --date 2026-05-29 --platform linkedin --platform x --dry-run --json` returns 2 entries; content guard passes.

## 2026-05-31 — Content audit said healthy while reference-map guard failed
- **Failure:** I told JT the content pipeline was hardened, but the current weekly file still failed the new platform-specific reference-map guards for both LinkedIn and X while `scripts/content_calendar_audit.py --week 2026-05-25` still returned PASS.
- **Root cause:** I added the stricter `--require-reference-map` validation to the guard and cron prompts, but did not wire that stricter validation into the existing weekly audit script. The system could therefore report overall content health from older generic checks while missing the exact failure JT asked me to prevent.
- **Guardrail/rule:** A weekly content audit is not healthy unless it verifies both `## LinkedIn Reference Mechanics` and `## X Reference Mechanics` with source URLs, platform, niche, format, hook mechanic, and JT translation, or an explicit gap label.
- **Regression check:** `python3 scripts/content_calendar_audit.py --week 2026-05-25` must now fail on the current stale weekly file because the reference mechanics sections are missing; future generated weekly files must pass this audit before being called healthy.
- **Owner surface updated:** `scripts/content_calendar_audit.py`, `docs/agents/regression-checks.md`, `docs/agents/mistakes-log-recent.md`, daily note, and `MEMORY.md`.
- **Verification/date:** 2026-05-31 — audit script patched to call `content_distribution_guard.py` with both `--require-reference-map linkedin` and `--require-reference-map x`; `python3 scripts/content_calendar_audit.py --week 2026-05-25` now fails on missing LinkedIn/X reference mechanics instead of incorrectly passing.

## 2026-05-31 — Content niche map was too narrow and product/tool-biased
- **Failure:** I referenced current niches as if Claude Code, Vista, Glow Index, and App Marketing were acceptable default lanes for JT's broader content system, even though those are tools/product lanes and not JT's optimal current niches.
- **Root cause:** I treated "current projects" as the content taxonomy instead of deriving the hierarchy from JT's North Star, active consulting proof, buyer ICPs, job-market leverage, and passive-income priorities. The system had scattered niche labels but no canonical source of truth with priority order.
- **Guardrail/rule:** Content systems must load `memory/content/current-niche-map.md` before selecting a niche. Default LinkedIn content must bias toward consulting/proof and authority/career lanes; product/app lanes are secondary unless explicitly requested. Saved swipe/reference mechanics must use exact canonical lane names, not old shorthand aliases.
- **Regression check:** Before any content-generation prompt, swipe backfill task, or LinkedIn corpus task is called optimized, verify it references `memory/content/current-niche-map.md` and does not treat Claude Code, Vista, Glow Index, Nash Satoshi, App Marketing, AI Consulting, NYC SMB, or Personal Brand as the default/saved niche universe. `content_distribution_guard.py --require-reference-map linkedin --require-reference-map x` must fail non-canonical `Niche:` values.
- **Owner surface updated:** `memory/content/current-niche-map.md`, `docs/agents/content-rules.md`, `memory/content-voice.md`, `agents/content-calendar/AGENT.md`, `skills/content-generation/SKILL.md`, `scripts/notion-swipe-push.py`, Mission Control content tasks, `MEMORY.md`, daily note, weekly recap, and this Mistakes Log entry.
- **Verification/date:** 2026-05-31 — created canonical niche map, patched content rules/agents/skill/swipe taxonomy, updated relevant Mission Control task descriptions, added exact-niche enforcement to `content_distribution_guard.py`, and verified Python compilation plus task-board state.

## 2026-05-31 — Reused invalid proof-log type
- **Failure:** I tried to log a Mission Control task correction with `scripts/log-proof.py --type task_update`, which is not a valid proof type.
- **Root cause:** I relied on a semantic label that sounded right instead of checking the script's accepted enum before calling it. This repeated the same class of invalid proof-type error from earlier in the day.
- **Guardrail/rule:** Before using `scripts/log-proof.py` with a non-obvious type, run `python3 scripts/log-proof.py --help` or use a known accepted generic type: `file_edit`, `script_execution`, `api_call`, or `other`.
- **Regression check:** Any failed `log-proof.py` invocation must be retried with a valid enum and the proof guard must pass before closeout.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; proof logging was retried with `--type other`.
- **Verification/date:** 2026-05-31 — invalid `task_update` call failed, then `python3 scripts/log-proof.py --type other --title "Passive Income Mission Control ClaimRisk correction" ...` succeeded with proof id `[df5cd6ef]`.

## 2026-05-31 — `openclaw doctor --fix` applied an unprompted route repair
- **Failure:** JT instructed me to run `openclaw doctor --fix` and accept only orphan transcript cleanup. I approved the orphan transcript prompt, but the command also auto-repaired one legacy Codex session route without a separate prompt before I could stop it.
- **Root cause:** I assumed `doctor --fix` would prompt for each fixable category because orphan cleanup prompted, instead of treating the command as a batch fixer that may apply additional noninteractive repairs after the accepted prompt.
- **Guardrail/rule:** When JT authorizes only one doctor fix category, do not run broad `openclaw doctor --fix` unless the CLI exposes a category-specific flag or dry-run plan proving it will not apply other fixes. If no scoped flag exists, stop after `openclaw doctor`, report the proposed fixes, and ask JT before running broad `--fix`.
- **Regression check:** Before future doctor repairs, run `openclaw doctor --help` / `openclaw doctor --fix --help` and verify whether a scoped fix flag exists; if not, do not execute broad `--fix` for a single-category approval.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; user-facing report explicitly disclosed the unprompted route repair.
- **Verification/date:** 2026-05-31 — follow-up `openclaw doctor` no longer shows the orphan transcript state-integrity warning; it still shows the duplicate lossless-claw warning, command-owner warning, cron model override warning, plaintext secret warning, and memory-search warning.

## 2026-06-01 — Mission Control task payload used uppercase assignee
- **Failure:** During the monthly niche fitness review, the required `mission_control_task_gate.py --create-file` call returned HTTP 500 when the task payload used `"assignee": "JT"`.
- **Root cause:** The local task templates in `TOOLS.md` and `docs/agents/task-board-rules.md` documented the assignee value as `JT`, but Mission Control's Convex schema only accepts lowercase enum values: `jt`, `eve`, or `both`. I trusted the stale template instead of checking the schema before creating the payload.
- **Guardrail/rule:** Mission Control task payloads must use lowercase `assignee` enum values (`jt`, `eve`, `both`). If the gate returns HTTP 500 on create, check payload schema before treating Mission Control as down.
- **Regression check:** Before creating a task from a JSON file, verify required fields and enum casing against `mission-control/convex/tasks.ts` when the payload is new or generated by a cron. A duplicate check plus successful `mission_control_task_gate.py --create-file ... --json` is the closeout proof.
- **Owner surface updated:** `TOOLS.md`, `docs/agents/task-board-rules.md`, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-01 — changed `/tmp/niche-fitness-task.json` to `"assignee": "jt"` and reran the gate successfully; created task `j572qymhhp6enefn648cjb40cx87tc0y`.

## 2026-06-01 — Revised LinkedIn queue buried AI Ops Teardown slot
- **Failure:** The revised 2026-06-01 LinkedIn queue claimed to be corrected, but the visible Drive review doc did not clearly include an AI Ops Teardown post; Wednesday became a StreetEasy case study and the teardown series only appeared indirectly in source/checklist language.
- **Root cause:** I optimized for replacing weak/generic angles and preserving current proof, but failed to enforce the queue-level content mix requirement that AI Ops Teardown remain visible as a named slot. The guard checked stale phrasing and reference mechanics, not whether the promised series label survived into the review doc.
- **Guardrail/rule:** Weekly LinkedIn queue revisions that involve named recurring series must preserve at least one clearly labeled slot for each promised series, or explicitly say the series was skipped and why. "Teardown-shaped" copy is not enough if the review doc hides the series label.
- **Regression check:** Before syncing a revised weekly LinkedIn doc, scan the LinkedIn sections for expected recurring-series labels from the prior plan and content bank, especially `AI Ops Teardown`; if missing, fail the closeout before Drive/Notion/MC updates.
- **Owner surface updated:** `memory/content/weekly-2026-06-01.md`, `memory/content/posted-log.jsonl`, Notion Content Calendar rows for 2026-06-01/03/05/07, Mission Control review task, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-01 — restored Wednesday as `AI Ops Teardown`, updated tracking rows, uploaded revised v3 Drive doc, updated all four Notion LinkedIn slots to v3, updated Mission Control, and reran `content_distribution_guard.py` plus `content_calendar_audit.py` successfully.

## 2026-06-01 — AI Ops Teardowns drifted into generic evergreen advice
- **Failure:** The AI Ops Teardown slot used a generic lease-renewal workflow hook and repeated the same approval/queue pattern instead of examining a trending company or current problem and designing the optimal AI workflow for that company/problem.
- **Root cause:** The AI Ops Teardown operating system allowed "buyer-relevant category workflow" to count as enough, so the generator optimized for proof-safe evergreen content instead of current-signal uniqueness, public relevance, and organic attention. The template also leaned on stale "not chatbot / workflow first / exception layer" structure.
- **Guardrail/rule:** AI Ops Teardowns must start from a current company, funding/product/market signal, regulation, or visible buyer problem in a JT-relevant niche, then show the workflow JT would build: inputs, system checks, exception routing, approval boundary, output, audit trail, and buyer outcome. Generic evergreen workflow advice is a failed teardown.
- **Regression check:** Before any AI Ops Teardown is added to a weekly queue or uploaded to Drive, verify the bundle has a source dated within 30 days or an explicit evergreen label, a named company/problem signal, a distinct angle from the last 45 days, and a concrete workflow map. If missing, write `SKIP_SLOT` or replace the topic.
- **Owner surface updated:** `memory/consulting/ai-ops-teardowns/system.md`, `memory/consulting/ai-ops-teardowns/templates.md`, `docs/agents/content-rules.md`, `skills/content-generation/SKILL.md`, `memory/content-voice.md`, `memory/FEEDBACK-LOG.md`, `MEMORY.md`, weekly queue/source files, and this Mistakes Log entry.
- **Verification/date:** 2026-06-01 — replaced the Wednesday teardown with a Canals $35M wholesale order-intake desk based on a 2026-05-29 source; created teardown and content-bank files; uploaded both to Drive; updated delivery calendar, weekly queue, posted-log, Notion, and Mission Control; reran content guard and calendar audit successfully.

## 2026-06-01 — Outreach update closed the wrong plumbing prospect task
- **Failure:** While logging JT's Petri Plumbing M1 send, `scripts/outreach_update.py` also closed the unrelated New York Plumbing Supply review task because both titles contained "Plumbing."
- **Root cause:** The Mission Control closeout helper matched any one company token from the supplied company name instead of requiring an exact slug match, exact company phrase, or all meaningful company tokens. Shared industry words like "Plumbing" were treated as sufficient identity.
- **Guardrail/rule:** Outreach task closeout must require exact slug identity when a slug exists, or a strict company match across the title/description. A single shared industry/category token can never close a Mission Control outreach task.
- **Regression check:** After running `scripts/outreach_update.py`, verify the active task board contains only the intended follow-up tasks, the original review/send task is closed, and adjacent same-category prospects remain in their prior state.
- **Owner surface updated:** `scripts/outreach_update.py`, `docs/agents/mistakes-log-recent.md`, `memory/2026-06-01.md`, and Mission Control task state.
- **Verification/date:** 2026-06-01 — restored New York Plumbing Supply to `todo`, archived stale duplicate HPM/Superior/Petri tasks, promoted the fresh Petri/HPM/Superior M2 tasks to high priority, and `python3 -m py_compile scripts/outreach_update.py` passed.

## 2026-06-01 — Reused invalid proof-log type again
- **Failure:** While closing the Vista private movie rating page, I first ran `scripts/log-proof.py --type build`, which failed because `build` is not an accepted proof type.
- **Root cause:** I treated a previous invalid-proof-type mistake as a one-off memory instead of adding a reliable pre-call habit. Under closeout pressure, I picked the semantic label again instead of using the known accepted deployment/file_edit/other enum.
- **Guardrail/rule:** For shipped website/app pages, use `scripts/log-proof.py --type deployment`. Do not invent proof types. If unsure, run `python3 scripts/log-proof.py --help` before the proof call.
- **Regression check:** Before final closeout on any shipped page, scan the proof command for `--type build`, `--type outreach`, `--type task_update`, or any non-enum value; if present, stop and replace with a valid enum before running.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; proof log retried with a valid `deployment` type.
- **Verification/date:** 2026-06-01 — invalid `build` call failed, then `python3 scripts/log-proof.py --type deployment --title "Vista Private Movie Rating Landing Page" ...` succeeded with proof id `[999733f7]`.

## 2026-06-01 — Vista SEO verifier allowed an incomplete cluster
- **Failure:** The `/rate-movies-out-of-100` build was initially reported complete even though the live page did not link to `/private-movie-rating-app`, `/1-100-movie-rating-app` did not reciprocally link back, and the new page exceeded the 250-line governance cap.
- **Root cause:** The page-specific verifier only required `/1-100-movie-rating-app` and `/movie-taste-profile-app` on the new page, accepted “at least two” inbound Vista links instead of requiring all existing cluster pages, and did not check the line-count governance cap. The subagent's local/production checks therefore validated a partial cluster.
- **Guardrail/rule:** New Vista SEO page verifiers must require the full intended cluster: outbound links from the new page to every relevant existing Vista SEO page, inbound links from every existing Vista SEO page named in the task, and the source-file line cap for the new page.
- **Regression check:** For future Vista SEO pages, run the page-specific verifier plus a production script that checks the new page, sitemap, llms.txt, and each reciprocal source page for the exact route. Missing one reciprocal page is a failure even if the page itself is live.
- **Owner surface updated:** `scripts/verify-vista-rate-movies-page.mjs`, `src/app/rate-movies-out-of-100/page.tsx`, `src/app/1-100-movie-rating-app/page.tsx`, `docs/agents/regression-checks.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-01 — tightened `scripts/verify-vista-rate-movies-page.mjs` to require `/private-movie-rating-app`, enforce the 250-line cap on the new page, and require all three existing Vista SEO pages to link back; `node scripts/verify-vista-rate-movies-page.mjs`, `git diff --check`, `npm run lint`, `npm run build`, and production checks passed after commits `5111a61` and `a24616f`.

## 2026-06-11 — Auth profile inspection printed raw credential-looking values
- **Failure:** While verifying whether Moonshot fallback was actually configured, I read `auth-profiles.json` too broadly and the tool output included raw credential-looking token/API-key values in the internal session transcript.
- **Root cause:** I used a quick string preview of the auth profile object instead of a structured redacted projection of provider/profile names only.
- **Guardrail/rule:** When inspecting auth/profile files, never print raw object previews. Use a script that emits only profile IDs, providers, auth types, and boolean presence flags, with values omitted before output.
- **Regression check:** Future auth inspections must run a redacted projection command only; any command output containing `sk-`, `Bearer`, JWT-looking strings, or long token values is a security failure and must be reported immediately.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; no config or credential files changed.
- **Verification/date:** 2026-06-11 — stopped further raw auth inspection, did not quote the values to JT, and alerted JT in the active conversation.

## 2026-06-11 — Evening Digest surfaced low-value ReelFarm hypotheses
- **Failure:** Evening Digest sent a ReelFarm Daily Strategy Intel item with three routine test hypotheses and a file path, leaving JT asking what he was supposed to take away from it.
- **Root cause:** Phase 5 routed routine FYI output into the digest, but the ReelFarm prompt still treated "meaningful hypotheses" as enough for delivery instead of requiring a decision, same-day action, or verified critical finding.
- **Guardrail/rule:** Digest entries must answer "what should JT do with this?" Routine hypotheses, trend translations, and saved reports stay in files unless they create a concrete action, decision, or critical alert.
- **Regression check:** A ReelFarm report with only medium-confidence app-marketing hypotheses must say `Send Telegram: no`, must not append to `memory/digest-queue.md`, and Evening Digest should remain empty unless another actionable item exists.
- **Owner surface updated:** `agents/reelfarm-intel/daily-prompt.md`, ReelFarm cron delivery instruction, `docs/agents/mistakes-log-recent.md`, and `memory/2026-06-11.md`.
- **Verification/date:** 2026-06-11 — updated the prompt and cron instruction after inspecting `memory/reelfarm/reports/daily/2026-06-11.md`; report value was only optional future creative tests, not a JT action.

## 2026-06-11 — Temporary cron smoke used deleteAfterRun true
- **Failure:** During Follow-up E Sonnet preflight, I created a temporary cron smoke with the CLI default `deleteAfterRun: true`, even though cron safety rules forbid delete-after-run jobs.
- **Root cause:** I optimized for a minimal cron-runtime preflight and trusted the CLI one-shot default instead of explicitly passing `--keep-after-run` or using an existing durable smoke harness.
- **Guardrail/rule:** Any temporary cron smoke must be created with `--keep-after-run`, then explicitly removed after verification if cleanup is approved/appropriate; never rely on `deleteAfterRun`.
- **Regression check:** Future cron smoke commands must show `--keep-after-run` in the creation command or use a non-cron preflight API; `openclaw cron get [temp-id]` or run history must confirm cleanup state after the smoke.
- **Owner surface updated:** This Mistakes Log entry; Follow-up E audit notes the temp job auto-deleted after success.
- **Verification/date:** 2026-06-11 — `openclaw cron get 60c2a353-3df9-4aee-a63e-1770120fa1cb` returned job not found after success, confirming the temporary job was removed, but the creation pattern was still wrong.

## 2026-06-11 — Broad process listing exposed a runtime secret in tool output
- **Failure:** While verifying Phase 2A post-restart health, I ran a broad `ps aux` and the internal tool output included a command-line `instance-secret` value from a local Convex process.
- **Root cause:** I used a whole-system process listing for health evidence instead of a targeted OpenClaw-only process query with sensitive argument redaction.
- **Guardrail/rule:** For runtime health checks, never run broad process dumps. Query only the needed process names/PIDs and redact command-line arguments before output, or use `pgrep`/`ps -p` with minimal columns.
- **Regression check:** Before any process-inspection command, check that it cannot print full command arguments for unrelated services; if full args are needed, pass them through a redaction script before output.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; no credential files changed.
- **Verification/date:** 2026-06-11 — did not quote or forward the secret value to JT; future Phase 2B loopback/Convex checks must use targeted `lsof`/health URLs and redacted process output.

## 2026-06-11 — Targeted pgrep still exposed Convex secret arguments
- **Failure:** During Phase 2B investigation, I ran `pgrep -fl openclaw` after already logging a process-output secret slip; because Mission Control/Convex paths include `.openclaw`, the internal tool output included the Convex command line and its `instance-secret` value again.
- **Root cause:** I treated `pgrep -fl` as a targeted process check, but `-f` prints full command arguments and a broad `openclaw` match can include local services with secrets embedded in argv.
- **Guardrail/rule:** Never use `pgrep -fl` with broad workspace/path terms. For process checks, either query exact ports with `lsof -nP -iTCP:<port> -sTCP:LISTEN` or use `ps -axo pid,comm` without command arguments. If full command arguments are unavoidable, pipe through a tested redactor before output.
- **Regression check:** Phase 2B loopback verification must use `lsof` for ports 3000/3210/3211/5678 and only print command, PID, user, protocol, and listen address; no `pgrep -fl`, `ps aux`, or full argv output.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md` and `memory/2026-06-11.md`; no credential files changed.
- **Verification/date:** 2026-06-11 — did not quote or forward the exposed value to JT; subsequent plan text will describe only the service/argument name and not the value.

## 2026-06-11 — Model status redaction missed a partial API key
- **Failure:** During the 18:12 heartbeat cron-auth check, I ran `openclaw models status` with a weak text redactor and the internal tool output still included a partial static provider key preview.
- **Root cause:** I assumed keyword-based `sed` redaction would cover all model-status credential previews, but the CLI prints shortened key samples without a nearby `key` label in every field.
- **Guardrail/rule:** Do not print `openclaw models status` raw during heartbeat/auth checks. Use a structured redacted projection or a narrower runtime-auth probe that reports provider status only.
- **Regression check:** Any future model/auth status command must redact `sk-`/provider-key patterns before output, or use a script that emits only provider names, profile counts, and runtime usability booleans.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; no credential or config files changed.
## 2026-06-16 — AI Ops Teardown reused prior company context inside the post
- **Failure:** The AppFolio AI Ops Teardown draft mentioned Canals twice even though JT had only provided Canals as a prior-post exclusion signal.
- **Root cause:** I treated "I already posted about Canal" as continuity context for the public post instead of exclusion-only context. The content guard checked stale phrasing and voice but did not specifically block prior AI Ops Teardown company references.
- **Guardrail/rule:** Previous AI Ops Teardown companies are exclusion-only context and must never be mentioned in the new teardown post. Each teardown must stand alone on the current company/signal.
- **Regression check:** `python3 scripts/content_distribution_guard.py --linkedin-draft [new-ai-ops-teardown-file]` must fail when the draft mentions a company derived from earlier `memory/content/bank/*/ai-ops-teardown-*.md` files and pass only after those references are removed.
- **Owner surface updated:** `docs/agents/content-rules.md`, `scripts/content_distribution_guard.py`, `scripts/test_content_distribution_guard.py`, AppFolio local teardown files, and Drive teardown docs.
- **Verification/date:** 2026-06-16 — regression test first failed because `check_ai_ops_teardown_prior_company_references` did not exist, then passed after implementation; guard failed on the Canals references before local cleanup and passed after removal.

- **Verification/date:** 2026-06-11 — did not quote or forward the partial key preview to JT; subsequent heartbeat summary omits credential material.

## 2026-06-03 — Cron prompts let useful work fail after brittle checkpoints
- **Failure:** `Viral Post Swipe File — X Research` failed after producing the current reply-target artifact because the agent tried to read `memory/content/content-voice.md`, which does not exist; `prospect-discovery` failed after a large live-research run because it consumed about 144k tokens and stopped before final confirmation.
- **Root cause:** The cron prompts relied on natural-language file/tool operations and oversized open-ended research goals. They did not pin the canonical `content-voice.md` path with a deterministic preflight, and Prospect Discovery asked for 15-30 prospects in one turn without hard search/candidate limits or a mandatory final checkpoint.
- **Guardrail/rule:** Cron prompts that read canonical files must include the full path and an exact preflight command. Research crons must have hard search/candidate/time caps plus a final success line; "no qualified output" must be a valid success state when the filters are strict.
- **Regression check:** For Viral Swipe, `python3 scripts/social_engagement_audit.py --json --gate x` must pass for the newest reply-target file and the prompt must include `VIRAL_SWIPE_CRON_OK`. For Prospect Discovery, the prompt must include bounded 6-8 / 8-12 targets, a run report path, and `PROSPECT_DISCOVERY_CRON_OK`.
- **Owner surface updated:** OpenClaw cron payloads `33b8b0a2-e86c-4f51-aa4f-b8537def3107` and `ebb843af-e752-4c65-923d-540d5ff5ad3f`, `mission-control/app/consulting/page.tsx`, `docs/agents/mistakes-log-recent.md`, `memory/weekly-recaps/current-week.md`, and `memory/content/technical-angles.md`.
- **Verification/date:** 2026-06-03 — confirmed `memory/content-voice.md` reads with `sed -n '1,120p'`, Viral Swipe payload contains the path hardening and `VIRAL_SWIPE_CRON_OK`, Prospect Discovery payload contains capped targets plus `PROSPECT_DISCOVERY_CRON_OK`, `scripts/social_engagement_audit.py --json --gate x` returned ok=true, and `scripts/cron_volume_guard.py` returned ok=true.

## 2026-06-03 — Crypto full analysis relied on manual LLM artifact writing
- **Failure:** Crypto Full Analysis fetched fresh June 3 portfolio/prices/baseline/X/whale data, then stopped before writing `latest-analysis.md`, `telegram-summary.txt`, history, or allocation-history for the day, so Telegram delivery was correctly blocked.
- **Root cause:** The cron bundled deterministic data collection, broad analysis, artifact writing, validation, and Telegram send into one open-ended LLM turn. The validator existed, but dated artifact creation still depended on the agent manually completing a long prompt.
- **Guardrail/rule:** Cron jobs with required file contracts must use deterministic artifact writers for dated files and JSON state, then run validators. The LLM can gather/reason over inputs, but file-contract completion cannot depend on prompt memory.
- **Regression check:** For Crypto Full Analysis, run `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/generate-full-analysis.py`, `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/x-research-guard.py --max-age-hours 3`, and `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/validate-full-analysis.py --max-x-age-hours 3`; cron payload must include `CRYPTO_FULL_ANALYSIS_OK`.
- **Owner surface updated:** `scripts/generate-full-analysis.py`, `scripts/run-x-research.py`, crypto cron `eve-crypto-morning-008`, `CLAUDE.md`, `TOOLS.md`, `MEMORY.md`, weekly recap, technical angles, recent builds, and this Mistakes Log entry.
- **Verification/date:** 2026-06-03 — generated dated June 3 artifacts, X guard passed with 25 entries at 2.22 hours old, full-analysis validator returned `ok: true`, and cron show confirmed the payload calls `generate-full-analysis.py` plus requires `CRYPTO_FULL_ANALYSIS_OK`.

## 2026-06-03 — Guyana resume omitted strongest anonymized client deployment proof
- **Failure:** The first Guyana growth resume did not include the live insurance-expiration workflow or dedicated local office PC deployment, even though those are among JT's strongest current implementation proof points.
- **Root cause:** I over-weighted broad industry portability and client-name privacy, then failed to convert the client proof into anonymized property-operations language. I treated "do not mention the client by name" as a reason to omit the proof instead of sanitizing it.
- **Guardrail/rule:** Resume packages for broad-network forwarding must include the strongest accepted anonymized client proof before product/app proof, especially paid/live workflows, local deployment, human handoff, and staff adoption evidence. Privacy means redact the name, not remove the result.
- **Regression check:** Before uploading a broad opportunity resume, scan `MEMORY.md` Active Clients and `memory/content-voice.md` Proof Points for paid/live proof and confirm at least one anonymized client deployment bullet appears in Experience or Key Projects.
- **Owner surface updated:** `memory/drafts/guyana-growth-resume.md`, Drive resume document, Mission Control task `j57chv0qv97ecfdqjfd746fc7h87z6wx`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-03 — revised resume now includes the insurance-expiration workflow, dedicated office PC installation, and local operating handoff; parser check confirmed the proof text is present and the Drive resume was updated in place.

## 2026-06-03 — Crypto recovery fixed artifacts but not freshness ownership
- **Failure:** After the deterministic writer fix, manual Crypto Full Analysis recovery still failed because the 6AM X research aged past the 3-hour validator window before delivery. The system could produce today-dated artifacts while upstream X evidence was stale.
- **Root cause:** I moved artifact writing into `generate-full-analysis.py`, but left X freshness enforcement outside the writer and left the cron as a long agent-orchestrated checklist. The writer trusted `data/x-research-latest.json` instead of owning its preflight contract.
- **Guardrail/rule:** Any deterministic writer that consumes freshness-gated evidence must enforce that freshness before writing outputs. Cron recovery paths must use one atomic pipeline command for fetch -> X -> guard -> generate -> validate instead of relying on an agent to sequence many steps.
- **Regression check:** For Crypto Full Analysis recovery, stale X must make `python3 scripts/generate-full-analysis.py --max-x-age-hours 3` exit before touching `data/latest-analysis.md`; `python3 scripts/run-full-analysis-pipeline.py --max-x-age-hours 3 --since 1d --limit 5` must return `checkpoint: CRYPTO_FULL_ANALYSIS_OK` before any Telegram send.
- **Owner surface updated:** `scripts/generate-full-analysis.py`, `scripts/run-full-analysis-pipeline.py`, crypto cron `eve-crypto-morning-008`, crypto `CLAUDE.md`, `TOOLS.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-03 — stale-X negative test returned `X preflight failed` and preserved `latest-analysis.md` mtime; fresh pipeline refreshed X, passed guard at age 0.00h, passed validator for 24 coins/6 held positions/25 X entries, and returned `CRYPTO_FULL_ANALYSIS_OK`.

## 2026-06-07 — Passive-income scout failure became a false strategist alert
- **Failure:** The Sunday passive-income scout failed twice before writing a valid same-day scout report. The strategist initially wrote a BLOCKED report instead of evaluating stale output, and the delivery guard later alerted that the strategist had failed silently. JT then corrected the policy: the weekly passive-income report should not be blocked by stale or degraded inputs when a filesystem artifact can still be produced.
- **Root cause:** Saturday signal fetch could report green even when child sources failed or pre-scout freshness was not actually safe for Sunday. The Scout cron skipped the pre-scout gate and asked one LLM turn to read all historical passive-income reports and run broad research, burning 100K+ tokens before final confirmation. The first repair still treated stale hard inputs as invalid instead of separating evidence quality from artifact availability.
- **Guardrail/rule:** Passive-income inputs can be DEGRADED but should not be INVALID unless the required directory/filesystem is unreadable or no artifact can be written. Scout must run bounded and produce a compact complete report from available inputs; Strategist must evaluate complete/degraded scout packets and reserve BLOCKED for true artifact/filesystem failure. Delivery guard must distinguish degraded/block states from silent missing-output failure.
- **Regression check:** `python3 scripts/passive_income_handoff_check.py --date 2026-06-07 --mode pre-scout --json`, `--mode pre-strategist --json`, and `--mode post-strategist --json` must return `ok: true`; `rg -n "INCOMPLETE|BLOCKED|PASSIVE_INCOME_HANDOFF_FAIL" memory/passive-income/2026-06-07-scout.md memory/passive-income/2026-06-07-strategist.md` must return no matches after rerun.
- **Owner surface updated:** `scripts/fetch-signals.py`, `agents/passive-income-scout/AGENT.md`, passive-income-scout cron payload in `~/.openclaw/cron/jobs.json`, `agents/passive-income-strategist/AGENT.md`, `scripts/passive_income_handoff_check.py`, `scripts/passive_income_strategist_delivery_guard.py`, `memory/passive-income/2026-06-07-scout.md`, `memory/passive-income/2026-06-07-strategist.md`, `agents/passive-income-scout/state.json`, Mission Control, daily note, weekly recap, and this Mistakes Log entry.
- **Verification/date:** 2026-06-07 — refreshed `weekly-trends.md`; regenerated complete June 7 scout and strategist reports; created Mission Control task `j5724f5hfc07cr9a7skahz1121887dnm`; pre-scout, pre-strategist, and post-strategist handoff checks returned `ok: true`; no `INCOMPLETE`, `BLOCKED`, or `PASSIVE_INCOME_HANDOFF_FAIL` markers remained in the June 7 reports.
## 2026-06-11 — Phase 4 checklist drift after corpus-first content cron rebuild
- **Failure:** Phase 4 was reported complete even though the exact prompt-specific backup file `docs/audits/replaced-prompts-2026-06-11.md` had not been created, and the posted-reply edit-delta rule was placed directly in `AGENTS.md` while `AGENTS.md` was within 1,500 chars of its 28K budget buffer.
- **Root cause:** I verified the operational cron outcome and broad guard behavior, but did not run a literal requirement-by-requirement checklist against JT's Phase 4 prompt before claiming completion.
- **Guardrail/rule:** For plan-gated phases, create a checklist from the user's exact requested artifacts and verify each named path/routing condition before final reporting; "behavior works" is not enough when the prompt names artifacts.
- **Regression check:** Rerun a verifier that checks corpus gate counts, cron JSON parsing, both model fields, first 200 chars of both payload messages, replaced-prompt backup existence, edit-delta rule ownership, wrapper presence, preservation versus backup, and plan status.
- **Owner surface updated:** Added `docs/audits/replaced-prompts-2026-06-11.md`; moved the full posted-reply edit-delta rule to `docs/agents/content-rules.md`; reduced `AGENTS.md` to a pointer.
- **Verification/date:** 2026-06-11; follow-up verification rerun in the same turn after remediation.

## 2026-06-14 — Passive-income Scout failed on pseudo-command live search before writing handoff
- **Failure:** The `passive-income-scout` cron failed three times and left no `memory/passive-income/2026-06-14-scout.md`, so the 3 PM Strategist handoff would have failed even though Saturday signal files were fresh.
- **Root cause:** The Scout still allowed optional live-search work to run before the artifact was guaranteed. The cron diagnostics showed a malformed pseudo-command path, `run source -> run python3 ~/.openclaw/workspace/scripts/web_search.py (agent)`, and the prompt did not force failed optional search commands to degrade into local-file-only reporting.
- **Guardrail/rule:** Passive-income Scout must write the same-day handoff from local weekly signal files when any optional live search fails. Cron/agent prompts must use real executable shell commands with full paths and must explicitly ban pseudo tool chains such as `run source -> run python3 ... (agent)` and `search ... (agent)`.
- **Regression check:** On any passive-income Scout failure or prompt edit, run `python3 scripts/passive_income_handoff_check.py --mode pre-scout` and `python3 scripts/passive_income_handoff_check.py --mode pre-strategist`; both must return `PASSIVE_INCOME_HANDOFF_OK` for the current date. Confirm the Scout cron payload and `agents/passive-income-scout/AGENT.md` contain the critical-path and command-safety rules.
- **Owner surface updated:** `agents/passive-income-scout/AGENT.md`, `passive-income-scout` cron payload, `memory/passive-income/2026-06-14-scout.md`, `agents/passive-income-scout/state.json`, `docs/agents/regression-checks.md`, `memory/weekly-recaps/current-week.md`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-14 — recovered the same-day scout report, updated Scout state to `last_run: 2026-06-14`, verified the cron payload contains the command-safety rule, and both pre-scout plus pre-strategist handoff checks returned `PASSIVE_INCOME_HANDOFF_OK`.

## 2026-06-15 — Monday X/LinkedIn content delivery silently failed
- **Failure:** JT did not receive the expected Monday X/LinkedIn content packet. The LinkedIn weekly generator reported `ok` but only delivered the partial summary `Starting Step 0 reads in parallel`; the X weekly generator errored with `Agent couldn't generate a response`; no `memory/content/weekly-2026-06-15.md` or scheduled weekly posted-log rows were produced.
- **Root cause:** The Monday flow depends on long weekly generator crons instead of the lightweight `content-reminder`, which only runs Tuesday-Saturday. The generator success criteria allowed a partial run summary to count as delivered, and the X generator failure did not trigger an immediate recovery packet.
- **Guardrail/rule:** Monday content delivery is not healthy unless the weekly file exists, posted-log rows for the week exist, and the Telegram message contains actionable post copy or a clear blocker. A cron `ok` state is insufficient when the artifact contract is missing.
- **Regression check:** Every Monday after 9:15 AM ET, verify `memory/content/weekly-YYYY-MM-DD.md` exists, `posted-log.jsonl` has LinkedIn/X rows with `source_weekly` for that file, and the latest `content-generate-linkedin` plus `content-generate-x` runs have delivered actionable summaries; otherwise send a recovery/blocker message the same day.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; follow-up owner should patch the content generator/reminder health check or Monday recovery cron.
- **Verification/date:** 2026-06-15 — checked cron run history for `content-generate-linkedin`, `content-generate-x`, `content-reminder`, and `Viral Post Swipe File`; confirmed no `memory/content/weekly-2026-06-15.md`; confirmed only the standalone news-hook row exists for 2026-06-15 in `posted-log.jsonl`.

## 2026-06-15 — Resume included internal fit-verdict language
- **Failure:** The Notion resume summary included “Strong fit for Notion's Professional Services Consultant role,” which is internal recommendation language and should never appear in applicant-facing resume materials.
- **Root cause:** I reused scoring/verdict phrasing from the role assessment inside the resume summary instead of separating internal evaluation language from external application copy.
- **Guardrail/rule:** Resumes must describe evidence, scope, outcomes, and role-relevant capabilities only. Never include evaluator language such as “Strong fit,” “good fit,” “great fit,” “ideal candidate,” “perfect fit,” or “fit for [company/role]” in any resume.
- **Regression check:** `scripts/build_resume_docx.py` now fails resume DOCX generation when banned fit-verdict phrases appear. Before any resume upload, run the markdown parse/build path and scan `memory/drafts/*resume.md` for `Strong fit`.
- **Owner surface updated:** `skills/job-application/SKILL.md`, `scripts/build_resume_docx.py`, Notion resume source/Drive doc, older affected resume drafts, and this Mistakes Log entry.
- **Verification/date:** 2026-06-15 — scanned `memory/drafts/*resume.md` for banned fit-verdict language with no matches, rebuilt the Notion resume DOCX from markdown, confirmed the generated DOCX contains no `Strong fit` or `fit for`, replaced the existing Drive resume doc in place, and verified the generator fails on a fixture containing `Strong fit`.

## 2026-06-15 — Job application materials exposed consulting client names
- **Failure:** The Notion resume and cover letter included specific consulting client names, including Aya and Altmark, in applicant-facing materials.
- **Root cause:** I treated resume/cover-letter proof points like internal proof inventory instead of applying the same privacy boundary used for public site/content copy. The generator guard only blocked fit-verdict language and only validated resumes, so cover letters could still leak client names.
- **Guardrail/rule:** Resume and cover-letter materials must use anonymized consulting proof only. Specific consulting client names are banned in applicant-facing job materials unless JT explicitly approves a one-off exception before upload.
- **Regression check:** `scripts/build_resume_docx.py` must fail both resume and cover-letter generation when banned consulting client names appear. Before upload, scan resume/cover-letter markdown drafts for the banned client-name list and verify the generated DOCX text is clean.
- **Owner surface updated:** `skills/job-application/SKILL.md`, `scripts/build_resume_docx.py`, Notion resume and cover-letter sources, older affected resume/cover-letter drafts, and this Mistakes Log entry.
- **Verification/date:** 2026-06-15 — scrubbed applicant-facing resume/cover-letter drafts for banned client names, rebuilt Notion DOCX files, replaced the existing Drive resume and cover letter docs in place, confirmed generated DOCX text contains no banned client names or fit-verdict language, verified negative fixtures fail for both resume and cover letter, and verified the no-markdown resume fallback is rejected.

## 2026-06-16 — Prompt 6 stalled because execution stopped between phases
- **Failure:** JT had to repeatedly ask for updates and completion on Claude Fable Prompt 6 because I gathered context, reported progress, then stopped before writing/uploading the artifact.
- **Root cause:** I over-applied research/context gathering to a prompt-writing task that already had enough structure, and I treated intermediate status updates as acceptable progress instead of forcing the artifact through the full local draft -> Drive upload -> live verification -> recap loop in one uninterrupted run.
- **Guardrail/rule:** For sequential prompt-package work after the first prompt in a series, cap context gathering at the minimum needed and execute the artifact pipeline immediately. A progress update is not a checkpoint unless the local file exists or a real blocker occurred.
- **Regression check:** Before telling JT a prompt is "in progress," confirm which phase is active. Before stopping, run `test -f memory/drafts/[prompt].md` for the expected local artifact or explicitly state the blocker. Completion requires local file, Drive URL, live Docs verification, and recap entry.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; operational behavior for current Claude Fable prompt series.
- **Verification/date:** 2026-06-16 — Prompt 7 was completed straight through with local draft, Drive upload, live Google Doc verification, weekly recap entry, and no stop after a partial progress update.

## 2026-06-16 — Mission Control mobile Work nav selected the legacy task board
- **Failure:** After Mission Control Slice 1 was reported complete, JT opened mobile Mission Control and saw the legacy `/tasks` Kanban board while the bottom nav highlighted Work, contradicting the expected Slice 1 Work lane.
- **Root cause:** I left `/tasks` as a reachable legacy route and included `/tasks` in the new Work nav aliases. That made an old URL look like the active redesigned Work lane instead of forcing users onto `/work`.
- **Guardrail/rule:** When replacing a primary route with a new lane, old primary URLs must redirect to the new lane or be clearly namespaced under `/legacy/*`; navigation aliases must not mark legacy pages as current primary lanes.
- **Regression check:** `bun test lib/mission-control/routes.test.ts` must assert Work href is `/work`, `/tasks` is not a Work alias, and `/tasks` redirects to `/work`; HTTP verification must confirm `curl -I /tasks` returns `location: /work`.
- **Owner surface updated:** `mission-control/lib/mission-control/routes.ts`, `mission-control/lib/mission-control/routes.test.ts`, `mission-control/components/Sidebar.tsx`, `mission-control/app/tasks/page.tsx`, `mission-control/app/legacy/tasks/page.tsx`, `mission-control/components/mission-control/LegacyTaskBoard.tsx`, `mission-control/CLAUDE.md`, weekly recap, and this Mistakes Log entry.
- **Verification/date:** 2026-06-16 — route tests passed, TypeScript passed, isolated Next build passed, `/tasks` returned 307 to `/work`, following `/tasks` landed on `/work`, and mobile Playwright screenshot of `/tasks` showed the Task router instead of Task Board.

## 2026-06-16 — Mission Control Work lane sorted by recency instead of priority
- **Failure:** JT opened mobile `/work` and saw medium-priority tasks above high-priority tasks, with weak priority color coordination, making the redesigned Work lane feel unlike the intended Claude Design operating cockpit.
- **Root cause:** I reused Convex/API newest-updated order for the Work router and only added neutral priority text. That made the lane behave like a chronological task feed instead of a priority-ranked operating surface.
- **Guardrail/rule:** Mission Control Work defaults must rank by operational importance before recency: high > medium > low, active/problem states above done inside each priority tier, then newest update as the tie-breaker. Priority must have visible color treatment on mobile rows.
- **Regression check:** `bun test lib/mission-control/work-priority.test.ts` must assert high-priority tasks sort above newer medium tasks, done work is demoted inside a priority tier, and high/medium/low visual classes are distinct.
- **Owner surface updated:** `mission-control/lib/mission-control/work-priority.ts`, `mission-control/lib/mission-control/work-priority.test.ts`, `mission-control/app/work/page.tsx`, `mission-control/CLAUDE.md`, Mission Control implementation notes/todo, weekly recap, content proof surfaces, and this Mistakes Log entry.
- **Verification/date:** 2026-06-16 — Work priority tests passed, full Mission Control test suite passed 25 tests / 66 assertions, TypeScript passed, isolated Next build passed, API order spot-check showed high-priority tasks leading, and mobile Playwright screenshot captured `/tmp/mission-control-screens/work-mobile-priority-sorted.png`.

## 2026-06-20 — LinkedIn news-topic drafts lost the article anchor
- **Failure:** JT asked for LinkedIn posts for News topics that add value on top of what the articles said, but the delivered drafts did not explicitly mention the article/source claim or what each article said.
- **Root cause:** I optimized for JT's positioning and current proof lanes after failing to recover exact article metadata, then filled the gap with inferred topic labels instead of stopping to ask for the missing article links/headlines or clearly labeling the drafts as topic-based only.
- **Guardrail/rule:** For News/article-driven content, every draft must begin from a verified source anchor: article title, publisher, link, or a quoted/paraphrased claim from the source. If article metadata is unavailable, ask JT for the links/headlines before drafting rather than writing around inferred topics.
- **Regression check:** Before sending any "News topic" LinkedIn/X draft, verify the saved draft contains a `Source:` line or an explicit first-paragraph article claim for each topic; if not, do not send it as article-based content.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`; operational behavior for News-topic content drafting.
- **Verification/date:** 2026-06-20 — LCM recall confirmed no exact article titles/links/snippets were recoverable from the prior context, and the saved draft only contained inferred topic labels.

## 2026-06-21 — Passive-income pipeline fix left LLM crons on the critical path
- **Failure:** The passive-income Scout failed again on 2026-06-21 after prior repairs, leaving no same-day Scout file. After a manual Scout fallback was created, the Strategist also failed before writing a fresh report.
- **Root cause:** The earlier fix improved prompt rules and degraded-input handling, but still kept long LLM research/validation inside the scheduled crons. That meant artifact creation and cron success still depended on an isolated Codex turn surviving high-token work and final confirmation. The delivery guard also accepted an old blocked-report delivery marker after the strategist report was overwritten.
- **Guardrail/rule:** Scheduled passive-income crons must be deterministic: Scout writes the same-day handoff via script first and stops; Strategist runs the deterministic delivery guard/fallback and stops. Deep Scout/Strategist research is optional/manual, not the weekly cron critical path. Delivery markers must be fresher than the report they prove.
- **Regression check:** Run `python3 scripts/test_passive_income_scout_handoff.py`, `python3 scripts/passive_income_handoff_check.py --mode pre-scout`, `--mode pre-strategist`, and `--mode post-strategist`; all must pass. Manually run both passive-income crons after payload edits and verify `lastRunStatus=ok`.
- **Owner surface updated:** `scripts/passive_income_scout_handoff.py`, `scripts/test_passive_income_scout_handoff.py`, `scripts/passive_income_strategist_delivery_guard.py`, `agents/passive-income-scout/AGENT.md`, passive-income Scout/Strategist cron payloads, `docs/agents/regression-checks.md`, daily note, weekly recap, and this Mistakes Log entry.
- **Verification/date:** 2026-06-21 — generated `memory/passive-income/2026-06-21-scout.md`, wrote a degraded fallback `2026-06-21-strategist.md`, sent fallback digest marker `messageId=24334`, verified pre-scout/pre-strategist/post-strategist all return `PASSIVE_INCOME_HANDOFF_OK`, `scripts/test_passive_income_scout_handoff.py` passes 3 tests, and manual Scout plus Strategist cron reruns both finished `lastRunStatus=ok`.

## 2026-06-22 — Night Autonomy redelivered stale Health Check-in blocker after the fix
- **Failure:** After JT approved fixing the Health Check-in cron, Night Autonomy was rerun and still redelivered the earlier `BLOCKED` report, even though the helper script, cron conversion, duplicate-skip verification, scheduler cleanup, and MC task closure had already happened.
- **Root cause:** I trusted the Night Autonomy rerun to observe fresh owner-surface state, but its prompt read stale daily-note/task context and did not independently verify the newly edited cron/helper/test evidence before reporting.
- **Guardrail/rule:** After repairing the exact blocker named in a Night Autonomy report, rerun verification must first check the changed artifact directly (`openclaw cron get`, helper/test commands, MC task status) and only then redeliver. Do not accept a Night Autonomy rerun summary if it contradicts fresher local evidence.
- **Regression check:** For any corrected Night Autonomy blocker, run the artifact-specific verification command set plus `openclaw cron runs --id [job] --limit 5` or equivalent owner-state check before sending the corrected report. If the cron output is stale, manually correct the report and update daily note/regression checks.
- **Owner surface updated:** `memory/2026-06-22.md`, `memory/weekly-recaps/current-week.md`, `MEMORY.md`, `docs/memory/MEMORY-full.md`, `docs/agents/regression-checks.md`, `scripts/health_checkin_cron.py`, `scripts/test_health_checkin_cron.py`, and this Mistakes Log entry.
- **Verification/date:** 2026-06-22 — `python3 -m unittest scripts/test_health_checkin_cron.py` passed 3/3; helper prepare returned `SKIPPED_DUPLICATE_HEALTH_CHECKIN` for 2026-06-22; Health Check-in cron state showed enabled, main-session systemEvent, next run 2026-06-23 21:00 ET, and `consecutiveErrors=0`; MC task `j572zr0zcfky50mj8cjqg045c5897xhy` was patched done.

## 2026-06-27 — Distribution Phase 2 live-file diffs were summarized instead of sent individually
- **Failure:** JT required individual diffs for each Distribution Phase 2 live-file edit before signoff, but I sent a completion summary and only partial diff coverage, leaving JT unable to approve edits he had not seen.
- **Root cause:** I treated scoped `git status`, rg verification, and earlier progress messages as equivalent to the explicit approval artifact. That collapsed the intended review gate from "each behavior-changing file gets its own diff" into a generic closeout summary.
- **Guardrail/rule:** Live-file edits that active agents/crons read at runtime are not considered done until their exact individual `git diff -- [path]` output has been sent, separately from summaries. Additive files may be batched only when JT explicitly allows batching.
- **Regression check:** Before asking for signoff or saying a gated live-file phase is complete, run `git diff --name-only` for the scoped target set and confirm every modified live file has a corresponding sent diff message or attached diff artifact in the same turn. If any diff was not sent, send it before any completion summary or commit.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`, `docs/agents/regression-checks.md`, and active Distribution Phase 2 closeout behavior.
- **Verification/date:** 2026-06-27 — sent separate diffs for `agents/app-marketing/product-content/AGENT.md`, `memory/app-marketing/templates/claude-design-brief.md`, `memory/app-marketing/experiment-card-template.md`, `memory/app-marketing/measurement-spine.md`, `docs/agents/post-detection-rules.md`, and `agents/vibe-marketing/AGENT.md`; no distribution Phase 2 commit was made.

## 2026-06-28 — Passive-income fallback digests looked like real no-build recommendations
- **Failure:** JT had to ask whether multiple weeks of no passive-income BUILD recommendations were actually optimal. The June 21 and June 28 digests said no BUILD, but both were deterministic fallback outputs, not full Strategist validation.
- **Root cause:** The June 21 safety repair correctly removed long LLM Scout/Strategist work from the scheduled cron critical path, but I did not add a follow-on escalation rule for repeated fallback weeks. That made artifact reliability improve while strategy quality silently degraded.
- **Guardrail/rule:** A passive-income `DEGRADED FALLBACK`, `RECOVERED DEGRADED RUN`, or `DETERMINISTIC HANDOFF` week is not a true no-build verdict. If fallback happens two weeks in a row, create/update one Mission Control validation task and label the next digest as degraded, not as a strategic conclusion.
- **Regression check:** Every Sunday passive-income digest and the next 10AM film review must check the current Scout/Strategist files for fallback markers. If found in consecutive weeks, verify a live MC validation task exists with first action, why it matters, and done state before closing the check.
- **Owner surface updated:** `docs/agents/mistakes-log-recent.md`, `docs/agents/regression-checks.md`, and the Mission Control passive-income validation task created from this finding.
- **Verification/date:** 2026-06-28 — audited June 7/14/21/28 reports; confirmed June 7 had one BUILD, June 14 was degraded with no BUILD, June 21 and June 28 were fallback-only; added regression check and created the follow-up MC task.

## 2026-07-05 — AI Ops Teardown resurfaced already-posted Canals bundle
- **Failure:** The AI Ops Teardown weekly response selected the existing Canals Wholesale Order Intake Desk bundle again even though JT had already posted a Canals teardown.
- **Root cause:** I trusted the delivery calendar and open Mission Control review task as the only unposted gate. Those sources still said Canals was ready/open, while the content-bank file had a pasted `posted:true` record and JT's correction confirmed the post had already happened. The posted-log also still said `posted:false`, so the stale state won.
- **Guardrail/rule:** Before resurfacing an existing teardown as `AI_OPS_TEARDOWN_SKIP`, cross-check delivery calendar, Mission Control task status, `memory/content/posted-log.jsonl`, and the bundle's content-bank posted marker. If any durable source or JT correction says already posted, retire the bundle and close the review task instead of asking JT to review/post it again.
- **Regression check:** For AI Ops Teardown weekly runs, `rg -n "\"posted\":true|JT_CONFIRMED|Status: posted" memory/content/posted-log.jsonl memory/content/bank memory/consulting/ai-ops-teardowns/delivery-calendar.md` must be checked before selecting an existing bundle; no selected topic may have a posted/retired marker.
- **Owner surface updated:** `memory/consulting/ai-ops-teardowns/delivery-calendar.md`, `memory/content/posted-log.jsonl`, `agents/ai-ops-teardown/weekly-prompt.md`, Mission Control task `j57fdnkcyd9ath934d35cyrdnh87tcbz`, and this Mistakes Log entry.
- **Verification/date:** 2026-07-05 — Canals delivery calendar moved to Posted / Retired, posted-log changed to posted with URL-not-captured marker, weekly prompt gained the cross-check rule, and Mission Control task `j57fdnkcyd9ath934d35cyrdnh87tcbz` verified `status: done`.
