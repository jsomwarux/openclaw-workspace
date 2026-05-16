#!/usr/bin/env python3
"""Validate JT's social engagement/reply system artifacts.

This is intentionally read-only. It catches the failure modes that prompts alone miss:
- X reply target files without direct links
- stale latest reply target files
- dynasty reply ledger missing/too thin/malformed
- recent dynasty cron summaries repeating the same target pack
- Reddit draft log malformed or duplicate-ish recent frames
- required engagement crons disabled/missing failure alerts
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(os.environ.get("OPENCLAW_WORKSPACE", "/Users/jtsomwaru/.openclaw/workspace"))
REQUIRED_CRONS = {
    "8b968751-6e59-42e5-b2ce-09f57d36176c": "dynasty-replies-gen",
    "bbe49024-458a-4496-9c7c-7a278615810f": "reddit-daily-gen",
    "fe575759-c8b1-4715-ae5a-0dbe034b3c9b": "reddit-karma-daily-reminder",
    "33b8b0a2-e86c-4f51-aa4f-b8537def3107": "Viral Post Swipe File — X Research",
}
X_URL_RE = re.compile(r"https://x\.com/[A-Za-z0-9_]+/status/\d+")
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


@dataclass
class Check:
    name: str
    status: str
    detail: str


def age_hours(path: Path) -> float:
    return (datetime.now().timestamp() - path.stat().st_mtime) / 3600


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_json_array_or_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load logs that may be either a JSON array or newline-delimited JSON.

    The Reddit draft log is named .jsonl and cron prompts append rows, so JSONL is
    the durable write format. Older hardening runs wrote it as a JSON array; keep
    backward compatibility so the validator enforces row quality instead of
    failing on storage-shape drift.
    """
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        rows: list[dict[str, Any]] = []
        for idx, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception as e:  # noqa: BLE001
                raise ValueError(f"line {idx}: {e}") from e
            if not isinstance(row, dict):
                raise ValueError(f"line {idx}: expected JSON object, got {type(row).__name__}")
            rows.append(row)
        return rows
    if not isinstance(data, list):
        raise ValueError(f"expected JSON array or JSONL objects, got {type(data).__name__}")
    for idx, row in enumerate(data, 1):
        if not isinstance(row, dict):
            raise ValueError(f"row {idx}: expected JSON object, got {type(row).__name__}")
    return data


def run_json(cmd: list[str], timeout: int = 30) -> Any | None:
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None
    # OpenClaw may print config warnings before or after JSON. Decode the first
    # valid JSON object inside the combined output instead of requiring clean stdout.
    txt = (cp.stdout or "") + "\n" + (cp.stderr or "")
    dec = json.JSONDecoder()
    for match in re.finditer(r"{", txt):
        try:
            obj, _ = dec.raw_decode(txt[match.start():])
            return obj
        except Exception:
            continue
    return None


def latest_reply_targets() -> Check:
    files = sorted(ROOT.glob("memory/content/reply-targets-*.md"))
    if not files:
        return Check("x_reply_targets_latest", "fail", "no reply-targets files found")
    latest = files[-1]
    txt = latest.read_text(errors="ignore")
    links = X_URL_RE.findall(txt)
    hours = age_hours(latest)
    status = "pass"
    reasons = []
    if hours > 96:
        status = "fail"
        reasons.append(f"latest file is {hours:.1f}h old")
    elif hours > 48:
        status = "warn"
        reasons.append(f"latest file is {hours:.1f}h old")
    if len(links) < 3:
        status = "fail"
        reasons.append(f"only {len(links)} direct X links")
    if "Link:" not in txt:
        status = "fail"
        reasons.append("missing Link: lines")
    if not reasons:
        reasons.append(f"{latest.name}; {len(links)} direct X links; {hours:.1f}h old")
    return Check("x_reply_targets_latest", status, "; ".join(reasons))


def older_reply_link_hygiene(days_back: int = 45) -> Check:
    files = sorted(ROOT.glob("memory/content/reply-targets-*.md"))[-12:]
    bad = []
    for p in files:
        txt = p.read_text(errors="ignore")
        if "https://x.com/" not in txt:
            bad.append(p.name)
    if bad:
        return Check("x_reply_targets_link_hygiene", "warn", f"recent files missing direct links: {', '.join(bad)}")
    return Check("x_reply_targets_link_hygiene", "pass", f"checked {len(files)} recent files")


