# Mission Control Outreach Suppression Owner

## Inactive-by-default boundary

Every suppression HTTP route and every direct Convex suppression query/mutation
checks `OUTREACH_SUPPRESSION_OWNER_ENABLED === "true"` before capability
validation or database access. The flag is nonsecret and must remain absent until a
separate activation approval. Disabled surfaces return only a sanitized 503.
The packaged runtime launcher and Convex synchronization explicitly delete the
flag, so an inherited or stale `true` value cannot activate the owner.

## Owner event API

- `POST /api/tasks/outreach-suppression` requires JT's trusted Tailscale identity
  plus the existing decision capability. Mission Control fixes `actorId` to `jt`,
  owns sequence/time/event ID/revision, and only appends.
- `GET /api/tasks/outreach-suppression` requires the existing review-authority
  read capability and an exact prospect, organization-fact, and channel tuple.
- Same request ID plus the same canonical payload returns the original event;
  changed payload conflicts.

The implementation consumes `contracts/outreach-suppression-v1-vectors.json`, the
same fixture used by `jt-ops`, for revision and state-machine parity.

## Immutable review binding and dual clear

New review submissions may carry a copy-free `suppressionBinding` that must match
the protected gate Git binding. Before storage, Mission Control fetches the exact
upstream-reachable gate and admission blobs from the canonical protected origin;
it verifies both raw blob hashes, the canonical gate-artifact hash, the gate's
admission references, and the admitted prospect/organization identities. Caller-
supplied self-consistent hashes are not authority. Its canonical hash covers
repository, commit, gate path/blob SHA-256 and Git blob OID, admission path/blob
SHA-256 and Git blob OID, gate artifact, channel
attestation/revision, prospect, organization fact, and channel fingerprint. Bound
reviews require an opaque `review_<20 lowercase hex>` authority ID.

After protected-origin verification, the Next.js owner creates a domain-separated
Web Crypto HMAC over the exact immutable review submission using the decision capability.
Convex verifies that server-only attestation before any database access and never
stores it. Possession of the review-card write capability alone cannot admit a
suppression binding. Legacy review submissions without a suppression binding remain
compatible and do not require an attestation. Suppression-bound review admission checks
the suppression feature flag and all four pairwise-distinct capabilities before protected
Git, HMAC, or database access at both the HTTP and direct Convex boundaries. Protected-binding mismatches return a
sanitized 400; protected-origin, SSH, and timeout failures return a sanitized 500.

`POST /api/tasks/outreach-suppression/clear` accepts exactly that review ID.
The browser sends only that JSON body; it never receives or submits a capability.
Behind the flag the route requires JT's trusted Tailscale identity, validates the
pairwise-distinct server capability configuration, injects the decision capability, loads the
binding server-side only from one exact authoritative, approved, immutable active review,
derives retry-stable owner request/evidence IDs, records the
consulting owner first through the fixed CLI, then records Mission Control.
Undecided, rejected, archived, or identity/hash-mismatched reviews never reach either owner.
Its success response validates and projects only each owner's event ID, owner
revision, and observation time; malformed dependency success data fails closed.

The consulting command is fixed to `/usr/bin/python3`, canonical script/cwd,
five-second timeout, and a one-variable nonsecret environment. Stderr, extra stdout,
or malformed owner output blocks.

## Pre-send receipts

`POST /api/tasks/outreach-pre-send-receipt` uses the review-card write capability.
It records one exact copy-free receipt only when the immutable review is
authoritative, approved, and matches review/draft/decision/binding hashes. Mission
Control owns the opaque ID, server time, and receipt hash. There is no update/delete
path. GET by opaque ID uses the review-authority read capability.

Raw channel data and message copy are forbidden from bindings and receipts.

## Capability matrix

- event write / dual clear: decision capability + JT identity;
- state read: review-authority read capability;
- receipt write: review-card write capability;
- receipt read: review-authority read capability.

All four roles must be nonblank and pairwise distinct. Generic task routes cannot
access suppression state.
