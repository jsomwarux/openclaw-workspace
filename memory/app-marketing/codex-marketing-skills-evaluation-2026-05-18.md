# Codex Marketing Skills Repo Evaluation — 2026-05-18

Repo: https://github.com/rbrown101010/codex-marketing-skills

## Executive read
Do not install wholesale. Integrate three patterns into App Marketing OS: YouTube hook/transcript research, motion-asset production discipline, and Buffer-style save/schedule safety. The strongest near-term fit is a YouTube/Shorts research lane for Vista, Glow Index, Nash Satoshi, and Action Arena.

## What is in the repo
- YouTube Researcher: YouTube search, channel scans, transcripts, hook analysis via SerpApi + Supadata.
- Genmedia: fal.ai media model discovery/run workflow.
- Buffer Publisher: GraphQL workflow for ideas/drafts/scheduled posts with safety gates.
- HyperFrames / Remotion: motion graphics, app demos, title cards, overlays, captions, launch videos.
- Excalidraw/Paper: visual explainers and diagrams.
- Readwise / brand deal research: not relevant to current app marketing OS.

## Integrate now

### 1. YouTube/Shorts Research Lane
Why: App Marketing OS currently has X/ReelFarm/SEO/GA4 signals but lacks systematic YouTube/Shorts research. YouTube titles, Shorts hooks, and transcripts are strong source material for TikTok/ReelFarm and SEO angles.

Use for:
- Vista: movie rating, Letterboxd alternatives, film taste, ranking videos.
- Glow Index: skincare product ranking, ingredient skepticism, dupe/value content, safe claim language.
- Nash Satoshi: crypto AI agents, token rankings, model disagreement, methodology explainers.
- Action Arena: bankroll challenge, fake-money betting league, parlay strategy, dynasty strategy hooks.

Integration pattern:
- Add a weekly/manual App Marketing research step: pull 10 videos + 3 transcripts for one app/topic.
- Extract: title hooks, opening 10 seconds, recurring visual formats, audience promises, CTA style, repeated objections.
- Route outputs into `experiment-calendar.md`, `optimization-rules.md`, or an app-specific research note only if they create a concrete test.

Guardrail: use as pattern intelligence, not copy. Do not clone scripts until API keys and cost/limits are approved.

### 2. Motion Asset Production Rules from HyperFrames/Remotion
Why: JT's app marketing bottleneck is not just copy. Vista/Nash/Glow need better reusable visual assets. HyperFrames has strong rules worth adopting even if we do not use the tool: visual identity gate, layout before animation, real data in motion, no generic AI design tells.

Integrate into App Marketing OS asset briefs:
- Require a visual identity before video/slide generation.
- Build hero frame/static layout before animation.
- For data/ranking videos, pair every number with visual weight.
- Avoid generic AI aesthetics: cyan-on-dark, purple gradients, identical card grids, dead-gray neutrals.

Best fit:
- Nash Satoshi ranking/methodology clips.
- Glow Index product-score explainers.
- Vista rating-precision app-demo clips.

### 3. Buffer Safety Model
Why: We may eventually save/schedule product posts through Buffer or another queue. The skill's publish safety model is useful regardless of tool.

Adopt these rules if/when a scheduler is wired:
- Save unscheduled content as ideas by default.
- Draft/schedule/publish only with explicit confirmation.
- Preflight before publish-affecting actions: account/channel/text/assets/mode/time.
- Never `shareNow` unless JT explicitly requests immediate publishing.

## Do not integrate now
- Genmedia/fal: useful for future asset experiments, but OpenClaw already has first-class image/video tools. Add only if fal model coverage becomes necessary.
- Excalidraw/Paper: useful for consulting/client explainers, not core app marketing right now.
- Readwise: no current signal for App Marketing OS.
- Brand deal researcher: not relevant until apps have meaningful audience or inbound sponsorship flow.

## Recommended next action
Create one App Marketing experiment: `YouTube Hook Mining Sprint`.

First action: run one manual research pass for Glow Index using YouTube/Shorts search terms around skincare dupes, product ranking, ingredient checker, and viral product reviews.

Done state: one saved report with 10 source videos, 5 hook patterns, 3 safe Glow experiments, and 1 update to `experiment-calendar.md` or `optimization-rules.md`.

## Decision
Integrate the ideas, not the repo. The repo is valuable as pattern intelligence. The optimal near-term system improvement is a YouTube/Shorts research lane feeding App Marketing OS experiments.
