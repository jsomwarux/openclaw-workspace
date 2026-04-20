#!/usr/bin/env python3
"""
vibe-post.py — Posts the next queued TikTok slideshow for a given product.

Called by each product's posting cron:
  python3 vibe-post.py --product vista
  python3 vibe-post.py --product nash-satoshi

Logic:
1. Read queue.jsonl — find the oldest approved+unposted TikTok entry for this product
2. Parse slide texts and hook from the queue entry
3. Call reelfarm-create-slideshow.py with correct args
4. Mark queue entry as posted
5. Log to performance-log.jsonl
6. Notify JT via Telegram with post result
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

# ── env loader ────────────────────────────────────────────────────────────────
def load_env():
    env_path = os.path.expanduser("~/.config/env/global.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
QUEUE_PATH = os.path.join(WORKSPACE, "agents/vibe-marketing/queue.jsonl")
PERF_LOG = os.path.join(WORKSPACE, "agents/vibe-marketing/performance-log.jsonl")
REGISTRY = os.path.join(WORKSPACE, "agents/vibe-marketing/product-registry.json")
SCRIPT = os.path.join(WORKSPACE, "scripts/reelfarm-create-slideshow.py")


def parse_slides_from_content(content: str) -> tuple:
    """
    Parse queue entry content into (hook_text, slides_list).
    Handles all three formats:
      Format A (TEXT OVERLAY):  'SLIDE 1 (hook — photo.jpg):\nTEXT OVERLAY: [text]'
      Format B (direct colon):  'SLIDE 1: [text]\nSLIDE 2: [text]'  (no TEXT OVERLAY prefix)
      Format C (LAST SLIDE):    'LAST SLIDE TEXT OVERLAY: [text]'

    Returns: (hook_text, [{"text": "...", "is_screenshot": bool, "is_last": bool}, ...])
    Raises ValueError if no text can be extracted — NO silent fallbacks.
    """
    import re
    slides = []

    # Split on slide headers (SLIDE N or LAST SLIDE)
    slide_blocks = re.split(r'(?:^|\n)(?=(?:SLIDE \d+|LAST SLIDE))', content)

    for block in slide_blocks:
        block = block.strip()
        if not block:
            continue

        header_line = block.split("\n")[0].lower()
        is_screenshot = "app screenshot" in header_line or (
            "screenshot" in header_line and "app" in header_line
        )
        is_last = block.upper().startswith("LAST SLIDE")

        # Try each extraction strategy in order
        text = ""
        block_lines = block.split("\n")

        # Strategy 1: TEXT OVERLAY:, TEXT:, LABEL: anywhere in block (including same line as SLIDE N)
        combined = " ".join(block_lines)
        for prefix in ["TEXT OVERLAY:", "TEXT:", "LABEL:"]:
            idx = combined.find(prefix)
            if idx != -1:
                extracted = combined[idx + len(prefix):].strip()
                # Clean up any残留 text before the prefix (e.g. "SLIDE 1 TEXT OVERLAY:" part)
                if extracted and not extracted[0].isupper():
                    extracted = extracted[0].upper() + extracted[1:]
                if extracted:
                    text = extracted
                    break

        # Strategy 2: direct colon format 'SLIDE N: text' (no TEXT OVERLAY)
        if not text:
            first = block_lines[0]
            m = re.match(r'^(?:SLIDE \d+|LAST SLIDE)\s*:\s*(.+)', first.strip())
            if m:
                text = m.group(1).strip()

        if not text:
            print(f"[parse_slides_from_content] WARNING: could not extract text from block: {block[:80]}")
            continue

        slides.append({"text": text, "is_screenshot": is_screenshot, "is_last": is_last})

    if not slides:
        print("[parse_slides_from_content] ERROR: no slides could be extracted!")
        print(f"  Content preview: {content[:300]}")
        raise ValueError("parse_slides_from_content: failed to extract any slides — content format not recognized")

    hook = slides[0]["text"]
    slide_list = slides[1:]
    return hook, slide_list


def resolve_photo_urls(product: str, slide_list: list) -> list:
    """
    Build the full ordered photo URL list for a slideshow:
      - Slot 0 (hook):       lifestyle photo from library
      - Middle screenshot slots: screenshot URLs from library screenshots section
      - Middle non-screenshot slots: lifestyle photo
      - Last slot (CTA):    lifestyle photo from library

    Returns a list of public URLs in slide order (hook included as index 0).
    Does NOT mark photos as used — that happens in reelfarm-create-slideshow.py
    when --photo-urls is NOT used. When --photo-urls IS used, we skip library
    selection there and instead mark usage here via a separate call.
    """
    import json
    from datetime import date, timedelta

    library_path = os.path.join(
        WORKSPACE, "agents", "vibe-marketing", "real-photos", product, "library.json"
    )
    if not os.path.exists(library_path):
        return []

    with open(library_path) as f:
        library = json.load(f)

    # --- Screenshot URLs ---
    screenshots = library.get("screenshots", {}).get("files", [])
    screenshot_urls = [s["public_url"] for s in screenshots if s.get("public_url")]
    screenshot_idx = 0  # cycling index through available screenshots

    # --- Lifestyle photo selection ---
    # Count how many lifestyle photo slots we need
    # Slot 0 (hook) + each non-screenshot middle slide + last slot (CTA)
    lifestyle_slots_needed = 1  # hook
    for s in slide_list:
        if not s.get("is_screenshot") and not s.get("is_last"):
            lifestyle_slots_needed += 1
    lifestyle_slots_needed += 1  # CTA (last slide always lifestyle)

    today = date.today()
    rotation_window = library.get("rotation_window_weeks", 6)

    available = []
    for photo in library["photos"]:
        if not photo.get("public_url"):
            continue
        if photo["last_used_week"] is None:
            available.append(photo)
        else:
            last_used = date.fromisoformat(photo["last_used_week"])
            cutoff = today - timedelta(weeks=rotation_window)
            if last_used <= cutoff:
                available.append(photo)

    available.sort(key=lambda p: (
        0 if p["last_used_week"] is None else 1,
        p.get("last_used_week", ""),
        p["use_count"]
    ))

    lifestyle_urls = [p["public_url"] for p in available[:lifestyle_slots_needed]]
    lifestyle_idx = 0

    def next_lifestyle():
        nonlocal lifestyle_idx
        if lifestyle_urls:
            url = lifestyle_urls[lifestyle_idx % len(lifestyle_urls)]
            lifestyle_idx += 1
            return url
        return ""

    def next_screenshot():
        nonlocal screenshot_idx
        if screenshot_urls:
            url = screenshot_urls[screenshot_idx % len(screenshot_urls)]
            screenshot_idx += 1
            return url
        # Fallback: use a lifestyle photo if no screenshots available
        print(f"  WARNING: No screenshots in R2 for {product} — using lifestyle photo for screenshot slot",
              file=sys.stderr)
        return next_lifestyle()

    # Build ordered URL list
    photo_urls = [next_lifestyle()]  # hook slide always lifestyle
    for slide in slide_list:
        if slide.get("is_last"):
            photo_urls.append(next_lifestyle())  # CTA always lifestyle
        elif slide.get("is_screenshot"):
            photo_urls.append(next_screenshot())
        else:
            photo_urls.append(next_lifestyle())

    # If last slide wasn't explicitly marked is_last, add CTA lifestyle photo
    if slide_list and not slide_list[-1].get("is_last"):
        photo_urls.append(next_lifestyle())

    return [u for u in photo_urls if u]  # filter empties


def build_caption(entry: dict) -> tuple[str, str]:
    """Build caption (≤89 chars, no hashtags) and description (hashtags) from queue entry."""
    hashtags = entry.get("hashtags", "")
    
    # Try to extract a short caption from the hook text
    hook = ""
    content = entry.get("content", "")
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    for line in lines:
        for prefix in ["TEXT OVERLAY:", "TEXT:", "LABEL:"]:
            if line.startswith(prefix):
                hook = line[len(prefix):].strip()
                break
        if hook:
            break

    # Truncate to 89 chars
    if len(hook) > 89:
        hook = hook[:86] + "..."
    
    caption = hook if hook else "watch this"
    description = hashtags if hashtags else ""
    
    return caption, description


def _hook_key(entry: dict) -> str:
    """Normalize hook text to a comparable key for duplicate detection.


    Extracts TEXT OVERLAY / TEXT: content, lowercases, strips punctuation
    and apostrophe variations so two queue entries with the same core hook
    normalize to the same key regardless of formatting differences.
    """
    import re
    content_text = entry.get("content", "")
    hook = ""

    for line in content_text.split("\n"):
        line = line.strip()
        for prefix in ["TEXT OVERLAY:", "TEXT:"]:
            if prefix in line:
                idx = line.index(prefix)
                candidate = line[idx + len(prefix):].strip()
                if candidate:
                    hook = candidate
                    break
        if hook:
            break

    if not hook:
        skip_prefixes = ("SLIDE", "CAPTION", "HASHTAG", "FORMAT", "SOURCE",
                         "SCREENSHOT", "LABEL", "NOTE", "TITLE")
        for line in content_text.split("\n"):
            line = line.strip()
            if line and not line.startswith(skip_prefixes):
                hook = line
                break

    key = hook.lower()
    key = key.replace("\u2019", "'").replace("\u2018", "'").replace("\u0027", "'")
    key = key.replace("\u2014", " ").replace("\u2013", " ")
    key = re.sub(r"[^a-z0-9 ' \s]", "", key)
    key = re.sub(r"\s+", " ", key).strip()
    return key


def _last_hook_key(product: str) -> str:
    """Get the hook key of the most recent TikTok post for this product.

    Reads the LAST line in performance-log.jsonl for this product+platform
    and returns its normalized hook key. Returns '' if nothing posted yet.
    """
    import re
    if not os.path.exists(PERF_LOG):
        return ""
    last_entry = None
    try:
        with open(PERF_LOG) as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    e = json.loads(stripped)
                    if e.get("product_slug") == product and e.get("platform") == "tiktok":
                        last_entry = e
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return ""
    if not last_entry:
        return ""
    queue_id = last_entry.get("id", "")
    if not queue_id:
        return ""
    try:
        with open(QUEUE_PATH) as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    e = json.loads(stripped)
                    if e.get("id") == queue_id:
                        return _hook_key(e)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return ""


def mark_posted(entry_id: str, slideshow_id: int, video_id: str):
    """Update the queue entry to mark it as posted."""
    if not os.path.exists(QUEUE_PATH):
        return
    
    lines = []
    with open(QUEUE_PATH) as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                lines.append(line)
                continue
            try:
                entry = json.loads(stripped)
                if entry.get("id") == entry_id:
                    entry["posted"] = True
                    entry["posted_date"] = datetime.now().strftime("%Y-%m-%d")
                    entry["slideshow_id"] = slideshow_id
                    entry["video_id"] = video_id
                    lines.append(json.dumps(entry) + "\n")
                else:
                    lines.append(line)
            except json.JSONDecodeError:
                lines.append(line)
    
    with open(QUEUE_PATH, "w") as f:
        f.writelines(lines)


def log_performance(entry: dict, slideshow_id: int, video_id: str):
    """Append to performance-log.jsonl for future analytics."""
    perf_entry = {
        "id": entry.get("id"),
        "product_slug": entry.get("product_slug"),
        "platform": "tiktok",
        "week_of": entry.get("week_of"),
        "posted_date": datetime.now().strftime("%Y-%m-%d"),
        "format_type": entry.get("format", "slideshow"),
        "hook_style": "lifestyle_overlay",
        "slideshow_id": slideshow_id,
        "video_id": video_id,
        "views": 0,
        "likes": 0,
        "comments": 0,
        "score": "pending",
        "icp_variant": entry.get("icp_variant", ""),
    }
    with open(PERF_LOG, "a") as f:
        f.write(json.dumps(perf_entry) + "\n")


def notify_jt(product: str, result: dict, entry_id: str, skipped: bool, reason: str = ""):
    """Send Telegram notification about the post result."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = "6608544825"
    
    if not token:
        print("WARNING: TELEGRAM_BOT_TOKEN not set — skipping notification")
        return
    
    if skipped:
        msg = f"📭 Vibe Post ({product}): No queued content — {reason}. Generate cron runs Monday 4:45AM."
    elif result.get("tiktok_post_status") in ("processing", "published"):
        msg = (
            f"✅ TikTok posted — {product}\n"
            f"video_id: {result.get('video_id')}\n"
            f"Photos: {', '.join(result.get('photos_used', []))}\n"
            f"Queue entry: {entry_id}"
        )
    else:
        msg = (
            f"⚠️ TikTok post failed — {product}\n"
            f"Status: {result.get('tiktok_post_status')}\n"
            f"Queue entry: {entry_id}"
        )
    
    try:
        import urllib.request
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": msg}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"WARNING: Telegram notify failed: {e}")


