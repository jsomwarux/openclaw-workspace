# Eve System Audit: Findings and Optimization Plan
**Date:** 2026-06-11
**Version:** 2 (incorporates Eve's review of the same date)
**Basis:** eve-audit-report.md (28,510 lines, command-verified), JT's stated North Star, frustrations, and constraints (OpenAI OAuth as default, minimal OpenRouter spend).

---

## Verdict

Eve is one of the most thoroughly documented personal agent systems I have seen, and it is structurally overextended. The system has 80 cron jobs, 80,425 characters of bootstrap loaded into every session, one auth profile carrying nearly all of it, and 30 of 80 jobs showing repeat failures during the audit window. The content pipeline that frustrates you most is failing for a design reason, not a tuning reason. The proactivity gap is real but it is not where you think it is: Eve produces more than you can consume, and your review bandwidth, not Eve's output, is the bottleneck. The self-improvement machinery is extensive but it optimizes uptime, not outcomes, and its patch mechanism is actively degrading prompt quality over time.

The good news: almost every problem below is fixable with configuration and design changes, not new infrastructure. Most of the hard parts (validators, guards, logging, Mission Control, Drive sync) are already built.

## What is working and should not change

The safety architecture is genuinely good: "never send outreach, JT presses send" is the right rule and stays. Telegram allowlist of one, gateway on loopback with token auth, Tailscale for remote, elevated tools off, sacred-files protection, the no-LLM LaunchAgent rule, and the deterministic guard scripts (content_distribution_guard, delivery guards, cron_volume_guard) are all correct. USER.md is excellent. The Mistakes Log with mandatory regression checks is better practice than most professional teams have. Keep all of it.

---

## Finding 1 (highest impact): One auth profile is carrying 80 jobs and it collapses daily

**Evidence.** Primary model is `openai/gpt-5.5` via the openai-codex OAuth, fallbacks are empty (`"fallbacks": []`), and roughly 70 of 80 jobs carry a per-job override to the same model. The dominant failure across the 30 flagged jobs is `No available auth profile for openai-codex (all in cooldown or unavailable)` plus `stream disconnected` from the Codex backend. Morning Brief itself failed 3 of its last 5 runs on exactly this.

**The math.** Weekdays run roughly 30 to 34 LLM cron sessions. Each one loads about 80K characters of bootstrap (around 20K tokens) before the job prompt, which itself averages 1,500 to 4,000 words of accumulated instructions. That is conservatively 1.5M to 2.5M tokens per day pushed through a consumer subscription OAuth. The provider rate-limits, the 1-hour failure window trips cooldown, the documented cooldown-persistence bug keeps it tripped, and everything scheduled in the 5:15 to 7:30 AM pileup dies together: job market 5:15, crypto 6:00, job app builder 6:15, cold hook 6:30, email pivot 6:45, build ideas 7:15, morning brief 7:30. Your most important daily output sits at the end of the most congested window on a single rate-limited credential.

**Fixes, ranked:**

1. **Approve one fallback for cron jobs: `moonshot/kimi-k2.6`.** It is already configured in your models block with cost listed at 0 and an API key in place. Set `agents.defaults.model.fallbacks: ["moonshot/kimi-k2.6"]` (or per-job for briefing and research jobs). Your Model Routing rule requires your explicit approval plus a named cap; this is that approval, cap $0 on Moonshot and verify its actual billing once. A morning brief written by Kimi beats a morning brief that never arrives. Smoke-test routing and billing with one throwaway run before flipping it, scope it to the cron tier if per-job fallbacks are supported, and require fallback runs to name their model in output. This change converts the audit window's auth-cooldown failures into degraded-but-delivered runs.
2. **Cut the bootstrap tax.** 80,425 chars per session is the silent driver of the rate limiting. MEMORY.md is at 19,977 of a 20,000 budget (99.9 percent full) and TOOLS.md at 15,232 of 16,000. Restructure MEMORY.md into an index of pointers with details in docs/memory, target under 8K. Move TOOLS.md command syntax into skills that load on demand. Target total bootstrap under 45K. That alone cuts per-session input roughly 45 percent across 30+ daily sessions.
3. **Automate the cooldown-bug recovery.** The fix is already documented (clear usageStats in auth-profiles.json, restart). Put it in the watchdog: if gateway is up but the last 3 cron runs failed with the cooldown error, run the clear script automatically. Right now a known bug with a known one-line fix takes down mornings until you notice.
4. **Spread the schedule.** Move non-consumer research jobs (skills researcher, ReelFarm intel, reddit gen, dynasty) into the 8 PM to 2 AM band. Keep the 90-minute producer-to-consumer rule. No more than 2 LLM jobs per 30-minute window before 9 AM.
5. **Remove the ~70 redundant per-job model overrides.** They all say `openai/gpt-5.5`, which is already the default. They add nothing today and mean any future model change requires editing 70 job entries. Inherit the default; override only where a job genuinely needs a different model.
6. **Housekeeping with hard thresholds.** lcm.db is at 185MB; your own recovery doc says back up and reset above 100MB. The watchdog log shows kickstart-failed loops repeating every 10 minutes for hours on May 4, May 13, and May 31 (with unload I/O errors), meaning the watchdog script itself has a bug in its restart path. Fix both this week.

---

## Finding 2: The content system cannot produce your voice, by design

This is your top frustration and the cause is structural. Four mechanisms are working against you simultaneously.

**1. Voice is defined almost entirely by negative constraints.** No em dashes, no -ly adverbs, no contrast pairs, no corporate words, banned phrase lists, mandatory checklists. Blocklists can only prevent failure modes; they cannot produce a specific human's voice. What a model writes under a constraint list is constraint-satisfying text, which is its own recognizable flavor of AI output. You have already experienced this: the rules got stricter and the output stayed obviously generated.

**2. The 5:1 you:I ratio rule is pointed the wrong way.** Forcing "you/your" to outnumber "I/my" 5 to 1 pushes every post into second-person advice format. Advice-format posting is the single most oversaturated, most AI-coded genre on LinkedIn and X right now. Your actual credibility asset is first-person operator proof: I built this, it broke here, this is what the client paid for, this is the number. Your own Worthiness Gate and recent-builds anchoring already point this direction; the ratio rule fights them. Kill the ratio rule. Replace it with: every post must contain at least one verifiable first-person specific (a number, an artifact, a named tool decision, a failure).

**3. Batch generation guarantees rhythmic sameness.** content-generate-x writes 7 posts in one context window; content-generate-linkedin writes 4; Weekly Content Batch writes 5 to 7 more. A model generating 7 posts in one pass converges on one sentence rhythm by post 3. Generate one post per fresh run, never more than 2.

**4. The generator never sees your actual writing at draft time.** The prompts instruct a "quick scan of Hard Rules" in content-voice.md and anchor on a swipe file of other people's viral posts. So the model imitates strangers' mechanics under your blocklist. The single highest-leverage change: build a `jt-corpus.md` of 15 to 25 posts you actually wrote (or heavily edited and posted), and require every content prompt to inline 5 of them verbatim, selected for format match, immediately before drafting, with the instruction "match the cadence, vocabulary, and proof style of these exemplars; the swipe reference supplies only the topic and hook mechanic." Few-shot on your own words beats every rule you have written.

**Two additions that close the loop:**

5. **Capture your edit deltas.** You already have posted-log.jsonl and FEEDBACK-LOG.md. The missing signal is the diff between Eve's draft and what you actually posted. Add a tiny step: when you reply "posted," Eve fetches your live post (x-research skill can pull your own profile), diffs it against the draft, and appends the delta to FEEDBACK-LOG.md. Ten of those diffs are worth more than every voice rule combined, and the weekly content jobs should be required to read the last 10 deltas before drafting.
6. **Put a better writer on the final pass, capped.** gpt-5.5 drafting and gpt-5.5 grading itself has correlated blind spots. Route a single rewrite-and-rank pass for the week's 8 to 11 posts through `openrouter/anthropic/claude-sonnet-4-6` (you already mandate Sonnet for resumes for the same precision reason). At your volume this is well under $5 per month against your $50 cap. Optionally run a monthly cross-model critique (Gemini or Claude grades the month's drafts against jt-corpus.md), which is exactly your second-opinion pattern applied to Eve.

