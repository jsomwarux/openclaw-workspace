# Python MCP Server Implementation Guide

## Quick Reference

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
import httpx

mcp = FastMCP("service_mcp")
```

## Server Naming
Format: `{service}_mcp` — e.g., `slack_mcp`, `hubspot_mcp`

## Tool Registration Pattern

```python
@mcp.tool(
    name="service_tool_name",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def service_tool_name(params: InputModel) -> str:
    """Tool description — becomes the 'description' field automatically."""
    pass
```

## Pydantic v2 Input Models

```python
class SearchInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    query: str = Field(..., description="Search query", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, ge=1, le=100)
    offset: Optional[int] = Field(default=0, ge=0)

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
```

## Response Formats

Support both JSON and Markdown:
```python
from enum import Enum

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
```

## Pagination Response

```python
response = {
    "total": data["total"],
    "count": len(items),
    "offset": params.offset,
    "items": items,
    "has_more": data["total"] > params.offset + len(items),
    "next_offset": params.offset + len(items) if has_more else None
}
```

## Error Handling

```python
def _handle_api_error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "Error: Resource not found. Check the ID is correct."
        elif e.response.status_code == 403:
            return "Error: Permission denied."
        elif e.response.status_code == 429:
            return "Error: Rate limit exceeded. Please wait."
        return f"Error: API request failed with status {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    return f"Error: Unexpected error: {type(e).__name__}"
```

## Shared API Client

```python
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## FastMCP + Consulting Note

For consulting Cowork plugins using FastMCP 3.0:
- Use `LocalProvider` for function-decorated tools
- Use `OpenAPIProvider` to wrap existing client REST APIs instantly
- Auth middleware goes in the FastMCP middleware chain, not in individual tools
- Per-client tool visibility: apply Transforms at the session level
