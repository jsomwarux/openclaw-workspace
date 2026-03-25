# auto-glow-index-image-system — 2026-03-24
Pillar: autonomous-detection
Source: build
Rubric: real outcome with specific number (100 products with images after backfill)

---

built an image system for glow index today.

100 products now have images after one backfill run.

the pattern: build the pipeline locally, verify it works, then a single curl command moves it to production. no manual uploads. no hardcoding.

the part that doesn't get talked about: the backfill is usually harder than the live system. you have to handle existing data that was never designed with images in mind.
