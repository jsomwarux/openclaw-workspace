#!/usr/bin/env bash
set -u

NODE_BIN="${OPENCLAW_NODE_BIN:-/opt/homebrew/opt/node@22/bin/node}"
OPENCLAW_INDEX="${OPENCLAW_INDEX:-/opt/homebrew/lib/node_modules/openclaw/dist/index.js}"
PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
LOG_DIR="$HOME/.openclaw/logs"
PREFLIGHT_LOG="$LOG_DIR/gateway-preflight.log"
ERR_LOG="$LOG_DIR/gateway.err.log"
OUT_LOG="$LOG_DIR/gateway.log"
CONFIG_PATH="$HOME/.openclaw/openclaw.json"
MODE="${1:-run}"

mkdir -p "$LOG_DIR"

ts() { date '+%Y-%m-%d %H:%M:%S %Z'; }
redact() {
  sed -E 's/(sk-[A-Za-z0-9_-]{8})[A-Za-z0-9_-]+/\1[REDACTED]/g; s/(Bearer )[A-Za-z0-9._-]+/\1[REDACTED]/g; s/([A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*=)[^[:space:]]+/\1[REDACTED]/g'
}
log() { printf '%s [preflight] %s\n' "$(ts)" "$*" | redact >> "$PREFLIGHT_LOG"; }
fail() {
  local category="$1"; shift
  local msg="$*"
  log "FAIL category=$category :: $msg"
  printf 'OPENCLAW_PREFLIGHT_FAIL category=%s :: %s\n' "$category" "$msg" | redact >&2
  exit 78
}

check_node() {
  [ -x "$NODE_BIN" ] || fail "dependency/runtime" "Node binary missing or not executable: $NODE_BIN. Recommended fix: brew update && brew reinstall node@22"
}

check_otool() {
  command -v otool >/dev/null 2>&1 || fail "dependency/runtime" "otool not found; cannot verify Homebrew dylib integrity. Install Xcode Command Line Tools."
  local out missing line path
  out="$(otool -L "$NODE_BIN" 2>&1)" || fail "dependency/runtime" "otool failed for $NODE_BIN: $out"
  missing=0
  while IFS= read -r line; do
    path="$(printf '%s' "$line" | awk '{print $1}')"
    # Skip otool's header line: /path/to/binary:
    case "$path" in
      *:) continue ;;
    esac
    case "$path" in
      /opt/homebrew/*|/usr/local/*)
        if [ ! -e "$path" ]; then
          log "missing dylib: $path"
          printf '%s\n' "$path"
          missing=1
        fi
        ;;
    esac
  done <<EOF
$out
EOF
  if [ "$missing" -ne 0 ]; then
    fail "dependency/runtime" "Node has missing linked dylibs listed above. Recommended fix: brew update && brew reinstall simdjson && brew reinstall node@22"
  fi
}

check_simdjson() {
  local dir="/opt/homebrew/opt/simdjson/lib"
  if [ ! -d "$dir" ]; then
    fail "dependency/runtime" "simdjson lib directory missing: $dir. Recommended fix: brew update && brew reinstall simdjson node@22"
  fi
  if ! ls "$dir"/libsimdjson.*.dylib >/dev/null 2>&1; then
    fail "dependency/runtime" "No versioned libsimdjson dylib found in $dir. Recommended fix: brew update && brew reinstall simdjson node@22"
  fi
}

check_port() {
  if command -v lsof >/dev/null 2>&1; then
    local holders
    holders="$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | tail -n +2 || true)"
    if [ -n "$holders" ]; then
      # If gateway already owns it, this is healthy for doctor mode but fatal for starting a second copy.
      if printf '%s\n' "$holders" | grep -qi 'node\|openclaw'; then
        [ "$MODE" = "check" ] && return 0
      fi
      fail "port-conflict" "Port $PORT is already listening: $(printf '%s' "$holders" | head -1). Recommended fix: identify process with lsof -nP -iTCP:$PORT -sTCP:LISTEN"
    fi
  fi
}

startup_banner() {
  local node_version oc_version model_route plugins
  node_version="$($NODE_BIN --version 2>/dev/null || echo unknown)"
  oc_version="$(node -e "try{console.log(require('/opt/homebrew/lib/node_modules/openclaw/package.json').version)}catch(e){console.log('unknown')}" 2>/dev/null || echo unknown)"
  model_route="$(python3 - <<'PY' 2>/dev/null || true
import json, os
p=os.path.expanduser('~/.openclaw/openclaw.json')
try:
 d=json.load(open(p))
 print(d.get('agents',{}).get('defaults',{}).get('model') or d.get('model') or 'unknown')
except Exception:
 print('unknown')
PY
)"
  plugins="$(python3 - <<'PY' 2>/dev/null || true
import json, os
p=os.path.expanduser('~/.openclaw/openclaw.json')
try:
 d=json.load(open(p))
 xs=d.get('plugins') or d.get('channels') or []
 if isinstance(xs, dict): xs=list(xs.keys())
 print(','.join(map(str,xs))[:300] or 'unknown')
except Exception:
 print('unknown')
PY
)"
  {
    echo "===== OpenClaw Gateway Startup $(ts) ====="
    echo "OpenClaw version: $oc_version"
    echo "node path: $NODE_BIN"
    echo "node version: $node_version"
    echo "gateway port: $PORT"
    echo "plugin list: $plugins"
    echo "model route: $model_route"
    echo "config path: $CONFIG_PATH"
  } | redact >> "$OUT_LOG"
}

run_checks() {
  check_node
  check_otool >/dev/null
  check_simdjson
  check_port
  log "OK node=$NODE_BIN port=$PORT"
}

if [ "$MODE" = "check" ]; then
  run_checks
  echo "OpenClaw gateway preflight OK"
  exit 0
fi

run_checks
startup_banner
exec "$NODE_BIN" "$OPENCLAW_INDEX" gateway --port "$PORT"
