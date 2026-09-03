# Prompt for Claude Opus: JT Ops Playbook v4

I am attaching two Markdown files:

1. `jt-ops-playbook.md` — the original v3 playbook you generated.
2. `jt-ops-playbook-review-2026-09-02.md` — Eve's evidence-based critique of v3.

Your job is to produce a replacement **JT Ops Playbook v4**. Do not defend, patch, or summarize v3. Re-architect it into the smallest reliable system that preserves its strongest ideas and can plausibly advance my North Star through buyer action and priced conversations.

## Governing objective

Design a **six-week demand-to-proof pilot** for NYC/NJ property managers and building owners:

verified operator demand signal → matching proof I actually own and can safely show → one buyer-ready workflow teardown → outreach/outcome evidence.

The pilot must improve my odds of reaching qualified buyers and priced conversations without displacing active client delivery, warm outreach, or cash-producing work. Planning this pilot does **not** itself authorize implementation or override any current freeze.

## Required judgment

Treat Eve's review as a binding issue list, but verify every technical claim independently against current official documentation before writing the playbook. If you disagree with a review finding, say so only when you can cite authoritative evidence and design a safer alternative. Do not preserve v3 architecture merely because work has already gone into it.

## Scope to keep

- Version-controlled prompts and routine instructions.
- Schema validation, pipeline registry, and run receipts.
- Source citations, verbatim-quote validation, permission controls, and anonymized proof.
- Independent verification that tests task-level correctness, not merely process exit status.
- A consumer contract for every recurring job: named consumer, decision changed, consumption artifact, deadline, and auto-pause condition.
- Human approval for buyer-facing artifacts, source-of-truth changes, and prompt changes.
- Four bounded functions only: demand trigger radar, proof matching, buyer-ready teardown generation, and outcome capture.

## Scope to remove

- Ensemble-core or cross-app abstraction work.
- Passive-income candidate generation.
- Knowledge ingestion or knowledge-atom systems.
- Automatic prompt mutation or automatic prompt merging.
- Eve retirement or a second all-purpose operating system.
- A new canonical store for facts already owned by OpenClaw, Mission Control/Convex, Drive, proof logs, client folders, or project repos.
- Any metric that treats records, reports, corpus size, or job-posting salary as commercial success.

## Pilot constraints

- Universe: 25 verified NYC/NJ property operators.
- Cadence: weekly, not daily.
- Maximum output: three qualified candidates per week.
- Hard gates for a qualified candidate: named buyer, reachable channel, fresh live workflow signal, matching permission-safe proof asset, and a specific reason to act now.
- Human decision: contact, reject, or defer.
- Week-six success: at least three qualified signals contacted, at least one priced conversation, zero fabricated quotes, zero permission leaks, and under 30 minutes of weekly review.
- Kill rule: if there is no priced conversation or buyer-confirmed pain by the end of week six, pause the pilot and preserve its evidence.
- No cron creation/enabling, deploy, direct-to-main push, external send, third-party system write, decommission, or source-of-truth migration may be presented as pre-authorized.

## Existing-system integration requirement

Before proposing a new file, database, repo, report, queue, or dashboard, identify whether an existing owner surface already owns that fact. Use one owner surface per fact and define read/write boundaries. Treat any new repo as a narrow append-only evidence exchange or reporting mart, not the canonical home for everything. Explicitly map the pilot to the existing proof system, future-signals process, correction/mistake lifecycle, Mission Control, Drive/client artifacts, and OpenClaw orchestration.

## Technical verification requirement

Use current official Anthropic and GitHub documentation to verify Claude Code Routines capabilities, network modes, supported triggers, branch behavior, quotas/limits, secrets, scheduling, and what a successful routine status actually proves. Cite the exact official URLs next to the affected design decisions. Resolve every contradiction named in Eve's review, including schema/join fields, stale routine names, Actions-versus-routine fetching, and task-success verification.

## Required output

Return one standalone Markdown document titled `JT OPS PLAYBOOK v4 — Six-Week Demand-to-Proof Pilot` that I can follow without referring back to this prompt.

It must include, in this order:

1. Executive decision: what is being built, what is excluded, and why.
2. Current-state integration map: each fact, its authoritative owner, readers, writers, and prohibited duplicate stores.
3. Minimal architecture and data flow.
4. Exact schemas and stable join keys.
5. Security, privacy, permission, and prompt-injection controls.
6. Independent verification model, with task-level acceptance tests and failure handling.
7. Six-week sequence with explicit approval gates and rollback/pause points.
8. For every step: owner/agent, exact tool or interface, exact copy-paste prompt or command, files read/written, prerequisites, expected raw output, verification command, pass/fail criteria, and recovery procedure.
9. Consumer contract for every recurring job.
10. Measurement dashboard: leading indicators, commercial outcomes, review-time budget, and kill criteria.
11. Cost/quota estimate and failure budget.
12. Final go/no-go checklist before any implementation begins.
13. A concise change log explaining how v4 resolves every material issue in Eve's review.

## Quality bar

- Prefer deletion and integration over invention.
- No placeholder commands, fake APIs, guessed UI labels, unsupported triggers, or instructions that rely on undocumented behavior.
- Clearly label any step that requires my explicit approval.
- Separate infrastructure success, task success, delivery success, and whole-request completion.
- A Git commit, green workflow, or zero exit code is never sufficient proof of factual correctness.
- If an unresolved platform limitation prevents an airtight step-by-step instruction, mark it as a blocker and give the safest manual alternative. Do not invent a workaround.
- Keep the weekly human burden under 30 minutes and state how that estimate is calculated.
- The result must be implementation-grade, internally consistent, and substantially smaller than v3.

Output only the completed v4 Markdown playbook. Do not start building anything.
