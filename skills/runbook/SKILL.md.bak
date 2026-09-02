# Runbook Skill — Operational Diagnosis

## Overview

This skill converts a symptom or error description into a structured diagnosis: symptom → likely causes → investigation steps → confirmed root cause → minimal fix.

Use it any time something in JT's stack is broken and the root cause isn't obvious. The protocol enforces one variable at a time, ranks causes by probability, and produces a concise output JT can act on immediately.

---

## When to Use

Trigger phrases:
- "why is X broken"
- "debug this"
- "how do I fix [error]"
- "what's causing [symptom]"
- "[system] is not working"
- "something's wrong with [cron/agent/workflow]"
- "debug this: [error message]"
- "investigate [symptom]"
- "why isn't [thing] firing/running/delivering"

---

## Investigation Protocol — 5 Steps

### Step 1 — Identify the Symptom
Capture exactly:
- What error or behavior was observed (exact message if available)
- When it first occurred (timestamp if known)
- What was working before and isn't now

> Ask JT for the exact error if he only described it vaguely. One clarifying question max.

### Step 2 — Check Recent Changes (last 24h)
Before forming hypotheses, check what changed:
- Deploys or code pushes (git log, n8n workflow edits)
- Config changes (openclaw.json, global.env edits)
- Cron runs (any new jobs, modified payloads, timing changes)
- Credential updates or rotations (API keys, tokens)
- Model routing changes (auth-profiles.json, models.json)

Command for recent git activity across key projects:
```bash
for d in ~/projects/jtsomwaru-com ~/projects/n8n-agent ~/projects/agentforce-agent; do
  echo "=== $d ==="; git -C $d log --oneline --since="24 hours ago" 2>/dev/null || echo "(no repo)";
done
```

### Step 3 — Narrow to Most Likely Cause
Rank candidate causes in this order (highest probability first):
1. **Credential / auth** — bad API key, expired token, revoked key, wrong profile
2. **Network / connectivity** — port down, process crashed, Tailscale dropped
3. **Config** — wrong model ID, bad env var, misconfigured cron payload
4. **Code** — TypeScript error, missing dep, broken import, logic bug
5. **External API** — provider outage, rate limit, schema change

Pick the top 1-2 candidates. Do not investigate all five simultaneously.

### Step 4 — Verify the Hypothesis
Run the specific check that confirms or rules out your top candidate. One check at a time.

Examples:
```bash
# Credential check
source ~/.config/env/global.env && echo $OPENROUTER_API_KEY | cut -c1-10

# Network check
curl -s http://localhost:3210/health | head -20

# Config check
cat ~/.openclaw/agents/main/agent/auth-profiles.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('usageStats',{}), indent=2))"

# Cron check
openclaw cron list | grep -A3 "[job-name]"

# Build check
cd ~/projects/[project] && npm run build 2>&1 | tail -30
```

If hypothesis is confirmed → proceed to Step 5.
If ruled out → move to next ranked candidate and repeat Step 4.

### Step 5 — Apply Minimal Fix + Document
- Apply the smallest change that resolves the confirmed root cause
- Do NOT change multiple things simultaneously
- After fix: verify the symptom is gone (re-run the Step 4 check)
- Document in the daily note: `memory/YYYY-MM-DD.md` under `## Fixes`

---

## Common Diagnosis Patterns

