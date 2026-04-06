#!/usr/bin/env python3
"""
reelfarm-create-slideshow.py
------------------------------
Creates a TikTok slideshow via Reel.farm API and publishes it.
Called by Eve from the vibe-marketing cron for each product per week.

Usage:
  python3 scripts/reelfarm-create-slideshow.py \
    --product vista \
    --hook "hook text for slide 1" \
    --slides '[{"text": "slide 2 text"}, {"text": "slide 3 text"}]' \
    --tiktok-account-id "tt_abc123" \
    --caption "TikTok caption (max 89 chars)" \
    --description "#hashtags"

Environment variables (from ~/.config/env/global.env):
  REELFARM_API_KEY - Reel.farm API key

Outputs JSON to stdout with slideshow_id, video_id, tiktok_post_status, photos_used.
"""

import json
import os
import sys
import argparse
import time
from datetime import date, timedelta

try:
    import requests
except ImportError:
    print("ERROR: requests is required. Install with: pip install requests")
    sys.exit(1)

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHOTOS_BASE = os.path.join(WORKSPACE, "agents", "vibe-marketing", "real-photos")
REELFARM_BASE = "https://reel.farm/api/v1"

PRODUCT_CONFIG = {
    "vista": {
        "library_path": os.path.join(PHOTOS_BASE, "vista", "library.json"),
        "photos_dir": os.path.join(PHOTOS_BASE, "vista"),
        "font": "TikTokDisplay-Bold",
        "text_style": "outline",
        "aspect_ratio": "4:5",
    },
    "nash-satoshi": {
        "library_path": os.path.join(PHOTOS_BASE, "nash-satoshi", "library.json"),
        "photos_dir": os.path.join(PHOTOS_BASE, "nash-satoshi"),
        "font": "TikTokDisplay-Bold",
        "text_style": "outline",
        "aspect_ratio": "4:5",
    },
}

POLL_INTERVAL = 5  # seconds
POLL_TIMEOUT = 120  # seconds


