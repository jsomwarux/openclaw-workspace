# Claude Code Controller — Explicit Cohort-Two Ledger Recovery

Run Claude Code on the **Mac Mini** from:

`/Users/jtsomwaru/projects/n8n-agent`

Paste everything below verbatim.

```text
You are implementing one bounded, explicit recovery command for JT Somwaru's cohort-two discovery ledger.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- remote: https://github.com/jsomwarux/n8n-agent.git
- required base: origin/main at exactly 153ef6860e0a1984c78cbeed53f0a335de4f5871
- create isolated worktree: /Users/jtsomwaru/projects/n8n-agent/.claude/worktrees/c2-ledger-explicit-recovery
- create branch: eve/c2-ledger-explicit-recovery

Known live recovery contract (evidence, not a target you may mutate):
- live file: /Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery/state/discovery-ledger.json
- exact legacy byte length: 149
- exact legacy SHA-256: 80275a1a4d727ec119685c41760637f198dc5f020b75201325170c32870eb056
- exact recovered byte length: 174
- exact recovered SHA-256: b2a02ff896117a60c713187ff72bfa8fba47a1ffc1696da1d34c7eda70ee066d

The rejected branch `eve/c2-ledger-watermark-migration` and worktree
`/Users/jtsomwaru/projects/n8n-agent/.claude/worktrees/c2-pr9-release` contain an implicit bootstrap migration that failed three fresh reviews. They are evidence only. Do not build on, merge, cherry-pick, edit, delete, or reuse them.

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely.
2. Fetch origin and verify origin/main is the exact required SHA. Stop BLOCKED if it differs.
3. Verify the new worktree path and branch name are unused; create both from origin/main.
4. Write a started handoff marker first at:
   /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-ledger-recovery.json
5. Inspect origin/main's `clients/cohort-two-discovery/tools/bootstrap.js`, relevant state/ledger tests, README/FINDINGS/runbook guidance, and the rejected diff only to understand what must be removed from the design.

Task:
Create a one-time, explicit recovery tool. Normal bootstrap must remain fail-closed and must never migrate an existing ledger.

Required behavior:
1. Add a purpose-named tool under `clients/cohort-two-discovery/tools/`, for example `recover-pristine-ledger-watermark.js`.
2. The tool requires exactly one explicit `--ledger <absolute-path>` argument. Reject missing, repeated, relative, extra, or unknown arguments.
3. Accept only a regular file named `discovery-ledger.json`. Refuse symlinks, directories, missing targets, and non-regular files. Do not follow a symlink at the final path.
4. Recovery is allowed only when the file's bytes match the exact 149-byte legacy payload AND SHA-256 `80275a1a4d727ec119685c41760637f198dc5f020b75201325170c32870eb056`.
5. Write only the exact 174-byte recovered payload whose SHA-256 is `b2a02ff896117a60c713187ff72bfa8fba47a1ffc1696da1d34c7eda70ee066d`:
   - same schema version;
   - same empty entries array;
   - same universe_records 0;
   - add only `ledger_entries: 0`;
   - preserve observed_at null.
6. Write atomically in the same directory using an exclusive private temp file; fsync the file; rename; fsync the containing directory where supported; verify the final exact bytes, length, and SHA-256 before reporting success. Clean up only the tool's own temp file on failure.
7. Idempotency is allowed only for the exact 174-byte recovered payload and exact recovered hash. In that case, report already-recovered and do not rewrite the file (mtime/inode/content must remain unchanged).
8. Every other input fails closed without modifying the target: populated ledger, reformatted equivalent JSON, wrong key order, extra field, missing field, wrong schema, wrong watermark values, wrong hash, truncated file, malformed JSON, another already-current ledger, or a path swapped to a symlink.
9. Do not infer safety by parsing and comparing values alone. The byte and hash contract is authoritative.
10. `tools/bootstrap.js` on origin/main must remain behaviorally unchanged: it may create missing state files and preserve existing ones, but it must not upgrade, normalize, or rewrite an existing ledger.
11. Replace stale manual-edit guidance with one exact recovery command plus the before/after hashes. State clearly that it is valid only for this known pristine legacy artifact and is not a general migration utility.

TDD protocol:
- Write focused tests first and run them RED for the missing tool/behavior.
- Implement the minimum code to make them GREEN.
- Cover exact before→after, exact-after idempotency/no rewrite, all argument errors, symlink refusal, wrong filename/type, every malformed/wrong-byte class above, atomic-write failure cleanup, and proof that normal bootstrap neither migrates nor rewrites an existing legacy file.
- Tests must operate only on temporary files. Never point tests or the implementation session at the live ledger.
- Verify the original symptom: the recovered fixture passes the same watermark contract N03 enforces; the legacy fixture fails it.

Scope constraints:
- Do not access, read, print, rotate, or request credentials/secrets.
- Do not mutate the live ledger or any live state/config/output file.
- Do not import, deploy, activate, schedule, or execute either n8n workflow.
- Do not run a real-data pilot, public-web request, model call, Mission Control write, suppression operation, heartbeat, or send.
- Do not modify workflow JSON, Code-node source, schemas, seed roster, proof card, D3 config, LaunchAgents, or unrelated files.
- Do not merge.

Verification and review:
1. Run focused recovery/bootstrap tests during development.
2. When ready, run the complete cohort-two offline suite: `node clients/cohort-two-discovery/test/run-tests.js` from the repository root.
3. Inspect the final diff; it must contain only the explicit tool, its tests, and the minimum documentation/lesson correction required by this recovery.
4. Launch one fresh non-builder reviewer in a clean clone at the exact final SHA. The reviewer must attack exact-byte/hash binding, alternate JSON encodings, symlink/path swap, atomicity, idempotency/no rewrite, failure cleanup, accidental generalization, and any ambient bootstrap migration.
5. If FAIL, repair only reproduced bounded defects test-first and run one fresh review. Maximum one repair cycle. If another systemic class appears, stop BLOCKED.
6. On CONFIRM, run one final clean-clone full suite and verify a clean worktree.
7. Commit, run the repository-visibility gate, push the exact confirmed branch, open a PR against main, and wait for available remote checks. Do not merge.

Handoff:
Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-ledger-recovery.json` with:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- repo, base SHA, branch, exact final SHA, PR URL
- files changed
- before/after byte lengths and SHA-256 values
- RED/GREEN evidence
- focused/full/reviewer/clean-clone/CI results
- blockers
- next_owner: Eve
- exact next_action: independently verify and merge the exact SHA; then apply the reviewed tool once to the known live ledger and resume the already-authorized pilot

Send exactly one completion event:
openclaw system event --text "Claude lane explicit-ledger-recovery: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-ledger-recovery.json" --mode now

Do not narrate progress to JT and do not ask routine questions. Terminal response: one line only — status + handoff path.
```
