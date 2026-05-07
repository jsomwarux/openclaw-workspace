from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
ENV_PATH = Path.home() / ".config" / "env" / "global.env"


def _load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _tweet_id(value: str) -> str | None:
    value = value.strip()
    if re.fullmatch(r"\d{5,}", value):
        return value
    m = re.search(r"/status(?:es)?/(\d+)", value)
    if m:
        return m.group(1)
    return None


def fetch(post: dict) -> dict | None:
    """Fetch X public metrics for a tweet using bearer-token auth.

    X docs indicate public_metrics are available with bearer auth and include
    impression_count, like_count, reply_count, retweet_count, quote_count,
    bookmark_count when tier/access allows. Private click metrics require user
    context and are intentionally not attempted here.
    """
    _load_env()
    token = os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN")
    if not token:
        return None
    tid = _tweet_id(str(post.get("url_or_id") or post.get("url") or ""))
    if not tid:
        return None
    params = urllib.parse.urlencode({"tweet.fields": "public_metrics,created_at"})
    url = f"https://api.x.com/2/tweets/{tid}?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "User-Agent": "OpenClawAppMarketingMetrics/0.1"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 - fixed X API host
        data = json.loads(resp.read().decode("utf-8"))
    tweet = data.get("data") or {}
    metrics = tweet.get("public_metrics") or {}
    impressions = int(metrics.get("impression_count") or 0)
    likes = int(metrics.get("like_count") or 0)
    replies = int(metrics.get("reply_count") or 0)
    reposts = int(metrics.get("retweet_count") or 0) + int(metrics.get("quote_count") or 0)
    bookmarks = int(metrics.get("bookmark_count") or 0)
    return {
        "date": post.get("date") or (tweet.get("created_at") or "")[:10],
        "week_of": post.get("week_of") or post.get("date") or (tweet.get("created_at") or "")[:10],
        "product_slug": post.get("product_slug"),
        "platform": "x",
        "content_id_or_hook": post.get("hook_or_title") or tweet.get("text", "")[:100],
        "views_or_impressions": impressions,
        "likes": likes,
        "comments": replies,
        "reposts": reposts,
        "saves": bookmarks,
        "url": post.get("url_or_id"),
        "notes": "x public_metrics via bearer token; private clicks require user-context auth",
    }


def _get_json(url: str) -> dict:
    _load_env()
    token = os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN")
    if not token:
        raise RuntimeError("missing X_BEARER_TOKEN")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "User-Agent": "OpenClawAppMarketingMetrics/0.1"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 - fixed X API host
        return json.loads(resp.read().decode("utf-8"))


def get_user_id(username: str) -> str | None:
    username = username.lstrip("@")
    params = urllib.parse.urlencode({"user.fields": "username,name"})
    data = _get_json(f"https://api.x.com/2/users/by/username/{urllib.parse.quote(username)}?{params}")
    return (data.get("data") or {}).get("id")


def recent_posts(username: str, max_results: int = 10) -> list[dict]:
    uid = get_user_id(username)
    if not uid:
        return []
    params = urllib.parse.urlencode({
        "max_results": max(5, min(max_results, 100)),
        "tweet.fields": "created_at,public_metrics",
        "exclude": "retweets,replies",
    })
    data = _get_json(f"https://api.x.com/2/users/{uid}/tweets?{params}")
    rows=[]
    for t in data.get("data") or []:
        rows.append({
            "id": t.get("id"),
            "text": t.get("text"),
            "created_at": t.get("created_at"),
            "public_metrics": t.get("public_metrics") or {},
            "url": f"https://x.com/{username.lstrip('@')}/status/{t.get('id')}",
        })
    return rows


def classify_product(username: str, text: str) -> str:
    u = username.lower().lstrip("@")
    t = text.lower()
    if "nash" in u or "nash satoshi" in t or "token" in t or "crypto" in t or "4 llm" in t or "4 ai" in t:
        return "nash-satoshi"
    if "vista" in t or "movie" in t or "film" in t or "letterboxd" in t or "rating" in t:
        return "vista"
    return "unknown"
