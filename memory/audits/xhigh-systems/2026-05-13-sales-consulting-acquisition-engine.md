# XHigh Systems Audit — Sales / Consulting Acquisition Engine

Date: 2026-05-13
System: JT Somwaru Consulting acquisition engine
Scope: consulting pipeline skill, pipeline tracker, client folders, shortlists, outreach scripts, email pivot flow, North Star sales/proof files, Mission Control acquisition tasks, relevant crons.

## Before Grade

**B.**

The engine had the right raw ingredients but was still too noisy and too cold-outreach-weighted:

- Strong current wedges existed: Altmark → family-office referrals, Property / Family-Office AI Ops Diagnostic, Guyana warm-intro validation, wholesale pilot, Marketsmith warm path.
- Pipeline guardrails were present: research before outreach, buyer-channel gate, tier routing, T3 no individual Drive folder, JT review default.
- Cold outreach backlog was structurally large and competed with warmer/proof-led channels.
- Stale M2 email pivots existed locally but were not fully visible in MC before repair.
- Proof assets existed, especially the property insurance expiration teardown, but the acquisition engine had not made that the obvious next sales asset.
- Mission Control contained stale generic Review + Send clutter that made “what should JT do next?” less obvious.

## After Grade

**A-.**

The acquisition engine is coherent again: warm/proof-led path first, cold outreach recovery second, and stale review/send clutter reduced. It is not A+ until one proof-led or warm path creates a real external outcome: Altmark acceptance/proof, a Yair/referral ask, first diagnostic conversation, 2+ qualified Guyana intros, or the AI Ops Teardown posted with CTA.

## Inventory Findings

### Core system inspected

- `skills/jt-consulting-pipeline/SKILL.md`
- `~/projects/jt-consulting-pipeline/pipeline.md`
- `~/projects/jt-consulting-pipeline/drive-canonical-names.md`
- `~/projects/jt-consulting-pipeline/EMAIL-PIVOT-RULES.md`
- `~/projects/jt-consulting-pipeline/shortlists/*.md`
- `~/projects/jt-consulting-pipeline/clients/*/{research.md,outreach-draft.md,email-draft.md,brief.json}`
- `scripts/outreach_update.py`
- `scripts/outreach_email_pivot.py`
- `scripts/pipeline_drive_sync.py`
- `memory/north-star/consulting-sales-engine.md`
- `memory/north-star/proof-distribution-engine.md`
- `memory/consulting/property-family-office-ai-ops-offer-2026-05-13.md`
- `memory/consulting/ai-ops-teardowns/2026-05-10-property-insurance-expiration.md`
- `memory/content/bank/2026-05-10/ai-ops-teardown-property-insurance-expiration.md`
- `memory/research/guyana/local-content-ops-validation-sprint-2026-05-13.md`
- `memory/research/guyana/local-content-ops-capability-brief-2026-05-13.md`
- `memory/research/guyana/guyana-intro-ask-scripts-2026-05-13.md`
- Mission Control `/api/tasks`
- Cron jobs: `outreach-pipeline`, `outreach-email-pivot-daily`, `prospect-discovery`, `AI Ops Teardown Weekly Draft`, Altmark follow-up check.

### Current wedges

1. **Altmark / family-office referrals** — strongest near-term warm path, but gated by PC handoff, acceptance/payment clarity, and redacted proof capture.
2. **Property / Family-Office AI Ops Diagnostic** — best packaged offer; lead with exception visibility, audit trail, human approval, and existing-system fit.
3. **Property insurance expiration AI Ops Teardown** — best proof-led distribution asset because it maps directly to Altmark/family-office pain without exposing client details.
4. **Guyana Local Content Ops** — valid only as 10-conversation warm-intro validation. Do not build the demo or broad prospect list until intros confirm pain.
5. **Cold outreach / email pivots** — useful as low-priority recovery, not the main acquisition lane.

### Mission Control snapshot after patches

- Active tasks: **225**
- Active Consulting tasks: **80**
- Consulting priorities: **9 high / 36 medium / 35 low**
- Consulting assignees: **57 JT / 23 Eve**
- Active generic `Review + Send:` tasks: **0**
- Active `Email Pivot:` tasks: **8**
- Email Pivot tasks now include `slug` and `pipelineStage=email-pivot`.

## Score Gates

| Gate | Before | After | Notes |
|---|---:|---:|---|
| ICP / wedge clarity | B+ | A | Current top lane is property/family-office ops, with Altmark proof gate and Guyana as validation-only. |
| Outreach volume / quality | C+ | B+ | Cold backlog still exists but no longer outranks warm/proof-led work. |
| Warm-intro priority | B | A- | Altmark/Yair and Guyana family-network tasks are now clearly above generic cold sends. |
| Proof gate | B- | A- | Proof engine now points at insurance-expiration teardown + Altmark acceptance gate. |
| Pipeline stages / guardrails | A- | A- | Existing skill is strong: research, buyer channel, tier routing, Drive rules, JT review. |
| Drive sync | B+ | A- | Email pivots reused/uploaded Drive docs; canonical names used. |
| MC review/send tasks | C | A- | 16 stale generic review/send tasks archived; 8 missing email pivot tasks created/reused. |
| Follow-up cadence | B- | A- | Email pivot script now detects existing drafts and missing tasks without overwriting copy. |
| Stale task cleanup | C | A- | Generic review/send clutter removed, audit tasks closed. |
| Duplicate M-status prevention | B | A- | Cron prompt and pivot script dedup are stronger; no active generic Review + Send remains. |
| Generic AI consultant risk | B | A | Updated North Star files force exception-visibility/property-family-office framing. |

