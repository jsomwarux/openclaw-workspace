# Outreach Decision Authority Hardening Plan

**Goal:** Ensure only authenticated JT traffic can record an outreach decision, only the Mission Control server can call outreach mutations, and generic task writes cannot create a decision-eligible review card.

**Architecture:** Tailscale Serve remains the trusted identity proxy and the Next server remains bound to localhost. The decision route compares `Tailscale-User-Login` with `OUTREACH_DECISION_JT_LOGIN`, then passes an env-held `OUTREACH_DECISION_CAPABILITY` to Convex. Convex compares the capability with its protected env value before admission or decision. A dedicated outreach-review route atomically creates a create-only task with a server-stamped eligibility marker. Generic task routes reject that marker.

## Task 1: Authenticate human decisions

- [x] Add RED route tests for missing configuration, missing identity, and mismatched/spoofed identity.
- [x] Add a pure authorization helper and require it before the decision mutation.
- [x] Prove the configured JT identity reaches the mutation without client-owned authority fields.

## Task 2: Protect Convex mutations

- [x] Add RED tests proving decision/admission resolution rejects missing or wrong capability.
- [x] Require the capability in both public Convex mutation argument contracts and validate it against protected Convex environment state.
- [x] Ensure the capability is never returned or logged.

## Task 3: Server-owned review eligibility

- [x] Add RED tests proving generic POST/PATCH/create-only reject `outreachReview` and generic candidate/draft fields never render decision controls.
- [x] Add a dedicated authenticated server route and atomic create-only Convex mutation that stamps `outreachReview`.
- [x] Render controls only when the marker exactly matches the task candidate/draft identity.

## Task 4: Verify and hand off

- [x] Run focused hostile tests, the full Bun suite, TypeScript, and the isolated production build.
- [x] Inspect for secret values/logging and run `git diff --check`.
- [x] Update project contract and implementation records.
- [x] Commit explicit paths only; do not push or deploy.
