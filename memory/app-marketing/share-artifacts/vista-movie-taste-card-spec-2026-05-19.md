# Vista Movie Taste Card Spec
Date: 2026-05-19
App: Vista
Owner: Eve / JT
Status: product-led acquisition artifact spec

## Strategic Verdict
Vista should not lead with “another movie tracker” or “Letterboxd killer.” The strongest low-cost acquisition wedge is **movie taste identity**: a share card that lets someone show what their ratings say about them, then invite a friend to compare.

The artifact should make the user look **tasteful, funny, precise, and socially legible**. A card that says “I rated movies” is weak. A card that says “my movie taste is emotionally specific and my friend is only 34% compatible with me” has a reason to travel.

## Source Signals
- Letterboxd’s homepage and App Store listing emphasize social film discovery, logging, lists, reviews, friends, and 5-star ratings. Source: https://letterboxd.com/ and https://apps.apple.com/us/app/letterboxd/id1054271011
- Letterboxd reports massive visible activity on its homepage, including billions of films watched, and foregrounds likes/views/reviews as social proof. Source: https://letterboxd.com/
- Letterboxd App Store Editors’ Choice copy says the first thing people want after a movie is to talk about it, and highlights sharing lists/reviews and commenting on friends’ updates. Source: https://apps.apple.com/us/app/letterboxd/id1054271011
- Reddit searches show repeated demand for similar-taste discovery, compatibility, recommendations from top four favorites, and stats/visualizations based on Letterboxd profiles. Sources: https://www.reddit.com/r/Letterboxd/comments/lp06yi/what_would_you_like_to_see_in_a_film_taste/ and https://www.reddit.com/r/Letterboxd/comments/1chpa9i/letterboxd_movie_recommendations_and_statistics/
- FilmTok/Letterboxd behavior uses four favorites/top-four identity as a recommendation and social prompt. Source example surfaced by search: https://www.tiktok.com/@letterboxd/video/7543264757587954975
- Prior Vista performance note: taste compatibility hooks beat pure precision-rating posts. Local context: `memory/app-marketing/competitor-intel/2026-05-06-vista-nash.md`.

## Artifact Name
**Vista Movie Taste Card**

Secondary public label: **Your Movie Taste, Scored Precisely**

## Core User Promise
“Rate movies from 1–100. Vista turns your ratings into a taste profile you can share or compare with a friend.”

## Formats
1. **Square card**: 1080x1080 for X, Instagram feed, Reddit image posts.
2. **Vertical card**: 1080x1920 for TikTok slideshow, IG Story/Reels cover, Shorts.
3. **Compact image**: 1200x630 OG/social preview if used on web landing pages.

## MVP Card Modules
### 1. Header
- Vista logo/name.
- User display name or handle.
- Date/rating count.
- Microcopy: “Movie Taste Card” or “My Movie Taste”.

### 2. Taste Archetype
Generate one taste identity from ratings. Keep it playful, not pseudo-scientific.

Examples:
- “The Prestige Romantic”
- “Chaos With Standards”
- “Comfort Rewatch Maximalist”
- “A24 With Popcorn Taste”
- “Highbrow Crowdpleaser”
- “Bleak But Selective”
- “Sentimental Contrarian”

Rule: archetype must be derived from actual rating patterns: genre clusters, average rating, variance, top-rated films, polarizing films, rewatch/comfort flags if available.

### 3. Precision Rating Snapshot
Show 3–5 concrete data points:
- Average rating: `78/100`
- Rating strictness: `Tough grader` / `Generous critic` / `Polarized`
- Highest-rated genre/tag: `Noir: 88 avg`
- Most divisive rating: `You rated [Movie] 92 when average is 71` if external average exists
- Rating spread: `Lowest 22 / Highest 98`

If external averages are unavailable, use only within-user patterns.

### 4. Top Four by Actual Rating
A clean poster grid or text list:
- `1. Movie — 97`
- `2. Movie — 94`
- `3. Movie — 93`
- `4. Movie — 91`

This borrows the familiar “four favorites” behavior without copying Letterboxd’s exact framing.

### 5. Taste Tension Line
One social sentence designed to be screenshot-worthy:
- “Five stars would hide how picky I actually am.”
- “Apparently I trust vibes more than consensus.”
- “My taste says comfort movie, my ratings say courtroom drama.”
- “I rate crowdpleasers harder than slow sad movies.”

### 6. CTA Footer
- Primary: “Compare your taste in Vista”
- Secondary: “Rate 25 movies to make yours”
- Optional QR/deep link if used in web exports.

