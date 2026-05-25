# Mission Control Cleanup Plan — 2026-05-24

## Current verified state
- Active tasks: 291
- High-priority tasks: 39
- Single North Star state file created: `memory/north-star/active-this-week.md`

## Cleanup rule
Do not bulk-archive blindly. Keep high priority only for tasks that are:
1. Altmark proof/payment/access this week
2. Critical system-health blockers that can break delivery
3. Truly JT-only urgent obligations

Everything else should become medium/low, validation-only, or be archived if stale/duplicative.

## Keep high this week
- Altmark: lock PC handoff + acceptance/payment clarity
- Altmark: capture redacted proof screenshots during PC handoff
- Altmark: confirm acceptance/access, then migrate n8n HTTPS + Google OAuth
- Fix weekly systems review drift: cron cap, gateway load, bootstrap budgets
- Complete weekly unemployment certification if not already done

## Likely downgrade from high
- Vista/Nash/Glow app-marketing tasks that are not today-critical
- M2 connection-request tasks unless part of a live, proof-backed push
- Guyana/local-content exploration tasks
- Generic content/offering review tasks
- Health/content automation improvements unless broken today

## Needs careful handling
- Aya co-living dashboard remains active client revenue but is pending approval; keep visible, probably not above Altmark.
- Strategy: Clean Buyer-Channel State Before More Outreach is important, but not the single active weekly priority.

## Recommended next action
Run a safe Mission Control update pass that only changes priority/sortOrder/status for obvious non-North-Star high tasks, then re-audit high count. Target: <=10 high tasks.
