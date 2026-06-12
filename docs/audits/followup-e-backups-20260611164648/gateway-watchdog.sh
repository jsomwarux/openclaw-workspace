#!/usr/bin/env bash
# Gateway watchdog — runs every 10 minutes via LaunchAgent.
# Hardened: dependency diagnostics, deduped alerts, restart-loop backoff.
set -u

LOG="$HOME/.openclaw/logs/watchdog.log"
STATE="$HOME/.openclaw/logs/watchdog-state.json"
DIAG="$HOME/.openclaw/workspace/scripts/gateway-diagnose.py"
PREFLIGHT="$HOME/.openclaw/workspace/scripts/gateway-preflight.sh"
RESTART="$HOME/.openclaw/workspace/scripts/restart-gateway.sh"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
LABEL="ai.openclaw.gateway"
GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://127.0.0.1:18789/}"
DRY_RUN="${WATCHDOG_DRY_RUN:-0}"
mkdir -p "$(dirname "$LOG")"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "$(timestamp) [watchdog] $*" >> "$LOG"; }

send_telegram() {
    local msg="$1"
    if [ -f "$HOME/.config/env/global.env" ]; then
        # shellcheck disable=SC1090
        source "$HOME/.config/env/global.env"
    fi
    [ -n "${TELEGRAM_BOT_TOKEN:-}" ] || { log "Telegram token missing; cannot alert"; return 0; }
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=6608544825" \
        --data-urlencode "text=${msg}" \
        > /dev/null 2>&1 || true
}

state_get() {
    local key="$1"
    python3 - "$STATE" "$key" <<'PY'
import json,sys,os
p,k=sys.argv[1:3]
try: d=json.load(open(p))
except Exception: d={}
print(d.get(k,''))
PY
}

state_set_json() {
    local json_payload="$1"
    python3 - "$STATE" "$json_payload" <<'PY'
import json,sys,os,tempfile
p=sys.argv[1]
upd=json.loads(sys.argv[2])
try: d=json.load(open(p))
except Exception: d={}
d.update(upd)
os.makedirs(os.path.dirname(p), exist_ok=True)
fd,tmp=tempfile.mkstemp(dir=os.path.dirname(p), prefix='.watchdog-state.', text=True)
with os.fdopen(fd,'w') as f: json.dump(d,f,indent=2,sort_keys=True)
os.replace(tmp,p)
PY
}

alert_deduped() {
    local msg="$1"
    # Never send green/empty diagnostics to JT. Watchdog is quiet unless there is
    # a real outage or a real recovery from an outage.
    if [[ -z "$msg" || "$msg" == *"gateway diagnostic: healthy"* || "$msg" == *"gateway failure: healthy"* ]]; then
        log "suppressed non-actionable gateway diagnostic"
        return 0
    fi
    local sig now last_sig repeat first_ts
    sig=$(printf '%s' "$msg" | shasum -a 256 | awk '{print $1}')
    now=$(date +%s)
    last_sig=$(state_get last_alert_sig)
    repeat=$(state_get repeat_count); repeat=${repeat:-0}
    first_ts=$(state_get first_repeat_ts); first_ts=${first_ts:-$now}

    if [ "$sig" = "$last_sig" ]; then
        repeat=$((repeat + 1))
        state_set_json "{\"repeat_count\":$repeat}"
        if [ "$repeat" -eq 12 ]; then
            local hours=$(( (now - first_ts) / 3600 ))
            send_telegram "⚠️ OpenClaw gateway: same failure repeated ${repeat} times over ~${hours}h. Suppressing duplicate alerts until the root cause changes."
        else
            log "suppressed duplicate alert repeat=$repeat sig=$sig"
        fi
        return 0
    fi

    state_set_json "{\"last_alert_sig\":\"$sig\",\"repeat_count\":1,\"first_repeat_ts\":$now}"
    send_telegram "$msg"
}

