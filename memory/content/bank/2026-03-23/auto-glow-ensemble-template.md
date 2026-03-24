# auto-glow-ensemble-template — 2026-03-23
Pillar: autonomous-detection
Source: main-session | build
Rubric: architectural decision with real tradeoffs + non-obvious problem solved

---

built the same 4-LLM ensemble twice.

first for Nash Satoshi (crypto game theory rankings).
second for Glow Index (skincare product analysis).

the second build took 20% of the time because i extracted the pattern into a reusable template after the first one.

the lesson: ensemble pipelines look custom. they're not. the architecture is always the same — model pool, independent scoring, aggregation layer, callback. what changes is the domain prompt.

build the template first. the second product is almost free.
