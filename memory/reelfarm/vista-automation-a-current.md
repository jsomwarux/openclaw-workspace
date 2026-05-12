# Vista ReelFarm Automation A — Current Settings

Updated: 2026-05-11
Source of truth: screenshots sent by JT, saved in `memory/reelfarm/screenshots/vista-automation-a/`.
Extraction: OpenClaw image tool after image/OCR fix.

## Screenshot Files

1. `memory/reelfarm/screenshots/vista-automation-a/01.jpg`
2. `memory/reelfarm/screenshots/vista-automation-a/02.jpg`
3. `memory/reelfarm/screenshots/vista-automation-a/03.jpg`
4. `memory/reelfarm/screenshots/vista-automation-a/04.jpg`
5. `memory/reelfarm/screenshots/vista-automation-a/05.jpg`
6. `memory/reelfarm/screenshots/vista-automation-a/06.jpg`

## Extracted Current Settings

### Text Content — Hooks

- Selected tab: `Hooks (14)`
- Hook count: 14
- Helper text: each line is a separate hook
- Visible hooks:
  - “Me and my boyfriend are 34% compatible on Vista. We're doing couples counseling now.”
  - “My best friend and I are 91% compatible on Vista. I'm starting to think we share a brain.”
  - “I made my dad join Vista. Turns out our taste overlap is 12%. I have questions.”
  - “My girlfriend's Taste Title is "Rom-Com Devotee." Mine is "Slow Cinema Snob." We're doomed.”
  - “My situationship and I are 78% compatible on Vista. So why won't he commit.”
  - “Vista gave me the Taste Title "Thriller Connoisseur" and I've never felt more seen.”
  - “My Taste Title on Vista is "Drama Devotee" and I'm genuinely offended.”
  - Partial/uncertain lower hook: “Vista said I'm a trash critic. I'm giving myself 2 films...”

### Text Content — Format Instructions

Visible text:

> Slide 1: one text item centered, font TikTokDisplay-Bold, size extra_large, text_style white_background. Hook should feel personal and conversational, like texting a friend a hot take. When Vista scores (numbers 1-100) or Taste Titles (in quotes) appear, keep them as-is for readability. Render "Vista" with only the first letter capitalized, never as all caps.
>
> Body slides 2-5: one text item at bottom position, font TikTokDisplay-Bold, size medium, text_style white_background. Each body text is a short specific statement — a movie title with its Vista score (e.g. "The Godfather - 94"), a compatibility data point (e.g. "Dune: he gave it 67, I gave it 89"), or a Taste Title detail. Each body slide should build on the hook's story — slides 2-4 deliver specific proof or details that support the hook, slide...

Prompt text continues below visible area.

### Image Content

- Hook collection: `vista-lifestyle`
- All Slides collection: `vista-lifestyle`
- Hook Slide Grid: `Single`
- Body Slides Grid: `Single`
- Auto-images: OFF
- Repeat hook image: OFF
- Force CTA slide: OFF
- Keep original aspect ratio: OFF
- Enable overlay: ON
- Enable overlay on hook image: ON
- Aspect ratio: `9:16`
- Overlay opacity: `30%`

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
- Auto-music: OFF / disabled because posting as draft cannot auto-add music
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

Expected for Vista Automation A:
- all-lifestyle format ✅
- `vista-lifestyle` for hook and all slides ✅
- overlay ON ✅
- hook overlay ON ✅
- 9:16 ✅
- TikTokDisplay-Bold ✅
- Larry-framework hooks weighted heavily ✅
- no all-caps Vista ✅

Potential issues:
- `Post as draft` is ON, which blocks Auto-music. This is compatible with manual warm-up posting but not fully autonomous runtime with auto-music.
- Captions use four hashtags, which may push the caption above the under-80-char constraint and make it feel less native/premium. Needs performance review.
