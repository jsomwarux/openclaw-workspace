# Client Dashboard — Altmark Group

## Outcome We Are Paid To Improve
- Primary outcome: local-first automation for sensitive back-office/property/family-office workflows with audit trail, human approval, and clear exception handling.
- Baseline: manual/local back-office processes before JT installed local workflow infrastructure.
- Target: insurance workflow stable in production, rent delinquency workflow tested/deployed cleanly, and DHCR Lease Renewal Phase 1 ready to kick off after rent delinquency acceptance.
- Current status: active — dedicated PC installed at Altmark office; insurance expiration workflow live in production and final 50% paid; rent delinquency initial 50% paid and in active build/testing; DHCR Lease Renewal proposal reviewed and delivery assets prepared.

## Live Status
| Area | Status | Notes | Owner | Next Action | Due |
|---|---|---|---|---|---|
| Insurance expiration workflow | Live in production / paid | Working as expected after a few minor updates; final 50% received | JT / Yair / Navid | Capture proof-safe screenshots/run logs/acceptance wording for referral/case-study use | This week |
| Dedicated PC handoff | Installed in office | Local workflow environment running production workflow | JT / Navid | Confirm support/admin path and backup visibility, but do not block revenue proof on old install uncertainty | This week |
| Rent delinquency workflow | Synthetic gate passed / client sample needed | Initial 50% received; 2026-05-29 dry run processed 8 synthetic rows into 1 included, 4 manual review, 1 excluded, 2 cleanup, with 0 tenant-facing drafts | JT / Yair / Matt/Karen | Use `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md` to request redacted Altmark sample export, source report path, refresh cadence, named output reviewer, and exception rules | Immediate |
| DHCR Lease Renewal Phase 1 | Proposal reviewed / delivery assets ready | Legal-rent renewals only; $3,500 proposal; preferential-rent renewals parked as Phase 2 | JT / Eve / Yair / Matt | After rent delinquency deployment/testing, confirm kickoff payment, populated command center spreadsheet, RGB rates, included units/properties, approved email recipients, and rent rolls | After rent delinquency gate |
| n8n HTTPS + Google OAuth | Reliability improvement / not commercial gate | Migration runbook exists; now lower priority than rent testing and proof capture unless current production workflow needs it | Eve / JT | Only migrate after backup/admin path is clear and non-sensitive smoke test is ready | After testing/proof |
| Reusable IP capture | Active | Insurance workflow is now proof-eligible subject to privacy/anonymization boundary | Eve / JT | Build anonymized workflow case file from verified facts only | This week |

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
- Use `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md` as the next rent delinquency action: the synthetic dry run passed, so the next gate is client sample/export shape, source report path, refresh cadence, named output reviewer, and confirmed exception rules.
- Keep `proof-assets/tuesday-closeout-branch-sheet-2026-05-26.md` available for any unresolved insurance/access/payment facts, but do not let old closeout wording obscure the current rent delinquency sample-export gate.
- DHCR Lease Renewal Phase 1 is now ready for kickoff sequencing after rent delinquency: use `proof-assets/dhcr-kickoff-command-sheet-2026-05-27.md`, `client-os/acceptance-checklist-dhcr-lease-renewal.md`, and `runbooks/dhcr-lease-renewal-workflow.md`.
- For infrastructure reliability, use `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md` only after PC/admin access and backup path are confirmed: back up n8n, choose stable HTTPS pattern, configure Google OAuth redirect, reconnect credentials, and run a non-sensitive smoke test.
- Older prep remains available at `proof-assets/tuesday-execution-pack-2026-05-12.md`, `proof-assets/monday-command-sheet-2026-05-11.md`, and `proof-assets/tomorrow-execution-pack-2026-05-08.md`.


## Decision Needed From Client
- Confirm support/admin owner for the installed PC and production workflow environment.
- Confirm any remaining insurance workflow open issues, if any.
- Confirm rent delinquency testing inputs, owner/date for acceptance, and production cutover expectations.
- Confirm DHCR Lease Renewal kickoff timing after rent delinquency deployment/testing, including $1,750 start payment, populated spreadsheet owner/date, RGB rates, included legal-rent units/properties, and approved recipients.

## Internal Control Added — 2026-05-13
- Weekly update must explicitly say whether the Altmark MC blocker was updated.
- Proof/referral assets remain gated until acceptance/payment clarity exists.

## Current Delivery Focus — 2026-05-26
- Insurance expiration workflow: live in production, stable after minor updates, final payment received. Capture proof-safe evidence and support/runbook details.
- Rent delinquency workflow: paid kickoff complete; active build/testing is now the main delivery priority. Testing pack prepared at `acceptance-checklist-rent-delinquency.md` and `runbooks/rent-delinquency-workflow.md`.
- DHCR Lease Renewal Phase 1: proposal reviewed; kickoff/acceptance/runbook assets created. Next delivery after rent delinquency deploys unless Altmark explicitly reprioritizes.
- Referral path: stronger now because one workflow is live and paid, but still keep naming/permission boundaries clean before using Altmark publicly or asking Yair for intros.

## Current Delivery Focus — 2026-05-30
- Rent delinquency synthetic smoke test passed on 2026-05-29.
- Next gate: get redacted Altmark source export with columns intact, source report path/name or export process, refresh cadence, named output reviewer, and exception rules.
- First real-report test stays review-only and blocked from tenant-facing sends until Altmark approves scope.
