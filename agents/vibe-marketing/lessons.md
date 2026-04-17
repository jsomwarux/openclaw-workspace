# Vibe Marketing System — Lessons Learned

## [vibe-marketing] TikTok duplicate post — same entry posted twice (2026-04-12)
- **Problem:** "I can't believe I've been using half-stars" TikTok posted on Apr 6 AND Apr 12 — same content, twice. JT noticed both went out.
- **Root cause — two compounding failures:**
  1. **Apr 6 run was silent:** `vibe-post-vista-sunday` at that time used `delivery.mode: none` (before the fix from the 2026-04-06 lesson). JT was never notified that a post went out. Without a notification, he couldn't confirm whether it was posted.
  2. **Apr 6 run never set `posted: true`:** The `reelfarm-create-slideshow.py` bug (now fixed) caused `mark_photos_used()` to error when `vibe-post.py` passed pre-resolved photo URLs. That error propagated — or more likely, `mark_posted()` was never called because the script exited early at the `post_status` check before reaching the `mark_posted()` call.
  3. **No duplicate detection:** `vibe-post.py` had no guard to skip an entry that was already posted in a prior run. It only checked `posted: false` in the queue AND that a result from Reel.farm returned a non-success status.
- **Fix:**
  1. **`vibe-post.py` now deduplicates by hook key:** Before picking the next entry, it calls `_last_hook_key(product)` which reads the LAST entry in `performance-log.jsonl` for that product+platform, reconstructs the normalized hook key, and skips any queued entry whose hook key matches. This prevents the same hook from posting twice even if the queue entry was never marked posted.
  2. **Performance log seeded:** Two seed entries added to `performance-log.jsonl` for the two Apr posts (slideshow 419199/video 411049 and 440438/429913) so the dedup guard has data to work from going forward.
  3. **Performance log auto-updates:** `vibe-post.py` now writes to `performance-log.jsonl` after every post (was already in the code but the log was empty/never populated before). This is the dedup guard's source of truth.
- **Prevention:** Any posting pipeline must check what was LAST POSTED before publishing, not just the queue's `posted` field. Queue entries can persist across restarts, system upgrades, or silent failures and remain un-marked. The dedup guard must be hook-based, not status-based.

