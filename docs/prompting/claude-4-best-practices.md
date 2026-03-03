# Claude 4.6 Prompting Best Practices
*Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices*
*Fetched: 2026-02-21 | Applies to: Claude Opus 4.6, Claude Sonnet 4.6, Claude Haiku 4.5*

---

## General Principles

### 1. Be Explicit — Don't Rely on Inference

Claude 4.6 follows instructions precisely. If you want "above and beyond" behavior, ask for it explicitly.

**Less effective:**
```
Create an analytics dashboard
```
**More effective:**
```
Create an analytics dashboard. Include as many relevant features and interactions as possible.
Go beyond the basics to create a fully-featured implementation.
```

### 2. Add Context / Motivation Behind Instructions

Explaining *why* helps Claude generalize correctly.

**Less effective:**
```
NEVER use ellipses
```
**More effective:**
```
Your response will be read aloud by a text-to-speech engine, so never use ellipses
since the TTS engine won't know how to pronounce them.
```

### 3. Watch Your Examples Carefully

Claude pays close attention to examples. Make sure they demonstrate exactly what you want — including edge cases.

### 4. Long-Horizon Reasoning & State Tracking

Claude 4.6 excels at multi-step tasks across extended sessions. Key patterns:

- **Incremental progress**: Focus on a few things at a time, not everything at once
- **Structured state files**: Use JSON for test status, task queues, etc.
- **Unstructured progress notes**: Free-form text for general context
- **Git for state**: Claude 4.6 works especially well using git to track progress
- **Tests first**: Write tests before implementing; remind Claude "do not remove tests"

**Context compaction prompt** (if your harness auto-compacts):
```
Your context window will be automatically compacted as it approaches its limit, allowing
you to continue working indefinitely from where you left off. Therefore, do not stop tasks
early due to token budget concerns. As you approach your token budget limit, save your
current progress and state to memory before the context window refreshes. Always be as
persistent and autonomous as possible and complete tasks fully.
```

**Multi-window workflow tips:**
1. First window: set up framework (write tests, create setup scripts)
2. Future windows: iterate on a todo list
3. Start fresh windows by reading: `progress.txt`, `tests.json`, git logs
4. Run integration tests before new features

**State data best practices:**
```json
// tests.json — structured
{
  "tests": [
    {"id": 1, "name": "auth_flow", "status": "passing"},
    {"id": 2, "name": "user_mgmt", "status": "failing"}
  ],
  "total": 200, "passing": 150, "failing": 25
}
```
```
// progress.txt — unstructured
Session 3: Fixed auth token validation. Next: investigate user_mgmt failures.
Do not remove tests — could cause missing functionality.
```

### 5. Communication Style (What Changed in 4.6)

Claude 4.6 is more concise and direct than 4.5:
- Skips detailed summaries unless asked
- Gives fact-based progress reports, not celebratory ones
- Jumps to next action after tool use without narrating it

If you want updates between steps, add: `"After completing a task involving tool use, provide a quick summary."`

---

## Specific Guidance by Situation

### Tool Usage — Be Direct

Claude 4.6 follows instructions precisely. "Can you suggest..." = will suggest, not implement.

**For action:**
```
Change this function to improve its performance.
```
**For suggestions only:**
```
Can you suggest some changes to improve this function?
```

**To make Claude proactive by default** (system prompt):
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is
unclear, infer the most useful likely action and proceed, using tools to discover any
missing details instead of guessing.
</default_to_action>
```

**To make Claude conservative by default:**
```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed. When intent
is ambiguous, default to providing information and recommendations rather than action.
</do_not_act_before_instructions>
```

### Tool Triggering — Dial Back Aggressive Language

Claude 4.6 overtriggers on aggressive instructions. Replace:
- ❌ `"CRITICAL: You MUST use this tool when..."`
- ✅ `"Use this tool when..."`

### Autonomy & Safety (Especially Opus 4.6)

Opus 4.6 may take hard-to-reverse actions. Add to system prompt if needed:
```
Consider the reversibility and potential impact of your actions. You are encouraged to
take local, reversible actions like editing files or running tests, but for actions that
are hard to reverse, affect shared systems, or could be destructive, ask the user before
proceeding.

