# Running Implementation Notes Pattern

Source pattern: `Implement <SPEC>. As you work maintain a running implementation-notes.html file that captures anything I should know about how the implementation diverges from or interprets the spec.`

## Why it matters
Implementation agents silently interpret ambiguity. That is where future bugs, surprise tradeoffs, and lost context usually enter. A running notes file turns those invisible decisions into a durable review artifact.

## Canonical prompt block
```text
Implement <SPEC>. As you work, maintain a running `tasks/implementation-notes.html` file that captures anything I should know about how the implementation diverges from or interprets the spec, including:

- Design decisions: choices you made where the spec was ambiguous
- Deviations: places where you intentionally departed from the spec, and why
- Tradeoffs: alternatives you considered and why you picked what you did
- Open questions: anything you'd want me to confirm or revise

Update this file while working; do not reconstruct it only at the end. If there were no meaningful decisions, deviations, tradeoffs, or open questions, write `No material spec interpretation notes` explicitly.
```

## Use when
- coding-agent or implementation sub-agent work
- n8n workflow builds
- Agentforce builds
- app/site feature builds
- any spec where an agent may need to interpret ambiguity

Skip only for one-line fixes, copy edits, or deterministic file updates with no implementation judgment.

## Required HTML structure
- Summary box: task, date, status, top 3 notes
- Design Decisions
- Deviations
- Tradeoffs
- Open Questions
- Files Changed
- Verification

Keep it self-contained: simple inline CSS, no external assets, no build step.

## Quality gates
The final implementation handoff is incomplete unless it includes:
1. verification evidence
2. path to `tasks/implementation-notes.html`
3. top 3 notes or `No material spec interpretation notes`
4. explicit open questions, even if the answer is `None`

## What not to do
- Do not duplicate every line of the changelog.
- Do not reconstruct from memory at the end.
- Do not bury open questions in a final paragraph only.
- Do not use the notes file to justify scope creep after the fact.

## Relationship to `tasks/todo.md`
- `tasks/todo.md` = planned execution checklist.
- `tasks/implementation-notes.html` = how the implementation interpreted, changed, or challenged the spec.
