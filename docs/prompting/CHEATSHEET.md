# Eve's Prompting Cheat Sheet
*Quick reference for writing system prompts, SOUL.md, HEARTBEAT.md, cron instructions, and any prompt that Claude reads*
*Based on: Anthropic official docs for Claude Opus 4.6 / Sonnet 4.6*

---

## The 10-Second Rules

1. **Explicit > implicit** — Say what you want. Claude won't infer "go above and beyond."
2. **Context + reason > bare instruction** — Tell Claude *why*, it generalizes better.
3. **XML tags for structure** — `<instructions>`, `<context>`, `<example>`, `<output_format>`
4. **Examples beat description** — Show, don't just tell. 3–5 examples = dramatically better output.
5. **Tell what to DO, not what NOT to do** — "Write in prose" beats "Don't use bullets."
6. **Remove anti-laziness language** — "Be thorough / think carefully / don't be lazy" → delete it. 4.6 is already proactive; these prompts cause runaway behavior.
7. **Soften tool-use language** — "Use this tool when..." not "ALWAYS use / CRITICAL: MUST use..."
8. **No think-tool instructions** — Don't tell 4.6 to "use the think tool" — it thinks fine on its own.

---

## Model Behavior by Default (Know Before You Prompt)

| Behavior | Sonnet 4.6 | Opus 4.6 |
|---|---|---|
| Thinking | Adaptive (high effort default) | Adaptive |
| Subagent spawning | Moderate | Aggressive (may over-spawn) |
| Upfront exploration | High | Very high |
| Overeagerness/overengineering | Moderate | High — needs guardrails |
| Tool responsiveness | Responsive | Very responsive |
| Autonomy (risky actions) | Moderate | High — needs safety guardrails |

---

## Copy-Paste Snippets

### Make Claude take action by default
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. Infer the most useful
likely action and proceed, using tools to discover missing details instead of guessing.
</default_to_action>
```

### Prevent overengineering (use with Opus 4.6)
```xml
<no_overengineering>
Only make changes that are directly requested or clearly necessary. Don't add features,
refactor surrounding code, add docstrings to unchanged code, or create abstractions for
one-time operations. Keep solutions minimal and focused.
</no_overengineering>
```

### Prevent risky autonomous actions (Opus 4.6 agentic use)
```xml
<safety>
Consider reversibility before acting. Take local, reversible actions freely (edit files,
run tests). For hard-to-reverse actions (delete, force push, post externally, drop tables),
ask the user before proceeding.
</safety>
```

### Prevent overuse of subagents (Opus 4.6)
```xml
<subagent_guidance>
Use subagents for parallel workstreams requiring isolated context. For simple tasks,
sequential operations, or tasks requiring shared state, work directly without delegating.
</subagent_guidance>
```

### Minimal markdown output
```xml
<avoid_excessive_markdown_and_bullet_points>
Write in clear, flowing prose using complete paragraphs. Reserve markdown for `inline code`
and code blocks only. Do not use ordered or unordered lists unless presenting truly discrete
items. Incorporate points naturally into sentences.
</avoid_excessive_markdown_and_bullet_points>
```

### Parallel tool calls (max efficiency)
```xml
<use_parallel_tool_calls>
If calling multiple tools with no dependencies between them, make all calls in parallel.
Never use placeholders or guess parameters. Only call sequentially when results depend on
previous calls.
</use_parallel_tool_calls>
```

### Research mode
```
Search for this information in a structured way. Develop competing hypotheses as you gather
data. Track confidence levels. Regularly self-critique your approach. Break down the research
task systematically and update a notes file to persist findings.
```

### Prevent hallucination in code tasks
```xml
<investigate_before_answering>
Never speculate about code you have not read. If the user references a specific file,
read it before answering. Never make claims about code without investigating first.
</investigate_before_answering>
```

### Prevent runaway thinking / slow responses
```
Prioritize execution over deliberation. Choose one approach and begin immediately.
Do not compare alternatives or plan the full solution before starting. Write each piece
once. If uncertain, make a reasonable choice and continue.
```

---

## When Writing System Prompts / Markdown Instructions

Checklist before saving:
- [ ] Is every desired behavior stated explicitly (not assumed)?
- [ ] Does each instruction include context/reason for *why*?
- [ ] Are complex multi-part instructions wrapped in XML tags?
- [ ] Are there examples showing desired output format?
- [ ] Are there any anti-laziness phrases to remove? ("be thorough", "think carefully", "don't be lazy")
- [ ] Is tool-use language appropriately calm ("use X when..." not "MUST/CRITICAL/ALWAYS")?
- [ ] Does the formatting style of the prompt match desired output style?
- [ ] For Opus 4.6 instructions: are safety/autonomy guardrails included?
- [ ] Is the instruction telling Claude what to DO (not just what NOT to do)?

---

## Full Docs (Local)
- `docs/prompting/claude-4-best-practices.md` — Full Anthropic guide for Claude 4.6
- `docs/prompting/techniques.md` — Core techniques: clarity, XML, multishot, CoT, system prompts
- `docs/prompting/CHEATSHEET.md` — This file

*Source docs at: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/*
