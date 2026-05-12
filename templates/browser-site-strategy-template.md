# Browser / Site Strategy Template

Use after exploratory browser/site work reveals a repeatable path, hidden endpoint, stable selector set, or gotcha. This is the holding artifact before promoting to a full skill or helper script.

## Task
- **Site / app:**
- **Goal:**
- **Read-only or write action:**
- **Owner / client / project:**
- **Date discovered:**

## Recommended Method
Choose one:
- deterministic fetch/API
- static HTML parser
- Playwright/browser automation
- manual/human approval required

Why this method:

## Inputs
- Required inputs:
- Optional filters/params:
- Auth/session assumptions:
- Rate limits / anti-bot / CAPTCHA risk:

## Cheapest Reliable Path
1.
2.
3.

## Endpoints / Selectors / Commands
### Endpoints or network calls
- URL:
- Method:
- Required headers:
- Query/body params:
- Response fields:

### Selectors / UI path
- Page URL:
- Wait condition:
- Selector/action:
- Fallback selector/action:

### Helper script
- Path:
- Command:
- Expected output:

## Gotchas
- Region/IP/session behavior:
- Dynamic rendering behavior:
- Silent failure modes:
- Drift indicators:

## Validation Recipe
- Sample input:
- Expected output:
- Verification command/check:
- What failure looks like:

## Fallback Path
If recommended method fails:
1.
2.
3.

## Promotion Decision
- Keep as strategy note / promote to helper script / promote to SKILL.md
- Reason:
- Next action:
