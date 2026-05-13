# Mission Control Priority Auditor Autoresearch Checklist

Target: `agents/mission-control-priority-auditor/AGENT.md` + `scripts/mission_control_north_star_audit.py`

Pass/fail checks:
1. Does the audit leave no more than ~15 active `high` tasks unless a genuine crisis exists?
2. Do the top high-priority tasks map to North Star categories: immediate cash, client proof, warm opportunity, current app distribution, or health/financial stability?
3. Are stale cold outreach batches, M2/M3/email pivots, and old Review+Send tasks kept below warm/referral/client proof work?
4. Are generic skills/tool-update/speculative build tasks prevented from outranking current consulting cash/proof/distribution work?
5. Does the script save a report and run through Morning Brief/heartbeat or an equivalent recurring path so JT can trust Mission Control when he opens it?
6. Does the script avoid destructive behavior: no deletes, no external sends, and only priority/sortOrder/description patches?

Passing score: 5/6 minimum; target 6/6.
