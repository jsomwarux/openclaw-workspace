# Mistakes Log — Recent Entries
> Source: AGENTS.md §Mistakes Log
> Full archive: docs/agents/mistakes-log.md

## Logging Rule
Every entry MUST have six fields: (1) specific failure, (2) root cause one level deeper than "I forgot," (3) concrete guardrail/rule, (4) regression check that would catch recurrence, (5) owner surface updated, (6) verification/date. A mistake entry without a regression check + owner surface is incomplete — finish it before moving on. Reference: `docs/agents/regression-checks.md`.

## Recent Entries (2026-04)

| Date | Mistake | Fix |
|------|---------|-----|

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
