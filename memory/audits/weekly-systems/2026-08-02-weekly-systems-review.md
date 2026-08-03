# Weekly Systems Review - 2026-08-02

## North Star Opening

- Scoreboard: $5,575 collected; $4,425 gap to $10K collected; weighted forecast $5,400; forecast-adjusted gap $0; 5 pipeline records; 2 aging items.
- Stage movement: MSI engagement is signed/in delivery; kickoff invoice cleared 2026-07-28; remaining $5,400 waits on completion/acceptance.
- Waiting-on older than 7 days:
  - Altmark rent delinquency remainder: blocked, $2,250, waiting on client since 2026-07-16.
  - DHCR Lease Renewal Phase 1 deposit: pending, ~$1,750, waiting on client since 2026-07-16.

## Phase 7 KPI Numbers

1. Posts delivered vs posted: 0 delivered/queued local posted-log entries dated 2026-07-27 through 2026-08-02; 0 posted confirmations. Source: `memory/content/posted-log.jsonl`. Gap: actual platform engagement requires manual/public URL capture.
2. Engagement per posted item: unknown; no same-week posted URLs or engagement artifacts in local state. Fix: capture public URLs and engagement metrics in posted-log when JT confirms posts.
3. Outreach packets completed vs sent vs replied: 0 packet artifacts found in same-week outreach paths; sends/replies unknown because no same-week outreach send log source was found. Fix: enforce `scripts/outreach_update.py` for every JT-confirmed send.
4. Consulting pipeline stage movement: MSI moved/confirmed signed delivery with kickoff cleared on 2026-07-28; Altmark and DHCR remain client-waiting from 2026-07-16.
5. Cron delivery rate: 13 jobs checked; 12 last-run ok, 1 stale last-run error; 4/4 announce jobs delivered; 9 delivery-not-requested jobs.
6. Dollars spent: OpenRouter billing delta $0.990737 from 2026-07-27 to 2026-08-02 snapshots; X API $0 from `memory/costs/x-api.jsonl`. Weekly model cost review total: $0.673.

## Cron Health

- Jobs checked: 13 enabled jobs.
- Current issue: Weekly Systems Review itself has stale `lastRunStatus:error`, `consecutiveErrors:6`, and latest stored failure from 2026-07-27: `run openclaw cron (agent)` pseudo-command failure.
- This live run got past that failure, but the required pinned command path is now stale: `/opt/homebrew/Cellar/node@22/22.22.2_2/bin` fails OpenClaw with `Node.js >=22.22.3 <23, >=24.15.0 <25, or >=25.9.0 is required`.
- Workaround verified: prefixing Node 26.5.0 before the stale Node 22 path allows `openclaw cron list`, `openclaw status`, and `openclaw --version` to run.
- No jobs are within 10% of timeout.
- No jobs with missing `lastRunAtMs`.
- Invocation cap: Sunday 12 scheduled invocations; weekdays 6-7/day; under the 20/day cap.

## File Budgets

- `AGENTS.md`: 27,806 / 28,000 chars. Under budget but tight; next append should extract before adding.
- `MEMORY.md`: 6,943 / 20,000 chars.
- `TOOLS.md`: 5,278 / 16,000 chars.
- `HEARTBEAT.md`: 4,189 / 16,000 chars.

## Process Health

- Gateway reachable and healthy under Node 26: pid 22648, active, loopback reachable in 28ms.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- Gateway process is above the RAM watch threshold: ~529MB RSS with long uptime. CPU was low. Flag for monitoring, not restart.
- Two high-CPU Node processes appeared from the active cron run itself and were only seconds old, so not classified as runaway.

## LaunchAgent Config

- `ai.openclaw.gateway`: `ThrottleInterval=10` - OK.
- `com.openclaw.gateway-watchdog`: `StartInterval=600` - OK at the limit.

## Version

- Installed: OpenClaw `2026.7.1-2 (0790d9f)`.
- Latest release found: `v2026.7.1`, GitHub release published 2026-07-13.
- Update available: no clear release-tag update. Local build suffix is newer than the public tag.
- Source: `https://github.com/openclaw/openclaw/releases/tag/v2026.7.1`.

## Plugin Audit

- `~/.claude/settings.json`: `context-mode@context-mode` is `false`.
- `~/.openclaw/extensions/`: only `lossless-claw` plus `.openclaw-install-backups` seen.
- OpenClaw config warning persists: duplicate `lossless-claw` plugin id; status also reports shared SQLite conflicting plugin install metadata for `brave`, `codex`, and `lossless-claw`.

## Critical File Integrity

- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: exists.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL.

## Maintenance

- Autoresearch enrollment: no `SKILL.md` or `AGENT.md` files modified in the last 7 days; no new enrollment.
- Future signals: no active signal graduated. The dated `jtsomwaru.com Deferred Conversion Rows - 30-Day Park` trigger was checked on 2026-08-02 but did not meet its conditional gates.
- Passive-income queue pruning: Mission Control reachable; 251 tasks loaded; 0 todo `[PI]`/`Build idea:` tasks with sortOrder >=500, so nothing pruned/promoted.
- Weekly cost review: total 7-day spend $0.673; gpt-5.5 $0.544; unknown $0.129; Claude Sonnet $0.000. Monthly pace $0.58 vs $50 target.
- Prompt rewrite ritual: proposal files saved under `docs/audits/prompt-rewrites/2026-08-02/`; no prompts installed.
- Convex instance-secret check: no current evidence that local Convex can move `--instance-secret` out of argv without changing runtime approach; keep redaction guard and do not change runtime config without JT approval.

## Issues Fixed This Run

- Created Mission Control task `j571gbnxsn6h535tkak5fyv6p98bp289` to fix the Weekly Systems Review Node/OpenClaw CLI prefix.
- Saved monthly prompt rewrite proposals for the five longest live payloads.

## Needs JT Attention

- Approve fixing the Weekly Systems Review command prefix or installing a supported Node 22 patch. The cron prompt still hardcodes Node 22.22.2, which now fails OpenClaw before the audit can run cleanly.
- Decide whether to clean duplicate plugin install metadata for `brave`, `codex`, and `lossless-claw`; this is not currently breaking runtime but keeps surfacing in status.
- `AGENTS.md` is only 194 chars under budget. Any future correction append should extract first.

## Next Review

2026-08-09.
