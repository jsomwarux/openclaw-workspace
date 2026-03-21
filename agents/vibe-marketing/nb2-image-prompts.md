# NB2 Image Prompt Templates — Realistic Scene Photography
*Model: `google/gemini-3.1-flash-image-preview` via OpenRouter*
*Generation script: `~/.openclaw/workspace/scripts/nb2-generate.py`*
*Last updated: 2026-03-20*

---

## Core Principles

**NB2 generates photorealistic scene backgrounds. Nothing else.**

- No text baked into any image — NB2 hallucinates words even on short strings. All text goes in TikTok's native editor.
- No logos, UI elements, or product references in the generated image.
- Every image should look like a photo a real person took of their real environment — not a stock photo, not a staged shoot.
- Leave breathing room at top and center of the frame for text overlays JT will add.
- 9:16 aspect ratio for all slides.
- Thinking mode: OFF on every call.

**The goal:** when someone sees Slide 1, they think "this looks like someone's actual home" — then they read the text JT overlaid and stop scrolling.

**Universal avoid list (include in every prompt):**
```
Avoid: studio lighting, perfect symmetry, stock photo aesthetic, CGI look, artificial sharpness, smooth plastic surfaces, oversaturated colors, beauty filters, dramatic HDR, visible watermarks, text, logos, UI elements, any product branding.
```

---

## How Scene Generation Works (weekly rotation)

**These are variation seeds, not fixed prompts.** The Monday cron generates 2 brand new scene photos per product every week — hook scene + CTA scene. It picks from the concept list below, injects variation parameters, and generates fresh. Zero repeats.

**Rotation rule:** check `state.json` → `last_scene_concept.[product_slug]` before generating. Never pick the same concept two weeks in a row. Cycle through the concept list in order, wrapping around after the last one.

**Variation parameters (inject into every generation — change these weekly):**
- Time cue: "night" / "late evening" / "early morning before sunrise"
- Specific objects on surface: swap what's on the table/desk week to week (coffee → tea → water glass → whiskey → energy drink can)
- Angle: "from slightly above" / "from the side" / "from across the room" / "close-up"
- Season/texture hint: "winter — blanket heavier, thicker" / "summer — lighter fabrics, fan visible" / "rainy night — sound of rain implied by mood"

**Result:** 3x/week posting for 6+ months = 72+ posts, every scene photo unique.

---

## Slide Structure (both products)

| Slide | Who creates it | What it is |
|---|---|---|
| Slide 1 | NB2 (Eve generates fresh weekly) | Realistic scene photo — hook |
| Slides 2–4 | JT (app screenshots from phone) | App UI, rankings, real data |
| Last slide | NB2 (Eve generates fresh weekly) | Realistic scene photo — CTA close |

JT adds ALL text in TikTok's native text editor before posting. Sound is added in TikTok too.

---

## Vista — Scene Concepts (rotation seeds)

Cycle through these in order. Each Monday: pick next concept, inject variation parameters from above, generate fresh image. Never repeat same concept back-to-back.

| # | Concept name | Core elements |
|---|---|---|
| V-1 | Cozy living room | Couch, blanket, dim ambient light from offscreen source |
| V-2 | Hands holding phone | Overhead shot, hands on lap, blanket underneath |
| V-3 | Film ratings notebook | Open notebook with handwritten lists, coffee, wooden surface |
| V-4 | Movie ticket stubs | Stubs + popcorn on coffee table, warm lamp background |
| V-5 | Cozy armchair | Single lamp, book left open, lived-in chair, no person |
| V-6 | Dim bedroom | Bedside lamp on, phone on nightstand, sheets rumpled |
| V-7 | Kitchen table night | Cup of something warm, dim overhead light, quiet late-night feel |
| V-8 | Window at night | Rain or city lights outside, cozy interior foreground, condensation on glass |

`state.json` tracks: `last_scene_concept.vista` = last concept number used. Always pick next one in sequence.

---

