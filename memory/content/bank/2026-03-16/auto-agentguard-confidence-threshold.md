# auto-agentguard-confidence-threshold — 2026-03-17
Pillar: autonomous-detection
Source: build
Rubric: non-obvious problem solved
angle_id: null

---

most AI agents give you an answer.

they don't tell you how confident they were. they don't do anything different when they aren't sure.

AgentGuard does. every decision scored. high confidence executes. low confidence queues for human review.

70% isn't magic — it's a starting point you can tune. the value is that the line exists, it's enforced, and every crossing is logged.

that's the difference between an AI prototype and an AI deployment.
