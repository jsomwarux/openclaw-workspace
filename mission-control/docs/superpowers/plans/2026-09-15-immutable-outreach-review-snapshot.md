# Immutable Outreach Review Snapshot Plan

**Goal:** Make each server-admitted outreach review task an immutable snapshot of everything JT saw, with the specialized decision mutation as the only permitted append.

**Design choice:** Keep the marker, review content, and decision on the existing task rather than introduce a second record/store. A single pure guard rejects every generic mutation when `outreachReview` exists. Scheduled bulk mutations skip review tasks. Exact lookup additionally refuses archived tasks.

## TDD sequence

- [x] Add hostile tests covering generic status, content, identity, assignee, priority, upsert, delete, auto-archive, and archived lookup.
- [x] Verify RED against current field-specific protection.
- [x] Implement the single immutable-review guard and wire every task mutation path.
- [x] Verify focused GREEN.
- [x] Run the full suite, TypeScript, production build, and secret/diff scan.
- [x] Update project notes and commit explicit paths without push/deploy.

## Fresh-verifier repair

- [x] Prove review admission and JT decision use distinct least-privilege capabilities.
- [x] Prove scheduled/bulk mutations skip both server review markers and legacy decisions.
- [ ] Rebuild from current `origin/master` by cherry-picking only scoped outreach commits.
- [ ] Re-run the complete verification matrix and audit the clean diff for unrelated ancestry.
