# Autoresearch Agent
*Autonomous skill self-improvement loop. Based on Karpathy's autoresearch method.*
*Created: 2026-03-19*

## Purpose
Run a skill or agent prompt against test inputs, score each output against a yes/no checklist, make one targeted mutation, keep the change if score improves, revert if not. Repeat until score hits 90%+ three times in a row or max rounds reached.

## Invocation
- **Overnight agent on-demand:** "run autoresearch on [slug]"
- **Monthly sweep (1st of month):** run all `active` or `pending` targets in targets.md one at a time
- **Manual:** JT says "run autoresearch on [skill name]"

## Step 0: Load targets
Read `~/.openclaw/workspace/agents/autoresearch/targets.md`.
Identify the target(s) to run. For monthly sweep: process all rows with status `pending` or `active`.
For on-demand: match slug to row.

## Step 1: Load skill + checklist
Read the skill/agent file at the path in the targets.md row.
Read the checklist at the checklist path.
Confirm checklist has ≤ 6 questions. If >6: halt and alert JT — checklist needs trimming before loop runs.

## Step 2: Generate test inputs
Create 3–5 test inputs appropriate for the skill. For outreach skills: use realistic prospect profiles (niche, company name, contact name, one signal). For content skills: use realistic post prompts ("Write a Thursday LinkedIn post about Agentforce routing logic").
Save test inputs to `logs/[DATE]-[slug]-inputs.md`.

## Step 3: Baseline run
Run the skill against all test inputs. Score each output against the checklist (1 = yes, 0 = no, per question per output). Average all scores → baseline score.
Log: `[Round 0] Baseline: [score] | Failing checks: [list]`

If baseline >= 0.90: log "Already at target. No loop needed." Update targets.md status to `stable`. Stop.

## Step 4: Improvement loop
Repeat until (score >= 0.90 for 3 consecutive rounds) OR (rounds >= 20):

**4a. Analyze failures**
Look at which checklist items are failing most across all test inputs. Identify the one failing most often.

**4b. Diagnose root cause**
Read the current skill prompt carefully. Identify ONE specific rule, example, constraint, or missing instruction that plausibly explains why that checklist item keeps failing.

**4c. Mutate (smallest change first)**
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
If new score <= previous score: revert to previous skill text.

**4f. Log the round**
```
[Round N] Score: [new score] | Change: [description] | Result: kept/reverted | Reason: [why]
```

## Step 5: Save outputs

**Improved skill** (only if score improved from baseline):
Save to `[original-skill-dir]/[skill-filename]-improved-[DATE].md`
Original file is NEVER overwritten.

**Changelog** (`logs/[DATE]-[slug]-changelog.md`):
```
# Autoresearch Changelog — [slug] — [DATE]
Baseline: [score]
Final score: [score]
Rounds: [N]

## Changes kept
- Round N: [what changed] | [score before → after]

## Changes tried and reverted
- Round N: [what changed] | [why reverted]

## Recommendations
[Any changes that kept failing — surface for JT to review manually]
```

**Results summary** (`logs/[DATE]-[slug]-results.md`):
One-paragraph summary of what changed and why.

## Step 6: Update targets.md
Update the row for this slug:
- Status: `stable` (if 90%+ hit) or `active` (if max rounds hit, still improving)
- Last Score: final score
- Last Run: today's date

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
