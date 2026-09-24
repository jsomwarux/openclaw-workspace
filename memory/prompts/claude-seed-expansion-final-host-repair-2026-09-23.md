# Claude Code Continuation — Final Seed-Expansion Host Guard Repair

Paste everything below into the **existing Claude Code session** for the cohort-two seed-expansion lane. Run it from `/Users/jtsomwaru/projects/n8n-agent`.

```text
Resume the existing cohort-two seed-expansion lane from its durable handoff. JT/Eve explicitly authorizes ONE final bounded repair cycle beyond the controller's original two-cycle ceiling. This authorization covers only the special-use/private hostname validation defect found by the third reviewer. It does not authorize any architecture, roster, discovery, deployment, credential, or live-state change.

Exact continuation state:
- repo: /Users/jtsomwaru/projects/n8n-agent
- worktree: /Users/jtsomwaru/.openclaw/workspace/.worktrees/n8n-cohort-two-seed-expansion
- branch: eve/cohort-two-seed-expansion
- required current SHA: cd96e8b81328f4d59c1d29122ee96e6cb69cb652
- base: origin/main at 41ef3bfb49dd6a0579377355cc5d0af7ce442093
- handoff: /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json

Before editing:
1. Read the handoff JSON completely.
2. Verify the worktree is clean, on `eve/cohort-two-seed-expansion`, at exact SHA `cd96e8b81328f4d59c1d29122ee96e6cb69cb652`.
3. Do not reset, recreate, squash, or discard the existing nine commits.
4. Reproduce the reviewer defect against the current shared helper and N03 path.

Authorized repair only:
- Make the shared `isRegistrableHost` contract reject the complete currently in-scope special-use/private suffix class:
  - `localhost`
  - `localdomain`
  - `local`
  - `internal`
  - `lan`
  - `home`
  - `corp`
  - `test`
  - `invalid`
  - `example`
  - `onion`
  - `arpa`
- The rejection must be suffix/TLD based for the current exact-one-dot registrable-host contract, not substring based. Valid public hosts such as `internal.org`, `home.org`, `example.org`, `cucs.org`, and `housingplusnyc.org` must remain valid.
- Preserve every existing rejection: schemes, paths, ports, wildcard, userinfo, IP literals, bare localhost, trailing dot, uppercase, padding, `www.`, denied hosts, duplicate hosts, and cross-organization duplicates.
- Do not broaden the accepted hostname grammar or introduce a public-suffix dependency.
- Update authored/shared source first, then regenerate N03/workflow artifacts through the checked-in generators. Do not hand-edit generated artifacts.
- Update only the FINDINGS D16 claim/lesson text necessary to state the corrected special-use-host boundary.

Mandatory TDD:
1. RED first: add a table-driven regression test that proves every listed special-use/private suffix currently passes the vulnerable path and must be rejected.
2. Include controls proving the valid public hosts above remain accepted.
3. Run the RED test and record the expected failure before production code changes.
4. Apply the minimal shared-library fix.
5. Run focused GREEN tests, then generation/equality checks.

Final verification at the apparent final SHA:
- focused seed-roster/host tests;
- complete bootstrapped suite with zero failures and zero skips;
- render/build generation equality and clean worktree;
- topology and graph invariants;
- main workflow 58 nodes and error workflow 4 nodes;
- both workflows inactive;
- T1, N39, and N43H disabled;
- zero send-capable nodes;
- credential/PII/private-IP scan;
- repository visibility remains PRIVATE;
- prove at least 10 new providers still survive and record exact names/count.

Fresh review:
- Launch one new non-builder reviewer in a clean clone at the exact final SHA.
- Scope it to the full seed-expansion contract, with special attention to the special-use/private suffix class, valid-host controls, generated-source drift, evidence freshness, geography conflicts, truthful 0-4 card copy, and inactive/no-send boundaries.
- If verdict is CONFIRM: push exact confirmed SHA, open a PR against main, wait for available checks, and do not merge.
- If verdict is FAIL: stop HUMAN_DECISION. No further repair cycle is authorized.

Prohibited:
- live n8n, live cohort state, credentials/secrets, OpenClaw config, Mission Control, model calls, public pilot, deployment, activation, schedule, heartbeat, suppression capability, outreach, drafting, or sends;
- changing provider scope, roster contents, pagination, gates, ranking, prompts, output schemas, recheck semantics, or downstream authority;
- modifying the installed n8n package;
- merging the PR.

Handoff:
- Update `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json` with final status, SHA, PR URL, exact provider count/names, all verification results, reviewer verdict/SHA, boundaries, blockers, next_owner, and exact_next_action.
- Add a `notification` object containing the exact command used, exit status, and returned JSON. Notification is mandatory for COMPLETE, BLOCKED, HUMAN_DECISION, and BLOCKED_NOTIFICATION.

Notify Eve first with:
openclaw system event --session-key agent:main:telegram:direct:6608544825 --text "Claude lane cohort-two-seed-expansion: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json" --mode now --expect-final --json --timeout 120000

Inspect and persist the returned JSON. If the event does not return acknowledged/final delivery, retry it exactly once. If the second event attempt is not acknowledged, use this one fallback:
openclaw agent --session-key agent:main:telegram:direct:6608544825 --channel telegram --deliver --reply-to 6608544825 --message "Claude lane cohort-two-seed-expansion: <STATUS>. Read /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json and continue the lane." --json --timeout 120

Persist the fallback JSON too. If neither path proves delivery, set status `BLOCKED_NOTIFICATION`; do not falsely claim Eve was notified.

Terminal response: one line only — status + handoff path.
```
