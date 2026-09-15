# Convex Local Development Secret — Containment and Rotation Plan

## Scope

Mission Control currently uses Convex CLI `1.35.1` in local-deployment mode. The backend is started by `npx convex dev`; workspace launch scripts do not supply the instance secret.

## Confirmed finding

- Convex documents that a local backend runs as a subprocess of `npx convex dev` and stores state under the project `.convex` directory.
- The installed CLI exposes no command or flag for rotating the generated local instance secret in place.
- The current local deployment contains persistent state. Deleting or replacing `.convex` without an export and rollback copy risks data loss.
- Convex's self-hosted backend supports starting a backend with a newly generated instance secret, but that is a different operating mode. Changing the secret invalidates existing admin keys and sessions.

## Immediate containment

1. Treat the exposed value as compromised.
2. Keep Mission Control bound to localhost and restrict host access.
3. Do not run broad process-list commands that print command arguments. Use PID/name/resource-only diagnostics or a redacting collector.
4. Never paste, log, commit, or transmit the credential.

## Approval-gated rotation path

There is no supported in-place rotation for the current `npx convex dev` local deployment. The safe available path is a controlled local-deployment recreation:

1. Verify a fresh Convex export can be produced and inspected without exposing credentials.
2. Stop the Mission Control frontend and Convex LaunchAgents.
3. Move the existing `.convex` deployment directory to a timestamped rollback location; do not delete it.
4. Provision a new local deployment through the supported Convex CLI so it receives a new generated instance secret.
5. Import the verified export into the new deployment.
6. Restart Mission Control and verify `/api/tasks`, task counts, mutations, and the North Star audit.
7. Retain the rollback copy until JT confirms the restored data, then choose a separate approved disposal action.

Steps 2–7 require JT approval because they stop services, replace local deployment state, and may invalidate sessions. No restart, configuration change, export/import, key generation, or data move was performed during this investigation.

## Verification criteria

- Mission Control serves successfully on localhost.
- Task counts and representative records match the pre-rotation export.
- A reversible test mutation succeeds.
- `python3 scripts/mission_control_north_star_audit.py` passes.
- Diagnostic collection does not emit credential-bearing argv.

## Primary references

- Convex local deployments: https://docs.convex.dev/cli/local-deployments
- Convex self-hosted binary guidance: https://github.com/get-convex/convex-backend/blob/main/self-hosted/advanced/running_binary_directly.md

