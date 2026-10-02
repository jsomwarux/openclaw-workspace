# Growth OS Optimal Completion Sequencing Addendum

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the eight-lane Growth OS end to end as quickly as possible while minimizing duplicated model work, keeping Mission Control as the only human queue, and activating automation one proven capability at a time.

**Architecture:** Preserve the accepted shared spine: Mission Control owns human decisions, Eve/OpenClaw orchestrates, domain systems own facts, and n8n executes only deterministic work whose burden has been proven manually. Build independent lanes in parallel behind frozen contracts and single-writer file ownership. External sends, posts, applications, RSVPs, purchases, deployments, and schedule activation remain JT-controlled.

**Tech Stack:** Mission Control/Convex, OpenClaw/Eve through Codex, Claude Code, n8n, Python, TypeScript, `jt-ops`, Google Drive, Notion Content Calendar, GPT, Grok/xAI, GitHub.

**Authority status:** Proposed sequencing addendum for JT review. It does not supersede the canonical architecture, mutable state file, or `2026-09-24-ai-workflow-growth-os-completion.md`. After JT approval, link this addendum from the canonical completion plan and update the state file's next action; until then, conflicts resolve to the existing canonical source order.

---

## 1. Terminology and operating rule

- **Codex means Eve:** when JT says “Codex,” he means Eve operating through Codex, not a separate worker lane.
- **Claude Code:** reserved for complex multi-file implementation, difficult debugging, n8n construction, and high-risk integration review.
- **Eve/Codex:** owns orchestration, plans, contracts, deterministic modules, tests, fixtures, integration, proof collection, and JT communication.
- **One problem gets one builder.** A second model reviews an immutable diff or SHA; it does not independently rebuild the same solution unless the first attempt fails.

## 2. Current n8n inventory

### Growth OS workflows already built

| Workflow | Current state | Role | Decision |
|---|---|---|---|
| `c2discoveryMAIN1` / `cohort-two-prospect-discovery` | Live n8n: inactive, 58 nodes, not archived | Prospect discovery, evidence collection, qualification, packet assembly | Preserve. Do not schedule yet. Commercial output remains blocked by official-domain/identity quality. |
| `c2discoveryERRH1` / `cohort-two-discovery-error-handler` | Live n8n: inactive, 4 nodes, not archived | Failure capture for the main workflow | Preserve and attach to any accepted pilot. It is not sufficient as an external liveness monitor. |

The accepted live deployment is pinned to merge `0a27bcce…`. The dirty primary checkout currently exposes a 57-node source file, while accepted live state records 58 nodes. Treat that discrepancy as a release-integrity check; never deploy from the primary checkout.

### Existing n8n workflows that are not part of Growth OS

The local n8n instance also contains active or staged workflows for Glow Index, Nash Satoshi, Oswald RAG, client work, and demos. They are reusable implementation evidence, not Growth OS completion. Their existence must not be counted as progress on the eight lanes or changed as part of this plan.

## 3. What still needs to be built

### Required to finish the operating system

1. **LinkedIn Program 0 completion**
   - retire the contradictory Wednesday skill authority;
   - obtain a clean 196/196 suite;
   - run phase one and collect JT’s bounded truth/focus/permission response;
   - run phase two and obtain independent `VERDICT: CONFIRM`;
   - prove three posted fixture modes: build/field lesson, teardown, and AI news;
   - prove the single Mission Control acknowledgment/day-seven loop.

2. **X/Grok manual router proof**
   - audit/reconcile the existing Revenue Signal Lab forward period for source usefulness, duplicates/noise, downstream artifacts, and actual outcomes; count it as cycle 1 only if the evidence is complete;
   - create the minimum viable X voice/source corpus, then expand only where the audit shows gaps;
   - run one fresh manual Intelligence Router cycle after the existing-period audit, or two fresh cycles if the old evidence is incomplete;
   - record noise, duplication, source usefulness, routed destination, and actual downstream yield;
   - decide from evidence whether stateful n8n collection is warranted.

