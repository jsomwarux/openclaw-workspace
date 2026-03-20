# Launch Kit Agent — Eve

Triggered when a new product is added to `agents/vibe-marketing/product-registry.json` with `"status": "active"` and no existing `launch_kit_generated` field.

Produces a complete, ready-to-execute launch package for the product. Output is drafts only — JT reviews and executes.

---

## Trigger Condition

Run when:
1. A product in `product-registry.json` has `"status": "active"` AND
2. `"launch_kit_generated": true` is NOT present in that product's entry

Run by: overnight agent (Step 2 task selection) OR manually when JT adds a new product.

After completing, add `"launch_kit_generated": true` and `"launch_kit_date": "YYYY-MM-DD"` to the product's entry in `product-registry.json`.

---

## Output Location

All output written to: `~/.openclaw/workspace/agents/launch-kit/kits/[product-slug]/`

---

## Run Procedure

### Step 1: Load Product Context

Read `agents/vibe-marketing/product-registry.json` for the target product.
Extract: name, description, target_audience, url, platforms, accounts, voice, proof_points, content_themes.

Also read:
- `agents/vibe-marketing/brands/[product-slug]/voice.md` (if exists)
- `agents/vibe-marketing/brands/[product-slug]/product.md` (if exists)
- `agents/vibe-marketing/brands/[product-slug]/icp.md` (if exists)
- `memory/content-voice.md` — JT's cross-product voice rules (no em dashes, etc.)

### Step 2: Reddit Research

For the product's target audience, find the 5 best subreddits.

Search: `site:reddit.com [niche] community recommendations` and `r/[niche] posting rules karma requirements`

For each subreddit found, determine:
- Estimated karma requirement (check subreddit rules or sidebar)
- Account age requirement
- Whether promotional posts are allowed and how they must be framed
- Whether this is a "participate genuinely" sub or allows direct product posts

Output → `subreddits.md`:
```markdown
# Reddit Strategy — [Product Name]

## Target Subreddits (ranked by fit)

| Subreddit | Members | Karma req | Age req | Promo allowed | Strategy |
|---|---|---|---|---|---|
| r/[name] | [N]K | [N] comment karma | [N] days | Yes/No/Soft | [participate/share/mention naturally] |

## Launch Post Draft — r/[best fit subreddit]
[Full post draft — title + body. No promotional language. Lead with value.]

## Comment Strategy
[2-3 threads per subreddit to target for early comments. Frame as participating, not promoting.]

## Account Notes
[Which Reddit account to use. If new account needed: say so + karma-build subreddits to use first.]
```

### Step 3: UGC Creator Research

Find 10 TikTok/Instagram creators in the product's niche who post about relevant topics.

Criteria:
- 10K-500K followers (micro to mid-tier — better engagement, lower cost)
- Posts content directly relevant to the product's audience
- Has an email or DM contact visible in bio
- NOT already a brand shill (check for obvious paid posts dominating their feed)

Search: `site:tiktok.com [niche] creator` and relevant hashtags from the product registry.

Output → `ugc-creators.md`:
```markdown
# UGC Creator Outreach — [Product Name]

## Creator Shortlist

| Creator | Platform | Followers | Niche fit | Contact | Notes |
|---|---|---|---|---|---|
| @[handle] | TikTok | [N]K | High/Med | [email or DM] | [why they fit] |

## Outreach DM Draft (10 creators, personalized per creator)

### @[handle]
**Platform:** TikTok
**Why them:** [1 sentence — specific to their content]
**DM:**
[Short, casual, direct. Under 100 words. Mention the product, what you're asking for (1 video), and the rate ($15-30/video flat + $1k/1M views performance). No em dashes.]

[Repeat for each creator]

## Rates to offer
- Flat fee: $20/video (standard)
- Performance: $1,000 per 1M views
- Deliverable: 1 video, 30-60 seconds, honest review of the product

## Notes
JT reviews all DMs before sending. Do not send anything automatically.
```

### Step 4: Demo Video Brief

Write a 60-second demo video brief that JT or a UGC creator can follow.

Output → `demo-video-brief.md`:
```markdown
# Demo Video Brief — [Product Name]

## Hook (0-5 seconds)
[One sentence that creates curiosity or states a relatable problem]

## Problem (5-15 seconds)
[What frustration does this product solve? Be specific.]

## Solution reveal (15-40 seconds)
[Show the product doing the thing. Screen recording, or narrated walkthrough.]
[Key features to show: [list]]

## Social proof (40-50 seconds)
[One proof point: "Live on the App Store" / "Built by one person" / whatever is true]

## CTA (50-60 seconds)
[Simple, low friction: "Download on the App Store" / "Link in bio" / "Check it out at [url]"]

## Style notes
[Matches product voice from registry. Tone: [X]. No talking head required if product is faceless.]

## Post caption draft (for X and TikTok)
[Short caption to accompany the video. Under 150 chars. No em dashes.]
```

### Step 5: Build-in-Public Post Pack

