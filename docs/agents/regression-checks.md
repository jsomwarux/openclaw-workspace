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
| Content violates JT voice corrections | Content agents must read `memory/content-voice.md` / `memory/FEEDBACK-LOG.md` and run audit checklist before drafting. | Content rules + content skills | Every content draft | active |
| Bootstrap files exceed budgets | `wc -c` on bootstrap files before append and at session start; trim/archive before adding. | AGENTS.md Budget Rule | Every session/append | active |
| Mission Control tasks are vague | Task descriptions must include first action, why it matters, and done state. | AGENTS.md Task Descriptions rule | Every task creation | active |
| New recurring agent/skill lacks scoreable improvement loop | Run autoresearch candidacy check and enroll if it is repeated, scoreable, and has clear failure modes. | docs/agents/autoresearch-rules.md + targets.md | Skill/agent creation + weekly audit | active |
| Fix logged but not enforced where failure occurred | Mistake entry must name owner surface and update that file/prompt/script/cron in same turn. | AGENTS.md Correction Loop + this file | Every correction | active |
| Cron reports `ok` but user-visible delivery failed | Critical user-facing crons must verify latest run `deliveryStatus`/`deliveryError` with `openclaw cron runs`, not just `lastRunStatus` or state files; resend manually if delivery failed. | HEARTBEAT.md cron health + Spanish delivery check + this file | Every heartbeat for critical failures; daily for Spanish | active |
| Duplicate heartbeat daily-note entries | Before appending, check whether the exact `## Heartbeat HH:MM` section already exists; suppress duplicate entries within 5 minutes unless state changed. | HEARTBEAT.md Heartbeat Log Idempotency Rule + daily notes | Every heartbeat + 10AM film review | active |
| Stale sources framed as fresh content intel | Any content draft with "this week/today/new/fresh" or market-stat language must verify source date within 14 days, or explicitly label older context with date; unknown date means cut the stat. | docs/agents/content-rules.md + weekly content/intel prompts | Every content draft using external claims | active |
| @dynastyjig content becomes generic aphorisms | Sports GM/autoresearch must verify @dynastyjig packs include 3/5 current player/news/market-specific posts and fail closed when fresh signal is thin. | skills/sports-gm/SKILL.md + Daily DynastyJig cron + agents/autoresearch/checklists/sports-gm.md | Weekly autoresearch + any sports content patch | active |

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