def _posted_ids_from_perf_log() -> set:
    """Get all entry IDs that have already been posted (from performance log)."""
    posted = set()
    if not os.path.exists(PERF_LOG):
        return posted
    try:
        with open(PERF_LOG) as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    e = json.loads(stripped)
                    if e.get('id'):
                        posted.add(e['id'])
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return posted


def find_next_entry(product: str):
    """
    Find the oldest approved+unposted TikTok entry for the given product.
    Reads queue.jsonl in order and returns the first match.
    Skips entries already in the performance log (already posted — across ALL products).
    """
    posted_ids = _posted_ids_from_perf_log()
    last_hook  = _last_hook_key(product)

    with open(QUEUE_PATH) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError:
                continue  # skip corrupted lines

            # Must match product and TikTok platform
            if entry.get("product_slug") != product:
                continue
            if entry.get("platform") != "tiktok":
                continue

            # Must be approved and not yet posted
            if entry.get("status") != "approved":
                continue
            if entry.get("posted"):
                continue

            # Duplicate guard: skip if already in performance log (already posted)
            if entry['id'] in posted_ids:
                print(f"[find_next_entry] Skipping {entry['id']} — already in performance log (already posted)")
                continue

            # Hook-diversity guard: skip if same hook as last post for this product
            hook_key = _hook_key(entry)
            if last_hook and hook_key == last_hook:
                print(f"[find_next_entry] Skipping duplicate hook: {hook_key[:40]}...")
                continue

            return entry

    return None


