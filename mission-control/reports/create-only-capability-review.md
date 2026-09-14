# Create-Only Capability Handshake — Builder Evidence

Date: 2026-09-14
Branch: `eve/mc-create-only-capability`
Base: `origin/eve/mc-create-only`

## Release order

Review, merge, and deploy this Mission Control capability before activating the
dependent jt-ops adapter/heartbeat write path at commit
`af60141200d2b7d8802b5c8f05e675be1e04889b` or any descendant. The client must
remain dry-run until `POST /api/tasks/create-only` returns
`writeMode: "create-only"`. Merge,
deployment, and schedule activation remain separate JT approvals.

## Claim

Mission Control exposes a dedicated `POST /api/tasks/create-only` endpoint that performs atomic create-only admission and returns the stable capability marker `writeMode: "create-only"`; older deployments cannot route that request into ordinary mutable task POST behavior.

## Acceptance criteria

- Created create-only result includes `writeMode: "create-only"`.
- Existing create-only result includes `writeMode: "create-only"`.
- Missing dedupe keys fail before the mutation callback runs.
- The legacy dynamic `/api/tasks/[id]` route has no POST handler, so an unsupported dedicated path cannot mutate.
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
- Dedicated-route TDD RED: three assertions failed because `app/api/tasks/create-only/route.ts` was absent; the legacy no-POST test and all ordinary route-response tests passed.
- Dedicated-route focused GREEN: `bun test lib/mission-control/task-create-only-route.test.ts lib/mission-control/task-write-mode.test.ts lib/mission-control/task-create-only.test.ts` — 14 pass, 0 fail.
- Updated full tests: `bun test` — 142 pass, 0 fail, 342 assertions across 28 files.
- Updated TypeScript: `bunx tsc --noEmit` — exit 0.
- Initial dedicated-route build failed because Next.js rejects non-route exports from App Router modules; moving the injected test factory into `lib/mission-control/task-create-only-post.ts` addressed that framework boundary.
- Updated build: `NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build` — exit 0, 39/39 pages generated, including distinct route `/api/tasks/create-only`.

## Environment note

The isolated clone lacked `node_modules`. Both checked-in lockfiles were already stale relative to `package.json`: `bun install --frozen-lockfile` and `npm ci` refused to install without lockfile changes. Verification used a temporary symlink to the existing local Mission Control dependency tree and removed it afterward. No dependency or lockfile change is part of this patch.

## Fresh verifier commands

Run from `mission-control/` with dependencies already available:

```bash
bun test lib/mission-control/task-create-only-route.test.ts lib/mission-control/task-write-mode.test.ts lib/mission-control/task-create-only.test.ts
bun test
bunx tsc --noEmit
NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build
git diff --check origin/eve/mc-create-only..HEAD
```

Fresh verifier verdict: **PENDING**.
