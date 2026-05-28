# ReelFarm App Profiles

Updated: 2026-05-11
Source: JT direct explanation. Screenshots are the source of truth for current ReelFarm settings.

## Current Operational Status

All six automations are currently paused.

Source recovery protocol:
`memory/reelfarm/manual-post-recovery-protocol-2026-05-26.md`

Reason:
- Vista and Nash Satoshi had recent posts getting 0 views.
- Vista posts were going out silent, with no audio attached.
- TikTok account checks show no violations or eligibility issues; accounts are in good standing.
- Likely causes: new-account cold-start distribution, lack of human-pattern engagement signals, and Vista silent slideshows being suppressed.
- Glow Index automations are configured but have not yet been activated.

Recovery plan:
1. Manual posting from TikTok app on each account: 2-3 posts each, sounds picked by hand.
2. Daily account engagement during warm-up: scroll, like, comment in niche.
3. Prefer ReelFarm draft generation/upload when possible; JT manually reviews/posts from TikTok.
4. Restart automations at reduced frequency: 1 post per week per account after warming.
5. Scale frequency back up only after 24h/72h/7d metrics show normal distribution for 2-3 weeks.

## Universal Automation A/B Settings

| Setting | Automation A — all-lifestyle | Automation B — lifestyle hook + screenshots |
|---|---|---|
| Hooks list | App-specific hooks naming products/features/scores | Generic hooks compatible with random screenshots, especially “explained in 5 slides” |
| Hook collection | `{app}-lifestyle` | `{app}-lifestyle` |
| All slides collection | `{app}-lifestyle` | `{app}-screenshots` |
| Format instructions | Hook slide and body slides | Hook slide only |
| Enable overlay | ON | OFF |
| Enable overlay on hook image | ON | ON |
| Overlay opacity | 25–35%, depending on photo brightness | 25–35%, affects hook only |
| `text_on_first_slide_only` | OFF | ON |
| Auto-post to TikTok | ON | ON |
| Export as video | OFF | OFF |
| Auto-music | ON | ON |

## Vista

Product:
Social movie-rating app with a 1–100 precision scale, automatically generated personality labels called Taste Titles, and friend compatibility scoring. Vista is not an AI recommendation engine. It positions movie taste as identity and social currency. Letterboxd-adjacent.

TikTok account: `@mashed386`

Audience:
Late-20s to 30s aesthetic-conscious viewers who watch movies socially. Letterboxd users, A24 enthusiasts, Criterion Collection types, and people who treat film taste as identity.

Voice:
Warm, slightly literary, self-aware, specific. Like someone roasting their own taste at a dinner party.

Signature hook devices:
- Compatibility drama with a named person.
- Taste Title identity callouts.
- Rating-as-content lists.
- “Explained in 5 slides” for Automation B.

Examples:
- “Me and my boyfriend are 34% compatible on Vista. We're doing couples counseling now.”
- “Vista gave me the Taste Title ‘Drama Devotee’ and I'm offended.”
- “I rated every Christopher Nolan film on Vista. Oppenheimer didn't crack the top 3.”

Voice DOs:
- Reference specific Vista features naturally: “on Vista,” “my Vista profile,” “my Taste Title.”
- Use the 1–100 scale precisely, e.g. “The Godfather 94,” not “amazing.”
- Be self-deprecating about taste.
- Treat compatibility scores as relationship drama.

Voice DON'Ts:
- Marketing language like “download now” or “best app for.”
- Generic movie recommendations without Vista context.
- All-caps brand rendering.

Image collections:
- `vista-lifestyle`: cozy movie-watching aesthetic — dimly lit home theaters, TVs glowing in dark rooms, popcorn on couches, blanket forts, late-night screenings.
- `vista-screenshots`: Vista app screenshots — taste profile pages, compatibility score views, film rating screens, Taste Title displays.

Schedule when scaled:
- Automation A: `0 16 * * 0,2` — Sunday + Tuesday 4pm PT / 7pm ET.
- Automation B: `0 17 * * 4` — Thursday 5pm PT / 8pm ET.

## Nash Satoshi

