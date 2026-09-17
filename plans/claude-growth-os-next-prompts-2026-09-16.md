# AI Workflow Growth OS — Claude Controller Runbook

Date: 2026-09-16  
Host: **Mac Mini only** (`/Users/jtsomwaru`)  
Concurrency: maximum **two** Claude Code sessions at once

## Execution order

```text
WAVE 1 — run in parallel now
  A. Suppression review / repair / PR
  B. n8n blueprint preflight / version-ceiling audit / PR

WAVE 2 — after A is merged into jt-ops main; run in parallel
  C. Mission Control suppression reconciliation / PR
  D. COI proof-asset evidence pack (human decision only)

WAVE 2B — after JT approves the proof sentence
  E. Canonical proof-asset card / PR

WAVE 3 — after C is deployed inactive and E is merged
  F. Final n8n blueprint reconciliation / PR

WAVE 4 — after F is merged
  G. n8n workflow implementation / PR

EVE ONLY
  Merge/deploy reviewed PRs, protected runtime configuration, final synthetic no-send proof.
```

Never run two Claude sessions against the same repository at the same time. Do not start a later wave because a builder says it is done; start it only when the prerequisite branch is merged/deployed as stated.

---

## Prompt A — suppression lane controller

Start Claude Code in:

`/Users/jtsomwaru/.openclaw/workspace/.worktrees/jt-ops-suppression-owner`

Paste:

```text
You are the autonomous controller for the suppression-owner lane of JT Somwaru's AI Workflow Growth OS. Work only on this Mac Mini.

Repository/worktree:
- /Users/jtsomwaru/.openclaw/workspace/.worktrees/jt-ops-suppression-owner
- branch: eve/suppression-owner-adapters
- required starting head: ea8673ffb4a2b23d656a7baf4c92e27933bb5bb5
- upstream base: origin/main

Read completely before acting:
- CLAUDE.md
- tasks/todo.md
- tasks/lessons.md
- every suppression design/plan referenced by the branch
- git diff origin/main...HEAD

Authorized:
- inspect, test, edit, commit;
- create fresh temporary clones/worktrees;
- run a fresh non-builder security review;
- repair reproduced failures test-first, maximum two repair/review cycles;
- push the exact confirmed feature branch;
- open or update one PR against main;
- wait for all remote CI checks;
- write the durable handoff and send one OpenClaw internal event.

Not authorized:
- merge;
- deploy or activate;
- create/rotate/read credentials;
- add/enable schedules;
- send anything externally;
- edit unrelated files.

Protocol:
1. Verify exact branch, exact starting head, and clean worktree. If any differ, write BLOCKED handoff and stop.
2. From a fresh isolated context and clean clone, attack:
   - raw channel leakage into durable artifacts;
   - candidate/draft/report/Git-binding substitution;
   - Mission Control vs consulting-owner disagreement;
   - terminal precedence for reply_received, opt_out, hard_bounce;
   - valid later-clear semantics for sent/manual_hold;
   - changed channel or later observation;
   - stale/future/malformed/non-UTC timestamps;
   - receipt copy/replay/mutation/wrong candidate/wrong draft;
   - uncapped responses, timeout inconsistency, redirects, ambient proxies, credential forwarding, capability leakage;
   - malformed JSON/types and traceback leakage;
   - mutable path, symlink, TOCTOU, stale inode, checkout substitution;
   - confirmed-send accepting anything except one opaque owner-issued receipt ID;
   - any approval-to-send shortcut.
3. If review FAILS, give only reproduced failures to a repair context. Repair test-first. Use focused tests during repair.
4. Re-run a fresh review on the amended exact SHA. Maximum two repair cycles. If still failing, stop BLOCKED.
5. On CONFIRM, run one final Python 3.12 clean-clone gate: focused suppression/confirmed-send suites, full suite, record validation, every checked-in CI guard, credential scan, clean worktree.
6. Push the exact confirmed branch, open/update the PR against main, and wait for every remote check. Do not merge.
7. Write JSON to:
   /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json

Exact JSON fields:
{
  "lane": "suppression",
  "status": "COMPLETE|BLOCKED|HUMAN_DECISION",
  "repo": "jsomwarux/jt-ops",
  "branch": "eve/suppression-owner-adapters",
  "sha": "<40-char SHA>",
  "pr_url": "<URL or null>",
  "review_verdict": "CONFIRM|FAIL|NOT_RUN",
  "focused_tests": "<compact result>",
  "full_tests": "<compact result>",
  "remote_ci": "<compact result>",
  "files_changed": ["<paths>"],
  "blockers": ["<blocker>"],
  "next_owner": "Eve",
  "next_action": "<exact action>"
}
8. Run exactly one notification:
   openclaw system event --text "Claude lane suppression: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json" --mode now

No progress narration to JT. Do not print logs in the terminal response. Terminal response must be one line: status + handoff path.
```

