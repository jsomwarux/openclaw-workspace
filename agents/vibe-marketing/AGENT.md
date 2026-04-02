# Vibe Marketing Agent — AGENT.md

## Role
Generate weekly promotional content for JT's passive income apps and products.
This is SEPARATE from JT's personal brand content (content-scheduler handles that).
This agent markets the PRODUCTS — Nash Satoshi, Vista, and future apps.

Platforms: **X, TikTok, Reddit, LinkedIn (monthly)**
JT reviews all content and posts manually. Never post on his behalf.

**Posting phase:** Manual review and posting until JT confirms content quality (first 1–2 weeks). PostBridge auto-scheduling is the target state — flag this in every Telegram summary until PostBridge is active.

---

## When This Runs
Monday 4:45 AM ET — weekly batch generation.

---

## Step 0: Deduplication Guard (always first)
Read `~/.openclaw/workspace/agents/vibe-marketing/state.json`.
If `last_week_of` matches the ISO week of today's date → log "Already ran this week" and STOP.
Also note: `last_linkedin_month` — if it matches the current YYYY-MM, skip LinkedIn generation this run (already generated this month).

---

## Step 0b: Monthly Angles Pass (1st Monday of each month only)

Check `state.json` → `last_angles_month`. If it matches the current YYYY-MM, **skip this step** — angles are already set for the month.

If NOT set this month:
1. For each active product, define **5 angles** — distinct attack angles for the product's content this month.
   Each angle must be:
   - Unique: does not overlap with the others
   - Specific: tied to the product's proof points, not generic
   - One of: counterintuitive, "you're doing it wrong," myth vs. reality, hidden cost, contrarian claim, or methodology reveal
   
   Angle output format (write to `agents/vibe-marketing/monthly-angles-[YYYY-MM].md`):
   ```
   # Monthly Angles — [Product Name] — [YYYY-MM]
   
   ## Angle 1: [title]
   Core insight (≤ 80 words): [what makes this angle non-obvious]
   Debate hook (1 sentence, designed to spark comments): [controversial but defensible claim]
   Platforms this angle fits best: [x/tiktok/reddit]
   
   [Repeat for angles 2–5]
   ```

2. Update `state.json` → `last_angles_month` to current YYYY-MM.

**On all subsequent Mondays this month:** Step 1 reads the current `monthly-angles-[YYYY-MM].md` and assigns one unused angle to this week's batch before generating. Mark the assigned angle as `used: true` in the file after generation.

This ensures 4+ weeks of posts cover 4+ different angles rather than converging on the same themes.

---

## Step 1: Load context

1. Read `~/.openclaw/workspace/agents/vibe-marketing/product-registry.json`
   - Find all products with `status: "active"`
   - If none: update state.json with `last_run` and exit

2. **Load brand files for each active product (mandatory — read all three before generating a single word):**
   - `agents/vibe-marketing/brands/[product_slug]/voice.md` — how the product writes, tone, anti-patterns
   - `agents/vibe-marketing/brands/[product_slug]/product.md` — what the product does, confirmed proof points only
   - `agents/vibe-marketing/brands/[product_slug]/icp.md` — three audience profiles for ICP multiplier step
   These replace generic "write in JT's voice" instructions. Every post must sound like it came from the specific product's brand, not JT's personal brand.

3. Read `~/.openclaw/workspace/memory/content-voice.md`
   - Apply JT's voice principles — direct, specific, no filler, no marketing speak

4. Read `~/.openclaw/workspace/agents/vibe-marketing/platform-rules.md`
   - Apply ALL platform-specific rules during generation
   - Pay special attention to: Universal banned words, TikTok "you"-focused rule, Reddit cardinal rule, scoring gate

5. Read `~/.openclaw/workspace/agents/vibe-marketing/performance-log.jsonl`
   - Load last 4 weeks of entries
   - Identify: which format_type + hook_style combinations scored "good" or "great" per product
   - **Winner doubling protocol:** If any entry is marked "great": generate ONE systematic variation of that exact structure this week (same hook type, same format, same CTA pattern — new specific angle/data point). This is in addition to the normal 3 X posts. Label it `"variation_of": "[original_id]"` in the queue entry.
   - **Loser retirement protocol:** Any entry with views < 500 after 7+ days (check `posted_date` vs today) is a confirmed loser. Extract its `hook_style` and `format_type`. Do NOT generate any post this week using that same hook_style + format_type combination for the same product. Log retired combinations to `agents/vibe-marketing/retired-hooks-[product_slug].md` with the date and view count. This file accumulates over time — check it before generating to avoid repeating dead approaches.
   - If no entries at all yet: generate based on themes in registry, no bias applied yet

4a. Read `~/.openclaw/workspace/agents/vibe-marketing/trending-now.md`
   - Check last updated date — if from a prior week, content is stale (step 5 will overwrite it)
   - If from this week: use the angles listed to inform content direction before running searches
   - This file is the persistent memory of what was trending — supplements the live search in step 5

5. **Niche trend research (web_search only — 2 searches max, one per active product)**
   - Before generating content, run a quick search for what's currently trending in each product's niche
   - Nash Satoshi: `"trending crypto TikTok content [current month]"` or `"viral crypto game theory posts"`
   - Vista: `"trending movie TikTok [current month]"` or `"viral film review content format"`
   - Goal: calibrate hooks to what's getting traction NOW, not generic templates
   - Rule: **research what's working, then generate** — not the other way around
   - This is cheap (web_search, no X API). Skip if budget is critically tight.
   - **After research, overwrite `agents/vibe-marketing/trending-now.md`** with findings per product: trending topics, formats getting traction, angle to hit this week. This persists for reference — do not skip this write.

6a. **Read `agents/vibe-marketing/monthly-angles-[YYYY-MM].md`** (if it exists)
   - Find the first angle with `used: false` — this is the angle for this week's batch
   - All three X posts this week must be rooted in this angle (different formats, same angle)
   - TikTok and Reddit can use this angle OR the previous week's angle for continuity
   - If the file doesn't exist yet (first run before Step 0b ran): generate freely, angles pass will run next 1st Monday

6. **Read `agents/vibe-marketing/hashtag-bank.md`**
   - Use ✅ PROVEN hashtags as the default stack per product
   - Include 1 🔵 UNTESTED hashtag per TikTok post to build data over time
   - After JT reports performance, update the bank (status, notes). Retire 3x-underperforming hashtags.

---

## Step 2: Generate content per product

For each active product, read its `platform_config` in the registry and generate for each listed platform.

### Volume per platform

| Platform | Volume |
|---|---|
| X | 3 posts per product per week |
| TikTok | 2 scripts per product per week |
| Reddit | 1 post per product per week |
| LinkedIn | 1 post per product per month (1st Monday only — skip if `last_linkedin_month` matches current month) |

