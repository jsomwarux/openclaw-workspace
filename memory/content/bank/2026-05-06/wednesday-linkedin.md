## Wednesday LinkedIn Profile: Maintenance Request Triage (PM Triage)

A maintenance inbox gets messy because every request arrives with the same weight.

A leaking pipe. A noisy neighbor. A broken appliance. A vague message from a tenant.

If the property manager has to read every request, classify urgency, decide who owns it, and write the response, the system is not triage. It is manual sorting with a nicer inbox.

While building the property management maintenance triage workflow, the useful piece was the first decision.

The flow uses Claude 3.5 Sonnet to read the incoming request, classify the issue category, assign an urgency score, and draft the tenant confirmation. If it is a leaking pipe, the system pulls the emergency plumber contact and alerts the manager. If it is a noisy neighbor, it drafts a compliance notice.

The behavior change was simple.

Urgent maintenance stopped getting buried in a generic inbox. The property manager only checks the dashboard for blockers or edge cases, while routine dispatch happens without them.

Handoff design is where the value shows up. The point was not faster replies, but making sure the dangerous request stopped looking like every other message.

---

## Advisory Board
The Exec: PASS — Names a familiar property management pain and provides a concrete outcome: emergency requests stop getting buried in the inbox.
The Practitioner: PASS — Mentions specific implementation: Claude 3.5 Sonnet classification, urgency scoring, and automated emergency routing.
The Lurker: PASS — The opening line identifies a felt stress for anyone running an operations inbox. The outcome is believable and aspirational.

## Status: APPROVED