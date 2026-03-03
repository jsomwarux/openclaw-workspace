# Claude Prompting Techniques
*Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/*
*Fetched: 2026-02-21 | Applies to: All Claude models (4.6 specific notes in best-practices.md)*

---

## 1. Be Clear, Direct, and Detailed

Think of Claude as a brilliant new employee with amnesia — no implicit context, no assumed norms.

**The golden rule**: Show your prompt to a colleague with minimal context. If they're confused, Claude will be too.

### How to be clear

- **Give contextual information**: What will the output be used for? Who is the audience? Where does this fit in a larger workflow?
- **Be specific about output**: If you want only code, say "output only code and nothing else."
- **Use sequential steps**: Numbered lists for multi-part instructions outperform prose paragraphs

### Examples

**Vague:**
```
Analyze this outage report and summarize key points.
```

**Specific:**
```
Analyze this AcmeCloud outage report. Skip the preamble. Keep your response terse —
bare bones necessary information only. List:
1) Cause
2) Duration
3) Impacted services
4) Number of affected users
5) Estimated revenue loss
```

---

## 2. XML Tags for Structure

When prompts have multiple components (context, instructions, examples, data), XML tags prevent Claude from mixing them up.

### Why XML tags work

- **Clarity**: Clearly separate context, instructions, and data
- **Accuracy**: Reduces misinterpretation of prompt sections
- **Parseability**: Tagged output is easier to post-process
- **Flexibility**: Easy to add/modify sections without rewriting everything

### Best practices

- **Be consistent**: Use the same tag names throughout; reference them by name ("Using the contract in `<contract>` tags...")
- **Nest for hierarchy**: `<outer><inner></inner></outer>`
- **Combine with other techniques**: XML + multishot + chain of thought = powerful

### Common tag patterns

```xml
<context>
Background information Claude needs to understand the task.
</context>

<instructions>
1. Step one
2. Step two
</instructions>

<data>
{{INPUT_DATA}}
</data>

<formatting_example>
{{EXAMPLE_OUTPUT}}
</formatting_example>

<findings>
(Claude writes here)
</findings>

<recommendations>
(Claude writes here)
</recommendations>
```

### Example: Without vs. with XML

**Without XML** (Claude may confuse example with instructions):
```
Generate a Q2 financial report like this example from last year: {{Q1_REPORT}}.
Use data from this spreadsheet: {{SPREADSHEET_DATA}}.
The report should be concise and professional.
```

**With XML** (Claude parses cleanly):
```xml
Generate a Q2 financial report for our investors.

<data>{{SPREADSHEET_DATA}}</data>

<instructions>
1. Include sections: Revenue Growth, Profit Margins, Cash Flow.
2. Highlight strengths and areas for improvement.
</instructions>

<formatting_example>{{Q1_REPORT}}</formatting_example>

Make your tone concise and professional.
```

---

## 3. Multishot Prompting (Examples)

Examples are the fastest way to get Claude to produce exactly the format and style you want.

**Rule of thumb**: 3–5 diverse, relevant examples dramatically improve accuracy, consistency, and format adherence.

### Why examples work

- **Accuracy**: Reduces misinterpretation of abstract instructions
- **Consistency**: Enforces uniform structure across outputs
- **Performance**: Especially effective for complex tasks and structured output

### Crafting effective examples

- **Relevant**: Mirror your actual use case
- **Diverse**: Cover edge cases and variations — avoid patterns Claude might over-index on
- **Wrapped in `<example>` tags**: For multiple examples, nest in `<examples>`

```xml
<examples>
  <example>
    Input: The new dashboard is slow and I can't find the export button. Fix ASAP!
    Category: UI/UX, Performance
    Sentiment: Negative
    Priority: High
  </example>
  <example>
    Input: Love the Salesforce integration! Can you add Hubspot too?
    Category: Integration, Feature Request
    Sentiment: Positive
    Priority: Medium
  </example>
</examples>
```

### Power tip

Ask Claude to evaluate or generate additional examples:
- "Evaluate these examples for relevance and diversity"
- "Generate 3 more examples based on this initial set"

---

## 4. Chain of Thought (Let Claude Think)

For complex reasoning tasks, ask Claude to think through problems step by step before answering.

### When to use

- Math, logic, or multi-step reasoning
- Tasks where accuracy matters more than speed
- Problems requiring the model to eliminate wrong answers before committing

### How to trigger it

- **Simple**: "Think step by step before answering."
- **Structured**: Ask Claude to show reasoning in `<thinking>` tags, then final answer in `<answer>` tags
- **Automatic in 4.6**: Adaptive thinking handles this automatically for complex queries — don't over-prompt

```xml
Think through this step by step in <thinking> tags, then provide your final answer
in <answer> tags.
```

> **4.6 note**: Don't tell Claude to "use the think tool" or "think carefully" — 4.6 models
> think effectively without being told. Over-prompting this causes runaway reasoning.

---

## 5. System Prompts — Give Claude a Role

System prompts establish persistent context, persona, tone, and constraints for a session.

### Best for

- Establishing a persona or role ("You are a financial analyst at AcmeCorp...")
- Setting output constraints that apply to every response
- Defining tools available and when to use them
- Configuring Claude's default behavior (action vs. suggestion, verbose vs. terse)

### Tips

- Put role/persona first, constraints after
- Use XML tags within system prompts for complex, multi-part instructions
- Match formatting style of system prompt to desired output style

---

## 6. Chaining Complex Prompts

For long, multi-step tasks, break them into sequential prompt chains where each step's output feeds the next.

### When to chain

- Multi-stage workflows (research → draft → review → format)
- Tasks too long for a single context window
- Situations where you need to verify intermediate outputs

### Pattern

```
Step 1: Research → output saved to research.md
Step 2: Draft based on research.md → output saved to draft.md
Step 3: Review draft.md for accuracy → output saved to final.md
```

---

## 7. Long Context Tips

When feeding large documents (code, reports, books):

- Put the document in `<document>` tags with clear label
- Put your instructions **after** the document, not before — Claude attends better to instructions at the end of long contexts
- Use `<excerpt>` tags if referencing specific sections
- For code: provide full file in `<file>` tags, specify filename in attributes

```xml
<document name="quarterly_report.pdf">
{{DOCUMENT_CONTENT}}
</document>

Based on the document above, answer these specific questions:
1. ...
2. ...
```

---

## Quick Reference: What to Use When

| Situation | Technique |
|---|---|
| Output format not matching expectations | XML tags + formatting example |
| Claude misunderstands the task | Add context/motivation, sequential steps |
| Inconsistent output across runs | Multishot examples (3–5) |
| Complex reasoning errors | Chain of thought (`<thinking>` tags) |
| Persistent behavior across turns | System prompt |
| Long document analysis | Long context tips (instructions after doc) |
| Multi-stage tasks | Prompt chaining |
| Claude making unexpected choices | Explicit step-by-step instructions |