## Compatibility Variant
This is the highest-share variant once friend graph or invite flow exists.

### Card Name
**Movie Taste Compatibility Card**

### Required Inputs
- User A ratings.
- User B ratings OR friend invite pending.
- Shared watched films count.
- Rating distance across shared films.
- Shared favorites overlap if available.

### Main Metrics
- Compatibility score: `34% movie match`
- Shared watched films: `18 films in common`
- Biggest agreement: `[Movie] — both 91+`
- Biggest disagreement: `[Movie] — 92 vs 41`
- Taste label: `Perfect movie-night chaos` / `Dangerous double feature` / `Same taste, different standards`

### Guardrails
- Do not imply relationship compatibility or romantic claims as fact.
- Keep it playful: “movie match,” “taste match,” “movie-night risk.”
- Avoid fake friend comparisons in public assets. Use demo names or mark as sample.

## Export UX
### Trigger Points
1. After user rates 25 movies: “Your taste card is ready.”
2. After user rates 100 movies: “Your taste profile got sharper.”
3. After friend comparison: “You and [friend] are [X]% movie-compatible.”
4. End-of-month recap: “Your May movie taste.”

### Share Actions
- Save image.
- Share to Instagram/TikTok/X.
- Copy invite link.
- Copy caption.

### Suggested Auto-Captions
- “I rated movies out of 100 and apparently this is my taste.”
- “Five stars were hiding too much.”
- “Drop your top 4 and I’ll compare taste.”
- “My movie taste card is more accurate than my dating profile.”
- “I need someone with higher compatibility than this.”

## Design Direction
- Dark cinematic background, but avoid generic streaming-app black gradients.
- Poster grid + bold numeric ratings should be the visual hook.
- Typography: clean, high-contrast, slightly editorial.
- Use one accent color per archetype.
- Let the number scale own the differentiation: `97/100`, not stars.

## Data Model Requirements
Minimum:
- User ID / display name.
- Rated movie IDs.
- Rating values 1–100.
- Rating timestamps.
- Movie poster/title/year/genre metadata.

Preferred:
- Friend comparison table.
- Genre/tag aggregates.
- External average rating source if license-safe.
- Share event table: artifact type, source, export action, click/download attribution.

## Tracking Spine
Every exported card should attach:
- `artifact_type=movie_taste_card|compatibility_card|top_four_card`
- `share_format=square|vertical|og`
- `source_tag=vista_card_export`
- `rating_count_bucket=25|50|100|250+`
- `deep_link=/invite?source=vista_card_export&artifact=[type]`

Success metrics:
- Export rate: exports / eligible users.
- Share intent: share taps / exports.
- Invite conversion: installs from card links.
- Activation: new user rates 25 movies.

## MVP Build Recommendation
Build in this order:
1. **Static Movie Taste Card** after 25 ratings.
2. **Top Four by Actual Rating** export.
3. **Compatibility Card** with invite link.
4. Monthly recap card.

## Experiment Cards
Only experiments scoring 24+/35 are included.

## Experiment: Movie Taste Card Export Prompt

App: Vista
Date created: 2026-05-19
Owner: JT / Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://letterboxd.com/
- https://apps.apple.com/us/app/letterboxd/id1054271011
- https://www.reddit.com/r/Letterboxd/comments/1chpa9i/letterboxd_movie_recommendations_and_statistics/
Observed pattern: Film users share ratings, lists, stats, profiles, and identity artifacts. Letterboxd’s social loop is built around making film activity visible. Reddit users also seek stats/visualizations from profiles.
Proof of traction: Letterboxd shows billions of films watched and 88K App Store ratings; Reddit threads repeatedly ask for profile-based recommendations/stats.
Audience: Movie loggers, Letterboxd-adjacent users, social film fans.
Competitor/incumbent gap: Letterboxd has social scale, but its core rating expression is still 5-star/half-star. Vista can own precision + taste identity.

### Hypothesis
If we prompt users after 25 ratings to export a taste card, then some will share because the card makes their taste legible and gives friends a reason to compare.

### Asset Needed
- Creative/share artifact: square + vertical Movie Taste Card.
- Copy/hook: “Five stars were hiding too much.”
- Landing/app destination: App Store or Vista landing page with `rate 25 movies` CTA.
- Tracking link/source tag: `vista_card_export_movie_taste`.

### Distribution
Channel: in-app export, X, Instagram Story, TikTok slideshow, Reddit when value-first.
Borrowed audience target, if any: micro FilmTok creators who do rating/list content.
CTA: “Rate 25 movies to make yours.”
Run date: TBD after asset build.

