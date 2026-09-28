# Exact Prompt for Opus 5.5 — LinkedIn Content OS Adversarial Architecture Review

You are the independent principal architect, content-systems designer, evaluator, and adversarial reviewer for JT Somwaru's LinkedIn Content OS.

Do not flatter the plan. Your job is to find the architecture that will fail in practice before it is built: wrong abstractions, duplicate owners, missing evidence, stale inputs, weak ranking logic, misleading feedback signals, privacy or rights failures, hidden manual burden, brittle image production, untestable requirements, schedule failure modes, and needless complexity.

Return one best recommendation. Separate verified facts from assumptions. If a component should be removed or deferred, say so directly.

Think carefully before deciding. Trace each recommendation through source collection, selection, generation, image production, JT review, publication, and learning so local improvements do not create downstream failure.

## Who JT is

JT Somwaru is an NYC-based AI implementation consultant and operator-builder. He builds controlled AI and workflow systems for ops-heavy businesses and is also targeting senior AI implementation, enablement, and workflow-transformation roles. His LinkedIn feed is a due-diligence surface for buyers, recruiters, and builders. It should demonstrate implementation judgment through real proof, public-evidence teardowns, and timely AI-news analysis.

JT's preferred voice is direct, practical, specific, and operator-led. Strong posts name the input, system, owner, constraint, approval boundary, or measured result. Weak posts use generic AI-consultant hooks, polished contrarian formulas, guru language, vague outcomes, or internal content-system commentary.

## Product goal

Build an automated preparation system that produces two or three qualified LinkedIn posts per week when evidence supports them, across exactly three modes:

1. workflow/project build proof;
2. company or niche research and operational teardowns;
3. AI news, including items JT forwards from X.

Every post must have exactly one accompanying image. A valid run may output `SKIP`. JT remains the only person who publishes. No automatic posting, commenting, replying, or LinkedIn account action is allowed.

The first approved angle, **Approval is not execution**, is an acceptance fixture for the build-proof mode, not the final product.

## Current assets

The workspace already has:

- a JT voice profile and evidence corpus;
- a current niche map and deterministic voice/stale-pattern guards;
- a 246-entry post ledger;
- recent-build, proof, and technical-angle feeds;
- existing content rules and posted-reply handling;
- Mission Control as the only human decision surface;
- a generic exact-payload lane-packet contract with idempotent admission, approval binding, typed closure, evidence, and outcomes;
- a strict rule that JT alone performs external posts.

## Confirmed gaps

- The edit-delta ledger is empty, so the system is not learning from JT's rewrites.
- Some current-effort and weekly-intelligence inputs are stale.
- Existing content/news/X automations are disabled or belong to older designs.
- There is no governed company-teardown scorer.
- There is no unified candidate -> post -> image -> approval -> published URL -> outcome loop.
- Existing content documents contain conflicting older strategies, including one-post-per-week and carousel assumptions that the new goal supersedes.

## Proposed design

The proposed system separates:

1. source collectors;
2. versioned signal and candidate ledgers;
3. hard gates, fixed scoring, semantic deduplication, and a rolling mix controller;
4. small mode-specific gold-set retrieval;
5. one-draft writing;
6. exactly-one-image production;
7. deterministic and model-based QA;
8. exact-payload Mission Control review;
9. append-only edits, publication receipts, and outcomes.

Key decisions:

- Three accepted manual fixtures are required before recurrence: build proof, teardown, and AI news. Two fixtures cannot prove three distinct evidence and visual contracts.
- Missing primary evidence, missing permission, expired content, unsafe claims, semantic repeats, weak positioning, and no viable image path fail closed before scoring.
- An eligible candidate needs at least 75/100 before any small diversity adjustment.
- Candidate scoring emphasizes commercial relevance and evidence strength, then earned JT angle, freshness, workflow usefulness, novelty, visual clarity, and qualified-conversation potential.
- The rolling eight-post target is three build-proof, three teardown, and two AI-news posts. This is not a quota; weak lanes never get filler.
- Only one unresolved content review card can exist at a time.
- A Claude Design prompt is an intermediate visual-production input. A review-ready packet needs a concrete image asset with dimensions, MIME type, byte length, and SHA-256.
- AI-news screenshots require reuse rights; the fallback is an original attributed text-first source card with no copied logo or artwork.
- Client-identifying claims, metrics, and private screenshots require an exact JT permission record. Automated privacy checks may reject but cannot grant permission.
- V1 does not automatically change weights. After at least 30 published posts and at least eight per core mode, it may propose a change for JT approval.
- Recurring jobs require a later separate JT authorization and a default-off kill switch.

## Canonical design to inspect

If you have filesystem access, read this entire file first:

`/Users/jtsomwaru/.config/superpowers/worktrees/workspace/linkedin-content-os-design/docs/superpowers/specs/2026-09-28-linkedin-content-os-design.md`

Then inspect these read-only references only where needed:

- `/Users/jtsomwaru/.openclaw/workspace/docs/agents/content-rules.md`
- `/Users/jtsomwaru/.openclaw/workspace/skills/content-generation/SKILL.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/jt-voice-profile.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/jt-voice-evidence-corpus.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/current-niche-map.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/current-efforts.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/recent-builds.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/posted-log.jsonl`
- `/Users/jtsomwaru/.openclaw/workspace/memory/content/edit-deltas.jsonl`
- `/Users/jtsomwaru/.openclaw/workspace/mission-control/docs/mission-control-lane-packet-contract.md`
- `/Users/jtsomwaru/.openclaw/workspace/docs/superpowers/plans/2026-09-24-ai-workflow-growth-os-completion.md`

