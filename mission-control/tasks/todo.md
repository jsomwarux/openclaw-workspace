# Mission Control Redesign Slice 1

## Goal
Ship the first useful cockpit slice in the existing Mission Control app without a backend rewrite.

## Plan
- [x] Read project rules and current Mission Control docs.
- [x] Audit existing routes, components, task schema, and API shapes.
- [x] Add score/signal model tests first.
- [x] Implement client-side signal normalization and ranking.
- [x] Replace the 16-tab sidebar with the 7-lane navigation model while keeping old routes reachable.
- [x] Build the Command cockpit over existing task/cron/proof/agent/cost data.
- [x] Build the Work lane over existing task data with inspection drawer support.
- [x] Add empty/loading/error/stale states for the new surfaces.
- [x] Run focused tests, type/build checks, and browser verification.

## Deferred
- `/api/signals` backend aggregation.
- Persisted multi-device `lastSeenAt`.
- Full proof-ref resolver.
- Saved filters.
- Systems/Skills redesign.
- Deep Ship/Machine/Evidence/Health lane implementations beyond safe redirects and shell alignment.

# Mission Control Slice 1.1 Mobile Shell + Revenue Lane

## Goal
Make the mobile cockpit feel intentional on phone screens, then replace the old Revenue/Consulting page with a North Star cash-path lane over existing local data.

## Plan
- [x] Add tested mobile shell/nav layout constants so bottom navigation stays centered and phone-safe.
- [x] Patch the mobile top/bottom shell and Work lane spacing for current iPhone/Safari constraints.
- [x] Verify the mobile `/work` screenshot after the nav fix.
- [x] Audit existing local revenue/job/consulting data sources that can power Slice 1.1 without schema rewrites.
- [x] Add tested revenue-signal adapters over current task/proof/local-data shapes.
- [x] Replace `/consulting` with a Revenue cockpit focused on collected/contracted/pipeline/job/app upside.
- [x] Run tests, typecheck, isolated build, route HTTP checks, and mobile screenshots.
- [x] Add explicit Todo/Doing/Done task controls to `/work` so mobile users can move tasks without discovering the old tiny status-dot behavior.
- [x] Sort Work tasks by priority before recency and add visible high/medium/low color treatment.
- [x] Add a Work task inspection/action drawer with context, evidence, ranking explanation, status controls, priority controls, defer, and archive actions.

# Mission Control Slice 1.3 Command Attention Brief

## Goal
Make the Command cockpit explain what changed and what matters now, using existing task/proof/revenue signals without backend/schema rewrites.

## Plan
- [x] Add failing tests for Command attention brief summary logic.
- [x] Implement a small Command brief model over current signals and queue data.
- [x] Wire the homepage to show top priority, latest proof, stale/risk count, and money-path pressure.
- [x] Verify tests, typecheck, isolated build, live HTTP, and mobile screenshot.
- [x] Update implementation notes, memory/proof surfaces, and the JT review task.

# Mission Control Slice 1.4 Ship Lane

## Goal
Turn Ship from a legacy Vibe/Passive Income alias into a first-class operating lane for app distribution, content shipping, release gates, and proof coverage.

## Plan
- [x] Add failing tests for Ship summary/grouping behavior and `/ship` route promotion.
- [x] Implement a small Ship model over current Mission Control signals.
- [x] Make `/ship` the primary Ship lane, redirect `/vibe` to `/ship`, and preserve a legacy Vibe reference under `/legacy/vibe`.
- [x] Build the Ship cockpit with app distribution, content queue, release gates, proof coverage, and blocker/stale counters.
- [x] Verify focused tests, full Mission Control tests, TypeScript, isolated build, live HTTP routes, and mobile screenshot.
- [x] Update implementation notes, memory/proof surfaces, and the JT review task.

# Mission Control Slice 1.5 Machine Lane

## Goal
Turn Machine from an Agent Team alias into a first-class system-health lane for cron health, agent posture, cost pressure, and machine risks using existing APIs and signal adapters.

## Plan
- [x] Add failing tests for Machine summary/grouping behavior and `/machine` route promotion.
- [x] Implement a small Machine model over current cron, agent, cost, and machine-risk signals.
- [x] Make `/machine` the primary Machine lane, redirect `/agents` to `/machine`, and preserve the legacy Agent Team page under `/legacy/agents`.
- [x] Build the Machine cockpit with cron health, active agents, cost posture, automation risks, and recent machine work.
- [x] Verify focused tests, full Mission Control tests, TypeScript, isolated build, live HTTP routes, and mobile screenshot.
- [x] Update implementation notes, memory/proof surfaces, and the JT review task.

# Mission Control Slice 1.6 Evidence Lane

## Goal
Turn Evidence from the old Audit Trail page into a first-class proof/trust ledger over current proof signals and proof logs, while preserving the old audit list under legacy routing.

## Plan
- [x] Add failing tests for Evidence summary/grouping behavior and `/evidence` route promotion.
- [x] Implement a small Evidence model over current proof signals.
- [x] Make `/evidence` the primary Evidence lane, redirect `/audit` to `/evidence`, and preserve the old Audit Trail page under `/legacy/audit`.
- [x] Build the Evidence cockpit with proof coverage, latest proof, proof gaps, buyer/client proof, system proof, and content/proof assets.
- [x] Verify focused tests, full Mission Control tests, TypeScript, isolated build, live HTTP routes, and mobile screenshot.
- [x] Update implementation notes, memory/proof surfaces, and the JT review task.

# Mission Control Slice 1.7 Health Lane

## Goal
Turn Health from the old Monitor/Costs placeholders into a first-class ops health lane for failures, cost pressure, stale risk, and recovery work using existing Mission Control signals and cost data.

## Plan
- [x] Add failing tests for Health summary/grouping behavior and `/health` route promotion.
- [x] Implement a small Health model over current health, machine, risk, and cost signals.
- [x] Make `/health` the primary Health lane, redirect `/monitor` and `/costs` to `/health`, and preserve old views under `/legacy/monitor` and `/legacy/costs`.
- [x] Build the Health cockpit with ops failures, cost pressure, stale risk, and recovery work.
- [x] Verify focused tests, full Mission Control tests, TypeScript, isolated build, live HTTP routes, and mobile screenshot.
- [x] Update implementation notes, memory/proof surfaces, and the JT review task.