**Topic relevance fix.** Your complaint that subjects do not match what you are working on or attract buyers has a config-level cause: topics flow from the swipe file (what is viral among AI-creator X) and weekly-intel-brief (niche news), while `current-efforts.md` was explicitly demoted to "a relevance ladder, not a cage" in the 2026-05-07 patch. Invert it for two of the weekly slots: at least 2 posts per week must originate from recent-builds.md or an active client milestone, with the swipe file contributing only the hook mechanic. Buyers hire the person doing the work they need done; the work is in current-efforts, not in trending discourse.

**Volume cut.** You currently generate roughly 11+ branded posts per week plus daily news hooks, daily reddit, daily dynasty, daily DynastyJig packs, and 4 vibe posts. Your own App Marketing OS rule says MEASURE_FIRST and "do not recommend more volume without measurement," yet the execution layer ships volume daily. Until the voice rebuild lands and posting rate plus engagement is measured, cut to 4 to 5 high-quality posts per week. Less slop posted under your name is itself a reputation gain.

---

## Finding 3: Proactivity is gated by your review bandwidth, not Eve's output

You said Eve does not feel proactive. The data says the opposite problem: weekdays generate roughly 25 to 30 Telegram messages and Sundays stack about 17 jobs. The June 8 brief recorded 0 outreach sends in 7 days while the pipeline kept producing drafts, and Mission Control shows 32 cron rows with stale red metadata that nobody clears. The system is extremely proactive at generating recommendations and extremely weak at converting them into completed loops, because every loop ends with "JT reviews this." When 25 messages a day each end that way, none of them get reviewed, which feels like Eve doing nothing.

