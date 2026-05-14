# Glow Index — Crawler Access Check

Date: 2026-05-13
Method: `urllib.request` with Googlebot-style User-Agent, read-only GET requests.

## Result
Glow has a real crawler-access blocker for key durable-discovery surfaces.

| URL | Result | Note |
|---|---:|---|
| `https://glowindex.co/robots.txt` | 403 | Cloudflare “Just a moment...” challenge |
| `https://glowindex.co/sitemap.xml` | 403 | Cloudflare “Just a moment...” challenge |
| `https://glowindex.co/llms.txt` | 403 | Cloudflare “Just a moment...” challenge |
| `https://glowindex.co/rankings` | 200 | HTML loads |
| `https://glowindex.co/categories` | 403 | Cloudflare “Just a moment...” challenge |
| `https://glowindex.co/categories/serum` | 403 | Cloudflare “Just a moment...” challenge |

## Decision
Glow SEO/GEO is `MEASURE_FIRST` / crawlability-fix-first. Do not expand pSEO pages or submit directory listings that rely on sitemap/llms/category crawlability until these routes return normal 200 responses to crawlers.

## Fix path
First action: in Cloudflare/Replit hosting config, allow public crawler access to static discovery files and category routes: `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, `/categories/*`.

Preferred Cloudflare rule shape:
- Skip/allow managed challenge, JS challenge, and bot-fight checks for the path set above.
- If available, allow verified bots: Googlebot, Bingbot, Applebot, GPTBot, ClaudeBot, PerplexityBot.
- Do not disable all site protection if a narrow path/bot skip rule is available.

Diagnostic command:
```bash
cd ~/.openclaw/workspace
python3 scripts/glow_crawler_check.py
```

Done state: rerun the same GET checks and get 200 for all six URLs, with no Cloudflare challenge HTML on discovery files/category pages.

Guardrail: keep safe skincare claims; crawler access does not justify more medical/dupe/concern pages until structured product facts support them.