record_crash_and_should_backoff() {
    local now crashes_json count oldest backoff_until
    now=$(date +%s)
    python3 - "$STATE" "$now" <<'PY'
import json,sys,os,tempfile
p=sys.argv[1]; now=int(sys.argv[2])
try: d=json.load(open(p))
except Exception: d={}
crashes=[int(x) for x in d.get('crashes',[]) if now-int(x) <= 3600]
crashes.append(now)
d['crashes']=crashes
if len(crashes)>3:
    prev=int(d.get('backoff_seconds',10) or 10)
    backoff=min(max(prev*2,60),1800)
    d['backoff_seconds']=backoff
    d['backoff_until']=now+backoff
else:
    d.setdefault('backoff_seconds',10)
os.makedirs(os.path.dirname(p), exist_ok=True)
fd,tmp=tempfile.mkstemp(dir=os.path.dirname(p), prefix='.watchdog-state.', text=True)
with os.fdopen(fd,'w') as f: json.dump(d,f,indent=2,sort_keys=True)
os.replace(tmp,p)
print(len(crashes), d.get('backoff_until',0), d.get('backoff_seconds',10))
PY
}

is_backing_off() {
    local now until
    now=$(date +%s)
    until=$(state_get backoff_until); until=${until:-0}
    if [ "$until" -gt "$now" ]; then
        log "restart-loop protection active; backing off for $((until-now))s"
        return 0
    fi
    return 1
}

is_gateway_running() {
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$GATEWAY_URL" 2>/dev/null || true)
    [ "$http_code" = "200" ]
}

gateway_process_hint() {
    pgrep -f "/opt/homebrew/lib/node_modules/openclaw/dist/index.js gateway" >/dev/null 2>&1 && echo "process_match=yes" || echo "process_match=no"
}

latest_three_cron_runs_are_openai_codex_cooldown() {
    python3 - "$HOME/.openclaw/cron/runs" <<'PY'
import json, sys
from pathlib import Path

needle = "No available auth profile for openai-codex"
runs_dir = Path(sys.argv[1]).expanduser()
records = []
if runs_dir.exists():
    for path in runs_dir.glob("*.jsonl"):
        try:
            fallback_ts = path.stat().st_mtime * 1000
        except OSError:
            fallback_ts = 0
        try:
            lines = path.read_text(errors="replace").splitlines()
        except Exception:
            continue
        for idx, line in enumerate(lines):
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("action") != "finished":
                continue
            ts = obj.get("ts") or obj.get("finishedAt") or obj.get("runAtMs") or fallback_ts + idx
            text = json.dumps(obj, sort_keys=True)
            records.append((int(ts), obj.get("status"), needle in text))

records.sort(reverse=True)
latest = records[:3]
if len(latest) == 3 and all(status == "error" and has_needle for _, status, has_needle in latest):
    print("yes")
else:
    print("no")
PY
}

