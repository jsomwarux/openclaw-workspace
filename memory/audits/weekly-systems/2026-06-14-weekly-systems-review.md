# Weekly Systems Review - 2026-06-14

## North Star Scoreboard
- Current June collected: $5,575.
- Pipeline-weighted forecast: $4,057.50.
- Gap to $10K collected: $4,425.
- Gap to $10K including weighted forecast: $367.50.
- Primary next-dollar gate: Yair/Altmark rent delinquency inputs and approval packet.

## Pipeline Stage Movement
- Altmark rent delinquency remaining: active, $2,250 value, waiting on client since 2026-06-11.
- Altmark DHCR lease renewal phase 1: proposal, $3,500 value, waiting on client for 18 days; intentionally held behind rent delinquency.
- Aya StreetEasy scraper: closed/cancelled per 2026-06-11 correction.
- Aya co-living dashboard: closed/dead currently per 2026-06-11 correction.
- Aya acquisitions dashboard: lead only; revive only on a fresh trigger.
- Petri, HPM, Superior follow-ups: contacted, no reply to M1, waiting 13 days; M2 follow-up task already active.

## Waiting-On Items Older Than 7 Days
- Altmark DHCR lease renewal phase 1: waiting_on=client, 18 days.
- Petri Plumbing follow-up: waiting_on=prospect, 13 days.
- HPM follow-up: waiting_on=prospect, 13 days.
- Superior Plumbing follow-up: waiting_on=prospect, 13 days.

## Phase 7 KPI Numbers
1. Posts delivered vs posted: 11 content drafts delivered/scheduled for 2026-06-08 to 2026-06-14; 2 posts confirmed live in metrics/registry.
2. Engagement per posted item: Glow TikTok 492 views, 3 likes, 0 comments/saves/reposts; Nash X 40 impressions, 0 likes/comments/reposts. Average: 266 views/impressions and 1.5 interactions per posted item.
3. Outreach packets completed vs sent vs replied: 3 M2 follow-up drafts completed for Petri/HPM/Superior; 0 confirmed M2 sends; 0 replies. Current source also shows 3 M1 sends on 2026-06-01 with no replies.
4. Consulting pipeline movement: Altmark remains the cash gate; Aya scraper/co-living were moved to closed/dead; NYC property-management lookalike list and M2 follow-up drafts exist but sends/acceptance remain pending.
5. Cron delivery rate: last 7 days strict requested/unknown view = 60 delivered / 88 requested-or-unknown outcomes = 68.2%. Excluding unknown metadata: 60 delivered / 63 delivered-or-failed = 95.2%. All-run view: 174 ok / 251 finished = 69.3%.
6. Dollars spent: OpenClaw/OpenRouter-estimated 7-day spend $1.357; X API this week $10.24; combined weekly tracked spend $11.60. Month real API spend $4.43 / $50 target; X API month $24.05.

## Cron Health Audit
- Live jobs checked from `openclaw cron list`: 49 enabled jobs shown.
- Error status jobs:
  - `39435f7a-1102-49f0-8eec-4f7e0c38e7d5` passive-income-scout: latest error was "Codex stopped before confirming the turn was complete"; delivery not requested; useful work may exist but state was not confirmed.
  - `f96cc24f-55e6-4064-a075-b897156a22f2` AI Ops Teardown Weekly Draft: latest error was "Codex stopped before confirming the turn was complete"; delivery not delivered.
  - `870bf3ff-55c9-49c0-9970-361c81a0920b` vibe-marketing-generate: latest error included failed `scripts/nash_rankings_probe.py` plus stopped-before-confirming; delivery not delivered.
  - `008a349c-af59-4e6b-88bb-97f65dba61c6` Sports GM Weekly Market Report: latest error was no available `openai-codex` auth profile; delivery status unknown.
