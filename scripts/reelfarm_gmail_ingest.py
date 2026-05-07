#!/usr/bin/env python3
"""Ingest Social Growth Engineers emails into ReelFarm newsletter inbox.

Safe behavior:
- Reads Gmail only through `gog`; never sends or modifies email.
- If gog auth is missing, exits 0 with a status note so daily jobs don't fail.
- Dedupes by Gmail message id in memory/reelfarm/gmail-state.json.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path.home() / ".openclaw" / "workspace"
INBOX = ROOT / "memory" / "reelfarm" / "newsletters" / "inbox"
STATE_PATH = ROOT / "memory" / "reelfarm" / "gmail-state.json"
STATUS_PATH = ROOT / "memory" / "reelfarm" / "gmail-ingest-status.md"
DEFAULT_QUERY = '(from:socialgrowthengineers.com OR from:socialgrowthengineers OR "Social Growth Engineers") newer_than:7d'


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, timeout=60)


def write_status(text: str) -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    STATUS_PATH.write_text(f"# ReelFarm Gmail Ingest Status\n\nLast checked: {ts}\n\n{text}\n")


def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {"processed_ids": []}
    return {"processed_ids": []}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def flatten_messages(payload: Any) -> list[dict[str, Any]]:
    """Handle gog JSON envelopes across versions."""
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("messages", "results", "items", "data"):
        val = payload.get(key)
        if isinstance(val, list):
            return [x for x in val if isinstance(x, dict)]
        if isinstance(val, dict):
            nested = flatten_messages(val)
            if nested:
                return nested
    # Sometimes --results-only returns a single message object.
    if any(k in payload for k in ("id", "subject", "body", "snippet")):
        return [payload]
    return []


def pick(d: dict[str, Any], *keys: str) -> str:
    for key in keys:
        val = d
        ok = True
        for part in key.split('.'):
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                ok = False
                break
        if ok and val is not None:
            return str(val)
    return ""


def body_from_message(msg: dict[str, Any]) -> str:
    candidates = [
        pick(msg, "body", "text", "plain", "bodyText", "payload.body", "message.body"),
        pick(msg, "snippet"),
    ]
    # Also scan shallow string fields for the longest body-like value.
    for v in msg.values():
        if isinstance(v, str) and len(v) > 500:
            candidates.append(v)
    body = max(candidates, key=len, default="").strip()
    return body


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:80] or "social-growth-engineers"


def load_env_password() -> None:
    """Load GOG_KEYRING_PASSWORD from global.env for cron/non-interactive runs."""
    if os.environ.get("GOG_KEYRING_PASSWORD"):
        return
    env_path = Path.home() / ".config" / "env" / "global.env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        if line.startswith("GOG_KEYRING_PASSWORD="):
            os.environ["GOG_KEYRING_PASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
            return


def main() -> int:
    load_env_password()
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", default=os.environ.get("GOG_ACCOUNT", ""), help="Gmail account registered with gog")
    ap.add_argument("--query", default=DEFAULT_QUERY)
    ap.add_argument("--max", default="10")
    args = ap.parse_args()

    INBOX.mkdir(parents=True, exist_ok=True)

    auth = run(["gog", "auth", "list"])
    if auth.returncode != 0 or "No tokens stored" in (auth.stdout + auth.stderr):
        write_status("Gmail ingestion not active: `gog auth list` reports no stored tokens. Run OAuth setup, then this script will ingest automatically.")
        print("GMAIL_INGEST_AUTH_MISSING")
        return 0

    cmd = ["gog", "gmail", "messages", "search", args.query, "--max", args.max, "--json", "--full", "--no-input", "--gmail-no-send"]
    if args.account:
        cmd.extend(["--account", args.account])
    res = run(cmd)
    if res.returncode != 0:
        write_status(f"Gmail search failed. Command exited {res.returncode}.\n\nSTDERR:\n```\n{res.stderr[-2000:]}\n```")
        print("GMAIL_INGEST_SEARCH_FAILED")
        return 0

    try:
        payload = json.loads(res.stdout)
    except Exception as e:
        write_status(f"Gmail search returned non-JSON output: {e}\n\nOutput preview:\n```\n{res.stdout[:2000]}\n```")
        print("GMAIL_INGEST_BAD_JSON")
        return 0

    messages = flatten_messages(payload)
    state = load_state()
    processed = set(state.get("processed_ids", []))
    new_count = 0
    skipped = 0

    today = dt.datetime.now().astimezone().strftime("%Y-%m-%d")
    for msg in messages:
        mid = pick(msg, "id", "messageId", "gmailId") or str(hash(json.dumps(msg, sort_keys=True)[:500]))
        if mid in processed:
            skipped += 1
            continue
        subject = pick(msg, "subject", "headers.subject") or "Social Growth Engineers"
        body = body_from_message(msg)
        if len(body) < 500:
            skipped += 1
            processed.add(mid)
            continue
        filename = f"{today}-{slug(subject)}-{mid[:8]}.md"
        out = INBOX / filename
        i = 2
        while out.exists():
            out = INBOX / f"{today}-{slug(subject)}-{mid[:8]}-{i}.md"
            i += 1
        out.write_text(f"# {subject}\n\n<!-- gmail_message_id: {mid} -->\n\n{body}\n")
        processed.add(mid)
        new_count += 1

    state["processed_ids"] = sorted(processed)[-500:]
    state["last_run"] = dt.datetime.now().astimezone().isoformat()
    save_state(state)
    write_status(f"Gmail ingestion active. New files: {new_count}. Skipped/deduped: {skipped}. Query: `{args.query}`")
    print(f"GMAIL_INGEST_OK new={new_count} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
