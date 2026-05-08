# App Marketing OS — Directory & Backlink Submissions

## Purpose
Create durable discovery surfaces for every app beyond rented social platforms.

## Submission Pack Template
For each app, prepare:
- App name
- URL
- One-line tagline
- 50-word description
- 150-word description
- Category
- Tags/keywords
- Logo/icon
- 3–5 screenshots
- Founder/maker note
- Pricing
- Launch status
- Contact email
- Social links

## Priority Directories
General:
- Product Hunt
- BetaList
- Uneed
- AlternativeTo
- DevHunt
- Indie Hackers products/showcase if relevant
- SideProject directories

AI/tool directories where relevant:
- Futurepedia
- There’s An AI For That
- AI tool directories with permanent listings

Niche surfaces:
- Vista: Letterboxd alternative lists, movie app directories, iOS app discovery lists.
- Nash Satoshi: crypto tool directories, AI investing/tool lists, agent/x402 directories if relevant.
- Glow Index: skincare/beauty tool lists, ingredient checker directories, AI beauty directories.
- Action Arena: fantasy football tools, sports betting tools that allow fake-money/social strategy apps, game/beta directories.

## Current Backlog

### Vista
Status: not started
Priority: high
Reason: live App Store product; needs durable discovery.
First action: create Vista submission pack from App Store listing, screenshots, and current product copy.

### Nash Satoshi
Status: not started
Priority: high
Reason: live web app; SEO/backlinks can compound.
First action: create Nash submission pack emphasizing 4-LLM game-theory ranking and no price-prediction claims.

### Glow Index
Status: wait
Reason: pending/stability gate.
First action after activation: create skincare-safe submission pack with no medical claims.

### Action Arena
Status: prelaunch
Priority: medium-high after landing/waitlist exists
Reason: football season deadline; prelaunch surfaces can collect beta users.
First action: waitlist/landing page first, then submit as fake-money betting strategy league / fantasy football competition app.

### Dynasty Fantasy Football Simulator
Status: wait
Reason: separate build lane; needs product artifact/landing page before submissions.

## Guardrails
- Do not submit to sites requiring payment without JT approval.
- Do not create public claims not present in app registry/proof points.
- No gambling/real-money implication for Action Arena.
- Track every submission status and URL.


## Draft Packs Created
- [2026-05-07] Nash Satoshi directory pack: `memory/app-marketing/directory-packs-nash-satoshi.md` — draft-ready, not submitted.
- [2026-05-07] Vista SEO brief: `memory/app-marketing/seo-briefs-vista-1-100-movie-rating-app.md` — implemented on jtsomwaru.com at `/blog/one-hundred-point-movie-rating-app`.
- [2026-05-07] Vista directory pack: `memory/app-marketing/directory-packs-vista.md` — draft-ready, not submitted.

## Draft Packs Created
- [2026-05-07] Glow Index directory pack: `memory/app-marketing/directory-packs-glow-index.md` — draft-ready, not submitted. First recommended target: Uneed or Futurepedia after screenshots are selected and JT approves.

## Crawlability Issue Log
- [2026-05-07] Glow Index crawler-style fetches for `/categories`, `/categories/serum`, `/sitemap.xml`, and `/llms.txt` returned Cloudflare "Just a moment" to generic fetch tooling after deployment. JT can see pages in browser, but AI/search crawler access needs verification/fix before relying on GEO impact. Required follow-up: inspect Cloudflare/Replit front door settings, ensure `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/serum` are reachable by major AI/search crawlers without JS challenge.
