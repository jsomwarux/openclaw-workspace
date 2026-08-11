# Claude <> Eve Sync Prompt - 2026-08-10

Use this as the full prompt to Claude. Attach this file too if the Claude chat supports attachments.

## Prompt To Paste Into Claude

You are Claude, acting as JT Somwaru's parallel AI operator. I need you synced with Eve/OpenClaw's current understanding of my operating state as of Monday, August 10, 2026.

Read the attached context as the source-of-truth sync packet. Your job is not to rewrite it generically. Your job is to compare it against your own memory of me and identify:

1. Anything Eve/OpenClaw appears to have wrong or stale.
2. Anything you know that is missing from Eve's summary.
3. Any conflicts between your memory and Eve's memory.
4. The single canonical version of the truth you recommend we use going forward.
5. Any updates I should send back to Eve so both systems stay aligned.

Rules:
- Treat this Aug 10 sync correction as superseding stale July 16 items where it conflicts.
- Do not infer client payments, project status, outreach sent, or app state without evidence.
- Every collected dollar figure must cite the Mission Control payments ledger. `memory/pipeline.jsonl` is forecast/routing only.
- Separate facts from recommendations.
- For uncertain items, say "uncertain" and name the missing evidence.
- Do not optimize for encouragement. Optimize for operational accuracy.
- Keep external sends, client outreach, money movement, deploys, and public posting as JT-only actions unless I explicitly say otherwise.
- Remember my priority stack: consulting cash/proof first, Altmark + MSI delivery first, then referral asks and Run Control packaging, with apps capped/benched unless a hard trigger fires.

Output format:

## Sync Verdict
- Fully synced / mostly synced / materially out of sync
- One-sentence reason

## Conflicts Or Stale Items
List each discrepancy as:
- Topic:
- Eve says:
- Claude memory says:
- Recommended canonical truth:
- Evidence or missing evidence:

## Missing Context Eve Should Add
Only include items that materially affect decisions, priority, client state, money, project status, or positioning.

## Current Priority Stack
Give the ranked top 5 workstreams you believe JT should be operating from right now.

## Send Back To Eve
Write a concise bullet list I can paste back to Eve to update her memory.

## Context Packet From Eve/OpenClaw

### Operating Identity / Positioning
- JT Somwaru is positioning as a practical AI Implementation Specialist / AI Workflow Architect for ops-heavy SMBs.
- The credibility edge is business operations plus systems implementation plus AI workflows, not developer-for-hire positioning.
- Best language: messy handoffs, source data, approval boundaries, review queues, audit trails, delivery proof, adoption/value metrics, and measurable outcomes.
- North star: consulting cash and proof first. The real metric is earned consulting cash collected, excluding unemployment, paper equity, app vanity metrics, and crypto gains.
- Approximate income thresholds: safe around $10K/month, free around $30K/month, rich around $100K/month.
- Hard personal constraints: protect sleep, health, NYC/location stability; no relocation; no developer-only path.

### Active Priority Stack
1. Altmark delivery + Altmark FTE/NewCo negotiation
2. MSI / Marketsmith delivery
3. Maiky live-on-hold revenue path
4. Gil referral ask + Run Control / AI Enablement OS packaging
5. Karen reset, Guyana capped exploration, Ron/BDT watch-only, apps below caps

### Payments Ledger Rule
- Collected-cash source of record: Mission Control payments ledger (`mission-control/convex/payments.ts` seed and `/api/payments`).
- Ledger-confirmed collected payments as of Aug 10:
  - Altmark foundation infrastructure: $4,000, source says date not logged/month inferred.
  - Altmark COI expiration tracking: $2,250, source says date not logged/month inferred.
  - Altmark rent delinquency 50%: $2,250, source says date not logged/month inferred.
  - Aya dashboard: $1,500, source says date not logged/month inferred.
  - Aya dashboard updates: $1,000, confirmed by JT 2026-07-28.
  - SoberLife Phase 1: $3,000, confirmed by JT 2026-07-28.
  - MSI kickoff 50%: $5,400, confirmed by JT 2026-07-28.
- Any proposal, remaining balance, salary/equity position, or pipeline amount below is UNVERIFIED by payments ledger unless explicitly described as ledger-confirmed collected cash.

