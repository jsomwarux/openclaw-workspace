# technical-advanced-tool-use.md
_Angle ID: advanced-tool-use-context-efficiency_
_Bank: 2026-03-30 | Pass 2 Technical_
_Platform: X | posted: false | banked: true_
_Note: Thursday calendar post uses this angle compressed. This is the expanded bank version for a different slot._

---

the context window is the production bottleneck most people aren't tracking.

5 MCP servers. 58 tools. ~55K tokens. before conversation starts.

Anthropic's Tool Search cuts that 85%. Opus 4 tool accuracy: 49% to 74%.

the pattern: agents shouldn't load every tool upfront.

discover on demand. call what you need. defer the rest.

running 35 crons in production. context efficiency is a real cost, not a benchmark exercise.

---
**Checklist:**
- [x] Em dashes: none ✓
- [x] Contrarian flip: none ✓
- [x] -ly adverbs: none ✓
- [x] First line: "the context window is the production bottleneck most people aren't tracking" ✓
- [x] Specific numbers: 5 MCP servers, 58 tools, 55K tokens, 85% reduction, 49%→74% accuracy ✓
- [x] Personal proof: "running 35 crons in production" ✓
- [x] Reply hook: context-constrained practitioners will have opinions ✓
