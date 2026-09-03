# Review: JT Ops Playbook v4

**Date:** 2026-09-02  
**Verdict:** **REVISE — do not implement v4 yet**  
**Source:** `jt-ops-playbook-v4.md` (855 lines)  
**Live repo checked:** private `jsomwarux/jt-ops`, `main` at `84bf81e`

## 1. Executive judgment

v4 fixes the strategic failure in v3. It is smaller, commercially bounded, permission-aware, human-gated, and connected to a real outcome: qualified buyer contact and priced conversations. The demand-to-proof loop is now worth considering as a six-week pilot.

It is not implementation-ready. Several run-control and data-model gaps would recreate the exact silent-failure pattern the redesign is supposed to eliminate. The right next step is one v4.1 repair pass, not implementation.

## 2. What v4 gets right

- Deletes the ATS language feed from the commercial pilot.
- Keeps Eve and existing owner surfaces.
- Treats job postings as signals, not budgets.
- Moves permission-safe proof coverage into preflight.
- Caps output at three candidate cards per week.
- Separates infrastructure, task, delivery, and commercial success.
- Uses official current Claude Routines behavior for network modes, branches, connectors, triggers, and green-status limitations.
- Includes buyer-facing approval gates, zero tolerance for fabricated quotes and permission leaks, and a six-week kill rule.

## 3. Live-state evidence v4 must absorb

The private repo already exists and is not a blank skeleton.

- `main` contains 390 pending postings: 135 operator records and 255 ATS records.
- The daily GitHub Actions harvester is live and succeeded on 2026-09-02.
- The repo has assessed 252 NYC/NJ operators but can structurally read only 23, a 9.1% yield across the assessed set.
- `demand-ingest` and `demand-digest` have produced commits on `claude/` branches, but their receipts have not reached `main`; the registry on `main` therefore reports both as `NEVER RAN`.
- Current `main` CI is red from a deterministic extraction-flow regression.
- The OpenClaw action proof logger does not natively contain the stable `workflows_covered`, permission state/evidence, and shippable-claim fields assumed by v4. The proof export requires a real proof audit and mapping step, not a simple refresh.

This means Week 0 is a migration and repair project. It is not a clean one-evening build.

## 4. Blocking corrections required for v4.1

### B1. Remove the circular authorization gate

v4 says nothing in Week 0 may begin until section 12 is signed, but section 12 requires Step 0.4 proof coverage and Step 0.3 watchlist approval, which are Week 0 work.

Split the process:

1. **Read-only preflight authorization:** inspect live repo, proof coverage, watchlist feasibility, existing gates, and estimated build effort. No cron, workflow, routine, repo, or external write.
2. **Build authorization:** only after JT sees preflight evidence and explicitly overrides the freeze.

### B2. Restore the authoritative priced-conversation definition

The 90 Day Playbook defines a priced conversation as telling a real buyer a real number. v4 incorrectly requires a recurring line. A $1,500 Workflow Audit quote still counts.

Keep `recurring_line_quoted` as a separate commercial-quality field. Do not make it a prerequisite for `priced_conversation`.

### B3. Start from the live repo; do not create a second skeleton

Week 0 must begin with a read-only inventory and migration plan for the existing repo. Preserve history. Pause/archive excluded lanes; do not rewrite or delete append-only data. Fix current red CI before changing architecture.

### B4. Add stable posting identity and freshness

The observation model lacks a stable `posting_id`, `first_seen_at`, `last_seen_at`, `content_sha256`, and `active/removed` state. Without them, an old undated posting becomes “fresh” every weekly scan and can regenerate the same candidate forever.

Add deterministic dedupe, freshness, removal detection, contacted suppression, and a candidate cooldown.

### B5. Define who classifies workflows

`signal-scan` is described as deterministic Actions fetching, yet it writes `workflows[]`, `evidence_quote`, and offsets. The playbook never defines deterministic classification logic, and a generic rule would silently misclassify postings.

Actions should fetch and fingerprint only. The review routine should classify from the snapshot, then the verifier should test quote/offset/vocabulary and independently judge the mapping. Do not pretend workflow classification is deterministic unless exact tested rules exist.

### B6. Make the verifier event-driven and PR-aware

A fixed 07:30 schedule races a 07:00 review routine that may start late. It may find no PR and then wait a week. Also, a fresh clone starts from the default branch, so tests will not see candidate files unless the verifier explicitly fetches the PR diff/head.

Use the supported `pull_request.opened` or `pull_request.synchronize` trigger filtered to `candidates:` PRs. Specify exact PR fetch/diff behavior and test the PR head, not `main`.

### B7. Fix receipt invisibility

The live repo proves the failure: routine commits and receipts on unmerged `claude/` branches are invisible to the registry on `main`. v4 repeats it when zero candidates produce “no PR” and only a receipt.

Every weekly review must create one durable, human-visible artifact even at zero candidates: preferably one weekly PR containing the receipt and zero-result gate counts. No branch-only receipt may be treated as central run truth.

### B8. Replace the impossible client-name test

T6 requires a `client-map` held outside the repo, but the zero-connector fresh cloud verifier has no path to it. The test cannot run as written.

Run the client-name/permission scan at the OpenClaw export boundary before `proof-export.jsonl` enters GitHub. In-repo CI can validate the exported schema and permission states, but it cannot compare against a private map it cannot access.

### B9. Define real auto-pause authority

