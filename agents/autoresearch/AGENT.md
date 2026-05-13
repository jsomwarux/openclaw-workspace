# Autoresearch Agent
*Autonomous skill self-improvement loop. Based on Karpathy's autoresearch method.*
*Created: 2026-03-19*

## Purpose
Run a skill or agent prompt against test inputs, score each output against a yes/no checklist, make one targeted mutation, keep the change if score improves, revert if not. Repeat until score hits 90%+ three times in a row or max rounds reached.

## Karpathy-inspired experiment discipline
This loop adapts Karpathy's `autoresearch` pattern to skills/prompts instead of model training code:
- **Fixed metric:** checklist pass rate averaged across the same test inputs for baseline and every mutation.
- **Baseline first:** every run starts by scoring the unmodified target.
- **One modifiable target:** mutate only the selected skill/agent/prompt/cron payload, never unrelated files.
- **One mutation per round:** one small rule/example/constraint change at a time.
- **Keep/discard/crash ledger:** every round is logged as `keep`, `discard`, or `crash` in changelog and `results.tsv`.
- **Revert discipline:** if score is equal/worse, restore the exact pre-mutation text/payload before trying another idea.
- **Simplicity criterion:** prefer the smallest clear rule that improves score; reject complexity unless it materially improves the metric.
- **Crash handling:** syntax errors, missing files, bad cron payloads, or tool failures are logged as `crash`; restore pre-run state before continuing or blocking.

## Invocation
- **Overnight agent on-demand:** "run autoresearch on [slug]"
- **Recurring sweep (Mon/Wed/Fri 11:15 AM ET, cron `ec9f36d3-3bf8-4bc9-a4b1-06aa886a24ff`):** run one bounded high-value `active` or `pending` target from targets.md using `weekly-sweep-prompt.md`
- **Manual:** JT says "run autoresearch on [skill name]"
- **Volume trigger (outreach):** After the outreach pipeline has generated 10+ cold email drafts since the last autoresearch run on `cold-email` (check `logs/` for last run date vs. pipeline shortlist counts), the overnight agent should run autoresearch on cold-email before the next batch. Check: count entries in `~/projects/jt-consulting-pipeline/shortlists/` with M1/M2/M3 dates newer than the last cold-email autoresearch log date.

## Step 0: Load targets
Read `~/.openclaw/workspace/agents/autoresearch/targets.md`.
Identify the target(s) to run. For recurring sweep: pick exactly one highest-value row with status `pending` or `active`.
For on-demand: match slug to row.

## Step 1: Load skill + checklist
Read the skill/agent file at the path in the targets.md row.
Read the checklist at the checklist path.
Confirm checklist has ≤ 6 questions. If >6: halt and alert JT — checklist needs trimming before loop runs.

## Step 2: Generate test inputs
Create 3–5 test inputs appropriate for the skill. For outreach skills: use realistic prospect profiles (niche, company name, contact name, one signal). For content skills: use realistic post prompts ("Write a Thursday LinkedIn post about Agentforce routing logic").
Save test inputs to `logs/[DATE]-[slug]-inputs.md`.
Use the exact same test inputs for baseline and every mutation in the run. Changing test inputs mid-run invalidates the comparison.

## Step 3: Baseline run
Run the skill against all test inputs. Score each output against the checklist (1 = yes, 0 = no, per question per output). Average all scores → baseline score.
Log: `[Round 0] Baseline: [score] | Failing checks: [list]`

If baseline >= 0.90: log "Already at target. No loop needed." Update targets.md status to `stable`. Stop.

## Step 3.5: Mutation safety preflight
Before any mutation, run and log:
```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
```
Budget gates:
- `AGENTS.md` must stay <28,000 bytes.
- `MEMORY.md` must stay <20,000 bytes.
- `TOOLS.md` must stay <16,000 bytes.
- `HEARTBEAT.md` must stay <16,000 bytes.
If a target mutation would touch one of these files and the file is within 500 bytes of budget, compact/move old material to a subfile first or mark BLOCKED. Never append to a near-budget bootstrap file blindly.

## Step 4: Improvement loop
Repeat until (score >= 0.90 for 3 consecutive rounds) OR (rounds >= 20):

**4a. Analyze failures**
Look at which checklist items are failing most across all test inputs. Identify the one failing most often.

