# Nano Banana 2 — Image Generation Prompt Templates
*Model: `google/gemini-3.1-flash-image-preview` via OpenRouter*
*Generation script: `~/.openclaw/workspace/scripts/nb2-generate.py`*
*Last updated: 2026-03-16*

---

## Core Principles

**NB2 is an image generator, not a typesetter.** Write prompts in visual/cinematic language — mood, composition, lighting, texture, aesthetic reference points. Hex codes and pixel percentages don't translate.

**All slides are background-only.** NB2 never renders text — it hallucinates words and numbers even on short strings. NB2's job is atmosphere, color, composition, and mood. ALL text goes in CapCut as overlays. This is non-negotiable.

**Aesthetic consistency = brand recognition.** Same palette, same visual language, same feel every week. Viewers should recognize Nash Satoshi and Vista content in 0.3 seconds before reading a word.

**Prompt language that works:** cinematic references, material descriptions, lighting conditions, mood, compositional rules, aesthetic inspirations (e.g. "Bloomberg terminal dark mode," "35mm film grain," "noir movie poster").

**Thinking mode: OFF for all slides.** Only enable for maps or complex spatial grounding.

**Output:** 9:16 aspect ratio, 512px → upscale winner to 1080×1920.

---

## Nash Satoshi — Visual Identity

**Aesthetic anchor:** Bloomberg terminal meets crypto dark mode. Institutional, data-forward, analytical. Not flashy, not crypto-bro. The visual language says "this is serious analysis" before any text is read.

**Palette (describe this way in prompts):** Deep navy almost-black background. Pure white for primary text. Electric blue — the kind you see on a trading terminal or a CoinGecko dark mode chart — for data points and accents. No warm tones. No gradients. No decorative shapes.

**Mood:** Late night, focused, like someone doing real market research at 2AM. Cool, precise, institutional.

---

### NS Slide 1 — Hook Card
**Purpose:** Stop the scroll. One bold claim that makes the viewer need to see the next slide.
**Render mode:** Full render — NB2 renders the hook text.

```
A vertical TikTok slide (9:16). Dark navy background, nearly black, completely flat — no gradients, no texture, no glow. The slide feels like a high-contrast terminal screen.

Center of the frame: bold, large, all-caps sans-serif text in pure white reading:
"[HOOK TEXT]"
Text is the dominant element. Nothing competes with it. No decorative shapes, no icons.

Below the text: a single thin horizontal line in bright electric blue — the kind of blue you see on a Bloomberg terminal or a dark-mode crypto chart. The line is 60% of the slide width, centered.

Bottom-left corner: the URL "NashSatoshi.com" in small electric blue text, minimal, unobtrusive.

The overall feel: clean, institutional, like a data terminal. This is analytical, not hype.
Avoid: gradients, glows, decorative elements, any warm colors, anything that looks like crypto marketing.
```

---

### NS Slide 2 — Data / Rankings Card
**Purpose:** Show the actual consensus scores. This is the evidence slide — the data that backs the hook.
**Render mode:** Background-only. NB2 generates the frame; rankings data overlaid in CapCut by JT.

```
A vertical TikTok slide (9:16) designed as a data visualization frame — no readable text needed, JT will add the data as a text overlay.

Background: deep navy, nearly black, flat and clean like a terminal.

Left side of the frame: a subtle vertical electric blue line running from 15% from top to 85% from top, 2-3px thick — like a data table left border.

Top section: a thin horizontal electric blue line spanning 85% of the width, 20% from the top — this is where the category header text will be overlaid.

Below that: evenly spaced horizontal guides — 4-5 of them, each subtle (very low opacity, almost invisible), spanning 85% width — these mark where each ranking row will go.

Bottom right: a faint attribution block placeholder — just a subtle rectangular region of slightly lighter navy.

The structure should feel like a financial data table or a terminal readout. Grid-like. Precise. Ready for data.
Avoid: any text, icons, decorative elements. This is a frame for overlaying data, not a finished slide.
```

**Post-processing (CapCut):** JT overlays: category label at top, 3-5 ranking rows (RANK. TICKER — SCORE) in white/electric blue, attribution line at bottom right.

---

### NS Slide 3 — Insight / CTA Card
**Purpose:** Land the takeaway and drive to the website. The payoff.
**Render mode:** Full render — NB2 renders insight text and CTA.

```
A vertical TikTok slide (9:16). Same deep navy background as the other slides — flat, dark, terminal aesthetic.

Upper-center of the frame (starting around 35% from top): bold white sans-serif text reading:
"[INSIGHT — 1 sentence, under 14 words]"

A thin electric blue horizontal rule below the insight text, centered, 50% slide width.

Below the rule: smaller electric blue text reading:
"[CTA — e.g. 'Full rankings at NashSatoshi.com']"

The slide feels like the conclusion screen of a data presentation. Sparse. Authoritative. Everything has been earned by slides 1 and 2.
Avoid: decorative elements, warm colors, anything that looks like a call-to-action button or marketing material.
```

---

