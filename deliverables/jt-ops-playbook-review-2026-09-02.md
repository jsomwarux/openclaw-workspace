# Review: JT Ops Playbook v3

**Date:** 2026-09-02  
**Reviewer:** Eve  
**Source:** `media/inbound/openclaw-staged-8a9caa2a-a570-4d18-a1f5-db981b2ae239/input-jt-ops-playbook---d4aaecba-c453-4d00-b011-296e90191cc3.md`

## 1. Objective

Assess whether the playbook's proposed automation portfolio would create unique, reliable, North-Star-relevant value, and identify what Claude Opus should revise before JT considers implementation.

## 2. Executive verdict

The core thesis is right: several canceled automations failed because their outputs lacked strong inputs, consumers, outcome feedback, and shutdown rules, not because the underlying ideas were worthless.

The proposed implementation is not ready. It combines one excellent commercial loop with several frozen or speculative systems, creates a competing source of truth, relies on outdated Claude Routines assumptions, and overstates the trust gained by moving work from Eve to GitHub.

**Best idea:** one demand-to-proof loop: verified operator demand -> proof coverage -> one buyer-ready teardown -> outreach/outcome evidence.

**Wrong idea:** build the entire eleven-part operating system and then retire Eve.

## 3. What to preserve

### A. Preserve as design standards

- Version-controlled routine prompts.
- Schema validation before records enter a corpus.
- Run receipts that distinguish zero-result runs from failed runs.
- A registry that detects pipelines that never ran.
- Source citations, verbatim quote checks, permission states, and anonymized proof.
- A consumer contract for every recurring job: who reads it, what decision changes, proof of consumption, and auto-pause behavior.
- Human approval for buyer-facing artifacts and prompt changes.

These are stronger than the old automation model because they make evidence, consumption, and failure visible.

### B. Pilot only the commercial loop

1. **Demand trigger radar:** monitor a small, verified set of NYC/NJ property operators for operational hiring signals.
2. **Evidence ledger:** map each verified signal to proof JT can actually show.
3. **Teardown generator:** produce one buyer-ready workflow teardown only when a signal survives human review.
4. **Outcome capture:** record whether JT contacted the buyer, reached a priced conversation, or rejected the signal.

This is the only proposed loop with a plausible path to an invoice inside 90 days. It is also explicitly on the current freeze list as a niche research system, so implementation requires JT to say he is overriding that freeze.

## 4. What to integrate instead of rebuild

- **Evidence Ledger:** extend the existing proof log, proof guard, recent-builds, technical-angles, and client-proof process. Do not create a second canonical proof system.
- **Signal Evaluator:** extend `memory/future-signals.md`; the wake-condition pattern already exists.
- **Correction Harvester:** use the existing Mistakes Log, regression checks, feedback log, and Skill Workshop lifecycle. GitHub PR comments are useful additional inputs, not the whole correction stream.
- **Passive board:** the existing Mission Control passive-income surface already owns this state.
- **Morning brief/heartbeat:** improve their consumer contracts and shrink output; do not move all operating context into GitHub.

## 5. What to defer or cut

### Defer

- **Correction-harvester automation:** good corpus idea, but meaningful only after enough real corrections and outcomes accumulate.
- **Prompt tuner:** retain manual experiments and independent verification; do not schedule automatic prompt mutation yet.
- **Knowledge atom lane:** thoughtful safety model, but explicitly frozen and unlikely to produce an invoice this quarter.

### Cut from this playbook

- **Ensemble-core:** extracting a shared abstraction from Glow, Nash, and AgentGuard is a product-engineering project, not an automation optimization. The three systems do not yet prove a stable shared interface, and all related app lanes are frozen.
- **Passive-candidate generator:** it recreates the idea-generation loop that previously produced plausible but unconsumed candidates.
- **Automatic prompt auto-merge:** a one-month clean streak and a five-point gain on a small stochastic golden set are not sufficient safety evidence.
- **Retiring Eve:** reject the premise. A Git commit proves that bytes changed; it does not prove that the committed claims are true. Cloud routines can commit hallucinated, stale, or misclassified records. Eve should orchestrate, reconcile live context, enforce cross-system policy, and route verification while bounded routines perform narrow work.

## 6. Commercial-model corrections

- A job posting proves that a company is willing to hire for work. It does **not** prove that the company will buy an automation service or that the posted salary is an automation budget.
- Operator postings are useful trigger evidence only when paired with a named reachable buyer, a workflow JT has proof for, and a current operational reason to act.
- AI-company Greenhouse/Lever postings can inform career positioning and proof language, but they should not be mixed with property-operator prospect scoring.
- A teardown is not automatically a Workflow Audit deliverable. A paid audit requires client-specific inputs, interviews, systems, exceptions, and acceptance. The generic teardown is a sales asset or hypothesis.

