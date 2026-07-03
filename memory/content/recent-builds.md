# Recent Builds Log

*Updated automatically when builds complete — by overnight agent (Step 5b) and by Eve in-session when JT confirms a build is done.*
*Read by content-generate as the primary source for Wednesday case studies and build-in-public posts.*
*Entries expire after 30 days — remove stale entries during weekly synthesis.*

## Format

```
## [Build Name] — [YYYY-MM-DD]
**What:** [1-sentence description of what was built]
**For:** [client name, or "internal" for Eve/personal builds]
**Outcome:** [metric, result, or capability unlocked — be specific: "$1,000 project", "runs every 14 days", "replaced 18 hrs/week"]
**Demonstrates:** [skill or capability this proves — e.g., "n8n workflow automation", "Agentforce multi-topic routing", "RAG over external catalog"]
**Content angle:** [suggested post angle for Wednesday LinkedIn or build-in-public X — 1 sentence]
**Status:** [complete | in-progress | review-needed]
```

---

<!-- Entries appended below — most recent first -->

## Karen Vitale SoberLife-Coach Website — 2026-07-02
**What:** Finished and verified the live SoberLife-Coach website for Karen Vitale with clear confidential recovery-coaching positioning, executive/public-figure/family audience paths, credential proof, and consultation CTA.
**For:** Karen Vitale client work.
**Outcome:** `https://soberlife-coach.com` redirects to `https://www.soberlife-coach.com/`, returns HTTP 200 on Vercel, and exposes title `SoberLife-Coach | Confidential Recovery Coaching` plus description metadata for confidential recovery coaching.
**Demonstrates:** local-service website delivery, sensitive-service positioning, metadata/launch verification, and client web presence packaging.
**Content angle:** The proof is not "I built a website." It is turning a sensitive solo-professional service into a clear, private, credible web presence that can support referrals and consultations.
**Status:** complete.

## Glow Index Product Analysis SEO/GEO Pass — 2026-06-18
- **What:** Upgraded existing `/rankings/[id]` product analysis pages with explicit `AI skincare analysis` extraction copy, source tag instrumentation, and category internal links.
- **For:** Internal app marketing / Glow Index organic acquisition.
- **Outcome:** Red/green source assertions passed, `npm run lint` exited 0 with two known image warnings, `DATABASE_URL='postgresql://postgres:password@localhost:5432/glowindex' npm run build` passed, final batch commit `3c60c25` was pushed, and production live verification passed after republish with crawler `all_clear=true`, `/rankings` extraction/schema markers, and a live product detail extraction section present.
- **Demonstrates:** GEO product-page optimization, acquisition instrumentation, safe consumer-research positioning, and crawl-gated app marketing execution.
- **Content angle:** Product SEO should start with pages that already match purchase intent before building new content volume.
- **Status:** complete.

## Mission Control Slice 1.7 Health Lane — 2026-06-16
**What:** Promoted Health to a first-class `/health` ops cockpit for failures, cost pressure, stale risk, and recovery work; `/monitor` and `/costs` now redirect to `/health`, with legacy views preserved at `/legacy/monitor` and `/legacy/costs`.
**For:** internal operating system / ops health and reliability
**Outcome:** `bun test lib/mission-control/*.test.ts` passed 44 tests and 132 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed with `/health`, `/monitor`, `/costs`, `/legacy/monitor`, and `/legacy/costs` generated, live HTTP checks returned `/health` 200, `/monitor` 307 to `/health`, `/costs` 307 to `/health`, legacy routes 200, and mobile screenshot `/tmp/mission-control-screens/health-mobile-cockpit.png` showed the ops health cockpit.
**Demonstrates:** ops-health cockpit design, route migration, cost/risk signal grouping, and reliability-focused UX without backend rewrite
**Content angle:** Health is not a placeholder monitor; it should separate failures, cost pressure, stale risk, and recovery work so operators know what needs intervention.
**Status:** complete

## Mission Control Slice 1.6 Evidence Lane — 2026-06-16
**What:** Promoted Evidence to a first-class `/evidence` proof ledger for buyer proof, system receipts, content proof assets, and proof gaps; `/audit` now redirects to `/evidence` and legacy Audit Trail context lives at `/legacy/audit`.
**For:** internal operating system / proof and trust ledger
**Outcome:** `bun test lib/mission-control/*.test.ts` passed 40 tests and 114 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed with `/evidence`, `/audit`, and `/legacy/audit` generated, live HTTP checks returned `/evidence` 200, `/audit` 307 to `/evidence`, `/legacy/audit` 200, and mobile screenshot `/tmp/mission-control-screens/evidence-mobile-ledger.png` showed the proof ledger.
**Demonstrates:** proof-led operating-system UX, route migration, trust-led evidence grouping, and audit-log adaptation without backend rewrite
**Content angle:** A proof lane is useful only when it separates buyer proof, system receipts, content assets, and missing references instead of leaving proof buried in an audit log.
**Status:** complete

## Mission Control Command Attention Brief — 2026-06-16
**What:** Replaced the dead `Since Last Look` block on `/` with a tested Command Brief that surfaces top action, latest proof, urgent JT count, revenue pressure, and risk count from current Mission Control signals.
**For:** internal operating system / JT + Eve daily command surface
**Outcome:** `bun test lib/mission-control/*.test.ts` passed 31 tests and 81 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed, `/` returned 200 with `Command Brief`, and mobile screenshot `/tmp/mission-control-screens/command-mobile-brief.png` was captured.
**Demonstrates:** operating-cockpit UX, tested attention summarization, proof/revenue/risk signal compression
**Content angle:** The homepage of an agent OS should not show stale dashboard filler; it should compress the current decision state into one readable brief.
**Status:** complete

## jtsomwaru.com Phase 3 Site Hygiene - 2026-06-13
**What:** Added blog Consulting/Product categories, dynamic diagram OG images for the three client case studies, Calendly `generate_lead` tracking, a site hygiene verifier, and email-alias handoff notes.
**For:** internal consulting site / JT consulting
**Outcome:** Pushed commit `9a7fad2` to GitHub and Vercel production completed; `npm run lint`, `NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-EGPE6ZNQ56 npm run build`, and the production verifier passed against `https://jtsomwaru.com` with 44 pages, 7 external links, 3 OG images, and 0 failures.
**Demonstrates:** site hygiene, AI-search/social-share metadata, conversion tracking instrumentation, proof-safe launch readiness
**Content angle:** The unsexy launch layer matters: links, categories, OG cards, and conversion events decide whether proof can travel and be measured.
**Status:** complete

## jtsomwaru.com Phase 2 Offer Pages - 2026-06-13
**What:** Added preview-ready COI tracking and rent delinquency automation service pages, sitemap/llms exposure, homepage routing, and a held silent-failure teardown draft.
**For:** internal consulting site / JT consulting
**Outcome:** Pushed commit `9a7fad2` to GitHub and Vercel production completed; production returned HTTP 200 for both new service routes and `/sitemap.xml`, while lint, build, and the production site verifier passed with 0 failures.
**Demonstrates:** consulting offer packaging, AI-search service-page implementation, property-ops workflow positioning, proof-safe human-approval framing
**Content angle:** Sensitive ops automation should sell the exception layer first: what gets held, reviewed, approved, and logged before AI touches the customer.
**Status:** complete

## Plan Review Pack Skill + Human Signal Workflow - 2026-06-06
**What:** Added `plan-review-pack` plus Client OS, AI Context OS, workflow protocol, proof, product, and video-generation wiring so internal agent plans become human-readable review/proof artifacts.
**For:** internal consulting delivery system
**Outcome:** New skill validated, portable `jt-operating-system` plugin updated/validated with cachebuster `0.2.0+codex.20260606170202`, autoresearch checklist/target added, and Mission Control task `j5728192wnpdjqhzg4bcrryj0x884rm6` created to apply it to the Altmark rent delinquency gate.
**Demonstrates:** agent operating-system design, client proof workflow packaging, human-as-signal delivery loops
**Content angle:** The useful version of human-in-the-loop is not approval on every step; it is a review pack that asks for direction, risk, taste, and acceptance at the exact right point.
**Status:** complete

