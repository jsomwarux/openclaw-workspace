# Regression Checks — Mistake Prevention Index

Purpose: turn repeated mistakes into concrete checks. A correction is not complete until the prevention rule is tied to an executable or reviewable check.

## Rule
Every operational mistake entry must include:
1. Failure — what happened
2. Root cause — why the system allowed it
3. Guardrail — what changed to prevent recurrence
4. Regression check — how we will detect this failure if it returns
5. Owner surface — the file/prompt/script/cron/skill that must enforce it
6. Verification — date or command proving the guardrail is in place

If a correction cannot name a regression check, it is only a note, not a fix.

## Active Checks

| Failure Pattern | Regression Check | Owner Surface | Cadence | Status |
|---|---|---|---|---|
| Cron timeouts silently repeat | Cron health review flags `consecutiveErrors >= 2`, `lastRunStatus=error`, or duration near timeout; timeout is resized based on full expected runtime, not a blind 50% bump. | HEARTBEAT.md cron health section | Every heartbeat | active |
| Generic cost alerts repeat without diagnosis | Cost alert handler must run supported diagnostics (`scripts/cost-tracker.py --check-runaway` plus `--snapshot`/`--weekly-review` as needed) before repeating generic spend alerts; `--diagnose` is not supported. | TOOLS.md Cost Tracker + HEARTBEAT cost check | Every cost alert | active |
| Outreach generated from stale data | Before outreach drafts, validate company status and prospect role via live web/search. | AGENTS.md outreach rules + cold-email/pipeline skills | Every outreach draft | active |
| Content violates JT voice corrections | Content agents must read `memory/content-voice.md` / `memory/FEEDBACK-LOG.md` and run audit checklist before drafting. LinkedIn drafts must also pass `python3 scripts/content_distribution_guard.py --linkedin-draft [draft-file]` before delivery. Guard must fail “not X, it’s Y,” “not X but Y,” and “X is not just Y. It is Z.” variants. | Content rules + `scripts/content_distribution_guard.py` | Every content draft; every LinkedIn draft gets executable stale-pattern scan | active |
| Bootstrap files exceed budgets | `wc -c` on bootstrap files before append and at session start; trim/archive before adding. | AGENTS.md Budget Rule | Every session/append | active |
| Mission Control tasks are vague | Task descriptions must include first action, why it matters, and done state. | AGENTS.md Task Descriptions rule | Every task creation | active |
| New recurring agent/skill lacks scoreable improvement loop | Run autoresearch candidacy check and enroll if it is repeated, scoreable, and has clear failure modes. | docs/agents/autoresearch-rules.md + targets.md | Skill/agent creation + weekly audit | active |
| Fix logged but not enforced where failure occurred | Mistake entry must name owner surface and update that file/prompt/script/cron in same turn. | AGENTS.md Correction Loop + this file | Every correction | active |
| Active Telegram message stalls behind maintenance/tool chains | If JT sends a live message, especially "are you there?", status checks, or live ops/debug questions, send a visible ack before any tool calls and keep ≤4 tool calls between visible replies. Heartbeat/proactive work is blocked until the active exchange is answered. | AGENTS.md Core Rules 9/9b/10 + this file | Every active Telegram turn | active |
| Cron reports `ok` but user-visible delivery failed | Critical user-facing crons must verify latest run `deliveryStatus`/`deliveryError` with `openclaw cron runs`, not just `lastRunStatus` or state files; resend manually if delivery failed. | HEARTBEAT.md cron health + Spanish delivery check + this file | Every heartbeat for critical failures; daily for Spanish | active |
| Duplicate heartbeat daily-note entries | Before appending, check whether the exact `## Heartbeat HH:MM` section already exists; suppress duplicate entries within 5 minutes unless state changed. | HEARTBEAT.md Heartbeat Log Idempotency Rule + daily notes | Every heartbeat + 10AM film review | active |
| Stale sources framed as fresh content intel | Any content draft with "this week/today/new/fresh" or market-stat language must verify source date within 14 days, or explicitly label older context with date; unknown date means cut the stat. | docs/agents/content-rules.md + weekly content/intel prompts | Every content draft using external claims | active |
| Weekly content audit passes without platform-specific reference mechanics | `python3 scripts/content_calendar_audit.py --week YYYY-MM-DD` must call `content_distribution_guard.py` with `--require-reference-map linkedin` and `--require-reference-map x`, so generic “Notion swipe references checked” cannot pass as healthy weekly generation. | `scripts/content_calendar_audit.py` + `scripts/content_distribution_guard.py` + content generation cron payloads | Every weekly content audit and content cron patch | active |
| @dynastyjig content becomes generic aphorisms | Sports GM/autoresearch must verify @dynastyjig packs include `Native pattern teardown`, `Rejected generic patterns`, 3/5 current player/news/market-specific posts, and draft-to-native-syntax/rhythm mapping; fail closed when fresh signal is thin. | skills/sports-gm/SKILL.md + Daily DynastyJig cron + agents/autoresearch/checklists/sports-gm.md | Weekly autoresearch + any sports content patch | active |
| Spanish lesson cron state update fails after delivery | After Spanish Daily Lesson runs, verify latest run delivery fields and run `python3 scripts/spanish_state_check.py --date YYYY-MM-DD --require-today`; if delivery succeeded but state update/artifact validation failed, patch state manually and update cron prompt/tool rule. | Spanish Daily Lesson cron payload + `scripts/spanish_state_check.py` + `spanish/state.json` + `agents/autoresearch/checklists/spanish-daily-lesson.md` | Daily lesson delivery check + heartbeat on errors | active |
| Paused Spanish lessons trigger stale-state alerts | If `spanish/state.json` has `"paused": true`, `python3 scripts/spanish_state_check.py --max-age-days 2` and `--require-today` must return `ok` with `paused:true` after validating required fields and date sanity, without requiring a fresh lesson. | `scripts/spanish_state_check.py` + `spanish/state.json` + HEARTBEAT Spanish checks | Every 10AM/10PM Spanish heartbeat check while paused | active |
| Cron task checks fail after useful work because of inline Python/heredocs | Research/ops crons must use existing script files, `rg`, `jq`, or simple shell checks for Mission Control and verification work. Mission Control duplicate checks/task creation must use `scripts/mission_control_task_gate.py`, not `fetch /api/tasks -> inline Python` or heredoc parsing. | Cron payloads + relevant agent prompts + `scripts/mission_control_task_gate.py` | Every cron-health fix and 10AM film review | active |
| Cron duplicate checks fail because a no-match search is treated as an error | Duplicate/non-actionable checks against known files must use non-fatal shell search (`rg ... || true`) or a purpose-built script, then interpret empty output as "not found" instead of a failed run. Do not use agent search tools for expected no-match checks. | Job Market Daily cron payload + `/Users/jtsomwaru/projects/job-market-agent/CLAUDE.md` + similar research cron prompts | Every cron-health fix and 10AM film review | active |
| Job-market live-posting checks fail after useful work because expired postings exit nonzero | Live-posting verification for market-intel/expiry classification must use `scripts/verify-live-posting.py --soft-exit` or explicit non-fatal handling, then route `ok:false` as expired/blocked instead of a cron failure. Strict nonzero verifier exit is reserved for apply/package gating. Never run the verifier without an explicit posting URL. | `/Users/jtsomwaru/projects/job-market-agent/scripts/verify-live-posting.py` + `/Users/jtsomwaru/projects/job-market-agent/CLAUDE.md` + daily brief template + Job Market Daily cron payload + Weekly Systems Review cron payload | Every job-market or systems-review cron-health fix and 10AM film review | active |
| Cron KB commands fail because `bun kb.ts` runs from the wrong directory | Knowledge Base commands must run from `~/.openclaw/workspace/knowledge` (`cd .../knowledge && bun kb.ts ...`) or a wrapper script. Bare `bun kb.ts` from workspace root or an agent run directory is invalid; rerun cwd/path failures from the knowledge directory before marking the cron unhealthy. | Skills & API Researcher cron payload + `agents/skills-researcher/AGENT.md` + `knowledge/kb.ts` | Every skills/API cron-health fix | active |
| Cron web-search freshness checks fail because `BRAVE_API_KEY` is not loaded | Any cron using `scripts/web_search.py` must source `~/.config/env/global.env` in the same shell command before running the script, retry `WEB_SEARCH_ERROR` once with that env-sourced command, and treat empty result sets as `SKIP_SLOT`/content-quality signals rather than tool failures. | Reddit Karma Daily cron payload + `scripts/web_search.py` + similar content cron prompts | Every content cron-health fix and 10AM film review | active |
| Nightly Leverage repeats same blocker as a fresh win | Before a Nightly Leverage report is sent, the cron prompt must compare the last 2 nightly runs, name a `Material delta`, and suppress/rotate if the same client/project/blocker appears twice with no new external input or verification evidence. | `nightly-autonomous-leverage-agent` cron payload + `memory/audits/xhigh-systems/2026-05-29-nightly-leverage-anti-repeat-audit.md` | Every nightly leverage run + 10AM film review after reports | active |
| Passive-income build ideas fail to populate Passive $ / MC | After strategist runs, verify `/api/passive-income` shows each 🟢 idea with non-empty `concept`, no `ALREADY QUEUED` duplicate cards, and exactly one active `[PI] Build:` task with `project=passive-income` for each 🟢 idea. | `mission-control/app/api/passive-income/route.ts` + `agents/autoresearch/checklists/passive-income-strategist.md` | Weekly strategist run + weekly autoresearch | active |