### V-1: Cozy Living Room (primary — hook slide)
**Use for:** hook slides with text like "my favorite films of the year so far," "I've been rating every movie I watch," "why I stopped trusting Rotten Tomatoes"

```
A candid photograph of a warm, lived-in living room at night. A large TV on the far wall glows softly — the screen is the primary light source in the room. On the couch: a knit blanket draped casually, a bowl of popcorn resting on a cushion. A half-drunk glass of something on the side table. The room is dim and cozy, the kind of dark that makes watching movies feel like a ritual.

Shot from slightly behind and above the couch, as if someone set their phone on the armrest and took a photo. The TV screen has a soft blue-warm glow but no readable image — just ambient light. The frame feels candid, not staged.

Photorealistic photography. Shot on iPhone. Natural, imperfect lighting. Slight digital noise in the shadow areas. The warmth and texture of a real home, not a model home. Shallow depth of field — the couch and foreground in focus, the TV softly blurred.

Vertical 9:16 frame. Leave the top third of the image with relatively clean visual space (lower contrast, minimal detail) — this is where text will be overlaid.

Avoid: studio lighting, perfect symmetry, stock photo aesthetic, CGI look, artificial sharpness, visible TV program content, any text or logos, overly glamorous interior design. This should look like a photo from someone's actual apartment, not an interior design shoot.
```

---

### V-2 (CTA/close): Late Night Film Session (variation — CTA/close slide)
**Use for:** last slide where JT overlays CTA like "Download Vista — App Store" or "Available now"

```
A close-up photograph of a couch corner at night. A phone face-down on the cushion next to a remote control. A nearly finished bowl of popcorn. The ambient light from the TV creates a warm, amber-blue glow across the scene. A throw pillow slightly crushed from someone sitting. The texture of the fabric is visible.

Shot from directly above, slightly angled — like someone held their phone over the couch and took a candid photo. The TV is partially in frame on the right edge, out of focus, just providing warm ambient light.

Photorealistic photography. Shot on iPhone. Warm ambient light only — no flash, no overhead lights. Slight motion blur or natural imperfection. The kind of photo someone takes and sends to a friend saying "movie night setup."

Vertical 9:16 frame. Leave the center of the frame visually uncluttered — moderate contrast area where text overlay will read clearly.

Avoid: studio lighting, visible phone screen content, any text, stock photo aesthetic, CGI look, overly clean or staged surfaces.
```

---

### V-3 (controversy/reaction): Cinema Seat / Theater (variation — for controversy/reaction posts)
**Use for:** slides reacting to IMDb ratings, crowd consensus posts, "hot take about movie ratings" content

```
A candid photograph taken from inside a movie theater, from a seat in the middle rows. The screen at the front of the theater is bright, casting light across the rows of seats ahead. The theater is dark except for the screen glow. A few silhouetted heads of other audience members visible in the lower portion of the frame. Armrests on either side.

Shot as if someone held their phone up casually during a film — slightly imperfect angle, natural. The screen shows bright light but no readable content. The mood is intimate and cinematic.

Photorealistic photography. Shot on iPhone in a dark environment — higher ISO, natural grain, slightly imperfect focus on the darker areas. The screen glow is the dominant light. Real theater atmosphere.

Vertical 9:16 frame. The upper third of the frame (above the audience heads) is primarily screen glow — clean bright area for text overlay.

Avoid: flash photography, studio lighting, perfect focus, any visible film content on screen, text, stock photo aesthetic.
```

---

## Nash Satoshi — Scene Concepts (rotation seeds)

Same rotation logic. `state.json` tracks: `last_scene_concept.nash-satoshi` = last concept number used.