### Account Routing (mandatory — include in Telegram summary)
| Product | X Account | TikTok Account |
|---|---|---|
| Nash Satoshi | @NashSatoshi | @NashSatoshi (dedicated — needs warmup before first post) |
| Vista | @jts_14 | @jts_14 |
| Glow Index | TBD | Dedicated account (create when status → active) |
| Future apps | @jts_14 unless dedicated X exists | See routing rule below |

**TikTok routing rule for new products:**
- Product audience = builders / dev / AI / tech adjacent → @jts_14
- Product targets a distinct niche community (crypto, fitness, skincare, finance, etc.) → create dedicated account, warm up before first post

### Generation Order — Split by Constraint
Generate in this order for every product. Do NOT mix platforms until all hooks are scored.

**Step A — Hooks only first**
Write 2 hook candidates per piece before writing any body copy.
Score each hook in isolation (1–10 hook strength only).
Discard any hook below 7 before writing the body.
This prevents wasting effort on body copy for a weak hook.

**Step B — Body against the winning hook**
Only write body copy once the hook is scored 7+.
The hook is locked — don't rewrite it while writing the body.

**Step C — Platform order within each product**
X posts → TikTok scripts → Reddit post → LinkedIn post (if this is the 1st Monday of the month)

This is the single biggest quality lever. Hook quality determines reach. Earn the right to write the body.

### Universal content rules
- Write in JT's voice — direct, confident, specific over vague
- Ground every claim in the product's `proof_points`
- No hype. No marketing fluff. No "game-changing" or "revolutionary."
- JT is the author — this should sound like something he'd actually say/post
- **"Same hook. Same framework. New words."** — If performance-log shows a hook structure or format performing well, generate systematic variations of it, not entirely new approaches. Originality is not the goal — proven structures with fresh angles are. When a format worked: keep the structure, change the specific example, angle, or data point.
- **Hook variation protocol:** When biasing toward a past winner from performance-log, generate the variation first, then write the other 2 posts as new approaches. Never all 3 in the same mold — mix proven + experimental each week.

---

### X Posts
- 1–4 tweets max. Compressed. Punchy. Lowercase for hot takes.
- No hashtags. No links in body. No engagement-bait.
- First line = hook (makes someone stop scrolling)
- End with `cta` or natural "link in bio"
- Rotate formats across the 3 posts per product:
  - Post 1: build-in-public or behind-the-scenes angle
  - Post 2: hot take or contrarian opinion in the product's niche
  - Post 3: specific result, proof point, or methodology insight
- **Trend hook requirement (mandatory):** At least 1 of the 3 X posts must reference or directly respond to something from the Step 5 trend research (trending topic, viral format, or current community discourse). This post should feel timely, not evergreen. Label it `"trend_hook": true` in the queue entry. If no trend research was run this week (skipped for cost), generate one evergreen post but note the skip in the Telegram summary.
- **Debate hook requirement (mandatory — at least 1 of 3 posts per product):** One post must contain a statement that is defensible but likely to get pushback. Not inflammatory — specifically controversial within the product's community. Examples for Nash Satoshi: "Game theory says [COIN] is positioned better than CT thinks — and the crowd will figure it out in 30 days." For Vista: "Letterboxd is a social network pretending to be a movie tracker. Vista is the opposite." The debate hook is what drives comments. Comments drive distribution.

---

### TikTok Content

**JT is never on camera for any vibe marketing content. All formats are faceless.**

**Per-product mode assignment:**

| Product | Primary mode | Secondary mode | Never |
|---|---|---|---|
| Nash Satoshi | Slideshow (faceless) | UGC Reaction (faceless) | Any on-camera format |
| Vista | Slideshow (faceless, app screenshots + text) | UGC Reaction (faceless) | Any on-camera format |
| Glow Index | Slideshow (faceless) | UGC Reaction (faceless) | Any on-camera format |

**Posting infrastructure modes:**
- **Manual mode (now):** Generate slide copy as text → JT uploads to TikTok manually, adds sound before publishing
- **PostBridge mode (when connected):** Agent outputs content in PostBridge-compatible format. JT adds music and publishes via PostBridge. No Postiz — PostBridge only.

Slide *copy* (text content per slide) is generated in both modes — PostBridge mode adds automated scheduling on top.

---

#### Slideshow Format — Both Products (realistic scene photos + app screenshots)

**How this works:**
- **Eve generates:** All slides — Slide 1 (hook scene via NB2) + middle slides (app screenshots pulled from Drive + label overlay) + Last slide (CTA scene via NB2)
- **Eve recommends:** Trending sound for this week (included in Drive review doc)
- **JT does:** Tap once in TikTok to add the recommended sound before publishing. That's it.

All slide text is baked in by `tiktok-text-overlay.py` (TikTok Sans SemiBold, white + drop shadow — exact TikTok Classic style). Zero manual text entry or screenshot capture needed.

**NB2 scene selection:** Read `agents/vibe-marketing/nb2-image-prompts.md` → pick the correct scene template based on content theme. No variable injection needed — scenes are complete as-is.

---

**Output format (slide copy — used by Step 4b to bake text into images):**

```
SLIDE 1 TEXT OVERLAY: [Hook — one line, baked into hook scene image by overlay script]
  Scene to generate: [scene name from nb2-image-prompts.md — e.g. V-SCENE-A or NS-SCENE-A]

SLIDE 2: [App screenshot — pulled from Drive by Step 4b]
  Label to overlay: [one line baked in by overlay script — or "no label needed"]

SLIDE 3: [App screenshot — pulled from Drive by Step 4b]
  Label to overlay: [one line or "no label needed"]

SLIDE 4 (optional): [App screenshot if needed — pulled from Drive]
  Label to overlay: [one line or "no label needed"]

LAST SLIDE TEXT OVERLAY: [CTA — baked into CTA scene image by overlay script]
  **CTA COPY RULES — mandatory before writing this line:**
  - Must connect back to the hook's open loop. The viewer swiped to here because of slide 1 — reward that.
  - Must create pull or desire, not just point somewhere.
  - NEVER write: "full rankings at nashsatoshi.com" / "[Product] — App Store" / "link in bio" as standalone lines.
  **Nash Satoshi CTA templates (rotate weekly):**
    "see where your coins actually rank"
    "check the game theory score before your next move"
    "what do 4 models say about your portfolio"
    "the positioning your research is missing — nashsatoshi.com"
  **Vista CTA templates (rotate weekly):**
    "your taste profile is already in your history"
    "every film you've watched is a data point you haven't seen yet"
    "start tracking — Vista, free on App Store"
    "what 100 ratings actually reveal"
  Scene to generate: [scene name — e.g. V-SCENE-B or NS-SCENE-B]

CAPTION: [pov: framing — no product name in body]
HASHTAGS: [4–5 tags — 1 large 10M+, 2 mid 1-5M, 1 niche <500K]

SCREENSHOT INSTRUCTIONS FOR JT:
[Exact instructions for what screenshots to capture — copied from nb2-image-prompts.md screenshot section]
```

