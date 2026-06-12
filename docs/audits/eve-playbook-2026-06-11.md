# Eve Optimization Playbook
**Date:** 2026-06-11
**Version:** 2 (incorporates Eve's review; supersedes the version Eve analyzed)
**Companion to:** eve-optimization-report.md
**Contents:** usage instructions, 8 phase prompts to paste to Eve in order, and Appendices A and B containing the full replacement prompts for content-generate-linkedin and content-generate-x.

---

## How to use this playbook

1. Send Eve both files (this playbook and the report) as Telegram document attachments, then paste the Phase 0 prompt. If attachments do not come through, upload both to Drive and have Eve download them, or paste the report in sections; the playbook must land on disk because Phase 4 installs the appendix prompts from it.
2. Run one phase per sitting. Order: 1, then 2B (plan, your go, apply), then 2A, then 3, 4, 5, 6, 7. The watchdog and restart path get fixed before the intentional restart in 2A. Let at least one normal cron day pass after Phases 2A, 4, and 5 so you can observe effects before continuing.
3. Run phases mid-day or evening, never during the 5:00 to 9:00 AM cron congestion window.
4. Phases 2B, 6, and 7 are plan-gated: Eve presents a plan and waits for your "go." All other phases execute directly because their scope is fully named.
5. Each prompt contains exactly the approvals that phase needs (Eve's Hard Rules require your explicit approval for model and auth config changes). Approvals are scoped to the named changes only.
6. If anything goes wrong, reply: "Stop. Restore the affected files from docs/audits/backups-2026-06-11 and report exactly what changed." Every phase creates backups before editing.
7. Do not paste the report and say "apply this." The report is reference material; these prompts are the execution layer.

---

## Phase 0: Save, back up, plan (no changes)

```
Eve, two files are attached: my external audit analysis and an execution playbook. Do exactly this and nothing else this session:

1. Save them to the workspace as:
   docs/audits/eve-optimization-report-2026-06-11.md
   docs/audits/eve-playbook-2026-06-11.md
2. Create docs/audits/backups-2026-06-11/ and copy into it: ~/.openclaw/openclaw.json, ~/.openclaw/cron/jobs.json, ~/.openclaw/agents/main/agent/auth-profiles.json, and AGENTS.md, MEMORY.md, TOOLS.md, HEARTBEAT.md, SOUL.md, USER.md from the workspace root.
3. Create plans/eve-optimization-2026-06-11.md listing Phases 1, 2A, 2B, 3, 4, 5, 6, 7 from the playbook, each with status=pending and a one-line scope.
4. Read the report's five Findings.

Reply with: the two saved paths, the backup file list with byte sizes, and one line per phase confirming you understand its scope. Do not change any config, cron job, prompt, or bootstrap file in this session.
```

---

## Phase 1: Cron cleanup (named list only)

```
Eve, Phase 1 of plans/eve-optimization-2026-06-11.md. Cron job cleanup, jobs.json only. Verify the backup at docs/audits/backups-2026-06-11/jobs.json exists before editing.

A. ARCHIVE THEN REMOVE these 12 jobs. First export each full JSON entry to docs/audits/removed-jobs-2026-06-11.json, then remove:
- All 7 jobs titled "Catch-up: ..." scheduled at 2026-04-28
- "Review Stalled Projects/Outreach" (at 2026-04-07)
- "Reminder: Reevaluate Codex harness config" (at 2026-05-09)
- "Altmark rent delinquency tracker follow-up check" (at 2026-05-15)
- "reddit-daily-gen-rerun-check-2026-05-24"
- "content-generate (DISABLED, split into linkedin + x generators)"
Keep "Reminder: YouTube TV midday" (2026-06-25); it is future-dated.

B. DISABLE, do not delete, the older duplicate in each pair:
- Keep passive-income-scout (1 PM Sun); disable Passive Income Scout (6:30 AM Sun)
- Keep passive-income-strategist (3 PM Sun); disable Passive Income Strategist (8:30 AM Sun)
- Keep Health Check-in (Pattern-Focused); disable Health Check-in Prompt
- Weekly Strategic Gut-Check vs Weekly North Star Command Center, both Sunday 6 PM: read both prompts. If one is a subset of the other, disable the subset and tell me which. If genuinely distinct, move one to 6:30 PM and keep both.
- Leave both TikTok warm-up reminders running; Phase 5 converts them to digest entries.

C. Edit jobs.json via a python script file (json load, modify, atomic write). No heredocs. Touch nothing outside the named jobs.

D. BASELINE: from the run records in jobs.json, compute the last-7-day delivery rate for user-facing jobs (delivered runs vs scheduled runs for jobs with Telegram delivery) and save it to docs/audits/baseline-delivery-2026-06-11.md. This is the before metric for the Phase 2A fallback change; we recompute it 7 days after Phase 2A.

E. Verify: openclaw cron list --json parses cleanly; report before/after job counts, the baseline delivery rate, the removed list, the disabled list, and the archive path. Update the plan file.
```

---

## Phase 2A: Config changes, lcm.db reset, restart

```
Eve, Phase 2A. I am giving explicit approval, per Hard Rule 1 and the Model Routing rule, for the model-config change below. Scope is exactly these edits to ~/.openclaw/openclaw.json using the Edit tool, never Write:

0. SMOKE TEST FIRST: before touching config, run one throwaway prompt explicitly on moonshot/kimi-k2.6 (a one-off session or a manual run with a model override). Confirm it routes and responds, then check the Moonshot account for what that single run actually billed. If routing fails or billing is not as expected, stop and report; do not set the fallback.
1. agents.defaults.model.fallbacks: set to ["moonshot/kimi-k2.6"]. Approved provider: Moonshot, expected cost $0 per the config's listed pricing. If OpenClaw supports per-job fallback chains, apply the fallback to cron jobs only and leave the interactive default without one; if it does not, set it globally. Either way, any run that actually executes on the fallback must name the model in its run summary or reply, so I always know when I am reading Kimi output. High-stakes work is unaffected: the two content jobs move to Sonnet in Phase 4 and job-application packages already mandate Sonnet.
2. tools.media.audio: remove the "language": "es" pin so transcription auto-detects. Keep echoTranscript and echoFormat unchanged.
3. Change no other key. Do not touch auth profiles, the primary model, or compaction settings.

Then back up and reset the oversized context DB per the documented recovery step: cp ~/.openclaw/lcm.db ~/.openclaw/lcm.db.backup-$(date +%Y%m%d) then remove the original (now ~192MB, past the documented 100MB threshold). Do this in a quiet window with no cron due in the next 30 minutes. The reset trades away some compaction continuity; we accept that cost knowingly.

Then restart with: bash ~/.openclaw/workspace/scripts/restart-gateway.sh "phase-2a config"

Verify: diff openclaw.json against the Phase 0 backup and confirm only the two intended changes exist; confirm the gateway is healthy; confirm a fresh small lcm.db was created; then run one normal exchange and check the next heartbeat for compaction or recall errors in the logs. Reply with the diff summary, the smoke-test result, and all statuses. Update the plan file.
```

---

## Phase 2B: Watchdog, loopback binds, secret scrub (plan-gated)

```
Eve, Phase 2B. Three reliability and security fixes. Plan Mode applies: investigate, send me the plan with summarized file diffs, and wait for my "go" before applying anything.

1. WATCHDOG. Read scripts/gateway-watchdog.sh and ~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist. Diagnose why "kickstart failed, trying unload+load once" looped every ~10 minutes for hours on 2026-05-04, 05-13, and 05-31 in ~/.openclaw/logs/watchdog.log, including the unload I/O errors. Propose a fix, plus this addition: if the gateway responds but the last 3 cron runs failed with "No available auth profile for openai-codex", automatically run the documented cooldown clear (reset usageStats in auth-profiles.json) and restart via restart-gateway.sh, rate-limited to once per 6 hours, logging every trigger to the watchdog log.

2. LOOPBACK BINDS. Bind n8n (port 5678, via com.n8n.server.plist env), mission-control next (port 3000), and convex (3210/3211) to 127.0.0.1. Tailscale serve proxies localhost, so remote access is preserved. After applying, verify https://jts-mac-mini.tailaf2fd2.ts.net and the /n8n path still load. If convex cannot bind loopback, leave it and note it.

3. SECRET SCRUB. Open memory/2026-02-21-model-routing.md and memory/2026-02-23.md. If they contain actual key or encryption-key VALUES rather than just names, replace each value with [REDACTED-name] and tell me which were live so I can rotate them. Add the memory/ directory to the existing key-pattern scan routine.

After my "go": apply, verify each item (watchdog dry-run, lsof -i to confirm binds, tailnet check), and report results. Update the plan file.
```

---

## Phase 3: Build the voice corpus

```
Eve, Phase 3: build memory/jt-corpus.md, the canonical sample of MY OWN published writing. This file will become the primary voice source for all content generation.

Sources, in priority order:
1. My live X posts: use the x-research skill to pull originals from @jts_14 (no replies, no reposts), last 6 months, up to 40 candidates. This spends X API budget once and is approved for this run only.
2. LinkedIn: pull anything harvested by the linkedin-corpus agent or skill. If it holds no posts, list what exists and I will paste my LinkedIn posts manually.
3. memory/content/bank/ entries and posted-log.jsonl rows with posted=true, ONLY where you can match them to a version I actually published. Drafts I never posted do not qualify.

Selection rules: 15 to 25 entries total. Favor format variety: proof posts, observations, thread openers, replies. For each entry record platform, format tag, date, and the full text VERBATIM. Do not edit, clean up, or improve my wording in any way. Cap the file at 15K characters; if over, keep the most recent and most stylistically distinct.

Deliver: upload the corpus to Drive (Content/Voice/jt-corpus) and give me the Drive link plus local path, with a 5-line note on the patterns you observe in my writing. Then stop. I will reply "corpus approved" or send edits. Do not wire the corpus into any cron yet. Update the plan file.
```

---

## Phase 4: Install the v2 content prompts and the edit-delta loop

Run only after you have replied "corpus approved."

```
Eve, Phase 4. Preconditions, confirm all before proceeding: I replied "corpus approved"; memory/jt-corpus.md exists; and the corpus passes this quality gate: at least 12 entries total, at least 4 LinkedIn and 6 X, at least 3 distinct formats. If the gate fails, stop and tell me exactly what is missing so I can paste more posts or write 2 or 3 fresh seed posts; do not install around a thin corpus. If the approved corpus lacks a format the appendix prompts assume (threads, for example), adjust that slot's format language to match the corpus and show me the adjusted lines before installing.

I am giving explicit approval per the Model Routing rule for a per-job model override on exactly two jobs: content-generate-linkedin and content-generate-x. Set payload.model to "openrouter/anthropic/claude-sonnet-4-6" on both. Named cost cap: $10 per month combined; alert me if the OpenRouter monthly spend line attributable to these two jobs crosses it.

Steps:
1. Read docs/audits/eve-playbook-2026-06-11.md, Appendix A (linkedin) and Appendix B (x). These are the complete replacement prompt texts.
2. Back up the current payload.message of both jobs to docs/audits/replaced-prompts-2026-06-11.md.
3. Optional but preferred: first create scripts/run_content_guard.sh, a thin wrapper taking platform and Monday date that runs the distribution guard with absolute paths; if you create it, substitute the wrapper call for the guard line in both appendix texts and show me the substitution. Then replace payload.message of each job with the (possibly substituted) appendix text exactly, and set payload.model as approved. Do this via a python script file editing jobs.json with an atomic write. No heredocs, no compound shell commands, absolute paths only, per Hard Rule 6. Change nothing else: schedules, ids, delivery, and every other job stay untouched.
4. Create an empty memory/content/edit-deltas.jsonl. Then run wc -c on AGENTS.md; if it is within 1,500 chars of its 28K budget, put the following rule in docs/agents/content-rules.md with a one-line pointer in AGENTS.md, otherwise add it to the AGENTS.md content section directly: "When JT replies posted: ask once, any edits? Paste the final text if changed. If he pastes, diff it against the draft and append {date, platform, draft_excerpt, final_excerpt, delta_summary} to memory/content/edit-deltas.jsonl. If no edits, log delta:none. Never fetch from the X API for this."
5. Verify: openclaw cron list --json parses; show me the first 200 characters of each new payload.message and both model fields.

Reply with the verification output and backup path. Update the plan file. The new prompts run on their normal schedules; after their first run I will review quality before any further content changes.
```

---

## Phase 5: Send Queue and evening digest

```
Eve, Phase 5: delivery restructure. Goal state: I receive ONE morning decision message capped at 3 items and ONE evening digest. Reminder-type jobs stop sending standalone Telegram messages.

1. Establish memory/digest-queue.md: jobs whose output is a reminder or FYI append a 1 to 3 line entry there instead of messaging me. Convert these jobs by editing ONLY the delivery instruction at the end of each payload.message, nothing else: reddit-karma-daily-reminder, Nash Satoshi TikTok Warmup Reminder, both TikTok App Account Warm-up Reminders, and ReelFarm Daily Strategy Intel (file write plus digest entry; Telegram only for a verified critical finding). Leave content-reminder fully intact; it delivers posts.

2. Create one new cron, "Evening Digest", daily 7:00 PM ET: read memory/digest-queue.md; if non-empty, send one consolidated message under 2,500 characters, then clear the file; if empty, send nothing. Lightweight: max 5 tool calls, no web searches.

3. Morning Brief: edit its prompt to open with a SEND QUEUE section, hard cap 3 items, each item a finished artifact with a link and a one-word reply keyword (send, post, or skip). Replace the Nash full-text delivery contract with: include the first 2 lines of the Nash X post and the Reddit draft plus the file path and Drive link; the full text appears as a Send Queue item when it is among the day's top 3 actions. This is my explicit decision overriding the existing non-negotiable Nash delivery block; annotate the change inline with today's date.

4. Back up every payload.message you edit to docs/audits/phase5-prompt-backups.md before changing it.

Verify: cron list parses; show me the new Morning Brief prompt's first 400 characters and the Evening Digest job entry. Update the plan file.
```

---

## Phase 6: Bootstrap diet and contradiction cleanup (plan-gated)

```
Eve, Phase 6: bootstrap reduction. Plan Mode: produce the plan and wait for my "go" before changing anything. Target: total bootstrap under 45K characters (currently about 80K). Nothing is deleted in this phase, only relocated, except the one contradictory rule named below.

1. MEMORY.md to an index format under 8K: each section compresses to 3 to 6 lines of current-state facts plus a pointer into docs/memory/MEMORY-full.md, where the detail moves.
2. TOOLS.md under 9K: move command-syntax blocks into docs/tools/TOOLS-full.md or the matching skill file; keep one-line pointers in TOOLS.md.
3. AGENTS.md: rewrite Core Rule 11 instead of deleting it. Remove the Gemini Flash-Lite default sentence, which contradicts the Model Routing section and the actual config, but keep the escalation principle as: complex multi-file coding, hard debugging, or high-stakes strategy work runs on Sonnet-class reasoning via sub-agent (openrouter/anthropic/claude-sonnet-4-6), a JT-approved standing exception counted against the named OpenRouter cap. Fix the stale TOOLS.md Notion line claiming a 5:30 AM isolated-sonnet cron. No other rule changes.
4. jobs.json: remove payload.model from every job where it equals "openai/gpt-5.5", since that is already the default. Preserve every override that differs, including the two Sonnet content jobs from Phase 4. Python script, atomic write, backup first.

Your plan must list: per-file before and after character counts, exactly which sections move to which destination files, and the count of overrides to be removed. After my "go": apply, run wc -c on all bootstrap files, run one test session confirming nothing critical fails to load, and report the numbers. Update the plan file.
```

---

## Phase 7: Night-agent merge, KPIs, autonomy lanes, rewrite ritual (plan-gated)

```
Eve, Phase 7: structural changes. Plan Mode: plan first, wait for my "go".

1. NIGHT MERGE. Combine nightly-autonomous-leverage-agent (9:45 PM) and the Overnight Autonomy Agent (3:20 AM) into ONE job at 11:00 PM with a two-phase prompt: phase one carries the strategic-worker behavior of the 9:45 prompt; phase two carries the verification and blocker-removal behavior of the 3:20 prompt. Raise the merged budget to completing one full artifact per night within the lanes in item 2. Disable both originals (do not delete) and archive their prompts to docs/audits/.

2. AUTONOMY LANES. After a wc -c budget check (extract to a subfile with pointer if needed), add to AGENTS.md: three sanctioned autonomous lanes with full completion authority and no asking: (a) content taken to ready state (drafted, validated, Drive, Notion, queued); (b) prospect research taken to a complete outreach packet (contact verified, hook, draft, Drive link); (c) ops self-healing (cron fixes, zombie cleanup, cooldown recovery, file-budget trims). Everything outside these lanes remains advisory. Never-send-outreach and all Hard Rules are unchanged.

3. OUTCOME KPIs. Edit the Weekly Systems Review prompt to report six numbers every week: posts delivered vs posted, engagement per posted item, outreach packets completed vs sent vs replied, consulting pipeline stage movement, cron delivery rate, dollars spent (OpenRouter plus X API). Edit the Monthly Goal-Skills Gap prompt so its comparison step targets these KPIs instead of job-description keyword scans.

4. REWRITE RITUAL. Add to Weekly Systems Review, first Sunday of each month: identify the 5 longest payload.message prompts, rewrite each clean under 600 words with tooling rules moved into scripts, and get my approval per prompt before installing. Also create scripts/cron_snapshot.py to copy jobs.json into config/cron-snapshots/jobs-[date].json and git commit it, invoked from the existing daily critical-files-integrity job so no new LLM cron is added.

Plan with diffs summarized, then apply on my "go", verify, report, and mark the plan file complete.
```

---
---

## Appendix A: Replacement prompt for content-generate-linkedin

Eve installs this verbatim as payload.message in Phase 4. Job model: openrouter/anthropic/claude-sonnet-4-6. Schedule unchanged.

```
You are Eve generating JT's weekly LinkedIn queue. Corpus-first design: JT's own published writing is the primary style source. Rules and references support it, never replace it.

STEP 0 REQUIRED READS. Stop with "BLOCKED: [file] missing" if a required file is absent:
1. memory/jt-corpus.md (REQUIRED)
2. memory/content/edit-deltas.jsonl, last 10 entries, if present. Treat JT's edits as the highest-signal voice corrections.
3. memory/content/current-efforts.md and memory/content/recent-builds.md
4. memory/content/weekly-intel-brief.md
5. memory/content/posted-log.jsonl, last 21 days, for anti-repeat
6. One narrow swipe fetch only: python3 /Users/jtsomwaru/.openclaw/workspace/scripts/notion-swipe-fetch.py --platform LinkedIn --niche "AI Consulting" --niche "Personal Brand" --limit 6 --since-days 30 --fetch-limit 200. Swipe results supply hook mechanics and topic signals only, never wording, rhythm, or persona.

STEP 1 SLOT PLAN. Two slots. Fewer, better posts.
- L1 (proof): must originate from recent-builds.md or an active current-efforts.md item. First-person operator proof.
- L2 (niche signal): one signal from weekly-intel-brief.md translated through JT's actual work. If no signal connects to JT's work, write SKIP_SLOT: no earned angle.

STEP 2 PER-SLOT PROCEDURE. One slot at a time. Finish L1 completely, including its audit, before starting L2.
a. Select the 5 corpus entries closest to this slot's format. Copy them verbatim into the weekly file under "### Exemplars used: L[N]".
b. Draft the post to match the exemplars' cadence, sentence length, vocabulary, and proof style. The exemplars are the voice target; the swipe mechanic shapes only the hook.
c. Write 3 alternative first lines, keep the strongest, discard the rest.
d. AUDIT. Every check must pass; revise once, then SKIP_SLOT:
- Contains at least one verifiable first-person specific: a number, artifact name, tool decision, or failure.
- First line names a buyer-recognizable problem or a concrete result. No warmup.
- Reads more like the exemplars than like the swipe references. If not after one rewrite, SKIP_SLOT: voice mismatch.
- No em dashes, no exclamation points, no stacked -ly adverbs, no placeholders, no [Source], no invented anecdotes, no real client or company names without recorded permission.
- Not a repeat of any topic or structure from the last 21 days of posted-log.jsonl.
The former you:I ratio rule is retired. First-person proof is encouraged.

STEP 3 FILE WRITE. Write the LinkedIn section and "## LinkedIn Reference Mechanics" to memory/content/weekly-[MONDAY-DATE].md. Every reference row includes Source URL, Platform, Niche, Format, Hook mechanic, and JT translation. Do not overwrite any existing X section.

STEP 4 GUARD, mandatory, single command, no cd chaining: python3 /Users/jtsomwaru/.openclaw/workspace/scripts/content_distribution_guard.py --weekly /Users/jtsomwaru/.openclaw/workspace/memory/content/weekly-[MONDAY-DATE].md --require-reference-map linkedin --check-notion-script
If the guard fails: no Drive upload, no approved copy. Send a concise BLOCKED packet with the failing lines and the local path.

STEP 5 FINALIZE. Upload to Drive (Content/LinkedIn). Append one posted-log.jsonl row per written slot: date, platform=linkedin, day, pillar, topic, posted=false, banked=false, scheduled_in_notion, drive_link, source_weekly. Verify with rg that the row count for this source_weekly equals the slots written; if zero, send a blocker instead of claiming success. Send the action-first Telegram review packet. If every slot was skipped, send only the skip reasons.

TOOLING: existing workspace scripts, rg, jq, and shell appends only. Single commands with absolute paths; no cd chaining, no compound commands, no heredocs or inline multi-line interpreter snippets. JT presses send. Never post publicly.
```

---

## Appendix B: Replacement prompt for content-generate-x

Eve installs this verbatim as payload.message in Phase 4. Job model: openrouter/anthropic/claude-sonnet-4-6. Schedule unchanged.

```
You are Eve generating JT's weekly X queue. Corpus-first design: JT's own published posts are the primary style source. Rules and references support it, never replace it.

STEP 0 REQUIRED READS. Stop with "BLOCKED: [file] missing" if a required file is absent:
1. memory/jt-corpus.md (REQUIRED)
2. memory/content/edit-deltas.jsonl, last 10 entries, if present. Treat JT's edits as the highest-signal voice corrections.
3. memory/content/current-efforts.md and memory/content/recent-builds.md
4. memory/content/weekly-intel-brief.md
5. memory/content/posted-log.jsonl, last 21 days
6. The existing memory/content/weekly-[MONDAY-DATE].md if present. Never overwrite the LinkedIn section.
7. One narrow swipe fetch only: python3 /Users/jtsomwaru/.openclaw/workspace/scripts/notion-swipe-fetch.py --platform X --niche "AI Consulting" --niche "AI Agents" --niche "Personal Brand" --limit 8 --since-days 30 --fetch-limit 200. Hook mechanics and topic signals only, never wording, rhythm, or persona.

STEP 1 SLOT PLAN. Three slots.
- X1 (proof): from recent-builds.md or an active current-efforts item. What was built or shipped, with one concrete detail.
- X2 (operator observation): a specific claim only someone doing JT's client or agent work would make, anchored to a current effort.
- X3 (optional): only if a fresh signal from the intel brief or swipe fetch connects to an earned angle. Otherwise write SKIP_SLOT: no fresh earned angle.

STEP 2 PER-SLOT PROCEDURE. Sequential. Complete each slot, including its audit, before starting the next.
a. Select the 5 corpus entries closest to this slot's format. Copy them verbatim into the weekly file under "### Exemplars used: X[N]".
b. Draft to match exemplar cadence, length, vocabulary, and proof style.
c. Write 3 first-line variants, keep the strongest.
d. AUDIT. Every check must pass; revise once, then SKIP_SLOT:
- First line opens with the point. Singles roughly 6 to 25 words. Threads max 3 tweets.
- At least one verifiable first-person specific: a number, artifact name, tool decision, or failure.
- No links in the body, no hashtags, no em dashes, no exclamation points, no banned -ly adverbs, no invented anecdotes, no real client or company names without recorded permission.
- Build-showcase endings state what the build does, not advice to the reader.
- Reads more like the exemplars than like the swipe references. If not after one rewrite, SKIP_SLOT: voice mismatch.
- No topic or structure repeat from the last 21 days of posted-log.jsonl.
The former you:I ratio rule is retired. First-person proof is encouraged.

STEP 3 FILE WRITE. Append "## X Reference Mechanics" and the X section to memory/content/weekly-[MONDAY-DATE].md. Every reference row includes Source URL, Platform, Niche, Format, Hook mechanic, and JT translation.

STEP 4 GUARD, mandatory, single command, no cd chaining: python3 /Users/jtsomwaru/.openclaw/workspace/scripts/content_distribution_guard.py --weekly /Users/jtsomwaru/.openclaw/workspace/memory/content/weekly-[MONDAY-DATE].md --require-reference-map x --check-notion-script
If the guard fails: no Notion push, no Drive upload, no approved copy. Send a concise BLOCKED packet with the failing lines and the local path.

STEP 5 FINALIZE. Upload the complete weekly file to Drive. Push Notion Calendar entries with python3 /Users/jtsomwaru/.openclaw/workspace/scripts/notion-calendar-push.py. Append one posted-log.jsonl row per written slot (posted=false) and verify with rg that the row count matches the slots written; if zero, send a blocker instead of claiming success. Send the action-first Telegram review packet. If every slot was skipped, send only the skip reasons.

TOOLING: existing workspace scripts, rg, jq, and shell appends only. Single commands with absolute paths; no cd chaining, no compound commands, no heredocs or inline multi-line interpreter snippets. JT presses send. Never post publicly.
```
