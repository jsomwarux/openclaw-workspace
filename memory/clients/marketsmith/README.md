# Client Operating System Template

Use this for every active consulting client from day one. The goal is to make the client experience feel like SaaS while turning delivery into reusable IP.

Create one folder per client engagement and keep these files current:

- `dashboard.md` — live client-facing status, KPIs, wins, misses, next actions
- `weekly-updates.md` — weekly account-owner update: wins, misses, blockers, next week's plan
- `decision-log.md` — dated reasoning behind scope, workflow, automation, and prioritization decisions
- `workflow-map.md` — current-state and target-state workflow documentation
- `failure-log.md` — failed workflows, failed campaigns, edge cases, causes, and fixes
- `automation-candidates.md` — manual steps worth encoding into automations/agents later
- `metrics.md` — outcome metrics, baseline, target, reporting cadence
- `quarterly-review.md` — decision-maker review agenda and account expansion opportunities
- `acceptance-checklist.md` — proof-safe acceptance gate for each deliverable before it is called done
- `plan-review-pack.md` — client/collaborator-readable review surface for plans, specs, risk questions, and acceptance criteria
- `reusable-ip-log.md` — reusable patterns captured without leaking private client data
- `raw-inputs/` — raw third-party/source inputs before cleaning
- `cleaned-inputs/` — normalized/cleaned datasets or extracts
- `outputs/` — delivered outputs tagged with client, date, workflow, and outcome
- `handoff.md` — client/internal handoff, support path, rollback, review cadence, and known open issues

Rule: do the work manually until repeat patterns and edge cases are visible. Then automate the pattern, not the fantasy version of the workflow.

Proof/privacy rule: raw client data stays private. Any case study, deck, content post, reusable template, or demo asset must use redacted, anonymized, or synthetic data unless JT has explicit client permission.

## Anti-Placeholder Gate
Before marking a Client OS initialized, every top-level file must contain at least one client-specific fact, a named unknown with owner/date, or an explicit N/A reason. Empty template bullets do not count.

## Acceptance Escalation
If any acceptance criterion is still `Not started`, `TBD`, or `Not confirmed` for more than one weekly update cycle, create or update exactly one Mission Control blocker with first action, why it matters, and done state. Do not create duplicate blockers for the same client/deliverable.
