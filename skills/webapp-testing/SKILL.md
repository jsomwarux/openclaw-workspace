---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. Use when testing any local web app built by a coding agent.
license: Apache 2.0 (source: github.com/anthropics/skills)
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available** (if present in project):
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. Do NOT read the source — invoke as black-box scripts.


## Browser Automation Ladder
Before using high-agency browser exploration, try cheaper/deterministic paths first:
1. **Fetch/API probe:** If the target data or state is available through HTML, JSON, network response, local file, API, or database, use deterministic fetch/parser/script instead of browser automation.
2. **Static DOM / rendered DOM:** For local apps, inspect HTML or rendered DOM and write a focused Playwright script with stable selectors.
3. **Browser reconnaissance:** Use screenshots/DOM/network inspection only when JS, auth, or dynamic UI blocks deterministic access.
4. **Skillify repeated discoveries:** If a browser task is likely to recur and exploration reveals a reliable path, write the shortest durable artifact: skill/checklist/script with selectors, endpoints, gotchas, and verification.

Do not pay the browser-agent discovery tax repeatedly. Expensive exploratory runs should graduate into deterministic helpers or reusable skills. If the path is not stable enough yet, save a strategy note with `templates/browser-site-strategy-template.md`.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

**Automation script (Playwright logic only — server managed automatically):**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Always headless
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS
    # ... automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
```python
page.screenshot(path='/tmp/inspect.png', full_page=True)
content = page.content()
page.locator('button').all()
```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`
- Capture screenshots for debugging: `page.screenshot(path='/tmp/debug.png')`
- Check console logs: `page.on('console', lambda msg: print(msg.text))`

## Install Playwright (if not present)
```bash
pip install playwright
playwright install chromium
```
