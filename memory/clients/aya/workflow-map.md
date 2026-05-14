# Workflow Map — Aya Delivery OS

## Current State
1. Aya has completed prior dashboard work, active StreetEasy scraper work, pending co-living dashboard quote, and stalled acquisitions dashboard thread.
2. Client OS now separates active delivery, pending expansion, stalled work, and reusable IP capture.
3. Proof/public claims are blocked until acceptance evidence and redaction boundaries exist.

## Roles / RACI
| Step | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Define deliverable inputs | JT / Aya contact | JT | Aya stakeholder | Eve |
| Build/run deliverable | JT | JT | Eve if documentation support needed | Aya contact |
| Confirm output usefulness | Aya contact | Aya stakeholder | JT | Eve |
| Capture acceptance evidence | JT | JT | Aya contact | Eve |
| Redact/anonymize proof | Eve / JT | JT | Aya if permission needed | Internal only |

## Systems Involved
- Aya source files/inputs for each deliverable
- StreetEasy/source search surfaces for scraper work
- Dashboard/reporting outputs
- Client OS files in this folder

## Edge Cases / Exceptions
- Private property/deal details cannot appear in reusable IP.
- Scraper pages may change, block, or return stale/missing fields.
- Co-living dashboard scope may change after approval.
- Acquisitions dashboard should not be repeatedly chased after stalled follow-ups.

## Target State
1. Every active Aya deliverable has an acceptance checklist.
2. Every accepted output has evidence, support path, and redaction boundary.
3. Reusable dashboard/scraper patterns are extracted into templates using anonymized/synthetic examples.

## Automation Boundary
- Manual judgement to preserve: relationship follow-up timing, proof permission, final client acceptance, interpretation of property/deal context.
- Repeatable steps to automate: input contract generation, output checklist, recurring dashboard status, scraper run/failure logging.
- Human approval gates: external/client messages, proof publication, any claim using client results.