3. **Prospect/outreach commercial closure**
   - reconcile authoritative Gmail reply state;
   - retain the current main/error workflow inactive;
   - keep Brave domain resolution parked until relationship semantics exist;
   - complete the 100-row Tier B benchmark, suppression CSV, immutable 25-row batch, and JT review;
   - use manual Tier A research as the floor until automation produces commercially valid packets.

4. **Jobs lifecycle closure**
   - keep the approved Decagon card frozen unless JT separately authorizes application;
   - prove application outcome reconciliation on a later authorized role;
   - connect job-owner outcomes to the generic Mission Control lifecycle;
   - do not add n8n unless a measured collection/retry burden appears.

5. **App marketing readiness**
   - create one verified product-truth profile per app;
   - require a live conversion destination and measurable event;
   - activate one app lane at a time, beginning with whichever app actually clears those gates;
   - reuse the Content OS rather than create separate content workflows.

6. **Networking, profile/site, and passive-income lanes**
   - keep networking and profile/site event-driven/manual until burden is demonstrated;
   - audit existing passive-income components and produce one proprietary-pain packet;
   - keep generic passive-income recurrence disabled.

7. **Shared operations**
   - finish the lane registry, owner/kill-switch/cost/freshness/receipt fields, outcome pointers, and one authoritative Today allocator;
   - add a zero-LLM no-run/freshness monitor and receipt for every capability before recurrence;
   - complete a ten-weekday operating proof with no duplicate or lost actions.

### Conditional n8n workflows — build only when earned

| Candidate workflow | Build trigger | Current decision |
|---|---|---|
| Prospect request/result adapter around cohort two | Accepted source/live delta map plus a commercially valid manual pilot | Delta/repair existing workflow; do not build a second prospect engine. |
| LinkedIn evidence selector | Three accepted posted fixtures show repeated selection/assembly burden | Start in tested Python/OpenClaw modules. Add thin n8n routing only if scheduling/state burden is real. |
| X Intelligence Router state layer | Two manual cycles show useful downstream yield, noise ≤20%, and cursor/dedupe burden | Conditional. n8n owns cursor/dedupe/hash only; Grok analyzes; Eve verifies. |
| App content trigger | App has verified truth profile, live destination, and measurable conversion event | One app at a time. Reuse shared content contracts. |
| Passive-income scout recurrence | One proprietary-pain packet has a real buyer, distribution path, and validation event | Deferred. |
| Networking/profile/site workflows | Manual process repeatedly misses time-sensitive opportunities | Not currently justified. |

## 4. Activation policy

Do **not** wait for the entire eight-lane system to be complete before activating anything. Also do **not** turn on multiple schedules together.

Each capability advances independently through this ladder:

1. **Local proof:** fixtures, deterministic tests, mutation/adversarial tests, no network side effects.
2. **Inactive deployment:** exact accepted bundle, source/live equality, disabled schedule and external actions.
3. **Manual controlled pilot:** one bounded run with before/after state snapshots; workflow remains inactive.
4. **Outcome reconciliation:** prove the output reached Mission Control, JT’s decision was captured, and the domain owner received the outcome.
5. **Internal recurrence approval:** JT approves the exact workflow, schedule, cost ceiling, egress, disable procedure, and kill switch.
6. **One-capability soak:** require a capability-specific clean window before adding the next schedule: at least three expected scheduled opportunities and five elapsed weekdays, with valid receipts, no duplicate/lost outcomes, freshness alerts proven, and every produced action consumed or typed-closed. If a capability runs less than three times in five weekdays, continue until three expected opportunities have occurred.
7. **Next capability:** only after the previous capability’s receipt and rollback path are proven.

External actions remain manual even after internal recurrence is active.

### Recommended activation order

