# Mission Control Card Contract Repair — Builder Claim

**Date:** 2026-09-15  
**Base commit:** `57c0946600215fab0e4c019a3d268fafbff1af42`  
**Status:** Awaiting fresh non-builder verification

## Claimed repair

- Invalid JSON bodies on generic task `POST` and `PATCH` return HTTP 400 before Convex is called.
- `exactSteps`, `pasteReadyPrompt`, and `pasteDestination` are type-validated before normalization or mutation.
- Blank or oversized feedback is rejected by the API parser with HTTP 400 before Convex is called.
- Valid feedback remains trimmed and append-only.

## Builder evidence

- RED: focused suite failed on malformed JSON, malformed card fields, and blank/oversized feedback.
- GREEN: `bun test lib/mission-control/task-admission.test.ts lib/mission-control/task-feedback.test.ts lib/mission-control/task-route-validation.test.ts` — 15 passed, 0 failed.
- Full suite: `bun test` — 204 passed, 0 failed.
- TypeScript: `bunx tsc --noEmit` — exit 0.
- Production build: `bun run build` — exit 0, 41 routes generated.
- `git diff --check` — exit 0.

The builder does not grade this claim. A fresh verifier must inspect the exact committed repair and return `CONFIRM` or `FAIL`.
