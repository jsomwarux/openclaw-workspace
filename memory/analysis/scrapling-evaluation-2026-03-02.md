# Scrapling Evaluation — 2026-03-02

**Task:** Evaluate Scrapling for use in StreetEasy scraper + JT Somwaru Consulting research pipeline.
**Source:** MC task `j575zxctr2xts3h9cj052qfyan82000a` (🔴 HIGH, overnight agent 3AM)

---

## What Scrapling Actually Is

**Scrapling is a Python open-source library** (`pip install "scrapling[ai]"`), NOT a native OpenClaw feature.

> **Correction to task card:** The @simplifyinAI X post (the MC task source) described it as "OpenClaw natively integrates Scrapling." This is misleading — there are no OpenClaw docs for Scrapling (confirmed 404 at docs.openclaw.ai/tools/scrapling). It's a standalone Python library used inside Python scripts that OpenClaw can exec. The WIRED article (`wired.com/story/openclaw-users-bypass-anti-bot-systems-cloudflare-scrapling/`) describes users *pairing* OpenClaw with Scrapling — not a built-in feature.

**GitHub:** github.com/D4Vinci/Scrapling | **Docs:** scrapling.readthedocs.io

---

## Key Capabilities

| Feature | Details |
|---------|---------|
| `StealthyFetcher` | Bypasses Cloudflare Turnstile + Interstitial out of the box |
| **Adaptive selectors** | `auto_save=True` → elements persist across site redesigns. `adaptive=True` → auto-relocates them if structure changes |
| `DynamicFetcher` | Full browser automation via Playwright (handles JS-rendered sites) |
| `Fetcher` | Fast HTTP with TLS fingerprint spoofing, HTTP/3, browser header impersonation |
| Spider API | Scrapy-like concurrent crawls, pause/resume, proxy rotation |
| MCP server | `scrapling.readthedocs.io/en/latest/ai/mcp-server/` — native OpenClaw MCP integration available |
| Speed | ~774x faster than BeautifulSoup with lxml per X posts (likely parsing, not network) |

---

## Application to JT's Stack

### 1. StreetEasy Scraper (Aya — $1K delivered project)
**Current stack:** Python + BeautifulSoup in n8n  
**Risk today:** StreetEasy uses Cloudflare. Any structural change to their site would break BeautifulSoup selectors.  
**With Scrapling:**
- `StealthyFetcher` handles Cloudflare without manual workarounds
- `auto_save=True` on listing selectors → survives site redesigns automatically
- Replace BeautifulSoup parsing with `p.css('.listing-info', auto_save=True)`

**Recommended change (draft only — JT review before modifying):**
```python
# BEFORE (BeautifulSoup)
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
listings = soup.select('.listing-info')

# AFTER (Scrapling)
from scrapling.fetchers import StealthyFetcher
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://streeteasy.com/...', headless=True)
listings = page.css('.listing-info', auto_save=True)
```

⚠️ **Do NOT deploy this change without JT's explicit approval** — the StreetEasy scraper is a live client deliverable.

### 2. JT Somwaru Consulting Research Pipeline
**Current stack:** research-agent does prospect research via web fetch  
**With Scrapling (via MCP server):** Eve could use Scrapling's MCP server as a tool to scrape target company pages without Cloudflare blocks, improving brief quality.  
**Recommendation:** Install Scrapling MCP server as a research-agent tool. Low risk (research pipeline is internal).

### 3. Glow Index
**Current stack:** n8n + scraping for product data  
**Benefit:** Scrapling's adaptive selectors would reduce breakage from skincare retailer site updates.

---

## Legal / ToS Considerations

- **WIRED report (Feb 2026):** Called out OpenClaw + Scrapling usage for bypassing Cloudflare. Cloudflare is actively working on countermeasures.
- **StreetEasy ToS:** Prohibits automated scraping. The current scraper already operates in a gray area. Scrapling doesn't change the ToS risk — it's about how the scraping is done, not what.
- **Risk verdict:** Scrapling doesn't introduce new legal risk vs. BeautifulSoup for the same scraping task. The risk is the same; Scrapling is just more reliable.

---

## Recommended Actions for JT

| Action | Priority | Notes |
|--------|----------|-------|
| Install Scrapling MCP server for JT Somwaru Consulting research pipeline | ✅ Low risk — do now | `pip install "scrapling[ai]"` + wire MCP server |
| Plan StreetEasy scraper upgrade to Scrapling | 🟡 Medium — JT approval needed | Create n8n workflow update; don't deploy without Aya sign-off |
| Evaluate Scrapling for Glow Index | 🟢 Nice to have | After Scrapling MCP is working |

---

## TOOLS.md Update (ready to apply)

Add to TOOLS.md under a new "Scrapling" section:

```
## Scrapling
- Library: `pip install "scrapling[ai]"` — adaptive Python web scraping framework
- NOT a native OpenClaw feature — used inside Python scripts exec'd by OpenClaw
- Key classes: `Fetcher` (fast HTTP), `StealthyFetcher` (Cloudflare bypass), `DynamicFetcher` (Playwright)
- Adaptive selectors: `page.css('.selector', auto_save=True)` — survives site redesigns
- MCP server: `scrapling.readthedocs.io/en/latest/ai/mcp-server/` — wire as tool in research-agent
- Docs: scrapling.readthedocs.io | GitHub: github.com/D4Vinci/Scrapling
- Use case: StreetEasy scraper resilience (upgrade plan in memory/analysis/scrapling-evaluation-2026-03-02.md)
```

---

## Estimated Time This Research Took
~15 minutes inline (web fetch + search + analysis)
