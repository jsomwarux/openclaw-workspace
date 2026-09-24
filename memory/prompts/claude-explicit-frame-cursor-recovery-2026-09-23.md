# Claude Code Controller — Explicit Pristine Frame-Cursor Recovery

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below.

```text
You are implementing one bounded, explicit recovery command for ONE known pristine legacy cohort-two frame cursor. This is not a general migration and must never touch live state.

Repository:
- path: /Users/jtsomwaru/projects/n8n-agent
- remote: jsomwarux/n8n-agent (PRIVATE)
- required base: origin/main at 0ff01144f2acff5eb808bd6420190705c6a7080f
- new branch: eve/c2-frame-cursor-explicit-recovery
- isolated worktree: /Users/jtsomwaru/projects/n8n-agent/.claude/worktrees/c2-frame-cursor-explicit-recovery

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely.
2. Fetch origin and verify origin/main is exactly the required base. Stop BLOCKED if it differs.
3. Verify the repository is PRIVATE.
4. Create the isolated worktree from exact origin/main.
5. Run the current fully bootstrapped cohort suite and require 449 passed, 0 failed, 0 skipped. Bootstrap only the worktree with the committed jt-ops proof card; never read or touch the live cohort state.

Known artifact contract:
- file name: frame-cursor.json
- legacy bytes: exactly the pretty-printed JSON below, including final newline; 105 bytes; SHA-256 df4e499feaac1162845a6b19c270e1ffa0842860063fd40b8ea66aa0ad4b145c
  {
    "dataset": "tesw-yqqr",
    "offset": 0,
    "last_registration_date_seen": null,
    "updated_at": null
  }
- recovered bytes: exactly the pretty-printed JSON below, including final newline; 147 bytes; SHA-256 88bbaec379d22d82a7f553cc12998d677e261b86757dad109695004c0fc05cf5
  {
    "schema_version": "c2-frame-cursor-v1",
    "dataset": "tesw-yqqr",
    "offset": 0,
    "last_registration_date_seen": null,
    "updated_at": null
  }

Task:
1. Add a separate command `clients/cohort-two-discovery/tools/recover-pristine-frame-cursor.js`.
2. Bind it to exactly `--cursor <absolute normalized path ending in frame-cursor.json>` and the exact before/after bytes, lengths, and hashes above.
3. Preserve the safety properties of the reviewed ledger recovery without refactoring or changing that tool:
   - final component must be a regular singly-linked file;
   - refuse symlinks/hard links, wrong name, missing file, malformed/reformatted/value-equal variants, populated/advanced cursors, extra keys, and every non-pinned byte sequence;
   - create a private 0600 exclusive scratch file in the same directory;
   - write the exact recovered bytes, fsync, read back, re-check the original target, atomic rename, directory fsync where supported, and final-path read-back;
   - preserve file mode;
   - report whether a failure occurred before or after target replacement;
   - exact recovered bytes are idempotent and are not rewritten.
4. Leave `tools/bootstrap.js` unchanged and fail-closed for every existing state file.
5. Add an exact operating note to FINDINGS/README with the command and pinned hashes. Remove any suggestion to hand-edit the cursor.
6. Add one durable lesson only if it contributes a new evidenced rule beyond lesson #177; otherwise reference #177 rather than duplicating it.

TDD and verification:
- Write RED tests first. Prove they fail before the command exists or before each guard is implemented.
- Cover exact recovery, exact already-recovered idempotence, wrong bytes/value-equal reformats, every advanced cursor field, wrong/missing schema, extra keys, wrong name/path, relative/non-normalized paths, symlink, hard link, FIFO/non-regular target, inode/content swaps, temp-file collisions, short writes, fsync/rename/read-back failures, mode preservation, cleanup ownership, and accurate before/after-replacement reporting.
- Prove N03 rejects the pinned legacy cursor with `cursor-schema-version-unexpected` and accepts the exact recovered cursor.
- Prove normal bootstrap keeps the pinned legacy cursor byte-for-byte, same inode and mtime.
- Mutation-test every security guard one at a time; every non-equivalent mutant must turn the suite red.
- Run focused tests during development.
- At the final SHA, run the fully bootstrapped cohort suite with zero skips.

Fresh review:
- Launch one fresh non-builder hostile review in a clean clone at the exact final SHA.
- Reviewer must mutate the byte/hash pins, path/basename checks, link/race guards, O_EXCL/0600, short-write loop, fsyncs, cleanup ownership, rename state, and final read-back; it must also try every plausible advanced cursor and value-equal reformat.
- If FAIL, repair only reproduced defects test-first and run one final fresh review. Maximum two repair cycles.
- If CONFIRM, run one clean-clone no-skips gate, visibility check, credential scan, and clean-worktree check.

Authorized:
- edit/test/commit within the isolated worktree;
- push the feature branch and open a PR after CONFIRM.

Not authorized:
- read, stat, hash, copy, or modify the live frame cursor or any live cohort state;
- modify the existing ledger recovery command or normal bootstrap behavior;
- merge, deploy, activate, schedule, run n8n, call public sources/models, access credentials, resume the pilot, or send anything.

Handoff:
Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-frame-cursor-recovery.json` with status, exact base/final SHA, PR URL, files changed, RED evidence, focused/full/no-skips results, reviewer verdict, mutation results, blockers, and exact next action.

Send exactly one event:
openclaw system event --text "Claude lane frame-cursor-recovery: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-frame-cursor-recovery.json" --mode now

Terminal response: one line only — status + handoff path.
```
