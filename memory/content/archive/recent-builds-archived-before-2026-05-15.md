# Recent Builds Archived Before 2026-05-15

Moved out of `memory/content/recent-builds.md` to keep the active build feed under its target size while preserving older proof history.

## jtsomwaru.com Public Proof Privacy Pass — 2026-05-14
**What:** Anonymized public client proof copy and removed exact proposal/deal amounts from site proof surfaces while keeping role/city/workflow specificity.
**For:** JT consulting / public credibility + client privacy
**Outcome:** Build + lint passed; pushed commit `11439c7`; production homepage, family-office detail route, and `/llms.txt` verified with no Aya/Altmark/Lady D/exact amount hits.
**Demonstrates:** Public proof hygiene, privacy-safe case-study packaging, attribution correction
**Content angle:** Strong proof does not require naming the client. It requires the workflow, the buyer type, and the operating result.
**Status:** complete

## jtsomwaru.com Client Outcome Attribution Fix — 2026-05-14
**What:** Corrected the site so Aya owns the construction dashboard and StreetEasy pipeline, added Altmark local-first family-office automation as its own client outcome/detail page, and restored Adversight AI under Apps.
**For:** JT consulting / proof accuracy
**Outcome:** Build + lint passed; pushed commit `25b9563`; production `/` and `/work/altmark-local-automation` verified with HTTP 200 and expected content strings.
**Demonstrates:** Proof attribution discipline, client-work packaging, portfolio inventory preservation
**Content angle:** Proof only works if the attribution is precise. Generic labels can hide the actual client story.
**Status:** complete

## jtsomwaru.com Positioning + Roles Update — 2026-05-14
**What:** Reworked the personal site around consulting-first positioning with balanced Work buckets, updated Who I Help niches, cleaner About/tools language, a new `/roles` recruiter path, footer links, and AI-search metadata updates.
**For:** JT consulting / selective recruiting upside
**Outcome:** `npm run build` and `npm run lint` passed; pushed to GitHub commit `fce1480`; production checks returned HTTP 200 for `/` and `/roles` on Vercel.
**Demonstrates:** Consulting positioning, proof-tier hygiene, Next.js implementation, recruiter/buyer path separation, GEO metadata maintenance
**Content angle:** A portfolio site should separate client outcomes, demos, internal systems, and apps without making the real client work look scarce.
**Status:** complete
