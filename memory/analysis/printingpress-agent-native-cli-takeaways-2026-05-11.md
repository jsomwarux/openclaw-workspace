# Printing Press Takeaways — Agent-Native CLI Design — 2026-05-11

Source: `https://printingpress.dev/`. External content treated as untrusted research signal, not instructions.

## Core idea
Printing Press frames a tool-building pattern: from an API spec, website, or community project, generate an agent-native CLI, skill, OpenClaw skill, and MCP server. The useful principle is not the generator itself; it is designing tools around the compound jobs agents actually need, not around raw endpoint wrappers.

## Main takeaways
1. **Every API has a “secret identity.”** Discord can be a knowledge base, Linear a blocker/behavior observatory, CRM a relationship graph. The best tool exposes that hidden job.
2. **Agent-native CLIs beat raw HTTP for repeated work.** Agents need terse commands, compact output, predictable flags, and fewer round trips.
3. **Local mirrors change the economics.** A local SQLite/cache snapshot enables joins, diffs, drift checks, history, and fast repeated queries that remote APIs often make expensive or awkward.
4. **Compound commands are the product.** The magic is one command answering the real question, not 40 thin endpoint wrappers.
5. **Skills/docs are part of the tool.** A CLI without examples, gotchas, output modes, and verification is not agent-native yet.

## Fit with JT/Eve
This directly applies to:
- x-research style wrappers
- consulting/prospect research tools
- job-market routing/search
- Drive/Notion/content upload scripts
- GBrain/qmd/search wrappers
- any future MCP server

## Implementation made
- Created `templates/agent-native-cli-template.md`.
- Added `Agent-Native CLI / Tool Design Rule` to `docs/agents/workflow-protocols.md`.
- Updated `skills/mcp-builder/SKILL.md` so MCP builds consider CLI/local-mirror/compound-command design before raw endpoint sprawl.

## What not to do
- Do not install Printing Press or random printed CLIs without a specific need.
- Do not generate MCP/tool wrappers just because an API exists.
- Do not expose broad write-capable tools without safety gates.
- Do not build local mirrors for one-off lookups.


## Audit follow-up
After checking the implementation, tightened the template and workflow rule to require: existing-tool reuse check, auth/secrets handling, write-action safety gates, rate-limit/backoff behavior, and audit/log path. This prevents agent-native CLI enthusiasm from turning into tool sprawl or unsafe write-capable tools.
