# @supermemory/openclaw-supermemory 2.0.2 — Evaluation
**Date**: 2026-03-08 | **Source**: npmjs.com + github.com/supermemoryai | **Evaluated by**: Eve (overnight)
**Package**: `@supermemory/openclaw-supermemory` v2.0.2 | Published: 2026-03-06

## What It Is
An OpenClaw plugin that adds **long-term persistent memory** to Eve, powered by Supermemory cloud. It works by:
- **Auto-capturing** conversations after each AI turn (extracted + stored in Supermemory cloud)
- **Auto-recalling** semantically relevant memories before each turn (injected into context)
- Building a **persistent user profile** (facts + preferences + conversation context)

Think of it as MEMORY.md but: semantic search instead of flat text, cloud-backed, auto-updated every turn rather than on-demand.

## Key Features (v2.0.2)
| Feature | Detail |
|---------|--------|
| Auto-Recall | Queries Supermemory before every AI turn, injects relevant memories |
| Auto-Capture | Stores conversation after every turn — cloud extraction + deduplication |
| Custom Containers | Route memories to named buckets (e.g., `work`, `personal`, `jt-consulting`) |
| AI Tools | `supermemory_store`, `supermemory_search`, `supermemory_forget`, `supermemory_profile` |
| CLI Commands | `search`, `profile`, `wipe`, `status` |
| Config Control | `autoRecall`, `autoCapture`, `maxRecallResults` (default: 10), `captureMode` |

## What's New in 2.0 vs 1.x
No public changelog found on npm or GitHub. However, based on the 6-version history and the description:
- v2.x adds **custom container tags** — memory routing to topic-specific buckets
- v2.x adds `supermemory_forget` tool (delete by query or ID)
- v2.x adds `profileFrequency` config (inject full profile every N turns, default 50)
- v2.x adds `setup-advanced` command for full interactive config
- Core auto-recall/auto-capture was present in v1.x; containers appear new in v2.x

## Relevance to JT / Eve
### The honest case for:
- Eve's current memory architecture (MEMORY.md + daily notes) is **manual and lossy** — facts discussed in a session are lost unless Eve explicitly writes them down
- Supermemory would catch things Eve misses — client details, preferences, context from quick exchanges
- Semantic search > keyword search over accumulated context
- Custom containers could route: `jt-consulting` (client work), `jt-profile` (JT's preferences), `job-search` (application history)

### The honest case against:
- **Privacy concern**: All conversations go to Supermemory cloud (third-party). JT's client details, financial context, personal preferences → external server. **This is a non-trivial data sharing decision.**
- **Cost**: Requires Supermemory Pro or above. Pricing not listed — need to check supermemory.ai. If monthly cost > $20, it doesn't justify the benefit when we already have MEMORY.md + kb.ts working.
- **Duplication risk**: Auto-capture every turn = every heartbeat, every cron response, every routine exchange → massive noise in the memory store unless `captureMode` is tuned carefully
- **Bootstrap budget impact**: Auto-recall injects up to 10 memories before every AI turn = adds tokens to every session. At scale this could increase per-session cost non-trivially.
- **JT hasn't asked for this**: Spec update task was auto-pushed by skills-researcher cron, not JT request. This is informational.

## Security Assessment
- **Data leaves the Mac**: All conversations sent to Supermemory cloud (US-based, enterprise-grade based on their site)
- **API key stored**: `SUPERMEMORY_OPENCLAW_API_KEY` in env — same risk level as other API keys (drive, notion, firecrawl)
- **No code execution** on Eve's machine — it's a read/write plugin
- **Risk surface**: Third-party data storage for sensitive operational content
- **Verdict: Requires explicit JT approval before install** — data privacy decision, not just a tech decision

## Current Eve Memory Stack (for comparison)
| Component | What it does | Coverage |
|-----------|-------------|----------|
| MEMORY.md | Core facts, projects, decisions | Manual, high-signal |
| Daily notes | Session log, decisions, mistakes | Manual, comprehensive |
| knowledge/kb.sqlite | Structured knowledge base | Manual, searchable |
| memory_search tool | Semantic search over .md files | Automatic at recall time |

**Gap Supermemory would fill**: Facts from quick exchanges that Eve doesn't write down, cross-session pattern building, auto-profile maintenance.

**Gap it wouldn't fill**: Structured project state (Convex/Mission Control), cost tracking, code artifacts.

## Recommendation
**Do not install without JT approval.** Key decisions needed:
1. **Data privacy**: Are you comfortable with conversation data going to Supermemory cloud?
2. **Cost**: Check supermemory.ai pricing — Pro tier. If ≤ $20/mo, arguably worth it. If > $20, not justified vs. existing stack.
3. **Scope**: If approved, configure with `captureMode: "all"` (filters short texts), `maxRecallResults: 5` (reduced from default 10 to protect bootstrap budget), custom containers for `jt-consulting` / `jt-profile` / `job-search`

**If JT approves:**
```bash
openclaw plugins install @supermemory/openclaw-supermemory
openclaw supermemory setup  # enter API key
openclaw supermemory setup-advanced  # configure containers + captureMode
```

## Suggested Config (if approved)
```json
{
  "apiKey": "${SUPERMEMORY_OPENCLAW_API_KEY}",
  "containerTag": "eve_main",
  "autoRecall": true,
  "autoCapture": true,
  "maxRecallResults": 5,
  "profileFrequency": 30,
  "captureMode": "all",
  "enableCustomContainerTags": true,
  "customContainers": [
    { "tag": "jt-consulting", "description": "Client work, pipeline, deliverables" },
    { "tag": "jt-profile", "description": "JT's preferences, goals, context" },
    { "tag": "job-search", "description": "Job applications, companies, roles" }
  ]
}
```

## Action Items for JT
- [ ] Decide: install supermemory plugin? (Data privacy decision — see Security section above)
- [ ] Check supermemory.ai Pro pricing before deciding
- [ ] If yes: approve and Eve installs + configures with suggested config above

---
*Task: 🟠 @supermemory/openclaw-supermemory 2.0.2 — Major update to persistent memory plugin*
*MC Task ID: j576fdkbqya5h4jpwcnbp4ktpn82eyj1*