### NS UGC Reaction — Background Card
**Purpose:** Visual backdrop for a text-overlay reaction to a crypto take. The background signals "this is game theory analysis responding to something."
**Render mode:** Background-only — NB2 generates frame; the claim being reacted to is overlaid in CapCut.

```
A vertical TikTok slide (9:16) designed as a reaction video background.

Background: deep navy, nearly black. A subtle dark radial vignette — edges slightly darker than center, like a spotlight on the content area.

Top 40% of the frame: a large, centered placeholder region with a subtle electric blue border (thin, 2-3px). Inside: a faint grid texture, like graph paper at very low opacity — this is where the "claim being reacted to" text will be overlaid.

Lower section: the electric blue accent line from the Nash Satoshi identity, thin, spanning 70% width, separating top and bottom halves.

Bottom 35%: clean dark navy, ready for the reaction commentary text overlay.

Bottom left: "NashSatoshi.com" very small in electric blue.

The visual language: this is a split-take format. Top = the claim. Bottom = the counter. The frame communicates this structure before any text is added.
Avoid: heavy decorative elements, anything that competes with text overlays.
```

---

## Vista — Visual Identity

**Aesthetic anchor:** Film poster meets personal journal. Cinematic, moody, intimate. This is for someone who takes movies seriously — not entertainment, not hype. The visual language says "a real film person made this."

**Palette (describe this way in prompts):** Very dark charcoal, almost black — richer and warmer than Nash Satoshi's cold navy. Off-white cream text, not stark white. Gold accents — not bright yellow, but the warm muted gold of old film titles. 35mm grain throughout. Film-strip details at low opacity.

**Mood:** Late night in a dark room with a film playing. The aesthetic of a Criterion Collection blu-ray menu — beautiful, restrained, reverent toward cinema.

---

### Vista Slide 1 — Hook Card
**Purpose:** Stop the scroll with a provocative take on movie ratings or taste. The hook is the whole slide.
**Render mode:** Full render — NB2 renders the hook text.

```
A vertical TikTok slide (9:16) with a cinematic, film-poster aesthetic.

Background: very dark charcoal, almost black but with a subtle warm undertone — richer than pure black, like the darkness of a movie theater. Overlaid with a fine 35mm film grain texture — visible but not heavy, the kind that makes digital look like film.

Center of the frame: large, bold, all-caps serif or high-contrast sans-serif text in off-white (warm cream, not pure white) reading:
"[HOOK TEXT]"

Below the text: a film-poster style divider — two thin horizontal lines with a small diamond shape at center, in warm muted gold. Like a title card from a classic film.

Below the divider: smaller gold text reading:
"[MOVIE TITLE + YEAR]"

Along the left and right edges: very faint, low-opacity vertical film-strip sprocket holes — subtle, not distracting. Just enough to reinforce the cinematic identity.

Bottom right corner: "Vista" in small cream text.

The overall feel: a film festival title card. Elegant, moody, serious about cinema.
Avoid: bright colors, digital gradients, anything that looks like a streaming app. This is analog cinema energy.
```

---

### Vista Slide 2 — Score Comparison Card
**Purpose:** Show the gap between the crowd score (IMDb) and Vista's personal taste score. The contrast IS the argument.
**Render mode:** Background-only for the frame structure. The actual scores are overlaid in CapCut.

```
A vertical TikTok slide (9:16) designed as a comparison frame — no readable numbers needed, JT will overlay the actual scores.

Background: very dark charcoal with 35mm film grain texture throughout.

Center of the frame: a two-column layout structure.
Left column: a subtle placeholder region for "IMDB" — topped by small all-caps label space in cream, with a muted red-tinted area below for the score number. No actual numbers — just the visual region.
Right column: a matching placeholder region for "VISTA" — topped by small all-caps label space, with a warm gold-tinted area below for the score. No actual numbers.

Between the columns: a thin vertical gold line as a divider, running about 60% of the frame height, centered vertically.

Below both columns: a thin horizontal gold line spanning 70% width, with a small blank region below it for a one-line verdict text overlay.

Film grain throughout. The frame should feel like a film critic's scorecard.
Avoid: any text or numbers. This is a structural frame — the data comes from JT's overlay.
```

**Post-processing (CapCut):** JT overlays: "IMDB" label + score (in muted red), "VISTA" label + score (in gold), one-line verdict below.

---

### Vista Slide 3 — CTA Card
**Purpose:** Convert interest to action. Download the app. Tone stays cinematic — never becomes an ad.
**Render mode:** Full render — NB2 renders CTA text.

```
A vertical TikTok slide (9:16). Same dark charcoal background with 35mm film grain.

Center of the frame (starting 38% from top): bold off-white text reading:
"[CTA — e.g. 'Rate it yourself on Vista']"

Below: the film-poster style gold divider (two thin lines + diamond).

Below the divider: smaller gold text reading:
"Vista — Honest Movie Ratings"

Near the bottom of the frame: small cream text reading:
"Download on the App Store"

The slide should feel like the final card of a film trailer — understated, not salesy. The CTA earns attention rather than demanding it.
Film grain throughout.
Avoid: bright colors, App Store badge graphics, anything that looks like a display ad.
```