**Fixes, ranked:**

1. **Replace the message firehose with one daily Send Queue.** One morning message, hard cap of 3 items, each a finished artifact with a link and a one-word reply to approve (send, post, skip). Everything else (news hooks, niche intel, reminders, research summaries) rolls into a single evening digest or stays in files and Mission Control. Reminders like reddit-karma, TikTok warmup x2, and Nash TikTok stop being standalone messages.
2. **Define three sanctioned autonomous lanes with full completion authority, no asking:** (a) content: draft, validate, upload to Drive, schedule in Notion, ready state; (b) prospecting: research through to a complete outreach packet (contact verified, hook written, draft done, Drive link) so your only action is send; (c) ops self-healing: cron fixes, zombie cleanup, cooldown recovery, file budget trims. Everything outside these lanes stays advisory. This is where to spend autonomy, not on raising tool-call caps everywhere.
3. **Merge the two night agents.** The 9:45 PM nightly-autonomous-leverage-agent does strategic work and the 3:20 AM Overnight Autonomy Agent's prompt literally says its job is to verify the 9:45 agent and remove one blocker with a 12-tool-call cap. That is two LLM sessions, two bootstrap loads, and a coordination protocol for what should be one agent with a two-phase prompt. Merge them, and raise the merged agent's budget to completing one full artifact per night inside the three lanes above.
4. **Execute the kill and merge list.** Delete 12 expired one-shot jobs still in jobs.json: 7 Catch-up jobs dated 2026-04-28, Review Stalled Projects (04-07), Codex harness reminder (05-09), Altmark follow-up check (05-15), reddit rerun check (05-24), plus the dead `content-generate (DISABLED)` job that still fails 5 of 5 runs and pollutes health metrics. Merge the duplicates: Passive Income Scout appears twice, Passive Income Strategist twice (4 Sunday passive-income jobs plus a fetch and a guard; one scout, one strategist, one guard is enough), two Health Check-ins both at 9 PM, Weekly Strategic Gut-Check and Weekly North Star Command Center both Sunday 6 PM, two TikTok warmup reminders. Decide consciously on the personal-growth and hobby jobs (Spanish daily plus weekly, Sports GM weekly, dynasty-replies daily, DynastyJig daily): they are fine if you want them, but each daily one is a bootstrap load and a message; weekly cadence likely serves the same purpose. Target: from 80 jobs to roughly 35 to 40. Fewer, deeper pipelines beat 80 shallow ones, and the OAuth pressure in Finding 1 drops with them.
5. **Alignment check against the North Star stack.** Consulting is your stated number 1 lane and gets maybe 12 to 15 of 80 jobs; content gets about 14; apps about 12; meta and ops about 15; zombies about 12. After the cuts, deliberately rebalance so the consulting pipeline (discovery, research, packet completion, follow-up state machine) is the deepest system Eve runs.

---

## Finding 4: Self-improvement exists but optimizes the wrong objective, and the patch mechanism is degrading the system

