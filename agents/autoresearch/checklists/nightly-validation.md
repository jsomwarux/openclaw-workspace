# Nightly Validation Controller Checklist

1. Does admission select only queued candidates and enforce the one-lane, three-candidate cap?
2. Does every admitted candidate produce one complete artifact or fail reconciliation explicitly?
3. Is each result independently verified against its falsification rule with fresh evidence?
4. Are promotion thresholds enforced exactly: score >=30/40, evidence >=4/5, distribution >=3/5, and no fatal constraint?
5. Do non-promotions avoid Mission Control tasks and Telegram delivery?
6. Does consumption create at most one idempotent promotion task with a concrete first action and done state?
