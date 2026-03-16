# Nano Banana 2 — Image Generation Prompt Templates
*Pre-written for when NB2 image generation is wired into vibe-marketing-generate cron.*
*Trigger: Nash Satoshi TikTok warmed + 4 weeks consistent posting + JT ready to remove manual image assembly.*
*Model: `google/gemini-3.1-flash-image-preview` via OpenRouter*
*Workflow: Generate at 512px → upscale after → cost ≈ NB1*
*Last updated: 2026-03-15*

---

## How to Use These Templates

Each template is a base prompt. The cron injects the **weekly variable fields** (hook text, data point, coin/movie name) before sending to NB2. Fixed aesthetic rules never change — recognizability compounds.

### Generation Workflow (use this, not one-shot)
1. **Batch generate** 5–8 variations of each slide using the Batch API (50% cost discount) at 512px, 9:16
2. **Review the grid** — pick the best composition
3. **Upscale only the winner** to 1080×1920 (or higher if needed)
This is materially cheaper than one-shot + upscale and produces better results.

**Thinking mode: OFF by default.** Only turn ON for complex infographics or when combining visual grounding with spatial reasoning (e.g., Guyana demo maps). Add `thinking: false` to every API call.

For all slides: generate at `512px`, aspect ratio `9:16` (TikTok vertical). Upscale winner to 1080×1920 after selection.

---

## Nash Satoshi — Slideshow Slide Templates

