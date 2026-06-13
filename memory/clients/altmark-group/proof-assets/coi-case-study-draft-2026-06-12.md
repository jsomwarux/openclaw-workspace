# Private COI Case Study Draft - Altmark Operations Workflow

Status: private draft only. Not public proof. Do not name Altmark externally or use real tenant/property/balance data without explicit permission.

Drive: https://docs.google.com/document/d/13fMON6B3r_-Z87MKT_FafT1gWSNXGY9HhyZg4tWlybA/edit

## One-Page Version

### Problem
A NYC property/family-office operator had multiple back-office workflows living across local files, spreadsheets, AppFolio-style property data, QuickBooks-style finance data, and inbox follow-ups. The work was sensitive enough that a generic cloud SaaS replacement was not the right first move. The useful first move was a local-first workflow layer with logs, review gates, and human approval.

Evidence:
- Local source: `memory/clients/altmark-group/repeatable-offer.md`
- Local source: `memory/clients/altmark-group/status.md`

### Build
JT set up a local workflow environment and delivered the first production workflow around insurance expiration tracking. The system is designed around internal review, audit trail, and no autonomous financial or external action. The next workflow, rent delinquency outreach, is built as a review-only queue until the client approves the source export, reviewer, cadence, and exception rules.

Evidence:
- Insurance workflow status and payment: `memory/clients/altmark-group/status.md`
- Rent delinquency plan review pack: `memory/clients/altmark-group/proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md`
- Rent delinquency acceptance checklist: `memory/clients/altmark-group/client-os/acceptance-checklist-rent-delinquency.md`

### Silent-Failure Catch
Verified artifact: the synthetic rent-delinquency dry run caught the exact class of failure this type of workflow has to prevent: unsafe or ambiguous rows silently flowing into normal tenant outreach. The 2026-05-29 dry run processed 8 synthetic rows and forced every row into one queue: 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified. No tenant-facing draft was generated for manual-review, excluded, or cleanup rows.

Evidence:
- Run log: `memory/clients/altmark-group/client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md`
- Output CSV: `memory/clients/altmark-group/client-os/outputs/rent-delinquency-synthetic-smoke-test-output-2026-05-29.csv`
- Proof log: `proofs/2026-05-29/actions.jsonl` proof id `e2e27c44`

UNVERIFIED: the exact phrase "June 2-9 silent-failure catch" is not backed by a matching local artifact found in this pass. The verified silent-failure artifact is the 2026-05-29 synthetic gate plus the 2026-06-06 plan review pack.

### Outcome
Verified outcomes:
- First workflow status is recorded as live in production and final 50% paid.
- Dedicated local workflow PC is recorded as installed at the client office.
- Rent delinquency workflow initial 50% is paid, but final delivery remains blocked on client inputs.
- Synthetic rent-delinquency gate passed with 0 unclassified rows and no unsafe tenant-facing drafts.

Evidence:
- `memory/clients/altmark-group/status.md`
- `memory/clients/altmark-group/client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md`

### Why This Matters To A COI
The repeatable pattern is not "AI chatbot for property management." It is a safer operations layer for sensitive property workflows:
- Existing systems stay in place.
- The workflow prepares queues, exceptions, summaries, and drafts.
- Humans approve external actions.
- Logs and review gates make the system supportable.

### Referral Ask Draft
Use only after acceptance/proof gates clear:

Yair, now that we have seen this working in a controlled workflow, I think the same pattern would be useful for other family-office or property-ops teams that have sensitive local files, AppFolio/QuickBooks-style data, and too many manual follow-ups.

Would you be comfortable introducing me to 2-3 operators where a short workflow diagnostic would be useful?

## LinkedIn Version

I do not think most property operators need "AI transformation."

They need one ugly workflow made reliable.

The pattern I keep seeing:

- critical data lives in the existing tools
- staff know the judgment calls
- the misses happen in the handoffs
- nobody wants another dashboard that creates work

The useful version of AI/automation is narrower:

1. Pull the messy source data.
2. Route every row into a clear queue.
3. Force ambiguous cases into human review.
4. Block sensitive external actions until approved.
5. Leave an audit trail the operator can actually read.

On one property-ops workflow, the most important test was not whether the system could generate outreach.

It was whether it refused to generate outreach when the row was risky.

In a synthetic dry run, every test row landed in one queue: included, manual review, excluded, or cleanup. Legal/process-sensitive, payment-plan, dispute, missing-contact, and credit/prepayment cases stayed out of normal outreach.

That is the bar.

Not "automate everything."

Automate the routing. Preserve the judgment. Make the exception visible before it becomes expensive.

Proof boundary: anonymized/synthetic workflow details only; no client name, tenant data, balances, or private screenshots.
