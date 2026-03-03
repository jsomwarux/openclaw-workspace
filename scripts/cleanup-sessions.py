#!/usr/bin/env python3
"""
Eve's OpenClaw Session Cleanup Script
Runs daily at 3:00 AM EST via launchd.

Removes stale cron-generated sessions from sessions.json.
Safe rules:
  - Always preserve the main session (key: agent:main:main)
  - Always preserve sessions updated within the last 24 hours
  - Remove all other sessions (cron orphans accumulate via isolated sessionTarget)
  - Writes atomically (temp file → rename) to avoid corruption
  - Logs results to today's daily note
"""

import json
import os
import sys
import time
import tempfile
import shutil
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
HOME = os.path.expanduser("~")
SESSIONS_FILE = f"{HOME}/.openclaw/agents/main/sessions/sessions.json"
MEMORY_DIR    = f"{HOME}/.openclaw/workspace/memory"
MAX_AGE_HOURS = 24   # remove sessions not updated within this window
ALWAYS_KEEP   = {"agent:main:main"}  # never remove these keys

# ── Helpers ───────────────────────────────────────────────────────────────────
def now_ms() -> int:
    return int(time.time() * 1000)

def log_to_daily_note(lines: list[str]):
    """Append cleanup summary to today's daily note."""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    note_path = f"{MEMORY_DIR}/{date_str}.md"
    timestamp = datetime.now().strftime("%H:%M")

    header = f"\n## Session Cleanup {timestamp}\n"
    body = "\n".join(f"- {l}" for l in lines) + "\n"

    with open(note_path, "a") as f:
        f.write(header + body)

def write_atomic(path: str, data: dict):
    """Write JSON atomically via temp file to avoid corruption."""
    dir_ = os.path.dirname(path)
    fd, tmp_path = tempfile.mkstemp(dir=dir_, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(tmp_path, 0o600)
        shutil.move(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(SESSIONS_FILE):
        print(f"[cleanup] sessions.json not found at {SESSIONS_FILE}")
        sys.exit(0)

    with open(SESSIONS_FILE) as f:
        sessions: dict = json.load(f)

    cutoff_ms = now_ms() - (MAX_AGE_HOURS * 3600 * 1000)
    total_before = len(sessions)
    removed = []
    kept = []

    for key, val in list(sessions.items()):
        updated_at = val.get("updatedAt", 0)

        # Rule 1: always keep protected keys
        if key in ALWAYS_KEEP:
            kept.append((key, "protected"))
            continue

        # Rule 2: keep recently-active sessions
        if updated_at >= cutoff_ms:
            kept.append((key, f"active ({_age_str(updated_at)})"))
            continue

        # Rule 3: stale — remove
        removed.append((key, updated_at))
        del sessions[key]

    total_after = len(sessions)
    removed_count = total_before - total_after

    # Write back only if something changed
    if removed_count > 0:
        write_atomic(SESSIONS_FILE, sessions)

    # ── Logging ───────────────────────────────────────────────────────────────
    size_kb = os.path.getsize(SESSIONS_FILE) / 1024

    log_lines = [
        f"Sessions before: {total_before}, after: {total_after}, removed: {removed_count}",
        f"sessions.json size: {size_kb:.1f} KB",
    ]

    if removed:
        log_lines.append("Removed sessions:")
        for key, ts in removed:
            log_lines.append(f"  {key} (last active: {_age_str(ts)})")
    else:
        log_lines.append("Nothing to clean up — all sessions recent or protected.")

    # Print to stdout (captured by launchd log)
    print(f"[cleanup-sessions] {datetime.now().isoformat()}")
    for line in log_lines:
        print(f"  {line}")

    # Append to daily note
    log_to_daily_note(log_lines)

def _age_str(updated_ms: int) -> str:
    if not updated_ms:
        return "unknown age"
    age_s = (now_ms() - updated_ms) / 1000
    if age_s < 3600:
        return f"{int(age_s / 60)}m ago"
    elif age_s < 86400:
        return f"{age_s / 3600:.1f}h ago"
    else:
        return f"{age_s / 86400:.1f}d ago"

if __name__ == "__main__":
    main()
