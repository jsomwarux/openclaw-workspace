# Mission Control Create-Only Capability Claim

## Claim

Mission Control now exposes atomic create-only task admission on a dedicated POST path that older servers cannot mistake for the ordinary mutable task route.

## Acceptance criteria

1. `POST /api/tasks/create-only` calls the atomic create-only mutation after the same admission and normalization used by task POST.
2. Both `created: true` and `created: false` results include `writeMode: "create-only"`.
3. Missing dedupe keys and unsupported older-server routing cannot invoke a mutable task mutation.
4. Ordinary `/api/tasks` create/upsert behavior remains unchanged.
5. Full Mission Control tests, TypeScript, and isolated production build pass.
6. No schema, deployment, push, production write, or external contact occurs.

## Artifact paths

- `mission-control/app/api/tasks/route.ts`
- `mission-control/app/api/tasks/create-only/route.ts`
- `mission-control/lib/mission-control/task-create-only-post.ts`
- `mission-control/lib/mission-control/task-create-only-route.test.ts`
- `mission-control/lib/mission-control/task-write-mode.ts`
- `mission-control/lib/mission-control/task-write-mode.test.ts`
- `mission-control/reports/create-only-capability-review.md`
- `mission-control/tasks/implementation-notes.html`

## Fresh verifier commands

Run from `mission-control/` with dependencies already available:

```bash
bun test lib/mission-control/task-create-only-route.test.ts lib/mission-control/task-write-mode.test.ts lib/mission-control/task-create-only.test.ts
bun test
bunx tsc --noEmit
NEXT_PUBLIC_CONVEX_URL=http://127.0.0.1:3210 bun run build
git diff --check origin/eve/mc-create-only..HEAD
```

## Verdict

PENDING fresh-context verification.