| # | Concept name | Core elements |
|---|---|---|
| NS-1 | Dark home office — multiple screens | 2-3 monitors, no person, late night research feel |
| NS-2 | Single laptop — coffee shop or home | Open laptop glow, coffee nearby, dim warm background |
| NS-3 | Dark living room — TV + laptop | Multi-screen setup from across room, no person |
| NS-4 | Phone on desk at night | Phone face-up (dark screen), notebook, pen, dark ambient |
| NS-5 | Close-up keyboard + screens | Tight shot of keyboard, monitor glow behind, coffee to the side |
| NS-6 | Balcony or window at night | City lights background, laptop or phone in foreground, outdoor/indoor edge |
| NS-7 | Couch + laptop at night | Person-less couch, laptop open, dim room, late night feel |
| NS-8 | Trading/research desk from above | Overhead flat lay — notebook, phone, laptop, coffee, dark surface |

---

### NS-1: Dark Home Office — Multiple Screens (primary — hook slide)
**Use for:** hook slides with text like "this tool permanently changed my crypto strategy," "spent 3 years picking coins based on vibes," "game theory scores every crypto asset"

```
A candid photograph of a home office setup at night, lit only by the glow of multiple computer monitors. Two or three monitors on a desk — the screens are bright with abstract data/chart-like visuals (no readable tickers or specific data — just the visual texture of screens showing information). The room behind the desk is completely dark. A coffee mug on the desk. A notebook. The atmosphere of someone doing serious late-night research.

Shot from slightly to the side, as if someone walked into the room and took a photo from the doorway. The glow from the monitors illuminates the desk and keyboard from the front. The chair is empty — just the workspace.

Photorealistic photography. Shot on iPhone. Only light source is the monitors — natural screen glow, slight halation around the brightest areas. The darkness around the edges is real, not artificially vigneted. The desk has the slight disorder of an actively used workspace — not a showroom.

Vertical 9:16 frame. Leave the upper third of the image as the darker ceiling/wall area — this is the primary text overlay zone.

Avoid: studio lighting, neon RGB gaming aesthetic, stock photo tech setup, perfect desk symmetry, any visible screen content that's readable, text or logos, CGI look. This should look like a real person's research setup, not a tech influencer's desk tour.
```

---

### NS-2 (hook/CTA): Single Laptop, Coffee Shop or Home (variation — hook/CTA)
**Use for:** "I've been using this for 6 months" hook slides, or closing CTA slides

```
A candid photograph of a person's laptop on a surface — either a dark wood coffee table in a living room or a café table at night. The laptop screen is open and bright, casting a soft glow on the immediate surface. A coffee cup or glass nearby. The background is warm and dim — blurred café lights or a dark apartment.

Shot from slightly above and to the side, like someone set their phone down and took a photo. The laptop screen is bright but no readable content — just the glow. The person using it is not in frame.

Photorealistic photography. Shot on iPhone. Natural ambient lighting supplemented by laptop screen glow. Grain in the darker areas. The warm imperfection of a real candid photo, not a styled flat lay.

Vertical 9:16 frame. The upper portion of the frame (above the laptop) should be the softest, least detailed area — ideal for text overlay.

Avoid: studio lighting, stock tech photography, visible screen content, any brand logos on laptop, perfect surface alignment, text, CGI look, any neon or gaming aesthetics.
```

---

### NS-3 (aspirational): Dark Living Room, Multiple Screens (variation — aspirational)
**Use for:** high-aspirational hook slides, "the setup" energy, posts targeting serious traders

```
A candid photograph of a dark, modern living room at night. A large TV on the wall. A laptop open on the coffee table. The room is lit only by the screens — cool blue-white light from the TV, warmer tones from the laptop. A glass of water or whiskey on the table. The couch visible, lived in. No lamps on, no overhead lighting.

Shot from across the room, slightly elevated — like someone is standing near the entrance and captures the whole scene. The vibe is: serious, late-night, focused. The kind of setup where real decisions get made.

Photorealistic photography. Shot on iPhone. Low-light, natural screen glow only. Significant grain in the dark areas. The image feels slightly moody but not cinematic — this is an apartment, not a movie set.

Vertical 9:16 frame. The upper portion — wall above the TV — is the darkest and cleanest area. Ideal for text overlay.

Avoid: visible screen content, neon lighting, RGB gaming setup, overly luxurious apartment aesthetics (no penthouse vibes — this is a regular apartment where someone works hard), studio lighting, text, logos, CGI look.
```