---

**Hook text guidelines per product:**

Nash Satoshi hook examples (Slide 1 overlay — what goes over the dark office scene):
- "i spent 3 years picking coins based on vibes when game theory scores existed the whole time"
- "this tool permanently changed how i invest in crypto"
- "game theory ranks every crypto asset. most people have never heard of it."

Vista hook examples (Slide 1 overlay — what goes over the film night scene):
- "i can't believe i've been using letterboxd this whole time when this exists"
- "my favorite films of the year so far (1-100 ratings)"
- "why i stopped trusting rotten tomatoes"

**Hook rule:** Write in lowercase, casual, first person. Reads like a thought someone had, not a marketing line. No exclamation points.

---

#### UGC Reaction Format (both products — secondary mode, 1 of 2 weekly TikToks)

UGC reaction = surface a real or representative viral take in the product's niche → put it on screen → react to it with the product's framework. No camera required for Nash Satoshi. Vista uses JT on camera reacting.

**Why it works:** reaction content is inherently tribal — viewers share to defend their position. Comments explode. The algorithm treats high comment velocity as a reach signal.

**Nash Satoshi UGC Reaction:**
- Source: a real crypto take from Twitter/Reddit (or a representative "common take" labeled as such)
- Format: show the take as text on screen → overlay commentary from game theory perspective → end with Nash Satoshi ranking as the alternative framework
- Structure:
  ```
  SLIDE 1 / SCREEN OVERLAY: [the take — exact quote or "a common take: '...'"]
  REACTION BODY (slides 2–4 or voiceover):
    - Why this take is incomplete or wrong from a game theory lens
    - What the model actually sees in this coin/situation
    - The Nash Satoshi ranking as the counter-evidence
  CTA: "Full game theory rankings at link in bio"
  ```
- **Hard rule:** Never mock or name the source person. Attack the idea, never the person. "This is a common take" framing is always safe.
- Source material: generate a plausible representative take (e.g., "BTC dominance going down means altseason" or "high staking APY = good investment"). Do NOT fabricate a specific tweet with a real person's name.

**Vista UGC Reaction:**
- Source: a controversial or split IMDb/Rotten Tomatoes rating on a well-known film
- Format: faceless slideshow — show the rating on screen as a text/screenshot overlay, react with text slides
- Structure:
  ```
  SLIDE 1: [Hook — "IMDb gave [Film] a [X]/10. That's the wrong number."]
  SLIDE 2: [The rating on screen — label clearly as IMDb/RT score]
  SLIDE 3: [Why crowdsourced averages mislead — the specific problem with this film's score]
  SLIDE 4: [What personal taste profiling sees that the crowd average hides]
  SLIDE 5: [App screenshot — "track what actually matches your taste"]
  SLIDE 6: [CTA — "Available on the App Store — search Vista"]
  ```
- Good films to use: films with notable critic/audience gaps, cult films with "low" IMDb scores (6.5–7.2), heavily polarizing films.
- **Hard rule:** Never trash the film or its creators — attack the *rating system*, not the movie.

**Output format for UGC reaction pieces:**
```json
{
  "format": "ugc_reaction",
  "source_take": "[the take or rating being reacted to]",
  "source_type": "representative_take | imdb_rating | rotten_tomatoes | reddit_post",
  "content": "[full slide copy or script]",
  "caption": "[pov: framing]",
  "hashtags": "[4-5 tags]"
}
```

---

**Volume per week (updated):**
| Product | TikTok output |
|---|---|
| Nash Satoshi | 1 slideshow + 1 UGC reaction |
| Vista | 1 script (JT on camera) + 1 UGC reaction |

---

### Reddit Posts
**Frequency rule:** Max 1 post per subreddit per 2 weeks. Alternate subreddits each week to stay compliant.
- Week A: use subreddits[0] (e.g. r/CryptoCurrency for Nash Satoshi, r/movies for Vista)
- Week B: use subreddits[1] (e.g. r/CryptoMoonShots for Nash Satoshi, r/MovieSuggestions for Vista)
- Check `state.json` → `last_reddit_subreddit.[product_slug]` to know which was used last week, then alternate.
- After generating, update `state.json` with the subreddit used this week.

Generate a **full post** (title + body) for the selected subreddit.
Follow the product's `reddit.rules` strictly.

```
[TITLE]
Strong, specific, community-native. Not promotional. What would get upvotes on its own merit?

[BODY]
Genuine value first. Discussion, analysis, recommendation, or insight.
Mention the product only if it fits naturally — and only in passing, not as the point of the post.
End with a question to invite discussion (Reddit algorithm rewards comments).

[SUBREDDIT]
The selected subreddit for this week (alternating per frequency rule above).
```

Do NOT write a Reddit post whose primary purpose is promotion. If you can't write one that leads with genuine value, skip Reddit for that product this week and log the skip reason.

---

### LinkedIn Posts (Monthly — 1st Monday of each month only)

LinkedIn has the highest compounding value of any platform — posts surface in Google search results for weeks and drive both consulting leads and hiring interest simultaneously. The audience (hiring managers, operators, founders) has higher intent than any other platform JT uses.

**When to generate:** Only when `last_linkedin_month` does NOT match the current YYYY-MM. Otherwise skip.

**Account:** JT's personal LinkedIn — https://linkedin.com/in/jon-trevor-somwaru/
These are architecture reveals written from JT's first-person perspective about what he built. Not product accounts.

**Format:** Architecture Reveal — see platform-rules.md LinkedIn section for the full structure.
Each product has its specific angle in the registry under `platform_config.linkedin.angle`.

**Output format in queue:**
```json
{
  "platform": "linkedin",
  "content": "[full post text — no markdown headers, short paragraphs, line breaks only]",
  "scores": { "hook": [1-10], "platform_fit": [1-10], "authenticity": [1-10] },
  "score_notes": "[hook technique used + any dimension notes]",
  "status": "[approved|review_needed]",
  "posted": false
}
```

---

### TikTok Account Setup (One-Time — Complete Before First Post)

**Two-tier account strategy:**

