# Claude Code Controller — Cohort-Two Empty-Contact Runtime Repair

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below.

```text
You are repairing one reproduced n8n runtime defect in JT Somwaru's cohort-two prospect-discovery workflow.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- remote: jsomwarux/n8n-agent
- required starting base: origin/main at 1e37f62651b3aea50da0c4c84b40087f6593cbdb
- current production workflow IDs: c2discoveryMAIN1 and c2discoveryERRH1

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely.
2. Fetch origin and verify origin/main is exactly `1e37f62651b3aea50da0c4c84b40087f6593cbdb`. If it differs, stop BLOCKED and report the actual SHA.
3. Verify `gh repo view jsomwarux/n8n-agent --json visibility,isPrivate` reports PRIVATE.
4. Create an isolated worktree and branch:
   - worktree: /Users/jtsomwaru/.openclaw/workspace/.worktrees/n8n-c2-empty-contact-repair
   - branch: eve/cohort-two-empty-contact-repair
   - base: origin/main
5. Read the merged blueprint, workflow generator, N07B/N08/N09 code, pipeline harness, runtime-shape capture tooling, and the relevant tests before changing anything.

Reproduced failure evidence:
- Authorized manual pilot execution 1716 ran on local n8n 2.14.1.
- N07 returned 400 HPD registration rows.
- N07B emitted two chunks of 200 registration IDs.
- N08's public HPD contacts requests returned valid empty JSON arrays and therefore emitted ZERO n8n items.
- n8n silently ended the workflow at N08 with status `success`; N09 and every downstream node never ran.
- No Anthropic/model call occurred. No cohort, artifact, completion marker, Mission Control write, suppression call, heartbeat write, or send occurred. State hashes were unchanged.
- Public read-only sampling found no contact rows for registration pages at offsets 0, 400, 800, 1200, 1600, or 2000. Offset 4000 did contain contact rows. Do NOT hard-code offset 4000 or mutate the cursor to disguise the defect.
- The fixture harness missed this because it invokes N09 directly with `[]`, bypassing n8n zero-item propagation.
- A separate release-contract defect was reproduced: the documented D3 `N8N_RESTRICT_FILE_ACCESS_TO` value omits `/Users/jtsomwaru/.openclaw/workspace/reports/outreach-pipeline`, even though N04 reads the daily preflight there.

Required behavior:
1. A valid empty HPD contacts response must not terminate the workflow silently.
2. Preserve one explicit runtime item that carries the empty contacts result into N09, using a shape proven on n8n 2.14.1.
3. N09 must distinguish that exact valid-empty transport shape from malformed contact data. It must not weaken field/schema validation for non-empty responses.
4. On a valid empty contact result, N09 must continue through the already-approved seed-roster path. The seed roster is an intentional source; do not invent new prospects or hard-code a data offset.
5. If both HPD contacts and the approved seed roster yield no fetchable candidates, the existing spine/sentinel contract must still run to an explicit terminal artifact/outcome. A zero-item edge must never again look like a completed pilot merely because n8n returned `success`.
6. Correct every D3 documentation/test/example value so the required allowlist preserves all three roots:
   - /Users/jtsomwaru/.n8n-files
   - /Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery
   - /Users/jtsomwaru/.openclaw/workspace/reports/outreach-pipeline
   using n8n's semicolon separator.
7. Keep both workflows inactive. Keep T1, N39, and N43H disabled. Keep zero send-capable nodes.

TDD and runtime-capture protocol:
1. Reproduce RED with a test that models a NONEMPTY N07/N07B result followed by an EMPTY N08 response. The test must fail because downstream execution disappears, not because it directly calls N09 with `[]`.
2. Capture the actual n8n 2.14.1 item shape for a loopback HTTP endpoint returning `[]`. Use an isolated n8n user folder and task-broker port; do not touch the live n8n database or workflows.
3. Check the captured runtime-shape fixture into `clients/cohort-two-discovery/test/runtime-shapes/` and guard its defining properties so it cannot be tidied into a hand-built shape.
4. Implement the smallest robust repair in the workflow generator and source. Do not solve this by hard-coding offset 4000, changing the real cursor, or adding an unbounded pagination loop.
5. Prove GREEN for:
   - 400 registrations plus zero contacts continues into N09 and the seed roster;
   - zero contacts cannot bypass schema checks for a malformed non-empty response;
   - zero contacts plus an empty seed roster reaches an explicit terminal no-cohort outcome rather than disappearing;
   - a normal non-empty contacts response remains unchanged;
   - all existing exactly-five/all-or-nothing, state-ordering, no-send, topology, credential, and inactive-boundary tests remain green;
   - the D3 allowlist contract includes all three required roots.
6. Mutation-check the new guard: temporarily remove/break the empty-result preservation and prove the new test turns red, then restore the repair.

Authorized:
- edit only the cohort-two workflow source/generator, generated workflow JSON, focused tests/fixtures, blueprint/runbook/README/FINDINGS, and a genuinely reusable tasks/lessons.md entry;
- run public read-only NYC Open Data GETs needed to reproduce the empty response;
- use an isolated local n8n 2.14.1 user folder for loopback runtime-shape capture;
- commit, push the exact confirmed branch, open a PR against main, and wait for available checks.

Not authorized:
- no Anthropic/OpenAI/model calls;
- no credential access, creation, rotation, printing, or modification;
- no real workflow activation or schedule;
- no edits to the live n8n LaunchAgent or restart;
- no live workflow/database mutation;
- no real-prospect pilot rerun;
- no Mission Control, heartbeat, suppression-owner, drafting, or send capability;
- no merge or deployment.

Verification/review:
- During implementation run focused tests only.
- When the branch appears ready, launch one fresh non-builder reviewer in a clean clone at the exact SHA.
- The reviewer must attack: zero-item propagation, malformed-empty ambiguity, seed-roster continuity, explicit terminal outcome, state non-advancement on incomplete runs, D3 allowlist completeness, inactive boundaries, and any hidden external/send path.
- Maximum two bounded repair/review cycles. A new architecture class after that means BLOCKED, not another patch loop.
- On CONFIRM, run one full clean-clone gate: all 261+ offline tests, new runtime-shape guard, topology/export validation, credential/PII scan, repository visibility, and clean worktree.
- Push the exact confirmed SHA, open a PR against main, and wait for available CI. Do not merge.

Write the handoff to:
`/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-c2-empty-contact-repair.json`

Required handoff fields:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- repo, base SHA, branch, exact final SHA, PR URL
- files changed
- focused/full/runtime-capture/reviewer/clean-clone/CI results
- inactive/no-send proof
- reproduced root cause and exact repair
- blockers
- next_owner and exact_next_action

Send exactly one event:
`openclaw system event --text "Claude lane c2-empty-contact-repair: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-c2-empty-contact-repair.json" --mode now`

Terminal response: one line only — status + handoff path.
```
