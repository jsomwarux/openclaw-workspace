# Cohort-Two Bounded Two-Page Inactive Deployment Receipt

- Deployed: 2026-09-23 16:41 EDT
- Source: `jsomwarux/n8n-agent` `main@41ef3bfb49dd6a0579377355cc5d0af7ce442093`
- Runtime: n8n `2.14.1` at `127.0.0.1:5678`
- Main workflow: `c2discoveryMAIN1`, 58 nodes, inactive
- Error workflow: `c2discoveryERRH1`, 4 nodes, inactive
- Guarded nodes: weekly schedule, Mission Control post, and heartbeat post all disabled
- Send-capable nodes: zero
- Two-page contract: `N06P` emits exactly two offsets; `N07` uses deterministic `$order`, `$limit`, and `$offset`; `N07B` validates `pairedItem` provenance before combining
- Source/live equality: connections match exactly; nodes match after removing n8n's expected existing credential-ID binding
- Unrelated active workflows: unchanged at 11
- Runtime health: HTTP 200
- Latest cohort execution after deployment: 1721 (no new execution)
- Discovery state after deployment: cursor 800, ledger 9, carryover 0
- Pilot/model/state/action activity during deployment: none
- Recoverable backups: `database-before.sqlite`, `c2discoveryMAIN1-before.json`, and `c2discoveryERRH1-before.json` in this directory
- Proof log: `ca2c0deb`

