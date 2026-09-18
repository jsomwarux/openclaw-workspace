# Claude Code Controller — N08 HPD Contact Truncation Guard

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below.

```text
You are implementing one bounded pre-pilot repair for JT Somwaru's inactive cohort-two n8n discovery workflow.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- required base: origin/main at 76f998b
- workflow: workflows/cohort-two-prospect-discovery.json
- blueprint: tasks/cohort-two-prospect-discovery-blueprint.md
- existing handoff evidence: /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-c2-empty-contact-repair.json

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely.
2. Fetch origin and verify origin/main is exactly 76f998b. Stop BLOCKED if it differs.
3. Verify the main checkout's unrelated dirty files are not touched.
4. Create an isolated worktree and branch from origin/main:
   - worktree: /Users/jtsomwaru/.openclaw/workspace/.worktrees/n8n-n08-truncation-guard
   - branch: eve/n08-truncation-guard
5. Read the merged blueprint, N07B/N08/N09 implementation, renderer/source files, runtime-shape fixtures, and focused pipeline tests before changing anything.

Confirmed defect:
- N07B sends chunks of 200 registration IDs to N08.
- N08 currently requests `$limit=2000` from NYC HPD contacts dataset `feu5-w2e2`.
- Live HPD contains individual registrations with 8,688 and 2,325 contact rows, so one registration can exhaust the current page and silently drop the other registrations in its chunk.
- This cannot poison the ledger, but it can silently lose legitimate candidates and invalidate an under-five pilot result.
- Official Socrata SODA v2 semantics: `$limit` is one page, v2 has a 50,000-row maximum, and pagination uses `$limit` plus `$offset`.

Approved design:
1. Change N08's explicit `$limit` from 2,000 to 50,000.
2. Add one named constant for the N08 contact-page cap in the relevant workflow source/render path; do not scatter magic numbers.
3. In the shared N09 SODA-envelope decoder, validate each N08 response envelope independently. After validating 2xx status and array body, if an HPD-contact response body has length exactly 50,000, throw a fail-closed error whose stable reason begins `frame-source-truncated` and names the envelope index and cap.
4. A body length below 50,000, including zero, remains valid. A malformed body or non-2xx response retains the existing fail-loud behavior.
5. Do not implement pagination in this repair. If the 50,000-row sentry ever fires in a real run, that is the explicit trigger for a separately designed pagination change.
6. Keep both workflows inactive. Do not run a real-data pilot, public-model call, Mission Control write, suppression call, heartbeat write, activation, schedule, credential operation, or send.

TDD requirements:
- First reproduce RED for all of these cases at the real N08→N09 boundary:
  a. a contact response with more than 2,000 and fewer than 50,000 rows is preserved completely;
  b. 49,999 rows pass;
  c. exactly 50,000 rows fail with `frame-source-truncated`;
  d. an empty 2xx body still propagates explicitly through the repaired full-response envelope path;
  e. malformed/non-array and non-2xx bodies retain current failures;
  f. two envelopes are checked independently so one capped envelope cannot be hidden by another short envelope.
- Add a static/render guard proving the built workflow contains `$limit=50000` and the truncation sentry.
- Update the blueprint and lessons only where the verified contract changed.
- Preserve byte-identical render/source expectations used by this repository.

Efficiency:
- Run focused tests during implementation.
- Run one full clean-clone gate only at the final candidate SHA.
- Do not reopen unrelated architecture or prior repaired defects.

Review:
1. Commit the bounded repair.
2. Launch one fresh non-builder reviewer in a clean clone at the exact SHA.
3. Reviewer must attack: cap off-by-one behavior, per-envelope checking, empty-array propagation, malformed envelopes, render drift, accidental pagination claims, workflow activation, hidden external calls, and any ledger/state write before the truncation failure.
4. Maximum one repair cycle for reproduced defects. If a new systemic architecture issue appears, stop BLOCKED.
5. On CONFIRM, run the full repository gate, clean-clone replay, workflow validation, credential/PII scan, visibility gate, and clean-worktree check.
6. Push the exact confirmed branch, open a PR against main, and wait for available remote checks. Do not merge or deploy.

Handoff:
Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n08-truncation.json` with:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- repo, branch, base SHA, exact final SHA, PR URL
- files changed
- focused/full/reviewer/clean-clone/CI results
- proof both workflows remain inactive and no external side effect occurred
- blockers
- next owner and exact next action

Send exactly one event:
openclaw system event --text "Claude lane n08-truncation: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n08-truncation.json" --mode now

Terminal response: one line only — status + handoff path.
```