## Patches Applied

### Files changed

1. `scripts/outreach_email_pivot.py`
   - Preserves existing `email-draft.md` during repair/backfill runs instead of overwriting JT-reviewed drafts.
   - Creates missing Email Pivot MC tasks when a draft exists but no active task exists.
   - Improves active-task dedup with normalized title matching, including FCM/First Class variants.
   - Makes generated Email Pivot tasks **low priority**, not high-priority cold-outreach clutter.
   - Adds structured task contract: first action, why it matters, done state.
   - Adds `slug` and `pipelineStage: email-pivot` to new tasks.

2. `memory/north-star/consulting-sales-engine.md`
   - Added 2026-05-13 acquisition engine update.
   - Set priority order: Altmark proof/referrals → Property/Family Office Diagnostic → proof-led distribution → Guyana validation → low-priority cold recovery.
   - Added A+ gate.

3. `memory/north-star/proof-distribution-engine.md`
   - Added acquisition update making property insurance expiration teardown the top proof-led sales asset.
   - Added guardrail against unverified Altmark claims.

4. Cron job metadata: `outreach-pipeline`
   - Revalidated payload uses `openai-codex/gpt-5.5`, `thinking=high`, `timeoutSeconds=1800`, no routine delivery, failure alerts enabled.
   - Description updated to reflect the 2026-05-13 audit: proof/warm-intro path first, cold Review+Send creation low-priority and M-status-deduped.

### Mission Control tasks changed

- **Created/reused 8 Email Pivot tasks:**
  - Conner Strong & Buckelew — Jim
  - R.E.M. Residential — Zachary
  - Lawley Insurance — Chris
  - ProRealty USA — David
  - First Class Management — Albert
  - Atlas NYC Property Management — Eric
  - Globe Electric — Joseph
  - Premier HVAC Services — Boris

- **Patched 8 Email Pivot tasks** with `slug` + `pipelineStage=email-pivot`.
- **Archived 16 stale generic Review + Send tasks** that competed with the current warm/proof-led path. No outreach was fabricated or marked sent.
- **Closed 2 audit tasks** now completed by this sweep:
  - `Run first Consulting Sales Engine audit`
  - `Run first Proof + Distribution audit`

## Validation

Commands run:

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 -m py_compile scripts/outreach_email_pivot.py scripts/outreach_update.py scripts/pipeline_drive_sync.py scripts/mission_control_north_star_audit.py
python3 scripts/outreach_email_pivot.py --min-days 7
python3 scripts/mission_control_north_star_audit.py --dry-run
curl -s http://localhost:3000/api/tasks
openclaw cron list --json
openclaw cron show 651fa1da-84d7-44b3-8e10-6a46e1c05cf6 --json
```

Results:

- Bootstrap sizes at start: AGENTS 27,013; MEMORY 19,019; TOOLS 13,947; HEARTBEAT 14,330. Bootstrap sizes at validation after existing session drift: AGENTS 27,013; MEMORY 19,019; TOOLS 13,947; HEARTBEAT 15,014.
- Python compile passed for all checked scripts.
- Email pivot final scan: 8 prospects detected, all had existing draft + active Email Pivot MC task, so **no duplicate pivots created**.
- MC final check: 225 active tasks, 80 active Consulting tasks, 0 active generic `Review + Send:` tasks, 8 active `Email Pivot:` tasks.
- Outreach cron final payload: `model=openai-codex/gpt-5.5`, `thinking=high`, `timeoutSeconds=1800`, no routine delivery, failure alert enabled.
- Mission Control dry-run reported `errors=0`; it still wants 9 priority/description changes and flags 6 uncontrolled high tasks globally, which is outside this sales-engine scope and belongs to the broader MC hygiene pass.

## Remaining Blockers

1. **A+ outcome gate not cleared yet.** Need one real proof/warm-path external outcome.
2. **Altmark proof gate is the highest-leverage blocker.** PC handoff, acceptance/payment clarity, and redacted screenshots must happen before referral ask.
3. **Property / Family-Office one-pager still needs final call-ready packaging.** Existing offer copy is strong, but MC task remains open.
4. **Guyana is still validation-only.** Warm intros must come before demo/prospect buildout.
5. **Cold recovery tasks are visible but low priority.** Several email pivots have unverified or missing email addresses; JT should only use them if he deliberately chooses cold recovery after warm/proof actions.

## Recommended Next Action

Do **not** start another cold batch first.

Next best move:

1. Finish Altmark handoff/proof/payment clarity.
2. Review/post the property insurance expiration LinkedIn teardown.
3. Package the Property / Family-Office AI Ops Diagnostic one-pager.
4. Then ask Yair for 2–3 family-office intros once the Altmark gate is clean.

## Report Path

`/Users/jtsomwaru/.openclaw/workspace/memory/audits/xhigh-systems/2026-05-13-sales-consulting-acquisition-engine.md`
