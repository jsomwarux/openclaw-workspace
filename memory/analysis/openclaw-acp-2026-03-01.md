# OpenClaw ACP — Research & Activation Findings
*Date: 2026-03-01 | Researcher: Eve Overnight Agent*

---

## What Is ACP?

**ACP stands for "Agent Client Protocol"** — not "Agent Communication Protocol" as the tweet described it. The naming distinction matters: ACP is *not* a protocol for agents to communicate with each other. It's a bridge that lets **IDEs and external tools** (like the Zed editor) speak a standardized protocol over stdio, with the OpenClaw Gateway forwarding those prompts to the configured AI agent via WebSocket.

- ACP runs as a local process: `openclaw acp`
- It keeps ACP sessions mapped to Gateway session keys
- Each ACP session targets a single Gateway session key (e.g., `agent:main:main`)
- Default session prefix when not overridden: `acp:<uuid>` (isolated)

ACP is an **IDE integration protocol**, not an agent-to-agent communication layer. The tweet's framing of "Agent Communication Protocol" likely confused ACP with the broader multi-agent routing system.

---

## What Was Added in the Update

Based on current docs (OpenClaw v2026.2.24 installed, docs reflect latest):

### 1. ACP Bridge (`openclaw acp`)
Full IDE integration via the Agent Client Protocol spec. Key features:
- Attach Zed, or any ACP-compatible IDE, to any Gateway session
- Session key targeting (`--session agent:main:main`)
- Session label resolution (`--session-label "label"`)
- Session reset (`--reset-session`)
- Per-session metadata overrides (sessionKey, sessionLabel, resetSession via `_meta`)
- Built-in debug client (`openclaw acp client`)
- Token-file auth for local process safety

