# Wednesday LinkedIn — 2026-04-29

## Draft

Every property manager I spoke to during outreach had the same gap.

A tenant submits a maintenance request. The system logs it. Then nothing happens until someone checks the queue. If the vendor no-shows, the tenant calls again. If the manager never gets flagged, the request sits for days. The dashboard shows green. The tenant is still waiting.

So I built a workflow around where the form breaks.

The intake trigger is a simple message. An AI model classifies the issue by urgency and type. If it is routine, the workflow routes it to the right vendor and sets a follow-up window. If the vendor does not confirm within that window, the manager gets an alert. If the tenant reports the same issue twice, the workflow flags it as unresolved and bumps the priority. The manager sees what needs attention. The tenant stops calling twice for the same problem.

The property manager did not need another dashboard. They needed the system to tell them when the normal path broke.

Most ops tools are built to log work. The ones that matter are built to surface what the log missed.

## Advisory Board

The Exec: PASS — Concrete outcome: manager sees what needs attention, tenant stops calling twice. Framed as outreach pattern, not fabricated client. Build specificity is high enough to describe to a colleague.

The Practitioner: PASS — Trigger is specific (simple message intake). AI model classifies by urgency and type. Routing logic is clear (routine → vendor + follow-up window). Escalation conditions are specific (vendor no-confirm, tenant repeat report). No hand-waving.

The Lurker: PASS — "The dashboard shows green. The tenant is still waiting" is the stop-scroll moment. Identity Validation: every PM has felt the gap between logged and resolved. Aspiration check: the outcome feels achievable, not out of reach.

## Status: APPROVED
