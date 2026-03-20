# Autoresearch Runner — Build Plan
*Created: 2026-03-19 | Source: Karpathy autoresearch method (via aisolo.beehiiv.com)*

## What It Does
Autonomous skill self-improvement loop. Runs a skill against test inputs, scores each output against a yes/no checklist, makes one targeted change to the skill prompt, keeps the change if score goes up, reverts if it doesn't. Repeats until score hits 95%+ three times in a row (or max rounds reached).

## First Target: cold-email/SKILL.md
Highest value. Runs every night. Direct revenue impact. Checklist is half-written already from existing rules.

## Scoring Checklist (6 questions max — overfitting risk above this)

For cold-email/SKILL.md Message 1:
1. Is the message under 100 words?
2. Does the opener reference something specific to the INDIVIDUAL (not just the company or niche)?
3. Is there no signature block in Message 1?
4. Does the message contain no "I built X" claim in Message 1?
5. Does the closing question avoid a binary choice structure ("still manual or have you built something?")?
6. Is the opener format different from the previous message in the batch (rotation check)?

## Agent Spec (AGENT.md)

### Inputs
- `skill_path`: path to SKILL.md to optimize (default: cold-email/SKILL.md)
- `test_inputs`: 3-5 sample prospect profiles (niche, company name, contact name, one signal)
- `checklist`: the 6 yes/no scoring questions above
- `max_rounds`: default 20
- `target_score`: default 0.90 (90%)

### Loop
1. Load current SKILL.md
2. For each test input: run the skill (Claude generation), score output against checklist (0/1 per question), average across all test inputs → score for this round
3. If score >= target for 3 consecutive rounds → STOP, save improved version
4. If score < target: analyze which checklist items are failing most often → identify ONE specific rule in SKILL.md that plausibly caused those failures → make the smallest possible change (add a rule, tighten a constraint, add a banned phrase, add a worked example)
5. Re-run → score again. If new score > old score: keep change. If not: revert.
6. Repeat from step 3.

### Mutation types (in order of preference — try simpler mutations first)
1. Add a banned phrase or word to an existing list
2. Tighten a constraint (change "under 150 words" to "under 100 words")
3. Add a specific rule for the most common failure
4. Add a worked example showing what good looks like
5. Remove a rule that may be causing unintended side effects

### Outputs
- `skills/cold-email/SKILL-improved-[DATE].md` — improved version (original untouched)
- `agents/autoresearch/logs/[DATE]-changelog.md` — every round: score, change tried, kept/reverted, reason
- `agents/autoresearch/logs/[DATE]-results.md` — baseline → final score, summary of changes kept

### Cost guardrails
- Max 20 rounds per run
- Max 5 test inputs per round
- Estimated cost: ~$0.10-0.20 per full run (text generation only, no web searches)
- Hard stop if cost estimate exceeds $0.50

## Invocation
- **On-demand:** overnight agent can invoke when no higher-priority tasks exist
- **Monthly:** could wire as a monthly cron (1st of month, after niche fitness review)
- **Manual:** JT says "run autoresearch on cold-email skill"

## All targets (priority order)

### Target 1: cold-email/SKILL.md (first — prove the loop)
Checklist: under 100 words | individual signal present | no signature block | no "I built X" | no binary close | opener rotated

### Target 2: agents/t3-cold-hook/AGENT.md (same pattern, swap checklist)
Checklist: under 75 words | references prospect's specific niche/role signal | no pitch in M1 | niche-correct stack (Agentforce for Salesforce shops, n8n for others) | closing question is open-ended (not binary) | no filler opener

### Target 3: content-generate-linkedin cron (slop score already written)
Checklist: no em dashes | no contrarian flip more than once | opener names reader's problem (not build name) | no vague declarative | no adverbs | slop score ≥ 35/50

### Target 4: content-generate-x cron (after LinkedIn validated)
Checklist: first line is the point (no warmup) | no hashtags | no links in body | debate hook test (specific enough only an implementer wrote it) | no em dashes | ends on capability proof for build-showcase posts

## File structure
```
agents/autoresearch/
├── AGENT.md          ← full loop logic + scoring
├── state.json        ← last run date, last score per skill
├── checklists/
│   └── cold-email.md ← the 6 yes/no questions
└── logs/
    └── [DATE]-changelog.md
```

## Key constraint from original method
Checklist must stay ≤ 6 questions. More = the agent starts gaming the checklist (optimizes for passing the test rather than actually improving). Each question must be a clean yes/no — no scoring rubrics, no 1-10 scales.

## Build order
1. Write AGENT.md with full loop logic (shared across all targets — skill path + checklist are inputs)
2. Write checklists/cold-email.md (6 questions)
3. Run one test on cold-email (10 rounds max) — validate the loop works, review changelog
4. Write checklists/t3-cold-hook.md + test
5. Write checklists/linkedin.md + test (slop score already done, just formalize)
6. Write checklists/x-posts.md + test
7. Wire to overnight agent as on-demand invocation for all 4 targets
8. After all 4 validated: consider monthly cron (1st of month, after niche fitness review)
