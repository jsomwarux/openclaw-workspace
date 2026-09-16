# Outreach Capability Operations

Mission Control uses four opaque, pairwise-distinct outreach capabilities:

- `review` protects review-snapshot admission and lookup.
- `decision` protects JT decision admission and lookup.
- `review-authority-write` protects server-authored review-authority admission.
- `review-authority-read` protects exact review-authority lookup.

The review and decision capabilities remain mandatory. The review-authority write/read pair is optional until an explicitly approved rotation activates it. When neither authority item exists, the existing review and decision services start normally, Next receives no review-authority environment variables, and Convex sync explicitly deletes any stale authority variables; only `/api/tasks/outreach-review-authority` remains unavailable with `503`. If exactly one authority item exists, either stored item is blank, or any of the four values collide, service launch and Convex configuration sync fail closed.

## Runtime mapping

The checked-in Swift source compiles only to the stable `.runtime/outreach-keychain-helper-v3` path. That v3 helper encodes all four values in one versioned JSON capability set and stores the set with one macOS Keychain item update/add. `read-set` returns the whole set in one captured pipe response; the Node wrapper validates the exact shape, nonblank values, and pairwise distinction without putting values in arguments or logs. Service launch transfers the resulting environment from the locked child to its parent only over a parent-created file descriptor 3; stdout and stderr remain nonsecret, and missing private transport fails before Keychain access. The unchanged `.runtime/outreach-keychain-helper` remains the sole owner/reader of legacy review and decision items. A complete authority pair adds the same three variables to both the Next.js process and local Convex configuration:

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

The install command rotates all four capabilities as one requested operation and migrates legacy installations by creating the single set through v3. If the set is absent, v3 reports absence and the legacy helper may read only its own review and decision items under one `lockf` operation; authority stays absent. Never run install merely to inspect state. Never copy capability values into source, shell arguments, documentation, or logs.

## Failure and recovery

- Missing mandatory review or decision value: startup and sync fail closed.
- Both authority values absent: existing services start; Next omits authority variables and Convex receives explicit deletions for all three authority variables.
- Partial authority pair, present-but-blank value, or any collision: startup and sync fail closed.
- Missing v3 helper: compile and probe privately, atomically publish the owner-only source stamp first, then publish stable v3 last; legacy bytes remain unchanged. A crash after stamp publication leaves the helper absent and safely recompilable, so Keychain installation cannot begin from a partial publish.
- Existing v3 probe/stamp mismatch: fail closed with versioned migration guidance. Never replace an existing Keychain-owning helper path.
- Failed rotation: the prior versioned set remains authoritative; no individual capability item is partially changed.
- Concurrent reads/rotation: `/usr/bin/lockf` serializes the complete short-lived operation on `.runtime/outreach-capability.lock`; the OS releases the advisory lock on process death.
- Hung helper, compile, lock, or Convex sync: bounded timeout fails closed; capabilities never enter process arguments.
- Missing local Convex admin configuration: sync fails without exposing credentials or capabilities.

Do not create, rotate, inspect, restart, or deploy during code verification. Tests use temporary executable fakes, lock contention, and fresh Swift compilation without invoking a real Keychain operation.
