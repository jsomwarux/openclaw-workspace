# Review — AI Workflow Growth Operating System v3

**Reviewer:** Eve  
**Source:** Fable v3, 720 lines, received 2026-09-09  
**Verdict:** **REVISE BEFORE EXECUTION**  
**Architecture verdict:** Approved. No further redesign round is needed.

## Objective

Verify that Fable's v3 is a standalone, executable synthesis of the prior v2, Grok feedback, current workspace state, and JT's September 8 strategic reset.

## What v3 gets right

1. Extends `jt-ops`; does not build a second spine or task board.
2. Preserves specialist ownership: n8n for workflow source/runtime, Job Hedge for jobs, app repos for product truth, Mission Control for human decisions, OpenClaw for orchestration and verification routing.
3. Starts manual buyer motion in parallel with repair work.
4. Separates outreach intelligence from delivery infrastructure.
5. Uses typed contracts, payload hashes, provenance, fresh verification, run receipts, backpressure, and explicit failure behavior.
6. Caps daily human review at 30–45 minutes and global build WIP at two tracks.
7. Keeps sends, posts, applications, purchases, schedules, DNS, deployments, and account changes behind JT approval.
8. Hardens existing systems instead of rebuilding Job Hedge or creating separate content stacks.

## Blocking corrections

### 1. Define the real cohort-one repository and write path

The D2 prompt assumes the preflight and 58 folders are in one “outreach repository.” They are not:

- Preflight code: `/Users/jtsomwaru/.openclaw/workspace/scripts/outreach_pipeline_runner.py`
- Prospect folders: `/Users/jtsomwaru/projects/jt-consulting-pipeline/clients/`
- Existing preflight reports: `/Users/jtsomwaru/.openclaw/workspace/reports/outreach-pipeline/`
- Proposed canonical cohort report: `jt-ops/reports/cohort-1-review.md`

**Required fix:** Name all three source surfaces and one canonical destination. D2 should read the workspace preflight and consulting-pipeline data, then write the review artifact and manifest to a `jt-ops` worktree. It must not edit suppression state or duplicate relationship truth.

### 2. Split repair from feature expansion, and fix the impossible `main` claim

D1 bundles R1–R3 root-cause repair with R4 contract/Convex expansion. That can bury the urgent pipeline repair inside new feature work.

A feature branch also cannot prove “main CI green for 24 hours” before an approved merge.

**Required fix:**

1. Checkpoint 1A: R1–R3 only; local/branch tests green; open a PR; builder does not merge.
2. JT approves the merge.
3. Verify `main` CI and one live end-to-end cycle for 24 hours.
4. Checkpoint 1B: R4 schema/adapter additions only after the repair gate passes.

No dispatch prompt may imply that a builder can push, merge, pause a schedule, or alter production without the named approval.

### 3. Resolve the feedback-routing contradiction

Section 7.1 says the feedback box routes to the owning agent's lessons file. Section 12 correctly says raw feedback never writes directly into the canonical skill.

**Required fix:** Raw feedback goes to one append-only feedback log. The Friday evaluator proposes a diff with evidence and a regression test. Only an approved patch reaches a canonical skill or lessons file.

### 4. Give prospect/client state one owner

The ownership table lists both “existing consulting files and Mission Control” as authoritative for prospect/client relationship state.

**Required fix:** Split the fact:

- Mission Control owns current stage, next action, assignee, and decision state.
- The consulting-pipeline/client folder owns research, drafts, correspondence evidence, and client artifacts.
- `jt-ops` stores immutable pointers/hashes only.

### 5. Make the first niche singular

“Property/supportive housing first” conflicts with the one-active-niche rule and would blend materially different buyers and outcomes.

**Required fix:** Use the M-1 requalification yield to select one first cohort. If both segments run, treat them as separate cohorts with separate scoreboards and never pool reply evidence.

### 6. Do not mandate the established mailbox

M-2 requires JT to send from his established mailbox while the delivery section protects the primary business domain from cold-volume campaigns.

**Required fix:** The cohort card must name the approved sending mailbox and its risk boundary. A primary/established address may be used only for a small hand-written cohort after authentication and reputation checks; otherwise the sends wait for an approved dedicated mailbox. The plan should not choose this implicitly.

### 7. Correct Grok Bot pricing and entitlement

The current official xAI documentation says Grok Bot access is included with eligible paid Cursor, SuperGrok, and X Premium+ plans, with usage governed by the plan and optional on-demand billing. The fixed `$120–$300/month` claim is not current enough to retain.

**Required fix:** Replace the price with `included/allowance TBD at activation; verify account entitlement and incremental usage price`.

### 8. Keep private X samples out of console logs

D4b says to print the newest three liked posts and bookmarks. Bookmarks are private user data.

**Required fix:** Console output should contain counts, status, and cost only. Store minimal sample IDs/hashes in a protected local test artifact; do not print post contents into logs or a shareable report.

## Non-blocking clarifications

1. Manual X publishing is correct because JT is the approval boundary; the API's low per-post price is not the reason.
2. `overflow auto-redates` needs a named deterministic Mission Control owner, idempotency behavior, and a no-duplicate test.
3. Fresh verification must use a separate clean-context session when native subagents are unavailable.
4. Dispatch prompts should require each repository's `CLAUDE.md`, `AGENTS.md`, and lessons file before changes.

## Verified current facts

- GitHub `jsomwarux/jt-ops` still points to `main@2d1c95dc` (`harvest: 2026-09-09`). Recent `harvest` and `validate` runs on the current line are failing.
- The September 9 outreach preflight reports no fresh copy-review queue; the old 57 are not automatically send-ready.
- X API Owned Reads currently price own bookmarks and liked posts at `$0.001` per returned resource.
- Gmail guidance supports the plan's `<0.1%` target and `0.3%` hard ceiling, alongside authentication and gradual ramping.
- Grok Bot availability/pricing language in v3 needs the correction above.

## Acceptance criteria for v3.1

- All eight blocking corrections are incorporated.
- D1 and D2 each name exact working directories, read surfaces, write paths, branch behavior, and approval boundaries.
- Repair and schema expansion are separate checkpoints.
- No worker's done condition depends on an unapproved merge or production mutation.
- No raw feedback writes directly to a skill/lessons file.
- One first outreach niche is selected or cohort metrics remain separated.
- Current platform costs are either cited and current or explicitly `TBD` until activation.

## Next action

Patch v3 directly into a v3.1 execution copy. Do not request another model rewrite. After the eight corrections, the plan is ready for JT to approve Checkpoint 1A and the five-prospect manual research packet track separately.
