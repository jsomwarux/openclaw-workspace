# XHigh Systems Audit — Autoresearch / Self-Improvement Target System

Date: 2026-05-13
Auditor: subagent `xhigh-audit-autoresearch`
Scope: `agents/autoresearch/*`, target registry/checklists/results ledger, recurring Autoresearch cron, enrollment rules in bootstrap docs, recent run history.

## Executive Score

**Before grade:** B+

Why: the system was real and already running successfully: a dedicated M/W/F cron existed, it used an isolated agent with bounded rounds/cost, recent runs produced logs and updated `targets.md` / `results.tsv`, and the core AGENT.md had Karpathy-style baseline/mutation/revert discipline. But it was not honest A-level because:
- Autoresearch cron had no failure-alert configuration, so a failed recurring self-improvement loop could silently stop.
- `runbook` checklist was scoreable to a human but not cleanly machine-detectable because every numbered item began with bold labels before the yes/no question.
- The sweep prompt did not explicitly block/repair invalid checklists/registry paths before scoring.
- The agent docs lacked a hard finality gate for non-empty logs, registry update, TSV row, and training-log line before returning `AUTORESEARCH_OK`.

**After grade:** A-

The main reliability gaps are patched and verified. Remaining reason it is not A+: many pending targets have not been executed yet, and cost cap enforcement is still prompt-level/estimated rather than measured by a deterministic wrapper.

## Inventory

### Cron
- Job: `Autoresearch Sweep`
- ID: `ec9f36d3-3bf8-4bc9-a4b1-06aa886a24ff`
- Schedule: `15 11 * * 1,3,5` America/New_York
- Session: isolated
- Delivery: none
- Model: `openai-codex/gpt-5.5`
- Fallbacks: `anthropic/claude-sonnet-4-6`, `moonshot/kimi-k2.6`
- Timeout: 1800s
- Last run: 2026-05-13, status ok, duration 410,778ms
- Failure alert after patch: Telegram announce to JT after 1 execution error, cooldown 6h, skipped runs excluded

### Registry / Runs
- Registry: `agents/autoresearch/targets.md`
- Active target rows checked: 34
- Recent results ledger rows:
  - 2026-05-12 `mission-control-priority-auditor`: baseline 1.000 → final 1.000
  - 2026-05-13 `opticfy-pipeline`: baseline 0.833 → final 0.944, one kept mutation
- Pending backlog remains large, but the M/W/F recurring cadence is now appropriate for gradual burn-down.

### Checklist Health
- All 34 non-archived target checklists exist.
- All target paths exist or are explicitly cron/payload references.
- All checklists now have 4–6 detectable yes/no questions.
- `runbook` was the only checklist with 0 detectable yes/no questions under a simple parser due to bold-label formatting; patched to six direct yes/no questions.

## Patches Applied

1. `agents/autoresearch/targets.md`
   - Tightened enrollment instructions: checklists must be binary yes/no and numbered `1.`–`6.`.
   - Added explicit path-verification requirement unless path is a cron/payload reference.

2. `agents/autoresearch/AGENT.md`
   - Added vague-checklist guard: if fewer than 4 detectable yes/no questions or scoring is ambiguous, patch obvious checklist issues first or block.
   - Added output finality gate: non-empty inputs/changelog/results, `targets.md`, `results.tsv`, and training-log update must exist before returning OK.
   - Added post-update verification for selected target row and exactly one new TSV row.

3. `agents/autoresearch/weekly-sweep-prompt.md`
   - Added target-selection priority 0 for registry/checklist hygiene that would invalidate scoring.
   - Added final verification step before returning: all log files non-empty, registry updated, TSV row present, training-log line exists.

4. `agents/autoresearch/checklists/runbook.md`
   - Rewrote the six checklist items as direct yes/no questions while preserving the original intent: current names, verified endpoints/paths, real escalation tree, current tool/API/CLI details, correct step order, and failure recovery.

5. Cron config
   - Added failure alerts to `ec9f36d3-3bf8-4bc9-a4b1-06aa886a24ff`:
     - `after: 1`
     - `mode: announce`
     - `channel: telegram`
     - `to: 6608544825`
     - `cooldownMs: 21600000`
     - `includeSkipped: false`

## Validation Results

- Bootstrap budget preflight:
  - `AGENTS.md`: 27,863 bytes (<28,000, near ceiling)
  - `MEMORY.md`: 19,161 bytes (<20,000, near ceiling)
  - `TOOLS.md`: 13,581 bytes (<16,000)
  - `HEARTBEAT.md`: 15,788 bytes (<16,000, near ceiling)
- Cron state inspected with `openclaw cron list --json` and `openclaw cron runs`.
- Cron patch verified with `openclaw cron show ... --json`; returned job includes the intended failureAlert object.
- Registry/checklist/path smoke test passed:
  - 34 active target rows checked
  - 0 missing checklists
  - 0 missing target paths, excluding explicit cron/payload references
  - 0 checklists over 6 questions
  - 0 checklists below 4 detectable yes/no questions after patch
- `results.tsv` shape check passed: every row has 11 tab-separated columns.
- Recent run history confirms the sweep actually completes and logs useful summaries.

## Gate Scores

| Gate | Before | After | Notes |
|---|---:|---:|---|
| Purpose alignment | A | A | Clear self-improvement loop tied to skills/prompts. |
| Target enrollment freshness | A- | A- | Many recent targets enrolled; backlog remains. |
| Checklist quality | B | A- | Runbook parser issue patched; still needs execution reality tests over time. |
| Scoring reliability | B+ | A- | Fixed-input baseline/mutation/revert exists; added invalid-checklist and finality gates. |
| Cost cap | B+ | B+ | $0.50 cap exists in prompt, but no deterministic token/cost kill switch. |
| Failure alerts | C | A | Cron now alerts on first execution failure. |
| No unsafe config mutation | A | A | No auth/model/summary config touched. |
| Bootstrap-size guards | A- | A- | Guards exist; AGENTS/MEMORY/HEARTBEAT near budgets. |
| Output finality | B | A | Explicit final verification added. |
| MC/memory updates | B+ | B+ | Training log required; MC task only for blockers remains acceptable. |
| Repeat-failure promotion | B+ | B+ | Covered via weekly/film rules, but not directly deterministic in autoresearch runner. |

## Remaining Blockers / Exact Follow-up

No urgent blocker. The system is good enough to keep running.

Because this is not honest A+ yet, I created a medium Mission Control task:
- `Autoresearch: add deterministic cost-cap wrapper` (`j57f1aj7t529vsdajsjkkptwvh86m0pe`)

Not A+ yet because:
1. Pending backlog is large; A+ requires several more successful target runs across different skill types.
2. Cost cap is still instruction-level. A deterministic wrapper could read run usage/cost and abort at cap, but that is a larger change than this audit's safe patch scope.
3. Bootstrap files are close to budget, especially `AGENTS.md`, `MEMORY.md`, and `HEARTBEAT.md`; future edits should compact before appending.

Recommended next check after 3 more sweeps: verify at least two more pending targets moved to stable/active with complete logs and no alert noise.
