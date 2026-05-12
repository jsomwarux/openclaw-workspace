# Glow Index ReelFarm Automation A — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/glow-automation-a/`.
Extraction: OpenClaw image tool.

## Screenshot Files

1. `memory/reelfarm/screenshots/glow-automation-a/01.jpg`
2. `memory/reelfarm/screenshots/glow-automation-a/02.jpg`
3. `memory/reelfarm/screenshots/glow-automation-a/03.jpg`
4. `memory/reelfarm/screenshots/glow-automation-a/04.jpg`
5. `memory/reelfarm/screenshots/glow-automation-a/05.jpg`
6. `memory/reelfarm/screenshots/glow-automation-a/06.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (14)`
- Hook count: 14
- Helper text: each line is a separate hook
- Visible hooks:
  - “4 AIs analyzed every Drunk Elephant product. The top pick was under $40.”
  - “This $215 moisturizer scored a 45 out of 100. Here's what 4 AIs found.”
  - “The $12 serum that outscored luxury skincare brands in 4-AI testing.”
  - “Skincare girlies are not going to like what 4 AIs said about this cult product.”
  - “4 AIs flagged the ingredient in your "clean" skincare that's actually irritating.”
  - “La Mer scored lower than CeraVe in 4-AI testing. Here's why.”
  - “The Ordinary, ranked best to worst by 4 AIs. Some picks will surprise you.”
  - Partial/cutoff: “4 AIs confirmed these dupes. Save the screenshot before brands...”
- Only 8 of 14 hooks visible.

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style white_background. Hook should feel like a friend spilling a secret over coffee — informed and slightly skeptical of skincare marketing, never clinical or preachy. Keep to 8-14 words. When prices or scores appear, keep them as digits for readability ("$215", "45/100"). Render "Glow Index" with proper capitalization, never all caps.
>
> Body slides 2-5: one text item at bottom position, font TikTokDisplay-Bold, size medium, text_style white_background. KEEP EACH BODY SLIDE TO 8-15 WORDS MAXIMUM. Each body text must reference one specific element: an ingredient name (retinol, niacinamide, hyaluronic acid, vitamin C), a price comparison, a specific score or tier, a brand name, or a 4-AI...

Prompt continues below visible area.

### Image Content

- Hook collection: `glow-lifestyle`
- All Slides collection: `glow-lifestyle`
- Hook Slide Grid: `Single`
- Body Slides Grid: `Single`
- Auto-images: OFF
- Repeat hook image: OFF
- Force CTA slide: OFF
- Keep original aspect ratio: OFF
- Enable overlay: ON
- Enable overlay on hook image: ON
- Aspect ratio: `9:16`
- Overlay opacity: `25%`

### TikTok Settings

- Auto-post to TikTok: ON
- TikTok account: `@glow.index`
- Display name: `Glow Index`

Title:
- Use prompt: ON
- Prompt: “Match the text on the first slide exactly, in sentence case. Do not add anything.”

Caption:
- Use prompt: ON
- Visible prompt: “Write a TikTok caption under 80 characters that teases the finding without giving it all away. Mention "Glow Index" or "glowindex.co" naturally if it fits. End with 4 hashtags: #skintok #skincare #skincareingredients #glowindex. No exclamation points. One...”
- Caption prompt continues below visible area.

Default TikTok settings:
- Post as draft: ON
- Publish as: Slideshow
- Video option disabled with note: enable “Export as video” in Settings to publish as video
- Auto-music: OFF because posting as draft cannot auto-add music
- Who can view: Public
- Allow comments: ON
- Allow duet: ON
- Allow stitch: ON
- Disclose video content: OFF

## Not Visible / Not Captured

- Schedule / cron not visible in screenshots.
- Overall automation enabled/paused status not visible.
- Full prompt/caption text below visible cutoff not captured.
- Export-as-video global setting not directly visible, though publish-as-video is disabled and slideshow is selected.

## Baseline Comparison Notes

Expected for Glow Automation A:
- all-lifestyle format ✅
- `glow-lifestyle` for hook and all slides ✅
- overlay ON ✅
- hook overlay ON ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- Glow Index proper case ✅
- skincare brand/ingredient callouts allowed ✅
- friend-spilling-secrets voice present ✅

Potential issues:
- Several visible hooks are longer than the universal 8–14 word hook rule. Examples: Drunk Elephant hook, $215 moisturizer hook, “skincare girlies” hook, clean skincare ingredient hook.
- `Post as draft` is ON, which blocks Auto-music. Compatible with manual warm-up, not fully autonomous runtime with auto-music.
- Caption prompt requires 4 hashtags while also under 80 characters; this is probably too crowded. Glow allows one subtle emoji in captions, but no emoji is visible in prompt before cutoff.
- Some hooks are strong but feature/test-forward rather than Larry-framework person + conflict + reveal. For Glow this can work because price exposés and brand callouts are stable, but hook list should still bias toward human skincare regret/conflict.
