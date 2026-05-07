#!/usr/bin/env python3
"""Collect app marketing metrics from available connectors.

MVP behavior:
- Reads memory/app-marketing/post-registry.jsonl
- Uses connectors that can run without sensitive auth first
- Appends normalized rows to memory/app-marketing/metrics-inbox.jsonl
- Refreshes weekly-scoreboard.md

Private API connectors are intentionally opt-in and fail closed when env vars are absent.
"""
from __future__ import annotations

import importlib
import fcntl
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BASE = ROOT / "memory" / "app-marketing"
POSTS = BASE / "post-registry.jsonl"
INBOX = BASE / "metrics-inbox.jsonl"


def locked_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open('a+')
    fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0)
    return f
CONNECTORS = {
    "reddit": "scripts.app_marketing_connectors.reddit_metrics",
    "x": "scripts.app_marketing_connectors.x_metrics",
    "tiktok": "scripts.app_marketing_connectors.reelfarm_metrics",
    "reelfarm": "scripts.app_marketing_connectors.reelfarm_metrics",
    "app_store": "scripts.app_marketing_connectors.app_store_metrics",
    "web": "scripts.app_marketing_connectors.web_metrics",
}


def load_posts() -> list[dict]:
    posts=[]
    if not POSTS.exists():
        return posts
    for i,line in enumerate(POSTS.read_text().splitlines(),1):
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            posts.append(json.loads(line))
        except Exception as exc:  # noqa: BLE001
            print(f"WARN post-registry line {i} invalid: {exc}", file=sys.stderr)
    return posts


def _metric_key(row: dict) -> tuple[str, str, str, str, str]:
    return (
        str(row.get("date") or ""),
        str(row.get("product_slug") or ""),
        str(row.get("platform") or ""),
        str(row.get("url") or ""),
        str(row.get("content_id_or_hook") or ""),
    )


def _existing_metric_keys_from_text(text: str) -> set[tuple[str, str, str, str, str]]:
    keys=set()
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            keys.add(_metric_key(json.loads(line)))
        except Exception:
            continue
    return keys


def _existing_metric_keys() -> set[tuple[str, str, str, str, str]]:
    return _existing_metric_keys_from_text(INBOX.read_text() if INBOX.exists() else "")


def append_metrics(rows: list[dict]) -> int:
    if not rows:
        return 0
    with locked_file(INBOX) as f:
        existing_text = f.read()
        existing_keys = _existing_metric_keys_from_text(existing_text)
        f.seek(0, 2)
        if existing_text and not existing_text.endswith('\n'):
            f.write('\n')
        written = 0
        for r in rows:
            key=_metric_key(r)
            if key in existing_keys:
                continue
            existing_keys.add(key)
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            written += 1
        return written


def main() -> int:
    posts=load_posts()
    rows=[]
    for post in posts:
        platform=str(post.get('platform','')).lower()
        mod_name=CONNECTORS.get(platform)
        if not mod_name:
            print(f"SKIP unsupported platform={platform} url_or_id={post.get('url_or_id')}")
            continue
        try:
            mod=importlib.import_module(mod_name)
            result=mod.fetch(post)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN connector_failed platform={platform} id={post.get('url_or_id')} error={exc}", file=sys.stderr)
            continue
        if result:
            rows.append(result)
    appended = append_metrics(rows)
    subprocess.run([sys.executable, str(ROOT/'scripts/app_marketing_metrics.py')], check=False)
    print(f"APP_MARKETING_COLLECT_OK posts={len(posts)} metrics_rows={len(rows)} appended={appended}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
