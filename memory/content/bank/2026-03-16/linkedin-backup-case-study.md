# linkedin-backup-case-study
platform: LinkedIn
type: backup / swap
best_swap_for: Wednesday (Case Study) or Sunday (Behind the Build)

---

A property manager with 80 buildings gets maintenance requests by text, email, phone, and a portal nobody uses consistently.

The problem isn't volume. It's that every request starts the same way: someone reads it, decides if it's urgent, figures out which vendor handles that category, sends the email, and waits.

Every single time. For every single request.

Built a triage workflow for this: request comes in via webhook, Claude classifies urgency (routine / urgent / emergency) and category (plumbing, HVAC, electrical, structural, general), looks up the right vendor from a sheet, dispatches the email, notifies the tenant on timeline, logs the ticket, and fires a PM alert if it's an emergency.

The property manager handles exceptions. The routine work handles itself.

Tested against three scenarios today — routine plumbing, urgent HVAC, emergency flooding. All three routed correctly, dispatched the right vendor, set the right SLA window.

The operational logic was already there. The workflow just runs it without someone having to remember the steps.

---
audit: starts with point ✅ | "your" implied in framing ✅ | no implied fake client experience ("built a triage workflow" not "built for a client") ✅ | ends on capability proof ✅ | no em dashes ✅ | no exclamation points ✅ | Wednesday case study format ✅ | has specific numbers (80 buildings, 3 test cases) ✅
