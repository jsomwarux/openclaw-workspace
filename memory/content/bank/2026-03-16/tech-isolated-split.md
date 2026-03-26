# tech-isolated-split
angle_id: arch-isolated-split
platform: X
type: technical
suggested_slot: Tuesday or Saturday

---

Content generation and content delivery are two different crons.

The generator runs isolated: no conversational context needed, just file reads and writes.
The delivery cron runs in 60 seconds, pulls the file, sends it.

If they're the same job, one failure kills both.
Separation isn't complexity. It's reliability.

---
audit: starts with point ✅ | you/I ratio N/A (system observation, no I) ✅ | no em dashes ✅ | no exclamation points ✅ | no self-promotion ✅ | no unverifiable specifics ✅ | ends on capability proof ✅