## Daily Film Review Add-on
During 10AM film review, check yesterday's corrections:
- Did each correction include a guardrail and regression check?
- Was the owner surface updated, not just a memory note?
- Did any failure pattern repeat within the last 14 days?

If any answer is no, write one targeted fix before ending the review.

## Weekly Review Add-on
During weekly systems review, scan recent daily notes + mistakes log for repeated terms: `mistake`, `missed`, `stale`, `timeout`, `hallucinated`, `duplicate`, `failed`, `incorrect`.

If a pattern appears twice in 14 days, promote it to an Active Check above and update the owner surface.

## Niche Fitness Review Check
Before any monthly niche fitness review is sent, verify the report includes:
- `Recent Context Applied` with last-48-hour strategic updates and their scoring impact.
- `Proof Proximity` and `GTM Traction` columns in both score tables.
- A `Reality Adjustment` section explaining where recommendations differ from raw score.
- An operational decision summary: Primary / Adjacent expansion / Hold-test / Strategic proof lane.
If any element is missing, do not send the review; update `agents/niche-fitness/AGENT.md` output and regenerate.

## Job Posting Apply Route Freshness Check
- **Trigger:** Before surfacing any job as `apply` or `both`, or before creating application materials/tasks.
- **Check:** Verify the live posting UI/ATS still accepts applications and does not show removed/closed/expired language. Do not rely on cached aggregator JD text or HTTP 200 alone.
- **Failure action:** Set role status `expired`, route `market-intel`, close any application MC task, and log the stale source.
- **Owner surface:** `~/projects/job-market-agent/CLAUDE.md` + `knowledge/scoring-criteria.md`.
- **Added:** 2026-05-11 after Ridgeline stale apply-route failure.

