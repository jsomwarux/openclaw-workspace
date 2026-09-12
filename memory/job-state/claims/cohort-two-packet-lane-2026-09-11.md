# Builder claim: cohort-two packet lane — 2026-09-11

## Claim

Branch eve/cohort-2-packet-lane implements the inactive deterministic cohort-two
packet lane requested, without discovery, sends, schedules, deployment, model API
calls, or production Mission Control writes.

## Acceptance criteria

1. Qualified input fails closed on buyer, channel, signal, proof, suppression,
   mailbox, segment, and structure gates.
2. Prepare writes traceable work queue jobs referencing standalone prompt, voice,
   copy-standard, proof-card, and ranked source hashes.
3. Worker prompt produces one M1 plus metadata using supplied sources only.
4. Verify rejects stale sources, unlicensed questions, proof overreach, false
   control/live claims, segment mismatch, duplicate/fixed structures, and cycle 3.
5. Render emits one cohort packet with seven human fields, source links, unknowns,
   unresolved mailbox risk, JT send ownership, stop-on-reply, done condition, and a
   Checkpoint 1B adapter dry-run.
6. Required unit, validation, security, path, test-count, staging, registry,
   receipt, visibility, compile, and diff gates pass.
7. Branch is pushed and PR #37 is stacked on eve/checkpoint-1b, not main.

## Artifacts

- Worktree: /Users/jtsomwaru/Desktop/jt-ops-cohort-2-eve
- Review: reports/cohort-2-lane-review.md
- Implementation notes: tasks/implementation-notes.html
- Copy standard: docs/standards/outreach-copy-standard.md
- Field diff: docs/qualified-prospect-contract.md
- Code: scripts/cohort_packet_lane.py
- Tests: scripts/tests/test_cohort_packet_lane.py
- Initial commit: 163a3f9
- Pull request: https://github.com/jsomwarux/jt-ops/pull/37

## Exact verifier commands

Run from /Users/jtsomwaru/Desktop/jt-ops-cohort-2-eve:

    git status --short --branch
    git diff origin/eve/checkpoint-1b...HEAD --check
    .venv/bin/python -m unittest discover -s scripts/tests
    .venv/bin/python scripts/validate.py
    .venv/bin/python scripts/ci/credential_scan.py
    .venv/bin/python scripts/ci/path_guard.py origin/eve/checkpoint-1b..HEAD
    .venv/bin/python scripts/ci/atom_phrasing.py
    .venv/bin/python scripts/ci/check_test_count.py
    .venv/bin/python scripts/ci/check_staging_size.py
    .venv/bin/python scripts/ci/check_routine_registry.py
    .venv/bin/python scripts/ci/check_receipt_names.py
    .venv/bin/python scripts/ci/check_routine_visibility.py
    .venv/bin/python -m py_compile scripts/*.py scripts/ci/*.py scripts/tests/*.py
    git diff --check
    git diff --cached --check

Adversarially inspect the requirements against the code, prompt, copy standard,
fixtures, review report, and PR base. The builder does not append the verdict.