1. **LinkedIn acknowledgment/check-in projection** — internal, low-risk, after Program 0 and three fixture modes are accepted.
2. **Jobs discovery/package recurrence** — only after one authorized end-to-end outcome reconciliation; no application automation.
3. **X Intelligence Router internal recurrence** — only if the two manual cycles earn it.
4. **Prospect discovery recurrence** — only after a controlled pilot produces commercially valid packets and identity/domain quality is resolved or safely narrowed.
5. **First conversion-ready app content trigger.**
6. **Additional app or passive-income recurrence** only after the previous lane is consumed and measured.

The cohort-two n8n schedule should not be first merely because its workflow already exists; its current bottleneck is output validity, not scheduling.

## 5. Parallel execution model

Use at most three builder/reviewer lanes plus Eve as integration owner. Every lane gets an isolated worktree, exclusive files, a frozen interface, and an immutable handoff SHA.

| Lane | Owner | Scope | Must not touch |
|---|---|---|---|
| Integration/control | Eve/Codex | DAG, contracts, Mission Control integration, lane registry, proofs, user gates | Lane implementation files owned by another active builder |
| LinkedIn/Jobs deterministic lane | Eve/Codex | Program 0, corpus/fixtures, lifecycle adapters, focused tests | n8n workflow JSON |
| n8n/outreach lane | Claude Code | Read canonical n8n lessons/protocols, prove the accepted source/live delta, then assess only a buyer-recovery or verified-domain-input path that avoids the parked identity problem | LinkedIn/Jobs authority files; no broad redesign |
| Fresh verification | Whichever model did not build | Diff/SHA review, contract enforcement, full milestone suite | No implementation edits except a separately assigned repair |

### Model-budget rules

- Use Eve/Codex for deterministic implementation, test loops, schema work, fixtures, CLI wiring, and integration.
- Use Claude Code for n8n workflow construction, complex multi-file code, difficult runtime bugs, and adversarial architecture review.
- Review by narrow diff, contract, and test evidence—not full-repository context dumps.
- Run focused tests per task; run cross-module review and the full suite once per milestone, not after every tiny commit.
- Never pay two models to generate competing implementations by default.

## 6. Execution waves

### Wave 0 — unblock and freeze (immediate)

- [ ] JT authorizes/enables exact migration of Skill Workshop proposal `wednesday-linkedin-20260928-029c4a76c9`; Eve/operator applies it through Skill Workshop. Direct editing remains prohibited.
- [ ] Rerun all 196 LinkedIn Program 0 tests.
- [ ] Capture a fresh, read-only Growth OS/n8n inventory and resolve the accepted-58-versus-primary-57 source discrepancy.
- [ ] Freeze lane contracts, file ownership, and activation gates in the lane registry.
- [ ] Obtain separate JT authorization to rotate/revoke the exposed Convex runtime credential and detected Slack/HubSpot credentials; block live activation on affected surfaces until rotation is proven.

### Wave 1 — parallel manual truth and local completion

**Eve/Codex**
- [ ] Run LinkedIn phase one after the suite is clean.
- [ ] Produce the bounded JT recovery/focus/permission packet.
- [ ] Audit the existing Revenue Signal Lab forward period before building new X machinery; count it as cycle 1 only if its evidence is complete.
- [ ] Build only the remaining X manual-router evaluation harness/corpus delta needed for one fresh cycle (or two if the old evidence is incomplete).
- [ ] Finish shared lane-registry and learning-loop contract gaps.

**Claude Code**
- [ ] Read `/Users/jtsomwaru/projects/n8n-agent/tasks/lessons.md` and `docs/agents/workflow-protocols.md` in full before any n8n action.
- [ ] Resolve the accepted-live-versus-source delta from an immutable accepted checkout; never use the dirty primary checkout as release authority.
- [ ] Check whether a buyer-recovery-only or verified-domain-input path can produce commercially valid packets without reopening parked manager/affiliate identity semantics.
- [ ] Only if that bounded path is solvable, produce the exact node-by-node n8n blueprint and offline runtime-shape proof. Otherwise return a typed `BLOCKED` finding and stop; do not perform a general redesign, deploy, or activate.

