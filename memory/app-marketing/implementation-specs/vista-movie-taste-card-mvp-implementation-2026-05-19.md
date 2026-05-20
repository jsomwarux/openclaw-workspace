# Vista — Movie Taste Card MVP Implementation Plan
Date: 2026-05-19
Status: build-ready handoff, source repo not found on Mac mini

## Verdict
Build the Vista share artifact as the next product-led acquisition unlock, but do **not** assign coding until the iOS source repo/location is confirmed. The local Mac mini search did not surface a Vista Xcode/Swift project under known project paths; current available assets are App Store/site screenshots only.

## Product Goal
Create a shareable card after a user rates 25 movies:

`rate 25 movies → generate Movie Taste Card → save/share → friend compares or installs`

## Required User-Facing Feature
### MVP: Movie Taste Card
Trigger: user has rated at least 25 movies.

Card formats:
- square 1080x1080
- vertical 1080x1920

Card content:
1. Vista logo/name
2. user display name or handle
3. rating count/date
4. taste archetype
5. average rating / rating strictness / rating spread
6. top four by actual 1-100 rating
7. taste tension line
8. CTA: `Rate 25 movies to make yours` or `Compare your taste in Vista`

## Data Requirements
Minimum local app data:
- user id
- user display name
- rated movie IDs
- rating values 1-100
- movie title/year/poster metadata
- rating timestamp

Nice-to-have later:
- genre/tag aggregates
- external average ratings if license-safe
- friend comparison table
- share attribution/deep links

## Implementation Approach
Because this is iOS, preferred implementation is native SwiftUI image rendering.

Recommended architecture:
1. `TasteCardModel`
   - derived from local ratings
   - stores archetype, top four, rating summary, tension line
2. `TasteCardView`
   - SwiftUI card view sized for square and vertical export
3. `TasteCardRenderer`
   - renders SwiftUI view to PNG using `ImageRenderer` on iOS 16+
   - fallback: `UIGraphicsImageRenderer` if needed
4. `ShareTasteCardButton`
   - appears when user reaches 25 ratings
   - opens native share sheet with generated PNG + caption
5. Deep link / source tag if available
   - `vista_card_export_movie_taste`
   - invite link if app already supports it

## Archetype Logic MVP
Use deterministic rules, not LLM calls.

Inputs:
- average rating
- standard deviation / rating spread
- top genres if available
- number of very high ratings, e.g. 90+
- number of low ratings, e.g. below 40

Example rules:
- high average + low variance → `Generous Curator`
- low average + high variance → `Selective Contrarian`
- high variance + many 90+ → `Chaos With Standards`
- genre-heavy top four → `[Genre] Loyalist`

## Acceptance Criteria
- User with fewer than 25 ratings does not see share prompt.
- User with 25+ ratings can generate square PNG.
- Generated PNG includes real movie titles and ratings, not placeholder data.
- Share sheet opens successfully on iOS.
- Card contains no fake compatibility claims.
- Card can be saved to camera roll.
- Build passes Xcode compile/tests.

## Manual/JT Blocker
Need exact Vista source repo/project location before implementation.

JT task should ask for one of:
- GitHub repo link
- local project path
- TestFlight/App Store Connect project source location
- confirmation that coding must happen on laptop instead of Mac mini

## References
- `memory/app-marketing/share-artifacts/vista-movie-taste-card-spec-2026-05-19.md`
- `memory/app-marketing/competitor-intel/vista-movie-app-teardown-2026-05-19.md`
- `memory/app-marketing/outreach-packs/vista-borrowed-audience-pack-2026-05-19.md`
