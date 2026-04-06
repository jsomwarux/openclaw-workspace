#!/bin/bash
# Gateway watchdog — runs every 10 minutes via LaunchAgent
# If openclaw-gateway is dead, kicks it. If context-mode plugin is runaway (>5min CPU), kills it.

LOG="$HOME/.openclaw/logs/watchdog.log"
mkdir -p "$(dirname "$LOG")"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

send_telegram() {
    local msg="$1"
    if [ -f "$HOME/.config/env/global.env" ]; then
        source "$HOME/.config/env/global.env"
    fi
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=6608544825" \
        -d "text=${msg}" \
        > /dev/null 2>&1 || true
}

# 1. Check for runaway context-mode plugin (>1.5GB RSS)
CONTEXT_PID=$(pgrep -f "context-mode.*start.mjs" 2>/dev/null | head -1)
if [ -n "$CONTEXT_PID" ]; then
    RSS_KB=$(ps -o rss= -p "$CONTEXT_PID" 2>/dev/null | tr -d ' ')
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
# Note: openclaw-gateway is a compiled binary — pgrep -f misses it. Use ps-based check.
if ! ps aux | grep -q "[o]penclaw-gateway"; then
    echo "$(timestamp) [watchdog] gateway not running — attempting recovery" >> "$LOG"

    # Step 1: Try kickstart (works if launchd still has the job registered)
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway" >> "$LOG" 2>&1
    sleep 6

    if ps aux | grep -q "[o]penclaw-gateway"; then
        echo "$(timestamp) [watchdog] gateway recovered via kickstart" >> "$LOG"
    else
        # Step 2: kickstart failed — job may be deregistered after crash loop.
        # Fall back to unload+load (re-registers the job from scratch — always works).
        echo "$(timestamp) [watchdog] kickstart failed — trying unload+load" >> "$LOG"
        launchctl unload "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" >> "$LOG" 2>&1 || true
        sleep 3
        launchctl load "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" >> "$LOG" 2>&1
        sleep 10

        if ps aux | grep -q "[o]penclaw-gateway"; then
            echo "$(timestamp) [watchdog] gateway recovered via unload+load" >> "$LOG"
            send_telegram "⚠️ Gateway watchdog: kickstart failed, recovered via hard unload+load. You may have missed messages. $(date '+%Y-%m-%d %H:%M')"
        else
            echo "$(timestamp) [watchdog] CRITICAL: gateway still dead after unload+load — manual intervention required" >> "$LOG"
            send_telegram "🚨 Gateway is DOWN and watchdog cannot recover it. Manual fix: launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
        fi
    fi
fi
