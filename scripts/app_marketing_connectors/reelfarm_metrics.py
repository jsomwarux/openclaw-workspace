from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ENV_PATH = Path.home() / ".config" / "env" / "global.env"
BASE = "https://reel.farm/api/v1"
ACCOUNT_MAP = Path.home() / ".openclaw" / "workspace" / "memory" / "app-marketing" / "account-map.json"
GENERIC_HOOKS = {"", "watch this", "untitled", "draft", "video"}


def _load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _get_json(path: str, params: dict | None = None) -> dict:
    _load_env()
    key = os.environ.get("REELFARM_API_KEY")
    if not key:
        raise RuntimeError("missing REELFARM_API_KEY")
    qs = "?" + urllib.parse.urlencode(params or {}) if params else ""
    req = urllib.request.Request(
        f"{BASE}{path}{qs}",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "OpenClawAppMarketingMetrics/0.1"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 - fixed ReelFarm API host
        return json.loads(resp.read().decode("utf-8"))


def _account_rows() -> list[dict]:
    if not ACCOUNT_MAP.exists():
        return []
    try:
        return (json.loads(ACCOUNT_MAP.read_text()).get("reelfarm") or [])
    except Exception:
        return []


def account_slug_map() -> dict[str, str]:
    out = {}
    for row in _account_rows():
        slug = row.get("product_slug")
        if not slug:
            continue
        for key in [row.get("account_username"), row.get("tiktok_account_id"), str(row.get("account", "")).lstrip("@")]:
            if key:
                out[str(key).lower()] = slug
    return out


def account_id_for_product(product_slug: str | None) -> str | None:
    if not product_slug:
        return None
    for row in _account_rows():
        if row.get("product_slug") == product_slug and row.get("tiktok_account_id"):
            return str(row["tiktok_account_id"])
    return None


def product_for_candidate(candidate: dict) -> str | None:
    m = account_slug_map()
    username = str(candidate.get("account_username") or "").lower()
    account_id = str(candidate.get("tiktok_account_id") or "").lower()
    return m.get(username) or m.get(account_id)


def list_accounts() -> list[dict]:
    data = _get_json("/tiktok/accounts")
    return data.get("accounts") or []


def list_posts(timeframe: int | str = 30, tiktok_account_id: str | None = None, limit: int = 200) -> list[dict]:
    params: dict[str, str | int] = {"timeframe": timeframe, "limit": min(limit, 200), "sort": "recent"}
    if tiktok_account_id:
        params["tiktok_account_id"] = tiktok_account_id
    data = _get_json("/tiktok/posts", params)
    return data.get("posts") or []


def _candidate_allowed(post: dict, candidate: dict) -> bool:
    expected_product = post.get("product_slug")
    actual_product = product_for_candidate(candidate)
    if expected_product and actual_product and expected_product != actual_product:
        return False
    expected_account = post.get("tiktok_account_id") or account_id_for_product(expected_product)
    if expected_account and str(candidate.get("tiktok_account_id") or "") != str(expected_account):
        return False
    return True


def _matches_post(post: dict, candidate: dict) -> bool:
    if not _candidate_allowed(post, candidate):
        return False
    target_post_id = str(post.get("post_id") or post.get("url_or_id") or "").strip()
    target_video_id = str(post.get("video_id") or "").strip()
    if target_post_id and target_post_id == str(candidate.get("post_id") or ""):
        return True
    if target_video_id and target_video_id == str(candidate.get("video_id") or ""):
        return True
    # Hook matching is only allowed when explicitly requested and sufficiently unique.
    if not post.get("allow_hook_match"):
        return False
    hook = str(post.get("hook_or_title") or "").lower().strip()
    title = str(candidate.get("title") or "").lower()
    if hook in GENERIC_HOOKS or len(hook) < 30:
        return False
    return hook[:60] in title


def _normalize(post: dict, candidate: dict) -> dict:
    product = post.get("product_slug") or product_for_candidate(candidate)
    return {
        "date": post.get("date") or str(candidate.get("published_at") or "")[:10],
        "week_of": post.get("week_of") or post.get("date") or str(candidate.get("published_at") or "")[:10],
        "product_slug": product,
        "platform": "tiktok",
        "content_id_or_hook": post.get("hook_or_title") or candidate.get("title"),
        "views_or_impressions": int(candidate.get("view_count") or 0),
        "likes": int(candidate.get("like_count") or 0),
        "comments": int(candidate.get("comment_count") or 0),
        "saves": int(candidate.get("bookmark_count") or 0),
        "reposts": int(candidate.get("share_count") or 0),
        "url": post.get("url_or_id") or str(candidate.get("post_id") or candidate.get("video_id") or ""),
        "post_id": str(candidate.get("post_id") or ""),
        "video_id": str(candidate.get("video_id") or ""),
        "account": candidate.get("account_username"),
        "notes": f"reelfarm /tiktok/posts analytics; account={candidate.get('account_username')}",
    }


def fetch(post: dict) -> dict | None:
    """Fetch TikTok analytics from ReelFarm /tiktok/posts.

    Safe matching rules:
    - Prefer exact TikTok post_id or ReelFarm video_id.
    - Enforce product/account match from account-map.json.
    - Never match generic hooks like "watch this" by title.
    """
    account_id = post.get("tiktok_account_id") or account_id_for_product(post.get("product_slug"))
    posts = list_posts(timeframe=post.get("timeframe") or 30, tiktok_account_id=account_id)
    for candidate in posts:
        if _matches_post(post, candidate):
            return _normalize(post, candidate)
    return None


def discover_recent_metrics(product_slug: str | None = None, timeframe: int | str = 30) -> list[dict]:
    rows=[]
    acct_map = account_slug_map()
    for p in list_posts(timeframe=timeframe):
        slug = product_slug or product_for_candidate(p)
        username = str(p.get("account_username") or "").lower()
        account_id = str(p.get("tiktok_account_id") or "").lower()
        title = str(p.get("title") or "").lower()
        if not slug:
            slug = acct_map.get(username) or acct_map.get(account_id)
        if not slug:
            if "nash" in username or "nash" in title or "crypto" in title or "token" in title:
                slug = "nash-satoshi"
            elif username == "mashed386" or "vista" in title or "movie" in title or "film" in title or "imdb" in title or "rating" in title:
                slug = "vista"
            else:
                slug = "unknown"
        rows.append(_normalize({"product_slug": slug}, p))
    return rows


def inspect_available_fields(limit: int = 5) -> dict:
    accounts = list_accounts()
    posts = list_posts(limit=limit)
    return {
        "accounts": [{k: a.get(k) for k in ["tiktok_account_id", "account_name", "account_username"]} for a in accounts],
        "post_keys": [sorted(p.keys()) for p in posts[:limit]],
        "sample_metrics": [
            {k: p.get(k) for k in ["post_id", "video_id", "title", "view_count", "like_count", "comment_count", "share_count", "bookmark_count", "account_username", "published_at"]}
            for p in posts[:limit]
        ],
    }
