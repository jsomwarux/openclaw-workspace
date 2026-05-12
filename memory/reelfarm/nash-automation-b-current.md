# Nash Satoshi ReelFarm Automation B — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/nash-automation-b/`.
Extraction: OpenClaw image tool.

## Screenshot Files

1. `memory/reelfarm/screenshots/nash-automation-b/01.jpg`
2. `memory/reelfarm/screenshots/nash-automation-b/02.jpg`
3. `memory/reelfarm/screenshots/nash-automation-b/03.jpg`
4. `memory/reelfarm/screenshots/nash-automation-b/04.jpg`
5. `memory/reelfarm/screenshots/nash-automation-b/05.jpg`
6. `memory/reelfarm/screenshots/nash-automation-b/06.jpg`
7. `memory/reelfarm/screenshots/nash-automation-b/07.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (15)`
- Hook count: 15
- Helper text: each line is a separate hook
- Visible hooks:
  - “How I rank crypto tokens using 4 AIs, explained in 5 slides.”
  - “What Nash Satoshi actually measures, in 5 slides.”
  - “Why I stopped trusting crypto Twitter and built this instead, in 5 slides.”
  - “4 AIs, 6 scoring dimensions, one score. Here's how it works.”
  - “The framework I use to avoid exit liquidity, in 5 slides.”
  - “I built a tool that runs crypto tokens through 4 AI models. Here's what you actually see.”
  - “I got tired of losing money on crypto Twitter hype. So I built this.”
  - “What it looks like when 4 AIs disagree on a token. The disagreement IS the signal.”
  - “I ran 279 tokens through 4 AIs. This is what the output looks like.”
  - “The 6 dimensions every token should be scored on. Most crypto tools only measure one.”
- More hooks may exist below scroll.

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style black_background. Keep hook to 10-16 words maximum. Hook should feel contrarian and analytical with a touch of attitude. Render "Nash Satoshi" with proper capitalization.
>
> Body slides 2-5: no overlay text. The Nash Satoshi platform screenshots carry all the information on their own. Viewers see the actual tool — the rankings page, the scoring breakdowns, the tier system — which demonstrates the product visually better than any text overlay could.
>
> Tone on the hook slide is analytical with attitude — skeptical of crypto hype, confident in the framework. No exclamation points, no emojis, no hype language like "secret" or "insane"...

Prompt may continue below visible area.

### Text Content — Settings Beta

- Hook text only: ON
- No text: OFF
- Product context: `No product context`

### Image Content

- Hook collection: `nash-lifestyle`
- All Slides collection: `nash-screenshots`
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
- Visible prompt: “Write one short line (under 50 characters) that states the core analytical finding with a touch of attitude, then on a new line add these 5 hashtags: #crypto #altcoins #cryptotok #gametheory #cryptotwitter. No exclamation points. No emojis. No hype words.”
- Caption prompt may continue below visible area.

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

Expected for Nash Automation B:
- lifestyle hook + screenshots format ✅
- `nash-lifestyle` hook collection ✅
- `nash-screenshots` all-slides collection ✅
- hook text only ON ✅
- screenshot body text OFF ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- no specific token tickers in visible hooks ✅
- no banned moon/gem/10x hype in visible hooks ✅

Potential issues:
- Prompt says hook max is 10–16 words, but universal baseline says hook slides should be 8–14 words. Tighten to 8–14 unless there is performance evidence for Nash B needing longer hooks.
- `Enable overlay` is ON while body slides are screenshots. Baseline says Automation B body overlay should be OFF so screenshots stay clean and legible; only hook overlay should be ON. Need verify whether ReelFarm's hook-text-only prevents body overlay from applying. If not, turn global overlay OFF and keep hook overlay ON.
- `Post as draft` is ON, which blocks Auto-music. Compatible with manual warm-up, not fully autonomous runtime with auto-music.
- Captions use five hashtags; may exceed under-80-char caption constraint and feel less native/premium.
- Several hooks are feature/build-forward (“I built a tool...”), less Larry-framework/human-conflict oriented. For Automation B this is acceptable in moderation, but hook list may need more trader pain/conflict hooks.
