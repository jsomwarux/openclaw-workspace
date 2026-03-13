# ACP Dispatch Config Audit — 2026-03-12

**Task:** Verify OpenClaw v2026.3.2 ACP dispatch breaking change in active config  
**Triggered by:** MC task j570082nvatqrpmzvj3tfzdk7h82fhcp  
**Reviewed by:** Overnight Autonomy Agent

---

## Finding

`~/.openclaw/openclaw.json` has **no `acp` section** at all.

Since v2026.3.2 changed `acp.dispatch.enabled` to default `true`, this means ACP routing is currently **enabled by inheritance** (not explicitly configured).

---

## Risk Assessment

**Risk level: LOW**

ACP dispatch being "enabled" does NOT mean every message or cron session automatically routes to ACP. It means:
- The gateway is willing to route to ACP agents when explicitly invoked via `sessions_spawn(runtime="acp")`
- Explicit dispatch rules would need to exist for automatic routing to occur

**Evidence of no unexpected routing:**
- All current cron jobs use `payload.kind: "systemEvent"` or `payload.kind: "agentTurn"` with `sessionTarget: "isolated"` — neither triggers ACP dispatch automatically
- No unexpected sub-agent spawns detected in session logs or overnight runs
- Cron sessions are isolated by design and do not pass through ACP dispatch pipeline

**Conclusion:** Current config is safe. The concern raised in the task description (unexpected sub-agent spawns in cron sessions) is not occurring.

---

## Recommendation

Add explicit `acp.dispatch` config to document intent clearly. This is a **documentation improvement only**, not a security fix:

```json
"acp": {
  "dispatch": {
    "enabled": true
  }
}
```

This makes the intent explicit and future-proof. JT can decide whether to set `enabled: false` if ACP routing should be gated.

**Do not apply this change without JT approval** — config writes require care (AGENTS.md: gateway config changes can drop connections if applied incorrectly).

---

## OpenRouter & Anthropic Profile Context

The active profiles in openclaw.json are:
- `anthropic:default` (mode: token — OAuth/subscription, no per-token billing)
- `openrouter:default` (mode: token — used for all non-Anthropic models)
- `groq:manual` (mode: token — fallback)

None of these profiles have ACP-specific routing rules. This confirms ACP dispatch, even in its default-enabled state, does not alter how existing sessions or cron jobs route their model calls.

## Status

✅ Audit complete. No action required. Config is safe as-is.  
📋 Optional: JT to decide whether to explicitly document `acp.dispatch.enabled` in openclaw.json.  
📝 If JT wants hard documentation of intent: add `"acp": {"dispatch": {"enabled": true}}` to openclaw.json in a future config review session.
