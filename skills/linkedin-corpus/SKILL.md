---
name: linkedin-corpus
description: "Use when JT provides LinkedIn posts, screenshots, accounts, or asks to improve LinkedIn swipe coverage, creator targets, viral pattern extraction, or the LinkedIn content corpus."
---

# LinkedIn Corpus

Use this to convert LinkedIn examples into reusable content intelligence.

## Inputs
- Post URLs, account URLs, screenshots, copied post text, or creator names.
- Optional lane hints from `memory/content/current-niche-map.md`.

## Workflow
1. Load `memory/content/current-niche-map.md` and select the exact canonical lane.
2. Extract only observable mechanics:
   - source URL or screenshot path
   - creator/account
   - platform: LinkedIn
   - canonical niche lane
   - format
   - hook mechanic
   - opening-line mechanic
   - proof mechanism
   - emotional driver
   - specificity level
   - CTA type
   - why it worked
   - JT translation
3. Save high-quality examples to Notion Viral Post Swipe with `scripts/notion-swipe-push.py`.
4. Update or create:
   - `memory/content/linkedin-creator-targets.json`
   - `memory/content/linkedin-pattern-library.md`
5. Reject weak examples. Do not preserve generic motivation, guru tone, vague AI hype, or posts that cannot translate into JT's practical operator voice.

## Quality Bar
- Prioritize Tier 1/Tier 2 lanes from the niche map.
- The corpus is not optimized until it has at least 5 relevant creators/accounts and 30 usable posts.
- Product/app examples are allowed only when they support a current app marketing objective.
- X examples do not substitute for LinkedIn examples.

## Output
Return:
- accepted examples count
- rejected examples count and why
- files updated
- remaining corpus gap by lane

