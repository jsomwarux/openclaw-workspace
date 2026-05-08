#!/usr/bin/env python3
"""Discover recent posts and reconcile them into the App Marketing post registry.

Supported:
- ReelFarm/TikTok via /tiktok/posts
- X account discovery via X API

Design rule:
Planned draft rows are canonical. When a live post is discovered, update the
matching planned row with exact post_id/video_id/URL instead of appending a
second row. This keeps the draft -> posted -> metrics chain traceable.
"""
from __future__ import annotations

import fcntl
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path.home() / ".openclaw" / "workspace"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BASE = ROOT / "memory" / "app-marketing"
REGISTRY = BASE / "post-registry.jsonl"
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "how", "i", "in", "is", "it", "its", "me", "not", "of", "on", "or", "so",
    "that", "the", "this", "to", "was", "we", "what", "when", "where", "with",
    "you", "your", "now", "new", "same",
}


def locked_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open("a+")
    fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0)
    return f


def _parse_registry_text(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        raw = line.rstrip("\n")
        stripped = raw.strip()
        if not stripped:
            rows.append({"_kind": "blank", "_raw": raw})
            continue
        if stripped.startswith("#"):
            rows.append({"_kind": "comment", "_raw": raw})
            continue
        try:
            rows.append({"_kind": "json", "data": json.loads(stripped)})
        except Exception as exc:  # noqa: BLE001
            rows.append({"_kind": "raw", "_raw": raw, "_error": f"line {line_no}: {exc}"})
    return rows


def _serialize_registry_rows(rows: list[dict[str, Any]]) -> str:
    out: list[str] = []
    for row in rows:
        if row.get("_kind") == "json":
            out.append(json.dumps(row["data"], ensure_ascii=False))
        else:
            out.append(row.get("_raw", ""))
    return "\n".join(out).rstrip() + "\n"


def _json_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r["data"] for r in rows if r.get("_kind") == "json"]


def _account_norm(value: Any) -> str:
    return str(value or "").strip().lower().lstrip("@")


def _platform_norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _tokens(text: Any) -> set[str]:
    words = re.findall(r"[a-z0-9$]+", str(text or "").lower())
    return {w for w in words if len(w) > 1 and w not in STOPWORDS}


def _similarity(a: Any, b: Any) -> float:
    a_text = str(a or "").lower().strip()
    b_text = str(b or "").lower().strip()
    if not a_text or not b_text:
        return 0.0
    if a_text[:50] and a_text[:50] in b_text:
        return 1.0
    if b_text[:50] and b_text[:50] in a_text:
        return 1.0
    ta, tb = _tokens(a_text), _tokens(b_text)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(1, len(ta | tb))


def _date_or_none(value: Any) -> date | None:
    try:
        if not value:
            return None
        return datetime.fromisoformat(str(value)[:10]).date()
    except Exception:
        return None


def _is_planned(row: dict[str, Any]) -> bool:
    return str(row.get("status") or "").lower() == "planned" or str(row.get("url_or_id") or "").startswith("planned:")


def _registry_key(row: dict[str, Any]) -> tuple[str, str]:
    return (_platform_norm(row.get("platform")), str(row.get("url_or_id") or ""))


def _matching_planned_index(existing: list[dict[str, Any]], live: dict[str, Any]) -> int | None:
    live_platform = _platform_norm(live.get("platform"))
    live_product = str(live.get("product_slug") or "")
    live_account = _account_norm(live.get("account"))
    live_text = live.get("hook_or_title") or live.get("content") or ""
    live_date = _date_or_none(live.get("date"))
    best: tuple[float, int] | None = None
    for idx, row in enumerate(existing):
        if not _is_planned(row):
            continue
        if _platform_norm(row.get("platform")) != live_platform:
            continue
        if live_product and row.get("product_slug") and str(row.get("product_slug")) != live_product:
            continue
        if live_account and row.get("account") and _account_norm(row.get("account")) != live_account:
            continue
        planned_date = _date_or_none(row.get("date"))
        if planned_date and live_date and abs((live_date - planned_date).days) > 14:
            continue
        score = _similarity(row.get("hook_or_title") or row.get("content") or "", live_text)
        # Strong exact-ish text match, or a high-confidence single planned candidate.
        if score >= 0.32:
            if best is None or score > best[0]:
                best = (score, idx)
    return best[1] if best else None


