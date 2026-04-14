#!/usr/bin/env python3
"""
API Discovery Pipeline — finds newly launched/discovered APIs from 4 sources.

Sources:
  1. APIs.guru — new APIs added in last 30 days (catalog tracks 'added' date)
  2. Product Hunt RSS — newest tools tagged API / developer
  3. Hacker News "new" — pull top 10 from past 2 days for API/developer mentions
  4. AlternativeTo API mentions — search for "alternatives to [X] API" pattern

Output: memory/passive-income/weekly-apis.md
"""

import json
import re
import time as time_module
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict

import requests
import xml.etree.ElementTree as ET

WORKSPACE = Path(__file__).resolve().parent.parent
OUTPUT_FILE = WORKSPACE / "memory" / "passive-income" / "weekly-apis.md"
CACHE_DIR = WORKSPACE / "memory" / "passive-income" / ".apis-cache"
CACHE_TTL_DAYS = 3
CUTOFF_DAYS = 30

HEADERS = {"User-Agent": "PassiveIncomeScout/1.0 (API discovery)"}


def _cache_path(key: str) -> Path:
    return CACHE_DIR / (key.replace(" ", "_") + ".json")


def _cached(key: str) -> Optional[Dict]:
    p = _cache_path(key)
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age < timedelta(days=CACHE_TTL_DAYS):
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def _save(key: str, data: Dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_path(key).write_text(json.dumps(data))
    except Exception:
        pass


# ── Source 1: APIs.guru (new in last 30 days) ──────────────────────────────
def fetch_apis_guru() -> Dict:
    """Returns new APIs added to APIs.guru catalog in last CUTOFF_DAYS."""
    cache_key = "apis_guru_new"
    cached = _cached(cache_key)
    if cached:
        return cached

    print("  Fetching APIs.guru catalog...")
    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=CUTOFF_DAYS)

    try:
        resp = requests.get(
            "https://api.apis.guru/v2/list.json",
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        catalog = resp.json()

        for api_name, api_data in catalog.items():
            preferred = api_data.get("preferred", "")
            versions = api_data.get("versions", {})
            version_data = versions.get(preferred, versions.get(list(versions.keys())[0], {}))
            if not version_data:
                continue

            added_str = version_data.get("added", "")
            if not added_str:
                continue

            try:
                added_date = datetime.fromisoformat(added_str.replace("Z", "+00:00"))
                if added_date.tzinfo:
                    added_date = added_date.replace(tzinfo=timezone.utc)
                else:
                    added_date = added_date.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue

            if added_date >= cutoff:
                info = version_data.get("info", {})
                results.append({
                    "name": info.get("title", api_name),
                    "description": (info.get("description", "") or "")[:200],
                    "url": info.get("contact", {}).get("url", ""),
                    "category": info.get("tags", ["unknown"])[0] if info.get("tags") else "unknown",
                    "added": added_str,
                })

    except Exception as e:
        print("  ⚠ APIs.guru error: " + str(e))

    result = {"source": "APIs.guru", "apis": results, "fetched_at": datetime.now().isoformat()}
    _save(cache_key, result)
    return result


# ── Source 2: Product Hunt RSS (new tools — API/dev category) ───────────────
def fetch_product_hunt() -> Dict:
    """Pull top 10 from PH RSS for API/developer/devtools tags."""
    cache_key = "product_hunt_new"
    cached = _cached(cache_key)
    if cached:
        return cached

    print("  Fetching Product Hunt RSS...")
    results = []

    try:
        resp = requests.get(
            "https://www.producthunt.com/feed",
            headers=HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        ns = {"ph": "http://www.w3.org/2005/Atom"}

        for item in root.findall("ph:entry", ns)[:15]:
            name_el = item.find("ph:name", ns)
            tagline = item.find("ph:tagline", ns)
            url_el = item.find("ph:url", ns)
            topic_els = item.findall("ph:topics/ph:topic/ph:name", ns)

            name = name_el.text if name_el is not None else ""
            tagline_text = tagline.text if tagline is not None else ""
            url = url_el.text if url_el is not None else ""
            topics = [t.text for t in topic_els if t.text]

            # Filter for API/developer tools
            api_signal = any(
                kw in (tagline_text + " " + " ".join(topics)).lower()
                for kw in ["api", "developer", "devtool", "integration", "webhook", "sdk", "cli"]
            )
            if not api_signal:
                continue

            results.append({
                "name": name,
                "tagline": tagline_text,
                "url": url,
                "topics": topics,
            })
            if len(results) >= 10:
                break

    except Exception as e:
        print("  ⚠ Product Hunt error: " + str(e))

    result = {"source": "Product Hunt", "tools": results, "fetched_at": datetime.now().isoformat()}
    _save(cache_key, result)
    return result


# ── Source 3: Hacker News "new" — API/dev mentions ─────────────────────────
def fetch_hacker_news() -> Dict:
    """Pull top stories from HN 'newest' API, filter for API/dev tools."""
    cache_key = "hacker_news_api"
    cached = _cached(cache_key)
    if cached:
        return cached

    print("  Fetching Hacker News newest...")
    results = []

    try:
        # Get top 50 newest stories
        resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/newstories.json",
            headers=HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
        story_ids = resp.json()[:50]

        # Fetch each story in batch (batched requests reduce overhead)
        for sid in story_ids:
            try:
                sresp = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    headers=HEADERS,
                    timeout=10,
                )
                sresp.raise_for_status()
                story = sresp.json()
                if not story:
                    continue

                title = story.get("title", "")
                url = story.get("url", "")
                score = story.get("score", 0)

                # Filter: API, SDK, dev tool, developer tool, AI API, etc.
                if not any(kw in title.lower() for kw in [
                    "api", "sdk", "library", "framework", "devtool",
                    "open-source", "developer", "cli tool", "webhook",
                    "integration", " wrapper", "sdk", "tool",
                ]):
                    continue

                results.append({
                    "title": title,
                    "url": url,
                    "score": score,
                    "hn_id": sid,
                })

                if len(results) >= 10:
                    break

            except Exception:
                continue

            time_module.sleep(0.1)  # Be respectful (no rate limit but don't spam)

    except Exception as e:
        print("  ⚠ HN error: " + str(e))

    result = {"source": "Hacker News", "stories": results, "fetched_at": datetime.now().isoformat()}
    _save(cache_key, result)
    return result


# ── Source 4: RapidAPI Developer Blog (new APIs) ────────────────────────────
def fetch_rapidapi_discover() -> Dict:
    """Search for new API launches via Brave Search (developer search)."""
    cache_key = "rapidapi_discover"
    cached = _cached(cache_key)
    if cached:
        return cached

    print("  Searching for new API launches...")
    results = []

    # Use a focused search — new API launches in last 30 days
    search_queries = [
        "new API launched 2026",
        "announced new API developer tool 2026",
        "launched API integration platform 2026",
    ]

    for query in search_queries:
        try:
            # Brave Search via API
            resp = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": 5},
                headers={
                    **HEADERS,
                    "Accept": "application/json",
                    "X-Subscription-Token": "BSDA1JMiB_MBiN9z2d5x1Y0a-MqBbI4P4aSY11x7Q1M",
                },
                timeout=10,
            )
            if resp.status_code != 200:
                continue

            data = resp.json()
            web_results = data.get("web", {}).get("results", {}).get("hits", [])
            for hit in web_results[:3]:
                results.append({
                    "title": hit.get("title", ""),
                    "url": hit.get("url", ""),
                    "description": hit.get("description", "")[:150],
                })

            time_module.sleep(2)

        except Exception as e:
            print("  ⚠ RapidAPI discover error: " + str(e))
            continue

    result = {"source": "Developer Search", "discoveries": results, "fetched_at": datetime.now().isoformat()}
    _save(cache_key, result)
    return result


