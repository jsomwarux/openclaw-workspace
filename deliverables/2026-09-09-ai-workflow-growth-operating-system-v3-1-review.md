# Review of AI Workflow Growth Operating System v3.1

**Verdict:** APPROVE AFTER FOUR SURGICAL PREFLIGHT EDITS. Do not send this back for another strategy rewrite.

## What v3.1 fixed

All eight blocking findings from the v3 review are resolved:

1. D2 now names the real outreach preflight, report, prospect-folder, and `jt-ops` write surfaces.
2. `jt-ops` repair is split into Checkpoint 1A (R1-R3) and Checkpoint 1B (R4), with JT-controlled merge and a real 24-hour `main` gate.
3. Feedback is append-only and reaches canonical lessons only through Friday-reviewed, regression-tested proposals.
4. Mission Control owns relationship stage and decisions; `jt-consulting-pipeline` owns research, correspondence evidence, drafts, and client artifacts.
5. The first outreach niche is selected from evidence; property management and supportive housing remain separate cohorts and scoreboards.
6. The plan no longer silently chooses JT's established mailbox.
7. Grok Bot cost/entitlement is correctly left account-specific and unverified until activation.
8. Private X likes/bookmarks are excluded from console and shareable report output.

The runbook also fixes the prior plan's usability problem: JT now has an ordered sequence and paste-ready dispatch prompts.

## Four required edits before execution

### E1. Establish one canonical local `jt-ops` path before Step 2

The runbook alternates among `jsomwarux/jt-ops`, `jt-ops`, and a “fresh jt-ops worktree,” but there is no current local clone under `/Users/jtsomwaru/projects/`.

Add a Step 0:

> **Step 0 [PASTE]:** Create or verify the canonical local clone at `/Users/jtsomwaru/projects/jt-ops`, verify its `origin` is `git@github.com:jsomwarux/jt-ops.git` (or the authenticated equivalent), fetch without mutation, and create two named worktrees for D1A and D2. Record the absolute paths. Do not push, merge, or edit schedules.

Replace every ambiguous `in jt-ops` / `in jsomwarux/jt-ops` reference with the recorded absolute clone or worktree path. Cross-repo prompts D3, D4b, D5, and D6 must use the absolute plan/report paths.

### E2. Split first pilot campaign activation from the 50-message fleet decision

Step 20 currently says to inspect the first 50 delivered messages before approving the “first real campaign.” Those 50 messages cannot come from the four-inbox pilot until a first pilot campaign is approved.

Use three gates:

1. **Warmup gate:** five QA-passing packets + spend approval authorizes infrastructure and warmup only.
2. **Pilot campaign gate:** warmup complete, SPF/DKIM/DMARC/TLS and placement checks pass, suppression/unsubscribe/reply ownership proven, cohort copy approved, and JT activates one low-volume campaign with a fixed send cap.
3. **Fleet/volume gate:** after 50 delivered niche-consistent messages, apply bounce, complaint, positive-reply, and buyer-pain evidence before raising volume or adding inboxes.

Change Runbook Step 20 to “evaluate the first 50 delivered pilot messages for scale,” not “approve the first real campaign.”

### E3. Sandbox Content Engine adapter tests

D9 can currently write synthetic cards through Mission Control and push approved items to live Notion during a build session.

Add to D9:

> All Mission Control and Notion tests use mocks, local/test deployments, or dry-run adapters. No production Mission Control row or Notion page may be created or edited. Live adapter activation and the first production write each require separate JT approval after the PR merges.

The synthetic end-to-end acceptance test must prove the outbound payload and idempotency without mutating production.

### E4. Isolate Job Hedge's synthetic Drive test

D5 requires a synthetic role to round-trip through live Drive readback but does not name an isolated test destination or cleanup policy.

Add to D5:

> The synthetic package uses a dedicated Drive test folder or a mocked Drive adapter. It may not enter the real Job Applications folders or Mission Control. Any live test artifact requires explicit JT approval, is labeled TEST, and is retained or removed only by an approved cleanup decision.

Real packages continue to follow the existing job-application skill and Drive rules.

## Execution decision

After E1-E4 are inserted, approve Runbook Steps 1-3 only. Those steps still do not authorize sends by an agent, purchases, schedule changes, merges, deployments, or production integration writes.

Checkpoint One succeeds only when:

- D1A produces a PR with branch evidence;
- JT approves the merge;
- `main` remains green for 24 hours;
- one live end-to-end cycle is visible on `main`;
- D2 produces five verified packets in one evidence-selected niche;
- JT independently decides whether and how to send them.

Do not begin D1B, warmup purchases, Content Engine production adapters, or any scheduled lane merely because a branch is green.
