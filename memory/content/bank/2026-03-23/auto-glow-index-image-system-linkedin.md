# auto-glow-index-image-system-linkedin — 2026-03-24
Pillar: autonomous-detection
Source: build
Rubric: real outcome with specific number (100 products with images after backfill)

---

When you add a new system to an existing product, the migration is usually the hardest part.

I built an image system for Glow Index today — automated product image fetching and display. The live system was straightforward. What took real work was the backfill: 100 existing products with no images, each needing to be processed through the new pipeline without breaking anything already in production.

One backfill run. 100 products covered. Verified locally, then a single curl command moves it to Replit production.

The pattern I keep coming back to: build it so the migration is a command, not a project. If moving from local to prod requires more than one step, the deployment model isn't clean enough.

Glow Index is a skincare ranking app. Every product now has images. The architecture that made the backfill simple is the same one that'll make future updates trivial.