You asked whether Eve is optimally self-improving. Honest answer: the machinery is extensive (Kobe Protocol daily film review, weekly skills audit, monthly goal-skills gap, mistakes log with six required fields, autoresearch sweeps, regression checks) and it works, but almost everything it improves is operational reliability. Nothing measures whether the content got better, whether outreach reply rates moved, whether revenue-relevant loops closed faster. Eve is getting steadily better at not crashing and not measurably better at making you money.

Worse, the improvement mechanism is "append a dated hardening patch to the cron prompt." The Viral Swipe prompt now opens with seven patches from seven dates (05-07, 05-13, 05-29, 06-01, 06-02, 06-03, plus checkpoint rules) before the task even starts. Job Market Daily carries five. These prompts are now 2,000 to 4,000 word patch quilts where the creative or analytical task is buried under tooling caveats, which measurably worsens model performance and inflates every run's token bill.

**Fixes, ranked:**

1. **Move tooling rules out of prompts and into scripts.** Every "do not use heredocs," "use rg with || true," "parse JSON this way" patch is a deterministic rule that belongs in a wrapper script or pre/post-run validator, not in natural-language instructions a model can ignore. You already do this well in places (outreach_pipeline_runner, social_engagement_audit); finish the job. A cron prompt should be the task, the context files to read, and the output contract. Aim for under 600 words each.
2. **Institute a monthly prompt rewrite instead of perpetual append.** Once a month (fold into Weekly Systems Review on the first Sunday), rewrite the 5 most-patched prompts clean, incorporating lessons into structure rather than addenda, and version jobs.json prompts in git so regressions are diffable.
3. **Give self-improvement outcome KPIs.** Track weekly: posts delivered vs posted (your acceptance rate is the single best content-quality metric), engagement per posted item, outreach packets completed vs sent vs replied, consulting pipeline stage movement, cron delivery rate, dollars spent. Make the Weekly Systems Review report these six numbers and require the monthly gap analysis to propose changes against them, not against job-description keyword scans.
4. **Resolve the contradictory rules Eve re-reads every session.** AGENTS.md Core Rule 11 says Gemini Flash-Lite is the global default and elite tasks must spawn claude-sonnet-4-6 subagents; the Model Routing section in the same file says OpenAI OAuth is the default and forbids other providers in chains; openclaw.json says gpt-5.5. TOOLS.md says the Notion swipe cron runs 5:30 AM on "isolated sonnet" while the actual job runs 5:45 on the default model. Stale contradictory rules in bootstrap are noise the model must arbitrate on every single run. Rewrite Rule 11 (drop the Gemini default sentence, keep the Sonnet escalation principle as an approved standing exception), fix TOOLS.md, and add a cross-file consistency check for model references to the weekly review.

---

## Finding 5: Security and hygiene debt (moderate risk, cheap fixes)

1. **Exec is fully open while 80 jobs ingest untrusted content.** `exec.ask: off`, `security: full`, sandbox `danger-full-access`, approvals `never`, and dozens of jobs read web pages and X posts daily. Prompt injection from a malicious page is your main realistic attack vector, and your defenses against it are prompt-level instructions, which are the weakest kind. You cannot fully close this without losing the autonomy you want, but you can cut blast radius: keep the existing never-send and config-protection rules, and focus on the mitigations that actually bear load: loopback binds, fewer web-ingesting jobs, secret scanning, and separating untrusted-ingest sessions from sessions that write to Drive, Notion, or skills files. The first concrete split: the weekly intelligence job edits ICPs.md and the cold-email SKILL.md in the same session that ingests web content; have it write proposed edits to a staging file that a separate non-ingesting step applies. Gateway denyCommands adds little against unrestricted shell exec and should not be mistaken for a sandbox.
2. **n8n is listening on all interfaces** (`*:5678`), as are mission-control next (`*:3000`) and convex (`*:3210/3211`). Tailscale serve proxies localhost anyway, so bind all three to 127.0.0.1. Five-minute fix, removes LAN exposure.
3. **Possible secrets in memory files.** The scan flagged `apiKey` in memory/2026-02-21-model-routing.md and `encryptionKey` in memory/2026-02-23.md. Memory files get loaded into model context and shipped to providers. Verify whether these are values or just names, scrub values, and add memory/ to the existing key-pattern scanner.
4. **Audio transcription is set to Spanish** (`media.audio.language: "es"`). Useful for Spanish lessons, but it will mangle every English voice note you send Eve. Either remove the language pin (let it auto-detect) or scope it to the Spanish jobs.
5. **MEMORY.md is 23 bytes under its hard budget.** The live-update rule mandates same-turn writes, so every update now forces an emergency trim first. This is a recurring failure waiting to happen; the restructure in Finding 1.2 resolves it.
6. **Plugin warning:** duplicate lossless-claw plugin IDs (global overriding global). Clean the duplicate install under .openclaw/npm/projects.
7. **Internal contradiction to resolve:** the Telegram rule caps messages at 3,500 chars while the Morning Brief Nash contract demands the full X post plus full Reddit draft inline and forbids truncation. Pick one; I recommend Drive links plus first lines in the brief, full text in the Send Queue item.

