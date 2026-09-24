# Cohort-Two Seed Expansion Inactive Deployment Receipt

- Deployed: 2026-09-23 EDT
- Source: `jsomwarux/n8n-agent` `main@7863deee563406d96b6c508ad17777655d4bab57`
- Runtime: n8n `2.14.1` at `127.0.0.1:5678`
- Main workflow: `c2discoveryMAIN1`, 58 nodes, inactive
- Error workflow: `c2discoveryERRH1`, 4 nodes, inactive
- Seed roster: `c2-seed-roster-v2`, 20 evidence-bearing organizations, SHA-256 `d2c9977052573e930692374bebe1fb1c51e7ddcf4cbe00d9046e12433393fe62`
- Guarded nodes: weekly schedule, Mission Control post, and heartbeat post all disabled
- Send-capable nodes: zero
- Source/live equality: connections and settings match exactly; nodes match after removing n8n's expected existing credential-ID binding
- Seed-expansion contract: N03 requires roster v2 evidence, N09 uses verified roster hosts, and N33's 0-4 branch states that nothing is reviewable or sendable and routes to diagnosis/seed expansion
- Independent release gate: 623 passed, 0 failed, 0 skipped; regenerated source/workflow tree stayed clean
- Unrelated active workflows: unchanged at 11
- Runtime health: HTTP 200
- Latest cohort execution after deployment: 1722 (no new execution)
- Discovery state after deployment: cursor 1600, ledger 9, carryover 0
- Pilot/model/state/action activity during deployment: none
- Recoverable backups: `database-before.sqlite`, `c2discoveryMAIN1-before.json`, `c2discoveryERRH1-before.json`, and `seed-roster-before.json` in this directory