## Active Check — Reddit daily stale frame prevention
- **Scope:** `reddit-daily-gen` cron (`bbe49024-458a-4496-9c7c-7a278615810f`).
- **Check:** For the next 3 runs after 2026-05-11, verify outputs against `memory/content/reddit-draft-log.jsonl` and prior cron run summaries. Crypto must not repeat generic narrative/mechanism/protocol durability/stakeholder alignment frames without a fresh 48h source. Fantasy must not repeat roster-window/value/liquidity/calculator advice without a concrete current thread type.
- **Pass condition:** Repeated/stale slots become `SKIP_SLOT` or are grounded in a fresh named signal.
- **Owner surface:** Cron payload + `memory/content/reddit-strategy.md`.

## Active Check — Crypto Morning Explicit Delivery
- **Failure covered:** Crypto morning files generated but JT does not receive/notice actual portfolio recommendation while cron metadata says delivered.
- **Check cadence:** Daily 10AM heartbeat after crypto window.
- **Check:** For `eve-crypto-morning-008`, verify latest run final summary includes explicit `telegram_message_sent=true` and `summary_text`, or manually inspect `/Users/jtsomwaru/projects/crypto-agent/data/telegram-summary.txt` and resend it via Telegram.
- **Do not trust:** `lastRunStatus=ok` or `deliveryStatus=delivered` alone.
- **Owner surface:** cron payload for `eve-crypto-morning-008` and `HEARTBEAT.md` missed-cron/delivery checks.
- **Recovery:** resend `telegram-summary.txt` to JT, then patch cron if explicit send requirement is absent.
- **Last verified:** 2026-05-11 — cron payload patched and manual resend succeeded.

