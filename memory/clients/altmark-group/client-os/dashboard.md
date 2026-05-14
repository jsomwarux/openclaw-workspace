# Client Dashboard — Altmark Group

## Outcome We Are Paid To Improve
- Primary outcome: local-first automation for sensitive back-office/property/family-office workflows with audit trail, human approval, and clear exception handling.
- Baseline: manual/local back-office processes; first workflow finished but acceptance/payment evidence still not confirmed in Eve memory.
- Target: first workflow accepted, PC/access path clean, payment/deposit status clear, and next workflow gated by clean input data.
- Current status: active — insurance expiration workflow finished/awaiting acceptance confirmation; dedicated PC handoff/access path needs clarity; rent delinquency paused by data-readiness/deposit gate.

## Live Status
| Area | Status | Notes | Owner | Next Action | Due |
|---|---|---|---|---|---|
| Insurance expiration workflow | Finished / acceptance not confirmed in Eve memory | Acceptance checklist: `acceptance-checklist-insurance-expiration.md` | JT / Yair / Navid | Verify demo/logs/open issues/client acceptance/payment status | Immediate |
| Dedicated PC handoff | Needs confirmation | PC checklist exists in `runbooks/pc-handoff-checklist.md` | JT / Navid | Lock handoff/access path | Immediate |
| Rent delinquency workflow | Paused by data readiness | Do not start until clean report + exception rules + deposit timing | Yair / Matt / JT | Use readiness checklist only after acceptance/payment path is clean | After handoff |
| Reusable IP capture | Started | `reusable-ip-log.md` created; insurance exception-layer task already in MC | Eve / JT | Productize only with synthetic/anonymized data | After acceptance |

## Wins This Week
- Weekly execution pack exists for acceptance/handoff/payment/referral sequencing.
- Insurance, PC handoff, and rent delinquency runbooks/checklists exist.
- Proof-safe acceptance checklist and reusable IP log added.

## Misses / Risks This Week
- Acceptance/payment status is still not confirmed in Eve memory.
- Referral ask should wait until first workflow is accepted and payment/deposit status is clean.
- Public proof must not expose Altmark policy/entity/local network details.

## Metrics
| Metric | Baseline | Current | Target | Trend | Notes |
|---|---:|---:|---:|---|---|
| Accepted workflows | 0 documented | 0 confirmed in Eve memory | 1+ | Flat | Need Yair/Navid confirmation. |
| Workflows with runbook/checklist | 0 before OS | 3 | 100% active workflows | Up | Insurance, PC handoff, rent readiness. |
| Proof-safe reusable patterns | 0 | 2 logged | 1+ productized template | Up | Use synthetic/anonymized sample data. |

## Next 7 Days
- Use `proof-assets/wednesday-execution-pack-2026-05-13.md` as the current single-page execution sheet: confirm PC handoff/access path, verify insurance workflow acceptance, clarify payment/deposit status, and preserve the rent delinquency data-readiness boundary.
- Older prep remains available at `proof-assets/tuesday-execution-pack-2026-05-12.md`, `proof-assets/monday-command-sheet-2026-05-11.md`, and `proof-assets/tomorrow-execution-pack-2026-05-08.md`.


## Decision Needed From Client
- Confirm PC handoff/access path.
- Confirm insurance workflow acceptance wording/live usefulness.
- Confirm insurance workflow payment/final approval status.
- Confirm rent-delinquency deposit timing and cleaned sample export owner/date.

## Internal Control Added — 2026-05-13
- Weekly update must explicitly say whether the Altmark MC blocker was updated.
- Proof/referral assets remain gated until acceptance/payment clarity exists.

## Current Delivery Focus — 2026-05-06
- PC handoff: confirm exact delivery date/time or fallback access/verification path with Yair/Navid.
- Insurance expiration workflow: finished, needs acceptance confirmation, screenshots, final payment/approval status.
- Rent delinquency workflow: paused by Altmark-side reporting/ledger cleanup, not rejection. Do not start build work until the data-readiness checklist is satisfied and 50% deposit timing is confirmed.
- Data-readiness asset: `runbooks/rent-delinquency-data-readiness-checklist.md` is ready for Yair/Karen/Matt.
- Proof asset: capture only after PC handoff + insurance workflow acceptance.
- Referral path: ask Yair for 2–3 family-office intros after acceptance using proof-assets/yair-referral-ask-script.md.