### Altmark Delivery
- Altmark is the top paid/proof lane.
- Prior proposal total $34,750 is UNVERIFIED by payments ledger; treat as proposal context, not collected cash.
- Rent delinquency workflow status: 33 nodes, 91 passing tests, deactivated.
- Precise remaining gates:
  1. Yair clears AppFolio ledgers.
  2. billing@ credential re-point.
  3. Threshold column decision.
  4. Holiday dates.
  5. Attorney sign-off.
  6. Canary send approval.
  7. JT-owned blocker: add `outreach_id` as the 16th column header on the Outreach Log tab before next test run.
- Rent delinquency remaining balance $2,250 is UNVERIFIED by payments ledger because it is forecast/contract balance, not collected cash.
- Yair referral ask waits until delinquency is accepted in writing and an anonymized summary is clean. Payment and favor never go in the same message.

### Altmark FTE + NewCo Negotiation
- Split this from Ron/BDT.
- This is active negotiation with Yair and Adai, Yair's older brother, not a watch item.
- Aug 6 proposal is a full-time Altmark role plus partnership in a separate real-estate automation business.
- JT's stated negotiation positions are UNVERIFIED by payments ledger because they are comp/equity terms, not collected cash:
  - Salary anchor $185K.
  - Target $165K-$175K scaled to exclusivity.
  - Package floor only; no standalone salary floor.
  - Equity open 55%, target 50%, floor 45% with vetoes.
- Employment and NewCo must be separate contracts.
- NewCo formation plus IP terms must be signed before or with day one.
- JT's existing systems, toolkit, and playbook stay JT's personal IP. Non-negotiable.

### Ron / BDT Diamond District
- Separate from Altmark FTE/NewCo.
- Watch-only.
- Ron has not been briefed on the real-estate developments.

### DHCR
- DHCR proposal went to Matt, not Yair.
- Route DHCR as a delivery-track item.
- Do not chase the deposit inside the Altmark FTE/NewCo compensation negotiation thread.
- Any DHCR proposal/deposit figures are UNVERIFIED by payments ledger unless later recorded as collected.

### MSI / Marketsmith
- MSI / Marketsmith is signed and active delivery.
- Signed value: $10,800 fixed-scope Nexus engagement. UNVERIFIED by payments ledger as total signed value; only kickoff is ledger-confirmed collected cash.
- Scope: 80-hour cap.
- Payment terms: 50% kickoff / 50% completion.
- Kickoff $5,400 is ledger-confirmed collected cash, confirmed by JT 2026-07-28.
- MSI should not appear in sends-due anymore.
- Remaining $5,400 is UNVERIFIED by payments ledger and is completion/acceptance invoice only.
- MSI displacement rule is in effect: it owns serious delivery capacity alongside Altmark.
- Governed AI Ops methodology kit trigger fired because of MSI. Build generic-first. MSI-specific configs/deliverables stay MSI-owned and must not enter reusable IP.

### Karen / SoberLife
- Paid and closed-won, but not referral-eligible yet.
- Ledger-confirmed collected: SoberLife Phase 1 $3,000, confirmed by JT 2026-07-28.
- Referral ask is gated on written expectation reset because Karen expects top-3 for "sober life coach".
- Open handoff items: design files, documented credentials, final paid invoice, Google Business Profile.

### Gil / Aya Construction
- Gil equals the construction dashboard client/lane.
- Ledger-confirmed collected: Aya dashboard $1,500, date not logged/month inferred; Aya dashboard updates $1,000, confirmed by JT 2026-07-28.
- Gil referral ask is eligible.

### Maiky
- Maiky is separate from Gil/Aya construction dashboard.
- Live opportunity, on hold after cost review.
- $5,000 proposal is UNVERIFIED by payments ledger and is forecast/proposal context: 6 sheet automations plus 1 weekly delinquency report, 50/50.
- Unbundled entry point is UNVERIFIED by payments ledger: $2,000 delinquency report plus $500 per automation.
- Not dead. Closest live revenue after Altmark and MSI.
- StreetEasy $75/month retainer no longer exists.