## Active Check — Crypto Morning X Research Allocation Gate
- **Failure covered:** Crypto Morning allocation delivered without fresh X/API research, relying on prices/web/whale data while treating X as skippable for cost.
- **Check cadence:** Every Crypto Morning full-analysis before allocation scoring and again before Telegram send.
- **Check:** Run `python3 /Users/jtsomwaru/projects/crypto-agent/scripts/x-research-guard.py --max-age-hours 3`; it must verify fresh `data/x-research-latest.json` with one entry for `__NARRATIVE__` plus every ticker in `data/portfolio.json`, and no failed X commands.
- **Failure action:** Do not send allocation. Send JT `⚠️ Crypto analysis incomplete — X research failed/stale: [reason]`.
- **Owner surface:** `eve-crypto-morning-008` cron payload, `/Users/jtsomwaru/projects/crypto-agent/CLAUDE.md`, `scripts/run-x-research.py`, `scripts/x-research-guard.py`, `config/settings.yaml`.
- **Last verified:** 2026-05-14 — full X pass 20/20 commands succeeded; guard passed with portfolio coverage 20/20.

## Active Check — LinkedIn Semantic Topic Cooldown
- **Failure covered:** Weekly/daily content recommends the same LinkedIn idea in new wording because older manually posted rows are not marked `posted=true` and exact-text duplicate checks miss semantic repeats.
- **Check cadence:** Every content reminder before delivery and every weekly content generation audit.
- **Check:** `scripts/content_distribution_guard.py --weekly memory/content/weekly-YYYY-MM-DD.md --check-notion-script` must scan current/future weekly sections against `memory/content/posted-log.jsonl` topic clusters over a 45-day cooldown, regardless of `posted` flag.
- **Failure action:** Do not deliver the repeated post. Replace with a fresh current-effort/trend-backed slot or send a regeneration blocker.
- **Owner surface:** `scripts/content_distribution_guard.py`, content reminder cron, Sunday content cron, `docs/agents/content-rules.md`.
- **Last verified:** 2026-05-14 — repeated Agentforce boundary slot failed, replacement passed guard + content calendar audit.

## Active Check — Morning Brief Nash Full-Draft Delivery
- **Failure covered:** Morning Brief summarizes Nash X/Reddit drafts or only gives a saved file path instead of delivering usable post copy.
- **Check cadence:** Every Morning Brief with Nash content.
- **Check:** Final brief must include full Daily X Post text and full Reddit draft with subreddit/rationale, title, and body. Cron payload must include `NASH DELIVERY CONTRACT`.
- **Failure action:** Regenerate/resend the Nash section inline; shorten lower-priority sections first if needed.
- **Owner surface:** `HEARTBEAT.md` Morning Brief section + `eve-morning-brief-001` cron payload.
- **Last verified:** 2026-05-14 — HEARTBEAT and cron payload patched.

## Portfolio/site deploy inventory diff
- **Trigger:** Any jtsomwaru.com Work/App/Client Outcomes restructuring or portfolio-card deploy.
- **Check:** Compare previous visible cards to proposed visible cards. Every removed or renamed proof asset must be labeled `approved removal`, `anonymized rename`, or `blocked pending proof`. Client-name anonymization must still keep JT's expected work visible in a recognizable proof bucket.
- **Fail condition:** A live app/project disappears from visible Work/App sections without explicit JT approval, or paid client work becomes invisible because it was only renamed generically.
- **Owner surface:** portfolio-card/site-update workflow.

