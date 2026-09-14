# Atomic Create-Only Task Admission Review

Date: 2026-09-11
Branch: `eve/mc-create-only`

## Scope

This branch adds an explicit atomic create-only write path for immutable,
payload-versioned decision cards. Normal `POST /api/tasks` behavior is unchanged.
There was no deployment, Convex migration, production data write, or schedule change.

## RED

```text
$ bun test lib/mission-control/task-create-only.test.ts lib/mission-control/task-write-mode.test.ts
error: Cannot find module './task-write-mode'
error: Cannot find module './task-create-only'
0 pass
2 fail
2 errors
```

## GREEN

```text
$ bun test lib/mission-control/task-create-only.test.ts lib/mission-control/task-write-mode.test.ts
7 pass
0 fail
7 expect() calls
Ran 7 tests across 2 files.
```

## Full verification

The external Desktop worktree triggers macOS file-access hangs in Bun, so verification
ran against a byte-for-byte temporary mirror outside Desktop. The mirror used the
existing dependency directory and included the full repository so Python integration
tests retained their expected relative paths.

```text
$ bun test
135 pass
0 fail
325 expect() calls
Ran 135 tests across 27 files.
```

```text
$ bunx tsc --noEmit
(exit 0; no output)
```

```text
$ NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build
Compiled successfully
Generating static pages (38/38)
(exit 0)
```

The URL is a non-secret loopback build-time placeholder. No service was contacted.

## Guarantee

`createOnlyByDedupeKey` queries and inserts within one Convex mutation. An existing
key returns `{id, created: false}` without any patch fields. A missing key inserts
once and returns `{id, created: true}`. The explicit route mode selects that mutation;
ordinary keyed POSTs retain their existing upsert behavior.
