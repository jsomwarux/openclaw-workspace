# Outreach Capability Operations

Mission Control uses four opaque, pairwise-distinct outreach capabilities:

- `review` protects review-snapshot admission and lookup.
- `decision` protects JT decision admission and lookup.
- `review-authority-write` protects server-authored review-authority admission.
- `review-authority-read` protects exact review-authority lookup.

The review and decision capabilities remain mandatory. The review-authority write/read pair is optional until an explicitly approved rotation activates it. When neither authority item exists, the existing review and decision services start normally and receive no review-authority environment variables; only `/api/tasks/outreach-review-authority` remains unavailable with `503`. If exactly one authority item exists, or any of the four values collide, service launch and Convex configuration sync fail closed.

## Runtime mapping

The checked-in Swift helper stores the four values under separate macOS Keychain services and never prints values during installation. The Node wrapper reads them without putting them in arguments or logs. A complete authority pair adds the same three variables to both the Next.js process and local Convex configuration:

- `OUTREACH_REVIEW_AUTHORITY_WRITE_CAPABILITY`
- `OUTREACH_REVIEW_AUTHORITY_READ_CAPABILITY`
- `OUTREACH_REVIEW_AUTHORITY_VERIFIER_ACTOR_ID=openclaw:review-verifier-v1`

The verifier actor ID is a fixed, bounded server role. It is not operator-configurable and is omitted with the authority variables when the optional pair is absent.

## Explicit rotation and activation

Rotation is a configuration change and requires explicit approval. From `mission-control/`, the approved sequence is:

1. Run `node scripts/outreach-runtime-secrets.mjs install` to generate and store four new pairwise-distinct values.
2. With local Convex running, run `node scripts/outreach-runtime-secrets.mjs sync-convex`.
3. Restart the approved Mission Control Convex and Next services.
4. Verify existing review and decision routes, then verify the authority write/read route with a synthetic no-send proof.

The install command rotates all four capabilities as one requested operation. Never run it merely to inspect state. Never copy capability values into source, shell arguments, documentation, or logs.

## Failure and recovery

- Missing mandatory review or decision value: startup and sync fail closed.
- Both authority values absent: existing services start; authority variables are omitted.
- Partial authority pair, blank value, or any collision: startup and sync fail closed.
- Missing helper binary: the wrapper recompiles it from checked-in Swift source.
- Missing local Convex admin configuration: sync fails without exposing credentials or capabilities.

Do not create, rotate, inspect, restart, or deploy during code verification. Tests exercise pure configuration builders and compile the Swift source to a temporary output only.
