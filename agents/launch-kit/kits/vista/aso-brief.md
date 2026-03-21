# Vista — App Store Optimization Brief

## Competitor Analysis

| App | Rating | Reviews | Key Positioning | Keyword Strengths | Weaknesses to Exploit |
|-----|--------|---------|-----------------|------------------|----------------------|
| Letterboxd | 4.8 | 200K+ | Social film diary, star ratings | "movie diary", "film log", "movie tracker" | No numeric granularity. Stars only. Social feed is passive. |
| IMDb | 4.6 | 500K+ | Database, ratings, trailers | "movie ratings", "IMDb", "film database" | Not personal. No taste profile. Overwhelmingly a lookup tool. |
| Flickchart | 3.9 | 5K | Head-to-head movie ranking game | "movie ranking", "rank movies" | Outdated UI. No social. Low downloads signal. |
| Cinemanaut Bingo | 3.7 | 2K | Movie bingo challenge, niche | "movie challenge", "film bingo" | Very niche. Not a tracking or rating app in the traditional sense. |
| JustWatch | 4.7 | 150K+ | Streaming availability tracker, watchlist | "where to watch", "streaming", "watchlist" | Purely a logistics app. No ratings, no social, no taste signal. |

---

## Keyword Strategy

### Title (30 chars max)
**Vista: Movie Taste Profiles**

Current title appears solid. Keep it. "Taste Profiles" is differentiated and searchable.

### Subtitle (30 chars max)
**Rate, Track & Rank Your Films**

Recommended change. Packs three high-intent keywords: "rate," "track," "rank." These are the verbs users type when searching.

### Keyword Field (100 chars max)
**movie log,film diary,watchlist,cinema,letterboxd,rate movies,movie tracker,film ranking,taste**

Notes:
- "letterboxd" is searchable and your users are coming from there
- "film diary" gets real traffic from people looking for Letterboxd alternatives
- "taste" alone is low-competition and unique to Vista's positioning
- Do not include "Vista" in keyword field (it's already in title)
- Do not include spaces around commas (wastes character space)

---

## Screenshot Recommendations

**Screenshot 1 (Hero):**
Show the rating interface. Full-screen view of the 1-100 slider on a dark background with a film poster behind it. Overlay text: "Rate films from 1 to 100. Every point matters." This is the primary differentiator. Lead with it.

**Screenshot 2 (Taste Profile):**
Show the personal taste profile screen. Display All Time Favorite, Recent Favorite, Top Genre, Top Performer. Overlay text: "Your taste, ranked automatically." This screen is the emotional hook. People want to know what it says about them.

**Screenshot 3 (Friends Feed):**
Show the Friends tab with 3 friends' recent ratings visible. One has a comment. One has a like. Overlay text: "See what your friends think, in real time." Targets ICP 3 (Social Watcher). Instagram-style feed imagery resonates.

**Screenshot 4 (Explore Tab):**
Show the Explore tab with trending films and a watchlist section. Overlay text: "Find what to watch next. Save it instantly." Targets ICP 2 (Casual Watcher) who relies on external sources.

**Screenshot 5 (Rating History):**
Show a list of 8-10 rated films with their 1-100 scores visible. Sorted by score. Overlay text: "Your full rating history. Sorted the way you want." Shows the app as a long-term companion, not a one-time novelty.

---

## Full App Store Description (Rewrite)

**Character count target: under 4,000**

---

Star ratings aren't enough.

When everything you love sits at 4 or 5 stars, you can't tell what you actually care about most. Vista gives you 1 to 100. Now you can.

**Rate with real precision**
Slide from 1 to 100. The difference between an 87 and a 91 means something. Your ratings build a picture of your taste over time.

**Your personal taste profile**
Vista tracks your All Time Favorite, Recent Favorite, Top Genre, and Top Performer. As you rate more films, your profile sharpens. You see patterns you didn't know were there.

**See what your friends think**
The Friends tab is a live feed of everyone you follow. When a friend rates something, you see it. Like it. Comment on it. Movies are more interesting when you know what the people you trust think.

**Find what to watch next**
The Explore tab surfaces trending films and films your friends are rating. Add anything to your watchlist. Never wonder what to watch tonight.

**Built for people who take movies seriously**
Vista is for the person who wants a real record of what they've watched and what they actually thought about it. Not a casual scroll. A real library.

Download Vista. Rate your first film today.

---

**Character count:** approximately 1,100 characters. Well under 4,000. Room to add testimonials or update with social proof as reviews come in.

---

## Rating Prompt Strategy

**Timing:** Prompt users for a rating after they have rated their 5th film in the app. Not on first open. Not after one rating. After 5 ratings, the user has invested enough to have an opinion about Vista itself.

**In-app copy (iOS native prompt):**
Use Apple's SKStoreReviewRequest API — do not build a custom interstitial. Apple's native prompt converts better and follows guidelines.

**Trigger conditions:**
- User completes their 5th rated film
- User adds a film to their watchlist for the first time (secondary trigger, optional)

**What NOT to do:** Do not prompt after first open, after onboarding, or after any friction moment. Prompt only after a positive action is completed.

**Re-prompt cadence:** Apple limits this to 3 times per year per device. Spend those wisely. The post-5th-rating moment is the best single trigger.
