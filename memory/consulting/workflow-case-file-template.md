# Workflow Case File Template

Created: 2026-05-15
Purpose: canonical artifact for one client workflow before splitting discovery/governance/testing/runbook work across separate agents.

## Data Handling / Redaction Protocol
- Use anonymized client/workflow labels unless explicit permission exists.
- Do not include credentials, API keys, tokens, private file paths, tenant/customer names, account numbers, bank details, legal advice, or confidential strategy.
- Separate reusable workflow patterns from client-specific facts.
- Mark every claim as: verified, client-stated, inferred, unverified/TODO, or blocked.
- Proof/content/referral reuse requires the proof pipeline gate to be clean.
- Store sensitive client samples only in the client folder with redaction notes; keep this case file safe to reuse as methodology unless marked otherwise.

## Case File Metadata
- Workflow name:
- Client / anonymized label:
- Industry / vertical:
- Business owner:
- Users / approvers:
- Date created:
- Source materials reviewed:
- Sensitivity level: low / medium / high
- External-action risk: none / draft-only / sends externally / edits records / financial/legal/customer-impacting

## 1. Intake Summary
- Business goal:
- Current pain:
- Why now:
- Frequency / volume:
- Economic event: booking / collection / renewal / saved labor / avoided penalty / faster response / other
- Success definition:
- Constraints:

## 2. Current-State Workflow Map
Use steps, not theory.

| Step | Actor | Tool/System | Input | Action | Output | Friction / Failure Mode |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |

## 3. Systems, Data, and Access
- Source systems/files:
- Destination systems/files:
- Data fields required:
- Data quality issues:
- Access owner:
- Local-first/client-owned storage need:
- Integration/API constraints:

## 4. Exceptions and Hidden Dependencies
- Missing data:
- Malformed input:
- Duplicate records:
- Ambiguous owner/assignee:
- Stale data:
- Deadline/threshold changes:
- Human approval delays:
- External party non-response:
- Other edge cases:

## 5. Approval-Boundary Map
| Bucket | Actions |
|---|---|
| Can automate |  |
| Can draft |  |
| Must approve |  |
| Must not automate |  |

## 6. First Safe Build Recommendation
- Recommended first build:
- Why this is safe enough:
- Why this creates value:
- Excluded scope:
- Human approval step:
- First prototype artifact:
- Expansion trigger:

## 7. Golden + Failure Test Cases
| Case | Input | Expected Output | Risk Covered | Pass/Fail |
|---|---|---|---|---|
| Golden 1 |  |  | happy path |  |
| Failure 1 |  |  | malformed/missing data |  |
| Failure 2 |  |  | duplicate/ambiguous owner |  |
| Failure 3 |  |  | wrong-recipient/sensitive detail |  |
| Failure 4 |  |  | stale data |  |

## 8. Launch Acceptance Checklist
- [ ] Source sample approved
- [ ] Field/schema assumptions documented
- [ ] Golden cases pass
- [ ] Failure cases route safely
- [ ] Human approval screen/review path accepted
- [ ] Audit log writes correctly
- [ ] Error branch tested
- [ ] Manual fallback documented
- [ ] Owner/backup owner named
- [ ] Client signoff or pilot go/no-go captured

## 9. Rollback / Manual Fallback
- Pause/kill switch:
- Manual process if automation fails:
- Recovery owner:
- Escalation path:
- Data restore/reconciliation need:

## 10. Runbook Skeleton
- What it does:
- When it runs:
- Who owns it:
- Where outputs go:
- How to review/approve:
- Common errors:
- How to pause/restart:
- Who to contact:

## 11. Post-Launch Review Notes
- Date reviewed:
- Actual usage:
- Errors/failures:
- Manual overrides:
- User confusion:
- Approval bottlenecks:
- Recommended iteration:
- Retainer/support opportunity:

## 12. Lessons Captured
- Discovery lesson:
- Governance/risk lesson:
- Build lesson:
- Testing lesson:
- Handoff/runbook lesson:
- Client communication lesson:

## 13. Reusable Patterns Extracted
| Pattern | Reusable Trigger | Inputs | Outputs | Guardrails | Where to add |
|---|---|---|---|---|---|
|  |  |  |  |  | `memory/consulting/implementation-pattern-library.md` |

## Recommendation
Verdict: Ready / Ready after cleanup / Not ready yet
First safe build:
Do first:
Do not do yet:
Expansion trigger:
