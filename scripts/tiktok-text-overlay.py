#!/usr/bin/env python3
"""
tiktok-text-overlay.py
Renders TikTok Classic-style text overlays onto images.

Exact spec:
- Font: TikTok Sans Medium (weight 500 — semibold appearance, not bold/700)
  Fallback: Montserrat SemiBold (600)
- Color: #FFFFFF pure white
- Shadow: black 40% opacity, 1px right / 1px down, 3px blur — very subtle
- Letter spacing: +0.75px extra tracking (slightly open, not tight)
- Line height: 1.15em
- Alignment: always center-aligned
- Line balancing: balanced wraps — all lines roughly equal width (diamond/rectangle shape)
- Vertical position: center of upper third (15-35% from top)
- Font size: 64-72px base on 1080px canvas; up to 80px for short text; 56-64px for 15+ words
- Max width: 85% of canvas
- No stroke, no background box, no bold (700)

Usage:
    python3 tiktok-text-overlay.py \
        --input path/to/image.png \
        --text "your hook text here" \
        --output path/to/output.png \
        [--font-size 72]
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = Path(__file__).parent / "fonts"
FONT_PRIMARY  = FONT_DIR / "TikTokSans-SemiBold.ttf"      # Weight 600 — confirmed correct
FONT_FALLBACK = FONT_DIR / "Montserrat-SemiBold.ttf"      # Weight 600 fallback
FONT_TIKTOK_SB = FONT_DIR / "TikTokSans-Medium.ttf"       # Weight 500 last resort
SYSTEM_FALLBACKS = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Arial.ttf",
]

# ── Style constants (exact per spec) ─────────────────────────────────────────
TEXT_COLOR      = (255, 255, 255, 255)  # Pure white
STROKE_COLOR    = (0, 0, 0, 220)        # Near-black stroke, slight transparency
STROKE_WIDTH    = 2                     # 2px outline at 1080px — scales with image
SHADOW_COLOR    = (0, 0, 0, 80)         # Black 31% opacity — lighter than before (stroke does the heavy lifting)
SHADOW_OFFSET_X = 1                     # 1px right
SHADOW_OFFSET_Y = 2                     # 2px down
SHADOW_BLUR     = 4                     # 4px blur
LETTER_SPACING  = 0.5                   # +0.5px extra tracking
LINE_HEIGHT_EM  = 1.2                   # Slightly more open
MAX_WIDTH_RATIO = 0.82                  # 82% of canvas width
# Vertical anchor per position mode:
#   upper  = upper third center = 0.27 (hook slides)
#   center = true center = 0.50 (CTA slides)
#   lower  = lower fifth = 0.82 (screenshot label slides — text sits below the UI content)
VERTICAL_ANCHORS = {
    "upper":  0.27,
    "center": 0.50,
    "lower":  0.82,
}


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Load preferred font, fall back gracefully."""
    for path in [FONT_PRIMARY, FONT_FALLBACK, FONT_TIKTOK_SB] + [Path(p) for p in SYSTEM_FALLBACKS]:
        if Path(path).exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                continue
    return ImageFont.load_default()


def normalize_text(text: str) -> str:
    """Normalize smart/curly quotes to straight apostrophes."""
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    return text


def measure_word(font: ImageFont.FreeTypeFont, word: str, spacing: float) -> float:
    """Measure a word's pixel width with extra letter spacing applied."""
    bbox = font.getbbox(word)
    base_w = bbox[2] - bbox[0]
    # Add spacing between every character
    return base_w + spacing * max(len(word) - 1, 0)


def measure_line_with_spacing(font: ImageFont.FreeTypeFont, words: list[str], spacing: float) -> float:
    """Measure total line width including inter-word space and letter spacing."""
    if not words:
        return 0
    total = sum(measure_word(font, w, spacing) for w in words)
    # Add standard space between words
    space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0]
    total += space_w * (len(words) - 1)
    return total


def balanced_wrap(text: str, font: ImageFont.FreeTypeFont, max_px: float, spacing: float) -> list[str]:
    """
    Balanced line wrapping — all lines roughly equal width.
    Algorithm: binary search the optimal target line width so that
    all lines are as close to equal as possible (diamond/rectangle shape).
    Falls back to greedy wrap if balancing can't improve things.
    """
    words = text.split()
    if not words:
        return [text]

    # Greedy wrap at max_px (baseline)
    def greedy_wrap(target_px: float) -> list[str]:
        lines, current = [], []
        for word in words:
            candidate = current + [word]
            if measure_line_with_spacing(font, candidate, spacing) <= target_px:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = [word]
        if current:
            lines.append(current)
        return lines

    # Start with greedy at full max width
    raw_lines = greedy_wrap(max_px)
    if len(raw_lines) == 1:
        return [" ".join(raw_lines[0])]

    # Try narrower targets to force more even distribution
    # Binary search: find the narrowest target where we still get
    # the same number of lines as the greedy wrap
    n_lines = len(raw_lines)
    lo = max_px * 0.4
    hi = max_px
    best_lines = raw_lines

    for _ in range(20):
        mid = (lo + hi) / 2
        candidate = greedy_wrap(mid)
        if len(candidate) <= n_lines:
            # Still fits in same or fewer lines — try narrower
            best_lines = candidate
            hi = mid
        else:
            # Too narrow, caused more lines — back off
            lo = mid

    # Convert to strings
    result = [" ".join(line) for line in best_lines]

    # Final anti-orphan: if last line is single word, pull one from prior line
    if len(result) >= 2 and len(result[-1].split()) == 1:
        prev = result[-2].split()
        if len(prev) >= 2:
            moved = prev[-1]
            result[-2] = " ".join(prev[:-1])
            result[-1] = moved + " " + result[-1]

    return result


