# Weekly Systems Review — 2026-07-12

## North Star Scoreboard
- Collected consulting cash: `$5,575`.
- Gap to $10K collected: `$4,425`.
- Weighted forecast: `$4,057.50`.
- Gap to $10K with forecast: `$367.50`.
- Aging pipeline items: `13`.
- Highest current gates: Altmark rent delinquency remaining `$2,250`, Marketsmith/Nexus follow-up state, Karen closeout/payment/profile.

## Waiting On >7 Days
- Altmark rent delinquency remaining — waiting on client.
- Altmark DHCR lease renewal phase 1 — waiting on client.
- Altmark support retainer — waiting on client.
- Altmark remaining workflow buildout — waiting on client.
- Aya acquisitions dashboard — waiting on client.
- Petri Plumbing follow-up — waiting on JT.
- HPM follow-up — waiting on prospect.
- Superior Plumbing follow-up — waiting on prospect.
- Family-office referral lane — waiting on client.
- Guyana connector leads — waiting on prospect.

Closed Aya StreetEasy scraper and Aya co-living dashboard appeared in the broad waiting scan because the local record contains `waiting_on`, but they are not active next-dollar gates.

## Phase 7 KPIs
1. Posts delivered vs posted: `3 delivered/queued`, `0 posted` since 2026-07-06 from `memory/content/posted-log.jsonl`.
2. Engagement per posted item: `unknown / not applicable` because no same-period posted item is confirmed; missing source is live engagement pull or posted-reply update.
3. Outreach packets completed vs sent vs replied: 2026-07-12 outreach preflight scanned `58` prospects, loaded `53` canonical Drive names, produced `1 warm_up_only`, `0 eligible copy-review`, `0 sent`, replies unknown from local preflight.
4. Consulting pipeline stage movement: no new stage movement proven during this run; current focus remains Altmark closeout, Marketsmith follow-up, Karen closeout, and Outbound v2 readiness.
5. Cron delivery rate: `12` enabled jobs; latest list shows `11 ok`, `1 stale error` (Weekly Systems Review from 2026-07-05), `3 delivered`, `9 not-requested`; delivered-or-not-requested rate `100%`.
6. Dollars spent: OpenRouter/OpenClaw weekly model spend `$1.494`; X API spend `unknown` because no current X billing ledger was found in the cost review output. Concrete fix: extend `scripts/cost-tracker.py --weekly-review` or a KPI script to include X API usage/billing.

## Cron Health
- `openclaw cron list` only worked when PATH included `/opt/homebrew/Cellar/node@22/22.22.2_2/bin`; normal shim failed with `env: node: No such file or directory`.
- Enabled jobs checked: `12`.
- Errors: `Weekly Systems Review` still shows previous `lastRunStatus=error`, `consecutiveErrors=3`, diagnostic `run openclaw cron (agent) failed`; this run is the natural proof that should clear it after completion.
- Delivery: no announce/user-facing job had failed latest delivery. Daily Send Sheet and weekly unemployment delivered.
- Diagnostics drift: Daily Send Sheet and weekly unemployment latest runs emitted pseudo-command warnings despite successful delivery.
- Timeout margins: no enabled job was observed within 10% of timeout. Notable long run: passive-income fetch signals `938,458 ms` on `3,600s` timeout.
- Sunday 10AM: Weekly Systems Review runs at 10:00; Pending Task Processor next at 10:30, so no direct 10AM collision.
- Never-ran enabled jobs: none from the CLI-listed enabled set.
- Invocation cap: registry `72 total / 12 enabled / 60 disabled`; weekday enabled count remains below the 20/day cap.

## File Budgets
- `AGENTS.md`: `27,806 / 28,000` chars. Under cap but very close; next append should extract first.
- `MEMORY.md`: `6,983 / 20,000`.
- `TOOLS.md`: `5,168 / 16,000`.
- `HEARTBEAT.md`: `4,189 / 16,000`.