# ── Combine all sources ──────────────────────────────────────────────────────
def main():
    print("=== API Discovery Pipeline ===\n")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    import json

    sources = [
        ("APIs.guru", fetch_apis_guru),
        ("Product Hunt", fetch_product_hunt),
        ("Hacker News", fetch_hacker_news),
        ("Developer Search", fetch_rapidapi_discover),
    ]

    all_results = {}
    for name, fn in sources:
        print("[" + name + "]")
        try:
            result = fn()
            all_results[name] = result
            if name == "APIs.guru":
                print("  ✅ " + str(len(result.get("apis", []))) + " new APIs")
            elif name == "Product Hunt":
                print("  ✅ " + str(len(result.get("tools", []))) + " PH tools")
            elif name == "Hacker News":
                print("  ✅ " + str(len(result.get("stories", []))) + " HN stories")
            elif name == "Developer Search":
                print("  ✅ " + str(len(result.get("discoveries", []))) + " discoveries")
        except Exception as e:
            print("  ⚠ Error: " + str(e))
            all_results[name] = {"source": name, "error": str(e)}
        print()

    # Write report
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    lines = [
        "# API Intelligence Report — " + date_str,
        "_Newly discovered APIs and dev tools — 4 sources checked_",
        "Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"),
        "",
    ]

    apis_guru = all_results.get("APIs.guru", {})
    ph = all_results.get("Product Hunt", {})
    hn = all_results.get("Hacker News", {})
    discover = all_results.get("Developer Search", {})

    total_new = len(apis_guru.get("apis", []))
    total_ph = len(ph.get("tools", []))
    total_hn = len(hn.get("stories", []))
    total_discover = len(discover.get("discoveries", []))

    lines.append(
        "**Totals:** " + str(total_new) + " new APIs | " + str(total_ph) + " PH tools | "
        + str(total_hn) + " HN stories | " + str(total_discover) + " discoveries"
    )
    lines.append("")

    if apis_guru.get("apis"):
        lines.append("## APIs.guru — Newly Added (" + str(CUTOFF_DAYS) + " days)")
        for api in apis_guru["apis"][:20]:
            lines.append("- **" + api["name"] + "** — " + api["description"][:100] + " ([link](" + api["url"] + "))")
            lines.append("  _category: " + api["category"] + " | added: " + api["added"] + "_")
        lines.append("")

    if ph.get("tools"):
        lines.append("## Product Hunt — API / Developer Tools")
        for t in ph["tools"]:
            lines.append("- **" + t["name"] + "** — " + t["tagline"])
            lines.append("  _" + ", ".join(t["topics"]) + "_ | [link](" + t["url"] + ")")
        lines.append("")

    if hn.get("stories"):
        lines.append("## Hacker News — Developer Tool Mentions")
        for s in sorted(hn["stories"], key=lambda x: x["score"], reverse=True)[:10]:
            lines.append("- **" + s["title"] + "** (score: " + str(s["score"]) + ") | [link](" + s["url"] + ")")
        lines.append("")

    if discover.get("discoveries"):
        lines.append("## Developer Search — New API Launches")
        for d in discover["discoveries"]:
            lines.append("- **" + d["title"] + "**")
            lines.append("  " + d.get("description", "")[:150] + " ([link](" + d["url"] + "))")
        lines.append("")

    if not any([apis_guru.get("apis"), ph.get("tools"), hn.get("stories"), discover.get("discoveries")]):
        lines.append("_No new APIs found. Catalogs may be mature — try again next week._")

    lines.append("")
    lines.append("## Scout Guidance")
    lines.append(
        "- APIs.guru new entries = high signal (verified by catalog maintainers)"
        "- Product Hunt tools = very early signal (pre-launch or launch-day)"
        "- HN developer tools = strong community validation signal"
        "- Developer Search = supplement only (check 1–2×/week)"
    )

    OUTPUT_FILE.write_text("\n".join(lines))
    total = total_new + total_ph + total_hn
    print("✅ API Discovery done — " + str(total) + " new items → " + OUTPUT_FILE.name)


if __name__ == "__main__":
    main()
