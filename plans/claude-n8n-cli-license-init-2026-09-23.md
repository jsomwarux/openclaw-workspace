# Claude Code controller prompt — n8n CLI license initialization

Run this in a fresh Claude Code session on the **Mac Mini**.

```text
You are the controller for one bounded n8n runtime-compatibility repair.

Repository:
- canonical repo: /Users/jtsomwaru/projects/n8n-agent
- create and work only in a fresh isolated worktree:
  /Users/jtsomwaru/projects/n8n-agent/.worktrees/n8n-cli-license-init
- branch: eve/n8n-cli-license-init
- base exact SHA: 16c832caa1029fc5ca7ea9a81e8fd00a62414ffb (origin/main)

Do not edit the dirty canonical checkout. Verify origin/main is exactly the base SHA before creating the worktree. Stop BLOCKED if the branch/worktree already exists with unexpected content.

Read completely before editing:
- CLAUDE.md
- tasks/lessons.md
- tasks/todo.md
- workflows/cohort-two-prospect-discovery.json
- the installed n8n 2.14.1 files:
  - /opt/homebrew/lib/node_modules/n8n/dist/commands/execute.js
  - /opt/homebrew/lib/node_modules/n8n/dist/commands/base-command.js
  - /opt/homebrew/lib/node_modules/n8n/dist/commands/start.js
  - /opt/homebrew/lib/node_modules/n8n/node_modules/@n8n/backend-common/dist/license-state.js

Observed defect — reproduce it from source and lock it with tests:
- `Start.init()` calls `initLicense()`.
- `Execute.init()` calls `super.init()`, binary-data init, dedup init, and external hooks, but never calls `initLicense()`.
- Cohort execution 1720 reached N22 and both Anthropic HTTP Request items failed before network I/O with:
  `Cannot query license state because license provider has not been set`.
- The stored `anthropicApi` credential exists and is ordinary (`isResolvable=0`, `resolvableAllowFallback=0`, no resolverId). Do not inspect, decrypt, print, copy, or modify credential data.
- The live n8n server path initializes the provider correctly. Production/server execution is not defective; only `n8n execute` is.

Task:
Build a project-local, explicit launcher for manual/controlled CLI workflow execution that initializes the n8n License/LicenseState provider before invoking the unchanged n8n execute command.

Required architecture:
1. Do not modify anything under /opt/homebrew/lib/node_modules, /opt/homebrew/bin, ~/.n8n, LaunchAgents, or live workflow/state directories.
2. Do not change workflow JSON, credential metadata/data, model configuration, schedule state, or n8n configuration.
3. Keep the workaround project-local under scripts/ and make it explicit at invocation; normal `n8n execute` must remain untouched.
4. Fail closed unless the installed n8n version and required internal methods match the reviewed compatibility contract. Pin/support n8n 2.14.1 only unless tests prove a broader exact contract.
5. Preserve all existing execute flags and environment variables required by the controlled pilot (`--id`, `--rawOutput`, file allowlist, excluded nodes, alternate task-broker/port values).
6. Never read, print, accept, or forward secret values itself. Credential resolution remains owned by n8n.
7. Do not suppress execution errors or alter exit semantics.
8. The launcher must initialize the provider exactly once and prove `LicenseState` has a provider before workflow execution begins.
9. Prefer the smallest maintainable mechanism. Do not copy n8n's execute implementation or patch installed source. If a safe in-process wrapper is impossible against the published package surface, stop with evidence rather than using a brittle global monkeypatch.

TDD and test requirements:
- Add failing tests first for the missing initialization and every fail-closed compatibility check.
- Tests must use isolated fakes/fixtures. They must not touch the live n8n DB, live workflow, live state, network, model APIs, credentials, Keychain, or filesystem outside a temporary directory.
- Prove: provider initialized before delegated execute; initialization failure prevents execution; unsupported version prevents execution; missing/renamed internal method prevents execution; flags/env pass through; exit/error semantics preserved; no secret-bearing env or credential data is logged.
- Add a static guard proving no installed-package write/patch path exists in the launcher.
- Update tasks/lessons.md with the verified n8n 2.14.1 CLI/server lifecycle distinction.
- Update tasks/todo.md with only this bounded task state.

Review protocol:
1. Implement test-first in the isolated worktree.
2. Run focused tests during development.
3. Run the repository's exact full zero-skip test command with the required jt-ops fixture/bootstrap dependency.
4. Launch a fresh non-builder hostile reviewer in a clean clone at the exact final SHA. The reviewer must attack secret leakage, installed-package mutation, version drift, double initialization, flag/env corruption, swallowed failures, accidental live DB access in tests, and any path that changes workflow/state.
5. Maximum two repair/review cycles. If a new systemic class remains, stop BLOCKED.
6. On CONFIRM, run one final clean-clone zero-skip gate, credential scan, and repository-visibility check.
7. Commit, push `eve/n8n-cli-license-init`, open a PR against main, and wait for remote checks. Do not merge.

Not authorized:
- live workflow execution or pilot resumption;
- live DB/state reads or writes beyond metadata-free health/version checks;
- model/web calls;
- credential access or changes;
- installed n8n edits;
- deploy, activate, schedule, send, merge, or unrelated cleanup.

Write the compact handoff to:
/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-cli-license-init.json

Handoff fields:
- status: COMPLETE | BLOCKED | HUMAN_DECISION
- repo, branch, exact SHA, PR URL
- reviewer verdict
- focused/full/clean-clone results and skip count
- files changed
- compatibility contract
- blockers
- next_owner: Eve
- exact next action

Send one internal event:
openclaw system event --text "Claude lane n8n-cli-license-init: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-n8n-cli-license-init.json" --mode now

Terminal response: one line only — status + handoff path.
```
