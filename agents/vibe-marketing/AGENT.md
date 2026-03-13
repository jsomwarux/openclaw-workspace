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

## Step 1: Load context

1. Read `~/.openclaw/workspace/agents/vibe-marketing/product-registry.json`
   - Find all products with `status: "active"`
   - If none: update state.json with `last_run` and exit

2. Read `~/.openclaw/workspace/memory/content-voice.md`
   - Apply JT's voice principles — direct, specific, no filler, no marketing speak

3. Read `~/.openclaw/workspace/agents/vibe-marketing/platform-rules.md`
   - Apply ALL platform-specific rules during generation
   - Pay special attention to: Universal banned words, TikTok "you"-focused rule, Reddit cardinal rule, scoring gate

4. Read `~/.openclaw/workspace/agents/vibe-marketing/performance-log.jsonl`
   - Load last 4 weeks of entries
   - Identify: which themes/formats scored "good" or "great" per product
   - Use this to bias generation toward what's worked — more of those formats, fewer of what flopped
   - If file is empty or fewer than 4 entries: generate based on themes in registry, no bias applied yet

5. **Niche trend research (web_search only — 2 searches max, one per active product)**
   - Before generating content, run a quick search for what's currently trending in each product's niche
   - Nash Satoshi: `"trending crypto TikTok content [current month]"` or `"viral crypto game theory posts"`
   - Vista: `"trending movie TikTok [current month]"` or `"viral film review content format"`
   - Goal: calibrate hooks to what's getting traction NOW, not generic templates
   - Rule: **research what's working, then generate** — not the other way around
   - This is cheap (web_search, no X API). Skip if budget is critically tight.

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

---

### TikTok Content

**Current mode (until Postiz + TikTok connected):** Generate scripts JT records himself.
**Slideshow mode (once Postiz connected):** Generate 6 OpenAI images per post + caption + hashtags. Agent uploads drafts to Postiz automatically. JT adds music and publishes.

#### Image Generation Quality Rules (apply when in slideshow mode)
- Use JSON-structured prompts, NOT text prompts. Text prompts produce AI-looking output.
- Lock the scene architecture across all 6 slides (dimensions, position, camera angle, environment). Only the style/progression changes between slides — this is what makes transformation feel real.
- Always include an `"avoid"` array: `["CGI", "AI-generated look", "smooth plastic skin", "studio lighting", "beauty filters", "perfect symmetry"]`. This array does most of the heavy lifting.
- Specify camera imperfections explicitly: `"device": "iPhone", "lens": "front-facing", "photo_characteristics": ["minor digital noise", "realistic smartphone dynamic range", "slight motion softness"]`
- **Color grading trick:** Find a Pinterest reference image with the right vibe for the product. Use Gemini to extract a detailed JSON of that image's color grading, lighting, and composition. Use that JSON as the generation reference. Eliminates the grey/washed-out default look.
- Slide 1 text overlay: 6.5% of image height font, positioned 30% from top, manual line breaks every 4–6 words. Full hook must fit on slide 1 — never split across slides.
- 6-slide structure: Hook → Problem → Discovery → Transformation 1 → Transformation 2 → CTA

#### Script Structure (current mode — JT records)
Generate a **script** JT can follow when recording — not a finished post.
Structure every TikTok script as:

```
[HOOK — 0-3 seconds]
One line. "You"-focused, not "I"-focused. Contrarian claim, surprising stat, or provocative question.
✅ Nash Satoshi: "You're evaluating crypto completely wrong — and it's costing you."
✅ Vista: "You've been tracking your movie ratings the wrong way."
❌ Never: "I built a movie app..." or "I discovered something about crypto..."

[BODY — 20-45 seconds]
3-4 punchy points. Short sentences. Write how JT TALKS, not how he writes.
Include visual directions in [brackets]: [show screen recording], [cut to results], [zoom on data point]
Deliver real value — don't tease without paying off.

[CTA — 5-10 seconds]
Reason to follow OR clear next action. Not just "follow me."
Tease next video, ask a question, or create a cliffhanger.
```

- Scripts must be 30–60 seconds when read aloud at conversational pace
- Include visual directions in [brackets] throughout — JT uses these when recording
- Generate a **caption separately from the script** — never name the product in the caption body. Use pov: framing or the conflict formula (`[Another person] + [conflict/doubt] → showed them [result] → they changed their mind`). Mystery drives comments; comments drive reach.
- List `tiktok.hashtags` from the registry as a separate field in the queue output, not in the script itself
- Queue output for TikTok must include three separate fields: `script` (what JT says on camera), `caption` (what goes in the TikTok caption — no product name), `hashtags` (separate, 4–5 tags)

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
For products where JT IS the story — build-in-public, solo dev, personal brand energy. The audience follows JT as a creator, not just the product.
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

## Step 3: Score each piece of content

Score every generated piece on three dimensions, each 1–10.
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

**Also apply before scoring:**
- Check against Universal banned words (platform-rules.md). Any banned word = automatic discard.
- Check for banned emojis (🚀🔥💯) or excessive exclamation points. Present = automatic discard.

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

## Step 5: Upload to Drive

