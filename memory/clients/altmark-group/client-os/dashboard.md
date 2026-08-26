# Client Dashboard — Altmark Group

## Outcome We Are Paid To Improve
- Primary outcome: local-first automation for sensitive back-office/property/family-office workflows with audit trail, human approval, and clear exception handling.
- Baseline: manual/local back-office processes before JT installed local workflow infrastructure.
- Target: insurance workflow stable in production, rent delinquency workflow tested/deployed cleanly, and DHCR Lease Renewal Phase 1 ready to kick off after rent delinquency acceptance.
- Current status: active. On 2026-08-24 Yair said Matt returns 2026-08-25 to clear rent delinquency outstanding items and Adi returns 2026-08-27, after which Yair will discuss JT's 2026-08-12 employment/NewCo proposal. Existing signed project terms remain the governing baseline unless replaced in writing. DHCR is on hold.

## Live Status
| Area | Status | Notes | Owner | Next Action | Due |
|---|---|---|---|---|---|
| Insurance expiration workflow | Live in production / paid | Working as expected after a few minor updates; final 50% received | JT / Yair / Navid | Capture proof-safe screenshots/run logs/acceptance wording for referral/case-study use | This week |
| Dedicated PC handoff | Installed in office | Local workflow environment running production workflow | JT / Navid | Confirm support/admin path and backup visibility, but do not block revenue proof on old install uncertainty | This week |
| Rent delinquency workflow | Client outstanding-item review acknowledged | Initial 50% received; synthetic gate passed; JT forwarded Matt the outstanding-item emails and messaged Yair/Matt on 2026-08-25; Matt replied “sounds good” | Yair / Matt / JT | Await substantive questions or deployment action; provide only genuinely missing inputs | Await client update |
| DHCR Lease Renewal Phase 1 | On hold | Do not chase as a standalone deposit/delivery item while Yair and Adi have not answered JT's 2026-08-12 employment/NewCo proposal | JT / Yair / Adi | Revisit only after response or explicit Altmark reprioritization | No due date |
| Altmark employment + NewCo | Waiting on scheduled discussion | Written proposal sent 2026-08-12; on 2026-08-24 Yair said he will discuss it with Adi after Adi returns 2026-08-27 | Yair / Adi / JT | Wait through stated checkpoint; revisit if no update | 2026-08-31 |
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
- Do not follow up before Adi returns 2026-08-27. If there is no update, revisit the employment/NewCo discussion 2026-08-31 without bundling DHCR, referrals, or favors.
- Keep DHCR on hold until Yair/Adi respond or explicitly pull it forward.
- After Yair/Matt substantively report back, use `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md` only for inputs that remain unresolved; Matt's acknowledgment alone does not clear deployment gates.
- Keep `proof-assets/tuesday-closeout-branch-sheet-2026-05-26.md` available for any unresolved insurance/access/payment facts, but do not let old closeout wording obscure the current rent delinquency sample-export gate.
- DHCR Lease Renewal Phase 1 is now ready for kickoff sequencing after rent delinquency: use `proof-assets/dhcr-kickoff-command-sheet-2026-05-27.md`, `client-os/acceptance-checklist-dhcr-lease-renewal.md`, and `runbooks/dhcr-lease-renewal-workflow.md`.
- For infrastructure reliability, use `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md` only after PC/admin access and backup path are confirmed: back up n8n, choose stable HTTPS pattern, configure Google OAuth redirect, reconnect credentials, and run a non-sensitive smoke test.
- Older prep remains available at `proof-assets/tuesday-execution-pack-2026-05-12.md`, `proof-assets/monday-command-sheet-2026-05-11.md`, and `proof-assets/tomorrow-execution-pack-2026-05-08.md`.


## Decision Needed From Client
- Confirm whether Yair and Adi want to proceed with the Altmark employment package and separate NewCo discussion.
- Confirm support/admin owner for the installed PC and production workflow environment.
- Confirm any remaining insurance workflow open issues, if any.
- Confirm rent delinquency testing inputs, owner/date for acceptance, and production cutover expectations.
- DHCR kickoff inputs are deferred until the employment/NewCo decision is answered or Altmark explicitly reprioritizes DHCR.

## Internal Control Added — 2026-05-13
- Weekly update must explicitly say whether the Altmark MC blocker was updated.
- Proof/referral assets remain gated until acceptance/payment clarity exists.

## Current Delivery Focus — 2026-05-26
- Insurance expiration workflow: live in production, stable after minor updates, final payment received. Capture proof-safe evidence and support/runbook details.
- Rent delinquency workflow: paid kickoff complete; awaiting Yair/Matt's outstanding-item review before further testing. Testing pack remains at `acceptance-checklist-rent-delinquency.md` and `runbooks/rent-delinquency-workflow.md`.
- DHCR Lease Renewal Phase 1: proposal reviewed; kickoff/acceptance/runbook assets created. Next delivery after rent delinquency deploys unless Altmark explicitly reprioritizes.
- Referral path: stronger now because one workflow is live and paid, but still keep naming/permission boundaries clean before using Altmark publicly or asking Yair for intros.

## Current Delivery Focus — 2026-05-30
- Rent delinquency synthetic smoke test passed on 2026-05-29.
- Next gate: get redacted Altmark source export with columns intact, source report path/name or export process, refresh cadence, named output reviewer, and exception rules.
- First real-report test stays review-only and blocked from tenant-facing sends until Altmark approves scope.

## Plan Review Pack — 2026-06-06
- Human-readable review pack created at `proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md`.
- Use it to review the rent delinquency gate with JT before any client-facing send or first Altmark sample run.
- Comment-back destinations are `acceptance-checklist-rent-delinquency.md`, `decision-log.md`, and `failure-log.md` so reviewer signal updates the Client OS instead of staying in chat.
