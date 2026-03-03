# Task Queue

## pending.jsonl
Deferred tasks that survive session resets. One JSON object per line.

### Schema
```json
{
  "id": "task-YYYYMMDD-HHMMSS",
  "created_at": "ISO8601",
  "priority": "high|medium|low",
  "title": "Short description",
  "task": "Full task description with all context needed to execute without current session history",
  "context": "Any background JT would need to know",
  "depends_on": [],
  "status": "pending|in_progress|done|failed"
}
```

### Priority
- `high` — process next available cycle
- `medium` — process within 2h
- `low` — process when idle

### Processing
Cron job `eve-pending-tasks-012` checks every 30 minutes during active hours (8AM–11PM).
Tasks are spawned as isolated sessions. Status updated in-place after completion.
