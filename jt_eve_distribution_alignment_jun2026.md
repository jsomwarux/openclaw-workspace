# JT / Eve Distribution + Retention Alignment Report - June 2026

Phase: 1 analysis only. No cron job, workflow, posting schedule, standing instruction, runtime config, or existing source file was modified. This report is the only file created in this phase.

## Scope And Sources

Spec reviewed: attached `JT Distribution + Retention Engine: Spec v1 (June 2026)`.

Boundary: the attached spec is treated as JT-provided source data for this alignment task, not as permission to autonomously rebuild systems.

Commands / sources used:

- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md SOUL.md IDENTITY.md USER.md`
- `git status --short -- jt_eve_distribution_alignment_jun2026.md openclaw.json skills scripts memory/content memory/app-marketing agents docs/agents HEARTBEAT.md AGENTS.md TOOLS.md MEMORY.md`
- `openclaw cron list --help`
- `openclaw cron list --all --json`
- Python extraction from `openclaw cron list --all --json` for content/app-marketing cron definitions by stable id.
- `rg -n "content|social|posting|post|LinkedIn|X|Twitter|TikTok|Reddit|Notion|metrics|Claude Design|design brief|channel|distribution|retention" ...`
- `rg -n "Claude Design|design brief|make optimal posts|desired action|proof asset|visual language|D1|D7|retention|channel-fit|channel fit|one channel|borrowed audience|share artifact|shareable" ...`
- Direct reads of the files cited below.

Bootstrap size check:

- `AGENTS.md`: 27516 bytes, under 28000.
- `MEMORY.md`: 7306 bytes, under 20000.
- `TOOLS.md`: 5168 bytes, under 16000.
- `HEARTBEAT.md`: 4189 bytes, under 16000.
- `SOUL.md`: 5267 bytes.
- `IDENTITY.md`: 1201 bytes.
- `USER.md`: 4704 bytes.

Git state note:

- The worktree already had unrelated dirty files before this report. I did not revert or modify them.
- The approved app-discovery baseline commit already exists: `6a3626b85f570c859a1b8970685270d2cece285b`.
- `skills/product-build-loop/SKILL.md` had a pre-existing uncommitted edit from the prior approved item 4 diff. This report did not touch it.

## Spec Thesis

The distribution spec is not asking for more autonomous posting. It argues the opposite:

- Content is fuel; reach is the engine.
- Channel-fit is a gate before cadence.
- Reach is built through product-led shareable outputs and borrowed audiences, not volume.
- Metrics should be ordered by right-person reach, then clicks, installs, D1/D7 retention.
- Claude Design is a narrow production support tool fed by a strict brief, not the strategic engine.
- Replies/objections should feed product backlog; retention should feed the content calendar.
- App work remains capped under 10 hours/week, so one app, one channel, one reach motion matters more than spreading effort.

## 1. Inventory

### Current Enabled Cron Jobs

#### `eve-morning-brief-001` - Morning Brief

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: daily 7:30 ET.
- Current behavior: reads `HEARTBEAT.md`, produces the morning brief, and includes a Nash delivery contract when rankings are fresh. The Nash branch creates a daily X post and a daily Reddit draft under `memory/app-marketing/daily-nash/YYYY-MM-DD.md`.
- Distribution relevance: app-content production can happen inside a general operating brief.
- Spec alignment: partial. It can surface app distribution material, but it is not a per-app channel-fit gate.

#### `eve-weekly-synthesis-007` - Weekly Intelligence Synthesis

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Sunday 8:00 ET.
- Current behavior: weekly intelligence synthesis; writes `memory/content/weekly-intel-brief.md`; can create content signals or drafts when signal criteria pass.
- Distribution relevance: upstream content intelligence.
- Spec alignment: partial. It can provide market inputs, but it is not a reach-motion or retention loop.

#### `d918122d-d58c-4985-a181-126cfd7e6be7` - `content-sunday`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Sunday 9:00 ET.
- Current behavior: sends JT Sunday LinkedIn and Sunday X from the latest weekly file plus an engagement check. It has an optimality delivery gate for stale or weak content.
- Distribution relevance: fixed weekly X/LinkedIn delivery routine.
- Spec alignment: weak for app distribution. It improves content quality, but the spec says cadence comes after channel-fit and one chosen channel.

#### `870bf3ff-55c9-49c0-9970-361c81a0920b` - `vibe-marketing-generate`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Monday 4:45 ET.
- Current behavior: App Marketing Product Content production run. It reads `agents/app-marketing/product-content/AGENT.md`, `memory/app-marketing/os-spec.md`, `memory/app-marketing/app-registry.md`, `memory/app-marketing/weekly-scoreboard.md`, and legacy Vibe files for queue/state compatibility. It states no Mac mini ReelFarm execution.
- Distribution relevance: main app-marketing content generator.
- Spec alignment: partial to strong in intent. It reads the App Marketing OS, which already emphasizes share artifacts, borrowed audience, source tags, and skip-volume defaults. But legacy compatibility still carries multi-platform content assumptions.

#### `33b8b0a2-e86c-4f51-aa4f-b8537def3107` - Viral Post Swipe File - X Research

- Source: current cron definition from `openclaw cron list --all --json`; related script `scripts/notion-swipe-fetch.py`.
- Schedule: Monday/Wednesday/Friday 5:45 ET.
- Current behavior: searches X for viral posts in JT's niches, pushes qualifying posts to the Notion swipe file, and produces reply targets / mechanics inputs.
- Distribution relevance: audience and hook research for X.
- Spec alignment: partial. Useful for audience-borrowing and conversation awareness, but X-specific and not per-app channel-fit.

#### `fe984519-ec58-4c6e-a096-9ac425f735a3` - `content-generate-linkedin`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Monday 6:45 ET.
- Current behavior: generates JT's weekly LinkedIn queue from `memory/jt-corpus.md`, recent builds, weekly intel, posted-log anti-repeat, and Notion swipe mechanics.
- Distribution relevance: fixed LinkedIn content-generation step.
- Spec alignment: weak for app distribution. It is personal-brand/consulting oriented and content-quality oriented, not channel-fit gated per app.

#### `c7033613-feec-456c-b72b-135beaa89fe2` - `app-marketing-weekly-scoreboard`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Monday 8:00 ET.
- Current behavior: weekly App Marketing OS scoreboard. It reads app marketing OS files, collects metrics, updates analysis/rules, writes summary, and never posts externally.
- Distribution relevance: app metrics and decision layer.
- Spec alignment: partial to strong. It is the closest current owner for measurement, but the metric order is not yet strictly right-person reach -> clicks -> installs -> D1/D7 retention.

#### `cb8f29dd-0db1-4abd-b87e-3e7168ca4a97` - `content-generate-x`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Monday 9:00 ET.
- Current behavior: generates weekly X queue from JT corpus, edit deltas, current efforts, recent builds, weekly intel, posted-log anti-repeat, existing weekly file, and Notion swipe fetch.
- Current state: enabled, but current cron metadata showed `lastRunStatus=error`.
- Distribution relevance: fixed X content-generation step.
- Spec alignment: weak for app distribution. It is useful for JT's personal brand and proof surface, but it defaults to X cadence rather than deciding per-app channel-fit.

#### `4a70dda4-da77-4437-9e1d-9c3001e9e1f9` - Daily News Hook

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: weekdays 9:30 ET.
- Current behavior: capped news hook generation and skip note if no concrete story.
- Distribution relevance: content input.
- Spec alignment: low. It is not an app distribution engine.

#### `5e66b4ee-aee3-497d-90ba-7aad670970a3` - `content-reminder`

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Tuesday-Saturday 8:00 ET.
- Current behavior: sends JT scheduled content from the current weekly file after running `scripts/content_distribution_guard.py`. It blocks if the guard fails. The prompt locates the exact current-week file, extracts today's content, and handles posting-state flow.
- Distribution relevance: delivery/reminder routine for scheduled content.
- Spec alignment: weak for app distribution. It guards content quality but still assumes a weekly content calendar exists.

#### `8033e775-29d2-42f2-83e9-1392352f6493` - TikTok App Account Warm-up Reminder

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: daily 14:00 ET.
- Current behavior: appends a digest reminder for JT to spend 15-20 minutes warming Vista, Nash Satoshi, and Glow Index TikTok accounts; it says not to mass-post.
- Distribution relevance: routine app-channel warmup across three app accounts.
- Spec alignment: partial but unfocused. It is not posting volume, but it still spreads attention across three apps/channels instead of one app, one chosen channel, one reach motion.

#### `a97df783-31c5-4269-a4f0-3ece75af838d` - ReelFarm Daily Strategy Intel

- Source: current cron definition from `openclaw cron list --all --json`; `agents/reelfarm-intel/daily-prompt.md`.
- Schedule: daily 17:15 ET.
- Current behavior: high-precision TikTok slideshow strategy filter from Social Growth Engineers newsletter input. Saves reports; digest/Telegram only when actionable or critical.
- Distribution relevance: TikTok/ReelFarm pattern intelligence.
- Spec alignment: partial. It treats ideas as tests, not optimizations, but it is TikTok-specific and not controlled by a per-app channel-fit gate.

#### `bb0819d0-8900-4e2a-99a2-28ab950365ab` - ReelFarm Weekly Strategy Synthesis

- Source: current cron definition from `openclaw cron list --all --json`; `agents/reelfarm-intel/weekly-prompt.md`.
- Schedule: Sunday 17:00 ET.
- Current behavior: weekly synthesis of Social Growth Engineers newsletter patterns, daily ReelFarm recommendations, and TikTok analytics feedback.
- Distribution relevance: TikTok strategy intelligence.
- Spec alignment: partial. Useful only if TikTok is the chosen channel for a chosen app.

#### `evening-digest-001` - Evening Digest

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: daily 19:00 ET.
- Current behavior: sends queued FYIs from `memory/digest-queue.md` and clears it.
- Distribution relevance: delivery path for app/content reminders and metrics outputs.
- Spec alignment: neutral.

#### `f96cc24f-55e6-4064-a075-b897156a22f2` - AI Ops Teardown Weekly Draft

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: Sunday 19:15 ET.
- Current behavior: scans buyer-relevant signals and produces a review-ready AI Ops Teardown bundle; no auto-posting.
- Distribution relevance: consulting content/proof.
- Spec alignment: mostly out of scope for app distribution, but subject to the same "do not confuse content with reach" warning if used as growth mechanism.

#### `eve-niche-monitor-006` - Niche Intelligence Monitor

- Source: current cron definition from `openclaw cron list --all --json`.
- Schedule: weekdays 9:00 ET.
- Current behavior: niche intelligence monitoring. Exact current payload was not fully inspected in this pass.
- Distribution relevance: upstream niche/content signal.
- Spec alignment: UNVERIFIED beyond current cron existence and broad niche-intel role.

### Disabled / Legacy Content And App-Marketing Cron Jobs

These were present in the current cron list but disabled:

- `1e614c8a-adb8-4a02-b35f-3031db55b337` - Daily DynastyJig Niche-Growth X Post Pack. Disabled. X draft pack.
- `06050403-afb5-4783-a95a-fc6708ce61ec` - `vibe-post-vista-sunday`. Disabled. Would run a Vista ReelFarm/TikTok publish script.
- `365e8277-f552-4192-9fce-e99dce68f77b` - `vibe-post-nash-tuesday`. Disabled. Would run Nash ReelFarm/TikTok publish script.
- `a81aa240-8eac-4874-a9cb-ddfd0aa238e2` - `vibe-post-vista-friday`. Disabled. Would run Vista ReelFarm/TikTok publish script.
- `faf41f37-938c-4bdb-baaa-fe84769a6160` - `vibe-post-nash-thursday`. Disabled. Would run Nash ReelFarm/TikTok publish script.
- `bbe49024-458a-4496-9c7c-7a278615810f` - `reddit-daily-gen`. Disabled. Daily Reddit draft generation.
- `d163df4a-5d96-4de7-90eb-0242b671800e` - TikTok App Account Warm-up Reminder. Disabled old/duplicate version.
- `d4dedeb1-a29a-489b-9a82-c8431c08e5b6` - `content-monday-send`. Disabled obsolete Monday sender; superseded by newer content generation flow.
- `ca536298-53d2-41bb-8f83-21ee2626eba8` - Weekly Content Batch. Disabled; superseded by `content-generate`.
- `fb1d6691-5663-47aa-bb78-f90813b33203` - Weekly Seeds Prompt. Disabled.
- `8b968751-6e59-42e5-b2ce-09f57d36176c` - `dynasty-replies-gen`. Disabled.
- `9a384044-f89f-46b5-9ba5-ca909b72ac27` - Nash Satoshi TikTok Warmup Reminder. Disabled.

Current status: these disabled jobs should stay disabled unless a future Phase 2 explicitly reactivates or rewrites them. Reactivation would be a cron/runtime change requiring individual before/after approval.

### Standing Instructions And Workflows

#### `AGENTS.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/AGENTS.md`.
- Current behavior: contains rules for content generation, post detection, proof updates, recent-builds updates, technical angles, Drive upload, and autonomous content-to-ready-state lane.
- Distribution relevance: system-wide authority for when Eve can draft content and update content memory.
- Spec alignment: partial. It enforces quality and proof hygiene, but it does not currently require channel-fit, reach motion, or D1/D7 retention before app-content cadence.

#### `docs/agents/content-rules.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/docs/agents/content-rules.md`.
- Current behavior: content voice/profile/evidence checklist, Notion swipe references, weekly content guard expectations, posted-log hygiene, relevance ladder, platform/niche fit requirements, and duplicate/staleness rules.
- Distribution relevance: strongest current personal-brand content quality system.
- Spec alignment: partial. It has platform/niche fit and reference mechanics, but not per-app single-channel reach-engine gating.

#### `docs/agents/post-detection-rules.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/docs/agents/post-detection-rules.md`.
- Current behavior: when notable work completes, evaluate against a rubric; if it passes, generate both X and LinkedIn drafts, upload both to Drive, push both to Notion calendar.
- Distribution relevance: automated proof-to-content workflow.
- Spec alignment: weak for app distribution. It can create cross-platform content from work completion before app-specific channel-fit is established.

#### `docs/agents/content-posted-reply-handler.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/docs/agents/content-posted-reply-handler.md`.
- Current behavior: maps JT's "posted" replies to posted-log and optional Notion state using `scripts/content_pending_reply_state.py`.
- Distribution relevance: posting-state feedback.
- Spec alignment: partial. It handles post-status feedback, but not replies/objections into product backlog or retention into calendar.

#### `skills/content-generation/SKILL.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/skills/content-generation/SKILL.md`.
- Current behavior: unified content generation for JT's social posts; balances build proof, consultant POV, and personal voice; uses swipe mechanics and corpus; outputs drafts to local memory/Drive/Notion as appropriate.
- Distribution relevance: general content-generation skill.
- Spec alignment: partial. Strong on quality and proof; weak on app-specific reach engine and retention feedback.

#### `skills/content-atomizer/SKILL.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/skills/content-atomizer/SKILL.md`.
- Current behavior: turns one source artifact into multiple platform-native derivatives such as X, LinkedIn, TikTok, and Reddit.
- Distribution relevance: multi-platform content expansion.
- Spec alignment: risky for app distribution. The spec says one app, one channel, one reach motion; atomization can become cross-posting if not gated.

#### `skills/wednesday-linkedin/SKILL.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/skills/wednesday-linkedin/SKILL.md`.
- Current behavior: Wednesday LinkedIn case-study pattern.
- Distribution relevance: LinkedIn-specific routine.
- Spec alignment: low for app distribution. Useful for consulting narrative, not app-channel reach.

#### `skills/x-research/SKILL.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/skills/x-research/SKILL.md`.
- Current behavior: X research, watchlist, weekly ledger and source mechanics for `@jts_14`.
- Distribution relevance: X-native audience and hook research.
- Spec alignment: partial. Useful when X is the chosen channel; overfit if applied before channel-fit.

#### `memory/app-marketing/os-spec.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/memory/app-marketing/os-spec.md`.
- Current behavior: App Marketing OS control layer. It emphasizes clear audience, promise, product-led share artifact, primary acquisition loop, borrowed-audience strategy, durable discovery channel, source tags, weekly metrics, and kill/pause/continue.
- Distribution relevance: strongest current alignment with the spec.
- Spec alignment: strong, but not yet enforced everywhere by cron/content routines.

#### `memory/app-marketing/revised-operating-model-2026-05-19.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/memory/app-marketing/revised-operating-model-2026-05-19.md`.
- Current behavior: states app marketing should optimize repeatable niche-specific acquisition loops, not generic content ideas. Requires product-led share artifacts, measurement spine, competitor/review mining, and borrowed-audience distribution.
- Distribution relevance: directly aligned operating model.
- Spec alignment: strong. This is already conceptually close to the new distribution spec.

#### `memory/app-marketing/share-artifact-roadmap.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/memory/app-marketing/share-artifact-roadmap.md`.
- Current behavior: defines Vista Movie Taste Card, Nash Weekly Ranking Receipt Card, and Glow Product Verdict Card.
- Distribution relevance: product-led shareable outputs.
- Spec alignment: strong.

#### `memory/app-marketing/measurement-spine.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/memory/app-marketing/measurement-spine.md`.
- Current behavior: every acquisition experiment needs source tag or it cannot teach the system; tracks 24h/72h/7d and downstream metrics. App-specific notes include some retention/activation gates.
- Distribution relevance: app marketing metrics.
- Spec alignment: partial. It is not yet strict enough on D1/D7 retention across app experiments.

#### `memory/app-marketing/app-registry.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/memory/app-marketing/app-registry.md`.
- Current behavior: current app states. Vista paused/passive; Nash capped to one weekly receipt-style item; Glow primary ongoing app bet via SEO/GEO; Action Arena gated around App Store and retention.
- Distribution relevance: app focus and channel choices.
- Spec alignment: partial to strong. It has restraint, but channel-fit artifacts are not formal gates for every app.

#### `agents/app-marketing/product-content/AGENT.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/agents/app-marketing/product-content/AGENT.md`.
- Current behavior: app product-content agent. It reads App Marketing OS, app registry, scoreboard, optimization rules, and defaults to `SKIP_CONTENT_VOLUME` unless a named gate/test exists. It maps generated items to named tests and requires reference mechanics.
- Distribution relevance: current app-marketing content owner.
- Spec alignment: strong foundation, but it needs explicit distribution-engine gates: channel-fit artifact, reach-motion artifact, strict Claude Design brief, retention-to-calendar, and reply-to-backlog.

#### `agents/vibe-marketing/AGENT.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/agents/vibe-marketing/AGENT.md`.
- Current behavior: legacy product marketing system. It has platform rules and historical output volumes across X, TikTok, Reddit, and LinkedIn, while also reading the App Marketing OS first.
- Distribution relevance: legacy app content generation.
- Spec alignment: mixed. It is a reduction target because its old volume/platform defaults conflict with one app, one channel, one reach motion.

#### `agents/vibe-marketing/platform-rules.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/agents/vibe-marketing/platform-rules.md`.
- Current behavior: platform-specific hook and format rules.
- Distribution relevance: production guidance after channel choice.
- Spec alignment: partial. Useful after channel-fit; should not decide channel or cadence by itself.

#### `agents/reelfarm-intel/daily-prompt.md` and `agents/reelfarm-intel/weekly-prompt.md`

- Source: `/Users/jtsomwaru/.openclaw/workspace/agents/reelfarm-intel/daily-prompt.md`, `/Users/jtsomwaru/.openclaw/workspace/agents/reelfarm-intel/weekly-prompt.md`.
- Current behavior: TikTok/ReelFarm strategy intelligence from newsletter and analytics inputs. Recommendations are treated as tests, not optimizations.
- Distribution relevance: TikTok channel intelligence.
- Spec alignment: partial and only relevant when TikTok is the chosen channel.

### Scripts And Data Files

#### `scripts/notion-swipe-fetch.py`

- Current behavior: fetches viral posts from the Notion Viral Swipe DB, filtered by platform/niche/format/since-days and sorted by engagement.
- Distribution relevance: hook and audience-mechanics research.
- Spec alignment: partial. Useful for channel research and audience-borrowing, but not a complete reach engine.

#### `scripts/notion-calendar-push.py`

- Current behavior: pushes content to the Notion Content Calendar DB and handles duplicate slot detection unless replacing.
- Distribution relevance: scheduling.
- Spec alignment: neutral to risky. Calendar execution should happen after channel-fit and reach-motion gates.

#### `scripts/content_distribution_guard.py`

- Current behavior: validates weekly content/reference mechanics/stale patterns and Notion script hygiene.
- Distribution relevance: content quality guard.
- Spec alignment: partial. It guards quality, not channel-fit/reach/retention.

#### `scripts/content_calendar_audit.py`

- Current behavior: audits weekly content, posted-log hygiene, content cron prompt guardrails, and optional Notion state.
- Distribution relevance: content-system health check.
- Spec alignment: partial. It does not verify app channel-fit or retention loop.

#### `scripts/content_pending_reply_state.py`

- Current behavior: writes/reads pending posted-reply state for JT's "posted" confirmation flow.
- Distribution relevance: post-status tracking.
- Spec alignment: partial. It does not transform comments/replies into product backlog items.

#### `scripts/app_marketing_collect_metrics.py`

- Current behavior: reads `post-registry.jsonl`, collects metrics via connectors for web/social/app surfaces, appends rows to `metrics-inbox.jsonl`, refreshes `weekly-scoreboard.md`, writes `metrics-collection-status.json`.
- Distribution relevance: app marketing metrics collection.
- Spec alignment: partial. It can support the measurement core, but schema/enforcement needs D1/D7 retention and right-person reach.

#### `scripts/app_marketing_metrics.py`

- Current behavior: summarizes app marketing metrics into a weekly scoreboard. Required fields include views/impressions, clicks/downloads/signups/conversions where available.
- Distribution relevance: app marketing measurement.
- Spec alignment: partial. It tracks downstream behavior in places, but not the spec's required order as a hard schema.

#### `scripts/app_marketing_experiment_calendar.py`

- Current behavior: turns metrics and optimization rules into weekly experiments; includes planned experiments for app channels and source tags.
- Distribution relevance: experiment planning.
- Spec alignment: partial. It is a natural place to enforce channel-fit and retention-driven calendar updates.

#### `memory/app-marketing/performance-analysis.md`

- Current behavior: summarizes app marketing performance, winners, losers, and recommendations from prior tests.
- Distribution relevance: feedback and decision layer.
- Spec alignment: partial. It already warns against increasing volume prematurely.

#### `memory/app-marketing/optimization-rules.md`

- Current behavior: stores channel/app optimization rules from measured tests, including patterns to avoid and double down on.
- Distribution relevance: kill/repeat logic.
- Spec alignment: partial. Useful for kill rules, but should be wired to the spec's metric order.

## 2. Gap Analysis, Ranked By Leverage

### 1. Channel-fit is not a mandatory artifact before app cadence

- Spec part: Stage 1, "Do not default to X and LinkedIn"; pick one channel per app; kill if no plausible reach channel.
- Current system: App Marketing OS and app registry partially encode channel choices and restraint. But active content jobs still generate fixed X/LinkedIn outputs for JT broadly, and the app-marketing generator does not require a separate channel-fit artifact before any app content test.
- Should do: require a `distribution_channel_fit.md` or equivalent per app before any app-specific cadence or content batch. It should choose exactly one primary channel, cite evidence, name why other channels are not chosen now, and include a kill/deprioritize decision if no searchable/reachable low-competition channel exists.
- Single specific target: `agents/app-marketing/product-content/AGENT.md`.
- Verification artifact for Phase 2: diff showing the new gate plus a sample app run or fixture where the agent refuses content generation without a channel-fit artifact.

### 2. Reach motion is not formalized as the gate

- Spec part: Stage 2, reach engine; product-led shareable output plus borrowed audiences.
- Current system: `memory/app-marketing/share-artifact-roadmap.md` and the share-artifact specs are strong. `memory/app-marketing/revised-operating-model-2026-05-19.md` explicitly prioritizes product-led share artifacts and borrowed audience. But content production can still happen without a single reach-motion artifact that names the share output, audience-borrowing surface, target accounts/communities, and test threshold.
- Should do: add a required reach-motion artifact before app content cadence. Content should attach to the reach motion, not the other way around.
- Single specific target: `memory/app-marketing/experiment-card-template.md`.
- Verification artifact for Phase 2: template diff plus one sample experiment card containing share artifact, borrowed-audience target, source tag, and kill/scale threshold.

### 3. Measurement spine is close but not strict enough on metric order and D1/D7 retention

- Spec part: Stage 4, metric order: right-person reach -> clicks -> installs -> D1/D7 retention.
- Current system: `memory/app-marketing/measurement-spine.md`, `scripts/app_marketing_collect_metrics.py`, and `scripts/app_marketing_metrics.py` already collect source-tagged metrics and downstream fields. But D1/D7 retention is not uniformly required, and "right people" is not a first-class field.
- Should do: require each app experiment to record or explicitly mark unavailable: qualified/right-person reach, clicks, installs/signups, D1, D7. Scoreboards should not declare a winner from impressions alone.
- Single specific target: `memory/app-marketing/measurement-spine.md`.
- Verification artifact for Phase 2: diff plus a sample scoreboard/metrics row showing required fields or `UNAVAILABLE` flags; script output from `scripts/app_marketing_metrics.py` if code is changed later.

### 4. Claude Design has no verified strict app-distribution brief gate

- Spec part: Stage 3, Claude Design's scoped role; strict brief required, no "make optimal posts."
- Current system: targeted search did not find a current operational Claude Design brief template with the spec's full field list in the inspected files. Some content/design references exist, but no verified gate requiring audience, pain, alternatives, existing shares, visual language, differentiated promise, desired action, proof asset, platform constraints, and hook directions before visual production.
- Should do: create a strict `claude_design_brief.md` template and require it before any app-marketing visual asset request.
- Single specific target: `agents/app-marketing/product-content/AGENT.md`.
- Verification artifact for Phase 2: diff plus `rg` check for required brief fields; sample brief populated for one app. If no visual asset is needed, the artifact should say `NO_DESIGN_ASSET_NEEDED`.
- UNVERIFIED: I did not inspect every file outside the scoped content/app-marketing trees, so the absence of any Claude Design brief in the entire workspace is not claimed.

### 5. Bidirectional feedback exists in pieces but not as a loop

- Spec part: replies and objections feed product backlog; retention feeds content calendar.
- Current system: `docs/agents/content-posted-reply-handler.md` and `scripts/content_pending_reply_state.py` handle posted-state replies. App marketing metrics feed `weekly-scoreboard.md`, `performance-analysis.md`, `optimization-rules.md`, and `experiment-calendar.md`. But there is no verified workflow that turns audience objections into a product backlog item, or D1/D7 retention changes into content-calendar changes.
- Should do: add a feedback-ingest step that classifies replies/objections into product backlog, copy/onboarding, channel insight, or discard; update experiment calendar from retention metrics.
- Single specific target: `scripts/app_marketing_experiment_calendar.py` for retention-to-calendar; likely a new additive script later for reply/objection ingest.
- Verification artifact for Phase 2: fixture reply/objection row -> generated backlog/copy item; retention metric row -> generated repeat/cut recommendation.

### 6. Legacy fixed-volume Vibe instructions conflict with the new focus discipline

- Spec part: one app, one channel, one reach motion; cadence is floor after engine exists.
- Current system: `agents/vibe-marketing/AGENT.md` still contains legacy multi-platform production assumptions, even though `vibe-marketing-generate` reads the App Marketing OS first and current app registry is more restrained.
- Should do: demote legacy Vibe volume rules behind channel-fit and App Marketing OS gates.
- Single specific target: `agents/vibe-marketing/AGENT.md`.
- Verification artifact for Phase 2: diff showing old platform-volume defaults are subordinate to channel-fit; `rg` check for "one app, one channel, one reach motion" and no unconditional multi-platform quota.

### 7. Autonomous proof-to-X-and-LinkedIn can create cross-platform content before app channel-fit

- Spec part: no default X/LinkedIn, no same content across networks, content production after reach engine.
- Current system: `docs/agents/post-detection-rules.md` says notable work can generate both X and LinkedIn posts and push both to Notion. This is useful for consulting proof, but risky for app distribution if treated as app growth.
- Should do: add an app-distribution exception: app/product posts generated from proof detection must obey the app's channel-fit artifact, or be marked consulting/personal-brand content only.
- Single specific target: `docs/agents/post-detection-rules.md`.
- Verification artifact for Phase 2: diff plus sample post-detection decision where an app proof item queues only the chosen channel or blocks without channel-fit.

## 3. Spec-Weight Elements

### Channel-fit before cadence

- Current status: PARTIAL.
- Evidence for partial: `memory/app-marketing/os-spec.md`, `memory/app-marketing/app-registry.md`, and `agents/app-marketing/product-content/AGENT.md` already discourage generic app content volume and use app state. Glow is SEO/GEO-led, Nash is capped, Vista is paused.
- Missing: a required per-app channel-fit artifact before content cadence. Active `content-generate-x`, `content-generate-linkedin`, and `content-reminder` are still fixed platform routines for JT content generally.

### Reach engine: audience-borrowing plus shareable product output

- Current status: PARTIAL to STRONG in app-marketing docs, PARTIAL in execution.
- Evidence for strong docs: `memory/app-marketing/revised-operating-model-2026-05-19.md` names product-led share artifacts, competitor/review mining, and borrowed-audience distribution. `memory/app-marketing/share-artifact-roadmap.md` defines app-specific share artifacts.
- Missing: one formal reach-motion gate per app/channel before content generation.

### Metrics ordering: right-person reach, clicks, installs, D1/D7 retention

- Current status: PARTIAL.
- Evidence: `memory/app-marketing/measurement-spine.md`, `scripts/app_marketing_collect_metrics.py`, and `scripts/app_marketing_metrics.py` already collect source-tagged metrics and downstream fields; `memory/app-marketing/app-registry.md` includes app-specific activation/retention concepts.
- Missing: required D1/D7 retention fields across app experiments and a first-class "right people" / qualified reach field. Current outputs can still over-emphasize views/impressions.

### Strict Claude Design brief

- Current status: DOES NOT / UNVERIFIED as a current enforced behavior.
- Evidence: targeted search did not find a current app-marketing Claude Design brief gate with the spec's required fields.
- Missing: explicit template and guard that prevents visual generation from a loose "make optimal posts" prompt.
- UNVERIFIED: absence across the entire workspace, because the search was scoped to content/app-marketing/scripts/agents/docs/skills and not every historical archive.

### Bidirectional feedback: replies to backlog, retention to calendar

- Current status: PARTIAL.
- Evidence: posted-reply state exists via `docs/agents/content-posted-reply-handler.md` and `scripts/content_pending_reply_state.py`; metrics feed weekly app marketing analysis via `scripts/app_marketing_collect_metrics.py`, `scripts/app_marketing_metrics.py`, and `scripts/app_marketing_experiment_calendar.py`.
- Missing: verified reply/objection -> product backlog workflow and D1/D7 retention -> content calendar update workflow.

## 4. Reductions List

The spec implies the following should stop, shrink, or be fenced before Phase 2 implementation.

### Reduce app promotion on fixed X/LinkedIn cadence

- Current source: `content-generate-x`, `content-generate-linkedin`, `content-sunday`, `content-reminder`.
- Issue: fixed X/LinkedIn systems are fine for JT personal brand and consulting proof, but should not become default app growth machinery.
- Reduction: app-specific content should require a channel-fit artifact first. If the chosen channel is SEO, Reddit, or a niche community, the X/LinkedIn weekly queue should not pretend to be the app distribution engine.

### Keep disabled direct-post Vibe/ReelFarm crons disabled

- Current source: disabled cron ids `06050403-afb5-4783-a95a-fc6708ce61ec`, `365e8277-f552-4192-9fce-e99dce68f77b`, `a81aa240-8eac-4874-a9cb-ddfd0aa238e2`, `faf41f37-938c-4bdb-baaa-fe84769a6160`.
- Issue: these represent direct app TikTok/ReelFarm posting routines.
- Reduction: do not reactivate until one app/channel/reach motion is selected and JT explicitly approves a cron/runtime change.

### Shrink multi-platform atomization for app distribution

- Current source: `skills/content-atomizer/SKILL.md`.
- Issue: atomization is useful for repurposing, but app distribution should not create X + LinkedIn + TikTok + Reddit versions before channel-fit.
- Reduction: app-distribution use of atomizer should be gated by a chosen channel, or explicitly labeled non-app personal-brand repurposing.

### Fence autonomous post detection for app proof

- Current source: `docs/agents/post-detection-rules.md`.
- Issue: it can create both X and LinkedIn drafts from notable work. That conflicts with one-channel app distribution if applied to product proof.
- Reduction: app proof should route through the app's channel-fit and reach-motion artifact before generating platform drafts.

### Shrink TikTok warm-up across three app accounts

- Current source: `8033e775-29d2-42f2-83e9-1392352f6493`.
- Issue: daily warm-up across Vista, Nash, and Glow spreads attention before one app/channel is chosen.
- Reduction: if kept, limit it to the currently selected app/channel for the active distribution cycle, or keep it as low-priority manual hygiene outside the app growth engine.

### Do not scale ReelFarm intel into posting unless TikTok is selected

- Current source: `a97df783-31c5-4269-a4f0-3ece75af838d`, `bb0819d0-8900-4e2a-99a2-28ab950365ab`, `agents/reelfarm-intel/*`.
- Issue: TikTok intelligence is useful only when TikTok/ReelFarm is the chosen channel.
- Reduction: keep as analysis only unless channel-fit selects TikTok for one app.

### Do not let views/impressions declare winners alone

- Current source: `memory/app-marketing/performance-analysis.md`, `scripts/app_marketing_metrics.py`.
- Issue: spec prioritizes right-person reach, clicks, installs, retention. Views alone are weak.
- Reduction: classify views-only wins as "attention signal" unless clicks/installs/retention confirm.

### Do not generate visuals from loose briefs

- Current source: no verified strict Claude Design gate found.
- Issue: spec explicitly rejects "make optimal posts."
- Reduction: no Claude Design production for app distribution without a strict brief or `NO_DESIGN_ASSET_NEEDED`.

## 5. Phase 2 Candidate Changes And Verification Artifacts

These are proposed only. No implementation was done in Phase 1.

### Change A - Add app distribution channel-fit gate

- Target: `agents/app-marketing/product-content/AGENT.md`.
- Change: require a per-app channel-fit artifact before app content generation.
- Verification artifact: diff plus a sample blocked run where missing channel-fit produces `BLOCKED: channel-fit artifact missing`.

### Change B - Add reach-motion fields to app experiment template

- Target: `memory/app-marketing/experiment-card-template.md`.
- Change: require chosen channel, shareable product output, borrowed-audience surface, target list, source tag, and kill/scale threshold.
- Verification artifact: file diff plus sample experiment card.

### Change C - Tighten metric spine to spec order

- Target: `memory/app-marketing/measurement-spine.md`.
- Change: require qualified/right-person reach, clicks, installs/signups, D1, D7, or explicit `UNAVAILABLE`.
- Verification artifact: diff plus sample metric row/scoreboard excerpt showing required fields.

### Change D - Add strict Claude Design brief template

- Target: additive file, likely `memory/app-marketing/templates/claude-design-brief.md`, plus requirement in `agents/app-marketing/product-content/AGENT.md`.
- Change: require the spec's brief fields before any design asset.
- Verification artifact: file list, template diff, and `rg` check for all required fields.

### Change E - Add reply/objection feedback ingest

- Target: additive script, likely `scripts/app_marketing_feedback_ingest.py`, and/or a template under `memory/app-marketing/templates/`.
- Change: convert comments/replies/objections into product backlog, copy/onboarding, channel insight, or discard.
- Verification artifact: failing/passing fixtures and command output showing a sample reply creates the expected backlog/copy item.

### Change F - Feed retention back into experiment calendar

- Target: `scripts/app_marketing_experiment_calendar.py`.
- Change: make D1/D7 retention decide repeat/cut/update calendar recommendations.
- Verification artifact: fixture metric row -> generated calendar decision; command output included.

### Change G - Fence post-detection for app distribution

- Target: `docs/agents/post-detection-rules.md`.
- Change: app/product proof cannot auto-create X+LinkedIn unless the app channel-fit artifact chooses those channels.
- Verification artifact: diff plus sample decision artifact showing app proof blocked/routed to one chosen channel.

### Change H - Demote legacy Vibe volume defaults

- Target: `agents/vibe-marketing/AGENT.md`.
- Change: make App Marketing OS/channel-fit/reach-motion gates override any legacy multi-platform quotas.
- Verification artifact: diff plus `rg` check that no unconditional app multi-platform volume quota remains.

## 6. Recommended Phase 2 Order

Do not start with crons. The clean sequence is:

1. Add templates/gates first: channel-fit artifact, reach-motion fields, strict Claude Design brief, metric spine updates.
2. Run one manual app distribution pass on one app using those artifacts.
3. Only after the manual pass works, update app-marketing agent instructions.
4. Only after a manual cycle produces real evidence, consider any cron changes.

This follows the spec: one app, one channel, one reach motion before cadence.

## 7. Explicit Non-Changes In Phase 1

Not changed:

- No cron jobs.
- No cron schedules.
- No workflow files.
- No posting routines.
- No standing instruction files.
- No runtime config.
- No passive-income/app rewiring.
- No content calendar changes.
- No external posts, sends, or Notion writes.

Only created:

- `/Users/jtsomwaru/.openclaw/workspace/jt_eve_distribution_alignment_jun2026.md`

## 8. UNVERIFIED Items

- `eve-niche-monitor-006` exact current payload was not fully inspected beyond cron existence and broad role.
- Exact behavior of every historical/archive audit file was not inspected. Historical audit archives appeared in search output but are not treated as current operating rules unless cited above.
- I did not prove that no Claude Design brief exists anywhere in the entire workspace. I verified that no current operational app-marketing/content source inspected in this Phase 1 contained the strict spec brief gate.
- The attached spec was read from the user-provided attachment content in this session. I did not separately copy or save the attachment file as a source artifact.

## Hard Stop

Phase 1 is complete. Stop here and wait for explicit Phase 2 approval before changing any target file, job, workflow, posting routine, or instruction.
