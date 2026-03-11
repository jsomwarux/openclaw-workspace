# Feedback & Operational Rules

## Heartbeat Deduplication
- Before writing any heartbeat log block for a given hour, check if today's daily note already has a substantive entry for that same hour. If yes → respond HEARTBEAT_OK without writing a duplicate.
- Known race condition (recurring): two triggers fire close together; both pass dedup check before either writes. Mitigate: treat any entry within 59 minutes of current hour as already-handled.
- Lockfile approach (identified 2026-03-08, not yet implemented in cron config): check `/tmp/heartbeat-HH-lock` before writing. If present → HEARTBEAT_OK. Requires cron behavior change to implement.

## Proactive Work
- If first-priority proactive item was already done this session, move to next item in priority list. Never skip proactive entirely when idle — always try the next category.
- Before picking a proactive work item: scan today's daily note for whether the same output file was already updated. If yes, skip and choose the next category.

## Task Staleness
- During any film review: check tasks.md for tasks with "this week", "apply this week", or explicit date-bound language.
- If the task was written >7 days ago and status is still pending → flag to JT in same heartbeat or push 🌙 MC task.
- Do not let time-sensitive tasks age silently past their implied deadline.

## Heartbeat-to-MC Rule
- Any heartbeat finding stating "flag for [day]" or "check [day]" about a named cron = push MC task immediately in the same heartbeat, not deferred.
- Any phrase matching "awaiting JT", "awaiting decision", "pending JT" in a daily note = push 🌙 Decide task same session.

## Build Close-Out
- Any build noting a "manual step pending" for JT must push it to Mission Control immediately. Task board is the only valid home for action items.
- Any file created during proactive heartbeat work is NOT done until Drive upload is confirmed — same heartbeat, same block. Drive link must be logged before moving on.
