# App Marketing OS — Competitor Ad Intelligence

## Purpose
Use competitor ad libraries as a read-only creative intelligence layer for app marketing.

This is not an ad-buying system. It does not connect ad accounts, create campaigns, change budgets, upload creatives, or touch spend.

## When to Use
Use after the measurement loop has enough baseline data, or when preparing a launch/SEO/directory push for an active app.

Best use cases:
- Extract hooks competitors are paying to test.
- Identify repeated offers/CTAs.
- Find visual frames and landing-page patterns.
- Validate whether a niche has paid demand.
- Improve organic TikTok/X/Reddit/landing-page copy with proven angles.

## Sources
Primary:
- Meta Ad Library / Meta Ads MCP / Pipeboard if available in read-only mode.

Secondary:
- TikTok Creative Center if accessible.
- Google Ads Transparency Center if relevant.
- Competitor landing pages and app-store listings.

## Product Lenses

### Vista
Look for:
- movie recommendation apps
- social movie apps
- watchlist apps
- dating/friend compatibility apps using taste matching
- entertainment discovery apps

Extract:
- taste compatibility hooks
- “what should I watch?” hooks
- social proof / friend comparison framing
- app-store screenshot patterns
- CTAs that create curiosity rather than generic download pushes

Avoid:
- copying Letterboxd positioning directly
- overclaiming recommendation accuracy

### Nash Satoshi
Use carefully because crypto ads are restricted.

Look for:
- portfolio-risk tools
- AI investing tools
- market research tools
- fintech dashboards
- crypto education tools, not token shills

Extract:
- methodology framing
- risk/uncertainty language
- dashboard proof frames
- ranking/scorecard CTAs

Avoid:
- price prediction
- return promises
- token promotion language

### Glow Index
Use once active.

Look for:
- skincare quiz ads
- ingredient checker ads
- dupe finder ads
- beauty scoring/ranking tools
- influencer-skeptic angles

Extract:
- ingredient skepticism hooks
- “before you buy” CTAs
- visual proof patterns
- quiz/diagnostic funnels

Avoid:
- medical claims
- dermatologist-like authority unless true

### Action Arena
Use later, after landing/waitlist exists.

Look for:
- fantasy football tools
- sportsbook education products
- bankroll trackers
- sports contest games
- pick’em games

Extract:
- competition hooks
- fake-money/no-risk phrasing
- league/social mechanics
- football-season urgency

Avoid:
- real-money gambling promises
- betting advice claims

## Output Format
For each ad-intel pass, write:

```md
# Competitor Ad Intel — [Product] — YYYY-MM-DD

## Sources checked
- [source/url/query]

## Repeated hooks
- Hook: ...
  - Seen in: ...
  - Transferable to JT app? yes/no
  - Suggested organic adaptation:

## Offers / CTAs
-

## Visual frames
-

## Landing page patterns
-

## What to test next
1.
2.
3.

## What NOT to copy
-
```

Save reports under:
`memory/app-marketing/competitor-intel/YYYY-MM-DD-[product].md`

## Guardrails
- Read-only only.
- No account connections unless JT explicitly approves.
- No spend or campaign creation.
- Do not copy competitor creative directly.
- Use patterns, not plagiarism.
- Treat ads as evidence of paid testing, not proof of organic performance.

## Priority
Current priority: staged, not skipped.

Order:
1. Finish automated metrics baseline.
2. Use ReelFarm/Social Growth Engineers trend intelligence continuously for TikTok.
3. Run competitor ad intel before major launch/SEO/directory pushes or when a product has weak hooks.
4. Only then consider ad-platform integrations beyond read-only research.