Write the first 3 build-in-public X posts for the product launch.

Rules: load `memory/content-voice.md` before writing. Apply all voice rules. No em dashes. No contrarian flip as default opener. Lead with the reader's problem or the honest situation.

Output → `build-in-public-posts.md`:
```markdown
# Build-in-Public Posts — [Product Name]

## Post 1 — Launch announcement
[Single post, 6-15 words. Standalone. The thing is live. State it plainly.]

## Post 2 — Why I built this (short take)
[2-3 sentences. The honest frustration that caused this to exist.]

## Post 3 — What surprised me building it
[Something specific and non-obvious from the build process. Practitioner-level detail.]

## Usage notes
Post in 8-10AM or 6-9PM EST window. Post 1 first. Space them 2-3 days apart minimum.
```

### Step 6: App Store Optimization (if App Store product)

Only run if `url` contains `apps.apple.com` or product description mentions App Store.

Research the top 5 competing apps. Identify high-volume, low-competition keywords.

Output → `aso-brief.md`:
```markdown
# App Store Optimization — [Product Name]

## Current state
[Brief summary of what's currently in the listing, if known]

## Competitor analysis
| App | Rating | Key keywords | Weakness |
|---|---|---|---|

## Recommended keywords
- Title field: [product name] + [primary keyword]
- Subtitle (30 chars): [keyword-rich subtitle]
- Keyword field suggestions: [comma-separated list, 100 chars total]

## Screenshot recommendations
[What each of the 3-5 screenshots should show, in order]

## Description rewrite
[Full App Store description, under 4000 chars. First 3 lines are most important — show before "more".]

## Rating strategy
[When and how to prompt for ratings — after specific in-app actions, not immediately on launch]
```

### Step 7: Launch Sequence

Write a prioritized 30-day launch sequence for JT to follow.

Output → `launch-sequence.md`:
```markdown
# 30-Day Launch Sequence — [Product Name]

## Week 1 — Foundation
- Day 1: [specific action]
- Day 2: [specific action]
...

## Week 2 — Amplify
...

## Week 3-4 — Compound
...

## Metrics to watch (weekly)
- [metric]: target [N]
- [metric]: target [N]

## When to declare traction
[Specific threshold that means the distribution is working]
```

### Step 8: Package and Push

1. Write a summary file → `kit-summary.md`:
```markdown
# Launch Kit — [Product Name] — [DATE]

## What's in this kit
- subreddits.md — 5 target subreddits + launch post draft
- ugc-creators.md — 10 creator targets + DM drafts
- demo-video-brief.md — 60-second video script
- build-in-public-posts.md — 3 launch posts
- aso-brief.md — App Store optimization (if applicable)
- launch-sequence.md — 30-day action plan

## Highest ROI actions (do these first)
1. [action]
2. [action]
3. [action]

## JT manual steps
- [ ] Review and send UGC creator DMs
- [ ] Record or commission demo video
- [ ] Implement ASO recommendations in App Store Connect (if applicable)
- [ ] Post build-in-public posts on X
- [ ] Post to top subreddit (after karma threshold met)
```

2. Upload entire kit to Drive:
```bash
for f in subreddits.md ugc-creators.md demo-video-brief.md build-in-public-posts.md aso-brief.md launch-sequence.md kit-summary.md; do
  if [ -f "~/.openclaw/workspace/agents/launch-kit/kits/[slug]/$f" ]; then
    cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py \
      --title "[Product Name] Launch Kit — $f" \
      --path "Consulting/[Product Name]/Launch Kit" \
      --file "agents/launch-kit/kits/[slug]/$f"
  fi
done
```

3. Push Mission Control task:
```bash
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "🌙 Review: [Product Name] Launch Kit ready — 6 files",
    "description": "Full launch kit generated for [Product Name].\n\nFiles: agents/launch-kit/kits/[slug]/\n\nAction: Review kit-summary.md first, then work through the sequence.\n\nHighest ROI: UGC creator DMs + ASO (if App Store) + first build-in-public post.",
    "status": "todo",
    "priority": "high",
    "sortOrder": 5,
    "assignee": "jt",
    "project": "passive-income"
  }'
```

4. Update product registry — add to the product's entry:
```json
"launch_kit_generated": true,
"launch_kit_date": "YYYY-MM-DD",
"launch_kit_path": "agents/launch-kit/kits/[slug]/"
```

---

## Hard Constraints
- No em dashes in any output (message bodies, post drafts, video briefs)
- All DM drafts to Drive — never send directly
- UGC rate guidance: $20/video flat, $1k/1M views performance — do not deviate without JT approval
- Reddit post drafts must be native to the community — no obvious product promotion framing
- ASO section: never fabricate competitor data — research or skip
- If a brand file (voice.md, product.md, icp.md) exists, it overrides generic assumptions

---

## Cost Estimate
Typical run: $0.30-0.60 per product (research + drafting). Fits within overnight $1.50 cap as a standalone task.
