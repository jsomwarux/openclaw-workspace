# Altmark n8n HTTPS + Google OAuth Migration Plan — 2026-05-21

Purpose: make Altmark's local-first automation environment reliable enough for Google Sheets/Drive OAuth and client-facing workflow runs without turning tomorrow into an improvised infrastructure session.

## Why This Matters
- Google OAuth usually rejects or degrades local/plain HTTP callback URLs.
- Altmark's workflows are now moving from build/handoff into reliable operation.
- A stable HTTPS endpoint + production-ready OAuth app is prerequisite infrastructure for Google Sheets/Drive integrations, supportability, and future workflows.

## Current Known State
- Dedicated workflow PC installed at Altmark office on 2026-05-19.
- Insurance expiration workflow is finished but post-install acceptance/payment proof still needs capture.
- Mission Control has a high-priority Eve task: `Altmark: Migrate n8n to HTTPS and publish Google OAuth app` targeted for 2026-05-21 to 2026-05-22.
- Do not change auth/model config or store secrets in workspace files.

## Non-Negotiables
- No client secrets/API keys in notes, code, Drive, screenshots, or repo files.
- No public proof/referral claims from this work until Altmark acceptance/payment gates clear.
- Keep local-first posture: sensitive Altmark files stay on Altmark-controlled machine/network unless explicitly approved.
- If a firewall/router/domain decision is needed, pause and ask JT/client rather than guessing.

## Preflight Checklist
Fill before changing anything.

| Item | Status | Notes |
|---|---|---|
| Can JT access the Altmark workflow PC/admin session? | Unknown | Needed before migration. |
| Current n8n URL and port known | Unknown | Capture privately, do not paste secrets. |
| Current n8n data directory backed up | Unknown | Backup before URL/credential changes. |
| Current workflow export created | Unknown | Export active workflows before migration. |
| OAuth provider/project owner known | Unknown | Google Cloud project/account must be clear. |
| Domain/subdomain decision made | Unknown | Prefer stable domain/subdomain over temporary tunnel. |
| HTTPS termination method chosen | Unknown | Reverse proxy/Tailscale Funnel/Cloudflare Tunnel/etc. depends on client environment. |
| Callback URL finalized | Unknown | Must match n8n external URL exactly. |

## Migration Sequence

### 1. Backup first
- Export active n8n workflows.
- Backup n8n credentials/database using the installed environment's documented method.
- Screenshot or record current environment variables/settings privately.
- Confirm rollback path before changing URLs.

### 2. Pick the HTTPS pattern
Choose the least fragile pattern that fits Altmark's office/network.

| Option | When to use | Watchouts |
|---|---|---|
| Reverse proxy on stable domain/subdomain | Best long-term if Altmark can point DNS and open/forward required ports. | Needs DNS/router/firewall cooperation. |
| Cloudflare Tunnel | Good if inbound ports are hard and client accepts Cloudflare account/tunnel. | Must document ownership and tunnel restart behavior. |
| Tailscale/Funnel-style access | Good for private/admin access; maybe not ideal for public OAuth callbacks depending setup. | Verify Google OAuth callback can reach it reliably. |
| Temporary tunnel/ngrok | Only for short test/debug, not production. | Fragile, not client-grade. |

Recommendation: use a stable client-owned hostname and documented reverse proxy/tunnel. Avoid temporary tunnel for production OAuth.

### 3. Set n8n public URL/callback configuration
Confirm/install the equivalent of:
- public editor/webhook URL = final HTTPS URL
- webhook/callback base URL = final HTTPS URL
- secure cookies/proxy headers handled correctly if behind reverse proxy

Do not paste actual secrets into this file.

### 4. Configure Google OAuth app
In Google Cloud Console:
- Confirm correct project/account ownership.
- Set app publishing status appropriate for production/client use.
- Add authorized redirect URI exactly matching n8n's OAuth callback URL.
- Add required scopes only.
- Ensure consent screen name/support email are client-safe.
- Save client ID/secret only in the approved credential store / n8n credential UI, never workspace docs.

### 5. Reconnect n8n Google credentials
- Update/recreate Google Sheets/Drive credentials inside n8n.
- Complete OAuth consent flow.
- Confirm credentials are saved and reusable after n8n restart.

### 6. Smoke test
Create or run a minimal non-sensitive test workflow:
1. Manual trigger.
2. Google Sheets read from a test sheet.
3. Optional Google Drive list/read from a test folder.
4. Write one harmless test value or skip write if client data risk exists.
5. Confirm success after restart/reload.

## Acceptance Criteria
- n8n is reachable over a stable HTTPS URL.
- Google OAuth redirect URI matches n8n callback URL exactly.
- Google app is published/production-ready or has a documented owner-approved exception.
- Google Sheets/Drive credential connects in n8n.
- Test workflow succeeds.
- Credential still works after n8n restart/reload.
- Rollback/backups exist.
- Client OS dashboard and weekly update reflect completion.

## Rollback Plan
- Restore previous n8n URL/environment settings.
- Re-import workflow backup if needed.
- Keep old credential until new credential is confirmed stable, if possible.
- Document any failed OAuth/config state in `client-os/failure-log.md` with exact symptom and fix.

## JT Tomorrow First Action
Open this file before touching Altmark infrastructure. First concrete move: confirm access to the workflow PC/admin session and create workflow + n8n data backups before changing the public URL or OAuth settings.

## What Done Looks Like For Mission Control
Update the MC task only when all are true: HTTPS endpoint works, Google OAuth app/redirect is configured, n8n credential connects, smoke test succeeds, and Client OS notes are updated.
