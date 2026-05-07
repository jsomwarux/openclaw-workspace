#!/usr/bin/env python3
"""Discover recent posts automatically and append to App Marketing post registry.

This reduces manual URL entry. Supported now:
- ReelFarm/TikTok via /tiktok/posts
- X account discovery is planned; X public metrics connector works once tweet URLs/IDs are known.
"""
from __future__ import annotations

import fcntl
import json
import sys
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BASE = ROOT / "memory" / "app-marketing"
REGISTRY = BASE / "post-registry.jsonl"


def locked_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open('a+')
    fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0)
    return f


def _existing_keys_from_text(text: str) -> set[tuple[str, str]]:
    keys=set()
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            obj=json.loads(line)
        except Exception:
            continue
        keys.add((str(obj.get('platform')), str(obj.get('url_or_id'))))
    return keys


def _existing_keys() -> set[tuple[str, str]]:
    return _existing_keys_from_text(REGISTRY.read_text() if REGISTRY.exists() else "")


def append_reelfarm() -> int:
    from scripts.app_marketing_connectors import reelfarm_metrics
    existing=_existing_keys()
    rows=[]
    for metric in reelfarm_metrics.discover_recent_metrics(timeframe=30):
        url_or_id=str(metric.get('url') or '')
        key=('tiktok', url_or_id)
        if not url_or_id or key in existing:
            continue
        rows.append({
            'date': metric.get('date'),
            'week_of': metric.get('week_of'),
            'product_slug': metric.get('product_slug'),
            'platform': 'tiktok',
            'account': metric.get('notes','').replace('reelfarm /tiktok/posts analytics; account=',''),
            'url_or_id': url_or_id,
            'hook_or_title': metric.get('content_id_or_hook'),
            'source_system': 'reelfarm-discovery',
            'post_id': url_or_id,
        })
    if rows:
        with locked_file(REGISTRY) as f:
            existing = _existing_keys_from_text(f.read())
            f.seek(0, 2)
            written = 0
            for r in rows:
                key = (str(r.get('platform')), str(r.get('url_or_id')))
                if key in existing:
                    continue
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
                existing.add(key)
                written += 1
            return written
    return 0


def append_x() -> int:
    from scripts.app_marketing_connectors import x_metrics
    account_map_path = BASE / "account-map.json"
    existing = _existing_keys()
    rows = []
    if not account_map_path.exists():
        return 0
    data = json.loads(account_map_path.read_text())
    for acct in data.get("x", []):
        username = acct.get("username") or str(acct.get("account", "")).lstrip("@")
        if not username or acct.get("status") not in {"active", None}:
            continue
        try:
            posts = x_metrics.recent_posts(username, 10)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN x_discovery_failed username={username} error={exc}")
            continue
        for post in posts:
            url = post.get("url")
            key = ("x", str(url))
            if not url or key in existing:
                continue
            slug = acct.get("product_slug")
            if username.lower() in {"jts_14", "jt__crypto"}:
                slug = x_metrics.classify_product(username, post.get("text") or "")
                if slug == "unknown":
                    # Shared personal accounts should not pollute product analytics.
                    continue
            rows.append({
                "date": str(post.get("created_at") or "")[:10],
                "week_of": str(post.get("created_at") or "")[:10],
                "product_slug": slug,
                "platform": "x",
                "account": "@" + username.lstrip("@"),
                "url_or_id": url,
                "hook_or_title": (post.get("text") or "")[:140],
                "source_system": "x-discovery",
                "post_id": post.get("id"),
            })
    if rows:
        with locked_file(REGISTRY) as f:
            existing = _existing_keys_from_text(f.read())
            f.seek(0, 2)
            written = 0
            for r in rows:
                key = (str(r.get('platform')), str(r.get('url_or_id')))
                if key in existing:
                    continue
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
                existing.add(key)
                written += 1
            return written
    return 0


def main() -> int:
    reelfarm_added = append_reelfarm()
    x_added = append_x()
    print(f'APP_MARKETING_DISCOVER_OK reelfarm_added={reelfarm_added} x_added={x_added}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
