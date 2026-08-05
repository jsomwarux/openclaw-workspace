# Altmark/DHCR Mission Control Cash-Send Map - 2026-08-04

Status: internal heartbeat research only. No send, post, schedule, task mutation, or client-facing asset was created.

## Source Snapshot
- Daily Send Sheet at 2026-08-04 07:30 surfaced two sends due:
  - Altmark rent delinquency remainder, 19 days stale, roughly $2,250.
  - DHCR Lease Renewal Phase 1 deposit, 19 days stale, roughly $1,750.
- `memory/send-queue.md` regenerated 2026-08-04 from `memory/pipeline.jsonl` and still lists only those two send queue items.
- `memory/pipeline.jsonl` source rows:
  - Altmark rent delinquency remainder: stage `blocked`, value `2250`, waiting on `client`, last touch `2026-07-16`.
  - DHCR Lease Renewal Phase 1 deposit: stage `pending`, value `1750`, waiting on `client`, last touch `2026-07-16`.

## Live Mission Control Mapping
- Altmark has a direct high-priority live Mission Control row:
  - `Altmark: send rent delinquency source/export gate and collect $2,250 closeout path`
  - status `todo`, priority `high`, project `Consulting`.
- DHCR has a live Mission Control row, but it is medium priority:
  - `Altmark DHCR: collect kickoff inputs after rent delinquency gate`
  - status `in-progress`, priority `medium`, project `Consulting`.

## Implication
- Altmark is aligned across Daily Send Sheet, send queue, pipeline, Mission Control priority report, and live Mission Control.
- DHCR is aligned as an active cash send in Daily Send Sheet/send queue/pipeline, but it is not currently a high-priority Mission Control row. Treat this as a routing/priority mismatch to review before relying on the high-priority task list as the only cash-gate source.
- Do not send or escalate either item without explicit JT approval.
