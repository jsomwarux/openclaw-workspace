# Phase 2 Item 1 Verification

Implemented file: `/Users/jtsomwaru/.openclaw/workspace/skills/app-discovery-loop/SKILL.md`


## git diff --no-index -- /dev/null skills/app-discovery-loop/SKILL.md

```text
diff --git a/skills/app-discovery-loop/SKILL.md b/skills/app-discovery-loop/SKILL.md
new file mode 100644
index 0000000..01245ab
--- /dev/null
+++ b/skills/app-discovery-loop/SKILL.md
@@ -0,0 +1,154 @@
+---
+name: app-discovery-loop
+description: "Use when evaluating a niche, app idea, passive-income product concept, or product opportunity before build work starts."
+---
+
+# App Discovery Loop
+
+Use this before building a new app, ranking product, dashboard, passive-income product, or major app wedge. The goal is not autonomous ideation volume. The goal is one evidence-backed opportunity, strict kill gates, and a build-ready contract only after validation.
+
+## Hard Rules
+- One niche at a time. One active folder at `memory/app-discovery/[slug]/`.
+- No cron creation or modification from this skill.
+- No passive-income doc rewiring unless JT separately approves it.
+- No code before Stage 5 validation passes and a build-ready spec exists.
+- If a claim cannot be sourced, mark it `UNVERIFIED` instead of smoothing it into confident prose.
+- "Same app, cleaner UI" is not enough. Kill or shrink unless there is a real owned edge.
+
+## Stage 0 - Source Selection
+Create `candidate_niches.md`.
+
+Rank sources in this order:
+1. Founder-market fit: niches JT understands, can reach, or can credibly talk to.
+2. Distribution-adjacent: niches with obvious X, LinkedIn, Reddit, TikTok, SEO, marketplace, or community access.
+3. Demand signal: reviews, forum complaints, search terms, job postings, paid tools, templates, spreadsheets, agencies, or repeated workarounds.
+4. Chart-chasing: trend lists, generic startup ideas, broad AI hype. Use only as weak input.
+
+Each candidate needs `source_quality`, `evidence_paths_or_urls`, `why_now`, `distribution_surface`, and `kill_reason_if_any`.
+
+## Stage 1 - Niche OS
+Create `niche_os.md`.
+
+Required sections:
+- user archetypes
+- repeated pains
+- existing workarounds
+- emotional language / voice of customer
+- willingness-to-pay evidence
+- frequency / retention hypothesis
+- trust signals and anti-needs
+- distribution surfaces
+- needs claims table
+
+Evidence rule: every needs claim must include `claim`, `source_url_or_path`, `source_snippet`, and `confidence`, or be marked `UNVERIFIED` with a reason. Run `scripts/app_discovery_evidence_guard.py` when it exists. Until then, manually inspect the claims table and label any unsupported claim `UNVERIFIED`.
+
+## Stage 2 - App Landscape Audit
+Create `landscape_audit.md`.
+
+Inspect app stores, web apps, Chrome extensions, templates, Reddit mentions, Product Hunt, GitHub when relevant, and SEO results. Score competitors by:
+- target user
+- core promise
+- pricing
+- feature coverage
+- review complaints
+- freshness
+- acquisition channel
+- retention hooks
+- trust / compliance posture
+- visible gaps
+
+Output a gap matrix: `users want X`, `existing options do Y poorly`, `evidence is Z`, `risk is R`.
+
+## Stage 3 - Equilibrium Interrogation
+Create `stage_3_equilibrium.md`. This is a gate, not a brainstorming section.
+
+Answer:
+- Why does this gap still exist?
+- What current equilibrium keeps users on bad tools or manual workarounds?
+- What would incumbents do if this worked?
+- What distribution barrier blocks new entrants?
+- What trust, switching-cost, or willingness-to-pay barrier could kill this?
+- What wedge lets JT enter and hold ground?
+- Which owned edge powers it: game-theoretic moat-check, SEO-first distribution, ensemble methodology, data pipelines/client adjacency, or another explicit JT edge?
+
+Verdict must be exactly `KILL`, `PAUSE`, or `CONTINUE`. `CONTINUE` requires a credible wedge and at least one owned edge.
+
+## Stage 4 - Product Concept And Unique Mechanism
+Create `concept_brief.md`.
+
+Required fields:
+- target user
+- painful moment
+- current workaround
+- wedge feature
+- unique mechanism
+- edge_that_powers_it
+- share artifact
+- retention loop
+- monetization hypothesis
+- first distribution channel
+- why this is not just cleaner UI
+
+If the unique mechanism is weak, shrink the product until the mechanism is real or mark `KILL_OR_SHRINK`.
+
+## Stage 5 - Validation Gate
+Create `validation_gate.md` before any build task.
+
+Use the smallest proof step that can kill or sharpen the idea:
+- fake-door page
+- waitlist
+- concierge MVP
+- direct probe interviews/messages
+- Reddit/X/LinkedIn positioning test
+- SEO demand test
+- manual spreadsheet/template test
+
+Required fields:
+- validation method
+- audience reached
+- proof artifact path or URL
+- activation signal
+- objections
+- result
+- threshold
+- decision: `KILL`, `PAUSE`, `ITERATE`, or `BUILD`
+
+`BUILD` requires evidence stronger than "I like this idea." If validation is skipped, mark the build decision `UNVERIFIED` and stop.
+
+## Stage 6 - Build-Ready Spec And Contract Freeze
+Create `build_ready_spec.md` only after Stage 5 returns `BUILD`.
+
+Required sections:
+- frozen problem statement
+- frozen target user
+- MVP scope
+- non-goals
+- frozen data contract: entities, fields, event names, API shape, import/export formats, and analytics events
+- frontend states and screens
+- backend responsibilities
+- validation evidence link
+- risks and kill thresholds
+- launch and retention measurement plan
+
+The frozen data contract is the handoff boundary. This contract freeze happens before frontend implementation or build routing. Claude Design may explore visuals from the spec, but it must not invent product behavior. Frontend implementation is blocked until the data contract is frozen.
+
+## Bounded `/goal` Templates
+Use one bounded goal per phase. Do not run one giant forever loop.
+
+Stage 1:
+`/goal Create a sourced Niche OS for [niche]. Done when memory/app-discovery/[slug]/niche_os.md has sourced or UNVERIFIED needs claims and an evidence-guard result.`
+
+Stage 2:
+`/goal Create an app landscape audit for [niche]. Done when memory/app-discovery/[slug]/landscape_audit.md has competitor scoring and a sourced gap matrix.`
+
+Stage 3:
+`/goal Run equilibrium interrogation for [niche/app concept]. Done when stage_3_equilibrium.md has KILL, PAUSE, or CONTINUE with explicit structural reasons.`
+
+Stage 5:
+`/goal Design and evaluate the smallest validation gate for [concept]. Done when validation_gate.md has evidence, objections, threshold result, and KILL/PAUSE/ITERATE/BUILD.`
+
+Stage 6:
+`/goal Produce build-ready spec for [validated concept]. Done when build_ready_spec.md freezes scope, data contract, validation link, launch metrics, and kill thresholds.`
+
+## Completion Artifact
+Return paths for every artifact created, commands run, and any `UNVERIFIED` claims. If a stage is blocked, stop at the gate and report the missing evidence.
```