## [vibe-marketing] Sound selection was aesthetic-first, not trend-first (2026-04-06)
- **Problem:** AGENT.md sound rules defaulted to aesthetic fits (lo-fi for crypto, Hans Zimmer for movies) instead of trending sounds. Wrong distribution strategy — trending audio is what drives TikTok reach, not aesthetic fit.
- **Root cause:** Sound selection was written as a creative direction, not a distribution strategy. No specific sound names were specified, so the agent defaulted to generic "lo-fi ambient" and "Hans Zimmer" which don't trend on TikTok.
- **Fix:** Updated AGENT.md Step 4c with:
  - Specific approved standing sounds per product (Bounce by фрози & joyful, Where I'm Going by Thundercat for Nash Satoshi; Charli xcx & John Cale "House", Azealia Banks "212" for Vista)
  - Cultural trend hooks to chase (Coachella April 10-26, Euphoria S3 April 12)
  - Rule: trending first, aesthetic as filter — never sacrifice 100K+ video trend for perfect aesthetic fit
  - Patched 4 existing queue entries (week 2026-04-06) with real sound recommendations
  - Updated vibe-post.py to print sound_rec in Telegram output when posting
- **Prevention:** Every new content vertical needs a "sounds" section with specific, named sounds and a cultural trend calendar. Generic category descriptions ("lo-fi ambient") are not actionable and lead to wrong defaults.

---

## [vibe-marketing] TikTok posting crons created but never executed (2026-04-06)
- **Problem:** 4 posting crons (vibe-post-nash-tuesday, vibe-post-nash-thursday, vibe-post-vista-friday, vibe-post-vista-sunday) were created but had NEVER RUN. All had `delivery.mode: none` making them silent.
- **Root cause:** Crons were created and enabled but the generator cron (vibe-marketing-generate) ran once, crashed mid-execution, and never wrote to the queue. Posting crons fired on empty queues and did nothing.
- **Fix:** 
  - Fixed generator cron: ensured it completes and writes to queue.jsonl
  - Fixed all posting crons: switched from `delivery.mode: none` to `announce` with Telegram channel
  - Generator now runs Mon 4:45 AM → queue populated → posting crons fire Tue/Thu/Fri/Sun → Telegram notification with sound recommendation
- **Prevention:** When creating a new cron pipeline, verify BOTH the producer AND consumer crons have actually executed at least once. Check `cron runs --id <jobId>` for zero-run jobs immediately after setup.

---

## [vibe-marketing] Cron Telegram delivery silent failures (2026-04-06)
- **Problem:** Outreach pipeline had 28 consecutive failed Telegram deliveries (since March 12). Content crons also failing. Root cause: crons using `delivery.mode: "none"` rely on internal `message` tool calls which silently fail in isolated agent sessions.
- **Root cause:** Isolated agent sessions (agentTurn) don't have access to the message tool for Telegram delivery. Only crons using OpenClaw's built-in `announce` delivery mode work.
- **Fix:** Switched all content and outreach crons from `delivery.mode: "none"` to `announce` with `channel: telegram`.
- **Prevention:** Any cron that needs to deliver a message to Telegram MUST use OpenClaw's `announce` delivery mode. Never use `message` tool inside an isolated agent session for channel delivery.

---

## 2026-04-16 — Cross-product contamination + silent post failures

### What happened
A Nash Satoshi TikTok was posted with Vista-related copy. Separately, `vista-tiktok-2026-03-30-1` was posted TWICE (duplicate, not caught).

### Root causes

**1. Generate agent overwrites queue.jsonl (CRITICAL — fixed 2026-04-15)**
The generate phase used `write` tool instead of append. It replaced the full queue (69 entries) with only 12 new entries. During the window when the queue only had Apr13 entries, the posting crons ran and found the wrong content (or nothing). The Apr 13 entries had Vista TikTok content alongside Nash entries, causing cross-product selection.

**Fix:** AGENT.md Step 4 now forces Python script append (read existing + combine + write). Committed `5a2c8aa`.

**2. mark_posted() silent failure**
The `find_next_entry()` function was NEVER defined before the fix on Apr 15. Crons ran vibe-post.py without it — the script errored out silently. Posts appeared to succeed (Reel.farm returned `processing`) but `mark_posted()` was never called, so queue entries stayed `posted=False`.

After `find_next_entry` was added, entries were found and API calls made, but `mark_posted` only fires when `post_status in ("processing","published","skipped")`. If the status was something else, it silently skipped.

**3. Duplicate guard used queue.jsonl, not performance log**
`_last_hook_key` read the LAST posted entry per product from queue.jsonl. But queue.jsonl was restored multiple times (resetting `posted=False`). The duplicate guard never saw the first `vista-tiktok-2026-03-30-1` post because after the restore, the guard looked at queue state (unposted) not performance log (posted).

**Fix:** Duplicate guard now checks performance-log.jsonl for ANY entry with the same ID (regardless of product). Committed `79bcf8c`.

**4. No cross-product content verification**
There was no runtime check that the selected entry's content actually matched the requested product. A Vista entry could be selected for Nash (or vice versa) if the product_slug somehow got mismatched.

**Fix:** Added keyword-based content verification in vibe-post.py. Script exits with FATAL if Nash content has movie keywords (>2 hits, 0 crypto) or Vista content has crypto keywords (>2 hits, 0 movie). Committed `79bcf8c`.

### What actually got posted (verified)
- ✅ `vista-tiktok-2026-03-30-1` — posted Apr 6 (performance log confirmed)
- ❌ `vista-tiktok-2026-03-30-1` — DUPLICATE posted Apr 12 (not caught — fixed)
- ❌ `nash-satoshi-tiktok-2026-04-06-1` — posted Apr 16 with potential Vista copy (queue was in wrong state during cron window)

### Lesson
Queue file is operational state. Generate + restore operations can corrupt it. Always use performance log as source of truth for "was it posted?" and add runtime content verification before any API call.