def _merge_live_into_planned(planned: dict[str, Any], live: dict[str, Any]) -> dict[str, Any]:
    merged = dict(planned)
    for key in ["date", "week_of", "product_slug", "platform", "account", "url_or_id", "post_id", "video_id", "hook_or_title"]:
        if live.get(key) not in (None, ""):
            merged[key] = live[key]
    merged["status"] = "posted"
    merged["posted_date"] = live.get("date") or planned.get("posted_date") or planned.get("date")
    merged["discovered_at"] = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    merged["discovered_from"] = live.get("source_system") or "auto-discovery"
    merged["planned_url_or_id"] = planned.get("url_or_id")
    if planned.get("draft_path"):
        merged["draft_path"] = planned.get("draft_path")
    return merged


def _upsert_live_rows(live_rows: list[dict[str, Any]]) -> tuple[int, int]:
    if not live_rows:
        return (0, 0)
    with locked_file(REGISTRY) as f:
        parsed = _parse_registry_text(f.read())
        existing = _json_rows(parsed)
        existing_keys = {_registry_key(r) for r in existing}
        appended = 0
        reconciled = 0
        for live in live_rows:
            key = _registry_key(live)
            if not live.get("url_or_id") or key in existing_keys:
                continue
            planned_idx = _matching_planned_index(existing, live)
            if planned_idx is not None:
                # Update both the convenience list and the parsed row object.
                existing[planned_idx] = _merge_live_into_planned(existing[planned_idx], live)
                json_seen = -1
                for row in parsed:
                    if row.get("_kind") != "json":
                        continue
                    json_seen += 1
                    if json_seen == planned_idx:
                        row["data"] = existing[planned_idx]
                        break
                existing_keys.add(key)
                reconciled += 1
            else:
                parsed.append({"_kind": "json", "data": live})
                existing.append(live)
                existing_keys.add(key)
                appended += 1
        if appended or reconciled:
            f.seek(0)
            f.truncate()
            f.write(_serialize_registry_rows(parsed))
        return (appended, reconciled)


def append_reelfarm() -> tuple[int, int]:
    from scripts.app_marketing_connectors import reelfarm_metrics

    rows = []
    for metric in reelfarm_metrics.discover_recent_metrics(timeframe=30):
        post_id = str(metric.get("post_id") or metric.get("url") or "")
        if not post_id:
            continue
        rows.append({
            "date": metric.get("date"),
            "week_of": metric.get("week_of"),
            "product_slug": metric.get("product_slug"),
            "platform": "tiktok",
            "account": str(metric.get("account") or metric.get("notes", "").replace("reelfarm /tiktok/posts analytics; account=", "")),
            "url_or_id": post_id,
            "hook_or_title": metric.get("content_id_or_hook"),
            "source_system": "reelfarm-discovery",
            "post_id": post_id,
            "video_id": metric.get("video_id"),
        })
    return _upsert_live_rows(rows)


def append_x() -> tuple[int, int]:
    from scripts.app_marketing_connectors import x_metrics

    account_map_path = BASE / "account-map.json"
    rows = []
    if not account_map_path.exists():
        return (0, 0)
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
            if not url:
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
                "hook_or_title": (post.get("text") or "")[:180],
                "source_system": "x-discovery",
                "post_id": post.get("id"),
            })
    return _upsert_live_rows(rows)


def main() -> int:
    reelfarm_added, reelfarm_reconciled = append_reelfarm()
    x_added, x_reconciled = append_x()
    print(
        "APP_MARKETING_DISCOVER_OK "
        f"reelfarm_added={reelfarm_added} reelfarm_reconciled={reelfarm_reconciled} "
        f"x_added={x_added} x_reconciled={x_reconciled}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