Examples requiring confirmation:
- Destructive: deleting files or branches, dropping tables, rm -rf
- Hard to reverse: git push --force, git reset --hard, amending published commits
- Visible to others: pushing code, commenting on PRs, sending messages
```

### Overthinking / Excessive Exploration

Claude 4.6 does much more upfront exploration than 4.5. To rein it in:
- **Remove anti-laziness prompts**: "be thorough," "think carefully," "do not be lazy" → remove these; they amplify already-proactive behavior and cause runaway thinking
- **Soften tool language**: `"You must use [tool]"` → `"Use [tool] when it would enhance understanding"`
- **Remove explicit think-tool instructions**: Claude 4.6 thinks effectively without being told to
- **Use effort parameter**: Lower effort = less thinking, less token usage

**If you want faster, less deliberate output:**
```
Prioritize execution over deliberation. Choose one approach and start producing output
immediately. Do not compare alternatives or plan the entire solution before writing.
Write each piece of work once; do not go back to revise or rewrite. If uncertain about
a detail, make a reasonable choice and continue.
```

### Formatting Control

Best practices (in order of effectiveness):

1. **Tell Claude what to do, not what NOT to do**
   - ❌ `"Do not use markdown"`
   - ✅ `"Write your response in smoothly flowing prose paragraphs."`

2. **Use XML format indicators**
   - `"Write the prose sections in <smoothly_flowing_prose_paragraphs> tags."`

3. **Match prompt style to desired output style** — markdown in prompts = markdown in output

4. **For minimal markdown** (system prompt):
```xml
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, or long-form content, write in
clear, flowing prose using complete paragraphs. Reserve markdown for `inline code`,
code blocks, and simple headings (##, ###). Avoid **bold** and *italics*.

DO NOT use ordered lists or unordered lists unless presenting truly discrete items
or the user explicitly requests a list. Incorporate items naturally into sentences.
</avoid_excessive_markdown_and_bullet_points>
```

### Subagent Orchestration

Opus 4.6 spawns subagents aggressively — even for simple tasks. Control it:
```
Use subagents when tasks can run in parallel, require isolated context, or involve
independent workstreams. For simple tasks, sequential operations, single-file edits,
or tasks where you need to maintain context across steps, work directly.
```

### Research

Claude 4.6 has strong agentic search. For complex research:
```
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track confidence levels in your progress notes. Regularly
self-critique your approach. Update a hypothesis tree or notes file to persist
information and provide transparency.
```

### Parallel Tool Calls

Claude 4.6 excels at parallel execution. To maximize it:
```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between them, make all
independent tool calls in parallel. Maximize use of parallel tool calls where possible.
Never use placeholders or guess missing parameters — only call tools sequentially when
results depend on previous calls.
</use_parallel_tool_calls>
```

### Prevent Overengineering (Especially Opus 4.6)

Opus 4.6 adds abstractions, extra files, and flexibility you didn't ask for:
```
Avoid over-engineering. Only make changes that are directly requested or clearly necessary.

- Scope: Don't add features or make "improvements" beyond what was asked.
- Documentation: Don't add docstrings or comments to code you didn't change.
- Defensive coding: Don't add error handling for scenarios that can't happen.
- Abstractions: Don't create helpers for one-time operations.
```

### Reducing Hallucinations in Code
```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Investigate and read relevant files BEFORE
answering questions. Never make claims about code before investigating.
</investigate_before_answering>
```

### Thinking Configuration

- **Opus 4.6**: Uses adaptive thinking (`thinking: {type: "adaptive"}`) — calibrates automatically
- **Sonnet 4.6**: Supports adaptive thinking AND manual extended thinking with interleaved mode
- **Effort parameter**: Controls thinking depth — `high`, `medium`, `low`
- **Default Sonnet 4.6 effort**: `high` (higher latency than 4.5 if not explicitly set)

**Recommended Sonnet 4.6 effort:**
- `medium` for most applications
- `low` for high-volume or latency-sensitive workloads
- Set `max_tokens: 64000` at medium/high effort

**Prompting adaptive thinking behavior:**
```
After receiving tool results, carefully reflect on their quality and determine optimal
next steps before proceeding. Use your thinking to plan and iterate based on this new
information, then take the best next action.
```

**If thinking triggers too much:**
```
Extended thinking adds latency and should only be used when it will meaningfully improve
answer quality — typically for multi-step reasoning problems. When in doubt, respond
directly.
```

### Prefilled Responses — DEPRECATED in 4.6

Prefills on the last assistant turn are no longer supported in 4.6.

**Migration patterns:**
- Output format: Use structured outputs or explicit system prompt instructions ("Respond directly without preamble.")
- Continuations: Move to user message: "Your previous response was interrupted and ended with `[text]`. Continue from where you left off."
- Context hydration: Inject into user turn for long conversations

---

## Migration Checklist: From 4.5 → 4.6

- [ ] Remove anti-laziness prompts ("be thorough", "think carefully", "don't be lazy")
- [ ] Soften tool-use language (remove "MUST", "CRITICAL", "always")
- [ ] Remove explicit think-tool instructions
- [ ] Replace `thinking: {type: "enabled", budget_tokens: N}` with adaptive thinking + effort parameter
- [ ] Remove or migrate any prefilled assistant turns
- [ ] Add explicit instructions for behaviors you want (don't rely on inference)
- [ ] Add autonomy/safety guardrails if using Opus 4.6 in agentic settings
- [ ] Set explicit effort level for Sonnet 4.6 (default `high` adds latency)

---

## Sonnet 4.6 vs. Opus 4.6 — When to Use Each

| Scenario | Model |
|---|---|
| Most chat, content gen, search, classification | Sonnet 4.6 (medium/low effort) |
| Agentic coding, multi-step tool use | Sonnet 4.6 (adaptive, medium/high effort) |
| Large-scale code migrations | Opus 4.6 |
| Deep research, extended autonomous work | Opus 4.6 |
| Computer use agents | Sonnet 4.6 (adaptive, best-in-class accuracy) |
| Hardest long-horizon problems | Opus 4.6 |
