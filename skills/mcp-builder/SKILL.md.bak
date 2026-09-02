---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Apache 2.0 (source: github.com/anthropics/skills)
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows. When building a general-purpose MCP server, keep broad coverage; when building for JT/Eve repeated operational work, prioritize the compound workflow tools agents will actually call.



**Agent-native CLI before raw MCP sprawl:**
For repeated operational workflows, first check whether an existing OpenClaw tool/skill/script can be improved or wrapped. If not, ask whether the better artifact is a local CLI/helper with compound commands, cache/mirror support, terse agent output, and explicit auth/safety gates. MCP should expose useful workflows, not just a bag of raw endpoints. If the workflow needs history, joins, diffs, drift checks, or fast repeated queries, consider a local SQLite/cache mirror and then expose the compound command through MCP if needed. Use `templates/agent-native-cli-template.md` for design.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

Start with the sitemap: `https://modelcontextprotocol.io/sitemap.xml`
Then fetch specific pages with `.md` suffix (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages: Specification overview, transport mechanisms (streamable HTTP, stdio), tool/resource/prompt definitions.

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK, broad usage, static typing) — OR Python/FastMCP for JT's stack
- **Transport**: Streamable HTTP for remote servers (stateless JSON). stdio for local servers.

**Load framework documentation:**
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Core guidelines
- **TypeScript SDK**: WebFetch `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md)
- **Python SDK**: WebFetch `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md)

#### 1.4 Plan Your Implementation

Review the service's API documentation. List endpoints to implement, starting with most common operations. Prioritize comprehensive API coverage.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure
See language-specific guides for project setup.

#### 2.2 Implement Core Infrastructure
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:
- **Input Schema**: Use Zod (TypeScript) or Pydantic (Python). Include constraints and clear descriptions.
- **Output Schema**: Define `outputSchema` where possible. Return both text and structured data.
- **Tool Description**: Concise summary, parameter descriptions, return type schema.
- **Implementation**: Async/await, proper error handling, pagination, actionable errors.
- **Annotations**: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`

---

### Phase 3: Review and Test

#### 3.1 Code Quality
- No duplicated code (DRY)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test
**TypeScript:** `npm run build` → test with `npx @modelcontextprotocol/inspector`
**Python:** `python -m py_compile your_server.py` → test with MCP Inspector

---

### Phase 4: Create Evaluations

Load [✅ Evaluation Guide](./reference/evaluation.md) for complete guidelines.

Create 10 evaluation questions. Each must be: independent, read-only, complex (multiple tool calls), realistic, verifiable (single answer), stable.

Output format:
```xml
<evaluation>
  <qa_pair>
    <question>...</question>
    <answer>single verifiable answer</answer>
  </qa_pair>
</evaluation>
```

---

# Reference Files

- [📋 MCP Best Practices](./reference/mcp_best_practices.md)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md)
- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md)
- [✅ Evaluation Guide](./reference/evaluation.md)