---

## Ranked action plan

**Week 1: stop the bleeding (reliability and noise)**
1. Smoke-test, then approve and set fallback `moonshot/kimi-k2.6` for cron jobs; verify Moonshot billing once; fallback runs must name their model.
2. Add automated cooldown-bug recovery to the watchdog; fix the watchdog kickstart-failure loop.
3. Delete the 12 expired jobs and the dead content-generate job; merge the 5 duplicate pairs. Re-run cron list to confirm clean health metadata.
4. Back up and reset lcm.db (185MB, past your own 100MB threshold).
5. Bind n8n, next, and convex to 127.0.0.1. Fix audio language scope. Verify and scrub the two flagged memory files.
6. Stand up the Send Queue format and route reminders into the evening digest.

**Weeks 2 to 3: content rebuild (your top frustration)**
7. Build memory/jt-corpus.md from 15 to 25 posts you actually wrote or posted after editing.
8. Rewrite the two generator prompts clean: one post per run, 5 corpus exemplars inlined per draft, swipe file demoted to hook-mechanic only, ratio rule replaced with the first-person-proof rule, 2 of 5 weekly slots required to come from current-efforts or recent-builds.
9. Add the edit-delta capture step to the "posted" reply handler and make generators read the last 10 deltas.
10. Add the Sonnet final-pass via OpenRouter with a $10 per month named cap. Cut weekly volume to 4 or 5 posts until acceptance rate exceeds 60 percent.

**Week 4: structure (proactivity and self-improvement)**
11. Cut the bootstrap: MEMORY.md to an indexed under-8K file, TOOLS.md syntax into on-demand skills, total under 45K. Remove the ~70 redundant per-job model overrides. Rewrite AGENTS.md Rule 11 (drop the Gemini default, keep the Sonnet escalation) and fix the stale TOOLS.md references.
12. Merge the two night agents into one with completion authority inside the three sanctioned lanes.
13. Convert the top 5 most-patched prompts into clean task prompts plus wrapper scripts; put jobs.json under git; schedule the monthly prompt rewrite.
14. Add the six outcome KPIs to Weekly Systems Review and repoint the monthly gap analysis at them.
15. Rebalance the remaining ~35 to 40 jobs so consulting pipeline depth exceeds every other category.

## Expected effects

Finding 1 fixes should collapse the audit-window failure pattern (30 of 80 jobs with repeat failures, almost all auth-cooldown) and cut daily token consumption 40 to 50 percent, which also relieves the OAuth rate limiting that caused the failures. Judge this by the 7-day delivery-rate baseline taken in Phase 1 and recomputed a week after the fallback lands, not by cron status snapshots, which have proven unreliable in both directions. Finding 2 changes attack the actual mechanism behind the AI-slop problem rather than adding a ninth rule to a blocklist; the acceptance-rate metric will tell you within three weeks whether it worked. Finding 3 turns 25 to 30 daily messages into one decision queue and one digest, which is the only realistic way your review minutes convert into sends and posts. Findings 4 and 5 are cheap insurance and compounding maintenance.

One closing pushback, since you prefer it straight: the instinct to fix this by making Eve more autonomous is half right. Autonomy inside the three artifact-producing lanes, yes. But the system's real constraint for the last month has been that its single most valuable consumer, you, was handed 30 messages a day and 0 outreach got sent. Build the system around your 15 minutes, not around Eve's capacity to generate.