## Crypto Full Analysis Atomic Pipeline - 2026-06-03
**What:** Added `scripts/run-full-analysis-pipeline.py` and X preflight enforcement inside `generate-full-analysis.py` so the crypto cron runs fetch -> X -> guard -> generate -> validate as one deterministic recovery path.
**For:** internal crypto automation
**Outcome:** Fresh pipeline passed with 25 X entries, X age 0.00h at guard time, validator ok=true for 24 coins and 6 held positions, and `checkpoint: CRYPTO_FULL_ANALYSIS_OK`; cron now calls the pipeline before Telegram delivery.
**Demonstrates:** atomic cron design, stale-evidence prevention, validator-gated delivery
**Content angle:** A deterministic writer is not enough if it trusts stale upstream evidence. The freshness gate belongs inside the writer and the pipeline.
**Status:** complete

## Crypto Full Analysis Deterministic Writer - 2026-06-03
**What:** Added a deterministic writer that converts fresh crypto portfolio, prices, X research, and whale inputs into dated analysis, Telegram summary, history, and allocation artifacts.
**For:** internal crypto automation
**Outcome:** June 3 validator passed for 24 coins, 6 held positions, 25 X entries, and `data/allocation-history/2026-06-03.json`; 6AM cron now calls the writer before Telegram delivery.
**Demonstrates:** cron reliability hardening, validator-gated artifact generation, financial-safety boundaries
**Content angle:** Production agents should not ask a model to remember to write every required artifact when deterministic code can guarantee the handoff.
**Status:** complete

## North Star Management Layer — 2026-06-11
- **What:** Built a deterministic scoreboard/pipeline/send-queue layer for JT's $10K/$30K/$100K monthly North Star and wired core review crons to read it.
- **For:** Internal operating system / consulting revenue focus.
- **Outcome:** 13-record pipeline seeded, weighted forecast verified at ~$4,057.50, gap-to-$10K surfaced, four approved CUT crons disabled, enabled cron count reduced to 49, and cron volume guard passed with no warnings.
- **Demonstrates:** Revenue operations design, agent prompt grounding, automation pruning.
- **Content angle:** A good chief-of-staff agent should not just remind you to make money; it should maintain the actual scoreboard and cut work that does not move it.
- **Status:** complete.

## jtsomwaru.com Phase 1 Fable Copy Overhaul — 2026-06-12
- **What:** Rewrote the homepage/project copy layer to align with the Fable audit: human-approved outreach, durable agent proof, non-perishable metrics, standard AI Implementation Consultant title, and intro-call CTA naming.
- **For:** JT consulting site / internal proof hub.
- **Outcome:** Local preview running at `http://localhost:3001`, before/after screenshots captured in `reports/screenshots/2026-06-12-phase1/`, `npm run lint` passed, and `NEXT_DIST_DIR=.next-build npm run build` passed with 51/51 static pages; Vercel preview deploy is blocked by missing credentials.
- **Demonstrates:** Consulting-positioning cleanup, proof-safe copy editing, preview evidence discipline.
- **Content angle:** A consulting site should say what the system actually does, who approves external actions, and what is paid/productized without pretending a draft retainer is live.
- **Status:** preview complete; production deploy held for JT review.

## Mission Control Command Cockpit Slice 1 — 2026-06-16
- **What:** Rebuilt Mission Control's home experience into a 7-lane operating cockpit with a ranked `Needs You Now` queue, revenue cockpit, Eve-handling column, risk/drift column, Work task-router lane, signal adapters, scoring tests, inspection drawer, and state blocks.
- **For:** Internal operating system / JT + Eve daily command surface.
- **Outcome:** `bun test lib/mission-control/score.test.ts lib/mission-control/adapters.test.ts` passed 11/11, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed with `/` and `/work` generated, local HTTP checks returned 200, and Playwright screenshots were captured for desktop/mobile Command and Work.
- **Demonstrates:** productized agent operating-system UX, repo-grounded redesign, tested ranking logic, graceful current-data adaptation without backend rewrite.
- **Content angle:** The useful AI dashboard is not a dashboard; it is a ranked decision queue backed by proof and machine state.
- **Status:** complete.

