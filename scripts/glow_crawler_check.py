#!/usr/bin/env python3
"""Read-only Glow Index crawler-access diagnostic.

Checks whether public discovery/category routes are reachable without Cloudflare
challenge HTML. Does not modify Cloudflare, Replit, or app config.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
OUT = ROOT / "memory" / "app-marketing" / "glow-crawler-access-status.json"
URLS = [
    "https://glowindex.co/robots.txt",
    "https://glowindex.co/sitemap.xml",
    "https://glowindex.co/llms.txt",
    "https://glowindex.co/rankings",
    "https://glowindex.co/categories",
    "https://glowindex.co/categories/serum",
]
UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
CHALLENGE_MARKERS = [
    "just a moment",
    "cf-browser-verification",
    "challenge-platform",
    "cf_chl_",
    "cloudflare",
]


def check(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*"})
    status = None
    body = ""
    error = None
    headers = {}
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.status
            headers = {k.lower(): v for k, v in resp.headers.items()}
            body = resp.read(5000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        headers = {k.lower(): v for k, v in e.headers.items()}
        body = e.read(5000).decode("utf-8", errors="replace")
        error = f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
    lower = body.lower()
    challenged = any(marker in lower for marker in CHALLENGE_MARKERS) and status in {403, 429, 503}
    return {
        "url": url,
        "status_code": status,
        "ok": status == 200 and not challenged,
        "cloudflare_challenge": challenged,
        "server": headers.get("server"),
        "content_type": headers.get("content-type"),
        "error": error,
    }


def main() -> int:
    rows = [check(url) for url in URLS]
    all_clear = all(r["ok"] for r in rows)
    result = {
        "date": date.today().isoformat(),
        "user_agent": UA,
        "all_clear": all_clear,
        "rows": rows,
        "next_action": (
            "Crawler gate is clear. The first Glow SEO/GEO batch is live; "
            "continue post-deploy measurement before building another "
            "category or methodology page."
            if all_clear
            else (
                "If any discovery/category row is not ok, first verify the "
                "skincare-rankings proxy.ts public-route fix is deployed/rebuilt. "
                "These paths previously redirected to Clerk sign-in, which then "
                "surfaced as a Cloudflare challenge on accounts.glowindex.co."
            )
        ),
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return 0 if result["all_clear"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