---

## Prompt B — n8n blueprint preflight controller

Run **in parallel with Prompt A**. Start Claude Code in:

`/Users/jtsomwaru/projects/n8n-agent`

Paste:

```text
You are the autonomous preflight controller for the cohort-two n8n prospect-discovery blueprint. Work only on this Mac Mini.

Repository:
- /Users/jtsomwaru/projects/n8n-agent
- branch: main
- required starting head: c42d105
- existing untracked blueprint: tasks/cohort-two-prospect-discovery-blueprint.md

Preserve the 2,308-line blueprint. Do not regenerate or overwrite it wholesale.

Read completely:
- CLAUDE.md
- tasks/lessons.md, especially lessons 132–144
- tasks/cohort-two-prospect-discovery-blueprint.md
- current jt-ops origin/main cohort-two contracts
- current Mission Control universal-card contract

Task:
Clear every blueprint preflight that is independent of the still-unmerged suppression/proof-card work.

Required work:
1. Verify the repository is private with `gh repo view jsomwarux/n8n-agent --json visibility,isPrivate`.
2. Verify the local n8n service and record its exact version. Expected current version is 2.14.1; do not assume it.
3. Inspect the installed `n8n-nodes-base` package and prove every selected node `typeVersion` in the blueprint is at or below the installed ceiling. Record exact evidence in §16.6.
4. Re-audit the 56-node list, connection list, terminal list, Error Trigger companion workflow, and one-entry fan-in inventory for internal consistency.
5. Confirm the fan-in redesign, runtime-shape-capture requirements, topology gate, disabled schedule, no-send boundary, and exactly-five rule remain intact.
6. Mark suppression SHAs/endpoints, proof-card presence, Mission Control deployed commit, jt-ops main SHA, and pipeline registration as PROVISIONAL for final reconciliation. Do not invent or hard-code unpublished values.
7. Add a compact preflight changelog to the blueprint. Focused edits only.
8. Run a fresh document review. Maximum one repair cycle because this is a blueprint audit, not implementation.
9. Commit the blueprint on a new branch named `eve/cohort-two-prospect-blueprint`. Push it, open a PR against main, and wait for available remote checks. Do not merge.

Not authorized:
- build/import/deploy/activate n8n nodes;
- inspect or modify credential values;
- create schedules;
- call Mission Control writes;
- send anything;
- change the architecture beyond corrections proven necessary by current evidence.

Write JSON to:
/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-preflight.json

Exact fields:
{
  "lane": "n8n-preflight",
  "status": "COMPLETE|BLOCKED|HUMAN_DECISION",
  "repo": "jsomwarux/n8n-agent",
  "branch": "eve/cohort-two-prospect-blueprint",
  "sha": "<40-char SHA>",
  "pr_url": "<URL or null>",
  "review_verdict": "CONFIRM|FAIL|NOT_RUN",
  "n8n_version": "<version>",
  "type_version_result": "<compact result>",
  "remaining_blockers": ["<blocker>"],
  "next_owner": "Eve",
  "next_action": "<exact action>"
}

Send one event:
openclaw system event --text "Claude lane n8n-preflight: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-preflight.json" --mode now

No progress narration to JT. Terminal response: one line only, status + handoff path.
```

---

## Prompt C — Mission Control suppression reconciliation

Run only after Prompt A's PR has been merged into `jt-ops/main`. It may run in parallel with Prompt D.

Start Claude Code in:

`/Users/jtsomwaru/.config/superpowers/worktrees/openclaw-workspace/mc-suppression-owner`

Paste:

```text
You are the autonomous reconciliation controller for Mission Control's inactive suppression owner.

Worktree:
- /Users/jtsomwaru/.config/superpowers/worktrees/openclaw-workspace/mc-suppression-owner
- branch: eve/mc-suppression-owner
- required starting head: 3d09ef9
- base branch: origin/master

Prerequisite:
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-suppression.json` must exist with status COMPLETE.
- Its exact confirmed suppression SHA must be an ancestor of current `jsomwarux/jt-ops` origin/main.
If either check fails, write BLOCKED handoff and stop.

Read CLAUDE.md, project lessons, suppression plans, tasks/todo.md, the complete origin/master...HEAD diff, and the suppression handoff.