## 7. Technical blockers and contradictions

1. **Network model is outdated.** The playbook says web access must be split into GitHub Actions because Claude cloud routines cannot reach external domains. Current Claude documentation supports Trusted, Custom, Full, and None network modes; Custom can allow named domains and Full permits any domain.
2. **Unsupported GitHub event.** The proof-capture routine requests `push to main`, but current Routines documentation lists pull-request and release events, not push events.
3. **Branch behavior conflicts with direct-to-main instructions.** Claude says routines clone the default branch and create `claude/`-prefixed branches. Several specs instruct routines to push directly to main.
4. **Green status is not task success.** Claude explicitly says a green routine status only means the session started and exited without infrastructure error. It does not prove the requested task succeeded.
5. **Research-preview risk omitted.** Routines are in research preview, have per-account daily run caps, and share subscription usage. Eleven routines are not a stable 30-minute/week system until real quota and failure data prove it.
6. **Schema mismatch.** `workflows_covered` becomes required later but is absent from the original proof schema.
7. **Join mismatch.** One section says machines join proof to demand using `workflows_covered`; another tells `link_proof_to_pains.py` to infer the join from free-text `reusable_pattern`.
8. **Stale routine names.** The playbook replaces `demand-corpus` with `demand-ingest` and `demand-digest`, then later edits and schedules `demand-corpus` again.
9. **Fetch split contradicts itself.** The architecture says fetches run in Actions, while `demand-ingest` still calls `harvest_postings.py` inside the routine. The atom lane makes the same mistake with `queue_sources.py`.
10. **Single-source-of-truth claim is false.** Money remains in Convex, tasks in Mission Control, client drafts in Drive, operational memory in OpenClaw, and code in project repos. `jt-ops` would be another store. It should be an append-only evidence exchange or reporting mart, not the canonical home for everything.

## 8. Recommended pilot design

Run one six-week pilot only after an explicit freeze override.

- **Universe:** 25 verified NYC/NJ property operators, not 60 ATS companies plus 60 operators.
- **Cadence:** weekly collection and digest, not daily model extraction.
- **Output:** maximum three candidates per week.
- **Hard gates:** named buyer, reachable channel, live workflow signal, matching proof asset, source freshness.
- **Human decision:** JT marks contact / reject / defer.
- **Success criteria by week six:** at least three qualified signals contacted, one priced conversation, zero fabricated quotes, zero client-permission leaks, and under 30 minutes weekly review.
- **Kill criterion:** no priced conversation or buyer-confirmed pain after six weeks; pause the system and preserve the evidence.
- **No automatic skills, app builds, prompt merges, or Eve decommissioning.**

## 9. Exact feedback to send Claude Opus

> Rework this from a full operating-system migration into a six-week demand-to-proof pilot. Preserve the run receipts, pipeline registry, schemas, versioned prompts, permission controls, independent verification, and consumer-contract rule. Limit execution to a small operator demand feed, proof matching, one buyer-ready teardown, and outcome capture. Remove ensemble-core, passive-candidate generation, the knowledge lane, automatic prompt merging, and Eve retirement from the implementation plan. Integrate with existing OpenClaw proof, future-signal, correction, Mission Control, and briefing owner surfaces instead of creating a second canonical system. Correct the Claude Routines assumptions using current official docs: custom/full network access exists; supported GitHub triggers are PR and release events; routine green status is not task success; routines use Claude-prefixed branches and have daily run/subscription limits. Resolve the `workflows_covered` schema/join conflict, the stale `demand-corpus` references, and the Actions-vs-routine fetch contradiction. Define pilot success as buyer action and priced conversations, not corpus size, records written, or reports generated.

## 10. Acceptance criteria before implementation

- One owner surface per fact is named.
- Every pipeline has a consumer, decision, consumption artifact, and auto-pause rule.
- Every routine is validated against current platform capabilities.
- Every direct write, push, cron creation, and decommission action has JT approval.
- Commercial success is measured by contacted qualified signals and priced conversations.
- Existing client delivery and warm-list work cannot be displaced.

## 11. Proof assets reviewed

- Full 2,022-line playbook received 2026-09-02.
- Existing automation inventory: `memory/automation-inventory-2026-08-12.md`.
- Current North Star mandate: `memory/operating-mandates/90-day-playbook-2026-08-19.md`.
- Current Claude Routines documentation: <https://code.claude.com/docs/en/routines>.
- Current Claude cloud environment documentation: <https://code.claude.com/docs/en/cloud-environments>.

## 12. Next action and owner

**Owner:** JT  
**Next action:** Send the feedback in section 9 to Claude Opus and request a revised pilot-only v4. No implementation is authorized by this review.
