# Vista SEO / AI-Search Page Map — Movie Taste Queries

Date: 2026-06-01
Status: planning brief, no site edits made

## Executive Read
Vista should build durable discovery around precise movie ratings and taste identity, not generic movie tracking.

The first page to build remains the 1-100 rating page because it is the clearest high-intent wedge and already has a brief. The next layer should expand into taste profile, top-four-by-score, friend comparison, and private tracking pages.

## Source Inputs
- `memory/app-marketing/vista-first-growth-sprint-2026-05-27.md`
- `memory/app-marketing/seo-backlog.md`
- `memory/app-marketing/seo-briefs-vista-1-100-movie-rating-app.md`
- `memory/app-marketing/share-artifacts/vista-movie-taste-card-spec-2026-05-19.md`

## Page Prioritization

| Priority | Page | Target query | Intent | Build now? |
|---:|---|---|---|---|
| 1 | 1-100 Movie Rating App | `1-100 movie rating app` | User wants more precision than stars | Yes |
| 2 | Movie Taste Profile App | `movie taste profile app` | User wants ratings turned into identity/profile | Yes, after page 1 |
| 3 | Letterboxd Alternative for Precise Ratings | `Letterboxd alternative precise ratings` | User likes Letterboxd but wants a different rating model | Yes, careful positioning |
| 4 | Top Four Movie Ratings | `top four movies app` / `movie top four ratings` | User wants shareable favorites/taste artifact | Yes, if visual/card assets exist |
| 5 | Movie Taste Compatibility | `movie taste compatibility app` | User wants friend comparison/recommendation overlap | Hold unless comparison exists |
| 6 | Private Movie Rating App | `private movie rating app` | User wants tracking without public review pressure | Yes |
| 7 | Precise Movie Rating Scale | `rate movies out of 100` | User searches for a rating system, not necessarily an app | Yes |
| 8 | Divisive Movies Rating Tracker | `most divisive movies ratings` | User wants social/taste conflict content | Later, needs data |

## Page Briefs

### 1. 1-100 Movie Rating App
Recommended URL: `/1-100-movie-rating-app`

Primary query:
`1-100 movie rating app`

Secondary queries:
- precise movie rating app
- movie rating app with 100 point scale
- app to rate movies out of 100
- 100 point movie rating scale

Search intent:
The user is frustrated by stars or half-stars and wants finer personal scoring.

Page angle:
Most movie apps compress your reaction into stars. Vista lets you use the number you mean.

Direct answer:
A 1-100 movie rating app lets you score films with more precision than a 5-star or half-star scale. Vista uses a 100-point system so movies that both feel like "4 stars" can still have different personal scores.

Internal links:
- Movie Taste Profile App
- Private Movie Rating App
- Top Four Movie Ratings

Schema:
- SoftwareApplication
- FAQPage
- BreadcrumbList

Status:
Build first. Existing brief is already available at `memory/app-marketing/seo-briefs-vista-1-100-movie-rating-app.md`.

### 2. Movie Taste Profile App
Recommended URL: `/movie-taste-profile-app`

Primary query:
`movie taste profile app`

Secondary queries:
- app that shows your movie taste
- movie taste tracker
- movie taste profile
- film taste profile app

Search intent:
The user wants their ratings to turn into an identity, profile, or shareable summary.

Page angle:
Vista turns your 1-100 ratings into a sharper picture of what you actually like.

Direct answer:
A movie taste profile app turns your ratings into a personal view of your film taste: favorites, rating patterns, strictness, genre lean, and the movies that define your profile. Vista starts with precise 1-100 ratings so the profile is based on more than broad star buckets.

Page sections:
1. What is a movie taste profile?
2. Why 1-100 ratings create a clearer profile than stars.
3. What Vista can show from your ratings.
4. Example taste-card modules.
5. FAQ.

Internal links:
- 1-100 Movie Rating App
- Top Four Movie Ratings
- Movie Taste Compatibility

Schema:
- SoftwareApplication
- FAQPage

Build note:
Use screenshots or sample cards only if clearly labeled. No fake user stats.

### 3. Letterboxd Alternative for Precise Ratings
Recommended URL: `/letterboxd-alternative-precise-ratings`

Primary query:
`Letterboxd alternative precise ratings`

Secondary queries:
- Letterboxd alternative 100 point rating
- movie rating app like Letterboxd
- Letterboxd alternative private ratings

Search intent:
The user knows Letterboxd but wants a different scoring or privacy model.

Page angle:
Vista is not trying to replace Letterboxd's social film diary. It is for people who want more precise personal ratings.

Direct answer:
Vista can be used as a Letterboxd alternative if your main goal is precise personal rating instead of public reviews, comments, and social film activity. It uses a 1-100 scale so your ratings can capture smaller differences between movies.

Guardrails:
- Do not attack Letterboxd.
- Do not claim Vista has more social proof, reviews, lists, or community unless verified.
- Position as "for precise personal ratings," not "better than Letterboxd."

