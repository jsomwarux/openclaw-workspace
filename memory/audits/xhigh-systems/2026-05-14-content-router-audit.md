# XHigh Audit — Content Calendar Router / Posted Follow-through

Date: 2026-05-14 08:20 ET
Scope: Re-audit the Content Calendar / posted follow-through system after local hardening, determine whether inbound router wiring is workspace-local or gateway/plugin-level, patch only safe local pieces, and identify the A+ path.

## Grade before / after

**Before:** A-

The deterministic posted-reply handler existed and was documented, but the two known follow-through gaps were real:
1. `content-reminder` and `content-sunday` did not write `memory/content/pending-posted-reply.json` after sending post reminders.
2. Telegram/direct inbound routing was not wired to claim `posted` replies and call `scripts/content_posted_reply_handler.py` automatically.

**After:** A / A-

Local follow-through is now stronger: reminder/Sunday prompts instruct agents to write exact pending state, a local pending-state writer exists, docs are updated, and `content_calendar_audit.py` now fails if the pending-state writer or cron prompt markers disappear.

The system is still not A+ because the final automatic inbound claim/route requires OpenClaw plugin/gateway-level wiring, not just a workspace script. Manual/main-agent handling can call the handler, but a Telegram reply beginning with `posted` is not yet deterministically intercepted before normal agent dispatch.

## Files inspected

- `memory/audits/xhigh-systems/2026-05-13-content-calendar-followthrough-hardening.md`
- `scripts/content_posted_reply_handler.py`
- `docs/agents/content-posted-reply-handler.md`
- `docs/agents/content-rules.md`
- `scripts/content_calendar_audit.py`
- `~/.openclaw/cron/jobs.json`
  - `content-reminder`
  - `content-sunday`
  - nearby/related content crons: `content-generate`, `content-generate-linkedin`, `content-generate-x`, `content-monday-send`, `Weekly Content Batch`, `Daily News Hook`, `AI Ops Teardown Weekly Draft`
- `agents/content-calendar/AGENT.md`
- `agents/content-scheduler/AGENT.md`
- OpenClaw local plugin/runtime docs/types:
  - `/opt/homebrew/lib/node_modules/openclaw/dist/plugin-sdk/src/plugins/hook-types.d.ts`
  - `/opt/homebrew/lib/node_modules/openclaw/dist/plugin-sdk/src/plugins/hook-message.types.d.ts`
  - `/opt/homebrew/lib/node_modules/openclaw/dist/hook-runner-global-D7rst51e.js`
  - `/opt/homebrew/lib/node_modules/openclaw/dist/plugin-sdk/src/plugin-sdk/plugin-entry.d.ts`
- Local plugin/config surfaces:
  - `~/.openclaw/plugins/installs.json`
  - `~/.openclaw/openclaw.json` was inspected only enough to confirm it is config surface; it was not edited.

## Files changed

- `scripts/content_pending_reply_state.py` — new local writer for `memory/content/pending-posted-reply.json`.
  - Can infer exact unposted rows from `posted-log.jsonl` by date/platform/day.
  - Can accept exact `--entries-json` from a reminder/router.
  - Supports `--dry-run`, alternate posted-log/pending paths, and JSON output.
- `scripts/content_calendar_audit.py` — now checks:
  - `content-reminder` prompt includes `content_pending_reply_state.py` and `pending-posted-reply.json`.
  - `content-sunday` prompt includes the same pending-state markers.
  - `scripts/content_pending_reply_state.py` exists and includes required safety markers.
- `docs/agents/content-posted-reply-handler.md` — documented the pending-state writer command and exact-entry mode.
- `docs/agents/content-rules.md` — updated audit scope and posted-reply rules to include pending-state creation.
- `~/.openclaw/cron/jobs.json` — patched only the two content delivery prompt payloads:
  - `content-reminder`: after sending Telegram post reminder, run `python3 scripts/content_pending_reply_state.py --date $(date +%F) --platform linkedin --platform x --source content-reminder`; include only actually sent platforms.
  - `content-sunday`: after sending Sunday posts, run `python3 scripts/content_pending_reply_state.py --date $(date +%F) --platform linkedin --platform x --day sunday --source content-sunday`; LinkedIn-only if Sunday X is blocked by `[Source]`.

No OpenClaw auth/model config, gateway internals, external messages, or real posted-log rows were changed.

## Router wiring finding

Router wiring is possible in OpenClaw, but it is **not cleanly workspace-local**.

Evidence:
- OpenClaw exposes plugin hook types for `inbound_claim`, `before_dispatch`, `reply_dispatch`, and message hooks.
- `PluginHookInboundClaimResult` can return `{ handled: boolean, reply?: ReplyPayload }`, which is the right shape for claiming a `posted` reply before normal agent dispatch.
- The relevant event includes `content`, `channel`, `senderId`, `isGroup`, `sessionKey`, and message metadata.
- No existing workspace-level router script/plugin currently registers an inbound claim hook for content posted replies.
- `openclaw plugin --help` is unavailable under current config because `plugins.allow` excludes `plugin`, and adding/installing a plugin or changing plugin allowlists would be gateway/plugin config work requiring JT approval.

