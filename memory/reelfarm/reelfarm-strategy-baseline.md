# ReelFarm Strategy Baseline

Updated: 2026-05-11
Source: JT direct explanation in Telegram. Screenshots are the source of truth for current configuration; this document is the source of truth for rationale, constraints, and operating logic.

## What ReelFarm Is Used For

ReelFarm is the automated TikTok slideshow generation and posting platform used on the Growth tier for three apps:

- Vista — movie taste rating
- Nash Satoshi — crypto game theory analysis
- Glow Index — skincare product analysis

Each app has a dedicated TikTok account and a pair of automations running on complementary schedules.

ReelFarm handles runtime end-to-end:

- image rotation from curated collections
- hook rotation from configured hook lists
- text overlay rendering
- caption generation from prompts
- direct API posting to TikTok on scheduled cron times

JT does not manually produce individual posts. Automations are configured once and generate three slideshow posts per app per week autonomously.

## Output Format

Required format:

- Native TikTok photo slideshow
- Never video export
- 9:16 aspect ratio
- TikTokDisplay-Bold font

Rationale: TikTok photo slideshows currently get materially higher organic reach than videos, roughly 3–10x in JT's observed results. TikTokDisplay-Bold matches the Classic TikTok aesthetic.

## Two-Automation Pattern

Each app has exactly two automations running simultaneously.

### Automation A — all-lifestyle

- All five slides use lifestyle photos from a curated collection matching the app aesthetic.
- Every slide carries text overlay.
- Photos are decorative, not informational.
- Text does the storytelling work.
- Purpose: top-of-funnel brand identity and value content.
- Cadence: 2 posts per week per app.

### Automation B — lifestyle hook + screenshots

- Slide 1 is a lifestyle photo with hook text overlay.
- Slides 2–5 are clean app screenshots from a separate screenshots collection.
- Screenshot slides have no text overlay because the product visuals tell the story.
- Purpose: mid-funnel product comprehension and conversion.
- Cadence: 1 post per week per app.

### Weekly Volume

- 3 posts per app per week.
- 3 apps total.
- 9 TikTok slideshow posts per week.

## Funnel Logic

The A/B split exists because each format serves a different funnel role:

- All-lifestyle = top-of-funnel pure value content and audience building.
- Lifestyle hook + screenshots = mid-funnel product understanding after hook interest.

Do not recommend killing either format. Removing one breaks the funnel.

## Universal Format Constraints

These apply across all three apps and are non-negotiable.

- TikTokDisplay-Bold font only.
- 9:16 aspect ratio.
- Native TikTok photo slideshow, never video export.
- Hook slides: 8–14 words maximum.
- Body slides: 8–15 words maximum.
- Captions: under 80 characters.
- No exclamation points in text overlays.
- No emojis in text overlays.
- One subtle emoji in captions is acceptable for Glow Index only.
- Brand names rendered in proper case: Vista, Nash Satoshi, Glow Index.
- No fabricated personal relationships in hooks. No fake “my sister” or “my brother-in-law.”
- Nash Satoshi: no specific token tickers because information ages too fast for evergreen content.
- Glow Index: specific brand names and ingredients are allowed because brands/ingredients are stable for years.

Available but rarely used fonts:

- BebasNeue-Regular
- CormorantGaramond-Regular
- CormorantGaramond-Italic

## Larry Framework

Observed winning hook pattern:

> another person + conflict + reveal

This framework outperformed feature-forward hooks by roughly 250x in JT's data sample.

Use this as the primary hook-evaluation lens for ReelFarm content recommendations unless app-specific evidence contradicts it.

## Hook Strategy — Larry Framework vs Feature-Forward

Feature-forward hooks describe the product, e.g. “This app rates movies on a 1-100 scale.”

Larry-framework hooks describe a human situation that happens to involve the product, e.g. “Me and my boyfriend are 34% compatible on Vista. We're doing couples counseling now.” The product enters through the back door.

When recommending hooks, favor another person + conflict + reveal over generic feature claims. Not every hook needs this pattern, but hook lists weighted toward it outperform feature-forward framing.

## Universal App Pattern for New Apps

Each new app should eventually get the same ReelFarm A/B structure:

- Product description
- Audience
- Voice
- Signature hook devices
- Banned language
- Image collections: lifestyle + screenshots
- Schedule
- Automation A: all-lifestyle, 2x/week when scaled
- Automation B: lifestyle hook + screenshots, 1x/week when scaled

Apps can be paused or sunset without breaking the review system by updating the status in `memory/reelfarm/apps.md`.
