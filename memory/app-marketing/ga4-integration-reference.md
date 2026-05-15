# GA4 Integration Reference for App Marketing OS

## Purpose

This document is the canonical reference for integrating Google Analytics 4 and Search Console into new apps in JT's portfolio. Use it when a new property comes online, when advising on GA setup for future Opticfy client work, or when troubleshooting analytics issues on existing apps. The patterns below were established through production debugging across Nash Satoshi and Glow Index in May 2026.

---

## Credential pattern

A single OAuth refresh token authenticated as the GA4 admin (jtsomwaru@gmail.com) covers every GA4 property in his account and every Search Console site he verifies. Scopes: `analytics.readonly` + `webmasters.readonly`. No per-property service accounts.

Why this matters: service accounts get rejected by GA4's "Add user" form on personal-Gmail GCP projects due to Google directory propagation issues. The gcloud Admin API bypass is also blocked for sensitive scopes on personal accounts. OAuth user credentials bypass both blockers entirely.

When a new GA4 property is created in his account, no new credential setup is needed. The existing OAuth refresh token immediately works for it. Just add the property to your registry.

The three env vars to expect: `GA4_OAUTH_CLIENT_ID`, `GA4_OAUTH_CLIENT_SECRET`, `GA4_OAUTH_REFRESH_TOKEN`. Same values used everywhere.

### Auth recovery

A 401 from GA4 or Search Console means the refresh token was revoked or expired. Do not attempt automatic re-auth — that requires user interaction via OAuth Playground. When 401 occurs:

1. Log the failure with timestamp and endpoint to mission control
2. Alert JT via Telegram with a regenerate-token request
3. Halt all GA4 and Search Console queries until he confirms the new token is in place

The OAuth app is in "Published" status (not Testing), so refresh tokens should be durable. Expiration is rare.

### Code patterns

GA4 Data API client:

```typescript
import { BetaAnalyticsDataClient } from "@google-analytics/data";
import { OAuth2Client } from "google-auth-library";

const oauth2Client = new OAuth2Client(
  process.env.GA4_OAUTH_CLIENT_ID,
  process.env.GA4_OAUTH_CLIENT_SECRET
);
oauth2Client.setCredentials({
  refresh_token: process.env.GA4_OAUTH_REFRESH_TOKEN,
});

const analyticsData = new BetaAnalyticsDataClient({ authClient: oauth2Client });
```

Search Console API (reuse the same oauth2Client):

```typescript
import { google } from "googleapis";
const searchconsole = google.searchconsole({ version: "v1", auth: oauth2Client });
```

Search Console site URL format for Domain-verified properties: `sc-domain:example.com`. For URL-prefix verified: `https://example.com/`.

---

## Instrumentation pattern

**Use static HTML installation. Never dynamic JS-based gtag injection.**

Dynamic injection (creating a `<script>` element via JavaScript at runtime, then appending to head) can fail to transmit beacons in production even when gtag.js loads and initializes correctly. The exact cause is not externally visible — gtag.js completes setup, dataLayer populates, `gtm.dom` and `gtm.load` events fire, but `/g/collect` POST requests silently never trigger. This failure was observed and confirmed during Nash Satoshi's launch debugging. Switching to static install resolved it immediately.

When advising on or auditing GA4 setup in any app, flag dynamic injection as the most likely cause of any "gtag loads but doesn't transmit" symptom.

### By framework

**Vite + React** (Nash Satoshi pattern):
- Canonical Google snippet placed in `client/index.html` as the first content in `<head>`
- Use Vite's `%VITE_GA4_MEASUREMENT_ID%` HTML substitution for the measurement ID
- Custom event helpers live in `src/lib/analytics.ts` and call `window.gtag('event', ...)` directly
- The analytics module should NOT inject the script tag — only install custom event listeners and expose typed helpers

**Next.js App Router** (Glow Index pattern):
- gtag setup placed in `app/layout.tsx` using Next.js `<Script strategy="afterInteractive">`
- Read measurement ID from `process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID`
- Wrap Script tags in a production gate (only render when `NODE_ENV === 'production'`)
- Custom event helpers live in `lib/analytics.ts`
- AnalyticsProvider component (if present) should NOT manage gtag loading — only custom routing/event logic

**Static HTML sites**:
- Paste canonical Google snippet directly into page template `<head>` immediately after the opening tag

### The canonical snippet

This is the pattern that works across all environments:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Note: no `{ send_page_view: false }` option. Let gtag auto-fire the initial page_view. Enhanced Measurement handles SPA navigation.

