#!/bin/bash
# Gateway watchdog — runs every 10 minutes via LaunchAgent
# If openclaw-gateway is dead, kicks it. If context-mode plugin is runaway (>5min CPU), kills it.

LOG="$HOME/.openclaw/logs/watchdog.log"
mkdir -p "$(dirname "$LOG")"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

# 1. Check for runaway context-mode plugin (>2GB RSS or >300s CPU time accumulated in one run)
CONTEXT_PID=$(pgrep -f "context-mode.*start.mjs" 2>/dev/null | head -1)
if [ -n "$CONTEXT_PID" ]; then
    RSS_KB=$(ps -o rss= -p "$CONTEXT_PID" 2>/dev/null | tr -d ' ')
    CPU_TIME=$(ps -o time= -p "$CONTEXT_PID" 2>/dev/null | tr -d ' ')
    RSS_MB=$((RSS_KB / 1024))
    if [ "$RSS_MB" -gt 1500 ]; then
        kill -9 "$CONTEXT_PID" 2>/dev/null
        echo "$(timestamp) [watchdog] KILLED context-mode PID $CONTEXT_PID — RSS was ${RSS_MB}MB (runaway)" >> "$LOG"
    fi
fi

# 2. Check if Mission Control (Next.js) is responding
MC_HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000/api/tasks 2>/dev/null)
if [ "$MC_HTTP" != "200" ]; then
    echo "$(timestamp) [watchdog] Mission Control API returned $MC_HTTP — kicking next LaunchAgent" >> "$LOG"
    launchctl kickstart -k "gui/$(id -u)/com.openclaw.mission-control-next" >> "$LOG" 2>&1
    sleep 8
    MC_HTTP2=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000/api/tasks 2>/dev/null)
    if [ "$MC_HTTP2" = "200" ]; then
        echo "$(timestamp) [watchdog] Mission Control recovered (HTTP $MC_HTTP2)" >> "$LOG"
    else
        echo "$(timestamp) [watchdog] Mission Control still unhealthy after kickstart (HTTP $MC_HTTP2)" >> "$LOG"
    fi
fi

# 3. Check if openclaw-gateway is running
if ! pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    echo "$(timestamp) [watchdog] gateway not running — kicking LaunchAgent" >> "$LOG"
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway" >> "$LOG" 2>&1
    sleep 5
    if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
        echo "$(timestamp) [watchdog] gateway recovered successfully" >> "$LOG"
    else
        echo "$(timestamp) [watchdog] gateway still dead after kickstart" >> "$LOG"
    fi
fi
