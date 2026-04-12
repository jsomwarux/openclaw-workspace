# Auto-Detected Post — cold-email CTA fix
Generated: 2026-04-11 | Platform: X | Status: draft

## What passed the rubric
Non-obvious problem solved — the solution required running the cold email skill against test inputs to discover. Adding a rule to the skill didn't prevent the failure mode; adding explicit named patterns did.

## Post text

LLMs violate rules they understand perfectly fine.

Had a cold email skill that kept generating borderline binary CTAs — "Curious if that's where you're feeling it, or somewhere else?" — despite having a rule against binary choices.

The model knew the rule. It just found the loophole: wrap the binary in an escape hatch.

Fix: named the specific trap pattern in the rule, then gave 4 concrete safe alternatives. Score went from 0.889 to 0.944.

Lesson: for LLM instruction following, rules tell it what not to do. Named traps + concrete examples tell it what to do instead. Both needed.