Task:
1. Fetch current origin/master and current jt-ops origin/main.
2. Merge current origin/master safely into this feature branch; preserve unrelated live-workspace changes.
3. Derive the exact reviewed confirmed-send source blob directly from merged jt-ops main. Do not accept a pasted SHA.
4. Reconcile the exact-byte wrapper, runtime pin, routes, Convex contract, and tests to that merged commit/blob.
5. Keep suppression disabled when `OUTREACH_SUPPRESSION_ENABLED` is absent.
6. Prove disabled direct HTTP and direct Convex paths fail before auth, DB, Keychain, or network.
7. Prove existing dashboard, task, review, decision, and review-authority routes remain healthy.
8. Prove JT clear derives only from immutable approved review state; protected Git attestations are checked at storage boundary; pre-send receipts remain immutable, opaque, copy-free, and exact-binding.
9. Prove the wrapper materializes only reviewed Git bytes into a private runtime directory and executes isolated stdlib-only Python; stale/symlinked/swapped paths and mismatched blob SHAs fail before Keychain access.
10. Do not create/rotate/read capability values. Do not enable the flag. Do not deploy, schedule, or send.

Use TDD. Run focused tests during repair, then one final gate: full Bun suite, TypeScript, Convex bundle, protected-origin smoke, production build, credential scan, clean worktree. Run a fresh non-builder review; maximum two repair cycles.

On CONFIRM: commit, push the feature branch, open/update a PR against master, and wait for available remote checks. Do not merge or deploy.

Write:
/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-mc-suppression.json
with lane/status/repo/branch/sha/pr_url/review_verdict/test results/blockers/next_owner/next_action.

Send one event:
openclaw system event --text "Claude lane mc-suppression: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-mc-suppression.json" --mode now

No progress narration to JT. Terminal response: one line only.
```

---

## Prompt D — COI proof-asset evidence pack

Run after Prompt A is merged. It may run in parallel with Prompt C.

Start Claude Code in any clean Mac Mini directory and paste:

```text
You are the evidence controller for one human decision: JT's canonical cohort-two proof claim.

Sources:
- repository: jsomwarux/jt-ops
- current origin/main
- PR #33, head 514fbacbfc289434bf8fdbba31df19e1a997741e
- proof schema: schemas/proof_asset_card.schema.json

Task:
1. Create a fresh temporary clone of jt-ops. Do not modify any existing worktree.
2. Read PR #33's read-only COI runtime evidence, the proof-card schema, current registry/pipeline contracts, and current main.
3. Build a concise evidence pack for exactly one proposed public claim. Every clause must map to specific committed evidence.
4. Proposed starting sentence to test:
   `I built a workflow that sends certificate reminders on a daily schedule and gives staff a daily digest of overdue follow-up, upcoming expirations, data issues, and certificate status.`
5. Tighten or split the sentence only if the evidence does not support it exactly. Do not add metrics or claims not present in committed evidence.
6. Produce a proposed canonical card payload, but do not set `verified_by: jt`, do not write the canonical evidence file, and do not open a PR. This lane must stop for human judgment.
7. Run one fresh evidence review checking clause-to-proof mapping and permission-safe wording.

Write:
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/cohort-two-proof-asset-review.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-proof-asset.json`

JSON status must be HUMAN_DECISION and include:
- proposed exact sentence;
- proposed card payload without JT verification fields;
- evidence paths/SHAs;
- reviewer verdict;
- the single question: `Approve this exact proof sentence?`

Send one event:
openclaw system event --text "Claude lane proof-asset: HUMAN_DECISION; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-proof-asset.json" --mode now

Do not push, merge, deploy, activate, schedule, or send. Terminal response: one line only.
```

---

## Prompt E — canonical proof-asset card

Run only after JT approves the exact sentence and Eve writes:

`/Users/jtsomwaru/.openclaw/workspace/memory/job-state/cohort-two-proof-asset-approval.json`

Start Claude Code in a fresh temporary clone of `jsomwarux/jt-ops` and paste:

```text
You are the autonomous finalizer for the canonical cohort-two proof-asset card.

Prerequisites:
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-proof-asset.json`
- `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/cohort-two-proof-asset-approval.json`
- approval file must identify JT as approver and contain the exact approved sentence.
If any prerequisite is missing, malformed, or text differs, write BLOCKED handoff and stop.

Repository: fresh clone of jsomwarux/jt-ops at current origin/main.

Task:
1. Re-read PR #33 evidence and current proof-card schema.
2. Create `evidence/cohort-two.proof-asset.json` using only the exact approved sentence and committed evidence.
3. Set JT verification fields only from the approval artifact; do not infer them.
4. Add focused schema/evidence-binding tests and any required registry updates.
5. Run Python 3.12 focused tests, full suite, record validation, every checked-in CI guard, credential scan, clean-clone replay.
6. Run a fresh non-builder evidence/security review. Maximum two repair cycles.
7. On CONFIRM: commit on `eve/cohort-two-proof-asset`, push, open a PR against main, and wait for all remote checks. Do not merge.

Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-proof-asset-final.json` with status, exact SHA, PR URL, evidence, tests, blockers, next owner/action.

Send one event:
openclaw system event --text "Claude lane proof-asset-final: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-proof-asset-final.json" --mode now

No progress narration to JT. Terminal response: one line only.
```

