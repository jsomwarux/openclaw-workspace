# HEARTBEAT.md — Periodic Wake Behaviors

## Active Hours
8:00 AM – 11:00 PM EST. Outside these hours: HEARTBEAT_OK immediately.

## Morning Brief (7:30 AM, cron)
Deliver to JT via Telegram:
1. Read memory/tasks.md — top 3 priorities
   **STALENESS CHECK (mandatory before surfacing any task):**
   - Any task referencing a specific content draft, Drive link, or post: check the `| Updated:` date on that task. If > 7 days old → SKIP IT.
   - Any task referencing a job application: check MEMORY.md Job Market section. If the role is marked expired/deprioritized → SKIP IT.
   - Only surface tasks that are actionable TODAY with no staleness risk.
2. Monitor AI news, crypto market, and job market activity.
3. Read memory/niche-monitor-latest.md — severity-filtered intel.
4. Check for any running automations or pending tasks, noting their statuses.
5. Provide one proactive suggestion aligned with current goals.

## Heartbeat (every 2 hours: 10AM, 2PM, 6PM, 10PM)
1. Check pending tasks queue — flag anything urgent or overdue.
2. Monitor any running cron jobs — alert if there are issues.
3. If idle, pick the highest-priority item from your mission and start working on it.

## Proactive Work Slot
If there’s nothing urgent during heartbeats, work on mission-aligned tasks such as:
- Client research
- Market monitoring
- App improvements
- Content drafting

## Logging
Log all actions taken during heartbeats in memory for visibility.