# Rent Delinquency Synthetic Smoke Test Log — 2026-05-29

## Scope
- Source fixture: `../cleaned-inputs/rent-delinquency-synthetic-smoke-test-2026-05-28.csv`
- Mode: dry-run / review-only
- Approval state: locked, no tenant-facing send path
- Output artifact: `rent-delinquency-synthetic-smoke-test-output-2026-05-29.csv`

## Result
| Queue | Expected | Actual | Case IDs |
|---|---:|---:|---|
| Included | 1 | 1 | RD-001 |
| Manual review | 4 | 4 | RD-002, RD-003, RD-004, RD-005 |
| Excluded | 1 | 1 | RD-006 |
| Cleanup | 2 | 2 | RD-007, RD-008 |
| Unclassified | 0 | 0 | none |

All 8 synthetic rows classified into exactly one queue. No tenant-facing draft was generated for manual-review, excluded, or cleanup rows.

## Edge-Case Checks
| Case | Check | Result |
|---|---|---|
| RD-002 | Recent payment stays out of normal outreach until live balance is confirmed | Pass |
| RD-003 | Payment plan routes to manual review | Pass |
| RD-004 | Dispute routes to manual review | Pass |
| RD-005 | Legal/process-sensitive flag routes to manual review and cannot produce a normal tenant-facing draft | Pass |
| RD-006 | Credit/prepayment is excluded | Pass |
| RD-007 | Missing contact method goes to cleanup | Pass |
| RD-008 | Missing unit/property identifier goes to cleanup | Pass |

## Decision Gate
Synthetic gate passes. Next safe step is to request a redacted Altmark sample export, the named output reviewer, source report path/export, and refresh cadence. Live acceptance remains blocked until Altmark provides that sample and confirms exception rules/output owner.

## Proof-Safe Boundary
This log uses synthetic tenant/property references only. It is an internal delivery-control artifact, not public proof.
