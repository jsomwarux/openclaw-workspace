# auto-nash-satoshi-n8n-linkedin — 2026-03-20
Pillar: autonomous-detection
Source: build
Rubric: real outcome with specific number + architectural decision with real tradeoffs
Format: Behind the Build (Sunday slot)
angle_id: null

---

Nash Satoshi was running on Gumloop. It worked until it didn't.

The problem: a 4-model ensemble needs GPT, Gemini, Claude, and Grok scoring the same crypto asset independently, in parallel. Gumloop handles sequential flows well. Parallel branches at that scale hit limits fast.

So I rebuilt the entire pipeline in n8n.

32 nodes. 3 stages: data ingestion, parallel 4-model scoring, ensemble synthesis. Each model scores independently. Results get reconciled into a single ranked output. Webhook trigger to final analysis in about 4 minutes.

The ensemble is fully self-hosted now. Runs on schedule, no platform dependency.

---
audit: starts with situation leading to problem ✅ | ends on capability proof (not advice) ✅ | no forbidden words ✅ | no em dashes ✅ | no exclamation points ✅ | specific numbers (32 nodes, 3 stages, 4 minutes) ✅ | no external link in body ✅ | no implied fake client ✅ | build-showcase ends on capability ✅