- No timeoutSeconds fields were present for the four erroring jobs, so no timeout bump was applied.
- Sunday 10AM conflict: Weekly Systems Review at 10:00 and Pending Task Processor at 10:30; no direct same-minute conflict.
- Never-ran jobs: `openclaw cron list` shows one future one-off YouTube TV reminder with no last run. `jobs.json` contains legacy/disabled-looking entries, so live list was treated as runtime truth.
- Cron volume: `scripts/cron_volume_guard.py` passed its relaxed guard with 49 enabled jobs, 198.46 estimated weekly invocations, 28.35 average daily invocations, and 24.35 agent-turn daily average. This still exceeds the stricter 20/day user cap and needs pruning or an explicit exception.

## File Budget Check
- AGENTS.md: 27,105 / 28,000 chars.
- MEMORY.md: 6,996 / 20,000 chars.
- TOOLS.md: 5,168 / 16,000 chars.
- HEARTBEAT.md: 4,189 / 16,000 chars.
- No bootstrap file is over budget. AGENTS.md is close enough to avoid casual appends.

## Process Health
- Gateway reachable by `openclaw status`, LaunchAgent loaded and running, pid 53174.
- Gateway node RSS sample: 594 MB, CPU 0.6%. This is above the 500 MB flag threshold but not CPU-runaway.
- Other notable node processes: n8n 252 MB; Codex app server 185 MB; Convex 94 MB; Mission Control Next 49 MB.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.

## LaunchAgent Config Review
- Gateway LaunchAgent label: `ai.openclaw.gateway`; ThrottleInterval: 10.
- Watchdog LaunchAgent label: `com.openclaw.gateway-watchdog`; StartInterval: 600.
- Config is within expected bounds.

## OpenClaw Version
- Current: OpenClaw 2026.5.28 (e932160).
- Version search result: GitHub releases show 2026.6.5-beta.1 published; GitHub repo updated recently. No stable update was installed. Existing OpenClaw runtime-update task remains the approval path.

## Plugin Audit
- `~/.claude/settings.json`: `context-mode@context-mode` is `false`.
- `~/.openclaw/extensions/`: `.openclaw-install-backups` and `lossless-claw`.
- Runtime warning persists: duplicate lossless-claw plugin id detected; global plugin overridden by global plugin path. No unexpected extension directory found, but duplicate warning should stay on radar.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL, 4 records.

## Weekly Maintenance Split
- Autoresearch enrollment: enrolled `ai-seo` because it was modified in the last 7 days, repeated, scoreable, and not registered. Added `agents/autoresearch/checklists/ai-seo.md` and target row in `agents/autoresearch/targets.md`.
- Future signals review: no active signal trigger met. Passive-income queue remains gated behind Altmark proof/consulting revenue or distribution signal; PostBridge/ViewTrack/Virlo/Remotion remain gated by actual posting consistency/revenue.
- Passive-income idea queue pruning: 9 `[PI]` tasks found at sortOrder >= 500, oldest 35 days; none reached the 60-day pruning threshold. No task was pruned or promoted.
- Weekly cost review: 7-day spend $1.357; gpt-5.5 drove 87% of tracked estimate. X API weekly spend is $10.24 and over the $10 target.

## Issues Fixed This Run
- Enrolled `ai-seo` into autoresearch with a six-question checklist.
- Created Mission Control task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` (`j57bd8z6jjnvyq7tg8hdtyhf2988n25a`).

## Needs JT Attention
- Send Yair/Altmark approve-edit packet; this is still the highest-value blocker.
- Send or skip Petri/HPM/Superior M2 follow-ups; drafts exist and replies are still zero.
- Decide whether the stricter 20/day cron invocation cap should override the executable cron guard threshold, because current agent-turn average is 24.35/day.
- Approve/decline OpenClaw update timing separately; no update was applied.

## Deferred / Not Fixed
- Did not rewrite cron prompts; outside the first-Sunday prompt rewrite ritual and needs approval for broader cron behavior changes.
- Did not rerun failed jobs solely to clear status.
- Did not alter auth/model config.

## Next Review
- 2026-06-21.
