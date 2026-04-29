#!/usr/bin/env bash
# Gateway watchdog — runs every 10 minutes via LaunchAgent.
# Hardened: dependency diagnostics, deduped alerts, restart-loop backoff.
set -u

LOG="$HOME/.openclaw/logs/watchdog.log"
STATE="$HOME/.openclaw/logs/watchdog-state.json"
DIAG="$HOME/.openclaw/workspace/scripts/gateway-diagnose.py"
PREFLIGHT="$HOME/.openclaw/workspace/scripts/gateway-preflight.sh"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
LABEL="ai.openclaw.gateway"
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
crashes=[int(x) for x in d.get('crashes',[]) if now-int(x) <= 60]
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
    # launchd runs Node directly; older pgrep openclaw-gateway check missed this.
    pgrep -f "/opt/homebrew/lib/node_modules/openclaw/dist/index.js gateway" >/dev/null 2>&1
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

# 4. Check if gateway is running
if ! is_gateway_running; then
    log "gateway not running — attempting recovery"
    crash_info=$(record_crash_and_should_backoff)
    log "crash-window info: $crash_info"
    if is_backing_off; then
        diag_msg=$(python3 "$DIAG" alert 2>/dev/null || echo "🚨 OpenClaw gateway is in restart-loop backoff. Run openclaw doctor.")
        alert_deduped "$diag_msg"
        exit 0
    fi

    launchctl kickstart -k "gui/$(id -u)/$LABEL" >> "$LOG" 2>&1
    sleep 6

    if is_gateway_running; then
        log "gateway recovered via kickstart"
        state_set_json '{"crashes":[],"backoff_until":0,"backoff_seconds":10}'
    else
        log "kickstart failed — trying unload+load once"
        launchctl unload "$PLIST" >> "$LOG" 2>&1 || true
        sleep 3
        launchctl load "$PLIST" >> "$LOG" 2>&1
        sleep 10

        if is_gateway_running; then
            log "gateway recovered via unload+load"
            state_set_json '{"crashes":[],"backoff_until":0,"backoff_seconds":10}'
            alert_deduped "✅ Gateway recovered after watchdog restart. You may have missed messages. $(date '+%Y-%m-%d %H:%M')"
        else
            log "CRITICAL: gateway still dead after unload+load"
            diag_msg=$(python3 "$DIAG" alert 2>/dev/null || echo "🚨 Gateway is DOWN and diagnostics failed. Manual fix: launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist")
            alert_deduped "$diag_msg"
        fi
    fi
fi
