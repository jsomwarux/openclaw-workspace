# Migration Runbook: Activate the July Directive Pack

For Eve, run WITH JT on the Mini. You prepare every diff. JT approves each batch before anything changes. Nothing here is autonomous.

## Ground rules for the whole migration

1. Every registry change and every AGENTS.md change is RED under directive 3. For each one: prepare the exact diff, show JT, wait for his explicit "approved" keyword, then apply, then paste the real tool output proving it landed, then log. No batch proceeds without approval.
2. Evidence contract, directive 1: after each applied change, paste the raw output that proves it, for example a fresh registry listing showing the job gone. No pasted proof means treat it as not done and stop.
3. Builder never grades, directive 2: do not self-certify. After each batch, re-read the live registry in a clean step and confirm the count against the target before moving on.
4. Hard Rules still bind: cron exec paths use `python3 /full/path/script.py`, update MEMORY.md's cron count and list in the same turn a job changes, and run `wc -c AGENTS.md` before any append.
5. Target state is the synced files, not memory. Read `directives/00-README.md` and `directives/01`–`05` first. The registry target, both message formats, and the disable list live there.

## Phase 0: Sync and baseline, green

1. Confirm the pack is present: `ls directives/` and `ls memory/job-state/`. Paste it.
2. List the full live cron registry with your cron tool. Paste the complete list. This is the baseline artifact.
3. Build a reconciliation table. For every live job, mark KEEP, DISABLE, or UNKNOWN.
   - KEEP is the 8 recurring jobs in the README registry table plus any one-shot reminders.
   - DISABLE maps to the README disable list, 37 named jobs in four groups.
   - UNKNOWN is any live job not named in either. The snapshot had 71 jobs and the audit named about 45, so expect unknowns. Do not guess. List them for JT with a one-line recommendation each.
4. Show JT the table. Do not change anything yet.

## Phase 1: Disable batch, red, needs approval

1. Present the disable diff: each job to disable, by its live id and name, grouped as refused-scope, reading-not-sends, killed-pending-marketing, merged-into-survivors, plus your recommendations for the unknowns.
2. Default to disable, which is reversible, not hard-delete. JT chooses whether to hard-delete after a clean week. The Friday scoreboard self-reduction line tracks eventual deletion.
3. On JT's approval, apply. If he edits the list, apply his version.
4. Paste the registry listing after. Confirm the surviving recurring count equals the target.

## Phase 2: Daily Send Sheet, red

1. Show the current Morning Brief job config and prompt next to the proposed rewrite: rename to Daily Send Sheet, schedule `30 7 * * *`, payload replaced by the Daily Send Sheet format in the README, Nash probe and every non-send section removed.
2. On approval, apply. Paste the new job config.

## Phase 3: Friday Scoreboard, red

1. Show the proposed new job: Friday Scoreboard, `0 16 * * 5`, announce delivery on, payload is the Friday Scoreboard format in the README with the directive 5 repeat-offender digest folded in before send.
2. On approval, apply. Paste the new job config.

## Phase 4: State files, green

1. For each surviving job, create `memory/job-state/<job-slug>.md` from `memory/job-state/TEMPLATE.md`. Create `memory/job-state/claims/` and `memory/job-state/archive/`.
2. Paste `ls -R memory/job-state/`.

## Phase 5: Activation, red, do this last

Do not activate before Phases 1 to 3 are done, or Eve will obey a registry spec that does not match the live jobs.

1. Run `wc -c AGENTS.md`.
2. Prepare the AGENTS.md diff:
   - Add one pointer line in File Routing, under the mandate line: standing directives load every session, obey after the mandate and above job prompts.
   - Add the compact non-negotiables block from the activation diff JT approved, so sub-agents, which see only AGENTS.md and TOOLS.md, inherit the rules.
   - To stay under 28,000 chars, relocate the now-dead sections whose jobs are killed to a subfile or delete them: Skills & API Researcher, Autoresearch Candidacy Rule, Niche Intel Propagation Rule. Removing these frees more than the block needs.
3. Show JT the full diff and the projected new `wc -c`. On approval, apply. Paste the new `wc -c`.
4. Update MEMORY.md: new cron count and list, per the Hard Rule.

## Close

1. Paste the final registry listing: 8 recurring jobs plus allowed one-shots.
2. Write the migration proof to `proofs/YYYY-MM-DD/` with every pasted artifact.
3. One-line summary to JT: jobs disabled, jobs surviving, activation done. From the next session, the directives govern.
