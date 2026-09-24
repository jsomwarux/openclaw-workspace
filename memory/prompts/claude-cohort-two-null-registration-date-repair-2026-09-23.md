# Claude Code Controller — Cohort-Two Nullable Registration-Date Repair

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below.

```text
You are the autonomous repair controller for one bounded cohort-two discovery defect found by the authorized live pilot.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- remote: https://github.com/jsomwarux/n8n-agent.git
- required base: origin/main at ef641355f014d79096c5c0cac6591224d934b23b
- create a fresh isolated worktree under /Users/jtsomwaru/projects/n8n-agent/.claude/worktrees/
- branch: eve/c2-null-registration-date-repair

Read completely before editing:
1. CLAUDE.md
2. tasks/lessons.md
3. clients/cohort-two-discovery/README.md
4. clients/cohort-two-discovery/FINDINGS.md sections relevant to N07/N07B/N09/N30, frame paging, state, runtime-shape captures, and lessons 136, 141–163, 177
5. the exact committed workflow, renderer/source files, test harness, and cursor/state contracts

Verify the base SHA and clean worktree before editing. Stop BLOCKED if either differs.

## Reproduced production evidence

The reviewed frame-cursor recovery was merged and applied successfully. N03 now accepts the exact recovered cursor. The resumed authorized pilot produced n8n execution 1719, which failed closed at N09 before any Anthropic/model call or cohort artifact:

`N09: frame-schema-drift: tesw-yqqr.lastregistrationdate`

Live source facts captured 2026-09-23:
- endpoint: `https://data.cityofnewyork.us/resource/tesw-yqqr.json`
- N07 requests:
  `registrationid,buildingid,boro,housenumber,streetname,zip,communityboard,lastregistrationdate,registrationenddate`
  ordered by `lastregistrationdate DESC`, limit 400, cursor offset
- that exact ordering returns rows with null `lastregistrationdate` first; Socrata omits a nullable field from each JSON object when its value is null
- the first page therefore contains no `lastregistrationdate` keys, although the column still exists
- read-only aggregate evidence:
  total rows = 203,887
  rows with lastregistrationdate = 200,545
  rows with registrationenddate = 203,887
  max lastregistrationdate = 2026-07-31T00:00:00.000
  null lastregistrationdate rows = 3,342
- metadata still defines `lastregistrationdate` as `LastRegistrationDate`, type `calendar_date`
- current N09 incorrectly treats absence of that nullable key across one page as dataset schema drift
- current cursor has `last_registration_date_seen`, but inspect whether production code ever derives it; do not preserve dead or misleading semantics by assumption
- execution 1719 left frame cursor, ledger, carryover, and output artifacts unchanged

## Task

Find and repair the ROOT CAUSE, test-first. Do not merely suppress the error.

The repaired design must satisfy all of these:

1. A legitimate page whose nullable `lastregistrationdate` values are all null must not be misclassified as schema drift.
2. A real source-schema removal/rename must still fail closed before downstream research/model work.
3. Paging must be deterministic and complete for the policy you choose. Add an explicit stable tie-breaker; never rely on order among equal timestamps.
4. Do not silently discard the 3,342 null-date registrations. If any rows are intentionally excluded, that is an architecture decision and must be justified with authoritative evidence plus a completeness accounting. Default preference is to preserve coverage.
5. Cursor semantics must be truthful. If `last_registration_date_seen` is retained, derive and test it. If it is not a real paging/control input, document its actual audit role; do not invent behavior.
6. Preserve offset advancement, exactly-five/all-or-nothing behavior, exclusion authority, state fail-closed rules, and the 50,000-row N08 truncation sentry.
7. Both workflow exports remain `active: false`; T1, N39, and N43H remain disabled; zero send-capable nodes.
8. No real model calls, no credential access, no live n8n edits, no workflow import/deploy, no pilot run, no schedule/activation/write/send.

## Allowed evidence gathering

- read-only GETs to the two public NYC Socrata datasets and their metadata endpoints
- read-only inspection of local n8n execution 1719/database records
- local/offline tests and fixture generation from minimized public response shapes

Do not copy unnecessary personal/contact data into fixtures. Use the minimum fields and synthetic/minimized rows needed to reproduce transport semantics.

## TDD protocol

1. Add the smallest regression tests first and run them RED against exact base.
2. Required cases include:
   - page where every row omits nullable `lastregistrationdate`;
   - mixed null/non-null page;
   - non-null page;
   - true required-column removal/rename still fails;
   - deterministic ordering/tie behavior;
   - cursor advancement and any `last_registration_date_seen` semantics;
   - render/source/export parity;
   - execution cannot proceed to model/research branches on true schema drift.
3. Prove each new test fails for the intended reason, not a fixture/harness default.
4. Implement one minimal root-cause fix.
5. Run focused tests during development.
6. Run the full no-skips gate only at the final candidate SHA with the required bootstrapped proof card and `C2_JT_OPS` set correctly.
7. Mutate/break the new guard at least once and prove the regression suite turns red; restore it and prove green.

## Review/release

- Inspect the final diff for scope. No unrelated refactor.
- Launch one fresh non-builder hostile review in a clean clone at the exact final SHA.
- Reviewer attacks nullable-field handling, actual schema-removal detection, deterministic pagination, page-boundary duplicates/omissions, cursor truthfulness, vacuous fixtures/assertions, source/render/export drift, and inactive/no-send boundaries.
- If FAIL, repair only reproduced defects test-first; maximum two repair/review cycles.
- If a new architecture decision is genuinely required after evidence gathering, stop HUMAN_DECISION with the exact alternatives and evidence. Do not guess.
- On CONFIRM, run one clean-clone full gate with zero skips, credential/PII scan, source/render/export parity, and clean worktree.
- Verify repository visibility is PRIVATE immediately before push.
- Push the branch, open a PR against main, and wait for available checks. Do not merge.

## Handoff

Write:
`/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-null-registration-date-repair.json`

Required fields:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- base SHA, branch, exact final SHA, PR URL
- root cause and chosen policy
- files changed
- RED evidence
- focused/full/mutation/reviewer/clean-clone results
- live/public evidence used
- proof inactive/no-send boundaries remain intact
- blockers
- next owner and exact next action

Send exactly one internal event:
`openclaw system event --text "Claude lane null-registration-date-repair: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-null-registration-date-repair.json" --mode now`

Terminal response: one line only — status + handoff path.
```
