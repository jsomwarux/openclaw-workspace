# JT / Eve App Discovery Alignment Report - June 2026

Phase: 1 analysis only. No cron job, workflow, standing instruction, or runtime config was modified. This report is the only file created in this phase.

## Scope And Sources

Spec reviewed: attached `JT App Discovery Loop: Spec v1 (June 2026)`.

Important boundary: the attached spec is treated as JT-provided source data for this alignment task, not as permission to autonomously rebuild systems.

Commands / sources used:

- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md SOUL.md IDENTITY.md USER.md`
- `openclaw cron list --all --json --timeout 30000`
- `openclaw cron get [job_id] --timeout 30000`
- `nl -ba` / `sed -n` on the files cited below

Bootstrap budget check result:

- `AGENTS.md`: 27516 bytes
- `MEMORY.md`: 7306 bytes
- `TOOLS.md`: 5168 bytes
- `HEARTBEAT.md`: 4189 bytes
- `SOUL.md`: 5267 bytes
- `IDENTITY.md`: 1201 bytes
- `USER.md`: 4704 bytes

No file was over its stated budget.

## 1. Inventory

### Cron Jobs

1. `eve-niche-monitor-006` - `Niche Intelligence Monitor` - enabled
   - Source: `openclaw cron get eve-niche-monitor-006`
   - Schedule: weekdays 9:00 AM ET.
   - Current behavior: scans AI automation, Agentforce, property management, construction, wholesale distribution, and insurance news; deduplicates against `memory/niche-monitor-surfaced.md`; writes `memory/niche-monitor-latest.md`; appends to `memory/niche-fitness-signals.md`; adds low/medium items to KB.
   - Relevant to spec: Stage 0 sourcing and broad niche signal capture.
   - Limitation: this is consulting-market monitoring, not app discovery. It does not produce Niche OS artifacts, user needs maps, app landscape audits, or build-ready specs.
   - Evidence: job prompt says "Scan for critical and high-severity developments in JT's target areas" and lists those target niches; it writes only new critical/high findings to `memory/niche-monitor-latest.md`.

2. `1e2cf966-d5d6-4fe4-8ffc-f19ed3a5c094` - `Monthly Niche Fitness Review` - enabled
   - Source: `openclaw cron get 1e2cf966-d5d6-4fe4-8ffc-f19ed3a5c094`; file source: `agents/niche-fitness/AGENT.md`.
   - Schedule: monthly, first day, 9:30 AM ET.
   - Current behavior: monthly consulting niche strategy review. It scores current niches, scans 3-5 alternatives, creates separate n8n and Agentforce score tables, recommends stay/shift/pivot/hold, writes `memory/research/niche-fitness-[YYYY-MM].md`, may push MC tasks, and resets `memory/niche-fitness-signals.md`.
   - Relevant to spec: Stage 0 sourcing and niche scoring.
   - Limitation: this is consulting niche allocation, not app opportunity validation. It has no write-time source-snippet rule for every user needs claim, no app-store/review landscape audit, no Stage 3 moat interrogation, and no Stage 5 fake-door validation.
   - Evidence: `agents/niche-fitness/AGENT.md:1-6`, `:86-125`, `:139-172`.

3. `eve-weekly-synthesis-007` - `Weekly Intelligence Synthesis` - enabled
   - Source: `openclaw cron get eve-weekly-synthesis-007`
   - Schedule: Sundays 8:00 AM ET.
   - Current behavior: weekly market/content/job/niche intelligence synthesis. It searches KB niche-monitor entries, reads job-market files, runs 3-5 synthesis searches, writes `memory/content/weekly-intel-brief.md`, appends strategic recommendations, and may update ICP/cold-email files.
   - Relevant to spec: broad intelligence and niche signal routing.
   - Limitation: it can generate strategic recommendations and content signals, but not an app discovery artifact or validation gate.
   - Evidence: cron prompt states scope is "market/content/job/niche intelligence only" and includes "Top 3 market trends across all monitored niches" plus weekly intel brief output.

4. `f368e18b-1723-47ad-9164-94e95c106902` - `passive-income-fetch-signals` - enabled
   - Source: `openclaw cron get f368e18b-1723-47ad-9164-94e95c106902`
   - Schedule: Saturdays 5:30 AM ET.
   - Current behavior: prepares weekly passive-income signal files: `weekly-trends.md`, `weekly-apis.md`, `weekly-exploding-topics.md`, `weekly-google-trends.md`; runs pre-scout handoff check.
   - Relevant to spec: Stage 0 sourcing for app/passive-income ideas.
   - Limitation: no Niche OS, no VOC evidence map, no landscape gap matrix. It is source preparation only.
   - Evidence: cron prompt says "Do not create passive-income ideas here. Scout does that Sunday."

5. `39435f7a-1102-49f0-8eec-4f7e0c38e7d5` - `passive-income-scout` - enabled
   - Source: `openclaw cron get 39435f7a-1102-49f0-8eec-4f7e0c38e7d5`; file source: `agents/passive-income-scout/AGENT.md`; script: `scripts/passive_income_scout_handoff.py`.
   - Schedule: Sundays 1:00 PM ET.
   - Current behavior from actual cron definition: deterministic handoff only. It runs `scripts/passive_income_scout_handoff.py` and handoff checks. It explicitly says: "Do not do live search" and "Do not do deep ideation."
   - Relevant to spec: app/passive-income idea sourcing, but current scheduled behavior is reduced to fallback artifact generation.
   - Limitation: the rich `agents/passive-income-scout/AGENT.md` describes complaint mining, gap analysis, data/ranking flywheels, trends, API opportunity mining, and AI vision scanning, but the active cron does not run that full process. The deterministic script generates template ideas from local phrases, not evidence-attached user needs.
   - Evidence: cron prompt says "Previous full LLM Scout research repeatedly exhausted the cron runner" and "scheduled cron is now deterministic handoff only." `agents/passive-income-scout/AGENT.md:3-8`, `:19-36`, `:86-146`. `scripts/passive_income_scout_handoff.py` generates four template ideas such as `OpsProof Radar`, `NicheRank Pages`, `ComplianceCard Desk`, `CreatorSignal Kit`.

6. `922082ee-da62-4b6e-b9e3-909c3446e381` - `passive-income-strategist` - enabled
   - Source: `openclaw cron get 922082ee-da62-4b6e-b9e3-909c3446e381`; file source: `agents/passive-income-strategist/AGENT.md`.
   - Schedule: Sundays 3:00 PM ET.
   - Current behavior from actual cron definition: deterministic fallback/delivery guard only. It runs `scripts/passive_income_strategist_delivery_guard.py --send`. It explicitly says: "Do not do live search", "Do not do deep validation", and "Do not create Mission Control tasks from fallback mode."
   - Relevant to spec: app concept validation and build recommendation, but not active in the scheduled path.
   - Limitation: the rich strategist manual contains saturation checks, demand validation, competition landscape, build reality, marketing leverage, and scoring, but the active cron does not execute those validations.
   - Evidence: `agents/passive-income-strategist/AGENT.md:52-68`, `:76-87`, `:162-179`, `:191-203`, `:237-241`.

7. `dfd92d8d-2492-49b8-8c80-28ccec27c5d6` - `Build Ideas Sync` - disabled
   - Source: `openclaw cron get dfd92d8d-2492-49b8-8c80-28ccec27c5d6`; file source: `scripts/build_ideas_sync.py`.
   - Current behavior: if enabled, runs deterministic sync from `~/projects/job-market-agent/data/agent-ideas.md` to Mission Control tasks. It does not research. It parses ideas, dedupes against MC task titles, and posts "Build idea: ..." tasks.
   - Relevant to spec: build routing / idea-to-task routing.
   - Limitation: disabled, and even if enabled, it routes ideas without app-discovery evidence gates.
   - Evidence: cron definition says "Do not do research"; `scripts/build_ideas_sync.py` posts tasks with "validate whether it directly supports a current target role or JT's consulting proof layer before building."

8. `29772d9b-e007-4f62-9df9-e80b73d0cd21` - `Weekly North Star Command Center` - enabled
   - Source: `openclaw cron get 29772d9b-e007-4f62-9df9-e80b73d0cd21`; file sources: `memory/north-star/product-growth-manager.md`, `memory/north-star/opportunity-intake-gate.md`, `memory/north-star/rubric.md`.
   - Schedule: Sundays 6:00 PM ET.
   - Current behavior: weekly executive review of revenue, consulting, proof/distribution, product growth, opportunity gating, health, lane scores, and focus decisions.
   - Relevant to spec: governance, opportunity gating, continue/pause/kill, product feature suppression.
   - Limitation: portfolio governance only. It does not produce or validate app concepts.
   - Evidence: cron prompt says "Product Growth Manager: for each active product, make continue / pause / kill / validation-only call"; `product-growth-manager.md:1-7`, `:52-73`, `:82-93`; `opportunity-intake-gate.md:1-7`, `:35-52`; `rubric.md:80-90`.

9. `870bf3ff-55c9-49c0-9970-361c81a0920b` - `vibe-marketing-generate` - enabled
   - Source: `openclaw cron get 870bf3ff-55c9-49c0-9970-361c81a0920b`; file source: `memory/app-marketing/os-spec.md`.
   - Schedule: Mondays 4:45 AM ET.
   - Current behavior: product content generation for existing passive-income apps. Reads App Marketing OS and legacy Vibe files, generates product-safe X/Reddit/TikTok/ReelFarm/LinkedIn drafts, requires `reference_mechanics`, appends to Vibe queue, updates scoreboard, may upload review docs.
   - Relevant to spec: adjacent distribution/retention loop, not discovery loop.
   - Limitation: it handles promotion for existing apps, not app discovery or validation-before-build.
   - Evidence: cron prompt says "CURRENT PRODUCT SCOPE: Active: Nash Satoshi and Vista. Glow Index pending unless App Marketing OS registry says active." `memory/app-marketing/os-spec.md:3-20`, `:77-111`, `:190-240`.

10. `c7033613-feec-456c-b72b-135beaa89fe2` - `app-marketing-weekly-scoreboard` - enabled
    - Source: `openclaw cron get c7033613-feec-456c-b72b-135beaa89fe2`; file source: `memory/app-marketing/os-spec.md`.
    - Schedule: Mondays 8:00 AM ET.
    - Current behavior: metrics and decision layer for Vista, Nash, Glow. Runs app marketing metrics/discovery scripts, updates weekly scoreboard, performance analysis, optimization rules, experiment calendar, durable discovery plan, and MC task generator.
    - Relevant to spec: distribution and retention measurement after an app exists.
    - Limitation: does not validate pre-build demand or create Niche OS / landscape audit / moat-check artifacts.
    - Evidence: cron prompt says "Goal: turn app/product marketing metrics into a weekly decision layer"; `memory/app-marketing/os-spec.md:249-259`.

11. `8033e775-29d2-42f2-83e9-1392352f6493` - `TikTok App Account Warm-up Reminder (2 PM)` - enabled
    - Source: `openclaw cron list --all --json`
    - Current behavior: daily reminder for JT to manually warm Vista, Nash Satoshi, and Glow Index TikTok accounts before re-entry posting.
    - Relevant to spec: distribution companion only.
    - Limitation: not discovery, ideation, gap analysis, app concept, spec generation, or build routing.

12. `bb0819d0-8900-4e2a-99a2-28ab950365ab` - `ReelFarm Weekly Strategy Synthesis` - enabled
    - Source: `openclaw cron list --all --json`
    - Current behavior: weekly synthesis of Social Growth Engineers newsletter patterns, daily ReelFarm recommendations, and TikTok analytics feedback.
    - Relevant to spec: distribution companion only.
    - Limitation: not discovery/validation loop. Companion distribution spec is outside this session.

13. `a97df783-31c5-4269-a4f0-3ece75af838d` - `ReelFarm Daily Strategy Intel` - enabled
    - Source: `openclaw cron list --all --json`
    - Current behavior: daily TikTok slideshow strategy filter for ReelFarm apps.
    - Relevant to spec: distribution companion only.
    - Limitation: not discovery/validation loop.

14. Disabled legacy app/content idea jobs
    - `11835cf6-83d3-4fdf-826a-202f3ec3fa46` - `Build Ideas -> Mission Control Sync` - disabled duplicate, replaced by disabled deterministic `dfd92d8d`.
    - `4e19c300-d387-4019-b658-9664f0d665d5` - legacy `Passive Income Strategist` - disabled duplicate.
    - `dcdbbef5-2f16-4f3d-81ab-78e1b34f6fd0` - legacy `Passive Income Scout` - disabled duplicate.
    - `ca536298-53d2-41bb-8f83-21ee2626eba8` - `Weekly Content Batch` - disabled.
    - Relevance: historical or disabled. Not current behavior.

### Workflows / Scripts / Agent Manuals

1. `agents/passive-income-scout/AGENT.md`
   - Current role: full manual for raw passive-income idea generation.
   - Relevant behavior: complaint mining, levelsio gap analysis, temporal mismatch mining, data/ranking flywheel, exploding topics, Google Trends, API mining, AI vision scan, TrustMRR, agent-native lens, TikTok Shop lens.
   - Evidence: `agents/passive-income-scout/AGENT.md:3-8`, `:86-146`, `:148-193`, `:197-220`.
   - Gap: not the active scheduled behavior; no write-time evidence attachment rule for every needs-claim.

2. `scripts/passive_income_scout_handoff.py`
   - Current role: deterministic fallback report writer.
   - Relevant behavior: extracts phrase seeds from weekly passive-income signal files and writes four template idea blocks.
   - Gap: useful reliability guard, but can generate concept language from weak phrase seeds. It does not enforce VOC snippets, unverified flags, landscape proof, moat interrogation, or validation gates.

3. `agents/passive-income-strategist/AGENT.md`
   - Current role: full manual for deep passive-income validation and build recommendation.
   - Relevant behavior: saturation filter, demand validation, competition landscape, TrustMRR, agent-native fit, behavioral demand, sandbox path, build reality, marketing assessment, scoring, verdict, full blueprint, MC push.
   - Evidence: `agents/passive-income-strategist/AGENT.md:52-68`, `:76-87`, `:123-135`, `:162-179`, `:191-203`, `:237-241`.
   - Gap: no explicit Stage 3 equilibrium interrogation in the spec's form; no fake-door / waitlist / concierge MVP gate before build tasks; active cron does not run this manual.

4. `scripts/build_ideas_sync.py`
   - Current role: deterministic sync from job-market agent ideas to Mission Control.
   - Relevant behavior: routes "build ideas" into MC after dedupe.
   - Gap: job-market-supporting build ideas, not app-discovery validation. No evidence gate.

5. `agents/niche-fitness/AGENT.md`
   - Current role: consulting niche fitness review.
   - Relevant behavior: scores current and emerging consulting niches; uses last-48-hour context; pushes MC task if recommendation changes.
   - Evidence: `agents/niche-fitness/AGENT.md:1-6`, `:86-125`, `:139-172`.
   - Gap: consulting-focused; no app landscape audit or product validation gate.

6. `memory/app-marketing/os-spec.md`
   - Current role: app distribution/measurement OS.
   - Relevant behavior: every app needs audience, promise, share artifact, primary loop, borrowed audience, durable discovery channel, weekly metric, no-manual default, and kill/pause/continue rule.
   - Evidence: `memory/app-marketing/os-spec.md:3-20`, `:126-165`, `:190-240`, `:249-259`.
   - Gap: strong distribution/measurement layer, but separate from discovery and validation before build.

7. `memory/north-star/product-growth-manager.md`
   - Current role: weekly product growth governance.
   - Relevant behavior: feature velocity without users is a trap; every app requires clear distribution loop, traction metric, kill/pause threshold; weekly review must ask who will see it, why they care now, what action they take, and how success is measured.
   - Evidence: `memory/north-star/product-growth-manager.md:1-7`, `:23-38`, `:40-50`, `:66-73`, `:82-93`.
   - Gap: governance after app exists or while active; not a Niche OS or concept validation workflow.

8. `memory/north-star/opportunity-intake-gate.md`
   - Current role: prevent every interesting opportunity from becoming work.
   - Relevant behavior: applies to new app ideas; scores cash-flow, distribution advantage, reusable IP, identity fit, energy cost, timing; requires distribution path, smallest validation step, kill condition.
   - Evidence: `memory/north-star/opportunity-intake-gate.md:1-7`, `:8-18`, `:35-52`, `:70-84`.
   - Gap: good high-level gate, but no evidence-attached source snippets or Stage 3 equilibrium interrogation.

9. `memory/north-star/rubric.md`
   - Current role: North Star lane rubric.
   - Relevant behavior: app/product building + marketing is priority 2; app products must have current revenue/user/monetization/distribution review; default bias against feature work until distribution or monetization bottleneck is named.
   - Evidence: `memory/north-star/rubric.md:8-12`, `:80-90`.
   - Gap: portfolio gate, not pre-build validation workflow.

10. `skills/product-build-loop/SKILL.md`
    - Current role: product/app build implementation discipline.
    - Relevant behavior: read project context, create/update `tasks/todo.md`, plan smallest useful shipped version, implement, quality pass, verify, proof routing.
    - Evidence: `skills/product-build-loop/SKILL.md:8-25`, `:27-40`.
    - Gap: starts when building. It does not require a frozen app discovery contract, Niche OS, Stage 5 validation, or contract-first backend/frontend handoff.

11. `skills/launch-strategy/SKILL.md`
    - Current role: launch planning for apps/features/services.
    - Relevant behavior: owned/rented/borrowed launch channels, pre-launch assets, audience warm-up, launch and post-launch tactics, "never launch to silence."
    - Evidence: `skills/launch-strategy/SKILL.md:26-47`, `:50-71`, `:129-132`.
    - Gap: launch after or around product; no pre-build discovery gate.

12. `skills/positioning-angles/SKILL.md`
    - Current role: positioning/differentiation.
    - Relevant behavior: live competitive research, buyer language, gaps, eight differentiation frameworks, proof-backed angles.
    - Evidence: `skills/positioning-angles/SKILL.md:21-34`, `:37-105`, `:109-150`.
    - Gap: useful for Stage 4 differentiation, but not app-specific and not wired into app concept gates.

### Standing Instructions

1. `AGENTS.md`
   - Relevant rules:
     - Plan Mode for 3+ steps or architectural decisions: `AGENTS.md:26-27`.
     - Model routing: complex/high-stakes strategy on Sonnet-class sub-agent: `AGENTS.md:65`.
     - Sanctioned autonomy lanes are content, prospect packets, and ops self-healing; app discovery is not listed: `AGENTS.md:67-68`.
     - New prompt quality rule: cron/agent prompts need task context, detailed rules, immediate task, and output formatting: `AGENTS.md:104-105`.
     - Niche intel propagation: high niche signals update ICP/cold-email before outreach: `AGENTS.md:143-144`.
     - Future signals rule: deferred opportunities get trigger conditions: `AGENTS.md:146-147`.
     - Build/code protocols require `tasks/todo.md` before nontrivial code and verification: `AGENTS.md:282-293` in the current full file context; line range above was not printed in the captured excerpt, so this exact line range is UNVERIFIED in this report.
   - Gap: no standing app-discovery loop instruction exists yet.

2. `MEMORY.md`
   - Relevant current facts:
     - App strategy correction says distribution + retention are survival constraint and new app loops must include niche-specific content/testing and retention instrumentation before viability.
     - App content loop priority ties content to audience pains, differentiated value, and retention behavior.
   - Evidence: `MEMORY.md` entries added before this phase; `wc -c` confirmed file exists and is within budget. Exact line numbers not captured in this report.
   - Gap: memory records the strategy, but no executable workflow enforces it.

3. `/goal` usage
   - Current verified standing behavior: no local standing instruction found that requires app discovery phases to run as bounded Codex `/goal` containers.
   - Evidence: no sourced file from this phase contained a `/goal` operating rule for app discovery.
   - Status: UNVERIFIED as a current system behavior. The prior Telegram answer advised bounded goals, but that is conversation guidance, not a durable workflow.

## 2. Ranked Gap Analysis

### Gap 1 - No write-time evidence rule for app-discovery needs claims

- Spec stage/rule: Stage 1 Demand and needs; evidence rule enforced at write time.
- Current system: Niche monitor records sourced news URLs; passive-income scout has rich research methods; app marketing requires `reference_mechanics`. None requires every needs-claim to carry a source snippet or `UNVERIFIED` flag at the moment the artifact is written.
- Should do: create a dedicated Niche OS artifact writer/guard that refuses or flags each needs claim unless it has `{claim, source_url/source_path, source_snippet, confidence}`.
- Single target for Phase 2: new file `scripts/app_discovery_evidence_guard.py`.
- Verification artifact: command output from `python3 scripts/app_discovery_evidence_guard.py --input [sample_niche_os.md] --json` showing `ok=true` only when all claims have snippets or `unverified=true`.

### Gap 2 - Active passive-income crons no longer run the rich discovery/validation manuals

- Spec stage/rule: whole loop, especially Stages 1-5.
- Current system: `passive-income-scout` and `passive-income-strategist` are enabled, but actual cron prompts are deterministic handoff/guard paths with "Do not do live search", "Do not do deep ideation", and "Do not do deep validation." The rich AGENT.md manuals are not the scheduled behavior.
- Should do: do not pretend the current crons are app discovery. Either keep them as reliability guards and create a separate manual/goal-driven App Discovery Loop, or explicitly rewire them later with a strict budget and evidence guard.
- Single target for Phase 2: new file `skills/app-discovery-loop/SKILL.md` rather than editing the existing passive-income crons first.
- Verification artifact: file diff showing the new skill exists and includes Stage 0-6, evidence schema, Stage 3 moat gate, Stage 5 validation gate, and "no code before validation."

### Gap 3 - No Stage 3 equilibrium interrogation gate

- Spec stage/rule: Stage 3 Equilibrium interrogation / moat-check.
- Current system: passive-income strategist has competition, uniqueness, founder sandbox, defensibility, distribution difficulty, and "what beginners get wrong"; but it does not force "why does this gap still exist, what is the current equilibrium, and what would have to be true for a new entrant to hold ground." It also does not route this stage through frontier reasoning as a distinct gate.
- Should do: add a Stage 3 artifact template and scoring guard: structural reason gap exists, current equilibrium, incumbent response, distribution barrier, willingness-to-pay barrier, new entrant wedge, kill/continue verdict.
- Single target for Phase 2: `skills/app-discovery-loop/SKILL.md`.
- Verification artifact: sample `memory/app-discovery/[niche]/stage-3-equilibrium.md` containing those fields plus a final `KILL|PAUSE|CONTINUE` decision.

### Gap 4 - Validation-before-build exists as philosophy, not as an enforced app build gate

- Spec stage/rule: Stage 5 Validation gate before Stage 6 Build.
- Current system: opportunity intake requires smallest validation step; product growth blocks feature work without distribution; passive-income strategist has sandbox path and value proposition tests. But there is no app-build entry gate requiring fake-door, concierge MVP, or direct probe evidence before code.
- Should do: require a `validation_gate.md` artifact before build routing, with kill/pause/cap thresholds and evidence of fake-door/waitlist/concierge/direct probe.
- Single target for Phase 2: `skills/product-build-loop/SKILL.md` or new `skills/app-discovery-loop/SKILL.md`. Cleaner first target: `skills/app-discovery-loop/SKILL.md`; later `product-build-loop` can check for the artifact.
- Verification artifact: diff showing the skill requires validation artifact before Stage 6; optional command `rg -n "validation_gate|fake-door|concierge|direct probe|no code" skills/app-discovery-loop/SKILL.md`.

### Gap 5 - No contract-freeze / build-routing handoff for Codex + Claude Design + Opus

- Spec stage/rule: Build configuration.
- Current system: `product-build-loop` requires a plan, implementation, quality pass, and verification. It does not mention freezing the API/data contract before parallel Codex backend, Claude Design visual exploration, Opus frontend implementation, and Codex integration.
- Should do: add a build-ready spec checklist that requires a frozen data contract before handoff.
- Single target for Phase 2: `skills/app-discovery-loop/SKILL.md` first; possible later follow-up `skills/product-build-loop/SKILL.md`.
- Verification artifact: diff showing contract freeze dependency graph; sample `build_ready_spec.md` with API schema and "frontend blocked until contract frozen" marker.

### Gap 6 - Source quality ordering is not enforced for app discovery

- Spec stage/rule: Stage 0 Sourcing.
- Current system: passive-income scout has broad methods and weekly trend/API files; consulting niche monitor scans target industries; neither enforces the spec's source ranking: founder-market fit, distribution-adjacent, demand signal, chart-chasing near zero.
- Should do: source-tag every candidate niche with a `source_quality` field and reject/deprioritize chart-chasing candidates.
- Single target for Phase 2: `skills/app-discovery-loop/SKILL.md`.
- Verification artifact: sample `candidate_niches.md` with source tags and a guard/section showing chart-chasing candidates capped or rejected.

### Gap 7 - Differentiation substrate is not forced into every app concept

- Spec stage/rule: four owned edges and Stage 4 differentiation menu.
- Current system: passive-income strategist includes JT stack leverage, agent-native fit, TrustMRR, marketing, uniqueness, and competition; positioning skill requires proof-backed differentiation. But no app concept must map to one of the four owned edges: game-theoretic moat-check, SEO-first distribution, ensemble methodology, or data pipelines/client adjacencies.
- Should do: require `unique_mechanism` plus `edge_that_powers_it` in every build-ready spec.
- Single target for Phase 2: `skills/app-discovery-loop/SKILL.md`.
- Verification artifact: sample build-ready spec where concepts without an owned edge are marked `KILL_OR_SHRINK`.

### Gap 8 - Current systems can still route ideas into MC without full evidence gates

- Spec stage/rule: validation-before-build and human gate.
- Current system: disabled `Build Ideas Sync` can create "Build idea" tasks from job-market agent ideas; passive-income strategist manual can push BUILD tasks after analysis. Current active strategist cron does not push in fallback mode, but the manual still allows MC build routing.
- Should do: app-related MC build tasks should require evidence-guard and validation-gate links in the task description.
- Single target for Phase 2: `scripts/build_ideas_sync.py` only if JT wants this applied to job-market build ideas; otherwise leave it disabled and create the new app-discovery skill first.
- Verification artifact: diff in `scripts/build_ideas_sync.py` requiring evidence/validation fields, or explicit decision note to leave disabled.

### Gap 9 - Bounded `/goal` containerization is not a durable instruction

- Spec stage/rule: parent loop coordinates phases; each phase is one bounded Codex `/goal`.
- Current system: isolated crons are bounded by schedule, prompts, and timeouts, but no verified file requires app discovery phases to run as bounded `/goal`s. Prior conversation guidance exists but is not a standing workflow.
- Should do: define phase-specific `/goal` templates in the new skill.
- Single target for Phase 2: `skills/app-discovery-loop/SKILL.md`.
- Verification artifact: file diff containing exact `/goal` prompt templates and done conditions for Stage 1, Stage 2, Stage 3, Stage 5, and Stage 6.

## 3. Load-Bearing Elements Status

1. Evidence rule enforced at write time
   - Current status: DOES NOT.
   - Current partials: Niche monitor records source URLs; app marketing requires `reference_mechanics`; passive-income scout/strategist ask for searches and evidence caveats.
   - Missing: a write-time schema/guard where every needs claim has a source snippet or `UNVERIFIED`.

2. Stage 3 equilibrium interrogation gate
   - Current status: PARTIALLY.
   - Current partials: passive-income strategist evaluates saturation, competition, uniqueness, defensibility, distribution difficulty, and sandbox path.
   - Missing: explicit current-equilibrium analysis, "why gap still exists", "what must be true to enter/hold ground", incumbent response, structural kill reasons, and frontier-reasoning routing.

3. Validation-before-build gate
   - Current status: PARTIALLY.
   - Current partials: opportunity intake requires smallest validation step; product growth blocks features without distribution/monetization bottleneck; passive-income strategist has sandbox path and value-proposition gates.
   - Missing: required fake-door/waitlist/concierge/direct-probe artifact before Stage 6 build routing.

4. Bounded `/goal` containerization
   - Current status: DOES NOT / UNVERIFIED.
   - Current partials: crons are isolated and some prompts have bounded outputs/timeouts.
   - Missing: a durable instruction that each app discovery phase runs as its own Codex `/goal` with done condition, budget, and verification artifact.

## 4. Explicit Reductions List

1. Stop treating the active passive-income Scout/Strategist crons as if they perform deep app discovery.
   - Reason: actual cron definitions are deterministic handoff/guard paths.
   - Direct action if approved: document them as signal/guard infrastructure, not the Product Opportunity Engine.

2. Stop routing generic build ideas toward work unless an evidence artifact and validation artifact exist.
   - Reason: the spec says ideation is cheap and gates are the product.
   - Direct action if approved: require evidence/validation fields before any app build task is created.

3. Stop generating needs from model priors.
   - Reason: the spec explicitly says models invent fluent generic needs when asked what a niche wants.
   - Direct action if approved: Niche OS writer must ingest real VOC/review/forum/search snippets and flag unsourced claims as `UNVERIFIED`.

4. Stop over-weighting "same app, cleaner UI".
   - Reason: spec says kill or shrink if the only mechanism is cleaner UI.
   - Direct action if approved: Stage 4 requires owned-edge mechanism; `taste advantage` alone must map to a real edge or shrink.

5. Stop considering Stage 6 build automation the valuable part.
   - Reason: spec says build is cheap, last, and least precious.
   - Direct action if approved: Product build loop should only run after Niche OS, landscape audit, moat gate, and validation gate exist.

6. Stop running broad continuous loops across many niches.
   - Reason: spec says one niche at a time; continuous looping compounds cost and drift.
   - Direct action if approved: new skill uses one active niche folder and one phase goal at a time.

7. Stop app-marketing volume increases without measurement.
   - Reason: current App Marketing OS already says do not increase volume until metrics capture is reliable.
   - Direct action if approved: keep distribution companion separate; do not merge it into discovery until the companion spec is reviewed.

8. Stop creating new recurring jobs as the default implementation.
   - Reason: AGENTS and North Star both prefer state files/tasks over cron bloat; the spec calls for bounded `/goal` phases.
   - Direct action if approved: Phase 2 should start with a manual skill + artifact templates, not a cron.

## 5. Proposed Phase 2 Changes And Verification Artifacts

No Phase 2 changes are approved yet. Proposed sequence if JT approves:

1. Create `skills/app-discovery-loop/SKILL.md`
   - Purpose: canonical Product Opportunity Engine workflow.
   - Includes: Stage 0-6, source-quality ranking, evidence rule, Niche OS template, landscape audit template, Stage 3 moat gate, Stage 4 owned-edge mechanism, Stage 5 validation gate, build-ready spec, bounded `/goal` templates.
   - Verification artifact: `git diff -- skills/app-discovery-loop/SKILL.md`; `rg -n "Evidence rule|Stage 3|Validation gate|/goal|contract freeze" skills/app-discovery-loop/SKILL.md`.

2. Add `scripts/app_discovery_evidence_guard.py`
   - Purpose: verify claims in Niche OS / gap matrix artifacts.
   - Verification artifact: command output:
     - failing fixture: `ok=false`, claim missing snippet
     - passing fixture: `ok=true`, all claims sourced or unverified

3. Add artifact templates under `memory/app-discovery/templates/`
   - Candidate list, Niche OS, landscape audit, equilibrium interrogation, validation gate, build-ready spec.
   - Verification artifact: file list plus template diff.

4. Optionally update `skills/product-build-loop/SKILL.md`
   - Purpose: require `build_ready_spec.md` and frozen data contract before build starts for new app concepts.
   - Verification artifact: diff plus `rg -n "build_ready_spec|contract freeze|validation_gate" skills/product-build-loop/SKILL.md`.

5. Optionally update existing passive-income docs later
   - Purpose: distinguish passive-income idea scouting from the new app-discovery loop.
   - Verification artifact: diff in `agents/passive-income-scout/AGENT.md` or `agents/passive-income-strategist/AGENT.md`.
   - Note: I would not make this the first change. The safer move is to build the new manual loop first, then decide whether passive-income should feed it.

6. Do not create or modify crons in the first Phase 2 pass unless JT explicitly approves a stable job ID and scope.
   - Verification artifact if later approved: `openclaw cron get [stable_id]` before and after, with prompt diff and no batched changes.

## Bottom Line

Current Eve has pieces of the desired system, but not the spec's actual app discovery loop.

The closest existing pieces are:

- Passive-income Scout/Strategist manuals for idea and validation logic.
- Product Growth Manager / Opportunity Intake Gate for focus, distribution, and kill decisions.
- App Marketing OS for post-build distribution and measurement.
- Product Build Loop for verified implementation.

The missing center is a dedicated Product Opportunity Engine that forces real VOC evidence, landscape proof, equilibrium interrogation, validation-before-build, owned-edge differentiation, and bounded `/goal` artifacts.

Recommended Phase 2 starting point: create the manual skill and evidence guard first. Do not touch crons yet.
