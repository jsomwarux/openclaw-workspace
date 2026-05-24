# Client Dashboard — Altmark Group

## Outcome We Are Paid To Improve
- Primary outcome: local-first automation for sensitive back-office/property/family-office workflows with audit trail, human approval, and clear exception handling.
- Baseline: manual/local back-office processes; first workflow finished but acceptance/payment evidence still not confirmed in Eve memory.
- Target: first workflow accepted, PC/access path clean, payment/deposit status clear, and next workflow gated by clean input data.
- Current status: active — dedicated PC installed at Altmark office on 2026-05-19; insurance expiration workflow finished and now needs post-install acceptance wording/payment clarity; rent delinquency paused by data-readiness/deposit gate.

## Live Status
| Area | Status | Notes | Owner | Next Action | Due |
|---|---|---|---|---|---|
| Insurance expiration workflow | Finished / post-install acceptance not confirmed in Eve memory | Acceptance checklist: `acceptance-checklist-insurance-expiration.md` | JT / Yair / Navid | Confirm workflow was verified on installed PC, capture acceptance wording/open issues/payment status | Immediate |
| Dedicated PC handoff | Installed 2026-05-19 / access confirmation needed | PC checklist exists in `runbooks/pc-handoff-checklist.md` | JT / Navid | Confirm who can access it, whether logs/workflow are visible, and any open setup issues | Immediate |
| Rent delinquency workflow | Paused by data readiness | Do not start until clean report + exception rules + deposit timing | Yair / Matt / JT | Use readiness checklist only after acceptance/payment path is clean | After handoff |
| n8n HTTPS + Google OAuth | Planned / high priority | Migration runbook created: `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md` | Eve / JT | Confirm PC/admin access, back up n8n, then migrate to stable HTTPS and reconnect Google credentials | 2026-05-21 to 2026-05-22 |
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
| Accepted workflows | 0 documented | 0 confirmed in Eve memory | 1+ | Flat | PC installed; need Yair/Navid post-install acceptance wording. |
| Workflows with runbook/checklist | 0 before OS | 3 | 100% active workflows | Up | Insurance, PC handoff, rent readiness. |
| Proof-safe reusable patterns | 0 | 2 logged | 1+ productized template | Up | Use synthetic/anonymized sample data. |

## Next 7 Days
- Use `proof-assets/monday-closeout-sheet-2026-05-25.md` as the next active closeout sheet if no weekend reply exists: confirm installed PC access/admin owner, verify insurance workflow/log visibility, capture acceptance wording/open issues, clarify insurance payment/approval status, and confirm rent delinquency deposit + clean sample report owner/date. `proof-assets/weekend-command-sheet-2026-05-23.md` remains the prior version; Friday/Wed packs remain available for context.
- For infrastructure reliability, use `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md` only after PC/admin access and backup path are confirmed: back up n8n, choose stable HTTPS pattern, configure Google OAuth redirect, reconnect credentials, and run a non-sensitive smoke test.
- Older prep remains available at `proof-assets/tuesday-execution-pack-2026-05-12.md`, `proof-assets/monday-command-sheet-2026-05-11.md`, and `proof-assets/tomorrow-execution-pack-2026-05-08.md`.


## Decision Needed From Client
- Confirm installed PC access path and who can operate/check it.
- Confirm insurance workflow acceptance wording/live usefulness.
- Confirm insurance workflow payment/final approval status.
- Confirm rent-delinquency deposit timing and cleaned sample export owner/date.

## Internal Control Added — 2026-05-13
- Weekly update must explicitly say whether the Altmark MC blocker was updated.
- Proof/referral assets remain gated until acceptance/payment clarity exists.

## Current Delivery Focus — 2026-05-06
- PC post-install verification: confirm access/verification path with Yair/Navid and capture open issues.
- Insurance expiration workflow: finished, needs acceptance confirmation, screenshots, final payment/approval status.
- Rent delinquency workflow: paused by Altmark-side reporting/ledger cleanup, not rejection. Do not start build work until the data-readiness checklist is satisfied and 50% deposit timing is confirmed.
- Data-readiness asset: `runbooks/rent-delinquency-data-readiness-checklist.md` is ready for Yair/Karen/Matt.
- Proof asset: capture only after installed PC access + insurance workflow acceptance/payment clarity.
- Referral path: ask Yair for 2–3 family-office intros only after `proof-assets/referral-readiness-gate-2026-05-23.md` is green; then use `proof-assets/yair-referral-ask-script.md` / `memory/consulting/yair-family-office-intro-ask-2026-05-13.md`.