## Client outcome attribution check
- **Trigger:** Any portfolio/site deploy or answer involving client-work ownership, public proof, metrics, or case-study attribution.
- **Check:** For every client outcome card or claim, verify `project slug -> actual client -> source file -> public label`. Accepted sources: `memory/clients/*/status.md`, proposal extracts, acceptance checklists, or current project source data when it explicitly names the client.
- **Fail condition:** Claiming a client owns work based on generic/anonymized labels, or changing public labels without preserving an internal mapping.
- **Owner surface:** portfolio-card/site-update workflow and client proof pipeline.

## Public proof privacy grep check
- **Trigger:** Any site, LinkedIn, outreach, portfolio, Drive-shareable, or public content update that references client work, proposals, paid work, or metrics.
- **Check:** Grep public/shareable files for real client names and exact proposal/deal amounts before publishing. Default labels must be anonymized by role/segment/city. Exact amounts require an explicit approval note from JT.
- **Fail condition:** Public copy contains unapproved client names, private stakeholder names, proposal totals, deposit amounts, or exact use-case prices.
- **Owner surface:** portfolio-card workflow, high-stakes draft review, site deploy workflow, client proof pipeline.

## ReelFarm Intel calibration check
- **Trigger:** Any ReelFarm/App Marketing OS TikTok slideshow intel, hook recommendation, settings review, or synthesis from external trend/newsletter sources.
- **Check:** Read `memory/reelfarm/calibration-2026-05-27.md`. Verify every recommendation uses `Medium - hypothesis` unless the account has 20+ normal-distribution posts, applies the Automation B screenshot-demo slotting test, uses Vista/Nash Satoshi/Glow Index proper casing, avoids trend-locked and viewer-interactive hooks, favors declarative hooks over questions, and surfaces cross-source convergence as its own finding.
- **Fail condition:** "High confidence" appears without real post-performance data, a non-screenshot walkthrough hook is assigned to Automation B, app names are all-caps, or static slideshow hooks require trend audio/video context or viewer interaction.
- **Owner surface:** ReelFarm review checklist, App Marketing OS optimization rules, ReelFarm strategy baseline.

## LinkedIn posted-log finalization check
- **Trigger:** Every `content-generate-linkedin` weekly run before it announces the LinkedIn queue is ready.
- **Check:** `memory/content/posted-log.jsonl` must contain one `platform=linkedin` row for every LinkedIn slot in the current weekly file, with `source_weekly` set to that file and `posted=false`. Run a pending-state dry run for the next eligible reminder date with both `--platform linkedin --platform x`.
- **Fail condition:** The weekly file or Notion has LinkedIn copy, but `posted-log.jsonl` has zero matching rows. Treat this as a blocker because reminders and posted-reply logging will drop LinkedIn.
- **Owner surface:** `content-generate-linkedin` cron payload, content reminder flow, posted-log hygiene.

## Current content niche-map check
- **Trigger:** Any content-generation prompt, swipe-file backfill, LinkedIn creator-corpus task, or content-system health claim.
- **Check:** Verify the workflow loads `memory/content/current-niche-map.md` and selects from its priority order. Default LinkedIn lanes must come from Tier 1/Tier 2: SMB AI Implementation, Property Management Operations, NYC SMB Operations, Wholesale Distribution Operations, Construction + Skilled Trades Operations, Insurance/Agentforce Operations, AI Operating Systems, AI Enablement/Solutions Architecture, and Productized Services.
- **Fail condition:** Claude Code, Vista, Glow Index, Nash Satoshi, App Marketing, Generic AI Agents, Personal Brand, or shorthand aliases like AI Consulting/NYC SMB are treated as the saved/default niche instead of exact canonical lanes or explicit secondary/product/tool lanes.
- **Command:** New weekly files must pass `python3 scripts/content_distribution_guard.py --weekly memory/content/weekly-YYYY-MM-DD.md --require-reference-map linkedin --require-reference-map x --check-notion-script`; the guard must fail non-canonical `Niche:` values in reference mechanics.
- **Owner surface:** `docs/agents/content-rules.md`, `memory/content-voice.md`, `memory/content/current-niche-map.md`, content-calendar agent, content-generation skill, and Notion swipe tooling.
