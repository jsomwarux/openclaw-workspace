---
platform: linkedin
type: format-signal
slug: resource-roundup-artifact-pack
date_generated: 2026-05-08
posted: false
source_signal: content-signals.md [2026-05-08] FORMAT Resource roundup / artifact pack
---

The problem was not generating more posts. The problem was keeping the content system pointed at the current business.

This week I patched my internal content agent with five artifacts:

1. A current-efforts file that tracks active consulting lanes, current clients, app priorities, and what not to overclaim.
2. A posted-log gate that blocks repeated topics and structures from the last 21 days.
3. A content-signals file that stores real platform signals, not generic “AI is hot” ideas.
4. A freshness rule that prefers sources from the last 14 days.
5. A skip rule that tells the agent to leave a slot empty when the proof is weak.

That last one matters most.

Most automated content systems fail because they are forced to fill the calendar. Once the agent must publish no matter what, quality becomes a scheduling problem instead of a judgment problem.

The better rule is simple:

If there is no fresh signal, no current effort, and no specific proof, skip the slot.

Autonomy without taste becomes spam.
