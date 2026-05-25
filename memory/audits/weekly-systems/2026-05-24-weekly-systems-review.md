# Weekly Systems Review — 2026-05-24

## Executive Summary
Grade: B / not clean A-level.

Core system is operational: cron statuses are green, critical files exist, watchdog is loaded, Mission Control is reachable, and costs are low. Drift remains in three places: cron volume exceeds the old ≤20/day cap, gateway process is resource-heavy, and bootstrap files are too close to budget for comfort.

## Cron Health Audit
- Jobs checked: 51.
- Errors: none visible in `openclaw cron list` table; no `lastRunStatus=error` or delivery failure surfaced in the human-readable list.
- Delivery: user-facing jobs shown as `delivered` or `not requested`; no failed delivery detected in list output.
- Never-ran jobs: none obvious from the rendered list; JSON output did not expose last-run fields reliably, so the rendered table was treated as source of truth.
- Timeout pressure: JSON output did not expose duration/timeout fields, so no automated timeout bump applied.
- Sunday conflict: 6PM has two weekly jobs (`Weekly North Star Command Center` and `Weekly Strategic Gut-Check`) at the same minute. Existing instruction says note, do not self-resolve.
- Invocation cap: 51 total scheduled jobs. Approx daily invocation estimate is above the old ≤20/day cap; active MEMORY.md already says keep daily cron invocations ≤20. Needs pruning/routing review.

## File Budgets
| File | Size | Budget | Status |
|---|---:|---:|---|
| AGENTS.md | 27,013 | 28,000 | Under, close |
| MEMORY.md | 19,535 | 20,000 | Under, close |
| TOOLS.md | 15,139 | 16,000 | Under, close |
| HEARTBEAT.md | 15,997 | 16,000 | Under by 3 chars — effectively full |

Recommended extraction: compact HEARTBEAT.md before any append. MEMORY.md should distill/archive older Active Automation details soon. TOOLS.md should move older app/plugin details to `docs/tools/TOOLS-full.md` if new tools are added.

## Process Health
Top process sampled:
- OpenClaw gateway PID 29836: ~2.3GB RSS; CPU samples: 25.6%, then ~10.1%. This exceeds the audit threshold (>500MB and >5% CPU) and should be watched/remediated.
- n8n process: ~125MB RSS, low CPU.
- Mission Control Convex/Next processes: low CPU, memory acceptable.

Gateway status: reachable on local loopback, LaunchAgent loaded/running, app version 2026.5.3-1.
Watchdog: `com.openclaw.gateway-watchdog` loaded.

## LaunchAgent Config
- Gateway plist: `Label=ai.openclaw.gateway`, `ThrottleInterval=1`. This is below the requested safe floor (`10+`) and is config drift. Not auto-fixed because LaunchAgent service config changes are stateful and should be approved/scheduled.
- Watchdog plist: `Label=com.openclaw.gateway-watchdog`, `StartInterval=600`. This is acceptable (`≤600`).

## OpenClaw Version
- Current: `OpenClaw 2026.5.3-1 (2eae30e)`.
- Latest npm: `2026.5.22`.
- Web search also surfaced GitHub/container results around `2026.5.16-beta.7`; npm says newer stable package exists.
- Update available: yes. Do not auto-update without JT decision.

## Plugin Audit
- `~/.claude/settings.json`: `enabledMcpjsonServers` is `{}`; `context-mode@context-mode` is not enabled. Desired false/disabled posture holds.
- `~/.openclaw/extensions/`: expected `lossless-claw` plus `.openclaw-install-backups`; no unexpected extension found.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: exists/readable.
- `scripts/gateway-watchdog.sh`: exists/executable.
- `health/health.sqlite`: exists.
- `tasks/pending.jsonl`: valid JSONL.

## Autoresearch Enrollment Check
- Modified in last 7 days and already registered: passive-income-scout, passive-income-strategist, cold-email, x-research.
- Modified but not enrolled: prompt-library. Decision: no enrollment — it is a meta-template skill, not a repeated scoreable output workflow with clear pass/fail behavior.
- No new checklist created.

## Future Signals Review
Reviewed `memory/future-signals.md` against current MEMORY/project reality. No triggers clearly met:
- ViewTrack/PostBridge/Creator Briefing require sustained app content/revenue or creators — not met.
- Clay requires 8+ active outreach prospects and >2hr/week manual tracking — not verified/met.
- Free Tool Strategy requires 200+ organic visits/week or paid traffic — not met.
- Passive Income App KPI dashboard requires Vista 500+ downloads/revenue or Nash active weekly users — not met.
- Sports GM app trigger requires job offer/consulting $3K/mo or strong demand signals — not proven in current MEMORY.

## Passive-Income Idea Queue Pruning
- Mission Control reachable.
- Matching `[PI]`/`Build idea:` todo tasks with sortOrder >=500: 7.
- Oldest age: ~14 days. None are older than 60 days, so none pruned.
- Closed one duplicate systems task unrelated to PI pruning: `Weekly systems review: prune cron cap + fix gateway throttle`, superseded by active task `Fix weekly systems review drift: cron cap, gateway load, bootstrap budgets`.

## Weekly Cost Review
Total 7-day spend: $2.813.
- gpt-5.5: $2.689 (96%, 2 sessions)
- deepseek/deepseek-chat-v3-0324: $0.124 (4%, 7 sessions)
Most expensive sessions:
- 2026-05-24 Cron: prospect-discovery — $1.565
- 2026-05-20 Cron: prospect-discovery — $1.125
Monthly pace: $10.19 vs $50 target; $39.81 headroom.
Observation: Groq/Llama unused this week; simple crons may not be using cheapest route.

## Issues Fixed This Run
- Closed duplicate Mission Control systems drift task; kept the stronger active task with broader scope.
- Added weekly systems review entry to `memory/training/training-log.md`.

## Needs JT Attention
1. Decide whether to update OpenClaw from 2026.5.3-1 to 2026.5.22.
2. Prune/consolidate crons to get daily invocations back near ≤20, or formally revise the cap if the newer operating model accepts higher volume.
3. Fix gateway LaunchAgent `ThrottleInterval=1` to `10+` during a planned maintenance window.
4. Investigate gateway memory/CPU load; consider a planned gateway restart window via approved restart script if load persists.
5. Compact HEARTBEAT.md before any append; it is effectively full.

## Next Review
Next Sunday: 2026-05-31.