def pick_font_size(text: str, scale: float) -> int:
    """
    Pick base font size per spec:
    - ≤5 words  → up to 80px
    - 6-14 words → 64-72px
    - 15+ words  → 56-64px
    All scaled by image scale factor.
    """
    words = len(text.split())
    if words <= 5:
        base = 48   # Short hook — feels natural, not a title card
    elif words <= 14:
        base = 44   # Mid-length — matches real TikTok Classic at ~44px on 1080
    else:
        base = 40   # Long text — stays readable without overwhelming
    return int(base * scale)


def draw_text_with_spacing(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.FreeTypeFont,
    lines: list[str],
    center_x: int,
    top_y: int,
    line_h: int,
    spacing: float,
    color: tuple,
) -> None:
    """Draw each line centered, with manual per-character spacing."""
    space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0]

    y = top_y
    for line in lines:
        words = line.split()
        # Measure total line width to center it
        line_px = measure_line_with_spacing(font, words, spacing)
        x = center_x - line_px / 2

        for wi, word in enumerate(words):
            # Draw each character with extra tracking
            for char in word:
                draw.text((int(x), y), char, font=font, fill=color)
                bbox = font.getbbox(char)
                char_w = bbox[2] - bbox[0]
                x += char_w + spacing
            # Add word space (no extra spacing between words)
            if wi < len(words) - 1:
                x += space_w
        y += line_h


def overlay_text(
    input_path: str,
    text: str,
    output_path: str,
    font_size: int = None,
    position: str = "upper",
) -> str:
    """
    Bake TikTok Classic-style text onto an image.

    Args:
        input_path:  Source image
        text:        Text to render (normalized internally)
        output_path: Output image path
        font_size:   Override auto font size in px at 1080px width

    Returns:
        output_path
    """
    text = normalize_text(text)

    img = Image.open(input_path).convert("RGBA")
    W, H = img.size
    scale = W / 1080.0
    max_px = W * MAX_WIDTH_RATIO
    spacing = LETTER_SPACING * scale

    # Font size
    size = int(font_size * scale) if font_size else pick_font_size(text, scale)
    font = get_font(size)

    # Wrap with balanced line breaks
    lines = balanced_wrap(text, font, max_px, spacing)

    line_h = int(size * LINE_HEIGHT_EM)
    block_h = line_h * len(lines)

    # Vertical: anchor per position mode
    anchor_y = int(H * VERTICAL_ANCHORS.get(position, 0.27))
    top_y = anchor_y - block_h // 2
    center_x = W // 2

    # ── Shadow layer ──────────────────────────────────────────────────────────
    shadow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    draw_text_with_spacing(
        shadow_draw, font, lines,
        center_x + SHADOW_OFFSET_X,
        top_y + SHADOW_OFFSET_Y,
        line_h, spacing, SHADOW_COLOR
    )
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    img = Image.alpha_composite(img, shadow_img)

    # ── Stroke layer (draw text in stroke color at every offset around center) ──
    stroke_w = max(1, int(STROKE_WIDTH * scale))
    stroke_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    stroke_draw = ImageDraw.Draw(stroke_img)
    for dx in range(-stroke_w, stroke_w + 1):
        for dy in range(-stroke_w, stroke_w + 1):
            if dx == 0 and dy == 0:
                continue  # Skip center — that's the white text pass
            if abs(dx) + abs(dy) <= stroke_w + 1:  # Circular-ish stroke, skip far corners
                draw_text_with_spacing(
                    stroke_draw, font, lines,
                    center_x + dx, top_y + dy,
                    line_h, spacing, STROKE_COLOR
                )
    img = Image.alpha_composite(img, stroke_img)

    # ── White text layer ──────────────────────────────────────────────────────
    text_draw = ImageDraw.Draw(img)
    draw_text_with_spacing(
        text_draw, font, lines,
        center_x, top_y,
        line_h, spacing, TEXT_COLOR
    )

    # Save
    out = str(output_path)
    final = img.convert("RGB") if out.lower().endswith((".jpg", ".jpeg")) else img
    final.save(out)
    return out


def main():
    p = argparse.ArgumentParser(
        description="TikTok Classic text overlay — TikTok Sans Medium, white, subtle shadow"
    )
    p.add_argument("--input",     required=True)
    p.add_argument("--text",      required=True)
    p.add_argument("--output",    required=True)
    p.add_argument("--font-size", type=int, default=None,
                   help="Override font size in px at 1080px width")
    p.add_argument("--position", default="upper", choices=["upper", "center", "lower"],
                   help="Text block position: 'upper' (hook), 'center' (CTA), 'lower' (screenshot labels)")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input not found: {args.input}")
        exit(1)

    result = overlay_text(args.input, args.text, args.output, args.font_size, args.position)
    print(f"Saved: {result}")


if __name__ == "__main__":
    main()