## rg -n "Evidence rule|Stage 3|Validation gate|/goal|contract freeze" skills/app-discovery-loop/SKILL.md

```text
43:Evidence rule: every needs claim must include `claim`, `source_url_or_path`, `source_snippet`, and `confidence`, or be marked `UNVERIFIED` with a reason. Run `scripts/app_discovery_evidence_guard.py` when it exists. Until then, manually inspect the claims table and label any unsupported claim `UNVERIFIED`.
62:## Stage 3 - Equilibrium Interrogation
133:The frozen data contract is the handoff boundary. This contract freeze happens before frontend implementation or build routing. Claude Design may explore visuals from the spec, but it must not invent product behavior. Frontend implementation is blocked until the data contract is frozen.
135:## Bounded `/goal` Templates
139:`/goal Create a sourced Niche OS for [niche]. Done when memory/app-discovery/[slug]/niche_os.md has sourced or UNVERIFIED needs claims and an evidence-guard result.`
142:`/goal Create an app landscape audit for [niche]. Done when memory/app-discovery/[slug]/landscape_audit.md has competitor scoring and a sourced gap matrix.`
144:Stage 3:
145:`/goal Run equilibrium interrogation for [niche/app concept]. Done when stage_3_equilibrium.md has KILL, PAUSE, or CONTINUE with explicit structural reasons.`
148:`/goal Design and evaluate the smallest validation gate for [concept]. Done when validation_gate.md has evidence, objections, threshold result, and KILL/PAUSE/ITERATE/BUILD.`
151:`/goal Produce build-ready spec for [validated concept]. Done when build_ready_spec.md freezes scope, data contract, validation link, launch metrics, and kill thresholds.`
```


## frontmatter validation

```text
frontmatter ok
```
