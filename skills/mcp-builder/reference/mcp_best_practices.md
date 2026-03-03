# MCP Server Best Practices

## Quick Reference

### Server Naming
- **Python**: `{service}_mcp` (e.g., `slack_mcp`)
- **Node/TypeScript**: `{service}-mcp-server` (e.g., `slack-mcp-server`)

### Tool Naming
- Use snake_case with service prefix
- Format: `{service}_{action}_{resource}`
- Example: `slack_send_message`, `github_create_issue`

### Response Formats
- Support both JSON and Markdown formats
- JSON for programmatic processing
- Markdown for human readability

### Pagination
- Always respect `limit` parameter
- Return `has_more`, `next_offset`, `total_count`
- Default to 20-50 items

### Transport
- **Streamable HTTP**: For remote servers, multi-client scenarios
- **stdio**: For local integrations, command-line tools
- Avoid SSE (deprecated in favor of streamable HTTP)

---

## Tool Design

- Tool descriptions must narrowly and unambiguously describe functionality
- Provide tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
- Keep tool operations focused and atomic

### Tool Annotations

| Annotation | Default | Description |
|---|---|---|
| `readOnlyHint` | false | Tool does not modify its environment |
| `destructiveHint` | true | Tool may perform destructive updates |
| `idempotentHint` | false | Repeated calls with same args have no additional effect |
| `openWorldHint` | true | Tool interacts with external entities |

---

## Pagination

```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## Security Best Practices

- Store API keys in environment variables, never in code
- Sanitize file paths to prevent directory traversal
- Validate URLs and external identifiers
- Use schema validation (Pydantic/Zod) for all inputs
- Don't expose internal errors to clients
- For streamable HTTP: validate `Origin` header, bind to `127.0.0.1`

---

## Error Handling

- Use standard JSON-RPC error codes
- Report tool errors within result objects (not protocol-level errors)
- Provide helpful, specific error messages with suggested next steps

```typescript
try {
  const result = performOperation();
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  return {
    isError: true,
    content: [{ type: "text", text: `Error: ${error.message}. Try using filter='active_only'.` }]
  };
}
```