def dynasty_ledger() -> Check:
    p = ROOT / "memory/sports-gm/dynasty-replies-ledger.jsonl"
    if not p.exists():
        return Check("dynasty_reply_ledger", "fail", "ledger missing")
    rows = []
    errors = []
    for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            errors.append(f"line {i}: {e}")
    if errors:
        return Check("dynasty_reply_ledger", "fail", "; ".join(errors[:3]))
    urls = [r.get("url") or r.get("status_id") for r in rows]
    dupes = [u for u, n in Counter(urls).items() if u and n > 1]
    recent_dates = sorted({r.get("date") for r in rows if r.get("date")})[-7:]
    if len(rows) < 14:
        return Check("dynasty_reply_ledger", "warn", f"ledger is valid but thin: {len(rows)} rows; dates={recent_dates}; cannot enforce 14-day history yet")
    if dupes:
        return Check("dynasty_reply_ledger", "fail", f"duplicate target URLs/status IDs: {dupes[:5]}")
    return Check("dynasty_reply_ledger", "pass", f"{len(rows)} rows; latest dates={recent_dates}")


def reddit_draft_log() -> Check:
    p = ROOT / "memory/content/reddit-draft-log.jsonl"
    if not p.exists():
        return Check("reddit_draft_log", "fail", "missing reddit-draft-log.jsonl")
    try:
        data = load_json_array_or_jsonl(p)
    except Exception as e:
        return Check("reddit_draft_log", "fail", f"not valid JSON array/JSONL: {e}")
    required = {"date", "subreddit", "type", "title_or_look_for", "first_120_chars", "core_angle", "body_hash"}
    missing = []
    for idx, row in enumerate(data, 1):
        miss = required - set(row)
        if miss:
            missing.append(f"row {idx}: {sorted(miss)}")
    hashes = [r.get("body_hash") for r in data]
    dupes = [h for h, n in Counter(hashes).items() if h and n > 1]
    detail = f"{len(data)} entries; latest dates={sorted({r.get('date') for r in data if r.get('date')})[-5:]}"
    if missing:
        return Check("reddit_draft_log", "fail", "; ".join(missing[:3]))
    if dupes:
        return Check("reddit_draft_log", "fail", f"duplicate body_hash values: {dupes[:5]}")
    if len(data) < 10:
        return Check("reddit_draft_log", "warn", detail + "; anti-repeat history is still shallow")
    return Check("reddit_draft_log", "pass", detail)


def cron_health() -> list[Check]:
    checks: list[Check] = []
    for cid, expected in REQUIRED_CRONS.items():
        d = run_json(["openclaw", "cron", "show", cid, "--json"])
        if not d:
            checks.append(Check(f"cron_{expected}", "fail", "cron show --json unavailable"))
            continue
        status = "pass"
        reasons = []
        if not d.get("enabled"):
            status = "fail"
            reasons.append("disabled")
        if d.get("deleteAfterRun"):
            status = "fail"
            reasons.append("deleteAfterRun=true")
        fa = d.get("failureAlert") or {}
        if not fa or fa.get("to") != "6608544825":
            status = "warn" if status == "pass" else status
            reasons.append("failure alert not routed to JT")
        state = d.get("state") or {}
        if state.get("lastRunStatus") not in (None, "ok"):
            status = "fail"
            reasons.append(f"lastRunStatus={state.get('lastRunStatus')}")
        if not reasons:
            reasons.append(f"enabled; last={state.get('lastRunStatus')}; delivery={state.get('lastDeliveryStatus')}")
        checks.append(Check(f"cron_{expected}", status, "; ".join(reasons)))
    return checks


