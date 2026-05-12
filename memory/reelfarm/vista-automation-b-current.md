# Vista ReelFarm Automation B — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/vista-automation-b/`.
Extraction: OpenClaw image tool after image/OCR fix.

## Screenshot Files

1. `memory/reelfarm/screenshots/vista-automation-b/01.jpg`
2. `memory/reelfarm/screenshots/vista-automation-b/02.jpg`
3. `memory/reelfarm/screenshots/vista-automation-b/03.jpg`
4. `memory/reelfarm/screenshots/vista-automation-b/04.jpg`
5. `memory/reelfarm/screenshots/vista-automation-b/05.jpg`
6. `memory/reelfarm/screenshots/vista-automation-b/06.jpg`
7. `memory/reelfarm/screenshots/vista-automation-b/07.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (9)`
- Hook count: 9
- Visible hooks:
  - “Rating every film I watched this year on VISTA.”
  - “My top 10 films on VISTA. Judge me.”
  - “I've been rating films on VISTA for a year. Here's what I learned about my taste.”
  - “My VISTA profile after rating 400 films.”
  - “How I rate films on VISTA, explained in 5 slides.”
  - “VISTA said I'm a tough critic. I've given exactly 3 films a 90+. It's right.”
  - “My top 10 on VISTA says more about me than my therapist does.”
  - “My VISTA profile after a year of rating. Judge me accordingly.”
  - “My average score on VISTA is 72. Apparently that makes me a tough critic.”

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style white_background. Hook should feel personal and conversational, like texting a friend a hot take. When Vista scores (numbers 1-100) or Taste Titles (in quotes) appear, keep them as-is for readability. Body slides 2-5: no overlay text — the Vista app screenshots carry all the information on their own.

### Text Content — Settings Beta

- Hook text only: ON
- No text: OFF
- Product context: `No product context`

### Image Content

- Hook collection: `vista-lifestyle`
- All Slides collection: `vista-screenshots`
- Hook Slide Grid: `Single`
- Body Slides Grid: `Single`
- Auto-images: OFF
- Repeat hook image: OFF
- Force CTA slide: OFF
- Keep original aspect ratio: OFF
- Enable overlay: OFF
- Enable overlay on hook image: ON
- Aspect ratio: `9:16`

### TikTok Settings

- Auto-post to TikTok: ON
- TikTok account: `@mashed386`
- Display name: `MASHED`

Title:
- Use prompt: ON
- Prompt: “Match the text on the first slide exactly, in sentence case. Do not add anything.”

Caption:
- Use prompt: ON
- Prompt: “Write one short line (under 50 characters) that teases the hook without giving it away, sounding like a friend texting a take. Then on a new line, add these 4 hashtags: #movietok #filmtok #letterboxd #vista. No exclamation points. No emojis. Nothing else.”

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
- Overlay opacity not visible because body overlay is off.
- Export-as-video global setting not directly visible, though slideshow is selected and video publish is disabled.

## Baseline Comparison Notes

Expected for Vista Automation B:
- lifestyle hook + screenshots format ✅
- `vista-lifestyle` hook collection ✅
- `vista-screenshots` all-slides collection ✅
- hook text only ON ✅
- body overlay OFF ✅
- hook overlay ON ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- screenshot-compatible “explained in 5 slides” style hooks present ✅

Potential issues:
- Hooks render Vista as `VISTA`, which conflicts with the baseline proper-case rule: use `Vista`, never all caps.
- `Post as draft` is ON, which blocks Auto-music. Compatible with manual warm-up, not fully autonomous runtime with auto-music.
- Captions use four hashtags; may exceed under-80-char caption constraint and feel less native/premium.
