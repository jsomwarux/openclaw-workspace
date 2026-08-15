# Mission Control Hygiene Snapshot - 2026-08-14 15:27 ET

Source: live `http://localhost:3000/api/tasks` after `python3 scripts/mission_control_north_star_audit.py`.

## Current Shape
- Active tasks: 66
- High priority: 10
- Medium priority: 48
- Low priority: 8
- Assigned to JT: 47
- Assigned to Eve: 19
- No due date: 54
- Overdue high-priority gates: 6
- Updated more than 30 days ago: 0

## Overdue High-Priority Gates
- `sortOrder 1` - JT - Consulting - MSI: Montclair-first Nexus delivery mechanics
- `sortOrder 2` - JT - Consulting - Altmark FTE + NewCo: separate comp/IP negotiation lane
- `sortOrder 3` - JT - Consulting - Altmark: clear delinquency go-live gates + JT outreach_id blocker
- `sortOrder 4` - Eve - Operations - Mission Control hygiene: retire stale backlog + fix task quality gates
- `sortOrder 20` - JT - Personal Admin - Complete weekly unemployment certification
- `sortOrder 25` - JT - Health - Start 14-day health protocol + book prescriber

## Queue Compression Candidates
- Content review queue has 22 review/post or queued-post tasks without due dates. These are likely better handled as one dated "review current content queue" task plus an archive list, not separate active tasks.
- Benched consulting follow-ups still appear active at low priority even though their title says `BENCHED until Aug 1`. These need either a new review date or archive status.
- Duplicate strategy framing appears around `Strategy: Package Outcome-Based Run Control` and `Strategy: Turn Run Control Into The Sales Asset`. Keep the high-priority due task and merge or archive the lower-priority duplicate after confirming no unique artifact is attached.
- Cron verification tasks at sort orders 181-183 are no-date operational follow-ups. They should be resolved during Weekly Systems Review or merged into that owner task.

## Safe Next Action
For the active Mission Control hygiene task, run one owner-approved pruning pass in this order:
1. Keep the top 10 high-priority tasks untouched except for owner/date cleanup.
2. Merge duplicate Run Control strategy tasks into the current high-priority package task.
3. Collapse stale content review tasks into one "current content queue review" item with a link to the draft index.
4. Convert benched consulting tasks to a dated review gate or archive them.
5. Move cron follow-ups into the Weekly Systems Review task unless a cron is actually unhealthy.

No live task mutation was made in this heartbeat.