**Fixed aesthetic rules (inject into every NS prompt):**
> Dark navy background (#0a0e1a or near equivalent). White primary text, electric blue (#4a9eff) accent for data points and rankings. Minimal layout — no decorative elements except one thin horizontal rule below the header. Clean sans-serif font, all caps for rankings and coin tickers. Data-forward: every slide must show at least one specific number. Same palette every week — recognizability compounds.

### NS Slide 1 — Hook / Title Card
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: deep navy (#0a0e1a), no gradients, no texture.
Layout: centered text block, starting 30% from the top.
Font style: clean bold sans-serif, white (#ffffff), all caps.
Text to display: "[HOOK TEXT — injected by cron, 6–10 words max, 2 line breaks every 4–6 words]"
Below text: one thin horizontal rule in electric blue (#4a9eff), 60% width, centered.
Bottom left corner: small "NashSatoshi.com" in electric blue, 3% image height font.
No other elements. No decorative shapes. No gradients. No film grain.
Exact replication of palette matters — same look every week.
```

### NS Slide 2 — Data / Rankings Card
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: deep navy (#0a0e1a).
Layout: left-aligned data block, 15% margin from left edge, starting 20% from top.
Header text: "[CATEGORY LABEL — e.g. 'GAME THEORY CONSENSUS SCORE']" — white, small caps, 3% image height.
Thin horizontal rule below header: electric blue (#4a9eff), 85% width.
Data rows (3–5 rows): "[RANK]. [COIN TICKER] — [SCORE or STAT]" — white for rank/ticker, electric blue for the number.
Row spacing: comfortable, not cramped.
Bottom attribution: "4-Model Ensemble · NashSatoshi.com" — electric blue, 2.5% font, bottom right.
No icons. No logos. No gradients. Pure data layout.
```

### NS Slide 3 — Insight / CTA Card
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: deep navy (#0a0e1a).
Layout: centered, text starting 35% from top.
Primary text: "[INSIGHT — 1 sentence, 8–14 words max]" — white, bold, 5% image height font, centered.
Secondary text below (small gap): "[CTA — e.g. 'Full rankings at NashSatoshi.com']" — electric blue, 3% font.
Thin electric blue rule separating primary and secondary text, 50% width, centered.
No other elements.
```

---

## Vista — Slideshow Slide Templates

**Fixed aesthetic rules (inject into every Vista prompt):**
> Dark charcoal/near-black background with subtle film-grain texture overlay (visible but not distracting — noise grain at ~8% opacity). Muted warm tones — gold (#c9a84c) for accent, off-white (#f0ebe0) for primary text. Wide-format cinematic letterbox feel even in 9:16 — use horizontal composition inside the vertical frame. Same palette every week — recognizability compounds.

### Vista Slide 1 — Hook / Rating Drop
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: very dark charcoal (#111111) with subtle film-grain texture overlay (noise at ~8% opacity, monochrome).
Layout: centered, starting 28% from top.
Primary text: "[HOOK — e.g. 'IMDB HAS THIS WRONG']" — off-white (#f0ebe0), bold, 5.5% image height font, all caps, centered.
Below: a movie-style horizontal divider — two thin lines with a small diamond shape in the center, in gold (#c9a84c).
Secondary text: "[MOVIE TITLE + YEAR]" — gold (#c9a84c), 3.5% font, centered.
Film-strip detail: very faint (10% opacity) repeating horizontal sprocket holes along left and right edges.
Bottom right: "Vista App" in off-white, 2.5% font.
```

### Vista Slide 2 — Score Comparison Card
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: dark charcoal (#111111) with film-grain texture overlay.
Layout: two-column comparison block, centered vertically in the frame.
Left column header: "IMDB" — small, off-white, 3% font, centered.
Left column score: "[IMDB SCORE]" — large, 12% font, muted red (#c94a4a).
Right column header: "VISTA" — small, off-white, 3% font, centered.
Right column score: "[VISTA SCORE]" — large, 12% font, gold (#c9a84c).
Thin gold vertical divider between columns.
Below both columns: "[ONE-LINE VERDICT — e.g. 'Underrated by 1.4 points']" — off-white, 3% font, centered.
Film-grain texture throughout.
```

### Vista Slide 3 — CTA Card
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio).

Background: dark charcoal (#111111) with film-grain texture.
Centered text block starting 38% from top.
Primary: "[CTA — e.g. 'Rate it yourself on Vista']" — off-white (#f0ebe0), bold, 5% font.
Movie-style divider below (gold, two lines + diamond).
Secondary: "Vista — Honest Movie Ratings" — gold (#c9a84c), 3% font.
App store badge placeholder (text only): "Download on the App Store" — off-white, 2.5% font, bottom center.
Film-grain throughout.
```

---

## UGC Reaction Slides (both products — faceless)

### Nash Satoshi — UGC Reaction Background Slide
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio) as a screen background for a UGC reaction video overlay.

Background: deep navy (#0a0e1a) gradient darkening toward edges.
Top section (40% of frame): large display of "[COIN TICKER]" in white, bold, 15% font — centered, this is what the camera reaction will frame against.
Below: "[CLAIM BEING REACTED TO — e.g. 'BTC is a store of value']" in electric blue (#4a9eff), 4% font, centered.
Bottom 30%: deliberately left empty/dark for reaction video overlay.
Subtle electric blue glow edge on the outer border (low opacity, ~15%).
```

### Vista — UGC Reaction Background Slide
```
Generate a 512px vertical TikTok slide (9:16 aspect ratio) as a screen background for a UGC reaction video overlay.

Background: dark charcoal (#111111) with heavy film-grain texture.
Top section (40% of frame): "[MOVIE TITLE]" in off-white (#f0ebe0), bold, 10% font — centered.
Below: "[SCORE BEING REACTED TO — e.g. 'IMDB: 6.2  |  Vista: 7.8']" — IMDB score in muted red, Vista score in gold (#c9a84c), 4% font.
Bottom 30%: deliberately empty/dark for reaction video overlay.
```

---

## Integration Notes (for when cron wiring begins)

- Variable fields injected by cron before API call: `[HOOK TEXT]`, `[COIN TICKER]`, `[SCORE]`, `[MOVIE TITLE]`, `[INSIGHT]`, `[CTA]`
- **Workflow:** Batch API (5–8 variations per slide at 512px) → pick winner → upscale winner only
- **Thinking mode:** `thinking: false` on every call. Only enable for infographics or visual grounding + spatial reasoning combos (e.g. Guyana map overlays)
- **Aspect ratio:** 9:16 for all TikTok slides. Extreme ratios (1:4, 1:8) available if ever needed for banners or web assets — not for TikTok
- **Upscaling:** any standard 2x upscaler works — NB2 512px output upscales cleanly to 1080×1920
- **Storage:** `agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]-slide-[N].png`
- **Cost estimate per weekly run:** 3 slides × 2 products × 6 batch variations = 36 calls at ~$0.005 each ≈ $0.18/week. Negligible.
- **Visual grounding:** off for slide text cards. Only enable for location/species-specific imagery (Guyana demos use it; TikTok slides don't need it)