| Symptom | Likely Causes | Investigation | Fix |
|---------|---------------|---------------|-----|
| `"provider in cooldown"` | LCM usageStats stuck, rate limit hit | `cat ~/.openclaw/agents/main/agent/auth-profiles.json \| python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('usageStats','empty'))"` | Clear usageStats: `python3 -c "import json,os; path=os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json'); d=json.load(open(path)); d['usageStats']={}; json.dump(d,open(path,'w'),indent=2)"` then restart gateway |
| `"gateway unreachable"` | Convex down, port conflict, LaunchAgent crashed | `curl -s http://localhost:3210/health` + `launchctl list \| grep openclaw` | `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex && launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next` |
| `"Telegram not delivering"` | getUpdates lock, bad bot token, message too long | `source ~/.config/env/global.env && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"` | Flush getUpdates: `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1"` |
| `"cron not firing"` | Job disabled, scheduler drift, cron recreated with wrong timing | `openclaw cron list` — check `enabled` flag and `nextRunAt` | Re-enable or recreate job via cron tool; check for post-restart drift (skip if >2h early) |
| `"build fails"` | Missing deps, TypeScript error, missing env var | `npm run build 2>&1 \| tail -40` — read the first error, not the last | Fix first error only; rerun build; repeat until clean |
| `"401 from OpenRouter"` | Bad/revoked API key, wrong model ID, wrong profile | `source ~/.config/env/global.env && echo $OPENROUTER_API_KEY \| cut -c1-15` + check model ID in payload | Update key in `~/.config/env/global.env` (Edit only — never overwrite); verify model ID at openrouter.ai/models |
| `"n8n workflow not triggering"` | Workflow inactive, webhook URL wrong, callback secret mismatch | n8n UI → check workflow active toggle; test webhook: `curl -X POST [webhook-url] -d '{}'` | Activate workflow in n8n UI; update webhook URL in caller; fix secret in env |
| `"Mission Control unreachable"` | Convex crashed, port 3210 conflict, Next.js not started | `curl -s http://localhost:3210/health` + `curl -s http://localhost:3000` | `launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex` then kickstart Next |
| `"cost alert flood"` | Duplicate cron firings, dedup not set, scheduler drift | `openclaw cron runs --id [jobId] --limit 10` — look for multiple runs in same window | Add dedup guard to cron payload; check for LaunchAgent + cron duplicate scheduling |
| `"sub-agent exited without output"` | Timeout hit, cost cap reached, hard crash in tool call | `openclaw sessions list` — check exit reason; look for timeout/cap in session logs | Respawn with `--timeout` increase; raise cost cap; check for tool call causing crash |
| `"LCM compaction failing"` | summaryModel rate-limited, DB too large, wrong model set | Check `~/.openclaw/openclaw.json` summaryModel; check `~/.openclaw/lcm.db` size | Set summaryModel to `openrouter/google/gemini-3.1-flash-lite-preview`; if DB >100MB: backup + delete |
| `"OpenRouter API key revoked"` | Key embedded in workspace file, scanned by security bot | Search workspace for key pattern: `grep -r "sk-or-v1" ~/.openclaw/workspace/` | Rotate key at openrouter.ai; scrub from all files; store only in `~/.config/env/global.env` |
| `"Replit deploy not showing changes"` | Redeploy reused old build, no fresh build triggered | Check if `npm run build` was run before redeploy | In Replit Shell: `npm run build` → then redeploy; OR Deployments → Redeploy → "Rebuild from scratch" |
| `"Glow Index engine 401"` | OpenRouter key in LaunchAgent plist is stale | `cat ~/Library/LaunchAgents/com.openclaw.glow-index-engine.plist \| grep OPENROUTER` | Edit plist key; `launchctl unload` + `launchctl load` to pick up change; engine at 127.0.0.1:8001 |

---

## JT's Debugging Rules

1. **One variable at a time.** Never change two things simultaneously when debugging — you won't know what fixed it.
2. **Form a hypothesis first.** Don't just run random commands. Name what you think is wrong, then test it.
3. **Run `openclaw doctor` first** when something is broken and root cause isn't obvious. Let diagnostics speak before forming theories.
4. **Check TOOLS.md before saying "I can't."** The tool or command probably exists.
5. **Minimal fix only.** Don't refactor while debugging. Apply the smallest change that resolves the root cause.
6. **Verify the fix worked.** Re-run the check from Step 4. Don't assume it's fixed.
7. **Document immediately.** Log the fix in the daily note before moving on.

---

## Output Format

When JT asks "debug X" or "why is X broken", respond with exactly this structure — no preamble:

```
**Most likely cause:** [1 sentence — specific, not vague]

**Verify:** `[exact command to run]`

**Fix:** [minimal fix — command or action]

**Prevent:** [1 sentence rule, only if this is a recurring pattern]
```

If the symptom matches a pattern in the table above, go straight to that row's Investigation and Fix — don't re-derive from scratch.

If the symptom doesn't match any table row, run the 5-step protocol and return output in the format above after Step 4 confirms a root cause.

---

## Quick Reference Commands

```bash
# Gateway health
openclaw doctor

# Clear cooldown
python3 -c "import json,os; path=os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json'); d=json.load(open(path)); d['usageStats']={}; json.dump(d,open(path,'w'),indent=2)"

# Flush Telegram lock
source ~/.config/env/global.env && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1"

# Kickstart Mission Control
launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-convex && launchctl kickstart -k gui/$(id -u)/com.openclaw.mission-control-next

# Check cron jobs
openclaw cron list

# Check recent cron runs
openclaw cron runs --id [jobId] --limit 5

# Check build errors
cd ~/projects/[project] && npm run build 2>&1 | tail -40

# Check env key exists (never print full key)
source ~/.config/env/global.env && echo $OPENROUTER_API_KEY | cut -c1-10

# Restart gateway safely
bash ~/.openclaw/workspace/scripts/restart-gateway.sh "reason"
```