---

## Page view tracking on SPAs

GA4 Enhanced Measurement has a "Browser history changes" setting (enabled by default) that auto-tracks SPA route changes via pushState/popState. Works with Wouter (React+Vite) and Next.js App Router without any custom code.

Avoid the pattern of `send_page_view: false` plus manual `gtag('event', 'page_view', ...)` on every route change. It conflicts with Enhanced Measurement in subtle ways, adds maintenance burden, and is the second-most-common cause of mysterious GA4 issues after dynamic injection. Use vanilla `gtag('config', ID)` (no options) and rely on Enhanced Measurement.

---

## Property setup expectations for new apps

When a new app's GA4 property comes online, expect this sequence:

1. JT creates the property in his GA4 account and captures Property ID, Measurement ID, Domain
2. Measurement ID is set as an env var with the appropriate framework prefix (`VITE_*` for Vite, `NEXT_PUBLIC_*` for Next.js, etc.)
3. Static gtag snippet installed in the framework-appropriate location
4. Custom events tailored to that app's product surface, defined in a typed helpers module
5. Replit Deployment Secrets contain: framework-prefixed measurement ID (client bundle), `GA4_PROPERTY_ID` (server), and the three `GA4_OAUTH_*` values (server, shared across all properties)
6. Search Console domain added with DNS verification at the registrar (`sc-domain:` URL format)
7. Production transmission validated via DevTools Network in a Chrome guest window, filtering for `collect`

You should expect to receive a configuration update like the briefings JT sends, including:
- Property ID and measurement ID
- Domain
- List of custom events the app fires
- Status flag

Until status flips to "live", do not query that property.

---

## Custom events architecture

Each app's events must reflect its actual product surface. Generic templates rarely fit cleanly. Examples from the portfolio:

| App | Events |
|---|---|
| Nash Satoshi | rankings_view, token_detail_view, token_search, methodology_view, outbound_click, auth_modal_open, signup_success, checkout_started |
| Glow Index | paywall_viewed, checkout_started, sign_in_started, billing_portal_opened, view_product, vote_upvoted, vote_request_submitted, vote_seed_clicked |

Each event should fire at the exact call site where the user-meaningful action completes, not on intermediate UI changes. Strip undefined parameters before sending — GA4 rejects them.

For modal-open events that need to know where they were triggered from, the app should thread a `triggerLocation` prop through every call site explicitly, not infer from referrer.

---

## Conversion vs engagement weighting

Mark only actual conversions as key events in GA4 Admin → Events. Treat them as primary signal in attribution scoring.

Examples that should be key events: `signup_success`, `checkout_started`, `lead_submitted`, `subscription_activated`.

Examples that should NOT be key events: `page_view`, `item_view`, `search`, any engagement-by-volume event.

High-volume engagement events drown the conversion column if marked as key events and produce noise instead of signal.

Note: events must fire at least once in production before they appear in the Events list in GA4 Admin, which is when they can be marked as key events.

---

## Common pitfalls and what to flag

### 1. Crypto wallet extensions break gtag transmission

MetaMask, Phantom, Coinbase Wallet, and similar wallet extensions inject SES (Secure ECMAScript) lockdown scripts via `lockdown-install.js`. These scripts patch JavaScript intrinsics in a way that can interfere with gtag transmission, even though gtag.js itself loads correctly.

Practical implications:
- Always advise testing in Chrome guest mode (no extensions), not regular browsers
- Real users with crypto wallets installed experience 20-40% data loss
- For crypto-focused apps (Nash Satoshi, Action Arena, future tokens projects), consider building a Measurement Protocol server-side path as a redundancy. Server-side events bypass all client-side blockers.

### 2. Replit has separate workspace vs deployment secrets

Env vars must be set in the Deployment Secrets context, not just the Workspace Secrets, for production builds to pick them up. Workspace secrets only apply when running `npm run dev` in the editor.

If a deployment goes live and the client bundle is missing the measurement ID, this is the first place to check.

### 3. GA4 Realtime can lag or appear empty even when data flows

Realtime is supposed to show 30-second-fresh data but in practice has 1-2 minute lag, sometimes longer for brand-new properties. An empty Realtime view does not mean broken tracking.

The true validation is Reports → Engagement → Pages and screens after 24-48 hours of live traffic. That's where real user data definitively appears.

### 4. The "Receiving traffic in past 48 hours" status is a weak signal

