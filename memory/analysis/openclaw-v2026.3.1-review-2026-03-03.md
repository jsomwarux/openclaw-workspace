# OpenClaw v2026.3.1 — Impact Analysis for JT's Setup
**Reviewed:** 2026-03-03 3AM  
**Current version:** v2026.2.24  
**Target version:** v2026.3.1 (published 2026-03-02)  
**Update command:** `openclaw update` or `npm install -g openclaw@latest`

---

## 🔴 IMMEDIATE ACTIONS (do before next gateway restart)

### 1. Security: ClawJacked patch is IN this release
v2026.3.1 includes the ClawJacked WebSocket fix (first alerted 2026-03-02 12PM, msg 2259). Until updated, JT's local OpenClaw gateway is vulnerable to WebSocket hijacking from malicious web pages. **Update immediately.**

### 2. compaction.mode still set to "safeguard"
Current `openclaw.json` has `compaction.mode: "safeguard"`. Per the AGENTS.md mistake log from 2026-02-25, this should be `"aggressive"` to prevent context resets on long builds. This is NOT changed by v2026.3.1 — it must be manually fixed. Configuration correction required.

---

## ⚠️ BEHAVIORAL CHANGES (review before updating)

### 3. Thinking defaults: `adaptive` is now default for Claude 4.6
**Before:** All agents defaulted to `thinking: "low"` (budget-controlled, fast)  
**After v2026.3.1:** All Claude 4.6 agents default to `thinking: "adaptive"` (escalates reasoning depth based on query complexity)

**Cost impact:** Uncertain. Adaptive thinking uses more tokens for complex queries. Heartbeats and simple crons should stay cheap (adaptive → low for easy tasks), but deep analysis crons (overnight agent, morning brief, skills-researcher) may cost more per run.

**Options:**
- **Keep adaptive** (recommended for main session + overnight agent) — better quality reasoning, cost self-regulates
- **Explicitly set `thinking: "low"` in individual cron jobs** for lightweight heartbeats where you want guaranteed low cost

**Current config recommendation:** No change needed at the global level. If costs spike after upgrade, add per-agent `thinking: "low"` overrides to heartbeat cron jobs.

### 4. Cron/Heartbeat light bootstrap context (NEW FEATURE — opt-in)
New feature: `agents.main.heartbeat.lightContext: true` in `openclaw.json`.  
When enabled, heartbeat runs only inject `HEARTBEAT.md` instead of the full bootstrap file set (AGENTS.md + SOUL.md + IDENTITY.md + USER.md + TOOLS.md + MEMORY.md etc.).

**Potential savings:** Heartbeat currently injects ~24KB of bootstrap files per call. Light context would reduce this to ~2KB. At 10 heartbeats/day, this is a meaningful token reduction.

**To enable:** Add to `openclaw.json`:
```json
"agents": {
  "defaults": { ... existing ... },
  "main": {
    "heartbeat": {
      "lightContext": true
    }
  }
}
```
**Caveat:** Light heartbeats won't have access to TOOLS.md or MEMORY.md for proactive checks. Only enable for the heartbeat poll itself — keep cron agent turns (morning brief, overnight, etc.) at full context.

**Decision needed from JT:** Enable light heartbeats? (saves tokens, slightly less context-aware proactive checks)

---

## ✅ POSITIVE CHANGES (no action needed)

### 5. NO_REPLY strip from mixed-content
Fixed bug where `NO_REPLY` token leaked to end users when mixed with actual content. Now stripped automatically. Means if a cron accidentally includes `NO_REPLY` in a real reply, it'll be cleanly removed. No configuration needed.

### 6. Thinking fallback resilience
When providers reject unsupported thinking levels, retry with `think=off` instead of hard failure. Makes model routing more resilient during fallback chains.

### 7. Gateway/macOS supervised restart improvement
Gateway restart now uses `launchctl kickstart -k` to bypass LaunchAgent ThrottleInterval delays. This means the restart script will complete faster after upgrade.

### 8. Cron/Delivery mode none fix
Previous bug: cron jobs with `delivery: { mode: "none" }` weren't always being respected. Now fixed. Any cron that was accidentally delivering to Telegram when it shouldn't have will be silenced after upgrade.

### 9. Agents/Thinking fallback chain
When Claude 4.6 with adaptive thinking hits a provider that rejects the thinking level, it now falls back to `think=off` instead of erroring. Better resilience for the main agent.

---

## 📋 TELEGRAM DM TOPICS (new capability — JT decision)

New feature: per-DM `direct` + topic config in `openclaw.json`:
```json
"channels": {
  "telegram": {
    "direct": {
      "topics": {
        "health": {
          "skills": ["health"],
          "systemPrompt": "You are Eve's health tracking module..."
        },
        "tasks": {
          "skills": ["task-manager"]
        }
      }
    }
  }
}
```
This routes DM topics as distinct inbound/outbound sessions with their own skills and system prompts.  
**Use case for JT:** Could route health check-ins to a dedicated topic, crypto alerts to another. Reduces context bleed between different intent types.  
**Priority:** Low — nice-to-have, not urgent.

---

## 🏃 UPDATE CHECKLIST

1. ☐ `openclaw update` or `npm install -g openclaw@latest`
2. ☐ Fix `compaction.mode: "safeguard"` → `"aggressive"` in openclaw.json
3. ☐ Restart gateway via script after update
4. ☐ Verify `openclaw doctor` shows v2026.3.1 and all channels green
5. ☐ Decision: enable `lightContext: true` for heartbeat? (token savings)
6. ☐ Decision: configure Telegram DM topics? (nice-to-have)
7. ☐ Monitor cron costs for 24h post-update (adaptive thinking change)

---

## Cost Assessment
- Update itself: $0
- Post-update adaptive thinking impact: unknown but likely minor (adaptive = low for simple, medium for complex — shouldn't spike dramatically)
- lightContext if enabled: estimated ~$0.05–0.10/day savings
