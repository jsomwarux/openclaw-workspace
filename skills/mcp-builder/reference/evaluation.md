# MCP Server Evaluation Guide

## Overview

Create 10 evaluation questions to test whether an LLM can effectively use your MCP server. Quality = how well the server enables real-world task completion.

## Requirements

- **Independent**: Each question stands alone
- **Read-only**: No destructive operations required
- **Complex**: Requires multiple (potentially dozens of) tool calls
- **Realistic**: Based on real human use cases
- **Verifiable**: Single, clear answer via direct string comparison
- **Stable**: Answer won't change over time

## Output Format

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
</evaluation>
```

## Question Design Guidelines

1. Require multi-hop reasoning (information from step A needed for step B)
2. Don't use specific keywords from the target content — use synonyms
3. May require paging through many results
4. Stress-test tools that return large JSON objects
5. Include ambiguous questions where there's still ONE verifiable answer
6. Specify output format in the question if needed: "Use YYYY/MM/DD", "Answer True or False"

## Answer Guidelines

- Single verifiable value: user ID, name, timestamp, boolean, count, URL, email
- Human-readable preferred over opaque IDs
- Must be stable — don't ask about current counts or live state
- Verified via direct string comparison — no complex structures
