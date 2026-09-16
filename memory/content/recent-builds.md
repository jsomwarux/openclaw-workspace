# Recent Builds Log

*Updated automatically when builds complete — by overnight agent (Step 5b) and by Eve in-session when JT confirms a build is done.*
*Read by content-generate as the primary source for Wednesday case studies and build-in-public posts.*
*Entries expire after 30 days — remove stale entries during weekly synthesis.*

## Format

```
## [Build Name] — [YYYY-MM-DD]
**What:** [1-sentence description of what was built]
**For:** [client name, or "internal" for Eve/personal builds]
**Outcome:** [metric, result, or capability unlocked — be specific: "$1,000 project", "runs every 14 days", "replaced 18 hrs/week"]
**Demonstrates:** [skill or capability this proves — e.g., "n8n workflow automation", "Agentforce multi-topic routing", "RAG over external catalog"]
**Content angle:** [suggested post angle for Wednesday LinkedIn or build-in-public X — 1 sentence]
**Status:** [complete | in-progress | review-needed]
```

---

<!-- Entries appended below — most recent first -->

## Cohort-Two Verified-Channel Owner Adapter — 2026-09-15
**What:** Added a read-only, fail-closed adapter that proves exactly one currently published organization email from a Git-bound contact surface without storing channel state as durable authority.
**For:** internal.
**Outcome:** PR #40 merged as `d015aa43`; 685 builder tests and hostile parser/network review passed before merge, and exact post-merge GitHub validation passed all ten jobs. The adapter remains inactive and cannot send.
**Demonstrates:** SSRF-resistant owner adapters, DNS/IP pinning with TLS hostname verification, hostile URI/email parsing, immutable evidence binding, and approval-gated delivery architecture.
**Content angle:** Internal control work only unless tied to a real cohort-two result; the practical lesson is that a reachable channel must be re-observed from its owner, not copied into a prospect record and trusted later.
**Status:** complete.

## Mission Control Universal Action Cards — 2026-09-15
**What:** Added typed exact steps, paste-ready prompt, paste/use destination, observable done state, and append-only feedback to Mission Control task cards.
**For:** internal.
**Outcome:** PR #4 merged as `68757613`; 204 tests, TypeScript, and the 41-route build passed; live verification round-tripped every field, preserved two feedback entries, rejected malformed/replacement writes with HTTP 400, and removed the synthetic test task with the active-task count restored to 47.
**Demonstrates:** backward-compatible schema evolution, action-card UX, append-only human feedback, hostile-request validation, and live deployment verification.
**Content angle:** Internal control work only unless paired with a real cohort-two decision where exact steps and preserved feedback changed the outcome.
**Status:** complete.

## Mission Control Immutable Outreach Review Contract — 2026-09-15
**What:** Deployed immutable outreach review snapshots, server-owned two-cycle allocation, and JT draft/snapshot-bound approve-or-reject decisions behind separate fail-closed capabilities.
**For:** internal.
**Outcome:** PR #2 merged as `10ba8982`; protected runtime capabilities were stored in Keychain and live-proved with two admitted review cycles, a blocked third cycle, immutable JT rejection, and wrong-capability denial; 202 full tests, 22 fresh focused tests, TypeScript, and the 41-route build passed.
**Demonstrates:** immutable human-decision surfaces, least-privilege capability separation, authenticated approval boundaries, and deployment verification.
**Content angle:** Internal control work only unless paired with buyer-facing evidence that immutable human review prevented a real workflow error.
**Status:** complete.

## AI Workflow Growth OS Checkpoint 1B — 2026-09-14
**What:** Merged the stateless `jt-ops` to Mission Control bridge, shared evidence validator, and inactive weekly-heartbeat renderer after deploying Mission Control's atomic create-only endpoint.
**For:** internal.
**Outcome:** Mission Control live no-overwrite behavior was verified; `jt-ops` PR #36 merged as `a9f3a690`; the exact post-merge `main` run passed all nine CI jobs; production writes and heartbeat scheduling remain deliberately inactive pending separate approval.
**Demonstrates:** cross-repository contract design, atomic task admission, fail-closed evidence validation, independent verification, and approval-gated deployment.
**Content angle:** The useful systems lesson is that an agent bridge should create a new decision packet or do nothing; it should never silently mutate a human-owned task.
**Status:** complete.