def main():
    parser = argparse.ArgumentParser(description="Post next queued TikTok slideshow for a product")
    parser.add_argument("--product", required=True, choices=["vista", "nash-satoshi"],
                        help="Product slug to post for")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build slideshow but skip TikTok publish")
    args = parser.parse_args()

    product = args.product
    print(f"[vibe-post] Running for product: {product}")

    # Find next queue entry
    entry = find_next_entry(product)
    if not entry:
        print(f"[vibe-post] No queued TikTok content for {product} — skipping.")
        notify_jt(product, {}, "", skipped=True, reason="no queued content")
        sys.exit(0)

    print(f"[vibe-post] Found entry: {entry['id']}")
    
    # ── PRODUCT CONTENT VERIFICATION ──────────────────────────────────────
    # CRITICAL: verify content actually matches the product before any API call
    content_lower = entry.get('content', '').lower()
    entry_product = entry.get('product_slug', '')
    
    if entry_product != product:
        print(f"[vibe-post] 🚨 FATAL: entry product_slug='{entry_product}' != requested product='{product}'")
        print(f"[vibe-post] 🚨 Stopping — cross-product contamination detected!")
        print(f"[vibe-post] 🚨 Entry: {entry['id']}")
        sys.exit(1)
    
    # Keyword-based content validation
    crypto_keywords = ['crypto', 'coin', 'token', 'staking', 'defi', 'blockchain', 
                      'bitcoin', 'eth ', 'solana', 'nft', 'trading', 'traders',
                      'game theory', 'nash', 'satoshi', 'market cap', 'liquidity',
                      'bullish', 'bearish', 'hodl', 'whale', 'altcoin', 'meme coin']
    movie_keywords  = ['movie', 'film', 'imdb', 'letterboxd', 'rotten tomatoes',
                      'rating', 'watched', 'genre', 'director', 'scene', 'cinema',
                      'screenplay', 'score', 'trailer', 'streaming', 'netflix', 'hulu']
    
    crypto_hits = sum(1 for kw in crypto_keywords if kw in content_lower)
    movie_hits  = sum(1 for kw in movie_keywords  if kw in content_lower)
    
    if product == 'nash-satoshi' and movie_hits > 2 and crypto_hits == 0:
        print(f"[vibe-post] 🚨 FATAL: Nash content has movie keywords ({movie_hits}) but no crypto keywords!")
        print(f"[vibe-post] 🚨 Stopping — content mismatch (Vista copy in Nash post?)")
        print(f"[vibe-post] 🚨 Entry: {entry['id']}")
        sys.exit(1)
    
    if product == 'vista' and crypto_hits > 2 and movie_hits == 0:
        print(f"[vibe-post] 🚨 FATAL: Vista content has crypto keywords ({crypto_hits}) but no movie keywords!")
        print(f"[vibe-post] 🚨 Stopping — content mismatch (Nash copy in Vista post?)")
        print(f"[vibe-post] 🚨 Entry: {entry['id']}")
        sys.exit(1)
    
    print(f"[vibe-post] ✅ Content verified: {crypto_hits} crypto hints, {movie_hits} movie hints")
    # ── END PRODUCT VERIFICATION ─────────────────────────────────────────
    
    # Parse content into hook + slides
    hook, slides = parse_slides_from_content(entry.get("content", ""))
    caption, description = build_caption(entry)
    
    print(f"[vibe-post] Hook: {hook[:60]}...")
    print(f"[vibe-post] Slides: {len(slides)}")
    print(f"[vibe-post] Caption: {caption}")
    sound_rec = entry.get('sound_rec', '')
    if sound_rec:
        print(f"[vibe-post] 🎵 SOUND: {sound_rec}")

    # Resolve photo URLs (lifestyle + screenshots in correct slot order)
    photo_urls = resolve_photo_urls(product, slides)
    print(f"[vibe-post] Resolved {len(photo_urls)} photo URLs")
    for i, url in enumerate(photo_urls):
        slot = "hook" if i == 0 else ("cta" if i == len(photo_urls) - 1 else f"slide-{i+1}")
        url_label = "[SCREENSHOT]" if "/screenshots/" in url else "[lifestyle]"
        print(f"  Slot {slot}: {url_label} {url.split('/')[-1]}")

    # Strip is_screenshot/is_last keys before passing to slideshow script
    clean_slides = [{"text": s["text"]} for s in slides]

    # Build command
    cmd = [
        sys.executable, SCRIPT,
        "--product", product,
        "--hook", hook,
        "--slides", json.dumps(clean_slides),
        "--photo-urls", json.dumps(photo_urls),
        "--caption", caption,
    ]
    if description:
        cmd += ["--description", description]
    if args.dry_run:
        cmd += ["--skip-publish"]

    print(f"[vibe-post] Calling reelfarm-create-slideshow.py...")
    
    result_json = {}
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(f"STDERR: {proc.stderr}", file=sys.stderr)
        
        # Parse JSON result from stdout
        result_json = {}
        for line in proc.stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    result_json = json.loads(line)
                    break
                except json.JSONDecodeError:
                    pass
        
        slideshow_id = result_json.get("slideshow_id", 0)
        video_id = result_json.get("video_id", "")
        
        post_status = str(result_json.get("tiktok_post_status") or "")
        # NOTE: never call mark_posted() in dry-run mode — dry run is preview only
        if post_status in ("processing", "published", "skipped"):
            if not args.dry_run:
                mark_posted(entry["id"], slideshow_id, video_id)
                log_performance(entry, slideshow_id, video_id)
            label = "dry-run" if args.dry_run else "live"
            print(f"[vibe-post] ✅ Done ({label}). slideshow_id={slideshow_id}, video_id={video_id}")
        else:
            print(f"[vibe-post] ⚠️ Post status: {post_status}")
        
    except subprocess.TimeoutExpired:
        print("[vibe-post] ERROR: Script timed out after 300s")
        result_json = {"tiktok_post_status": "timeout"}
    except Exception as e:
        print(f"[vibe-post] ERROR: {e}")
        result_json = {"tiktok_post_status": "error", "error": str(e)}

    notify_jt(product, result_json, entry["id"], skipped=False)


if __name__ == "__main__":
    main()
