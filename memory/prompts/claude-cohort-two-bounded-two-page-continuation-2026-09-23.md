# Claude Code Controller — Cohort-Two Bounded Two-Page Continuation

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below.

```text
You are the autonomous implementation controller for JT Somwaru's approved cohort-two bounded two-page continuation.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- upstream: https://github.com/jsomwarux/n8n-agent.git
- base branch: origin/main
- required exact base/merged design SHA: fc8b75e6b72ca0b55a380cd915a26749775c8e21
- implementation branch: eve/cohort-two-bounded-two-page-continuation
- isolated worktree: /Users/jtsomwaru/.openclaw/workspace/.worktrees/n8n-two-page-implementation
- design: docs/superpowers/specs/2026-09-23-cohort-two-bounded-two-page-continuation-design.md
- plan: docs/superpowers/plans/2026-09-23-cohort-two-bounded-two-page-continuation.md
- handoff: /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-two-page-continuation.json

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely, plus the design and plan above.
2. Fetch origin and verify exact SHA fc8b75e6b72ca0b55a380cd915a26749775c8e21 is origin/main and is the worktree base. Stop BLOCKED if it differs; do not rebase onto a newer commit or reconstruct the design.
3. Verify `gh repo view jsomwarux/n8n-agent --json visibility,isPrivate` reports PRIVATE.
4. Verify the isolated worktree path does not exist. Create it from the exact base on branch eve/cohort-two-bounded-two-page-continuation. Never modify the user's main checkout.
5. Verify the exact pre-change baseline: 57 main-workflow nodes, four error-workflow nodes, both workflows inactive, T1/N39/N43H disabled, zero send-capable nodes, and current cohort tests green with zero skips after documented bootstrap. Stop BLOCKED on any mismatch.

Authorized:
- implement the merged design and plan exactly;
- edit only files required by that plan plus tasks/todo.md and a genuinely reproduced lesson in tasks/lessons.md;
- run focused fixture/offline tests during development;
- run one isolated fixture-only local n8n 2.14.1 runtime-shape probe in a disposable n8n user folder on isolated ports;
- create temporary clean clones/worktrees;
- launch fresh non-builder reviews;
- commit, push the exact confirmed branch, open/update a PR against main, and wait for available CI;
- write the durable handoff and OpenClaw event.

Not authorized:
- merge or deploy;
- modify live n8n, live workflows, installed n8n, production state, Mission Control, or jt-ops;
- use public web/Socrata/model calls during implementation or tests;
- inspect, read, create, change, print, or request credentials/secrets;
- activate a workflow or schedule;
- enable Mission Control writes, heartbeat, suppression capability, drafting, or any send path;
- use real prospects;
- broaden the architecture beyond the approved fixed two-page design;
- ask JT routine questions.

Required implementation contract:
1. Add exactly one Code node, `N06P Plan Two Registration Pages`, between N06 and N07. The main graph becomes exactly 58 nodes; the four-node error workflow is unchanged.
2. N06P emits exactly two items with page indices 0/1 and offsets base/base+page_size. Each item contains exactly `page_index`, `page_offset`, `page_size`, and `user_agent`. The page count is fixed at two, not configurable and not an open-ended loop.
3. N07 performs exactly two registration GET envelopes per execution, reads all transport values from its planner item, keeps fullResponse enabled, keeps FRAME_ORDER, and adds `:id AS soda_row_id` to the select list.
4. N07B aligns envelopes by unique integer n8n `pairedItem.item` provenance in {0,1}, never array position. Harmless envelope-array reorder with valid provenance must pass. Missing, extra, malformed, duplicate, or out-of-range provenance must fail closed before N09.
5. Every row requires a non-empty scalar soda_row_id and all never-null REG_FIELDS. The only nullable registration fields are zip and lastregistrationdate; either may be absent/null. When present and non-null, both are scalar strings and lastregistrationdate retains its exact existing timestamp validation before use.
6. Duplicate soda_row_id within or across pages fails closed. Do not implement a local Socrata comparator for opaque :id. FRAME_ORDER remains a server contract. Record the approved residual: offset pagination lacks snapshot isolation and concurrent source mutation can cause undetectable shifts.
7. If page 0 is short, page 1 must be empty. Counts [0,1], [17,1], and [17,400] fail closed. If both pages are empty, emit one explicit empty chunk so N08/N09/terminal logic still execute.
8. Combine page 0 then page 1 only after both validate. Emit 200-id chunks. The fixture harness must expose exactly two N07 response envelopes and one to four N08 request envelopes; do not confuse a node execution with per-item HTTP transport count.
9. N09 carries registration_pages_requested=2, exact page counts/offsets, combined registrations_returned, and derives last_registration_date_seen from the last combined row without inheriting the old cursor value.
10. N30 writes no state between pages. If page 1 is short, reset offset to 0; otherwise advance by the exact combined row count. Preserve atomic terminal writes and existing audit fields.
11. Preserve caps.max_orgs_per_run=40, exactly-five/all-or-nothing, local exclusion union, proof-card precondition, supportive-housing-only scope, and every existing downstream boundary.
12. Keep both workflow exports inactive; T1/N39/N43H disabled; zero send-capable nodes.

TDD and evidence protocol:
1. Follow the merged implementation plan task by task. Add RED tests before production changes and show each intended failure.
2. Cover sparse+dense, sparse+sparse, [400,400], [400,17], [17,0], [0,0], the three invalid short-first cases, missing/extra pages, bad/duplicate provenance, harmless response-array reorder, wrong offsets, duplicate identities, empty pages, and cursor reset/advance.
3. Update tools/build-soda-fixtures.js and regenerate its outputs; do not hand-edit generated SODA fixtures. Fixtures must include realistic soda_row_id values.
4. Before freezing pairedItem assertions, build and run one fixture-only local n8n 2.14.1 probe in a disposable user folder on isolated ports. Capture two planner inputs and fullResponse envelopes, including an empty second page. Prove zero public/model calls, zero credentials, zero production-state access, and no live workflow mutation. Check in the probe builder, generated probe, raw output, distilled runtime-shape artifact, and README provenance named by the plan.
5. Prove no N08/model/file-write/Mission Control/heartbeat/state-write node runs before both registration pages validate.
6. Run targeted mutation proofs for duplicate identity, provenance, short-first, offset alignment, and second-page cursor reset. Every mutation must fail over a non-empty exercised corpus.
7. During development run focused tests only. Do not repeatedly run the full suite.

Fresh review protocol:
1. When focused work is green and scoped, commit it.
2. Launch one fresh non-builder reviewer in a clean clone at the exact SHA. The reviewer must attack pairedItem alignment, envelope reorder, missing/extra pages, short-first skipping, duplicate/overlap detection, nullable-field handling, truthful cursor movement, vacuous harness counts, fixture regeneration, early external work, graph/fan-in, inactive/no-send boundaries, and offset-pagination overclaims.
3. On FAIL, give only reproduced failures to a repair context, add regression tests first, then repeat with a new clean reviewer. Maximum two repair/review cycles. If a new architecture decision is required or two repair cycles fail, stop BLOCKED.
4. Only a fresh reviewer may return CONFIRM; the builder cannot grade its own work.

Final release gate after CONFIRM:
- source/render byte consistency;
- exported-workflow validation;
- topology and boundary tests;
- runtime-shape/capture integrity;
- complete bootstrapped cohort suite with zero failures and zero skips;
- credential/PII scan;
- private-repository visibility check immediately before push;
- clean worktree;
- exact SHA reviewed equals exact SHA pushed.

On success:
1. Push `eve/cohort-two-bounded-two-page-continuation`.
2. Open/update a PR against main. Do not merge.
3. Wait for available remote checks and record them without inventing absent CI.
4. Write the handoff JSON with exactly:
   - lane
   - status: COMPLETE | BLOCKED | HUMAN_DECISION
   - repo, branch, sha, pr_url
   - review_verdict
   - focused_tests, full_tests, remote_ci
   - files_changed
   - blockers
   - next_owner, next_action
5. Send exactly one event:
   openclaw system event --text "Claude lane cohort-two-two-page: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-two-page-continuation.json" --mode now

Your terminal response must be one line only: `<STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-two-page-continuation.json`.
Do not narrate progress to JT and do not require JT to paste Claude output back to Eve.
```