**JT**
- [ ] Provide the minimum LinkedIn inputs first: 30-day focus plus one genuinely permissioned positive fixture. Expand the full gold set after phase one identifies remaining gaps.
- [ ] Provide the minimum X corpus/watchlist inputs in Section 7. Expand only after the existing Revenue Signal Lab audit identifies gaps.
- [ ] Unlock Gmail locally for authoritative read-only reply reconciliation.

### Wave 2 — three content fixtures plus commercial bridge

- [ ] Complete LinkedIn fixture 1: permissioned build/field lesson.
- [ ] Complete LinkedIn fixture 2: public-evidence teardown.
- [ ] Complete LinkedIn fixture 3: primary-source AI news/operator implication.
- [ ] For each fixture, prove exact packet, one rendered image, JT decision, posted/not-yet/won’t-post acknowledgment, and day-seven outcome when posted.
- [ ] Run two manual X Router cycles and measure downstream yield.
- [ ] Complete Tier B benchmark/suppression/immutable-batch assets while Tier A stays manual.
- [ ] Independently verify each milestone; keep all schedules off.

### Wave 3 — build only earned automation

- [ ] Implement the smallest LinkedIn selector/routing automation justified by the three fixtures.
- [ ] Implement X cursor/dedupe/state only if the two manual cycles prove the burden.
- [ ] Repair or narrow cohort-two around the accepted commercially useful capability; do not broaden identity claims.
- [ ] Connect one conversion-ready app profile to the shared content packet lifecycle.
- [ ] Keep networking, profile/site, and passive-income manual unless new evidence earns automation.

### Wave 4 — inactive integration and controlled pilots

- [ ] Deploy each accepted capability inactive from an immutable bundle.
- [ ] Prove source/live equality, credentials by reference, egress allowlist, state snapshots, and rollback.
- [ ] Run one controlled pilot per capability, one at a time.
- [ ] Reconcile every result through Mission Control and its domain owner.
- [ ] Record cost, runtime, JT review time, defects, duplicates, and downstream usefulness.

### Wave 5 — one-by-one recurrence

- [ ] Approve and activate only the first internal capability that passes its pilot.
- [ ] Prove its kill switch, external heartbeat/freshness alert, disable path, and no-lost-outcome behavior.
- [ ] Add the next capability only after the previous one produces a clean receipt.
- [ ] Complete ten consecutive weekdays of integrated operation.

## 7. JT’s highest-leverage manual preparation

### Priority 1 — unblock Program 0 and commercial truth in parallel

- Authorize/enable the exact Wednesday-skill proposal migration so Eve/operator can apply it through Skill Workshop.
- When phase one produces the bounded packet, answer the current-focus, historical-publication, and permission questions exactly; do not infer missing history.
- Unlock Gmail locally so Eve can perform the authorized read-only reply check; this commercial lane does not wait on the content build.
- Mark each known outreach thread: replied, no reply, bounced, opted out, or unknown.

### Priority 2 — minimum viable LinkedIn truth, then the full gold set

Provide first:

- current 30-day audience and commercial focus in one paragraph;
- one genuinely permissioned positive build/field-lesson source;
- permission status: `approved-named`, `approved-anonymized`, or `not approved`;
- exact final text and public URL for the strongest known published LinkedIn example.

Then expand the same folder or document to include:

- 10–20 LinkedIn posts JT definitely published and still likes;
- exact final published text, not drafts or summaries;
- public LinkedIn URL where available;
- label each `KEEP`, `MIXED`, or `REJECT`;
- one sentence explaining the label;
- for edited posts, the original draft and JT’s final text if available;
- permission status for any client/build proof: `approved-named`, `approved-anonymized`, or `not approved`;

The first positive fixture must be genuinely permissioned client proof or a verified field lesson. Internal machinery such as Mission Control, job search, outreach internals, or Eve internals is not publishable proof in v1.

### Priority 3 — minimum viable X/Grok corpus, then expand by evidence

Provide first:

- 5–10 JT-authored X posts labeled `KEEP`, `MIXED`, or `REJECT` with short reasons;
- 10 admired X posts, kept separate from JT-authored examples;
- 5 priority accounts;
- 3 recurring topics/searches;
- 3 examples JT would route to different destinations such as LinkedIn, outreach, product, career, or archive.

Eve first audits the existing Revenue Signal Lab forward period. Count it as the first manual cycle only if source usefulness, duplication/noise, downstream artifacts, and outcomes are complete. Then run one fresh Router cycle; if the old evidence is incomplete, run two fresh cycles. Expand only where those results show gaps, toward:

- at least 20 JT-authored X posts labeled `KEEP`, `MIXED`, or `REJECT` with short reasons;
- 30 admired X posts, separated from JT-authored examples;
- 10–20 accounts for a curated operator/AI/workflow watchlist;
- 5–10 recurring topics or searches;
- examples of posts JT would want routed to LinkedIn, outreach, product, career, or archive;
- any JT-forwarded posts that should seed the first two manual router cycles.

Do **not** set up Grok Bot yet. Do **not** create Grok Automations yet. First prove two manual router cycles. Grok Bot is only justified for a five-account Tier A research spike if ordinary public/API research leaves material gaps. Grok Automations are only justified if public-X scouting helps while n8n remains the durable cursor/dedupe owner.

### Priority 4 — remaining outcome truth

- For any application JT chooses to submit later, return the official URL and exact submitted date so the Jobs outcome loop can be proved.

### Priority 5 — app truth and conversion readiness

Eve first pre-populates one truth profile per app from authoritative repositories, project guidance, and live surfaces. JT only confirms unresolved claims/conversion choices and supplies assets Eve cannot access. For Yardstick, Action Arena, and Nash Satoshi, the final profile must contain:

- current live URL/store surface;
- exact conversion action;
- what is shipped versus planned;
- approved/prohibited claims;
- three strongest screenshots or proof artifacts;
- one measurable event such as signup, install, activation, or waitlist conversion.

### Priority 6 — costs and credentials

- Decide pilot ceilings for X API/xAI, GPT, Claude Code, and any optional enrichment tool.
- Confirm whether existing Grok/xAI access is available; do not purchase anything yet.
- Separately authorize rotation/revocation of the exposed Convex runtime credential and detected Slack/HubSpot credentials. Affected live activation remains blocked until proof of rotation exists.
- Enter any needed credentials only through protected host-owned credential setup when requested. Never paste them into chat.

## 8. Immediate next actions

1. **JT:** authorize/enable the exact Wednesday skill migration and unlock Gmail locally.
2. **Eve/Codex:** rerun 196 tests, execute LinkedIn phase one, and return the bounded JT packet.
3. **Claude Code, in parallel:** after reading the n8n lessons/protocols, resolve the accepted source/live delta and assess only the bounded buyer-recovery/verified-domain path; blueprint it only if solvable.
4. **JT, in parallel:** provide the minimum LinkedIn focus/permission/example inputs and minimum X corpus/watchlist first; expand only after the audits identify gaps.
5. **Eve/Codex:** audit the existing Revenue Signal Lab period, build only the remaining X Router evaluation delta, pre-populate app truth profiles, and close lane-registry gaps while waiting for JT’s Program 0 answers.
6. **All:** complete the three LinkedIn fixtures and two X manual cycles before building content recurrence.
7. **Then:** build only the automation those cycles prove necessary and activate one internal capability at a time.

## 9. Definition of complete

Growth OS is complete when all eight lanes correctly handle their intended state: an eligible evaluated run may produce a bounded decision or a contract-defined truthful `SKIP`; an ineligible event-driven lane remains silent with a freshness receipt and creates no synthetic card. Every actionable decision reaches one Mission Control queue, all external actions remain JT-controlled, outcomes reconcile to domain owners, every active capability has a kill switch/cost/freshness/receipt, and ten consecutive weekdays run without duplicates, lost actions, shadow queues, or unsupported claims.