Product:
4-LLM crypto token analysis platform that scores tokens 0–100 across six dimensions: Coordination, Schelling Rank, Reflexivity, Virality, Asymmetry, and Game Theory. Uses ChatGPT-5.4, Claude Opus 4.6, Gemini 3.1 Pro, and Grok 4. Tier grades S+, S, A, B, C. Phase Detection lifecycle: Stealth, Expansion, Mania, Distribution, Dead. Free during beta; paid SaaS planned.

TikTok account: `@nashsatoshi`

Audience:
Crypto-burned retail traders age 25–40 who are skeptical of Crypto Twitter hype cycles and want sharper analytical frameworks. Game-theory-curious, tired of losing money on momentum trades.

Voice:
Analytical, contrarian, dry, with attitude. Skeptical of crypto hype, confident in the framework. Treats the reader as someone who has lost money and wants better tools. No hype language.

Signature hook devices:
- Exit liquidity accusation.
- Phase Detection language.
- Tier-based authority claims.
- Framework-as-edge.
- “Explained in 5 slides” for Automation B.

Examples:
- “You're not buying the bottom. You're exit liquidity.”
- “This token is in Distribution phase. The chart looks bullish. It isn't.”
- “Only 11 out of 279 tokens hit S+ tier this week.”
- “Asymmetry is worth 25 points out of 100. Most traders optimize for zero of them.”

Banned language:
- “Moon,” “gem,” “10x,” “100x,” “to the moon.”
- “Ape in,” “send it,” rocket emojis.
- Specific token tickers.
- Specific scores tied to real tokens.
- “This is not financial advice.”

Image collections:
- `nash-lifestyle`: cyberpunk trader workspace aesthetic — multiple-monitor setups, RGB-lit desks, Bloomberg-terminal-style screens, late-night trading environments, dim workstations.
- `nash-screenshots`: Nash Satoshi screenshots — rankings leaderboard, six-dimension score breakdown, tier system explanation, “Find Asymmetric Plays / Avoid Exit Liquidity,” 4-AI consensus visualization.

Schedule when scaled:
- Automation A: `30 5 * * 1` + `0 16 * * 0` — Monday 5:30am PT + Sunday 4pm PT.
- Automation B: `0 8 * * 4` — Thursday 8am PT.

## Glow Index

Product:
4-AI skincare product analysis platform. Scores products on ingredient efficacy, value, and formulation across six dimensions. Catches the gap between marketing claims and chemistry. Tier grades S+, S, A, B, C.

URL: `https://glowindex.co`
TikTok account: dedicated Glow Index account; exact handle pending from screenshots or JT.

Audience:
Ingredient-literate women age 22–40 skeptical of influencer marketing. They have overspent on hyped products, read ingredient labels, and want analysis grounded in data instead of aesthetics.

Voice:
Friend spilling secrets over coffee. Slightly skeptical of skincare marketing, friendly, specific. Not clinical, not preachy. Faceless brand voice, not founder voice. It should never read as a male founder speaking; it should read as a knowledgeable friend in the audience demographic.

Signature hook devices:
- Price exposés.
- Dupe reveals.
- Influencer disagreement callouts.
- Brand-name callouts.
- Ingredient-level callouts.

Examples:
- “This $215 moisturizer scored a 45 out of 100.”
- “The $12 serum that outscored luxury brands in 4-AI testing.”
- “4 AIs disagreed with every skincare influencer on this product.”

Brand/ingredient rule:
Brand names and ingredients are allowed because they remain stable. Examples: Drunk Elephant, La Mer, CeraVe, retinol, niacinamide, hyaluronic acid.

Image collections:
- `glow-lifestyle`: clean skincare-girlie aesthetic — bathroom flat lays on marble, vanity setups with soft lighting, hands holding skincare bottles, products on windowsills with morning light, cotton pads/tools, minimalist clean-girl aesthetic.
- `glow-screenshots`: Glow Index screenshots — rankings page, product detail pages, Score Breakdown, How It Works methodology, Top Rated Products, AI Consensus view.

Schedule when scaled:
- Automation A: `0 6 * * 0` + `0 16 * * 4` — Sunday 6am PT + Thursday 4pm PT.
- Automation B: `0 12 * * 2` — Tuesday 12pm PT.