Internal links:
- 1-100 Movie Rating App
- Private Movie Rating App

Schema:
- SoftwareApplication
- FAQPage

### 4. Top Four Movie Ratings
Recommended URL: `/top-four-movie-ratings`

Primary query:
`top four movie ratings`

Secondary queries:
- movie top four app
- top four movies rating app
- share top four movies
- best app for top four movies

Search intent:
The user wants to express taste through favorite movies, likely in a social/share format.

Page angle:
Top four hits harder when the movies are ranked by your actual scores.

Direct answer:
A top-four movie ratings page shows your highest-rated films with the scores that put them there. Vista can make the familiar top-four format more precise by pairing each favorite with its 1-100 rating.

Build requirement:
Only build with real or clearly sample visual card support. Do not imply user export exists until it does.

Internal links:
- Movie Taste Profile App
- 1-100 Movie Rating App

Schema:
- SoftwareApplication
- FAQPage

### 5. Movie Taste Compatibility
Recommended URL: `/movie-taste-compatibility-app`

Primary query:
`movie taste compatibility app`

Secondary queries:
- compare movie taste with friends
- movie compatibility app
- film taste match app
- compare Letterboxd taste

Search intent:
The user wants to compare ratings with another person.

Page angle:
Movie compatibility should show agreements, disagreements, and shared watched films, not just a vague match score.

Direct answer:
A movie taste compatibility app compares two people's ratings to show where their taste overlaps and where it clashes. A strong comparison should show shared watched films, biggest agreements, biggest disagreements, and rating distance.

Build status:
Hold as an indexable page until Vista supports comparison or the page is explicitly framed as a planned concept. If comparison is not live, this should be a product roadmap/content asset, not an acquisition page.

Internal links:
- Movie Taste Profile App
- Top Four Movie Ratings

Schema:
- FAQPage only if roadmap page, SoftwareApplication only if feature is live.

### 6. Private Movie Rating App
Recommended URL: `/private-movie-rating-app`

Primary query:
`private movie rating app`

Secondary queries:
- track movie ratings privately
- private movie diary app
- movie rating app without social pressure

Search intent:
The user wants to track taste without public review pressure.

Page angle:
Some ratings are for your own taste, not a public review feed.

Direct answer:
A private movie rating app lets you track what you watched and how you scored it without turning every rating into a public review. Vista is positioned around precise personal ratings, so it can work for people who want a cleaner private taste record.

Internal links:
- 1-100 Movie Rating App
- Movie Taste Profile App

Schema:
- SoftwareApplication
- FAQPage

### 7. Precise Movie Rating Scale
Recommended URL: `/rate-movies-out-of-100`

Primary query:
`rate movies out of 100`

Secondary queries:
- 100 point movie rating scale
- how to rate movies out of 100
- movie rating scale 1 to 100

Search intent:
The user may be looking for a method, not an app. This is an educational page that can still introduce Vista.

Page angle:
A 100-point scale is useful when stars hide too much difference between films.

Direct answer:
To rate movies out of 100, use broad bands for quality and then adjust within each band for personal feeling. For example, an 80-89 range can represent strong movies, while the exact score captures the difference between "solid" and "still thinking about it."

Internal links:
- 1-100 Movie Rating App
- Movie Taste Profile App

Schema:
- HowTo, if the page gives a rating method.
- FAQPage.

### 8. Divisive Movies Rating Tracker
Recommended URL: `/divisive-movie-ratings`

Primary query:
`divisive movie ratings`

Secondary queries:
- movies people disagree on
- polarizing movie ratings
- movie rating disagreement

Search intent:
The user wants social/taste-conflict discovery, likely a content page.

Page angle:
The most interesting movie taste data is often where ratings split.

Direct answer:
Divisive movie ratings show where people disagree most sharply. In a personal movie app, that can mean movies you rated much higher or lower than your friends or the average viewer.

Build status:
Later. This page needs real aggregate or comparison data. Do not fake divisive rankings.

Internal links:
- Movie Taste Compatibility
- Top Four Movie Ratings

Schema:
- Article or dataset-style schema only if real data exists.

## First Page To Build
Build `/1-100-movie-rating-app` first.

Why:
- It is already briefed.
- It has the clearest search intent.
- It supports every other page.
- It does not depend on friend comparison or aggregate data.
- It reinforces Vista's product distinction in one sentence.

## Implementation Guardrails
- No fake user statistics.
- No fake compatibility claims.
- No claim that Vista is a larger social network than Letterboxd.
- No "better than Letterboxd" framing.
- Use "precise personal ratings" and "taste profile" as the core language.
- Add App Store CTA only where the app/URL is available and approved.

## Success Metrics
- Page indexed.
- Search Console impressions for target and secondary queries.
- AI-search citation or mention checks for "1-100 movie rating app" and "movie taste profile app."
- App Store clicks/downloads if tracked.
- Replies or social comments using language like "100 point scale," "stars are too blunt," or "movie taste profile."
