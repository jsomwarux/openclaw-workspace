# Nash Satoshi ReelFarm Automation A — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/nash-automation-a/`.
Extraction: OpenClaw image tool, verified after `sharp` install.

## Screenshot Files

1. `memory/reelfarm/screenshots/nash-automation-a/01.jpg`
2. `memory/reelfarm/screenshots/nash-automation-a/02.jpg`
3. `memory/reelfarm/screenshots/nash-automation-a/03.jpg`
4. `memory/reelfarm/screenshots/nash-automation-a/04.jpg`
5. `memory/reelfarm/screenshots/nash-automation-a/05.jpg`
6. `memory/reelfarm/screenshots/nash-automation-a/06.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (14)`
- Hook count: 14
- Helper text: each line is a separate hook
- Visible hooks:
  - “You're not buying the bottom. You're exit liquidity.”
  - “The difference between buying strength and holding someone else's bags is 4 AIs.”
  - “If you have to ask whether you're exit liquidity, you already are.”
  - “This token is in Distribution phase. The chart looks bullish. It isn't.”
  - “Every pump has 5 phases. Most traders learn about Mania one phase too late.”
  - “By the time a token trends on CT, it's already in Distribution.”
  - “Only 11 out of 279 tokens hit S+ tier this week. The math is that strict.”
  - “4 AIs agreeing on a token is rarer than you think. It matters when they do.”
  - “S-tier requires 70 out of 100. Most tokens CT pumps score below 50.”
  - Partial/uncertain lower hook visible.

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style black_background. Hook should feel contrarian and analytical with a touch of attitude. Keep to 8-14 words maximum. Render "Nash Satoshi" with proper capitalization.
>
> Body slides 2-4: one text item at bottom position, font TikTokDisplay-Bold, size medium, text_style black_background. KEEP EACH BODY SLIDE TO 8-15 WORDS MAXIMUM. This is critical — TikTok viewers will not read longer text. One specific idea per slide. Examples of the right length:
> - "Most tokens fail the Asymmetry test."
> - "Schelling Rank above 80 is rare."
> - "Claude 4.6 flagged it 11 days before."

Prompt text is cut off after this point in screenshot.

### Image Content

- Hook collection: `nash-lifestyle`
- All Slides collection: `nash-lifestyle`
- Hook Slide Grid: `Single`
- Body Slides Grid: `Single`
- Auto-images: OFF
- Repeat hook image: OFF
- Force CTA slide: OFF
- Keep original aspect ratio: OFF
- Enable overlay: ON
- Enable overlay on hook image: ON
- Aspect ratio: `9:16`
- Overlay opacity: `35%`

### TikTok Settings

- Auto-post to TikTok: ON
- TikTok account: `@nashsatoshi`
- Display name: `Nash Satoshi`

Title:
- Use prompt: ON
- Prompt: “Match the text on the first slide exactly, in sentence case. Do not add anything.”

Caption:
- Use prompt: ON
- Prompt: “Write one short line (under 50 characters) that states the core insight without hype, direct and analytical. Then on a new line, add these 5 hashtags: #crypto #gametheory #altcoins #cryptoanalysis #cryptotok. No exclamation points. No emojis. No hype words like "moon" or "gem". Nothing else.”

Default TikTok settings:
- Post as draft: ON
- Publish as: Slideshow
- Video option disabled with note: enable “Export as video” in Settings to publish as video
- Auto-music: OFF / unavailable because posting as draft cannot auto-add music
- Who can view: Public
- Allow comments: ON
- Allow duet: ON
- Allow stitch: ON
- Disclose video content: OFF

## Not Visible / Not Captured

- Schedule / cron not visible in screenshots.
- Overall automation enabled/paused status not visible.
- Full prompt below visible cutoff not captured.
- Export-as-video global setting not directly visible, though publish-as-video is disabled and slideshow is selected.

## Baseline Comparison Notes

Expected for Nash Automation A:
- all-lifestyle format ✅
- `nash-lifestyle` for hook and all slides ✅
- overlay ON ✅
- hook overlay ON ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- no token tickers in visible hooks ✅
- no hype words in visible hooks ✅
- dry/contrarian voice ✅

Potential issue:
- `Post as draft` is ON, which blocks Auto-music. This is compatible with manual warm-up posting, but it does not match fully autonomous runtime if the goal is direct scheduled posting with TikTok auto-music.
- Captions use five hashtags. Baseline only requires captions under 80 characters; hashtags may push captions longer and may read less premium. Needs later review against actual performance.
