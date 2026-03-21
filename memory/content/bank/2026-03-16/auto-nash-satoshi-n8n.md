# auto-nash-satoshi-n8n — 2026-03-20
Pillar: autonomous-detection
Source: build
Rubric: real outcome with specific number + architectural decision with real tradeoffs
angle_id: null

---

replaced Gumloop with a self-hosted n8n workflow for Nash Satoshi.

32 nodes. 4 models (GPT, Gemini, Claude, Grok) running in parallel.

Gumloop handles sequential flows well. Parallel branches at that scale hit limits.

n8n doesn't have that problem.

---
audit: starts with point ✅ | reply hook (invites "why?" and "what's Nash Satoshi?") ✅ | ends on capability proof ✅ | no forbidden words ✅ | no em dashes ✅ | no exclamation points ✅ | specific numbers (32 nodes, 4 models) ✅ | no implied fake client experience ✅ | no self-promotion ✅
