# Claude Code Continuation — Cohort-Two n8n Decisions

Continue in the existing Mac Mini Claude Code session/worktree for:

- repository: `/Users/jtsomwaru/projects/n8n-agent`
- branch: `eve/cohort-two-discovery-impl`
- required starting head: `1276119fa5df9a66f1610cbd7a8c260a017b93fd`
- handoff: `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-build.json`

Verify the branch, exact head, handoff, and clean worktree before editing. Stop `BLOCKED` if they differ.

JT/Eve decisions:

1. **D12 APPROVED.** Correct the blueprint, graph comments, node notes, spine table, topology gate, and all implementation docs to n8n 2.14.1's measured `executionOrder: "v1"` rule: sibling branches are ordered by canvas position, topmost first, then leftmost; exact positional ties are forbidden. Preserve the intended invariant that every work subtree completes before its convergence branch. Treat connection-array order as non-authoritative.

2. **D1 APPROVED.** Apply the proven hash-last re-derivation:
   - homepage: `N10C[0] -> N12 -> N11`
   - page: `N16C[0] -> N18 -> N19 -> N19F -> N20 -> N17`
   Update readers, linear segments, terminal nodes, tests, captures, and documentation exactly as the runtime evidence requires. Hash the same bytes that are persisted.

3. **D8: DROP THE CHECK.** Remove N19's `content-length === byte_length` truncation test. A genuine truncated response already becomes a transport-failure item. Retain status, content-type, size, final-host, and binary/write-integrity guards. Correct every claim from “raw fetched bytes” to **the decompressed response bytes delivered by n8n/axios**; `content_sha256` and the persisted snapshot must bind to those identical decompressed bytes.

4. **D11 APPROVED WITH THIS DESIGN.** Add one main-workflow node, `N09D Prepare Output Directories`, using `n8n-nodes-base.executeCommand` v1 plus a checked-in fixed helper under `clients/cohort-two-discovery/tools/`.
   - It is a terminal sibling branch from N09.
   - Canvas order must make N09D run first, the N09F fetch subtree second, and N13 convergence last.
   - Run once per N09 item. For a normal item it creates only:
     `out/<run_id>/prospects/<prospect_id>/snapshots/`.
     For the sentinel it creates only `out/<run_id>/`.
   - The helper must hard-code/resolve the approved cohort-two root; validate `run_id` as Crockford ULID and `prospect_id` against the exact safe slug grammar before filesystem access; reject traversal, separators, shell metacharacters, symlinks, and paths outside the root; use recursive mkdir only; emit no input data or secrets.
   - The Execute Command expression may interpolate only values already validated by N09, and the helper must independently revalidate them. Use the fixed absolute Node executable and helper path. No arbitrary command or user-controlled path.
   - Empty/incomplete directories are harmless: without a valid final `COMPLETE.json`, the binder must refuse the run. Add hostile tests for injection, traversal, sentinel, zero-candidate, concurrent/retry idempotency, and work-before-convergence ordering.
   - Main workflow count becomes **57**; companion remains 4. Update every count, node inventory, topology assertion, capture, and handoff.

5. **D3 APPROVED AS A RELEASE PREREQUISITE, NOT FOR EXECUTION NOW.** Update the deployment/runbook and tests to require:
   `N8N_RESTRICT_FILE_ACCESS_TO=/Users/jtsomwaru/.n8n-files;/Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery`
   Preserve the existing default path and add only the cohort-two root. Do **not** edit the LaunchAgent, restart n8n, activate workflows, or perform go-live in this lane. Continue controlled CLI validation with a process-local environment. Eve will apply the LaunchAgent change and approved restart only after the completed branch receives `CONFIRM` and immediately before inactive deployment/go-live proof.

Implementation continuation:

- Implement all 18 real Code-node bodies and the approved 57-node graph.
- Repair the already identified D2/D10/D13 issues and retain all previously proven boundaries.
- Update the two imported local workflows only as `active:false`; T1, N39, and N43H remain disabled; no send-capable node.
- Make zero real prospect/model/Mission Control/heartbeat/suppression calls.
- Run focused tests during development.
- Then run one fresh non-builder review in a clean clone against the amended exact SHA. The architecture changed by explicit decision, so this review gets up to two bounded repair cycles. Stop `BLOCKED` on any new unresolved architecture decision.
- On `CONFIRM`, run one full clean-clone gate, visibility check, credential/PII scan, exported-workflow validation, runtime-shape/topology tests, and clean-worktree check.
- Push the confirmed branch, open/update the PR against `main`, and wait for available remote checks. Do not merge, deploy, activate, schedule, restart n8n, touch credentials, or send.

Update `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-build.json` and send the existing OpenClaw completion event. Terminal response: one line only — status plus handoff path.

Separate security incident, out of this lane: do not inspect, print, rotate, or edit the exposed OpenRouter credential. JT/Eve will handle rotation and containment separately.