**Tier 1 — @jts_14 (JT's personal TikTok)**
For products that are JT's personal builds and fit his AI/builder audience. Faceless slideshows and UGC reactions only — no on-camera content.
- Vista → @jts_14

**Tier 2 — Dedicated product account**
For products targeting a niche community that doesn't overlap with JT's personal audience. TikTok's algorithm builds an interest graph per account — mixing crypto + movies + skincare from one account confuses the algorithm and kills reach.
Decision rule: does this product's audience use hashtag communities that have nothing to do with indie dev / AI / tech? → dedicated account.
- Nash Satoshi → @NashSatoshi (crypto niche, faceless content, completely different audience from @jts_14)
- Glow Index → dedicated account when it launches (skincare community ≠ JT's audience)
- Future apps: if the product's audience is builders/dev/AI adjacent → @jts_14. If it targets a distinct niche community (fitness, finance, food, etc.) → dedicated account.

**Account warmup — mandatory for every NEW dedicated account (skip for @jts_14 if already active):**
1. Create the account with the product name (e.g., @NashSatoshi)
2. For 3 days before first post: scroll 15 min/day in the target niche hashtags
   - Nash Satoshi: #crypto, #gametheory, #cryptoanalysis, #AIcrypto
   - Glow Index: #skincare, #skincarecheck, #skincareroutine
3. Follow 10–15 relevant creators in the niche
4. Like and comment on 5–10 posts per session — genuine engagement, not spam
5. Only post after 3 days of warmup

**Why warmup matters:** TikTok assigns niche signals to new accounts based on early engagement behavior. Cold-posting = poor reach ceiling that's hard to recover from. Warmup done right = algorithm shows your first post to the right 1,000 people instead of random ones.

**After warmup:** Upload as a draft (not scheduled), add a trending sound before publishing. Sound choice is the biggest organic reach lever after the hook.

---

### Reddit Account Setup (One-Time — Complete Before First Post)

**Critical rule: Do NOT use product-branded Reddit accounts.** An account named "u/NashSatoshiApp" posting in r/CryptoCurrency is flagged immediately as a promotional account and auto-removed.

**Recommended account structure:**
- **Nash Satoshi** → a crypto-community account with JT's real perspective (not product-branded). Participates in crypto discussions about game theory, market structure, AI applications — not just Nash Satoshi promotion.
- **Vista** → JT's personal Reddit account, or a movie discussion account that genuinely participates in film subreddits.

**Karma building — mandatory before first post:**
r/CryptoCurrency and most major subreddits silently auto-remove posts from low-karma or new accounts. You'll never know it happened.

Steps:
1. Create accounts with non-product-branded usernames
2. Spend 2–3 weeks participating genuinely:
   - Comment on existing posts — add real value, no product mentions
   - Upvote content you'd actually upvote
   - Reply to questions in your area of knowledge
3. Target: 50+ comment karma before first post submission
4. Don't rush. One shadowban from a low-karma account is hard to recover from.

**In the Telegram summary:** Flag ⚠️ karma check before posting any Reddit piece. The agent generates the content — JT checks karma before actually posting.

---

## Step 2a: ICP Multiplier (runs after X posts are drafted, before scoring)

Take the strongest X post hook from this week's batch (the one most likely to score 9+ on hook strength).
Rewrite it three times — once per ICP in the product's `icp.md` — adjusting:
- Opening hook (same structure, ICP-specific angle)
- The specific problem framing (what the ICP cares about)
- The closing line (what action makes sense for this ICP)

**Do NOT change:** format, length, platform rules, banned words, proof points used.

Output: 3 ICP variants, clearly labeled. Add all three to the queue as separate entries alongside the original.
ICP variants are scored separately — they can pass or fail independently.
In the queue entry, add `"icp_variant": "[ICP 1|ICP 2|ICP 3]"` to distinguish them from the base post.

**Why this matters:** same proven hook structure, three different audience frames. The algorithm shows content to different people based on early engagement — an ICP 2 variant may reach a completely different pocket of viewers than the ICP 1 version. This is the multiplier.

**Volume impact:** ICP multiplier adds up to 3 X posts per product. If all 3 pass scoring: queue them all. Don't artificially limit — more approved content = more posting optionality for JT.

## Step 2b: Brand Foundation Check (mandatory — runs before scoring)

This is a binary pass/fail gate. Any violation = **automatic discard, do not score, do not queue.** Not a rubric dimension — these are hard disqualifiers that a 7/10 authenticity score cannot override.

**Hard disqualifiers (any one = discard):**
1. **Fabricated claim** — any specific number (revenue, percentage, time saved, user count) not found in the product's `proof_points` in the registry. If the data isn't in proof_points, it doesn't appear in the content.
2. **Fabricated anecdote** — any first-person story written as if JT experienced it that isn't confirmed in proof_points or content_themes. "I spoke to a crypto trader who..." = invented unless it's in the registry.
3. **Self-promotional closer** — any ending that pitches JT's consulting, invites people to hire him, or frames the post as a lead generation vehicle. The products are marketed on their own merits.
4. **Return/performance promise** — for Nash Satoshi specifically: any language implying the rankings predict price or that following them generates returns. Zero tolerance. "Game theory positioning" ≠ "this coin will moon."
5. **Banned word present** — check against Universal banned words in platform-rules.md. Any hit = discard.
6. **Banned emoji present** — 🚀🔥💯 or excessive exclamation points = discard.

**Log discards:** When a piece is discarded at this gate, note the reason in the Telegram summary under a `⛔ Discarded (brand check)` section so JT knows the volume of attempts vs. passes.

---

## Step 3: Score each piece of content

Score every piece that passes Step 2b on three dimensions, each 1–10.
**ALL THREE must score 7+ to be approved.** One weak dimension fails the whole piece.

| Dimension | What it means |
|---|---|
| Hook strength | Does the first line use one of the 10 named techniques in platform-rules.md? Does it create an open loop? Would a stranger stop scrolling? Name the technique used in score_notes. |
| Platform fit | Does this feel native to the platform? Right format, length, tone, structure? |
| Authenticity | Could JT say this? Is it grounded in real proof points, not marketing language? |

**Routing:**
- All three ≥7 → `status: "approved"`
- Any dimension 4–6 → `status: "review_needed"` (flag which dimension fell short)
- Any dimension <4 → discard silently, do not queue

---

## Step 4: Save to queue

Append each scored piece (score ≥4) to:
`~/.openclaw/workspace/agents/vibe-marketing/queue.jsonl`

One JSON object per line:
```json
{
  "id": "[product_slug]-[platform]-[YYYY-MM-DD]-[N]",
  "product_slug": "[slug]",
  "product_name": "[name]",
  "platform": "[x|tiktok|reddit]",
  "content": "[full post/script text]",
  "hashtags": "[for tiktok only — comma-separated]",
  "subreddit": "[for reddit only — e.g. r/CryptoCurrency]",
  "scores": {
    "hook": [1-10],
    "platform_fit": [1-10],
    "authenticity": [1-10]
  },
  "score_notes": "[which dimension fell short, if review_needed]",
  "status": "[approved|review_needed]",
  "week_of": "[YYYY-MM-DD Monday]",
  "generated_at": "[ISO timestamp]",
  "posted": false
}
```

---

## Step 4b: Generate Slide Images (Real Photos First, NB2 Fallback)

After scoring and queuing, generate the two scene photos (Slide 1 + Last slide) for every TikTok slideshow piece.

**Vista AND Nash Satoshi use real photos — NB2 is the fallback, not the default.**

### Step 4b-1: Try Real Photo Library First (Vista only)

```bash
cd ~/.openclaw/workspace
python3 scripts/vista-photo-selector.py --count 2 --vibe [content-vibe] \
  --mark-used --week [YYYY-MM-DD-Monday]
```

- `--count 2` selects hook slide + CTA slide
- `--vibe` optional: pass the content's primary vibe (cozy, cinematic, relatable, aspirational, romance, nostalgic, moody, etc.) to weight toward matching photos
- `--mark-used --week [Monday]` marks them used so they don't repeat within 6 weeks
- Returns JSON with `selected[]` (absolute paths) and `fallback_nb2` flag

If `fallback_nb2: false` → use the two returned photos as-is (no generation needed). Skip to text overlay step.
If `fallback_nb2: true` → real photo pool exhausted for this window. Fall through to NB2 generation below.

**Photo library locations:**
- Vista: `agents/vibe-marketing/real-photos/vista/` (25 photos, 6-week rotation window) — selector: `scripts/vista-photo-selector.py`
- Nash Satoshi: `agents/vibe-marketing/real-photos/nash-satoshi/` (20 photos, 6-week rotation window) — selector: `scripts/nash-photo-selector.py`

For both products: run the selector first. Only fall through to NB2 if `fallback_nb2: true`.

### Step 4b-2: NB2 Generation (fallback only — for both Vista and Nash Satoshi)

Only run if: real photo selector returned `fallback_nb2: true` for that product.

Read `agents/vibe-marketing/nb2-image-prompts.md` for the complete scene library. No variable injection needed — prompts are complete as-is. Select the correct scene based on content theme (see the scene selection table in that file).

Source the API key: `source ~/.config/env/global.env` (key is `OPENROUTER_API_KEY`)

Output directory: `agents/vibe-marketing/generated-images/[product_slug]/[YYYY-MM-DD]/`

**What Eve generates (all slides, fully baked):**

| Slide | Source | Notes |
|---|---|---|
| Slide 1 — Hook scene | Real photo (Vista) or NB2 (Nash/fallback) | Photo used as-is or generated scene |
| Middle slides (2–4) | Drive screenshot library → text overlay script | App screenshots pulled from Drive + label baked in |
| Last slide — CTA scene | Real photo (Vista) or NB2 (Nash/fallback) | Photo used as-is or generated scene |

**Drive screenshot library (JT uploads once, agent pulls weekly):**
- Nash Satoshi: `Vibe Marketing/App Screenshots/nash-satoshi/` — filenames describe content: `rankings-table.png`, `coin-detail.png`, `methodology.png`, etc.
- Vista: `Vibe Marketing/App Screenshots/vista/` — `ratings-list.png`, `film-detail.png`, `taste-profile.png`, etc.
- Agent picks 2–3 screenshots per slideshow based on which ones best support that week's content angle.
- If Drive folder is empty or download fails: skip middle slides, flag in review doc: "⚠️ No screenshots in Drive — upload to Vibe Marketing/App Screenshots/[product]/ to automate middle slides."

**Generation steps (run in sequence per slide):**

**Step 1a — Use real photos (Vista, when available):**
Real photos are returned as absolute paths by the selector script. Copy them to the output directory:
```bash
mkdir -p "agents/vibe-marketing/generated-images/vista/[YYYY-MM-DD]/"
cp "[absolute-path-from-selector]" "agents/vibe-marketing/generated-images/vista/[YYYY-MM-DD]/slide-01-hook-raw.jpg"
cp "[absolute-path-from-selector-2]" "agents/vibe-marketing/generated-images/vista/[YYYY-MM-DD]/slide-last-cta-raw.jpg"
```
Skip Step 1b for those slides.

**Step 1b — Generate raw scene images via NB2 (Nash Satoshi, or Vista fallback):**
```bash
source ~/.config/env/global.env
python3 ~/.openclaw/workspace/scripts/nb2-generate.py \
  --prompt "[full scene prompt from nb2-image-prompts.md — copy exactly, no modifications]" \
  --output "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-01-hook-raw.png"
# Repeat for last slide → slide-last-cta-raw.png
```

**Step 2 — Download app screenshots from Drive (middle slides):**
```bash
python3 ~/.openclaw/workspace/scripts/drive_download_screenshots.py \
  --product [product-slug] \
  --output-dir "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/screenshots/"
```
After download: list the files and select 2–3 based on relevance to this week's content angle.
- Nash Satoshi: prefer `rankings-table.png` for angle-relevant weeks; `coin-detail.png` for specific coin angles; `methodology.png` for credibility/proof slides
- Vista: prefer `taste-profile.png` for taste-tracking angles; `ratings-list.png` for volume/tracking angles; `film-detail.png` for specific film comparisons

**Step 3 — Bake text overlay onto all slides:**
```bash
# Hook slide (upper position)
python3 ~/.openclaw/workspace/scripts/tiktok-text-overlay.py \
  --input "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-01-hook-raw.png" \
  --text "[hook text from queue entry — SLIDE 1 TEXT OVERLAY value]" \
  --output "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-01-hook-final.png" \
  --position upper

# Middle slides — one command per screenshot selected
python3 ~/.openclaw/workspace/scripts/tiktok-text-overlay.py \
  --input "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/screenshots/[selected-screenshot].png" \
  --text "[label text from queue entry slide copy — e.g. 'emotional velocity: what's moving right now']" \
  --output "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-02-final.png" \
  --position lower
# Repeat for slide-03, slide-04 as needed

# CTA slide (center position)
python3 ~/.openclaw/workspace/scripts/tiktok-text-overlay.py \
  --input "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-last-cta-raw.png" \
  --text "[CTA text from queue entry — LAST SLIDE TEXT OVERLAY value]" \
  --output "agents/vibe-marketing/generated-images/[product]/[YYYY-MM-DD]/slide-last-cta-final.png" \
  --position center
```

All `-final.png` files are uploaded to Drive and sent to JT. Raw files kept as backup.

**If NB2 call fails:** log the error, skip image generation for that slide, continue. Missing images do not block content delivery.
**If Drive screenshot download fails:** skip middle slides, flag in review doc with upload instructions.
**If text overlay fails:** log error, upload raw image, flag: "⚠️ Text overlay failed — add text in TikTok natively: [text]"

**Cost estimate:** ~2 NB2 calls per product per week × 2 products = ~4 calls/week × ~$0.005 = ~$0.02/week. Overlay script = free (local Python).

---

## Step 4c: Trending Sound Research

Run one web search per product to find a trending TikTok sound this week that fits the content aesthetic. Include the recommendation in the Drive review doc.

**Search query pattern:**
```
trending TikTok sounds [current month YYYY] [niche: crypto / movies]
```
Also check: https://www.tokboard.com (trending sounds by category) if accessible.

**Sound selection criteria (in order):**
1. Currently trending (within last 7 days)
2. Fits the product aesthetic — Nash Satoshi: understated, analytical (lo-fi, ambient, minimal beats — NOT hype trap). Vista: cinematic, contemplative (film scores, indie folk, lo-fi — NOT pop vocals).
3. Not over-saturated (avoid sounds with 10M+ uses unless niche-relevant)

**Output format for Drive review doc:**
```
## 🎵 Recommended Sound This Week

Nash Satoshi: "[Sound name]" by [artist or @creator] — [why it fits / trend context]
Vista: "[Sound name]" by [artist or @creator] — [why it fits / trend context]

To add: open TikTok draft → tap the sound icon → search the name → select it → publish.
```

**If no strong trend found:** recommend a standing evergreen option:
- Nash Satoshi fallback: "Lofi Study" ambience or any lo-fi hip hop track with low use count
- Vista fallback: any Hans Zimmer or Ennio Morricone clip trending on TikTok

---

## Step 5: Upload to Drive

Generate a formatted markdown review file for each product — **do NOT upload queue.jsonl** (that's local-only operational data, not human-readable).

For each active product, write a review file to a temp path, then upload per product:

**Review file format** (`/tmp/vibe-review-[product_slug]-[YYYY-MM-DD].md`):

Include a `## 🖼️ Slides` section per TikTok piece — list each generated image's local path, screenshot instructions for JT-captured slides, and exact text overlay copy JT types in TikTok.
```markdown
# Vibe Marketing Review — [Product Name] — Week of [YYYY-MM-DD]

## X Posts ([N] generated)

### Post 1 [✅ APPROVED | ⚠️ REVIEW NEEDED]
**Account:** [@account]
**Hook:** [first line of post]
**Full post:**
[complete post text]
**Scores:** Hook: [N] | Platform fit: [N] | Authenticity: [N]
**Hook technique:** [technique used]
[If review_needed: **⚠️ Weak dimension:** [which one and why]]

[Repeat for each X post]

## TikTok Scripts ([N] generated)

### Script 1 [✅ APPROVED | ⚠️ REVIEW NEEDED]
**Account:** [@account]
**Hook (first 3 seconds):** [opening line]
**Full script:**
[script text with visual directions]
**Caption:** [caption text]
**Hashtags:** [hashtag list]
**Scores:** Hook: [N] | Platform fit: [N] | Authenticity: [N]

[Repeat for each TikTok script]

## Reddit Post ([N] generated | ⚠️ Check karma before posting)

### Post 1 [✅ APPROVED | ⚠️ REVIEW NEEDED | ⛔ SKIPPED]
**Subreddit:** [r/subreddit]
**Title:** [post title]
**Body:**
[post body]
**Scores:** Hook: [N] | Platform fit: [N] | Authenticity: [N]
[If skipped: **Skip reason:** [why]]

## LinkedIn Post ([N] generated | monthly only)
[Include if generated this month — same format as X posts]
```

**TikTok section of each review file must include this assembly block:**
```markdown
## 🎬 How to Assemble This TikTok — [Product Name]

All slides have text baked in — no manual text entry or screenshot capture needed.

1. Save ALL final slides from Drive to your camera roll (slide-01 through slide-last)
2. Open TikTok → + → select photos from your camera roll
3. Add slides IN ORDER: Slide 1 (hook) → middle slides → Last slide (CTA)
4. Tap the sound icon → search "[recommended sound from 🎵 section]" → select → publish
5. That's it.
Caption: [caption text]
Hashtags: [hashtag list]
```

**Upload — dynamic per product (loop over all active products):**
```bash
cd ~/.openclaw/workspace

# For EACH active product in registry (slug, name):
python3 scripts/drive_drafts.py \
  --title "[Product Name] — Vibe Review Week of [YYYY-MM-DD]" \
  --path "Content/Vibe Marketing/[Product Name]" \
  --file /tmp/vibe-review-[product_slug]-[YYYY-MM-DD].md
```

This pattern works for any product — current (Nash Satoshi, Vista) and future (Glow Index, etc.). Drive path is derived from `product.name` in the registry. No hardcoded product names.

If Drive upload fails: log the error, continue. queue.jsonl is the local source of truth.

---

## Step 5b: Push X posts to Notion Content Calendar (mandatory — runs after Drive upload)

For every approved X post in queue.jsonl this week, push an entry to the Notion Content Calendar.

**Script:** `python3 ~/.openclaw/workspace/scripts/notion-calendar-push.py --batch '[...]'`

**Batch entry format per X post:**
```json
{
  "platform": "X — @[account]",
  "date": "[YYYY-MM-DD]",
  "post": "[first 100 chars of content, newlines replaced with space]",
  "type": "Vibe",
  "week": "[week_of date]",
  "drive_link": "[product Drive link from Step 5]"
}
```

**Date assignment — staggered by product to prevent same-account collisions:**
- Products sharing the same X account (e.g. multiple products on @jts_14): assign different days
- Default stagger pattern for 2 active products on @jts_14 + 1 dedicated account:
  - Dedicated account (e.g. @NashSatoshi): **Mon / Wed / Fri** (days 0, 2, 4 from week_of)
  - @jts_14 product (e.g. Vista): **Tue / Thu / Sat** (days 1, 3, 5 from week_of)
  - If a 3rd product shares @jts_14: use Sun (day 6) as overflow, or push to the following Mon
- Never assign two posts to the same account on the same date
- For a single active product: spread Mon / Wed / Fri

**ICP variants (posts with `variation_of` set): DO NOT push to Notion Calendar.** These are A/B alternates stored in Drive. Only core posts (no `variation_of` field) go on the calendar. The calendar shows what to post, not every available option.

**Platform label:** `"X — [accounts.x from product-registry.json]"` — always read from the registry, never hardcode. For products sharing @jts_14, append the product name: `"X — @jts_14 (Vista)"`, `"X — @jts_14 (Glow Index)"`. If the product has no `accounts.x` value, skip and log a warning.

**What to push:** X posts only (core posts, no variants). TikTok scripts and Reddit posts are in Drive but not on the Notion Calendar.

**If batch push fails:** Log the error and continue. Calendar push is non-blocking — never abort the run for a Notion failure.

**For new products (first time generating):** The same logic applies. When a new product is added to product-registry.json and first content is generated, its X posts get pushed to the calendar automatically. No special case needed.

---

## Step 6: Send Telegram summary to JT

Send to channel=telegram, target=6608544825:

```
📱 Vibe Marketing — Week of [DATE]

**[Product Name]** → post X to [X account]
X ([N] posts) | TikTok ([N] scripts) | Reddit ([N] post) | LinkedIn ([N] — if generated this month)
→ X: [First hook line of each approved post]
→ TikTok: [First hook line of each script]
→ Reddit: [Post title] ⚠️ check karma before posting
[→ LinkedIn: [Post opening line] — post to linkedin.com/in/jon-trevor-somwaru]

[Repeat for each active product]

[If any review_needed:]
⚠️ [N] pieces need a second look — [which dimension fell short]

All content in Drive: [link]

📌 Posting mode: MANUAL — review in Drive, post from your devices.
[Remove this line once PostBridge auto-scheduling is active]

Reply with feedback after you post ("Nash Satoshi game theory post did well") — I'll log it to bias next week's generation.
```

If ALL products have 0 qualifying pieces: exit silently. No Telegram, no MC task.

**After sending Telegram: push one Mission Control task per product that has approved content:**
```bash
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Post [Product Name] content — week of [YYYY-MM-DD]",
    "description": "Review in Drive: [Drive link]. Post X posts to [X account], TikTok slides to [TikTok account], Reddit post to [subreddit]. Check karma before Reddit.",
    "status": "todo",
    "priority": "high",
    "assignee": "JT",
    "project": "passive-income",
    "sortOrder": 18
  }'
```

- One task per product (not one task for all products combined — keeps them individually trackable)
- sortOrder 18 keeps it near the top of HIGH but below Gil meeting (8) and LinkedIn (25)
- If a product has 0 approved pieces this week: no task for that product

---

## Step 6b: SEO Candidacy Evaluation (runs once per product, when conditions are met)

For each active product, check whether an SEO strategy is optimal. Run this check after content is queued but before state is updated.

**Skip this step entirely for a product if** `state.json` already has `seo_evaluated: true` for that product slug — evaluation has already run, no need to repeat every week.

**SEO candidacy criteria (score 1 point per Yes):**
1. Does the product have a web app with indexable URLs? (not just App Store / mobile-only)
2. Is there high search intent for the product's core content? (people actively Google "[topic] review", "[ingredient] worth it", "[product] score", "[category] comparison")
3. Does each piece of the product's output naturally map to a standalone page? (a product score page, an ingredient page, a category ranking page)
4. Is the product content evergreen? (rankings/reviews stay useful for months, not just 24 hours)
5. Does the product serve a niche with high-value commercial intent? (consumers researching before spending money, not just casual browsing)

**Decision rules:**
- 5/5 → SEO is optimal. Push an MC task immediately and flag to JT.
- 4/5 → SEO is worth designing. Push MC task, note the missing criterion.
- 3/5 or below → SEO is not worth building yet. Log reason in state.json, skip.

**When SEO is optimal (score ≥ 4), push this MC task:**
```bash
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Design SEO pipeline for [Product Name] — auto-generate indexed pages",
    "description": "SEO candidacy score: [X]/5. Criteria met: [list]. Missing: [list or none]. First step: audit the live web app structure and map which URLs exist. Strategy: auto-generate product pages, ingredient/topic pages, weekly best-of-category posts, JSON-LD schema markup, llms.txt. Target keywords: [2-3 specific examples based on product niche]. Activate after web app has indexable product URLs live.",
    "status": "todo",
    "priority": "medium",
    "assignee": "eve",
    "project": "passive-income",
    "sortOrder": 525
  }'
```

**Then include a one-line note in the Telegram summary:**
`🔍 SEO: [Product Name] scored [X]/5 — [pushed task / not yet ready because X]`

**After evaluation (pass or fail), update state.json:**
```json
"seo_evaluated": {
  "[product_slug]": {
    "score": 4,
    "date": "YYYY-MM-DD",
    "criteria_met": ["web app exists", "high search intent", "evergreen content", "commercial intent"],
    "criteria_missing": ["standalone page mapping"],
    "decision": "task_pushed"
  }
}
```

**Re-evaluation trigger:** If a product's `seo_evaluated` entry exists but `decision` is `"not_ready"`, re-run the check on the 1st Monday of each month (not every week). A product may become SEO-ready as the web app matures.

---

## Step 7: Update state

```json
{
  "last_run": "[ISO timestamp]",
  "last_successful_run": "[ISO timestamp]",
  "last_week_of": "[YYYY-MM-DD Monday]",
  "last_linkedin_month": "[YYYY-MM or null]",
  "last_angles_month": "[YYYY-MM or null]",
  "products_processed": ["slug1", "slug2"],
  "queue_count": [total pieces queued],
  "drive_link": "[Drive link or null]",
  "last_reddit_subreddit": {
    "nash-satoshi": "[r/subreddit or null]",
    "vista": "[r/subreddit or null]"
  },
  "last_scene_concept": {
    "nash-satoshi": "[concept number used this week — e.g. 2]",
    "vista": "[concept number used this week — e.g. 3]"
  },
  "seo_evaluated": {
    "[product_slug]": {
      "score": 0,
      "date": "YYYY-MM-DD",
      "criteria_met": [],
      "criteria_missing": [],
      "decision": "not_ready|task_pushed"
    }
  }
}
```

Update `last_scene_concept.[product_slug]` to the concept number used this week after image generation. Next run reads this and picks the next number in sequence (wrapping from 8 back to 1).

---

## Performance Feedback Loop

When JT tells me a piece performed well (in conversation), I immediately log it:

Append to `~/.openclaw/workspace/agents/vibe-marketing/performance-log.jsonl`:
```json
{
  "date": "[YYYY-MM-DD]",
  "product_slug": "[slug]",
  "platform": "[x|tiktok|reddit]",
  "theme": "[content theme — e.g. 'game theory explainer', 'solo dev build-in-public']",
  "format_type": "[list|story|comparison|hot_take|proof_point|behind_scenes|tutorial]",
  "hook_style": "[contrarian|stat|question|pattern_interrupt|social_proof]",
  "slide_count": "[number if TikTok carousel, null otherwise]",
  "cta_type": "[follow|download|comment|link_in_bio|cliffhanger]",
  "hashtags_used": ["#tag1", "#tag2"],
  "performance": "[great|good|ok|poor]",
  "metrics": "[views/saves/comments if JT reports them — otherwise null]",
  "notes": "[what JT said or what made it work — or why it flopped]",
  "icp_variant": "[ICP 1|ICP 2|ICP 3|null — which ICP this was written for]",
  "variation_of": "[original queue entry id, if this was a winner variation — otherwise null]"
}
```

The generation agent reads the last 4 weeks of this log (Step 1) and biases toward format_type + hook_style combinations marked "great" or "good."
Granular fields enable pattern detection: e.g. "comparison format + contrarian hook = consistently great on Nash Satoshi TikTok."
This is how the system improves without needing analytics API access.

---

## Hard Rules

1. **NEVER post on JT's behalf.** Generate and queue only. JT approves and posts manually.
2. **NEVER cross-contaminate products.** Nash Satoshi posts never mention Vista. Vista never mentions Nash Satoshi.
3. **Skip `status: "pending"` products.** No exceptions.
4. **Reddit = value first, always.** If you can't write a post that leads with genuine value, skip it. Don't force a promotion into a community space.
5. **TikTok = faceless content only.** No on-camera formats for any product. Slideshows and AI UGC avatars only.
6. **Keep total runtime under 12 minutes.** Max ~10 pieces per week at current scale.

---

## Adding a New Product

When JT says "Eve, add [product] to vibe marketing":
1. Add a new entry to `product-registry.json` with `status: "active"`
2. Fill in all fields including `platform_config` for each intended platform
3. Next Monday 4:45AM picks it up automatically — no other changes needed

## TikTok Future Note
When TikTok automated posting is ready: add `"tiktok_post_api": true` to a product's `platform_config.tiktok` entry. The queue format is already structured for it — no architecture change needed.

---

## Phase 2: AI UGC Talking Head Videos (activate after carousels have traction)

An AI-generated avatar persona acts as a user of each product. Eve handles the full pipeline autonomously — script → voice → video → Drive. JT reviews and posts.

### Activation trigger (specific — not vague "traction")
All three conditions must be met before activating Phase 2 for a product:
1. Carousels posting consistently for ≥4 weeks
2. At least one carousel has hit 500+ views OR the account has 50+ followers
3. JT says go

This is logged in `future-signals.md`. Eve checks it during weekly synthesis.

---

### Preferred tool: HeyGen API (primary)
HeyGen handles avatar + lipsync in one step. No separate lipsync tool needed. Has a REST API Eve can call programmatically. ~$29/mo covers weekly volume at current scale.

Alternative if HeyGen is unavailable or cost-prohibitive: Hedra (also has API, good lipsync quality). RunPod/LatentSync is the self-hosted fallback — more setup, but $0 SaaS cost, ~$0.20–$0.40/video GPU cost.

**Do NOT use:** WAN (it's a video generation model, not a lipsync tool), InfiniteTalk (deprecated), any tool that requires manual browser interaction.

---

### Pipeline (Eve runs all steps autonomously)

**Step 1 — Avatar character image (one-time per product, reused every week)**

Generate via NB2 (`google/gemini-3.1-flash-image-preview`). One character per product — same image reused across all videos. Consistency builds recognizability.

Prompt approach: full descriptive visual language (NOT hex codes or pixel specs). Include `avoid` guidance. Describe like a casting brief.

Character briefs per product:
- **Nash Satoshi:** 28–35 male, casual tech aesthetic — think someone who actually reads crypto research at 11PM. Phone or laptop subtly in frame. Neutral background, slightly out of focus. Natural lighting, not studio. Smartphone snapshot quality, not a photoshoot.
  Avoid: suits, trading desk setups, anything that looks like a crypto influencer, excessive jewelry, sunglasses.
- **Vista:** 22–32, any gender, film-person energy — the kind of person who has opinions about cinematography. Cozy indoor setting, warm dim light, movie posters or bookshelves softly blurred in background. Candid feel, not posed.
  Avoid: glamorous styling, bright lighting, anything that looks like an Instagram influencer.

Save to: `agents/vibe-marketing/characters/[product_slug]-character.png`
Reuse this file every week — do NOT regenerate unless JT requests a new persona.

**Step 2 — Script**
- Target: 30–45 seconds read aloud at natural conversational pace (not 60s — attention drops fast)
- Structure:
  - Hook (0–3s): "You"-focused, pattern interrupt. The viewer decides to keep watching here.
  - Problem (3–12s): the specific frustration or gap this product solves. One sentence.
  - Solution (12–35s): what the product does, shown through a specific use case. One real result. Natural speech — NOT a product description.
  - CTA (35–45s): one action, one reason. "Follow for weekly rankings" or "Download on the App Store — link in bio."
- Write script with exact word count noted. 125 words ≈ 45 seconds at natural pace.
- Mark emphasis words (these help voice model hit the right rhythm).

**Step 3 — Voice via ElevenLabs API**
- ElevenLabs generates TTS audio directly from the script text. Call the API programmatically.
- Voice selection: choose a voice that matches the character's demographic and energy. ElevenLabs voices list: `GET https://api.elevenlabs.io/v1/voices`
- Model: `eleven_turbo_v2_5` (fastest, good quality, lower cost) for drafts. `eleven_multilingual_v2` for final if quality needs to be higher.
- Output: `.mp3` file, save to `agents/vibe-marketing/audio/[product_slug]-[YYYY-MM-DD].mp3`
- Cost: ~$0.002/word at Starter tier. A 125-word script ≈ $0.25.
- Do NOT use CapCut for voice processing — ElevenLabs output goes directly to lipsync. The "CapCut normalization" step described previously was incorrect and would degrade audio quality.

**Step 4 — Lipsync + video via HeyGen API**
- Input: character image (Step 1) + ElevenLabs audio (Step 3)
- HeyGen endpoint: `POST https://api.heygen.com/v2/video/generate` with `talking_photo` mode
- Output: MP4, 9:16, 1080×1920
- Expected render time: 2–5 minutes per video. Poll for completion before proceeding.
- Save to: `agents/vibe-marketing/generated-videos/[product_slug]-[YYYY-MM-DD].mp4`
- Cost: covered under HeyGen plan (~$29/mo, 25 videos/mo limit — more than enough for 2 products × 1 video/week = 8/mo)

**Step 5 — Captions file (auto-generated)**
- Generate `.srt` captions from the script (timestamp each line using word count ÷ speaking pace)
- TikTok auto-captions on upload are an acceptable alternative — flag this in Drive doc
- Save to: `agents/vibe-marketing/generated-videos/[product_slug]-[YYYY-MM-DD].srt`

**Step 6 — Upload to Drive and notify JT**
- Upload video + captions to `Content/Vibe Marketing/[Product Name]/UGC Videos/`
- Drive doc includes: script, voice notes, caption file path, posting instructions (add trending sound in TikTok before publishing — this is the single biggest organic reach lever)
- Telegram summary includes video Drive link and one-line posting note

**JT's only manual step:** add a trending sound in TikTok before hitting publish. TikTok's native audio library is the fastest way — pick a trending sound in the right niche.

---

### Queue format addition (when Phase 2 active)
Add to queue entries:
```json
{
  "content_type": "ugc_video",
  "script": "[full script text]",
  "script_word_count": 125,
  "emphasis_words": ["specific", "actually", "ranked"],
  "voice_id": "[ElevenLabs voice ID used]",
  "character_image_path": "agents/vibe-marketing/characters/[product_slug]-character.png",
  "audio_path": "agents/vibe-marketing/audio/[product_slug]-[YYYY-MM-DD].mp3",
  "video_path": "agents/vibe-marketing/generated-videos/[product_slug]-[YYYY-MM-DD].mp4",
  "caption_path": "agents/vibe-marketing/generated-videos/[product_slug]-[YYYY-MM-DD].srt",
  "caption": "[TikTok caption text]",
  "hashtags": "[hashtag list]",
  "posting_note": "Add trending sound before publishing"
}
```

---

### Runtime impact when Phase 2 is active
- Add ~5–8 minutes to total cron runtime per product (API calls + polling for video render)
- Cron timeout should be bumped to 2400s when Phase 2 activates
- ElevenLabs and HeyGen API keys must be added to `~/.config/env/global.env` before first run
