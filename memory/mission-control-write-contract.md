# Mission Control write contract (v2 — after the payments/clients redesign)

## Cash
- Collected cash is recorded ONLY in the Convex payments table via the API. Never record a payment as prose in north-star.md and expect it to count.
- Every payment needs: clientName, amount, paidOn (real date), milestone, kind, cleared, source (evidence ref).
- pipeline.jsonl is FORECAST ONLY. Never zero out a client's value when they pay — change the stage instead. Zeroing is what made collected cash structurally invisible.
- MSI remaining value is $5,400 ($10,800 signed, $5,400 collected at kickoff). Do not revert this.
- Never restructure north-star.md headings or labels.

## Tasks you create
- Set clientId whenever the task is client-scoped. Unassigned client work will not appear in the Clients lane.
- Set dollars and stageProbability on anything cash-bearing. A task with no dollars scores 0 and will never surface, no matter how important it is.
- Set lane explicitly.
- Set waitingOn (who, what, since, nudgeAfterDays) when blocked on an external person. This parks it out of JT's queue until a nudge is due, which is intended.
- Set proofRequired true when completing it should yield a case study or reusable artifact.
- Do not create tasks with priority high. Propose at medium and note "proposes high" in the description for JT to review.

## What NOT to create
- During the consulting-cash mandate, do not create "Build idea:", "Strategy:", or "Positioning:" tasks. Route those to the pideas table or a memory note. The open-task list is for work, not for ideas.

## Facts, not rankings
- You never set priority or score directly. You update facts (dollars, dueDate, stageProbability, waitingOn) and the deterministic scorer ranks.
- Every field update includes an evidence string: a file path, URL, or quoted message. No evidence, no write.
- Never report a task complete without a verifiable output artifact.
