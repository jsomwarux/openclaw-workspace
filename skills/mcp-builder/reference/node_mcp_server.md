# Node/TypeScript MCP Server Implementation Guide

## Quick Reference

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const server = new McpServer({ name: "service-mcp-server", version: "1.0.0" });
```

## Server Naming
Format: `{service}-mcp-server` — e.g., `slack-mcp-server`, `hubspot-mcp-server`

## IMPORTANT: Use Modern APIs Only
- ✅ DO use: `server.registerTool()`, `server.registerResource()`, `server.registerPrompt()`
- ❌ DO NOT use: `server.tool()`, `server.setRequestHandler()`, manual handler registration

## Project Structure

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # McpServer init + transport
│   ├── types.ts          # TypeScript interfaces
│   ├── tools/            # Tool implementations
│   ├── services/         # API clients
│   ├── schemas/          # Zod schemas
│   └── constants.ts      # API_URL, CHARACTER_LIMIT, etc.
└── dist/                 # Built output (entry: dist/index.js)
```

## Tool Registration Pattern

```typescript
const SearchSchema = z.object({
    query: z.string().min(2).max(200).describe("Search query"),
    limit: z.number().int().min(1).max(100).default(20),
    offset: z.number().int().min(0).default(0)
}).strict();

server.registerTool(
    "service_search_items",
    {
        title: "Search Items",
        description: "Search for items. Use when...",
        inputSchema: SearchSchema,
        annotations: {
            readOnlyHint: true,
            destructiveHint: false,
            idempotentHint: true,
            openWorldHint: true
        }
    },
    async (params) => {
        try {
            const output = await fetchResults(params);
            return {
                content: [{ type: "text", text: JSON.stringify(output, null, 2) }],
                structuredContent: output
            };
        } catch (error) {
            return { content: [{ type: "text", text: handleApiError(error) }] };
        }
    }
);
```

## Error Handling

```typescript
function handleApiError(error: unknown): string {
    if (error instanceof AxiosError) {
        switch (error.response?.status) {
            case 404: return "Error: Resource not found. Check the ID.";
            case 403: return "Error: Permission denied.";
            case 429: return "Error: Rate limit exceeded. Wait and retry.";
        }
    }
    return `Error: ${error instanceof Error ? error.message : String(error)}`;
}
```

## Character Limit (prevent overwhelming responses)

```typescript
export const CHARACTER_LIMIT = 25000;

if (result.length > CHARACTER_LIMIT) {
    response.truncated = true;
    response.truncation_message = `Truncated. Use offset/filters to page.`;
}
```
