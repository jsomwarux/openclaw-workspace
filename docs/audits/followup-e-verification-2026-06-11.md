# Follow-up E Verification Sweep - 2026-06-11

Backup: `docs/audits/followup-e-backups-20260611164648/`.

## Results
- Status: cron fallback from Follow-up A is not live; Moonshot/Kimi remains blocked by billing and default fallback list is empty.
- Status: watchdog cooldown auto-clear is live; `scripts/gateway-watchdog.sh` clears `usageStats` and restarts through `restart-gateway.sh` when the exact openai-codex cooldown pattern appears.
- Delivery-rate recompute: not calendar-dated yet; Mission Control task `j572j139cb89jkpf91h7abz24988f1hp` says run 7 days after fallback actually lands.
- Sonnet preflight: initial cron runtime smoke failed because `openrouter/anthropic/claude-sonnet-4-6` was absent from `agents.defaults.models`; after the approved exact allowlist entry and gateway restart, rerun returned `SONNET_PREFLIGHT_OK`.
- Nash Groq override: removed from `9a384044-f89f-46b5-9ba5-ca909b72ac27`; `openclaw cron get` reports `model=None`.
- Guard enhancement: `scripts/model_routing_guard.py --include-disabled` now checks cron `payload.model` against configured/runtime-allowlisted models and passed.
- Memory trim: `MEMORY.md` is 6,721 bytes.
- Convex residual risk: `scripts/eve_audit_collect.py` redacts `--instance-secret [value]`; Weekly Systems Review first-Sunday ritual now checks upstream env/keychain/config support.
- Cleanup task: Mission Control task `j57cg7ht391v2n4vwckm8mqmpd88e6g5` created for 2026-07-11.

## Non-Bootstrap Injected File Sizes
- `SOUL.md`: 5,267 bytes.
- `IDENTITY.md`: 1,201 bytes.
- `USER.md`: 4,704 bytes.
- `SECURITY.md`: 3,199 bytes.

## Verification Commands
- `openclaw cron run 60c2a353-3df9-4aee-a63e-1770120fa1cb --wait --expect-final` -> `SONNET_PREFLIGHT_OK`; temp job deleted after success.
- `python3 -m py_compile scripts/model_routing_guard.py scripts/eve_audit_collect.py`
- `python3 scripts/model_routing_guard.py --include-disabled`
- `python3 -m json.tool ~/.openclaw/openclaw.json`
- `python3 -m json.tool ~/.openclaw/cron/jobs.json`
- `openclaw cron get 9a384044-f89f-46b5-9ba5-ca909b72ac27`
