# X Algorithm Reference — For You Feed (Phoenix/xAI, 2025)
> Source: https://github.com/xai-org/x-algorithm
> Use this before finalizing any post for JT. Optimize for the signals below.

## How Posts Get Ranked

The Phoenix transformer predicts probabilities for each action. Weighted score = Σ(weight × P(action)).

### Positive signals (boost your post — ranked by weight, highest first):
1. **Replies** — highest weight. A reply means the post made someone stop and engage. Always include a reply hook.
2. **Reposts** — reach multiplier. Posts that feel shareable/quotable get reposted.
3. **Quotes** — strong signal. Even disagreement = amplification.
4. **Likes** — baseline engagement. Important but lower weight than replies/reposts.
5. **Bookmarks / saves** — signals high-value content worth returning to.
6. **Profile clicks** — someone got curious about the author. Good hook + credibility cue drives this.
7. **Dwell time** — how long someone pauses. Broken formatting, line-by-line reveals, and counterintuitive statements increase dwell.
8. **Follows** — the ultimate signal. Rare but highest long-term value.

### Negative signals (suppress your post — avoid triggering these):
- **Fast scroll / low dwell** — weak hook or generic post; the feed learns people skip you.
- **Block / Mute** — tanks reach immediately.
- **"Not interested"** — soft suppression.
- **Report** — hard suppression.
- **Ad-safety / sensitive labels** — NSFW, gore, violence, ragebait, conspiracy framing, or other advertiser-hostile categories can dock distribution. Avoid bait formats even when they would get replies.
- **Slop / low-originality score** — repeated hooks, obvious AI filler, copied creator formats without JT-specific proof, AI-video slop, and generic engagement bait can get suppressed and damage account-level quality over time.

## What This Means for Post Construction

### Structure rules (derived from algorithm weights):
- **Open with a reply hook** — every post should have a line that makes someone want to respond, agree, disagree, or add to. This is the #1 signal.
- **Dwell bait** — use short punchy lines. Break text so the reader has to keep scrolling within the post itself. No wall of text.
- **Repost trigger** — include one line that someone would want to put their name on. A sharp take, a memorable analogy, a counterintuitive insight.
- **Bookmark trigger** — package one saved-useful artifact: teardown, checklist, ranked list, workflow map, mistake list, or “what changed / what to do now.” Alex Finn’s 2026-05-15 algorithm-code thread worked because the wrapper promised source-code compression, not just a take.
- **Profile click bait** — your name should feel like an authority on the topic by the end of the post. State something specific + credible.
- **Never beg for engagement** — "like and repost if you agree" trains the algorithm to see your audience as low-quality. Let the content earn it.

### Format rules:
- **Line breaks matter** — single sentences per line outperform paragraphs. Forces dwell.
- **No links in the post** — links get suppressed by the algorithm (user leaves X = bad signal). If linking, put it in a reply.
- **Images outperform plain text** for reach. Video outperforms images. But text-only posts with high reply rates can match media posts.
- **Polls** — useful for reply-equivalent signal at lower effort from the audience.
- **Thread openers** — the first post in a thread gets the algorithm boost. Make it the strongest standalone hook.
- **Avoid feed spam** — the feed appears to apply author-level repetition/decay. One strong X post beats several mediocre posts close together. Do not schedule multiple generic JT/Nash/Dynasty posts into the same audience window unless each has distinct proof and purpose.

### Timing rules:
- **First 30 minutes are everything** — velocity of early engagement determines if the algorithm amplifies. Post when your audience is active (typically 8–10AM or 6–9PM EST for JT's niches).
- **Reply to your own post immediately** — adds content to the thread, signals active engagement, boosts the original post.
- **Engage back fast** — replying to comments within the first hour signals healthy conversation, keeps the post in feeds.

### Content rules:
- **Specificity > generality** — "AI saved a contractor $1,500" beats "AI saves businesses money"
- **Contrarian > consensus, but not ragebait** — disagreement can drive replies/quotes, but ad-safety and negative feedback matter. Use useful tension, not outrage bait.
- **Personal > generic** — "I learned X from 6 years at Spectrum" outperforms "here are X tips"
- **Original proof > copied pattern** — extracting a swipe mechanic is fine; copying another creator's hook, cadence, image-thread bait, or generic “algorithm secrets” wrapper is slop. Every post needs JT-specific proof, data, build experience, or a real source inspected.
- **Source-teardown format works** — when a platform/tool/client workflow changes, use: `[Platform] changed [specific thing] → I reviewed [source/artifact] → here are the practical implications`. Only use if we actually inspected the source. No fake “I read 24,000 lines” claims.
- **Avoid low-quality/AI-spam signals** — do not post obvious AI filler, duplicated hooks, engagement-bait phrasing, shock claims without source, or image-thread bait with no real substance. These may get short-term reach but damage audience quality and can trigger downranking/negative feedback.
- **Short > long** (for reach) — under 280 chars gets more impressions. Longer posts get more profile clicks if they hook well.

## JT's Niches + Relevant Signals

| Niche | Best Format | Reply Hook Strategy |
|-------|------------|-------------------|
| AI Consulting | Hot Take, Data Drop | Challenge a common vendor claim |
| AI Agents | Bold Prediction, Contrarian | Predict something specific about where agents are going |
| Crypto / x402 | Data Drop, Contrarian | State a position on a coin/narrative most people haven't heard |
| Job Market | Personal Story, Data Surprise | Share something from your own job search experience |
| Personal Brand | Story, Behind-the-scenes | Show the reality behind a win or failure |

## Checklist Before Finalizing Any Post

- [ ] Does the first line make someone want to reply, disagree, or keep reading?
- [ ] Is it broken into short lines (dwell)?
- [ ] Is there one line someone would want to repost or quote?
- [ ] No links in the post body (move to reply)?
- [ ] Under 280 chars for pure reach, or hooks hard enough in first line for longer format?
- [ ] Does it sound like JT, not a generic AI tweet?
- [ ] References swipe file pattern for this niche/format without copying the creator's hook/cadence?
- [ ] If using a “source teardown” wrapper, did we actually inspect the source/artifact and save the evidence?
- [ ] Does it avoid obvious AI filler, duplicated hooks, and engagement-bait language that could trigger negative feedback?
- [ ] Is this the only post aimed at this audience/window, or is there a strong reason to publish another one today?
- [ ] Is it advertiser-safe and free of ragebait, conspiracy framing, NSFW/gore/violence hooks, or “watch this fight” style bait?