Generate a formatted markdown review file for each product — **do NOT upload queue.jsonl** (that's local-only operational data, not human-readable).

For each active product, write a review file to a temp path, then upload per product:

**Review file format** (`/tmp/vibe-review-[product_slug]-[YYYY-MM-DD].md`):
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

**Upload per product to its own Drive folder:**
```bash
cd ~/.openclaw/workspace

# Nash Satoshi
python3 scripts/drive_drafts.py \
  --title "Nash Satoshi — Vibe Review Week of [YYYY-MM-DD]" \
  --path "Content/Vibe Marketing/Nash Satoshi" \
  --file /tmp/vibe-review-nash-satoshi-[YYYY-MM-DD].md

# Vista
python3 scripts/drive_drafts.py \
  --title "Vista — Vibe Review Week of [YYYY-MM-DD]" \
  --path "Content/Vibe Marketing/Vista" \
  --file /tmp/vibe-review-vista-[YYYY-MM-DD].md

# Future products: --path "Content/Vibe Marketing/[Product Name]"
```

If Drive upload fails: log the error, continue. queue.jsonl is the local source of truth.

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

If ALL products have 0 qualifying pieces: exit silently. No Telegram.

---

## Step 7: Update state

```json
{
  "last_run": "[ISO timestamp]",
  "last_successful_run": "[ISO timestamp]",
  "last_week_of": "[YYYY-MM-DD Monday]",
  "last_linkedin_month": "[YYYY-MM or null]",
  "products_processed": ["slug1", "slug2"],
  "queue_count": [total pieces queued],
  "drive_link": "[Drive link or null]",
  "last_reddit_subreddit": {
    "nash-satoshi": "[r/subreddit or null]",
    "vista": "[r/subreddit or null]"
  }
}
```

---

## Performance Feedback Loop

When JT tells me a piece performed well (in conversation), I immediately log it:

Append to `~/.openclaw/workspace/agents/vibe-marketing/performance-log.jsonl`:
```json
{
  "date": "[YYYY-MM-DD]",
  "product_slug": "[slug]",
  "platform": "[x|tiktok|reddit]",
  "theme": "[content theme or format that performed — e.g. 'game theory explainer', 'solo dev build-in-public']",
  "performance": "[great|good|ok|poor]",
  "notes": "[what JT said or what made it work]"
}
```

The generation agent reads the last 4 weeks of this log (Step 1) and biases toward formats marked "great" or "good."
This is how the system improves without needing analytics API access.

---

## Hard Rules

1. **NEVER post on JT's behalf.** Generate and queue only. JT approves and posts manually.
2. **NEVER cross-contaminate products.** Nash Satoshi posts never mention Vista. Vista never mentions Nash Satoshi.
3. **Skip `status: "pending"` products.** No exceptions.
4. **Reddit = value first, always.** If you can't write a post that leads with genuine value, skip it. Don't force a promotion into a community space.
5. **TikTok = scripts, not posts.** JT records himself — write what he says, not a caption.
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

## Phase 2: AI UGC Talking Head Videos (build after carousels are live and getting views)

Instead of JT recording on camera, an AI-generated character acts as a user persona for each product. Works for Nash Satoshi ("I track my crypto portfolio with this") and Vista ("I've logged 200+ movies with this app"). No authenticity risk — it's a user persona, not JT.

### Pipeline per product
Each product gets ONE consistent character image (generated once, reused across all videos):

**Step 1 — Character (Nano Banana Pro JSON)**
- Generate a realistic user persona that matches the product's target audience
  - Nash Satoshi: 28–35 male, casual/tech vibe, phone or laptop in frame
  - Vista: 22–30 either gender, couch/cozy setting, movie poster background optional
- Use full JSON prompting — NOT text prompts. Include `"avoid"` array, camera imperfections, skin texture details
- Color grading: find Pinterest reference → upload to Gemini → extract color JSON → paste as reference
- Save as `agents/vibe-marketing/characters/[product_slug]-character.png` — reuse this image for every video

**Step 2 — Script**
- 30–60 seconds read aloud at conversational pace
- Hook (0–3s): "You"-focused, pattern interrupt
- Body (20–45s): specific use case, one real result, natural speech patterns
- CTA (5–10s): follow/download/try — give a reason
- Read aloud and time it with a stopwatch. That exact duration = video length in Step 4. Off by even 3 seconds = broken lipsync.

**Step 3 — Voice (ElevenLabs + CapCut two-step)**
- Generate audio from script in ElevenLabs
- Run through CapCut voice change first (any base voice — normalizes artifacts)
- Then apply final ElevenLabs voice on top of normalized audio
- Skipping the CapCut step = audio that sounds "off" even if quality is technically high

**Step 4 — Lipsync (WAN lipsync or InfiniteTalk on RunPod)**
- Input: character image (Step 1) + normalized voice audio (Step 3)
- Output: talking head video with lip movement synced to audio
- Use for 30–60 second single-speaker videos. Use Kling multi-shot for shorter multi-scene ads.

**Step 5 — Edit (CapCut)**
- Captions, CTA overlay, music, trim
- Export 9:16 for TikTok/Reels

### Queue format addition (when Phase 2 active)
Add `"content_type": "ugc_video"` to queue entries. Fields: `script`, `caption`, `hashtags`, `character_image_path`, `voice_notes` (which ElevenLabs voice, any tone direction).

### When to build Phase 2
- Carousels are live and posting consistently
- At least one product has TikTok traction (views, follows, comments)
- JT says go