**4b. Diagnose root cause**
Read the current skill prompt carefully. Identify ONE specific rule, example, constraint, or missing instruction that plausibly explains why that checklist item keeps failing.

**4c. Mutate (smallest change first)**
Before mutating, save an exact pre-mutation snapshot:
- For files: keep the original text in memory and note the path in the changelog.
- For cron payloads: fetch and save the original payload/message before `cron update`.
- For scripts: prefer textual rule/check changes over behavioral code changes unless the checklist explicitly requires code behavior.

Try mutation types in this order — stop at the first that addresses the root cause:
1. Add a banned phrase/word to an existing list
2. Tighten an existing constraint (stricter word count, more specific rule)
3. Add a new rule for the most common failure
4. Add a worked example showing what good looks like
5. Remove a rule causing unintended side effects

Make ONLY ONE change per round. Never rewrite whole sections.

**4d. Re-run + score**
Run the mutated skill against all test inputs. Score against checklist. Average → new score.

**4e. Keep or revert**
If new score > previous score: keep the change.
If new score <= previous score: revert to the exact pre-mutation skill text, file text, or cron payload.
If the mutated target crashes or cannot be evaluated: log `crash`, revert exact pre-mutation state, and try a smaller mutation only if the root cause is obvious.

**4f. Log the round**
```
[Round N] Score: [new score] | Change: [description] | Result: keep/discard/crash | Reason: [why]
```

## Step 5: Apply + Save outputs

**Apply the fix immediately — do not create an MC task.**
If score improved from baseline, the fix is validated. Apply it now:

For **skill files** (SKILL.md): overwrite the file directly using the Edit tool.
For **cron payloads**: patch with the verified CLI form `openclaw cron edit <id> --message "..."` plus any required `--timeout-seconds`, `--thinking`, `--cron`, or `--failure-alert*` flags. Confirm the returned job JSON contains the intended message/schedule/timeout/thinking before logging success. Do not use vague or unverified `cron update` wording.
For **AGENTS.md rules**: check `wc -c` first, then append/edit only if still under budget; otherwise move stale content to the documented subfiles before adding the rule.

There is no reason to create an MC task for a validated improvement. The loop already validated it. Creating a task and waiting for JT to apply it manually defeats the entire purpose of autoresearch.

**Exception:** if the mutation is architectural (restructuring entire skill, changing the skill's purpose, or removing a section JT wrote) — save to `-improved-[DATE].md` and flag to JT for review. Wording/constraint tweaks do not qualify as architectural.

**Changelog** (`logs/[DATE]-[slug]-changelog.md`):
```
# Autoresearch Changelog — [slug] — [DATE]
Baseline: [score]
Final score: [score]
Rounds: [N]

## Changes applied
- Round N: [what changed] | [score before → after] | Applied to: [file/cron ID]

## Changes tried and reverted
- Round N: [what changed] | [why reverted]

## Recommendations
[Any changes that kept failing — surface for JT to review manually]
```

**Results summary** (`logs/[DATE]-[slug]-results.md`):
One-paragraph summary of what changed, why, and where it was applied.

## Step 6: Update targets.md
Update the row for this slug:
- Status: `stable` (if 90%+ hit) or `active` (if max rounds hit, still improving)
- Last Score: final score
- Last Run: today's date

Also append one row to `agents/autoresearch/results.tsv`:
```
date	run_id	slug	baseline_score	final_score	rounds	status	changes_kept	changes_reverted	files_touched	description
```
Use `status=keep` when final score improved or was already stable, `discard` when no improvement survived, and `crash` when the run could not safely evaluate or restore.

## Step 7: Notify
If run by overnight agent: append to overnight log. Do NOT send a separate Telegram.
If run on-demand by JT: send Telegram summary (channel=telegram, target=6608544825):
```
🔬 Autoresearch — [slug]
Baseline: [X]% → Final: [Y]%
Rounds: [N] | Changes kept: [N] | Reverted: [N]
Improved skill saved: [path]
Changelog: [path]
```

## Cost guardrails
- Max 20 rounds per run
- Max 5 test inputs per round
- Hard stop if estimated cost exceeds $0.50 for this run
- Log estimated cost to changelog header

## Critical constraint
Checklist must stay ≤ 6 questions. If a skill needs more than 6 to score adequately, it means the skill is too broad — split it first, then enroll each part separately.
