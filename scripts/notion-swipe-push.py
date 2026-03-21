#!/usr/bin/env python3
"""
notion-swipe-push.py — Push a viral post to the Notion Swipe File database.
Includes duplicate detection: skips posts with text matching existing entries (first 120 chars).

Usage:
  python3 notion-swipe-push.py \
    --text "Full post text here" \
    --author "@handle" \
    --url "https://x.com/..." \
    --niche "AI Agents" \
    --format "Hot Take" \
    --why "Why this worked — 1-2 sentences" \
    --engagement 1200 \
    --hook "Contrarian claim" \
    [--tier "⚡ High (1K–10K)"]  # auto-calculated if omitted
"""

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

NOTION_TOKEN = "ntn_I6090101509856iOb9JOeecrHaqzwG24r7PCjud0PE49iU"
DATABASE_ID = "31316aff930580f6a195ca179793eb0e"
NOTION_VERSION = "2022-06-28"
API_URL = "https://api.notion.com/v1/pages"
QUERY_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

VALID_NICHES = ["AI Consulting", "Crypto", "AI Agents", "Job Market", "Personal Brand", "x402"]
VALID_FORMATS = ["Hot Take", "Thread Opener", "Story", "List", "Question", "Contrarian", "Behind-the-scenes", "Data Drop", "Analogy"]
VALID_HOOKS = ["Curiosity gap", "Contrarian claim", "Personal story", "Provocative question", "Bold prediction", "Data surprise"]

# Map freeform hook descriptions to nearest valid category
HOOK_ALIAS_MAP = {
    "contrarian opener": "Contrarian claim",
    "contrarian cost claim": "Contrarian claim",
    "contrarian hot take": "Contrarian claim",
    "counter-narrative": "Contrarian claim",
    "counter-narrative / cost subversion": "Contrarian claim",
    "cost contrast": "Contrarian claim",
    "cost contrast / r.i.p. opener": "Contrarian claim",
    "bold prediction": "Bold prediction",
    "data surprise": "Data surprise",
    "curiosity gap": "Curiosity gap",
    "curiosity gap — what comes after solo agents?": "Curiosity gap",
    "personal story": "Personal story",
    "nostalgia + utility reveal": "Personal story",
    "nostalgia + tool reveal": "Personal story",
    "authority + specificity / news hook": "Bold prediction",
    "surprising fact": "Data surprise",
    "disaster/warning": "Curiosity gap",
    "provocative question": "Provocative question",
    "absurd visual + insane opener": "Curiosity gap",
    "unexpected output format / shows don't tell": "Curiosity gap",
    "celebrity name-drop + breaking": "Bold prediction",
}


def auto_tier(engagement: int) -> str:
    if engagement >= 10000:
        return "🔥 Mega (10K+)"
    elif engagement >= 1000:
        return "⚡ High (1K–10K)"
    else:
        return "✅ Solid (100–1K)"


def normalize_hook(hook: str) -> str:
    """Map freeform hook descriptions to valid VALID_HOOKS categories."""
    if hook in VALID_HOOKS:
        return hook
    lower = hook.lower().strip()
    if lower in HOOK_ALIAS_MAP:
        return HOOK_ALIAS_MAP[lower]
    # Partial match fallback
    for alias, canonical in HOOK_ALIAS_MAP.items():
        if alias in lower or lower in alias:
            return canonical
    # Last resort: check if it contains a valid hook keyword
    for valid in VALID_HOOKS:
        if valid.lower() in lower:
            return valid
    # Default to Curiosity gap rather than storing raw text
    print(f"⚠️  Hook '{hook}' not recognized — defaulting to 'Curiosity gap'")
    return "Curiosity gap"


def fetch_existing_texts(limit=100) -> list[str]:
    """Fetch existing post texts (first 120 chars, lowercased) for dedup check."""
    existing = []
    payload = json.dumps({
        "page_size": limit,
        "sorts": [{"property": "Engagement", "direction": "descending"}]
    }).encode("utf-8")

    req = urllib.request.Request(
        QUERY_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            results = json.loads(resp.read().decode()).get("results", [])
            for page in results:
                title_parts = page.get("properties", {}).get("Post Text", {}).get("title", [])
                text = "".join(t.get("plain_text", "") for t in title_parts)
                existing.append(text[:120].lower().strip())
    except Exception as e:
        print(f"⚠️  Could not fetch existing posts for dedup: {e}")
    return existing


def is_duplicate(new_text: str, existing_texts: list[str], threshold: int = 80) -> bool:
    """Check if new_text's first `threshold` chars match any existing entry."""
    new_prefix = new_text[:threshold].lower().strip()
    for existing in existing_texts:
        if existing[:threshold] == new_prefix:
            return True
    return False


def push_to_notion(args) -> dict:
    tier = args.tier if args.tier else auto_tier(args.engagement)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Normalize hook to valid category
    normalized_hook = normalize_hook(args.hook)
    if normalized_hook != args.hook:
        print(f"ℹ️  Hook normalized: '{args.hook}' → '{normalized_hook}'")

    # Validate niches
    niches = [n.strip() for n in args.niche.split(",")]
    for n in niches:
        if n not in VALID_NICHES:
            print(f"⚠️  Warning: '{n}' not a recognized niche. Valid: {VALID_NICHES}")

    # Deduplication check
    existing_texts = fetch_existing_texts(limit=100)
    if is_duplicate(args.text, existing_texts, threshold=80):
        print(f"⏭️  SKIPPED (duplicate): First 80 chars match an existing entry.")
        print(f"   Text: {args.text[:80]}...")
        return {"success": False, "skipped": True, "reason": "duplicate"}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Post Text": {
                "title": [{"text": {"content": args.text[:2000]}}]
            },
            "Author Handle": {
                "rich_text": [{"text": {"content": args.author}}]
            },
            "URL": {
                "url": args.url
            },
            "Niche": {
                "multi_select": [{"name": n} for n in niches]
            },
            "Format": {
                "select": {"name": args.format}
            },
            "Why It Works": {
                "rich_text": [{"text": {"content": args.why}}]
            },
            "Engagement": {
                "number": args.engagement
            },
            "Engagement Tier": {
                "select": {"name": tier}
            },
            "Hook Type": {
                "select": {"name": normalized_hook}
            },
            "Date Captured": {
                "date": {"start": today}
            },
            "Used As Reference": {
                "checkbox": False
            }
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            page_id = result.get("id", "unknown")
            print(f"✅ Pushed to Notion: {args.author} | {args.format} | {normalized_hook} | {tier} | page_id={page_id}")
            return {"success": True, "page_id": page_id}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ Notion API error {e.code}: {body}")
        return {"success": False, "error": body}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Push a viral post to Notion Swipe File")
    parser.add_argument("--text", required=True, help="Full post text")
    parser.add_argument("--author", required=True, help="@handle of author")
    parser.add_argument("--url", required=True, help="X post URL")
    parser.add_argument("--niche", required=True, help="Niche(s), comma-separated")
    parser.add_argument("--format", required=True, help="Post format")
    parser.add_argument("--why", required=True, help="Why this post worked (1-2 sentences)")
    parser.add_argument("--engagement", required=True, type=int, help="Total engagement count")
    parser.add_argument("--hook", required=True, help="Hook type")
    parser.add_argument("--tier", help="Engagement tier (auto-calculated if omitted)")
    args = parser.parse_args()
    push_to_notion(args)


if __name__ == "__main__":
    main()
