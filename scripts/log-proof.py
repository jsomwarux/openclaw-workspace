#!/usr/bin/env python3
"""
Eve's Audit Trail Logger — log-proof.py

Usage (from shell or other scripts):
  python3 log-proof.py \
    --type file_creation \
    --title "Created backup script" \
    --description "..." \
    --outcome success \
    --files "~/.openclaw/workspace/scripts/backup.sh" \
    [--error "error message"] \
    [--cost-tokens 1200] \
    [--cost-usd 0.004] \
    [--meta '{"key": "value"}']

Or import and call log_proof() directly from Python.

Proof entries are stored as JSONL in:
  ~/.openclaw/workspace/proofs/YYYY-MM-DD/actions.jsonl
"""

import json
import os
import sys
import uuid
import argparse
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
PROOFS_DIR = os.path.join(WORKSPACE, "proofs")

VALID_TYPES = [
    "file_creation",
    "file_edit",
    "file_deletion",
    "cron_setup",
    "cron_removal",
    "script_execution",
    "research",
    "deployment",
    "config_change",
    "backup",
    "cleanup",
    "security",
    "kb_add",
    "kb_index",
    "automation_setup",
    "api_call",
    "other",
]

def log_proof(
    action_type: str,
    title: str,
    description: str,
    outcome: str = "success",
    files_affected: Optional[List[str]] = None,
    error: Optional[str] = None,
    cost_tokens: Optional[int] = None,
    cost_usd: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Write a proof entry to today's JSONL file.
    Returns the entry dict.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    ts = timestamp or now.isoformat()

    # Normalize file paths
    files = []
    for f in (files_affected or []):
        files.append(os.path.expanduser(str(f)))

    cost = None
    if cost_tokens is not None or cost_usd is not None:
        cost = {}
        if cost_tokens is not None:
            cost["tokens"] = cost_tokens
        if cost_usd is not None:
            cost["usd"] = round(cost_usd, 6)

    entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": ts,
        "action_type": action_type,
        "title": title,
        "description": description,
        "outcome": outcome,
        "error": error,
        "cost": cost,
        "files_affected": files,
        "metadata": metadata or {},
    }

    # Write to proofs/YYYY-MM-DD/actions.jsonl
    day_dir = os.path.join(PROOFS_DIR, date_str)
    os.makedirs(day_dir, exist_ok=True)
    proof_file = os.path.join(day_dir, "actions.jsonl")

    with open(proof_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


def read_proofs(date_str: Optional[str] = None) -> List[Dict[str, Any]]:
    """Read all proof entries for a given date (default: today)."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    proof_file = os.path.join(PROOFS_DIR, date_str, "actions.jsonl")
    if not os.path.exists(proof_file):
        return []
    entries = []
    with open(proof_file) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def main():
    parser = argparse.ArgumentParser(description="Log a proof entry to the audit trail.")
    parser.add_argument("--type", choices=VALID_TYPES, dest="action_type",
                        help="Action type")
    parser.add_argument("--title", help="Short title")
    parser.add_argument("--description", help="What was done")
    parser.add_argument("--outcome", default="success", choices=["success", "failure", "partial"],
                        help="Outcome (default: success)")
    parser.add_argument("--error", default=None, help="Error message if outcome is failure")
    parser.add_argument("--files", nargs="*", default=[], help="Files affected (space-separated)")
    parser.add_argument("--cost-tokens", type=int, default=None, help="Token cost")
    parser.add_argument("--cost-usd", type=float, default=None, help="USD cost")
    parser.add_argument("--meta", default=None, help="Extra metadata as JSON string")
    parser.add_argument("--timestamp", default=None, help="Override timestamp (ISO 8601)")
    parser.add_argument("--list", action="store_true", help="List today's proof entries")
    parser.add_argument("--date", default=None, help="Date for --list (YYYY-MM-DD)")

    args = parser.parse_args()

    if not args.list and not all([args.action_type, args.title, args.description]):
        parser.error("--type, --title, and --description are required unless using --list")

    if args.list:
        entries = read_proofs(args.date)
        if not entries:
            print(f"No entries for {args.date or 'today'}.")
        for e in entries:
            ts = e["timestamp"][:19].replace("T", " ")
            status = "✓" if e["outcome"] == "success" else "✗"
            print(f"[{ts}] {status} [{e['action_type']}] {e['title']}")
            if e.get("description"):
                print(f"    {e['description'][:80]}")
            if e.get("files_affected"):
                for f in e["files_affected"]:
                    print(f"    → {f}")
            print()
        return

    meta = None
    if args.meta:
        meta = json.loads(args.meta)

    entry = log_proof(
        action_type=args.action_type,
        title=args.title,
        description=args.description,
        outcome=args.outcome,
        files_affected=args.files,
        error=args.error,
        cost_tokens=args.cost_tokens,
        cost_usd=args.cost_usd,
        metadata=meta,
        timestamp=args.timestamp,
    )
    print(f"✓ Proof logged: [{entry['id']}] {entry['title']}")


if __name__ == "__main__":
    main()