def load_env():
    """Load required environment variables, sourcing global.env if needed."""
    api_key = os.environ.get("REELFARM_API_KEY")
    if not api_key:
        # Auto-source global.env
        env_path = os.path.expanduser("~/.config/env/global.env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip())
        api_key = os.environ.get("REELFARM_API_KEY")
    if not api_key:
        print("ERROR: REELFARM_API_KEY not found in environment or ~/.config/env/global.env")
        sys.exit(1)
    return api_key


def get_headers(api_key):
    """Return auth headers for Reel.farm API."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def load_library(product):
    """Load the photo library for a product."""
    config = PRODUCT_CONFIG[product]
    with open(config["library_path"], "r") as f:
        return json.load(f)


def save_library(product, library):
    """Save the photo library for a product."""
    config = PRODUCT_CONFIG[product]
    with open(config["library_path"], "w") as f:
        json.dump(library, f, indent=2)


def select_photos(library, count):
    """
    Select N unused photos that have public_url set.
    Uses same rotation logic as the selector scripts:
    prefer never-used, then least recently used.
    """
    today = date.today()
    rotation_window = library.get("rotation_window_weeks", 6)

    available = []
    for photo in library["photos"]:
        # Must have a public_url
        if not photo.get("public_url"):
            continue

        # Check rotation window
        if photo["last_used_week"] is None:
            available.append(photo)
        else:
            last_used = date.fromisoformat(photo["last_used_week"])
            cutoff = today - timedelta(weeks=rotation_window)
            if last_used <= cutoff:
                available.append(photo)

    # Sort: never-used first, then by least recently used, then by use_count
    def sort_key(p):
        if p["last_used_week"] is None:
            return (0, 0, p["use_count"])
        return (1, p["last_used_week"], p["use_count"])

    available.sort(key=sort_key)

    if len(available) < count:
        print(
            f"WARNING: Only {len(available)} photos available with public_url "
            f"(needed {count}). Skipping photos without public_url.",
            file=sys.stderr,
        )

    return available[:count]


def mark_photos_used(library, photo_ids, week_date):
    """Mark selected photos as used in the library."""
    for photo in library["photos"]:
        if photo["id"] in photo_ids:
            photo["last_used_week"] = week_date
            photo["use_count"] += 1
    library["last_updated"] = date.today().isoformat()


def build_slides(hook_text, slide_texts, photo_urls, product):
    """Build the slides array for the Reel.farm API."""
    config = PRODUCT_CONFIG[product]
    slides = []

    # Slide 1: hook photo + hook text
    if photo_urls:
        slides.append({
            "image_url": photo_urls[0],
            "text_items": [
                {
                    "text": hook_text,
                    "font_size": "extra_large",
                    "text_style": config["text_style"],
                    "font": config["font"],
                }
            ],
        })

    # Middle slides: remaining photos + slide texts
    for i, slide_data in enumerate(slide_texts):
        # Use photo at index i+1 (offset by 1 for hook photo)
        photo_idx = i + 1
        if photo_idx < len(photo_urls):
            image_url = photo_urls[photo_idx]
        else:
            # Reuse last photo if we run out
            image_url = photo_urls[-1] if photo_urls else None

        if image_url is None:
            print(
                f"WARNING: No photo available for slide {i + 2}, skipping",
                file=sys.stderr,
            )
            continue

        text = slide_data.get("text", "")
        slide = {"image_url": image_url}
        if text:
            slide["text_items"] = [
                {
                    "text": text,
                    "font_size": "extra_large",
                    "text_style": config["text_style"],
                    "font": config["font"],
                }
            ]
        slides.append(slide)

    return slides


def create_slideshow(api_key, slides, product, slideshow_type):
    """Call POST /slideshows/create and return the response."""
    config = PRODUCT_CONFIG[product]
    payload = {
        "slides": slides,
        "aspect_ratio": config["aspect_ratio"],
        "text_position": "center",
        "export_as_video": True,
        "duration": 4,
        "is_bg_overlay_on": True,
        "background_opacity": 30,
        'type': slideshow_type,  # Added type parameter
    }

    resp = requests.post(
        f"{REELFARM_BASE}/slideshows/create",
        headers=get_headers(api_key),
        json=payload,
        timeout=30,
    )

    if resp.status_code not in (200, 201):
        print(f"ERROR: Slideshow creation failed (HTTP {resp.status_code}): {resp.text}")
        sys.exit(1)

    return resp.json()


def poll_slideshow_status(api_key, slideshow_id):
    """Poll GET /slideshows/{id}/status until completed, then fetch video_id."""
    elapsed = 0
    while elapsed < POLL_TIMEOUT:
        resp = requests.get(
            f"{REELFARM_BASE}/slideshows/{slideshow_id}/status",
            headers=get_headers(api_key),
            timeout=15,
        )

        if resp.status_code != 200:
            print(
                f"ERROR: Status check failed (HTTP {resp.status_code}): {resp.text}",
                file=sys.stderr,
            )
            return None

        data = resp.json()
        status = data.get("status", "unknown")

        if status == "completed":
            # Fetch video_id from the videos list (most recent finished video = ours)
            vresp = requests.get(
                f"{REELFARM_BASE}/videos",
                headers=get_headers(api_key),
                timeout=15,
            )
            if vresp.status_code == 200:
                videos = vresp.json().get("videos", [])
                finished = [v for v in videos if v.get("finished") and not v.get("failed")]
                if finished:
                    data["video_id"] = finished[0]["video_id"]
                    print(f"  Resolved video_id: {data['video_id']}", file=sys.stderr)
            return data
        elif status == "failed":
            print(f"ERROR: Slideshow rendering failed: {data}", file=sys.stderr)
            return None

        print(
            f"  Rendering... status={status} ({elapsed}s/{POLL_TIMEOUT}s)",
            file=sys.stderr,
        )
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    print(f"ERROR: Slideshow rendering timed out after {POLL_TIMEOUT}s", file=sys.stderr)
    return None


def publish_to_tiktok(api_key, video_id, tiktok_account_id, caption, description):
    """Call POST /tiktok/publish to post the video."""
    payload = {
        "video_id": video_id,
        "tiktok_account_id": tiktok_account_id,
        "upload_type": "slides",
        "caption": caption[:89],  # enforce max 89 chars
        "description": description[:4000],  # enforce max 4000 chars
        "post_mode": "DIRECT_POST",
        "visibility": "PUBLIC_TO_EVERYONE",
        "auto_music": True,
    }

    resp = requests.post(
        f"{REELFARM_BASE}/tiktok/publish",
        headers=get_headers(api_key),
        json=payload,
        timeout=30,
    )

    if resp.status_code not in (200, 202):
        print(f"ERROR: TikTok publish failed (HTTP {resp.status_code}): {resp.text}")
        return {"status": "failed", "error": resp.text}

    data = resp.json()
    # 202 = processing (accepted by TikTok) — treat as success
    if resp.status_code == 202:
        data["status"] = "processing"
    return data


def get_current_week_monday():
    """Get the Monday of the current week as ISO date string."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def main():
    parser = argparse.ArgumentParser(
        description="Create a TikTok slideshow via Reel.farm and publish it"
    )
    parser.add_argument(
        "--product",
        required=True,
        choices=["vista", "nash-satoshi"],
        help="Which product's photos to use",
    )
    parser.add_argument(
        "--hook",
        required=True,
        help="Hook text for slide 1",
    )
    parser.add_argument(
        "--slides",
        required=True,
        help='JSON array of slide objects: [{"text": "slide 2 text"}, ...]',
    )
    parser.add_argument(
        "--tiktok-account-id",
        default=None,
        help="Reel.farm TikTok account ID (auto-loaded from product registry if omitted)",
    )
    parser.add_argument(
        "--caption",
        required=True,
        help="TikTok caption (max 89 chars)",
    )
    parser.add_argument(
        "--description",
        default="",
        help="TikTok description/hashtags (max 4000 chars)",
    )
    parser.add_argument(
        "--photo-urls",
        default=None,
        help="JSON array of pre-resolved photo URLs in slide order (hook first). "
             "When provided, skips library selection entirely.",
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Create slideshow but do not publish to TikTok",
    )
    args = parser.parse_args()

    # Parse slides JSON
    try:
        slide_texts = json.loads(args.slides)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid --slides JSON: {e}")
        sys.exit(1)

    api_key = load_env()

    # Load TikTok account ID from product registry if not provided
    tiktok_account_id = args.tiktok_account_id
    if not tiktok_account_id:
        registry_path = os.path.join(WORKSPACE, "agents", "vibe-marketing", "product-registry.json")
        with open(registry_path) as f:
            registry = json.load(f)
        for p in registry["products"]:
            if p["slug"] == args.product:
                tiktok_account_id = p.get("tiktok_account_id")
                break
        if not tiktok_account_id:
            print(f"ERROR: No tiktok_account_id found for product '{args.product}' in product-registry.json")
            sys.exit(1)

    # Photo URL resolution: use pre-resolved URLs from vibe-post.py if provided,
    # otherwise fall back to library selection (lifestyle-only, no screenshots)
    if args.photo_urls:
        photo_urls = json.loads(args.photo_urls)
        photo_ids = []  # no library mutation needed; vibe-post.py handles usage tracking
        print(f"Using {len(photo_urls)} pre-resolved photo URLs (hybrid mode)", file=sys.stderr)
        for i, url in enumerate(photo_urls):
            slot = "hook" if i == 0 else ("cta" if i == len(photo_urls) - 1 else f"slide-{i+1}")
            label = "[screenshot]" if "/screenshots/" in url else "[lifestyle]"
            print(f"  {slot}: {label} {url.split('/')[-1]}", file=sys.stderr)
    else:
        # Lifestyle-only fallback: select from library
        total_photos_needed = 1 + len(slide_texts)
        library = load_library(args.product)
        selected_photos = select_photos(library, total_photos_needed)

        if not selected_photos:
            print("ERROR: No photos available with public_url. Run reelfarm-upload-photos.py first.")
            sys.exit(1)

        photo_urls = [p["public_url"] for p in selected_photos]
        photo_ids = [p["id"] for p in selected_photos]

        print(f"Selected {len(selected_photos)} lifestyle photos for {args.product}", file=sys.stderr)
        for p in selected_photos:
            print(f"  {p['id']}: {p['file']}", file=sys.stderr)

    # Build slides
    slides = build_slides(args.hook, slide_texts, photo_urls, args.product)

    if not slides:
        print("ERROR: No slides could be built (no photos with public_url)")
        sys.exit(1)

    slideshow_type = "hybrid" if args.photo_urls else "lifestyle"
    print(f"Creating {slideshow_type} slideshow with {len(slides)} slides...", file=sys.stderr)

    # Create slideshow
    create_resp = create_slideshow(api_key, slides, args.product, slideshow_type)
    slideshow_id = create_resp.get("slideshow_id")

    if not slideshow_id:
        print(f"ERROR: No slideshow_id in response: {create_resp}")
        sys.exit(1)

    print(f"Slideshow created: {slideshow_id}", file=sys.stderr)

    # Poll for completion
    status_data = poll_slideshow_status(api_key, slideshow_id)

    if not status_data:
        # Output partial result even on failure
        result = {
            "slideshow_id": slideshow_id,
            "video_id": None,
            "tiktok_post_status": "slideshow_render_failed",
            "photos_used": photo_ids,
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    video_id = status_data.get("video_id")
    print(f"Slideshow ready. slideshow_id: {slideshow_id}, video_id: {video_id}", file=sys.stderr)

    # Publish to TikTok
    tiktok_result = {"status": "skipped"}
    if not args.skip_publish:
        if not video_id:
            print("ERROR: Could not resolve video_id — cannot publish", file=sys.stderr)
            tiktok_result = {"status": "failed", "error": "video_id not resolved"}
        else:
            print("Publishing to TikTok...", file=sys.stderr)
            tiktok_result = publish_to_tiktok(
                api_key, video_id, tiktok_account_id, args.caption, args.description
            )
        print(f"TikTok publish result: {tiktok_result}", file=sys.stderr)

    # Mark photos as used (only when library was loaded via fallback path)
    week_monday = get_current_week_monday()
    if 'library' in dir() and library is not None and photo_ids:
        mark_photos_used(library, photo_ids, week_monday)
        save_library(args.product, library)
        print(f"Marked {len(photo_ids)} photos as used for week {week_monday}", file=sys.stderr)
    else:
        print("Skipping mark_photos_used — hybrid mode (vibe-post.py tracks usage)", file=sys.stderr)

    # Output final result to stdout
    result = {
        "slideshow_id": slideshow_id,
        "video_id": tiktok_result.get("video_id"),
        "tiktok_post_status": tiktok_result.get("status", "unknown"),
        "photos_used": photo_ids,
        "product": args.product,
        "slide_count": len(slides),
        "week": week_monday,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
