# Outreach Capability Operations

Mission Control uses four opaque, pairwise-distinct outreach capabilities:

- `review` protects review-snapshot admission and lookup.
- `decision` protects JT decision admission and lookup.
- `review-authority-write` protects server-authored review-authority admission.
- `review-authority-read` protects exact review-authority lookup.

The review and decision capabilities remain mandatory. The review-authority write/read pair is optional until an explicitly approved rotation activates it. When neither authority item exists, the existing review and decision services start normally, Next receives no review-authority environment variables, and Convex sync explicitly deletes any stale authority variables; only `/api/tasks/outreach-review-authority` remains unavailable with `503`. If exactly one authority item exists, either stored item is blank, or any of the four values collide, service launch and Convex configuration sync fail closed.

## Runtime mapping

The checked-in Swift helper encodes all four values in one versioned JSON capability set and stores that set with one macOS Keychain item update/add. `read-set` returns the whole set in one captured pipe response; the Node wrapper validates the exact versioned shape, all nonblank values, and pairwise distinction without putting values in arguments or logs. A complete authority pair adds the same three variables to both the Next.js process and local Convex configuration:

- `OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY`
- `OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY`
- `OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID=openclaw:review-verifier-v1`

The verifier actor ID is a fixed, bounded server role. It is not operator-configurable. When the optional pair is absent, it is omitted from Next and explicitly deleted from Convex together with both authority capabilities.

## Explicit rotation and activation

Rotation is a configuration change and requires explicit approval. From `mission-control/`, the approved sequence is:

1. Run `node scripts/outreach-runtime-secrets.mjs install` to generate and store four new pairwise-distinct values.
2. With local Convex running, run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
3. Restart the approved Mission Control Convex and Next services.
4. Verify existing review and decision routes, then verify the authority write/read route with a synthetic no-send proof.

The install command rotates all four capabilities as one requested operation and migrates legacy installations to the single set item. If the set item is absent before migration, the runtime may read only the existing review and decision items under one owner-only lock and must treat authority as absent. Never run install merely to inspect state. Never copy capability values into source, shell arguments, documentation, or logs.

## Failure and recovery

- Missing mandatory review or decision value: startup and sync fail closed.
- Both authority values absent: existing services start; Next omits authority variables and Convex receives explicit deletions for all three authority variables.
- Partial authority pair, present-but-blank value, or any collision: startup and sync fail closed.
- Missing or stale helper binary: the wrapper checks both a silent v3 probe and a source-derived SHA-256 stamp, compiles to a private temporary executable, validates it, and atomically replaces helper plus stamp under the owner-only runtime lock.
- Failed rotation: the prior versioned set remains authoritative; no individual capability item is partially changed.
- Concurrent reads/rotation/helper replacement: `.runtime/outreach-capability.lock` serializes validation and use, preventing mixed generations and probe/use swaps.
- Missing local Convex admin configuration: sync fails without exposing credentials or capabilities.

Do not create, rotate, inspect, restart, or deploy during code verification. Tests use temporary executable fakes, lock contention, and fresh Swift compilation without invoking a real Keychain operation.