## Mission Control Slice 1.1 Mobile Shell + Revenue Lane — 2026-06-16
- **What:** Centered and safe-area-hardened the mobile bottom nav, replaced `/consulting` with a live cash-path cockpit over North Star/pipeline/task data, and hardened `/work` with explicit status controls, priority sorting, priority color treatment, and a task inspection/action drawer.
- **For:** Internal operating system / JT revenue focus.
- **Outcome:** `bun test lib/mission-control/*.test.ts` passed 28 tests and 73 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed, `/consulting` returned live values including `$3,375`, `$4,058`, `$368`, `/legacy/consulting` returned the old strategy page, `/work` rendered high-priority tasks first with distinct priority colors, Todo/Doing/Done controls, and drawer actions for status/priority/defer/archive, the task PATCH API was verified with temporary create/update/archive/delete checks, and Playwright screenshots were captured.
- **Demonstrates:** revenue-ops cockpit design, mobile product polish, deterministic local-data parsing, and practical cash-path prioritization without a backend rewrite.
- **Content angle:** A revenue dashboard is only useful when it shows collected cash, weighted forecast, remaining gap, and the exact next revenue actions in one place.
- **Status:** complete.

## Mission Control Slice 1.4 Ship Lane — 2026-06-16
- **What:** Promoted Ship to a first-class `/ship` cockpit for app distribution, content queue, release gates, proof coverage, and blocked/stale shipping work; `/vibe` now redirects to `/ship` and legacy Vibe context lives at `/legacy/vibe`.
- **For:** Internal operating system / app and content shipping focus.
- **Outcome:** `bun test lib/mission-control/*.test.ts` passed 34 tests and 90 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed with `/ship`, `/vibe`, and `/legacy/vibe` generated, live HTTP checks returned `/ship` 200, `/vibe` 307 to `/ship`, `/legacy/vibe` 200, and mobile screenshot `/tmp/mission-control-screens/ship-mobile-cockpit-final.png` showed live Ship counters.
- **Demonstrates:** product-shipping cockpit design, lane promotion without backend rewrite, route preservation, and proof-aware app/content prioritization.
- **Content angle:** A shipping lane is useful only when it separates distribution work, content work, release gates, and proof coverage instead of burying apps inside a generic marketing page.
- **Status:** complete.

## Mission Control Slice 1.5 Machine Lane — 2026-06-16
- **What:** Promoted Machine to a first-class `/machine` cockpit for cron health, agent posture, cost pressure, automation risks, and recent system work; `/agents` now redirects to `/machine` and legacy Agent Team context lives at `/legacy/agents`.
- **For:** Internal operating system / automation reliability.
- **Outcome:** `bun test lib/mission-control/*.test.ts` passed 37 tests and 102 assertions, `bunx tsc --noEmit` passed, `NEXT_DIST_DIR=.next-build bun run build` passed with `/machine`, `/agents`, and `/legacy/agents` generated, live HTTP checks returned `/machine` 200, `/agents` 307 to `/machine`, `/legacy/agents` 200, and mobile screenshot `/tmp/mission-control-screens/machine-mobile-cockpit.png` showed the system-health cockpit.
- **Demonstrates:** machine-status cockpit design, route migration, cron/agent/cost signal modeling, and reliability-focused product UX without a backend rewrite.
- **Content angle:** A machine lane is useful only when it separates cron health, agent state, cost pressure, and automation work instead of burying system risk in an agent directory.
- **Status:** complete.

## Mission Control Done Task Visibility — 2026-06-19
- **What:** Fixed the redesigned `/work` task router so completed tasks no longer stay mixed into active priority filters, added a Done view for recent completions, and exposed History for archived tasks.
- **For:** Internal operating system / JT + Eve task routing.
- **Outcome:** High-priority done tasks no longer remain on the active board; recently completed tasks are visible under Done until the existing seven-day archival path moves them to History; `bun test lib/mission-control/*.test.ts` passed 47/47, `npm run build` passed, `/work` and `/history` returned HTTP 200, and proof guard passed.
- **Demonstrates:** regression-driven product repair, task lifecycle UX, and tested Mission Control routing behavior.
- **Content angle:** Task systems need an explicit completion lane; hiding done work inside active priority sorting destroys trust in the board.
- **Status:** complete.
