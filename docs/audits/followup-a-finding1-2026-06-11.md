# Follow-up A - Finding 1

Date: 2026-06-11

## Moonshot Diagnosis

The Moonshot smoke-test blocker was account/provider billing state, not an OpenAI routing error and not the openai-codex cooldown bug.

Evidence:
- `openclaw models status` reports `moonshot:default` as `disabled:billing 2h`.
- Gateway logs show Moonshot `kimi-k2.6` requests returning HTTP 429 with account suspended / insufficient balance billing language.

Action required from JT:
1. Log into the Moonshot/Kimi billing dashboard for the configured account.
2. Recharge/top up or reactivate the suspended account/plan.
3. Tell Eve billing is fixed.

After JT confirms:
1. Rerun one throwaway smoke test on `moonshot/kimi-k2.6`.
2. If it routes and billing is as expected, apply the original Phase 2A fallback spec unchanged.

If Moonshot remains unsuitable, the approved alternative is OpenRouter Gemini Flash class after a throwaway smoke test, with a named cap of $5/month attributable to fallback runs and alert at $3.

## Cooldown Auto-Clear

Phase 2B already included the requested watchdog cooldown recovery.

Current behavior:
- Gateway must be HTTP-healthy.
- Latest 3 finished cron runs must be errors containing `No available auth profile for openai-codex`.
- Trigger is rate-limited to once per 6 hours via `watchdog-state.json`.
- On real trigger, watchdog clears `usageStats` in `auth-profiles.json`, backs up the auth file, and restarts via `scripts/restart-gateway.sh`.
- Every match/skip/action is logged to `~/.openclaw/logs/watchdog.log`.

Synthetic dry-run output:

```text
2026-06-11 15:42:54 [watchdog] auth cooldown trigger matched: latest 3 finished cron runs failed with openai-codex auth cooldown
2026-06-11 15:42:54 [watchdog] DRY_RUN: would clear auth usageStats and restart gateway
```

## Baseline Delivery

Phase 1 baseline delivery was:
- Delivered runs: 48
- Scheduled/executed runs in records: 76
- Delivery rate: 63.2%

Source: `docs/audits/baseline-delivery-2026-06-11.md`.

## Recompute

Safe recompute command:

```bash
python3 scripts/recompute_delivery_rate.py --days 7 --label fallback-plus-7 --json
```

Run it 7 days after the fallback actually lands.
