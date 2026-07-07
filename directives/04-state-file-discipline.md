# Eve Standing Directive 4 of 5: State File Discipline

Effective 2026-07-06. Approved by JT. Every job reads its state before working and writes its state after. No exceptions.

1. Every registry job owns exactly one state file at memory/job-state/<job-slug>.md, created from memory/job-state/TEMPLATE.md.
2. Read at start, always: last completed run, the cursor meaning the last processed item id or date, open items, last failure, and the started marker.
3. First write of every run: a started marker with timestamp, before any work.
4. Last write of every run: what ran, artifact paths, cursor advance, failures with signatures, next expected run, the claim file link if one was written, and clear the started marker.
5. Never redo logged work. If the state file or today's proofs show an item done, skip it. Redoing logged work is a failure with signature redid-logged-work. Re-verifying an already CONFIRMED item without new cause carries the same signature.
6. A stale started marker means the previous run died mid-flight. Reconcile from proofs and the claim file before acting, then resume from the cursor. Do not restart from zero and do not assume the dead run finished.
7. State files hold state, not content: current state plus the last 5 runs, older lines archived monthly to memory/job-state/archive/. Artifacts stay in proofs and referenced paths.
8. The heartbeat idempotency and proactive-work dedup rules in HEARTBEAT.md are instances of this directive and defer to it.
9. A job missing its state file creates it from the template, marks the run state-rebuilt, and proceeds conservatively, skipping anything proofs already show as done.
10. The Weekly Systems Review audits compliance: any run that skipped its start read or end write is flagged with signature state-skip.