The data stream UI shows this status if ANY events have arrived in the window. Could be from agent test events, curl checks, or one-off manual fires — not necessarily real production gtag from real users. Don't treat this status alone as proof of working production tracking.

### 5. Custom transport interceptors are dangerous

Any monkey-patching of `fetch`, `navigator.sendBeacon`, or `XMLHttpRequest` in the app's codebase can silently swallow gtag's network calls. This includes well-intentioned debug shims that log requests for development.

If a wrapper exists, it must forward calls to the original implementation. Pattern:

```typescript
const originalFetch = window.fetch;
window.fetch = function(...args) {
  // logging here
  return originalFetch.apply(this, args);  // CRITICAL: forward the call
};
```

When auditing an app's GA setup, grep the codebase for `sendBeacon`, `transport interceptors`, and `XMLHttpRequest.prototype.send` to surface any wrappers.

### 6. Dynamic gtag injection looks fine in dataLayer but fails to transmit

This is the specific failure mode that motivated the static-install rule. Symptoms:
- gtag.js loads successfully (visible in Network)
- `window.gtag` is a function
- `window.dataLayer` populates correctly with config and event entries
- `window.google_tag_manager['G-XXX']` initializes
- `gtm.dom` and `gtm.load` events appear in dataLayer
- BUT no `/g/collect` POST requests ever fire
- AND no `_ga`/`_ga_G-XXX` cookies get set

When you see this pattern, the immediate move is to switch to static installation. Don't waste time debugging the dynamic injection.

### 7. Search Console DNS propagation can take up to 48 hours

Schedule expectations accordingly. If a domain verification is pending and Search Console queries are blocked, that's normal — wait for propagation. URL-prefix verification via the GA4 measurement ID is a faster fallback once gtag is installed.

### 8. Custom domain on Replit and the `_ga` cookie

The `_ga` cookie is written by gtag.js to the apex domain. On Replit with a custom domain, make sure the cookie is being set on the actual apex (e.g., `.nashsatoshi.com`) and not the Replit deployment subdomain. Visible in DevTools Application → Cookies.

---

## App Marketing OS integration considerations

When a new property comes online, decide:

- **Query cadence**: hourly, daily, or on-demand? Higher cadence means fresher signal but more API quota usage. Daily is sufficient for most distribution-task scoring.
- **Which metrics matter**: typically `activeUsers`, `sessions`, `conversions per source/medium`, plus Search Console `impressions`, `clicks`, `queries`. Custom event counts for product-specific signals.
- **Attribution model**: how to credit directory/SEO/GEO efforts vs other channels. GA4 uses data-driven attribution by default, but for sparse early data, last-click may be more interpretable.
- **Conversion weighting**: which events should drive task scoring. Use the key-events list from GA4, not all custom events.
- **Self-improvement feedback loop**: how to track whether App Marketing OS tasks correlate with traffic/conversion changes. Weekly snapshots compared against task outcomes is one pattern.

Each app may need different settings. A high-volume content app needs different sampling than a low-volume B2B SaaS. Don't impose a single template.

For early-stage apps with low daily traffic (<100 users), expect noisy data. Smoothing windows of 7-14 days are more useful than daily snapshots for trend detection.

---

## Decision framework: do we instrument analytics for this app?

Default to yes. Specifically:

- Pre-launch waitlist or landing page → yes, install GA4 plus an event for primary CTA
- MVP launching to fewer than 100 users → yes, baseline establishment matters even at small scale
- Internal tool with no marketing surface → skip
- Throwaway prototype with no expected users → skip

Cost is roughly 30 minutes of setup if following the patterns in this document. Cost of missing data on the launch window is permanent.

For Opticfy client work, the equivalent question is: does the client need attribution and conversion data? If yes, install. Bill it as a deliverable.

---

## Current property registry

Maintain this as new properties come online. Source of truth for which properties are queryable.

| App | Property ID | Measurement ID | Domain | Status | Search Console |
|---|---|---|---|---|---|
| Nash Satoshi | 537280145 | G-BCVXQ3CYZS | nashsatoshi.com | live | verified |
| Glow Index | 537965547 | G-YH902137XF | glowindex.co | live | verified |
| jtsomwaru.com | 537855872 | G-EGPE6ZNQ56 | jtsomwaru.com | live | verified |
| Action Arena (future) | pending | pending | TBD | not started | pending |

Update when properties transition status, when new apps launch, or when measurement IDs change.

Stored reference path: `memory/app-marketing/ga4-integration-reference.md`. Keep `memory/app-marketing/account-map.json` in sync with the registry table above.