---

## Prompt F — final n8n blueprint reconciliation

Run only after:
- Mission Control suppression code is merged and deployed **inactive**;
- the canonical proof-asset card is merged into jt-ops main;
- Prompt B completed.

Start Claude Code in `/Users/jtsomwaru/projects/n8n-agent` and paste:

```text
You are the final reconciliation controller for the cohort-two prospect-discovery blueprint.

Repository: /Users/jtsomwaru/projects/n8n-agent
Blueprint: tasks/cohort-two-prospect-discovery-blueprint.md

Prerequisites:
- claude-n8n-preflight.json status COMPLETE;
- claude-mc-suppression.json status COMPLETE and its PR merged/deployed inactive;
- claude-proof-asset-final.json status COMPLETE and its PR merged;
- current local main fast-forwarded to origin/main.
If any fail, write BLOCKED handoff and stop.

Task:
1. Fetch current jt-ops main and current deployed Mission Control source.
2. Re-run every §16 reconciliation check against current evidence.
3. Replace provisional SHAs/contracts with exact merged/deployed values.
4. Confirm the canonical proof card exists, validates, is current, and is referenced by the blueprint.
5. Confirm suppression remains outside n8n and no suppression endpoint appears in the workflow design.
6. Incorporate Prompt B's exact n8n 2.14.1 node typeVersion ceiling evidence.
7. Re-check Mission Control universal-card fields and disabled write contract.
8. Define the exact jt-ops pipeline/routine registration files the builder must add.
9. Reconcile node count, node list, connections, terminal list, tests, fixtures, build order, and handoff.
10. Run a fresh document review. Maximum two repair cycles.

Do not build/import/deploy nodes, inspect credentials, activate schedules, or send.

On CONFIRM: commit/update the blueprint branch, push/update its PR, and wait for checks. Do not merge.

Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-reconciliation.json` and send:
openclaw system event --text "Claude lane n8n-reconciliation: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-reconciliation.json" --mode now

Terminal response: one line only.
```

---

## Prompt G — n8n workflow implementation controller

Run only after Prompt F's blueprint PR is merged.

Start Claude Code in `/Users/jtsomwaru/projects/n8n-agent` and paste:

```text
You are the autonomous implementation controller for the approved cohort-two n8n prospect-discovery workflow.

Repository: /Users/jtsomwaru/projects/n8n-agent
Blueprint: tasks/cohort-two-prospect-discovery-blueprint.md
Base: current origin/main containing the merged, final reconciled blueprint.

Read CLAUDE.md and tasks/lessons.md completely before any edit.

Authorized:
- create an isolated feature branch/worktree;
- implement the blueprint exactly;
- create synthetic fixtures and runtime-shape captures;
- run focused tests and a fresh hostile review;
- repair reproduced failures, maximum two cycles;
- export workflow JSON;
- commit, push, open a PR, wait for CI;
- write handoff/event.

Not authorized:
- alter architecture;
- inspect/create/modify credentials;
- import into the live n8n instance;
- deploy or activate;
- enable any trigger or Mission Control write;
- use real prospects;
- send anything.

Implementation requirements:
1. Build every node/connection/config exactly as the final blueprint specifies.
2. Keep schedule trigger disabled, workflow inactive, Mission Control write disabled, no send-capable node present.
3. Preserve the exactly-five rule and reachable-channel gate.
4. Capture and check in actual runtime item shapes from controlled fixture-backed execution; add shape guards.
5. Prove offline topology: only trigger-exclusive N01 may have multiple incoming connections; convergence array indices and Error Trigger companion workflow must match the blueprint.
6. Run happy, no-result, malformed, duplicate, stale, concurrent-fatal, alignment-mismatch, proof-card-missing, and contract-drift cases.
7. Run repository visibility gate before any push.
8. Update tasks/lessons.md only with verified, genuinely new operational lessons.
9. Run a fresh non-builder review of the exact final SHA. Maximum two repair cycles.
10. On CONFIRM run one full clean-clone gate, export final workflow JSON, commit, push, open PR, and wait for CI. Do not merge or deploy.

Write `/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-build.json` with status, exact SHA, PR URL, node count, workflow JSON path, focused/full/reviewer/CI results, blockers, next owner/action.

Send one event:
openclaw system event --text "Claude lane n8n-build: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-build.json" --mode now

No progress narration to JT. Terminal response: one line only.
```
