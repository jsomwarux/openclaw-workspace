# Convex Local Backend argv Secret Finding — 2026-09-07

## Finding

The local `convex dev` parent launches `convex-local-backend` with `--instance-secret [REDACTED]` in the child process argv. That makes the credential visible to same-host process inspection.

## Local upstream status

- Installed `convex dev --help` supports `--env-file` for deployment selection, but exposes no flag for relocating the generated local backend instance secret to an environment variable, keychain, or config file.
- The secret-bearing backend command is generated internally by the Convex CLI; the workspace LaunchAgent invokes only `convex dev` and does not provide the secret itself.
- `scripts/eve_audit_collect.py` already redacts this argv field in collected audit text, but redaction does not remove the process-table exposure.

## Recommendation

Do not change runtime configuration locally. Track upstream Convex support for a secret-file/env mechanism or a local-backend launcher that avoids secret material in argv. Until then, keep process-diagnostic artifacts redacted and limit host access.

No runtime, LaunchAgent, keychain, or Convex configuration was changed.

