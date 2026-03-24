#!/bin/bash
# mission-control-start.sh
# Starts the Mission Control Next.js dashboard.
# Called by com.openclaw.mission-control-next LaunchAgent.
# Category 2: pure automation — zero LLM calls. Approved 2026-02-26.
#
# WHY dev mode instead of start:
# `next start` bakes NEXT_PUBLIC_* env vars at build time. If Convex restarts
# and changes its deployment ID, the stale build can't connect → 500 errors.
# `next dev` reads .env.local at startup, always fresh. No rebuild needed.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/jtsomwaru"

cd /Users/jtsomwaru/.openclaw/workspace/mission-control

exec /opt/homebrew/bin/node node_modules/.bin/next dev -H 0.0.0.0 -p 3000
