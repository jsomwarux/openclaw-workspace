# Production AI Architecture Checklist

Use for AI implementation diagnostics, AgentGuard positioning, and non-trivial client AI builds with repeated use, sensitive data, external actions, or operational risk. Skip for tiny/internal prototypes. The goal is to prevent “one agent + one prompt” demos from being mistaken for production systems without forcing every workflow into architecture theater.

## Workflow / product context
- Workflow being automated or augmented:
- User / operator:
- Business decision or action affected:
- Read-only, draft-only, or write/action-capable:

## Core layers
### 1. Retrieval / RAG
- Sources:
- Freshness rule:
- Chunking/indexing approach:
- Source citation requirement:

### 2. Query rewriting / decomposition
- Does the system rewrite vague user requests?
- Does it decompose complex tasks into sub-questions?
- How are rewritten queries logged/debugged?

### 3. Routing
- What decides which path/tool/agent runs?
- Deterministic route vs model judgment:
- Fallback route:

### 4. Memory / context
- Session memory:
- Durable/project memory:
- What must never be remembered:
- Drift/conflict handling:

### 5. Semantic cache / reuse
- What repeated queries/results should be cached?
- Cache invalidation/freshness rule:
- Cost/latency target:

### 6. Specialist agents/tools
- Retrieval specialist:
- Structured data/API specialist:
- Drafting/summarization specialist:
- Checker/judge specialist:
- Human handoff path:

### 7. Evaluation / judge layer
- Golden dataset or known-good cases:
- Offline eval:
- Online monitoring:
- Confidence/source/completeness/risk checks:
- Escalation threshold:

### 8. Prompt registry / versioning
- Prompt files/registry location:
- Owner:
- Versioning/change log:
- Rollback path:

### 9. Observability / operations
- Logs:
- Audit trail:
- Cost/latency metrics:
- Failure alerts:
- Recovery/retry behavior:
- Human override capture:

### 10. Deployment / runtime / security
- Hosting/runtime:
- Auth/access control:
- Secrets handling:
- Queue/background jobs:
- Autoscaling or concurrency limits:
- Data retention/deletion:

## Done state
A build is production-shaped only if it has:
- clear routing
- source support
- eval/judge checks
- human handoff for risky/low-confidence cases
- prompt/version tracking
- observability and audit logs
- freshness/cache rules where repeated work exists
- auth, runtime, secrets, and retention handled for production/client use
