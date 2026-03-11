# Overnight Agent — Feedback & Learned Rules

Every time JT provides feedback on overnight work, Eve appends an entry here.
Each run reads ALL active rules before starting.

## Format
```
[DATE] Task: [task title]
Feedback: "[JT's exact words]"
Rule: [derived rule — actionable, specific, permanent]
Status: active
```

To retire a rule (if superseded or no longer applies), change `Status: active` → `Status: retired [DATE]`.

---

## Active Rules

[2026-03-06] Observed: 2026-03-05 daily note contains 5 duplicate "Heartbeat 22:00" entries — all firing between 9:36PM–10:36PM EST, each independently writing a new log block with identical content (Spanish nudge + no urgent items).
Rule: Before writing any heartbeat log entry, check if the current hour (rounded down) already has a log entry in today's daily note. If an entry for the same hour exists AND it covered the same checks (cost alerts, board review, Spanish), respond with HEARTBEAT_OK without writing a duplicate block. Each hour should have at most one substantive log entry.
Status: active

*(No rules yet — rules accumulate from JT's feedback after each overnight run)*

---

## Operational Rules (Eve-derived from film reviews)

[2026-03-03] Observed: Convex backend (Mission Control) crashed (exit -15) around 4PM on 2026-03-02 and wasn't caught until 10PM heartbeat — 6h downtime while heartbeat logged only "unreachable (may be down)" without attempting recovery.
Rule: When any heartbeat check finds Mission Control unreachable, immediately run: `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex 2>/dev/null; launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next 2>/dev/null`. Log whether kickstart restored the board. Don't just log "may be down" and move on.
Status: active

[2026-03-02] Observed: health check-in cron misfired 4x on 2026-03-01 (fired at wrong hours — 9AM, 11AM, 1AM, 3AM instead of 9PM). Root cause: nextRunAtMs state drift in the scheduler. No fix runbook existed.
Rule: When any cron fires >1h outside its expected window, log the job ID + actual fire time. If 3+ misfires on same job within 24h → delete and recreate the cron job to reset nextRunAtMs. Run `openclaw doctor` first to verify schedule config is correct before recreating.
Status: active

---

## Retired Rules

*(None)*
