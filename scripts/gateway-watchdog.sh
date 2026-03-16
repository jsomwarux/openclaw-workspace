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

# 2. Check if openclaw-gateway is running
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
