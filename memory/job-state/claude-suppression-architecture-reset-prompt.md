# Claude Controller — Suppression Boundary Architecture Reset

Run in a **fresh Claude Code session on the Mac Mini** from:

`/Users/jtsomwaru/.openclaw/workspace/.worktrees/jt-ops-suppression-owner`

```text
You are the controller for an architecture-reset cycle on the suppression-owner lane. This is not another regex patch cycle.

Repository:
/Users/jtsomwaru/.openclaw/workspace/.worktrees/jt-ops-suppression-owner

Required starting state:
- branch: eve/suppression-owner-adapters
- exact head: e9fda1cdd4f1f9a2f308146a123256d7ce93462d
- clean worktree
- latest handoff: /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json

Verify all four before editing. Stop BLOCKED if any differ.

Read CLAUDE.md, tasks/todo.md, the suppression plans, origin/main...HEAD, the latest handoff JSON, and the current mail-address tests.

Architecture decision — mandatory:
The buyer-facing cold-outreach draft may not contain any normalized literal `@` character. Remove the attempt to distinguish mailbox syntax from ordinary `@` prose. After `_buyer_facing_normalised`, any `@` in subject + newline + body is a blocking finding. Keep a bounded obfuscated-address guard for explicit `(at)/(dot)` forms. This stricter rule is intentional: legitimate cold-outreach copy does not need literal `@` prose, and false positives should trigger redrafting rather than risk channel leakage.

Do not preserve or further refine the complex `MAIL_ADDRESS_RE` classifier. Remove dead matcher constants/tests that no longer describe the policy.

Required TDD changes, in order:
1. Add one focused no-channel-copy test class proving:
   - ASCII `@`, fullwidth/small-at variants after normalization, quoted local parts, address literals, dotless hosts, asymmetric spaces/tabs/newlines, and a subject/body split all block;
   - any ordinary sentence containing literal `@` also blocks by policy;
   - approved buyer-facing copy without `@` passes;
   - explicit obfuscated `(at)/(dot)` address forms block;
   - scanning remains linear on the 4,000-character limit.
2. Add missing contract vectors for **each owner**:
   - a fresh clear for fingerprint A queried with fingerprint B returns observed=false, clear=false, current=null;
   - queriedAt exactly equal to observedAt returns clear=true;
   - register `current-ignores-fingerprint` and `clear-age-must-be-positive` in SIBLING_DEVIATIONS.
3. Harden the standalone import test so every `ast.Name` load of dynamic import builtins and every relevant `ast.Attribute` use is rejected, including alias assignment such as `smuggle = __import__`.
4. In the cohort CLI `record-confirmed-send` delegate, separate the durable append from output emission. A broken/closed stdout after a successful append must not return failure or leak a traceback; use the same guarded-emission contract as the standalone entrypoint.
5. Convert every well-formed-but-invalid suppression-owner object at `_validate_suppression_owner_query` into `LaneCannotRun` with `from None`, matching non-object owner failures. It must exit 2 and leave no durable artifact.

Protocol:
- RED before each fix; focused tests only during implementation.
- Do not change architecture outside the explicit no-`@` decision.
- Do not touch unrelated files.
- After focused tests pass, run one fresh hostile non-builder review in a clean clone. Review the changed boundary only: normalized `@` blocking, obfuscation, both-owner vectors, import isolation, post-append output failure, and owner-malfunction classification.
- If that review finds another new systemic class, stop BLOCKED and do not repair again.
- On CONFIRM, run one final Python 3.12 clean-clone gate: focused suites, full suite, record validation, all checked-in CI guards, credential scan, path guard, and clean worktree.
- Push the exact confirmed branch, open/update the PR against main, and wait for remote CI.
- Do not merge, deploy, activate, schedule, access/rotate secrets, or send.

Write the final handoff atomically to:
/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json

Required handoff fields:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- exact SHA and PR URL
- review verdict
- focused/full/CI results
- files changed
- blockers
- next_owner and next_action

Send exactly one event:
openclaw system event --text "Claude lane suppression-architecture-reset: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json" --mode now

No progress recaps. Terminal response: one line only — status + handoff path.
```