### 2. Thread-Bound Agents (Discord only)
New `channels.discord.threadBindings` config block that gates thread-aware routing:
- **`enabled`**: activates `/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, and bound delivery/routing in Discord threads
- **`idleHours`**: auto-unfocus threads after N hours of inactivity (0 = disabled)
- **`maxAgeHours`**: hard max age for thread binding (0 = disabled)
- **`spawnSubagentSessions`**: **opt-in** flag — enables `sessions_spawn({ thread: true })` to auto-create/bind Discord threads to sub-agent sessions. Defaults to `false`.

Thread-bound agents = Discord threads that get their own isolated agent session, with optional sub-agent spawn. The `spawnSubagentSessions` flag is the "dormant" feature referenced in the tweet — it's `false` by default and requires explicit opt-in.

### 3. Multi-Agent Routing Improvements
- `agents.list[]` for defining fully isolated agents with separate workspace, agentDir, sessions
- `bindings[]` for deterministic routing rules (peer, parentPeer, guildId, accountId, channel)
- Routing priority ladder: peer match → parentPeer → guildId+roles → guildId → teamId → accountId → channel-level → default
- `openclaw agents add <name>` wizard command

### 4. Session Maintenance System
- `session.maintenance.mode`: `warn` | `enforce`
- `pruneAfter`, `maxEntries`, `rotateBytes`, `maxDiskBytes`, `highWaterBytes`
- Default mode is `warn` — logs what would be pruned but never acts

### 5. Channel-Level Model Overrides
- `channels.modelByChannel.<channel>.<channelId>` to pin specific channel/group/topic to a model
- Applies per-session when no session-level override exists

### 6. Telegram Thread Topic Routing
- Topics (`groups.<groupId>.topics.<topicId>`) with per-topic skills, systemPrompt, requireMention
- Transcripts stored as `<SessionId>-topic-<threadId>.jsonl`

---

## Current Config Status

**Installed version:** `2026.2.24`
**Config last touched:** `2026-02-25` (wizard last run: `2026-02-21`)
**Config path:** `~/.openclaw/openclaw.json`

### Keys Checked

| Key | Status | Notes |
|-----|--------|-------|
| `channels.discord` | ❌ Not configured | Thread-bound agents N/A — no Discord |
| `channels.discord.threadBindings` | ❌ Not present | Core "dormant" feature from the tweet |
| `channels.discord.threadBindings.spawnSubagentSessions` | ❌ Not present | The sub-agent opt-in is disabled (not applicable) |
| `agents.list` | ❌ Not present | Single-agent mode only (main) |
| `bindings` | ❌ Not present | No multi-agent routing configured |
| `session.maintenance.mode` | ❌ Not set (defaults to `warn`) | Sessions grow unbounded — never pruned |
| `session.maintenance.pruneAfter` | ❌ Not set | No time-based pruning |
| `session.maintenance.maxEntries` | ❌ Not set | No count cap on sessions |
| `agents.defaults.compaction.mode` | ⚠️ `safeguard` | AGENTS.md notes it was changed to `aggressive` — config has NOT been updated |
| `agents.defaults.maxConcurrent` | ✅ `4` | Active |
| `agents.defaults.subagents.maxConcurrent` | ✅ `8` | Active |
| `session.dmScope` | ✅ `per-channel-peer` | Correctly set for single-user isolation |
| `channels.telegram.streaming` | ⚠️ `true` (boolean) | Docs say string: `partial` / `block` / `progress` / `off`. Boolean `true` is auto-migrated but flagged as legacy. |
| `hooks.internal.enabled` | ✅ `true` | Active |
| `hooks.internal.entries.boot-md` | ✅ enabled | Active |
| `hooks.internal.entries.bootstrap-extra-files` | ✅ enabled | Active |
| `hooks.internal.entries.command-logger` | ✅ enabled | Active |
| `hooks.internal.entries.session-memory` | ✅ enabled | Active |
| `tools.elevated.enabled` | ✅ `false` | Correctly disabled |
| `logging.redactSensitive` | ✅ `tools` | Active |
| `gateway.tailscale.mode` | ✅ `off` | No Tailscale — expected |

### ACP-Specific
No ACP keys exist in `openclaw.json` — and none are needed. ACP is a **CLI command**, not a gateway config feature. The command `openclaw acp` is available immediately; no config activation required. The IDE-side setup (e.g., Zed `settings.json`) lives outside openclaw.json.

### What's Actually "Half-Working"
The tweet's claim about features needing manual activation is **accurate for this setup**:
1. **Thread-bound agents** — Fully dormant. Requires Discord, which isn't configured.
2. **spawnSubagentSessions** — Dormant by design (opt-in, requires Discord, `false` by default).
3. **Session maintenance** — In `warn` mode. It discovers and logs stale sessions but never prunes them. Sessions will accumulate indefinitely until `mode: "enforce"` is set.
4. **Compaction mode discrepancy** — AGENTS.md records a decision to switch to `aggressive`, but the actual config still says `safeguard`. This is either a stale AGENTS.md note or a change that was intended but never applied.
5. **ACP** — Available but zero IDEs connected. Not a blocker for current workflow (Eve operates via Telegram, not an IDE).

---

## Recommended Activations

Only safe changes documented below — no gateway restart, no SECURITY.md/AGENTS.md modification.

> ⚠️ All changes below require a gateway restart to take effect per standard config update flow. Changes are documented only; do not apply without JT review.

### 1. Session Maintenance — High Priority
Current: `warn` mode (sessions grow forever). Recommended: enforce with conservative limits.

```json
// ADD to openclaw.json under "session"
"session": {
  "dmScope": "per-channel-peer",
  "maintenance": {
    "mode": "enforce",
    "pruneAfter": "30d",
    "maxEntries": 500,
    "rotateBytes": "10mb",
    "resetArchiveRetention": "14d"
  }
}
```

**Why safe:** These are the documented defaults for `enforce` mode. Running `openclaw sessions cleanup --dry-run --json` first will show projected impact before committing.

### 2. Fix Compaction Mode — Medium Priority
Config says `safeguard`, AGENTS.md says `aggressive` was chosen (Feb 25 decision). One of them is wrong.

```json
// CHANGE in openclaw.json under agents.defaults.compaction
"compaction": {
  "mode": "aggressive",      // was: "safeguard"
  "reserveTokens": 40000,
  "reserveTokensFloor": 12000,
  "keepRecentTokens": 10000
}
```

**Action needed:** JT should confirm whether the switch to `aggressive` was intentional. If yes, apply this change. If no, update AGENTS.md to remove the stale entry.

### 3. Telegram Streaming Mode — Low Priority
Current: `streaming: true` (boolean, legacy format). Docs recommend explicit string.

```json
// CHANGE in openclaw.json under channels.telegram
"streaming": "partial"   // was: true (boolean, auto-migrated but legacy)
```

**Why safe:** `partial` matches the behavior of `true`. This is a cleanup, not a behavior change. Low priority.

### 4. ACP + Zed IDE Integration — Optional / JT Decision
No config change needed in openclaw.json. To connect Zed editor to Eve's Gateway:

Add to `~/.config/zed/settings.json`:
```json
{
  "agent_servers": {
    "OpenClaw (Eve)": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp", "--session", "agent:main:main"],
      "env": {}
    }
  }
}
```

**Impact:** Lets JT (or a coding agent) drive Eve's main session directly from Zed. No openclaw.json change. No restart required. Activates immediately when Zed is opened.

### 5. Thread-Bound Agents + Discord — Future / Not Applicable Now
Requires Discord bot setup first. Document for future:
```json
// ADD when Discord is configured
"channels": {
  "discord": {
    "threadBindings": {
      "enabled": true,
      "idleHours": 24,
      "maxAgeHours": 0,
      "spawnSubagentSessions": true
    }
  }
}
```
**Current status:** Skip. Discord not in JT's stack.

---

## Multi-Agent Impact

### Current Architecture
```
JT (Telegram) → Eve main (agent:main)
                    ├── Overnight sub-agents (spawned via sessions_spawn)
                    └── Coding agents (pty=true, background)