---

### Vista Slides 4–6 — See Screenshot Instructions

Slides 4 (payoff/insight) can use the same visual treatment as Slide 3 with different text injected.
Slides 5–6 require JT-captured screenshots — see Screenshot Instructions section below.

---

### Vista UGC Reaction — Counter-Argument Background Card
**Purpose:** Visual backdrop for the "reaction" slides that respond to a specific IMDb/RT rating. Communicates "this is a counter-take" before any text is read.
**Render mode:** Background-only — the source rating (real IMDb screenshot) and counter text are overlaid by JT.

```
A vertical TikTok slide (9:16) designed as a reaction video background.

Background: very dark charcoal with heavy 35mm film grain texture — heavier grain than the standard slides, adding tension.

Top 40% of the frame: a framed placeholder region — thin gold border (2px), inside it a subtle darker background. A faint "reaction frame" energy. This is where the IMDb rating screenshot will be placed as an overlay.

Below the framed region: a thin gold horizontal line spanning 65% width — the visual separator between "the claim" and "the counter."

Bottom 45%: clean dark charcoal with film grain — ready for the counter-argument text overlay in CapCut.

Bottom right: "Vista" in very small cream text.

The visual language: this is a film critic's annotation of someone else's take. The gold frame on top signals "this is what we're reacting to." The open space below signals "here's why they're wrong."
Avoid: busy backgrounds, anything that competes with text overlays.
```

**Post-processing (CapCut):** JT places real IMDb screenshot in the top framed region + adds counter-argument text in the bottom section.

---

## Screenshot Instructions (JT captures — no NB2 needed)

These slides are more authentic with real screenshots than generated images. The agent includes these exact instructions in the Drive review doc each week.

### Vista — Slide 5: App UI
```
📸 SCREENSHOT NEEDED — Vista App (iOS)
Open Vista. Go to your personal ratings list or a film detail page.
Best shot: your profile showing 50+ logged films, OR a film detail showing your score vs. crowd score.
Capture full screen, portrait. Clean UI, no notifications showing.
This slide = social proof that the app is real and actively used.
Caption to add in CapCut: "what tracking [your film count]+ films actually looks like"
```

### Vista — Slide 6: App Store Listing
```
📸 SCREENSHOT NEEDED — App Store (iOS)
Open App Store → search "Vista" → open the listing.
Capture the app icon, name, rating, and download button in frame.
This is the conversion slide. Real App Store screenshot is 10x more credible than any generated image.
No caption needed — the App Store UI is the CTA.
```

### Nash Satoshi — Slide 3 (Optional Upgrade): Rankings Page
```
📸 SCREENSHOT OPTIONAL — NashSatoshi.com
Open nashsatoshi.com. Capture the live rankings table, top 10 visible.
Use instead of the NB2 CTA card when the rankings data is fresh.
A real screenshot of real data is stronger social proof than a generated card.
Add a CapCut text overlay: "Full rankings at NashSatoshi.com"
```

### Vista UGC Reaction — Slide 2: IMDb Source Rating
```
📸 SCREENSHOT NEEDED — IMDb app or imdb.com
Navigate to this week's film. Capture the rating (e.g. 7.1/10) with the film title visible.
Use a real screenshot — not a generated mock. Real source = reaction format feels legitimate.
Place in the top framed region of the NB2-generated UGC background card.
```

---

## Integration Notes

**Variable injection per call:** `[HOOK TEXT]`, `[MOVIE TITLE + YEAR]`, `[INSIGHT]`, `[CTA]`, `[COIN TICKER]`, `[CLAIM BEING REACTED TO]`

**What NB2 renders vs. what gets overlaid:**
| Slide | NB2 renders | CapCut overlay |
|---|---|---|
| NS Slide 1 — Hook | Full card + hook text | Nothing |
| NS Slide 2 — Data | Background frame only | Rankings, tickers, scores |
| NS Slide 3 — CTA | Full card + insight + CTA | Nothing (or swap for screenshot) |
| NS UGC Background | Frame only | Claim text + reaction text |
| Vista Slide 1 — Hook | Full card + hook text + movie title | Nothing |
| Vista Slide 2 — Scores | Background frame only | IMDB score, Vista score, verdict |
| Vista Slide 3 — CTA | Full card + CTA text | Nothing |
| Vista UGC Background | Frame only | IMDb screenshot + counter text |

**Generation command:**
```bash
source ~/.config/env/global.env
python3 ~/.openclaw/workspace/scripts/nb2-generate.py \
  --prompt "[full prompt with variables injected]" \
  --output "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-[N].png"
```

**Cost:** ~6-8 NB2 calls/week (reduced vs. earlier estimate — background-only slides cut total calls). ~$0.03-$0.05/week.

**Thinking mode:** `false` on every call — never enable for TikTok slides.

**Upscaling:** 512px output upscales cleanly to 1080×1920 with any standard 2x upscaler.

**If NB2 call fails:** log error, skip that slide, continue. Missing images don't block content delivery — copy is the primary output.