## Bounded Nightly Validation Operating System — 2026-08-24
**What:** Replaced broad night-autonomy loops with a deterministic three-phase controller and strict Mission Control admission/view layer.
**For:** internal.
**Outcome:** Controller suite passed 20 tests; Mission Control passed 126 tests and a 38-page isolated build; 60 systems were classified with revival triggers; the 11:15 PM ET cron passed repeated silent empty-queue runs; cron volume stayed healthy at 11 enabled jobs and 59 weekly invocations.
**Demonstrates:** bounded agent orchestration, independent-verifier gates, evidence privacy and integrity, idempotent task admission, Mission Control product integration, and regression-driven cron deployment.
**Content angle:** Useful only when tied to the practical design lesson that autonomous agents should keep weak research out of the human task list and promote only verified action.
**Status:** complete.

## Evidence-Backed Job Hedge Pipeline — 2026-08-22
**What:** Rebuilt the dormant job-market automation around evidence-backed competitiveness, live-posting checks, weekday direct briefs, and on-demand application packages.
**For:** internal.
**Outcome:** Weekday research and Tue/Thu submitted-application tracking are active; the legacy auto-builder remains disabled; direct-fit gates require 80% must-have evidence and a $150K floor; GPT-5.6 Sol is the default package model; independent verification confirmed both cron routes, guards, and archived rollback artifacts.
**Demonstrates:** agent workflow redesign, evidence-based candidate screening, cron governance, model-routing controls, and independent verification.
**Content angle:** Internal operating-system work only; not a standalone public post unless tied to an actual interview-rate outcome.
**Status:** complete.

## MSI / Marketsmith Nexus SOW — 2026-08-18
**What:** Delivered and closed an 80-hour fixed-scope Nexus analytics/platform engagement with all four SOW deliverables accepted.
**For:** client work, anonymized for public/proposal use until permission.
**Outcome:** Client technical lead independently re-verified on MSI systems and confirmed acceptance to the exec team on 2026-08-17; proof stack includes 500+ test cases, six quality checks, 224 mutation-tested behaviours, four independent spend-total query grains agreeing to the cent, full fiscal-calendar source verification, and 11 defects found/fixed in case-study framing.
**Demonstrates:** analytics QA, governed AI implementation, mutation testing, independent verification, fixed-scope client delivery.
**Content angle:** The useful proof is not that a dashboard shipped. It is that independent checks, source verification, and client-side re-verification made the work safe to accept.
**Status:** complete.

## Mission Control Today Drawer Trust Fix — 2026-08-10
- **What:** Fixed the Today inspection drawer so status actions mutate tasks, duplicate Inspect/Open controls do not appear for plain inspection tasks, proof warnings only show when proof is actually required, and rank audit rows render human-readable values.
- **For:** Internal operating system / JT + Eve task routing.
- **Outcome:** `bun test lib/mission-control` passed 109 tests, `bunx tsc --noEmit` passed, `bun run build` passed, and a live Playwright smoke against `localhost:3000` verified no raw audit internals leaked and the Done button emitted `PATCH /api/tasks` with `status: "done"` while intercepted.
- **Demonstrates:** regression-driven product repair, dashboard trust, task-action wiring, and proof-aware UI display.
- **Content angle:** If an operating dashboard leaks internal scoring fields or dead action buttons, the ranking system loses trust even when the data is right.
- **Status:** complete.

## Passive Income Strategist Recovery + Mission Control Startup Repair — 2026-07-27
**What:** Recovered the Passive Income Strategist fallback report/delivery path and repaired Mission Control startup scripts for the installed Homebrew `node@22` path.
**For:** internal Eve operations.
**Outcome:** Strategist guard verification returned `ok=true`, `fresh_for_report=true`, and `problems=[]`; Telegram digest marker refreshed to message `25289`; Mission Control `/api/tasks` returned 248 active tasks after Next.js and Convex started.
**Demonstrates:** cron/artifact recovery, delivery-marker verification, internal ops self-healing, and local service repair.
**Content angle:** A cron saying OK is not proof. The artifact, fresh delivery marker, and downstream task API need to agree.
**Status:** complete.
