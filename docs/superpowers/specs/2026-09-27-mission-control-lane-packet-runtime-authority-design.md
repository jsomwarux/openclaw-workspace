# Mission Control Lane-Packet Runtime Authority Design

## Goal

Provision the deployed generic lane-packet adapter with bounded local authority while preserving every existing outreach capability and keeping live packet admission closed.

## Architecture

Create a new versioned Keychain helper and capability-set owner (`v4`) rather than replacing the published v3 helper. The v4 install migrates the validated existing four outreach capabilities through helper stdin, generates only the distinct lane-packet producer and decision capabilities inside the helper, and atomically stores the resulting six-capability set. Runtime launch resolves the trusted JT Tailscale login once, privately injects the two lane capabilities and `LANE_PACKET_JT_LOGIN` into Next, and synchronizes only the two capabilities to local Convex.

If v4 is absent, the wrapper falls back to the existing v3/legacy readers and explicitly deletes lane-packet variables from Convex and the child environment. A v4 protocol/source mismatch fails closed and requires another versioned migration. Capability values never enter argv, stdout, stderr, logs, artifacts, documentation, or shell-visible variables.

## Data flow

1. The wrapper privately reads and validates the existing four-capability set, passes it to the v4 helper through stdin, and the helper generates two mutually distinct lane capabilities with `SecRandomCopyBytes` before storing one atomic six-capability JSON set in a new Keychain service.
2. The wrapper validates the set schema, uniqueness, and nonblank values under the existing advisory lock.
3. `run-next` transports the validated runtime environment through private file descriptor 3 and launches Next with existing outreach plus lane-packet variables.
4. `sync-convex` sends existing outreach variables plus the two lane-packet capabilities through Convex's protected local admin API; it never sends the trusted login.
5. The existing LaunchAgents restart against the wrapper. No route is called with a valid producer capability, so no packet can be admitted.

## Failure and rollback

- Any partial set, collision, missing login, helper mismatch, lock failure, or Convex sync failure fails closed.
- Existing v3 bytes and Keychain data are never overwritten by the migration.
- A pre-change metadata snapshot records helper hashes, service health, task identities, and the database rollback snapshot without reading secret values.
- Rollback restores the prior runtime files and restarts both services; v4 Keychain material may remain unused until a separately approved cleanup.

## Verification

- TDD proves v4 generation, parsing, fallback, collision refusal, private transport, Next injection, Convex synchronization, stale-variable deletion, and non-leakage.
- Full Mission Control tests, TypeScript, and isolated production build pass.
- Runtime probes prove: dashboard/API healthy; missing and incorrect producer capability return 401; a JT transition for a nonexistent task returns 404 rather than 503; Next and Convex expose matching configuration only through behavior; the exact task ID set is unchanged.
- Live admission, transition of a real card, Decagon application submission, scheduling, and external sends remain closed.