### Measurement
Primary metric: export rate among users with 25+ ratings.
Secondary metric: installs/activation from shared-card links.
24h result: TBD
72h result: TBD
7d result: TBD

### Decision
Scale / iterate / kill: TBD
Reason: Run only if export rate or install-from-share signal appears.
Next action: Build static MVP generator.

### Score
Audience fit: 5
Repeatability: 5
Proof: 4
Cost: 5
Conversion intent: 3
Shareability: 5
Competition gap: 4
Total: 31/35

## Experiment: Friend Compatibility Invite Card

App: Vista
Date created: 2026-05-19
Owner: JT / Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://www.reddit.com/r/Letterboxd/comments/lp06yi/what_would_you_like_to_see_in_a_film_taste/
- https://www.reddit.com/r/Letterboxd/comments/u9qghv/is_there_a_way_to_find_people_with_similar_tastes/
- `memory/app-marketing/competitor-intel/2026-05-06-vista-nash.md`
Observed pattern: Users want to find similar tastes and compare compatibility; prior Vista note found compatibility hooks outperforming pure rating precision posts.
Proof of traction: Reddit demand appears repeatedly; prior content signal showed better performance from “34% compatible” style hooks.
Audience: Friends/couples/movie-night groups and Letterboxd users who compare taste.
Competitor/incumbent gap: Incumbents have friends/follows, but compatibility is not the default share loop.

### Hypothesis
If Vista creates a compatibility invite card, then users will invite friends because the result is only interesting if another person completes it.

### Asset Needed
- Creative/share artifact: two-person compatibility card.
- Copy/hook: “We are only 34% movie-compatible and that explains too much.”
- Landing/app destination: friend invite deep link.
- Tracking link/source tag: `vista_card_export_compatibility`.

### Distribution
Channel: in-app share, TikTok/IG relationship/friend formats, X quote prompts.
Borrowed audience target, if any: creators who make “rate my taste,” “movie hot takes,” couples/friend compatibility content.
CTA: “Compare your movie taste.”
Run date: TBD after invite flow exists.

### Measurement
Primary metric: invites sent per compatibility card view/export.
Secondary metric: invited-user activation to 25 ratings.
24h result: TBD
72h result: TBD
7d result: TBD

### Decision
Scale / iterate / kill: TBD
Reason: Scale if invite-to-install beats generic App Store links.
Next action: Design demo card + product spec for invite flow.

### Score
Audience fit: 5
Repeatability: 4
Proof: 4
Cost: 4
Conversion intent: 4
Shareability: 5
Competition gap: 5
Total: 31/35

## Experiment: Top Four By Actual Rating Prompt

App: Vista
Date created: 2026-05-19
Owner: JT / Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://www.reddit.com/r/Letterboxd/comments/1lh5ws4/i_need_movie_recommendations_based_on_top_4/
- https://www.reddit.com/r/Letterboxd/comments/1jc4hio/recommend_me_movies_on_the_basis_of_my_4_favorite/
- https://www.tiktok.com/@letterboxd/video/7543264757587954975
Observed pattern: Four favorites/top-four behavior already functions as movie taste shorthand and recommendation prompt.
Proof of traction: Recurring Reddit threads ask for recommendations from top four; FilmTok has top-four recommendation formats.
Audience: Casual-to-serious movie fans who already understand top-four identity.
Competitor/incumbent gap: Vista can add numeric precision: “top four by actual 1–100 rating,” not generic favorites.

### Hypothesis
If Vista gives users a top-four card ranked by actual 1–100 ratings, then users will share it because it fits existing movie culture while making Vista’s precision obvious.

### Asset Needed
- Creative/share artifact: top-four poster grid with scores.
- Copy/hook: “My top four by actual rating, not vibes.”
- Landing/app destination: App Store / Vista landing page.
- Tracking link/source tag: `vista_card_export_top_four_rating`.

### Distribution
Channel: X prompt, Reddit value-first threads, TikTok slideshow.
Borrowed audience target, if any: film meme/list accounts and movie recommendation communities.
CTA: “Make your top four by actual rating.”
Run date: TBD after card generation.

### Measurement
Primary metric: shares/saves per exported top-four card.
Secondary metric: comments/replies with others’ top four; installs from UTM link.
24h result: TBD
72h result: TBD
7d result: TBD

### Decision
Scale / iterate / kill: TBD
Reason: Scale if replies/comments create organic comparison behavior.
Next action: Build simple poster-grid export.

### Score
Audience fit: 5
Repeatability: 5
Proof: 4
Cost: 5
Conversion intent: 3
Shareability: 5
Competition gap: 3
Total: 30/35