---

## Variable Fields Per Call

Before calling NB2, inject the correct scene template. No variable text fields — these prompts are complete as-is. Scene selection is based on content theme:

| Content theme | Vista scene | Nash Satoshi scene |
|---|---|---|
| Hook — personal discovery | V-SCENE-A | NS-SCENE-A |
| Hook — controversy / reaction | V-SCENE-C | NS-SCENE-A |
| CTA / close | V-SCENE-B | NS-SCENE-B |
| Aspirational / "the setup" | V-SCENE-A | NS-SCENE-C |

---

## Generation Command

```bash
source ~/.config/env/global.env
python3 ~/.openclaw/workspace/scripts/nb2-generate.py \
  --prompt "[full scene prompt — copy from above, no modifications]" \
  --output "agents/vibe-marketing/generated-images/[product_slug]/[YYYY-MM-DD]/slide-[1 or last].png"
```

Naming convention:
- Hook slide: `slide-01-hook.png`
- CTA slide: `slide-last-cta.png`

---

## Drive Delivery

After generating, upload both slides to Drive:

```bash
cd ~/.openclaw/workspace
python3 scripts/drive_drafts.py \
  --title "[Product] TikTok Slides — Week of [YYYY-MM-DD]" \
  --path "Content/Vibe Marketing/[Product Name]/TikTok Slides" \
  --file /tmp/vibe-slides-[product]-[date]-manifest.md
```

The manifest file lists the local image paths and includes JT's text overlay instructions for each slide.

---

## JT's TikTok Assembly Instructions (included in Drive manifest each week)

```
## How to assemble this TikTok

1. Open TikTok → + → select photos from your gallery
2. Upload in order: Slide 1 (hook scene) → your app screenshots → Last slide (CTA scene)
3. On Slide 1: add text overlay with the hook line (see slide copy below)
4. On middle slides: add text labels if needed (see slide copy below)
5. On Last slide: add text overlay with CTA (see slide copy below)
6. Pick a trending sound from TikTok's library in your niche before posting
7. Copy caption from review doc → paste into TikTok caption field → post

Slide 1 hook text: [from this week's slide copy]
Middle slide labels: [from this week's slide copy]
Last slide CTA text: [from this week's slide copy]
```

---

## Cost

~2 NB2 calls per product per week (hook + CTA slide) = 4 calls/week for both products.
~$0.01–$0.02/week total. Negligible.

**Thinking mode OFF:** never enable for scene photography — it adds cost and latency with no quality benefit for this use case.

---

## Screenshot Instructions (unchanged — JT provides these)

### Vista — App UI Slides (Slides 2–4)
```
📸 SCREENSHOTS NEEDED — Vista App (iOS)
Open Vista on your phone.
Capture 2-3 screenshots:
  1. Your ratings list — ideally 20+ films visible, showing variety of scores
  2. A film detail page — showing your personal score + the film info
  3. Your taste profile screen (optional — strong proof point)
These are Slides 2-4. The app UI IS the product demo.
```

### Vista — App Store Slide (optional last slide alternative)
```
📸 OPTIONAL — App Store listing screenshot
Open App Store → search Vista → capture the listing page with app icon visible.
More credible as a CTA than any generated image.
Use as the very last slide instead of the NB2 CTA scene if you want.
```

### Nash Satoshi — Rankings Slides (Slides 2–4)
```
📸 SCREENSHOTS NEEDED — NashSatoshi.com
Open nashsatoshi.com on your phone.
Capture 2-3 screenshots:
  1. Full rankings table — top 10 visible
  2. A specific asset's detail/score breakdown if available
  3. The scoring methodology page if available
Fresh data screenshots = more credible than any generated graphic.
```