Clean route:
- A tiny approved local plugin should register an `inbound_claim` hook.
- It should claim only direct Telegram messages from JT where normalized text starts with `posted` and either pending state exists or recent eligible content rows exist.
- It should run:
  `cd /Users/jtsomwaru/.openclaw/workspace && python3 scripts/content_posted_reply_handler.py --reply "$JT_REPLY" --json`
- It should return `handled: true` with the script's `confirmation` as the reply.
- On handler errors like `NO_MATCHING_CONTENT_SLOT` or `AMBIGUOUS_URL`, it should return a short actionable reply instead of dispatching to the main agent.

I did **not** edit gateway internals or plugin config because that would cross the task's safety boundary and likely require a restart/approval.

## Verification commands / results

```bash
python3 -m py_compile scripts/content_posted_reply_handler.py scripts/content_pending_reply_state.py scripts/content_calendar_audit.py
```
Result: passed.

```bash
python3 scripts/content_pending_reply_state.py --date 2026-05-13 --platform linkedin --dry-run --json
```
Result: matched one intended row only:
- line 161
- `2026-05-13 linkedin wednesday streeteasy-metric-correction-proof-discipline`

Temp-copy end-to-end test:

```bash
TMPDIR=$(mktemp -d)
cp memory/content/posted-log.jsonl "$TMPDIR/posted-log.jsonl"
python3 scripts/content_pending_reply_state.py --date 2026-05-13 --platform linkedin --posted-log "$TMPDIR/posted-log.jsonl" --pending "$TMPDIR/pending.json" --json
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn: https://www.linkedin.com/feed/update/test" --date 2026-05-13 --posted-log "$TMPDIR/posted-log.jsonl" --pending "$TMPDIR/pending.json" --skip-notion --json
python3 scripts/content_posted_reply_handler.py --reply "posted Wednesday LinkedIn: https://www.linkedin.com/feed/update/test" --date 2026-05-13 --posted-log "$TMPDIR/posted-log.jsonl" --pending "$TMPDIR/pending.json" --skip-notion --json
rm -rf "$TMPDIR"
```

Results:
- Pending writer wrote one exact pending entry.
- First handler call used `source: pending reminder state`, marked the temp posted-log row posted, added `posted_date`, `posted_at`, `posted_source`, and URL, and consumed pending state with `status: logged`.
- Second handler call returned `Already logged ✅` without duplicating mutation.
- Only temp files were changed.

```bash
python3 scripts/content_calendar_audit.py --week 2026-05-11
```
Result:
- `weekly: PASS`
- `posted_log: PASS`
- `crons: PASS`

Cron marker check:
- `content-reminder`: `content_pending_reply_state.py` present ✅, `pending-posted-reply.json` present ✅
- `content-sunday`: `content_pending_reply_state.py` present ✅, `pending-posted-reply.json` present ✅

## Remaining blockers

1. **Automatic Telegram/direct inbound claim hook is not installed.**
   - Needs approved OpenClaw plugin/config work.
   - Workspace scripts are ready; routing is the missing platform layer.
2. **First live reminder run still needs observation.**
   - Next `content-reminder` / `content-sunday` run should be checked to confirm the isolated agent actually executes the pending-state command after delivery.
   - The audit now catches prompt drift, but it cannot prove future agent compliance until a live run happens.
3. **Notion status remains optional best-effort.**
   - Handler updates Notion only when `NOTION_TOKEN` exists and exactly one matching date/platform row exists.

## Cleanest A+ path

1. Create a tiny local OpenClaw plugin: `content-posted-router`.
2. Register an `inbound_claim` hook.
3. Claim only:
   - `channel === "telegram"`
   - direct/not group
   - sender is JT / authorized direct chat
   - message text starts with `posted`
4. Run the local handler with `--json`.
5. Return the handler confirmation as the claim reply.
6. Add a dry-run/plugin test fixture for:
   - `posted LinkedIn` with pending file
   - duplicate `posted`
   - ambiguous URL across two platforms
   - non-content text ignored
7. Restart gateway through the approved restart path only after JT approves plugin/config changes.
8. After the next content reminder, verify:
   - `memory/content/pending-posted-reply.json` status is `pending`
   - replying `posted` consumes it and updates `posted-log.jsonl`
   - normal main-agent response is not invoked for that reply

## Recommendation for JT-facing summary

"Local side is now hardened: content reminders/Sunday prompts write pending state, there’s a tested local writer + handler, and the audit will fail if those pieces drift. The only thing keeping this from A+ is platform routing: we need one approved OpenClaw inbound-claim plugin so Telegram replies starting with `posted` get intercepted and logged automatically instead of going through normal chat." 