Changing `pipelines.json` does not pause a Claude Routine schedule. Official docs say the schedule is paused from the routine UI/CLI. No named actor in v4 is allowed to modify the registry, open the issue, and disable the actual schedule.

Make auto-pause two-stage: the job writes a pause-request artifact; JT explicitly disables the routine or approved orchestration does it. Name the actor, command/interface, proof, and rollback. Do not call a registry edit a paused automation.

### B10. Remove the outcome ownership conflict

v4 says Mission Control owns pipeline stage but `jt-ops` owns contacted/priced outcome records and mirrors contacted state back to Mission Control. That duplicates state.

Choose one:

- Mission Control owns current contact/stage state; `jt-ops` stores immutable pilot evidence events only, or
- `jt-ops` owns pilot outcomes and Mission Control stores only a linked task, not a copied stage.

The first option fits the existing system better.

### B11. Correct the credential claim

An API-triggered teardown requires a bearer token. Therefore “no credential is required” is false. Because JT is the human trigger, use **Run now** with the candidate id and remove the API trigger. If API triggering remains, the token needs a protected secret-store and rotation/revocation procedure.

### B12. Put approvals on every external or scheduled mutation

Step 0.5 creates and enables a scheduled GitHub Action with `contents: write` and direct commits to `main`, but it is not marked `[APPROVAL]`. That is an external scheduled write and requires explicit approval. Direct-to-main data writes also need a stronger factual gate than schema validation alone.

### B13. Implement the consumer contracts

The contracts describe pause behavior but no code or actor enforces it. Two zero-candidate weeks are also not automatically a failed scan; they may be valid market evidence. Separate machinery health, useful-zero results, unconsumed outputs, and commercial weakness.

### B14. Add snapshot retention

The layout says snapshots are pruned after use, but no job, retention window, acceptance condition, or receipt implements pruning. Preserve them through verification, then prune on a defined schedule while retaining hashes, citations, and source URLs.

### B15. Replace undefined ranking terms

`proof strength` and `channel directness` are ranking inputs but have no schema fields or deterministic order. Define them or remove ranking. Do not hide a subjective score behind unexplained words.

### B16. Make the time and cost estimate honest

The steady-state 30-minute review cap is plausible. “Week 0: one evening” is not. The live repo needs red-CI repair, legacy-lane migration, proof audit, 25-buyer verification, new schemas, acceptance tests, workflow changes, and three routine specs. Separate JT review time from agent engineering time and require an estimate after the read-only preflight.

## 5. Recommended v4.1 sequence

1. Read-only live-state audit.
2. JT sees proof coverage, operator yield, current CI/routine state, migration scope, and estimated engineering cost.
3. JT either stops or writes the explicit six-week freeze override.
4. Repair current CI and establish a clean baseline.
5. Migrate/pause legacy lanes without deleting history.
6. Build one weekly scan and one candidate-review PR path.
7. Trigger verification from the candidate PR.
8. Run one watched cycle with zero outreach.
9. Authorize the first buyer contact only after the complete evidence chain passes.
10. Apply the Week 3 and Week 6 kill gates.

## 6. Exact repair brief for Opus

> Produce v4.1 as a surgical correction of v4, not another redesign. Preserve the commercial scope and all sound sections. Correct every blocker B1-B16 in Eve's v4 review using the live `jsomwarux/jt-ops` state as the starting point. The repo already contains 390 pending postings, a live daily harvester, unmerged routine branches, two routines that appear NEVER RAN on main because their receipts never merged, and red CI. Add a read-only preflight before any freeze override or build authorization. Restore the authoritative priced-conversation definition: a real buyer heard a real number; recurring line quoted is separate. Add stable posting identity, first/last seen, removal state, dedupe, contacted suppression, and cooldown. Fetch in Actions; classify in the model routine; verify the PR head through a filtered pull_request trigger. Always create a durable weekly artifact, including zero-candidate weeks, so receipts cannot die on unmerged branches. Move the private client-name scan to the OpenClaw export boundary. Use Run now instead of an API bearer token for JT-fired teardowns. Define actual pause authority, snapshot retention, outcome ownership, ranking fields, and every approval boundary. Do not delete or rewrite legacy append-only data. Give exact commands, expected outputs, pass/fail criteria, and recovery steps only after verifying them against current official docs and the live repo. Output one standalone implementation playbook and a blocker-resolution table. Do not build anything.

## 7. Acceptance criteria for v4.1

- No circular approval dependency.
- Live repo state and migration are explicit.
- Current CI must be green before architecture changes.
- Every recurring run leaves evidence visible from `main` or a durable PR/issue.
- Freshness and dedupe cannot recycle stale postings.
- Verifier tests the actual PR head.
- Every test has access to every input it claims to use.
- Paused in registry and paused on the execution platform are distinguished.
- Mission Control and `jt-ops` do not both own contact stage.
- No credential-free claim while an API bearer token is required.
- The official priced-conversation definition is preserved.
- Week 0 effort is estimated from the live delta, not the imagined blank repo.

## 8. Sources checked

- Live private GitHub repo and Actions history, read-only, 2026-09-02.
- Current 90 Day Playbook: `memory/operating-mandates/90-day-playbook-2026-08-19.md`.
- Claude Routines: <https://code.claude.com/docs/en/routines>.
- Claude cloud environments: <https://code.claude.com/docs/en/cloud-environments>.
- GitHub Actions trigger behavior: <https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow>.

## 9. Next action

**Owner:** JT  
**Action:** Send section 6 plus this review to Opus for one v4.1 repair pass. Do not implement v4.
