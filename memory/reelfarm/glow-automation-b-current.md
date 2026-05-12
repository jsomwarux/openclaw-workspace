# Glow Index ReelFarm Automation B — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/glow-automation-b/`.
Extraction: OpenClaw image tool.

## Screenshot Files

1. `memory/reelfarm/screenshots/glow-automation-b/01.jpg`
2. `memory/reelfarm/screenshots/glow-automation-b/02.jpg`
3. `memory/reelfarm/screenshots/glow-automation-b/03.jpg`
4. `memory/reelfarm/screenshots/glow-automation-b/04.jpg`
5. `memory/reelfarm/screenshots/glow-automation-b/05.jpg`
6. `memory/reelfarm/screenshots/glow-automation-b/06.jpg`
7. `memory/reelfarm/screenshots/glow-automation-b/07.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (14)`
- Hook count: 14
- Helper text: each line is a separate hook
- Visible hooks:
  - “How 4 AIs analyze every skincare product, in 5 slides.”
  - “What Glow Index actually measures, in 5 slides.”
  - “Why I stopped trusting skincare influencers and built this instead.”
  - “4 AIs, every ingredient, one score. Here's how it works.”
  - “The 4-AI test every skincare product should pass before you buy.”
  - “How to spot a skincare scam in 30 seconds, using 4 AIs.”
  - “The framework I use to find skincare dupes, in 5 slides.”
  - “4 AIs disagree on more skincare products than you'd think. That's the point.”
  - “What separates an A-tier skincare product from a C-tier one.”
  - “The 4 AI models that rank every skincare product, explained.”
  - “Why "clean" skincare doesn't always score better. Here's the data.”
  - “The skincare scoring system that ignores marketing claims.”
  - “How Glow Index ranks every product on the market, in 5 slides.”
- Last hook is obscured/cut off.

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style white_background. Keep hook to 10-16 words maximum. Hook should feel like a friend spilling a secret — informed and slightly skeptical of skincare marketing. Render "Glow Index" with proper capitalization.
>
> Body slides 2-5: no overlay text. The Glow Index platform screenshots carry all the information on their own. Viewers see the actual tool — rankings, score breakdowns, ingredient analysis, 4-AI comparisons — which demonstrates the product visually better than text overlays could.
>
> Tone on the hook slide is informed, slightly skeptical, friendly. No medical jargon. No exclamation points, no emojis.

### Text Content — Settings Beta

- Hook text only: ON
- No text: OFF
- Product context: `No product context`

### Image Content

- Hook collection: `glow-lifestyle`
- All Slides collection: `glow-screenshots`
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
- Visible prompt: “Write a TikTok caption under 80 characters that teases the finding without giving it all away. Mention "Glow Index" or "glowindex.co" naturally if it fits. End with 4 hashtags: #skintok #skincare #skincareingredients #glowindex. No exclamation points. One subtle emoji at the very end if it fits naturally (e.g. the eyes...”
- Caption prompt continues below visible area.

Default TikTok settings:
- Post as draft: ON
- Publish as: Slideshow
- Video option disabled with note: enable “Export as video” in Settings to publish as video
- Auto-music: OFF / disabled because posting as draft cannot auto-add music
- Who can view: Public
- Allow comments: ON
- Allow duet: ON
- Allow stitch: ON
- Disclose video content: OFF

## Not Visible / Not Captured

- Schedule / cron not visible in screenshots.
- Overall automation enabled/paused status not visible.
- Global Settings page not shown.
- Export-as-video global setting not directly visible, though publish-as-video is disabled and slideshow is selected.

## Baseline Comparison Notes

Expected for Glow Automation B:
- lifestyle hook + screenshots format ✅
- `glow-lifestyle` hook collection ✅
- `glow-screenshots` all-slides collection ✅
- hook text only ON ✅
- screenshot body text OFF ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- Glow Index proper case ✅
- no medical jargon in prompt ✅
- no overlay text on screenshot slides ✅

Potential issues:
- Prompt says hook max is 10–16 words, but universal baseline says hook slides should be 8–14 words. Tighten to 8–14 unless performance data says Glow B needs longer hooks.
- `Enable overlay` is ON while body slides are screenshots. Baseline says Automation B body overlay should be OFF so screenshots stay clean and legible; only hook overlay should be ON. Need verify whether ReelFarm's hook-text-only prevents body overlay from applying. If not, turn global overlay OFF and keep hook overlay ON.
- `Post as draft` is ON, which blocks Auto-music. Compatible with manual warm-up, not fully autonomous runtime with auto-music.
- Caption prompt requires 4 hashtags while also under 80 characters and potentially one emoji. This is overcrowded.
- Visible hooks are mostly feature/process-forward. Add more skincare-buyer regret, influencer distrust, price shock, and dupe-conflict hooks.
