---
name: "claude-lane-controller"
description: "Delegate bounded Claude Code lanes with reviewed PRs and verified direct Eve handoffs."
---

# Claude Lane Controller

Use this procedure when Claude Code should implement a bounded coding or workflow lane while Eve retains architecture, release acceptance, credentials, deployment, and external-action control.

## Procedure

1. **Define one bounded lane.** Name one repository/worktree, branch, exact starting SHA, upstream base, governing plan/spec, allowed files, prohibited actions, absolute JSON handoff path, and Eve's exact OpenClaw session key. Finish when every precondition is explicit and independently checkable.

2. **Launch one controller session in the owning repository.** Tell Claude to verify the exact branch, SHA, and clean worktree before editing; read `CLAUDE.md`, `AGENTS.md` when present, lessons files, the governing spec, and the complete base-to-head diff. Require a `BLOCKED` handoff and stop if any precondition differs.

3. **Grant only internal build authority.** Allow inspection, edits, focused tests, commits, isolated temporary clones/worktrees, fresh non-builder review, confirmed branch push, PR creation/update, and CI waiting. Prohibit merge, deployment, activation, schedule changes, purchases, credentials/secrets, external sends, unrelated edits, and routine questions to JT.

4. **Develop test-first.** Run focused RED/GREEN tests during implementation. Do not repeatedly run the full suite. Finish when the bounded feature passes focused tests and the worktree contains only scoped changes.

5. **Review from a fresh context.** A non-builder reviewer uses a clean clone at the exact SHA and attacks only changed spec, authority, security, and integration boundaries. The builder never grades its own artifact. Finish when the reviewer returns `CONFIRM` or lists reproducible failures with evidence.

6. **Repair no more than twice.** On `FAIL`, give only reproduced failures to a repair context, add regression tests, and repeat fresh review. After two failed repair cycles, stop with `BLOCKED`; do not broaden architecture or continue phrase-by-phrase patching. If repeated failures evade a blacklist or static source checker, determine whether that checker is the real runtime authority boundary. When production instead executes an exact reviewed Git blob inside an isolated runtime, keep the checker as a narrowly described regression guard and rely on blob pinning plus isolation for authority; never extend the blacklist while claiming it is a complete sandbox.

7. **Run one final release gate.** On `CONFIRM`, run the full clean-clone suite and checked-in guards once. Push/open the PR only when this gate passes. Never merge.

8. **Write the durable handoff.** Save JSON at the declared path with exactly:
   - `lane`
   - `status`: `COMPLETE`, `BLOCKED`, or `HUMAN_DECISION`
   - `repo`, `branch`, `sha`, `pr_url`
   - `review_verdict`
   - `focused_tests`, `full_tests`, `remote_ci`
   - `files_changed`
   - `blockers`
   - `next_owner`, `next_action`

   For `HUMAN_DECISION`, `next_action` must contain one exact canonical proposal, its evidence source, and the literal approval/revision response expected from JT. Do not offer alternate model-written wording or interpret an approval phrase inside Claude. Stop the lane; Eve records JT's decision against the exact proposed bytes, updates the authoritative artifact, and then resumes or relaunches the controller.

9. **Notify Eve directly and verify delivery.** Run:

   `openclaw system event --session-key "<exact-eve-session-key>" --text "Claude lane <lane>: <status>; handoff at <absolute-path>" --mode now --expect-final --json`

   Require exit 0 and a successful JSON response. If delivery fails, retry the same command once. If it still fails, preserve the completed handoff and return `BLOCKED_NOTIFICATION`; do not claim Eve was notified. Return only one terminal line: status plus handoff path and notification result. Do not narrate progress to JT or require JT to paste Claude output into Eve.

## Concurrency and dependency rules

- Run at most two Claude lane controllers concurrently.
- Concurrent lanes must use different repositories/worktrees and have no write dependency.
- Never run builder and reviewer concurrently on the same change.
- Never run blueprint and implementation concurrently.
- A dependent lane starts only after the prerequisite handoff and required merge/deployment are complete.

## Eve handoff behavior

Eve reads the JSON handoff and compact diff, verifies the claimed SHA/PR/CI, and continues from the declared next action. Eve does not repeat Claude's broad discovery or development loop. Eve keeps protected-secret handling, Mission Control reconciliation, final deployment, synthetic live proof, and external-action decisions.

## Failure controls

- Missing repository, branch, SHA, authority, credential, governing artifact, or exact Eve session key produces `BLOCKED`, not reconstruction or guessing.
- Tool/model policy failure is reported as infrastructure failure, not an implementation verdict.
- Never treat green builder tests as release acceptance without fresh review.
- Never let a handoff claim merge, deploy, activation, schedule, purchase, or send unless JT separately authorized and the owning controller actually verified it.