clear_auth_cooldown_if_needed() {
    is_gateway_running || return 0
    [ "$(latest_three_cron_runs_are_openai_codex_cooldown)" = "yes" ] || return 0

    local now last
    now=$(date +%s)
    last=$(state_get last_auth_cooldown_clear_ts); last=${last:-0}
    if [ "$((now - last))" -lt 21600 ]; then
        log "auth cooldown clear skipped; last trigger was $((now - last))s ago"
        return 0
    fi

    log "auth cooldown trigger matched: latest 3 finished cron runs failed with openai-codex auth cooldown"
    if [ "$DRY_RUN" = "1" ]; then
        log "DRY_RUN: would clear auth usageStats and restart gateway"
        return 0
    fi

    if python3 - "$HOME/.openclaw/agents/main/agent/auth-profiles.json" <<'PY'
import json, os, shutil, sys, tempfile, time
path = os.path.expanduser(sys.argv[1])
with open(path) as f:
    data = json.load(f)
backup = f"{path}.watchdog-backup-{time.strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(path, backup)
data["usageStats"] = {}
directory = os.path.dirname(path)
fd, tmp = tempfile.mkstemp(dir=directory, prefix=".auth-profiles.", text=True)
with os.fdopen(fd, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
os.replace(tmp, path)
PY
    then
        state_set_json "{\"last_auth_cooldown_clear_ts\":$now}"
        log "auth usageStats cleared; restarting gateway via restart-gateway.sh"
        bash "$RESTART" "watchdog cleared openai-codex auth cooldown" >> "$LOG" 2>&1 || log "auth cooldown restart command failed"
    else
        log "auth cooldown clear failed"
    fi
}

# 1. Check for runaway context-mode plugin (>1.5GB RSS)
CONTEXT_PID=$(pgrep -f "context-mode.*start.mjs" 2>/dev/null | head -1)
if [ -n "$CONTEXT_PID" ]; then
    RSS_KB=$(ps -o rss= -p "$CONTEXT_PID" 2>/dev/null | tr -d ' ')
    RSS_MB=$((RSS_KB / 1024))
    if [ "$RSS_MB" -gt 1500 ]; then
        kill -9 "$CONTEXT_PID" 2>/dev/null
        log "KILLED context-mode PID $CONTEXT_PID — RSS was ${RSS_MB}MB (runaway)"
    fi
fi

# 2. Check Mission Control (Next.js)
MC_HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000/api/tasks 2>/dev/null)
if [ "$MC_HTTP" != "200" ]; then
    log "Mission Control API returned $MC_HTTP — kicking next LaunchAgent"
    launchctl kickstart -k "gui/$(id -u)/com.openclaw.mission-control-next" >> "$LOG" 2>&1
fi

# 3. Gateway dependency preflight first; do not launchd-thrash on missing dylibs.
if [ -x "$PREFLIGHT" ]; then
    if ! "$PREFLIGHT" check >> "$LOG" 2>&1; then
        diag_msg=$(python3 "$DIAG" alert 2>/dev/null || echo "🚨 OpenClaw gateway dependency preflight failed. Run: $PREFLIGHT check")
        alert_deduped "$diag_msg"
        log "preflight failed; not attempting restart"
        exit 0
    fi
fi

# 4. If the gateway is healthy but cron auth is wedged, clear auth cooldown once per 6h.
clear_auth_cooldown_if_needed

# 5. Check if gateway is running
if ! is_gateway_running; then
    log "gateway HTTP probe failed at $GATEWAY_URL ($(gateway_process_hint)) — attempting recovery"
    crash_info=$(record_crash_and_should_backoff)
    log "crash-window info: $crash_info"
    if is_backing_off; then
        diag_msg=$(python3 "$DIAG" alert 2>/dev/null || echo "🚨 OpenClaw gateway is in restart-loop backoff. Run openclaw doctor.")
        alert_deduped "$diag_msg"
        exit 0
    fi

    if [ "$DRY_RUN" = "1" ]; then
        log "DRY_RUN: would restart gateway via restart-gateway.sh"
        exit 0
    fi

    bash "$RESTART" "watchdog recovery" >> "$LOG" 2>&1 || log "restart-gateway.sh failed during watchdog recovery"
    sleep 6

    if is_gateway_running; then
        log "gateway recovered via restart-gateway.sh"
        state_set_json '{"crashes":[],"backoff_until":0,"backoff_seconds":10}'
        alert_deduped "✅ Gateway recovered after watchdog restart. You may have missed messages. $(date '+%Y-%m-%d %H:%M')"
    else
        log "CRITICAL: gateway still dead after restart-gateway.sh"
        diag_msg=$(python3 "$DIAG" alert 2>/dev/null || echo "🚨 Gateway is DOWN and diagnostics failed. Manual fix: run bash ~/.openclaw/workspace/scripts/restart-gateway.sh recovery")
        alert_deduped "$diag_msg"
    fi
fi