### Run Control / AI Enablement OS
- Strongest reusable IP lane.
- Packages intake, source-of-truth data, approved tools/actions, reviewer queue, audit trail, delivery proof, adoption/value metric, and stop/scale decisions.
- Current market/job signals validate this as the sales asset.
- Should become external sales/proof packaging, not just internal methodology.

### Apps / Products
- jtsomwaru.com: live. Current positioning is broader AI operations implementation for ops-heavy teams, with `/property` as focused property-management workflow audit path. Site is not the bottleneck unless explicitly reopened.
- Glow Index: maintain only. 2 hr/week cap, Sept 1 data gate. Built/deployed to Replit. Growth/data/analysis activation gated. Replit rule: fresh build required before redeploy; simple redeploy reuses old build.
- Nash Satoshi: capped. 1 merged hour/week, one human-reviewed receipt. Private repo. Crypto ranking/content can support reputation but does not outrank consulting cash.
- Vista: killed/held for 90 days under July canonical state despite older memory saying App Store/live. No maintenance or quick checks unless explicitly reactivated.
- Action Arena: re-gate Aug 15. Apple org conversion is blocker. If unresolved, wait for next season. 10 hr/week cap if reopened.
- Watchdog: benched into August as a structured experiment, but no jobs/copy/outbound should run without explicit activation. It is the productized COI/compliance lane.
- Outbound v2: benched into August, dependent on proof/deliverability. Send-ready requires named buyer plus reachable channel; email OR accepted LinkedIn is enough. No custom builds pre-reply.
- Market Bubble, Injury Edge, DynastyPulse, permit engine: killed/held 90 days per canonical July state.
- Guyana: not killed. Capped exploration. Named 2nd-degree prospect Paul James, The SaPaJ Group, Georgetown; mutual connection Rosh; intro drafts written. One warm intro in flight, ranked below the top four.
- H.C. Oswald: holding until personal website is polished enough plus demo agents are built. Not active.

### Job Market
- Consulting-first.
- Only exceptional AI Solutions Architect / AI Implementation Lead / AI Enablement roles around $150K+ NYC/remote should get attention.
- Avoid Apex/SFDX-heavy dev, pure ML/research, relocation, low comp.
- Latest job-market state is mostly positioning intel, not fresh application priority.
- Best proof language: Run Control / AI Enablement OS, governed operating assets, release/eval/rollback discipline, adoption leadership, documentation, and value reporting.

### Content
- Useful only when proof-led.
- Voice rule: first-person proof beats generic AI advice.
- Current high-value angles: Run Control, source/export gates, approval boundaries, and business-side AI operating systems.
- No auto-posting without JT's explicit approval.

### Crypto / Finance
- Crypto is research/ranking/threshold-awareness only.
- No trades, transfers, swaps, spend, wallet, payment-MCP, or x402 experiments without JT approval.
- Crypto recurring analysis jobs are currently disabled/refused.

### Health
- All automated health crons canceled Aug 7, 2026 at JT's request.
- Manual protocol tools remain available.
- Mission Control still has a high-priority "Start 14-day health protocol + book prescriber" task, but automation is off.

### Mission Control / Infrastructure
- Mission Control is up as of Aug 10.
- Do not quote 251 active tasks / 13 high / 0 overdue as health without triage.
- Aug 10 quick API check: 251 active tasks and 231 active tasks idle more than 30 days. "0 overdue" is likely due-date sparsity, not actual cleanliness.
- Run Mission Control triage before using task count as an operating signal.
- Crons/cost: 12 enabled crons, 0 unhealthy, costs clean as of the Aug 10 heartbeat.
- Costs clean.
- Spanish paused.
- Known issue: duplicate lossless-claw metadata warning persists.
- Eve's semantic memory search is currently down because the OpenAI embedding auth token expired; Eve read source files directly for this sync.
- AGENTS.md is near budget: 27,806 / 28,000, so next append requires trimming first.

### Biggest Sync Warning
- Treat the July 16 canonical file as source of truth when older memory conflicts.
- Older files still contain stale things like "Aya active," old app priorities, old crypto/job automation, and older model/setup notes.
- Live strategy is consulting cash/proof first, Altmark + MSI, then referral/Run Control packaging.
- Everything else is capped, benched, killed, or watch-only unless a hard trigger fires.
