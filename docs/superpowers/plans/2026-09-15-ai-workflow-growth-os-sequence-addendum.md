# AI Workflow Growth OS — September 15 Sequence Addendum

This addendum supersedes any current-action language in the v3.7 runbook that relies on the retired 90 Day Playbook, its November 17 freeze, or its invoice-within-90-days test. Those are historical only. The live capacity rule is operating rule 13: **in a week where zero qualified messages reach a buyer, no new infrastructure track starts.** JT sent five qualified cohort-one messages on September 15, 2026, so the rule is satisfied for this week.

## Current dependency-safe sequence

1. Fresh-verify Mission Control runtime/config commit `96a3dab`; push only after a non-builder `CONFIRM` and JT approval.
2. Merge and redeploy the reproducibility package under separate JT approvals.
3. Retarget cohort-two PR #39 to `main`, rerun CI, and merge only after JT approval.
4. Build the production owner adapters in order: verified channel, gate attestation, trusted review authority, suppression.
5. **Implement the universal seven-field Mission Control card contract before any cohort-two cards are generated.** Add real typed fields and rendering for: title, why, exact steps, paste-ready prompt when needed, where to paste/use it, observable done condition, and append-only feedback box. Migrate or adapt outreach cards without weakening their immutable snapshot/decision contract. This step may run alongside owner-adapter work but may not delay it.
6. Merge verified COI evidence from PR #33 into the canonical proof source.
7. Run one full synthetic no-send flow and independently verify it.
8. Activate production adapter writes and the visible weekly heartbeat only under separate JT approvals.
9. Hand-run cohort two: Eve researches five fresh prospects, reachable channel is required before drafting, JT reviews and sends. Replace this hand-run lane only after the n8n prospect workflow is built, deployed, and passes a verified production-like no-send run.
10. Keep manual LinkedIn and X posting live from verified real work while the content engines remain unbuilt.

## Deferral rule

A lane is deferred only when it lacks a current conversion surface, verified input, bounded next test, or available capacity after buyer contact. The retired playbook is not a deferral reason. Profile and homepage conversion work is active now because five cohort-one recipients can inspect those surfaces immediately.
