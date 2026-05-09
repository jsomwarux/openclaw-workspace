# Reddit Karma & Reputation Strategy

## The Goal
Build 500+ post and comment karma in highly engaged, sharp niche subreddits to establish JT and his brands as technical, systems-level authorities.

## 1. Nash Satoshi / Crypto Game Theory
**Subreddit targeting rule:** Pick active, discussion-native communities first. Never choose a subreddit only because the theme matches. Check latest posts + rules before drafting.

**Current crypto target stack:**
- `r/defi` — Primary for incentive alignment, reflexivity, protocol durability, LP/user/token-holder coordination. Best fit for game-theory discussion. No external links. If discussing a named protocol, include risks and audit context; otherwise keep it general.
- `r/CryptoMarkets` — Backup for broader market-structure takes. Good for attention-vs-durability, signal quality, and trader psychology. No shills, no links, no specific token recommendations.
- `r/ethtrader` — Only when the post is explicitly ETH/L2/restaking related. Avoid polished theory unless tied to a current ETH-market question.
- `r/CryptoTechnology` — Use for technical architecture only, not growth. Must not read like coin promotion.
- `r/ethfinance` — Do **not** target for daily growth drops unless recent activity proves it is active again. It is too inactive for growth right now.

**Hard mod-safety rules:**
- No Nash Satoshi link, CTA, launch mention, referral language, or tool-promo phrasing.
- Do not post the same crypto draft to multiple subreddits on the same day.
- Prefer neutral discussion questions over product-origin stories.
- If the copy contains a product name, URL, “I built,” or “my app/tool,” it needs extra scrutiny and usually should be rewritten.

**The Content Angle:**
Post architectural/game-theory takeaways without shilling:
- “Do DeFi protocols overvalue attention and undervalue incentive alignment?”
- “Attention is probably the weakest crypto signal people over-rely on.”
- “The useful distinction is hype momentum vs durable coordination incentives.”

## 2. Dynasty Fantasy Football (@dynastyjig)
**Access status:** `r/DynastyFF` is currently gated for JT — Reddit says he needs an established reputation before contributing. Do not target it until enough account karma/reputation is built.

**Current fantasy target stack until DynastyFF unlocks:**
- `r/Fantasy_Football` — Primary lower-friction target. Active advice/keeper/dynasty-adjacent posts; rules are basic: respectful, no politics, no league recruiting. Best for helpful comments and practical roster-structure takes.
- `r/fantasyfootballadvice` — Secondary target. Active team-advice posts with dynasty flairs. Best for comments, not abstract theory posts.
- `r/fantasyfootball` — Use for broader redraft/offseason macro comments. Avoid standalone dynasty-only posts unless clearly relevant to NFL draft impact.
- `r/DynastyFF` — Future target only after account can contribute.

**The Content Angle:**
Use the Systems Architect approach, but translate it into practical advice so lower-friction fantasy subs accept it:
- keeper value as liquidity, not just player rank
- roster construction before “best player available”
- market sentiment vs real roster need
- future picks/young players as flexible assets
- trade calculators as sentiment tools, not truth

**Mod-safety rules:**
- No DynastyJig product mentions, no links, no CTA.
- Prefer comments on existing advice threads until karma improves.
- Avoid sounding like a tout/account trying to build a brand. Be useful first.
- In `r/Fantasy_Football`, do not mention league recruiting or politics; keep it strictly roster advice.

## Daily Execution 
A daily Cron (`reddit-karma-farmer`) will draft one deep-dive post or highly technical comment for these subreddits and deliver it directly to JT via Telegram.

## Freshness + Anti-Repeat Rules — 2026-05-08

Source of truth for Reddit repeats: `memory/content/reddit-draft-log.jsonl`.

Every Reddit generator run must:
1. Read the last 30 days of `reddit-draft-log.jsonl` and `posted-log.jsonl` before drafting.
2. Log every non-skipped Reddit item with date, subreddit, type, title/look-for, first 120 chars, core angle, and body hash.
3. Skip or rewrite any draft that reuses the same title, hook, first paragraph, core analogy, or broad frame from the last 30 days.
4. Prefer `SKIP_SLOT` over recycled evergreen theory.

Crypto guardrail:
- No more generic protocol durability / stakeholder-alignment essays unless tied to a fresh specific debate.
- Avoid stale phrases like “who is forced to keep caring,” “temporary participation,” “stakeholder coordination,” and broad TVL/fees/emissions lists.

Fantasy guardrail:
- No abstract dynasty theory comments unless the thread directly asks for it.
- Comments must tie to a concrete thread type: trade offer, keeper decision, rookie pick, contender/rebuilder decision, player role, or draft-capital/landing-spot question.
- Avoid stale phrases like “assets have different jobs,” “calculators as sentiment checks,” “research alarm,” “liquidity,” “optionality,” and broad roster-window lectures.
