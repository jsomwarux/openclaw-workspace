# Create-Only Capability Handshake — Builder Evidence

Date: 2026-09-14
Branch: `eve/mc-create-only-capability`
Base: `origin/eve/mc-create-only`

## Claim

Successful `POST /api/tasks?mode=create-only` responses expose the stable capability marker `writeMode: "create-only"` for both newly created and already-existing outcomes, while normal upsert/create response shapes remain unchanged.

## Acceptance criteria

- Created create-only result includes `writeMode: "create-only"`.
- Existing create-only result includes `writeMode: "create-only"`.
- Normal upsert result does not gain the marker.
- Normal create and upsert routing behavior is unchanged.
- No schema, deployment, production, or external-system change.

## Builder evidence

- TDD RED: `bun test lib/mission-control/task-write-mode.test.ts` exited 1 with three expected `Received: undefined` failures for the missing response builder; five existing mode-selection tests passed.
- Focused GREEN: `bun test lib/mission-control/task-write-mode.test.ts lib/mission-control/task-create-only.test.ts` — 10 pass, 0 fail.
- Full tests: `bun test` — 138 pass, 0 fail, 328 assertions across 27 files.
- TypeScript: `bunx tsc --noEmit` — exit 0.
- Build: `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build` — exit 0, compiled successfully, 38/38 static pages generated.
- Diff check: `git diff --check` — exit 0.

## Environment note

The isolated clone lacked `node_modules`. Both checked-in lockfiles were already stale relative to `package.json`: `bun install --frozen-lockfile` and `npm ci` refused to install without lockfile changes. Verification used a temporary symlink to the existing local Mission Control dependency tree and removed it afterward. No dependency or lockfile change is part of this patch.

## Fresh verifier commands

Run from `mission-control/` with dependencies already available:

```bash
bun test lib/mission-control/task-write-mode.test.ts lib/mission-control/task-create-only.test.ts
bun test
bunx tsc --noEmit
NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build
git diff --check origin/eve/mc-create-only..HEAD
```

Fresh verifier verdict: **PENDING**.