def dynasty_recent_repeats() -> Check:
    d = run_json(["openclaw", "cron", "runs", "--id", "8b968751-6e59-42e5-b2ce-09f57d36176c", "--limit", "8"])
    if not d:
        return Check("dynasty_recent_repeat_pack", "warn", "could not inspect recent runs")

    packs = []
    blocked = 0
    for e in d.get("entries", []):
        s = e.get("summary") or ""
        urls = tuple(X_URL_RE.findall(s))
        if "BLOCKED:" in s:
            blocked += 1
        if urls:
            packs.append((e.get("runAtMs") or e.get("ts"), urls, s))

    if len(packs) >= 2 and packs[0][1] == packs[1][1]:
        latest_urls = set(packs[0][1])
        ledger_path = ROOT / "memory/sports-gm/dynasty-replies-ledger.jsonl"
        ledger_urls = set()
        if ledger_path.exists():
            for line in ledger_path.read_text(errors="ignore").splitlines():
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                if row.get("url"):
                    ledger_urls.add(row["url"])
        if latest_urls.issubset(ledger_urls):
            return Check(
                "dynasty_recent_repeat_pack",
                "warn",
                "latest two historical runs repeated, but repeated URLs are now sealed in ledger for future rejection",
            )
        return Check("dynasty_recent_repeat_pack", "fail", "latest two runs used identical X target URLs and repeats are not fully ledger-sealed")

    return Check("dynasty_recent_repeat_pack", "pass", f"inspected {len(packs)} recent packs; blocked runs={blocked}")


def cron_prompt_guards() -> Check:
    jobs_path = Path.home() / ".openclaw/cron/jobs.json"
    if not jobs_path.exists():
        return Check("cron_prompt_validator_guards", "fail", "~/.openclaw/cron/jobs.json missing")
    try:
        raw = json.loads(jobs_path.read_text())
    except Exception as e:
        return Check("cron_prompt_validator_guards", "fail", f"cannot read jobs.json: {e}")
    jobs = raw.get("jobs", []) if isinstance(raw, dict) else raw
    by_id = {j.get("id"): j for j in jobs if isinstance(j, dict)}
    required = {
        "8b968751-6e59-42e5-b2ce-09f57d36176c": [
            "scripts/social_engagement_audit.py --json --gate dynasty",
            "PRE-SEND VALIDATOR",
            "BLOCKED: social engagement validator failed",
        ],
        "bbe49024-458a-4496-9c7c-7a278615810f": [
            "scripts/social_engagement_audit.py --json --gate reddit",
            "PRE-SEND VALIDATOR",
            "BLOCKED: social engagement validator failed",
        ],
        "fe575759-c8b1-4715-ae5a-0dbe034b3c9b": [
            "scripts/social_engagement_audit.py --json --gate reddit",
            "PRE-SEND VALIDATOR",
        ],
        "33b8b0a2-e86c-4f51-aa4f-b8537def3107": [
            "scripts/social_engagement_audit.py --json --gate x",
            "PRE-SEND VALIDATOR",
            "direct X post URL",
        ],
    }
    missing = []
    for cid, needles in required.items():
        msg = ((by_id.get(cid) or {}).get("payload") or {}).get("message", "")
        for needle in needles:
            if needle not in msg:
                missing.append(f"{REQUIRED_CRONS.get(cid, cid)} missing {needle!r}")
    if missing:
        return Check("cron_prompt_validator_guards", "fail", "; ".join(missing[:5]))
    return Check("cron_prompt_validator_guards", "pass", "all social cron prompts include pre-send validator gates")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument(
        "--gate",
        choices=["all", "dynasty", "reddit", "x", "cron"],
        default="all",
        help="run only the checks relevant to one daily loop",
    )
    args = ap.parse_args()
    if args.gate == "dynasty":
        checks = [dynasty_ledger(), dynasty_recent_repeats()]
    elif args.gate == "reddit":
        checks = [reddit_draft_log()]
    elif args.gate == "x":
        checks = [latest_reply_targets(), older_reply_link_hygiene()]
    elif args.gate == "cron":
        checks = [cron_prompt_guards()]
        checks.extend(cron_health())
    else:
        checks = [latest_reply_targets(), older_reply_link_hygiene(), dynasty_ledger(), reddit_draft_log(), dynasty_recent_repeats(), cron_prompt_guards()]
        checks.extend(cron_health())
    summary = Counter(c.status for c in checks)
    ok = summary.get("fail", 0) == 0
    if args.json:
        print(json.dumps({"ok": ok, "summary": dict(summary), "checks": [asdict(c) for c in checks]}, indent=2))
    else:
        print(f"social_engagement_audit ok={ok} summary={dict(summary)}")
        for c in checks:
            print(f"[{c.status.upper()}] {c.name}: {c.detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