## Process Health
- Gateway reachable via `openclaw status` with manual Node PATH workaround; service loaded and running as pid `68142`.
- Watchdog loaded: `com.openclaw.gateway-watchdog`.
- Runaway candidates:
  - OpenClaw gateway: about `720 MB` RSS, `2.1%` CPU, long-running since 2026-07-03.
  - Codex app-server: about `152 MB` RSS, sampled `34.4%` CPU; flag for observation, but this cron session itself can account for transient CPU.
- n8n, Convex, and Mission Control Next dev processes are present and not over CPU threshold in the sample.

## LaunchAgent Config
- Gateway label: `ai.openclaw.gateway`.
- Gateway `ThrottleInterval`: `10`, acceptable.
- Gateway ProgramArguments still point to `/opt/homebrew/opt/node/bin/node`; that path is currently missing from normal shell checks.
- Watchdog label: `com.openclaw.gateway-watchdog`.
- Watchdog `StartInterval`: `600`, acceptable upper bound.

## Version
- Current: `OpenClaw 2026.5.28 (e932160)`.
- Direct Brave result shows docs release `v2026.6.11` and newer GitHub release activity within the last day.
- Update available: yes. No update applied because OpenClaw updates require JT approval.

## Plugins
- `~/.claude/settings.json`: `context-mode@context-mode` is `false`.
- Extensions directory: only `lossless-claw` plus install backups observed.
- Warning persists: duplicate `lossless-claw` plugin id detected; global plugin overrides global plugin path.
- Security note: Claude settings include an MCP bearer-style token in a configured server. Do not paste it; review/rotate/move to approved secret home during a controlled security pass.

## Critical File Integrity
- `docs/agents/mistakes-log.md`: readable.
- `scripts/gateway-watchdog.sh`: present.
- `health/health.sqlite`: present.
- `tasks/pending.jsonl`: valid JSONL, `4` records. Single-document `json.tool` fails by design with extra data; line-by-line validation passes.

## Maintenance
- Autoresearch enrollment: no new checklist added. Recent modified repeated/scorable surfaces (`skills/ui-clone/SKILL.md`, `agents/ai-ops-teardown/weekly-prompt.md`) are already registered.
- Future signals: no triggers met. Sports/fantasy, site conversion rows, passive-income queue, ViewTrack, PostBridge, Remotion, and related app/tool signals remain parked.
- Passive-income pruning: closed `CollectionProof` as stale/superseded backlog noise. RuleWatch and Spreadsheet-to-Agent are older than 60 days but remain strategically adjacent to consulting proof; no promotion because trigger is not met.
- Mission Control: reachable. Existing high-priority task `Weekly Systems Review: reduce cron errors and daily agent-turn volume` updated with today’s Node/OpenClaw restart risk and pseudo-command diagnostics.
- Weekly cost review: total 7-day spend `$1.494`; monthly pace `$7.10` vs `$50` target; headroom `$42.90`; Groq/Llama unused.

## Issues Fixed This Run
- Used explicit Node PATH to complete OpenClaw CLI audit despite missing normal `node`.
- Pruned stale passive-income `CollectionProof` task.
- Updated existing high-priority Mission Control systems task with concrete first action, why it matters, and done state.
- Added this report and training-log entry.

## Needs JT Attention
- Approve a quiet-window Node/OpenClaw repair: restore normal `node` availability or update LaunchAgent node path, then smoke-test `openclaw --version`, `openclaw status`, and `openclaw cron list` from a clean shell.
- Decide whether to approve OpenClaw update evaluation from `2026.5.28` to current stable/release train.
- Review duplicate `lossless-claw` plugin warning and the bearer-style MCP token in Claude settings during a security/config pass.
- Cron prompt edits for pseudo-command diagnostics remain approval-gated; do not patch inside this cron without JT approval.

## Next Review
2026-07-19.