```

### What ACP Changes (If Activated)
- ACP adds an IDE entry point. JT could talk to `agent:main:main` from Zed in addition to Telegram.
- Sub-agents spawned from Zed sessions would use `acp:<uuid>` session keys by default, isolated from Telegram sessions.
- No conflict risk with existing Telegram workflow.

### What Thread-Bound Agents Would Change (Hypothetically)
- If Discord were added, `spawnSubagentSessions: true` would let Discord threads auto-spawn their own sub-agent session. Each Discord thread = isolated agent brain.
- This is the key "half-working" feature from the tweet — powerful for team setups, irrelevant for solo Telegram-only use.

### What Multi-Agent Routing Would Change
- `agents.list` would let JT run a second agent (e.g., a dedicated coding agent with its own workspace, SOUL.md, and session history) side-by-side with Eve.
- Currently not needed — sub-agents handle task delegation adequately.
- Would matter if JT adds a second Telegram bot or channel account.

### Overnight Sub-Agent Impact
- No impact from ACP (overnight uses `sessions_spawn`, not ACP).
- Session maintenance enforcement (#1 above) *does* affect overnight — it means overnight sub-agent sessions get pruned after 30 days. This is correct behavior.
- Compaction mode correction (#2) affects context handling during long overnight tasks. `aggressive` compaction means the agent compacts earlier and harder, protecting against context exhaustion at the cost of slightly less full-history access. AGENTS.md rationale was to prevent context resets on long builds.

---

## Action Items for JT

### Requires JT Review/Approval
| Item | Reason | Risk |
|------|--------|------|
| Apply session maintenance `enforce` mode | Change from warn → enforce; will prune sessions after 30d | Low — run dry-run first with `openclaw sessions cleanup --dry-run --json` |
| Confirm compaction mode | AGENTS.md vs config discrepancy — which is correct? | None until applied |
| Zed ACP setup | Optional IDE integration | Zero — no openclaw.json change needed |
| Discord setup + threadBindings | Only if JT wants Discord channel | Medium — requires new bot token |

### Eve Can Handle After JT Approves
| Item | Action |
|------|--------|
| Session maintenance config | Edit `openclaw.json`, restart gateway via script |
| Compaction mode fix | Edit `openclaw.json`, restart gateway via script |
| Telegram streaming cleanup | Edit `openclaw.json`, restart gateway via script |
| Write to AGENTS.md | Update compaction decision note to match actual config state |

### Nothing to Do (Features Not Applicable)
- ACP in openclaw.json: no config needed — it's a CLI command
- Thread-bound agents: requires Discord, not in JT's stack
- Multi-agent routing: overkill for current single-Telegram setup

---

## Summary

The tweet's "half the features don't work until you manually activate them" is accurate but overstated for JT's setup. The specific dormant items that *actually matter* here:

1. **Session maintenance** → warn-only mode; sessions will accumulate forever. Fix: enforce mode. **Do this.**
2. **Compaction mode** → config/AGENTS.md desync. Clarify and align. **Minor but worth fixing.**
3. **Thread-bound agents** → Dormant because Discord isn't in the stack, not because of a config miss.
4. **ACP** → Not a config issue. Available via CLI when JT wants IDE integration.

No emergency actions needed. Session maintenance is the only one with real long-term consequence if left in `warn` mode.