Treat older content strategies as evidence, not authority. The goal in this prompt and the 2026-09-28 design supersede old cadence, carousel, property-only, and one-lane assumptions.

Do not modify files, create worktrees, call providers, access credentials, change Mission Control, create or enable schedules, generate posts, publish, or perform any external action. This is a read-only architecture review.

## Adversarial review questions

### 1. North star and scope

- Is this actually a content operating system, or an overbuilt generator?
- Is two or three qualified posts per week realistic without manufacturing filler?
- Are the three modes sufficient and mutually distinct?
- Is the one-unresolved-card rule useful backpressure or an avoidable bottleneck?

### 2. Source awareness

- Will the proposed project/build collectors know what JT is truly working on and what is actually complete?
- What owner or source precedence is missing?
- Which freshness windows are wrong?
- How should the system detect a meaningful current project without turning internal hygiene into public content?

### 3. Trend and AI-news discovery

- Does the design distinguish popularity from relevance and earned JT insight?
- Are public sources and JT-forwarded X items enough?
- What would cause stale, derivative, or summary-only posts?
- What primary-source and attribution controls are missing?

### 4. Company and niche teardowns

- Is trigger-based company discovery better than popularity-based discovery?
- Which public change signals best predict an interesting operational teardown?
- How could the scorer systematically choose famous but commercially useless companies?
- What protects against fake internal knowledge, invented pain, or a workflow no competent operator would buy?

### 5. Gold set and voice

- Is the proposed gold set sufficient to learn JT's voice, format, wording, and taste?
- How should positive, negative, edit-delta, external-mechanics, and outcome examples be weighted?
- What prevents overfitting to a small or stale corpus?
- Should retrieval be rule-based, embedding-based, model-selected, or hybrid?
- Which current content rules are likely overconstraints that make the writing worse?

### 6. Ranking and mix control

- Attack the hard gates, 100-point score, 75-point threshold, deductions, tie-breakers, 45-day semantic cooldown, and +/-6 diversity adjustment.
- Which dimensions double-count the same idea?
- Which scores cannot be evaluated reliably before publication?
- Is three build / three teardown / two news over eight posts the right rolling target?
- Provide a better exact scoring and portfolio-selection design if this one is weak.

### 7. Image system

- Is the screenshot / reconstruction / source crop / schematic / Claude Design route practical?
- Which route will create hidden manual work?
- What rights, attribution, privacy, readability, or mobile-feed failures remain?
- Should a review card block until a rendered image exists, or should visual production occur after copy approval?
- Recommend one exact image lifecycle.

### 8. Evaluation

- Are three fixtures enough to authorize scheduled operation?
- What must be frozen to make each fixture reproducible?
- Are the JT rating rubric and passing thresholds sufficient?
- What tests distinguish a system that is safe from one that actually produces strong content?
- Define the minimum evaluation set before any model or ranking comparison.

### 9. Learning loop

- Which outcomes should influence voice, selection, and cadence?
- How should the system weigh JT edits versus impressions, saves, target-reader replies, profile views, recruiter conversations, and buyer opportunities?
- Is 30 published posts with eight per mode enough before weight proposals?
- How do we prevent small-audience noise, survivorship bias, and engagement bait from corrupting the system?

### 10. Operations and implementation

- Attack the proposed source-health, retry, expiry, idempotency, backpressure, state-machine, kill-switch, and rollback rules.
- Which parts belong in deterministic code, which in a model, and which must stay human?
- Which components should use local scripts, OpenClaw, n8n, Mission Control, Drive, or none of them?
- Is the six-program implementation sequence optimal?
- What should be cut from v1?

## Required output

Use this level of specificity:

<example>
Weak: "Improve the scoring model."

Strong: "Remove qualified-conversation potential from pre-publication scoring because it duplicates commercial relevance and cannot be observed yet. Reassign its five points to evidence strength, then evaluate conversation outcomes only in the post-publication learning ledger."
</example>

Return exactly these sections:

1. **Executive verdict** — `SOUND`, `SOUND WITH CHANGES`, or `RETHINK`; maximum five sentences.
2. **Five biggest failure risks** — ranked, with concrete failure mechanism and evidence.
3. **Architecture ownership review** — keep/change/remove for every component and owner.
4. **Source-awareness design** — exact project, trend, X/news, and company-discovery architecture.
5. **Gold-set design** — exact corpus composition, labels, retrieval method, update rules, and contamination controls.
6. **Candidate schema and lifecycle critique** — missing fields, states, permissions, and idempotency rules.
7. **Ranking replacement or confirmation** — exact gates, formula, thresholds, cooldowns, diversity behavior, and tie-breakers.
8. **Image lifecycle** — one recommended path from candidate to rendered, verified asset for each mode.
9. **Evaluation plan** — frozen fixtures, gold evaluation set, JT rubric, automated tests, pass/fail thresholds, and model-comparison method.
10. **Learning loop** — which signals may change what, minimum samples, approval gates, and protections against noisy metrics.
11. **Operational design** — schedule, backpressure, source health, retries, receipts, kill switch, rollback, and observability.
12. **Optimal implementation sequence** — bounded programs with dependencies, acceptance evidence, and explicit stop conditions.
13. **Remove / simplify / add / defer** — ranked `P0`, `P1`, and `P2` changes.
14. **Contradictions to reconcile** — conflicts between the new design and older workspace rules/files.
15. **Questions for JT** — only decisions that materially change architecture; maximum five.

For every criticism, state the better replacement. Do not recommend automatic publishing. Do not optimize for impressions at the expense of buyer/recruiter trust, factual accuracy, privacy, or JT's actual voice.
