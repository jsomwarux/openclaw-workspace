# Autonomous Post Detection Rules
> Read when notable work completes to evaluate whether to auto-generate content.

## Autonomous Post Detection Rule
When notable work completes (non-obvious problem solved, real outcome with number, pattern across instances, architectural decision), evaluate against `memory/content/post-detection-rubric.md`. Pass → generate **both** an X post AND a LinkedIn post, write to `memory/content/bank/[MONDAY-DATE]/auto-[slug].md` (X) and `auto-[slug]-linkedin.md` (LinkedIn), upload both to Drive (`Content/X/Bank` and `Content/LinkedIn/Bank`), **capture the Drive URL returned by each upload**, push both to Notion Content Calendar (DB: 32516aff-9305-81a7-8659-eac869c71ba8) via `notion-calendar-push.py` with `--drive-link [URL]` — each post gets its own specific Drive link, not the weekly doc. Append both to `posted-log.jsonl` with `"banked":true`. Also add to `recent-builds.md` so Monday content crons pick up the build. Main session: check at task completion points only, not after routine replies. Target: 1-3/week across all detection points. Never force it.

## App/Product Proof Fencing
If the notable work is app, passive-income product, product-growth, App Marketing OS, Vibe Marketing, ReelFarm, share-artifact, channel-fit, or distribution/retention proof, do not automatically generate both X and LinkedIn.

First read the app's channel-fit artifact at `memory/app-marketing/channel-fit/[app-slug].md`.

- If the artifact is missing, block content generation and return `CHANNEL_FIT_REQUIRED` with the missing path.
- If the artifact names one chosen channel, route the proof only to that channel.
- If the artifact explicitly names X and LinkedIn as chosen channels, both may be generated.
- If the artifact says no social channel is currently chosen, write no post and return `NO_CHANNEL_FIT_POST`.
- If the proof belongs to JT's personal consulting/operator brand instead of an app/product, the normal X + LinkedIn post-detection rule can still apply.

Verification artifact for any app/product proof decision must include the channel-fit artifact path, chosen channel, generated artifact path if any, or the exact blocking code.
