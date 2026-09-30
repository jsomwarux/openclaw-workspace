# LinkedIn Manual Fixtures — Next-Wave Review Pack

**Date:** 2026-09-28

**State:** Superseded — Claude's 2026-09-29 adversarial review returned `CHANGES REQUIRED`. These packets are preserved as rejected review inputs and are not candidates for admission or publication. The replacement evidence is recorded in `reports/growth-os/2026-09-29-linkedin-manual-fixtures-review-reconciliation.md`.

**Authority:** Local drafting, rendering, and verification only. JT remains the sole publisher.

## Jobs correction

The approved plan initially treated Jobs commits `534673a…` and `e7e62e6…` as unfinished integration work. Repository handoff evidence showed both already descend into accepted repair `5e5902c…`, which was merged as `4f55916…`. Replaying or reintegrating those commits would duplicate accepted work. The next wave therefore moved directly to the two missing manual LinkedIn fixture modes.

## Fixture 1 — AppFolio × Column teardown

- **Packet:** `memory/content/linkedin-content-os/manual-fixtures/linkedin-teardown-appfolio-column-2026-09-28-v1/packet.v1.json`
- **Image:** `memory/content/linkedin-content-os/manual-fixtures/linkedin-teardown-appfolio-column-2026-09-28-v1/image.v1.png`
- **Primary source:** [AppFolio announcement](https://www.appfolio.com/newsroom/appfolio-and-column-announce-strategic-partnership-to-transform-financial-operations-for-real-estate?_storyblok_published=223315323218534), published September 24, 2026
- **Claim bindings:** 4/4 material public claims
- **Draft SHA-256:** `edb95876cb8422098c590b1474905a160161a5e358426b78e025c80baf425639`
- **Payload SHA-256:** `88681941a51975171fcdab2dc71fb6b8f7e2831005d31aa6ef008adc61643851`
- **Image SHA-256:** `534fb900b3c4f9bc5d8a92fe8e8ae8bc46aac0287d5b9981839211645c6debe6`
- **Expiry:** October 8, 2026 at 12:00 AM ET
- **Visual:** Original 1080×1350 system schematic labeled `Proposed system based on public information`; no source crop, screenshot, or logo

### Draft

> A property manager can close the books in one system while the money still sits in another.
>
> AppFolio's September 24 announcement says disconnected property-management and banking systems leave finance teams with manual reconciliation and fragmented payments. Its new Column partnership brings property data and accounting workflows together with bank-core, ledger, and payments infrastructure.
>
> Based only on that public information, the operating layer I would build is exception-first:
>
> 1. Bind each movement to a property, owner, and account.
> 2. Check approval and ledger context before it posts.
> 3. Route mismatches to a named human with the source attached.
> 4. Write the approved result back to the property record.
>
> If a mismatch has no owner before money moves, the systems are still disconnected where the risk lives.

## Fixture 2 — OpenAI external-access controls

- **Packet:** `memory/content/linkedin-content-os/manual-fixtures/linkedin-ai-news-openai-external-access-2026-09-28-v1/packet.v1.json`
- **Image:** `memory/content/linkedin-content-os/manual-fixtures/linkedin-ai-news-openai-external-access-2026-09-28-v1/image.v1.png`
- **Primary source:** [OpenAI Enterprise and Edu release notes](https://help.openai.com/en/articles/10128477-chatgpt-enterprise-and-edu-release-notes), update dated September 24, 2026
- **Claim bindings:** 4/4 material public claims
- **Draft SHA-256:** `83cf79051ab08fcc6837a01ca240e8f28c65de4f7790b0f402d357336e419e68`
- **Payload SHA-256:** `fd3b7a9cba821853e819d6b34f204495ed34ed0e1e820b871f482b738b30329e`
- **Image SHA-256:** `1e7f3c968ace8c29dd7252c40524b0c6012df340d6f70df49c51059e19902c2e`
- **Expiry:** September 29, 2026 at 11:59 PM ET
- **Visual:** Original 1080×1350 text-first source card; no OpenAI logo, screenshot, source crop, or proprietary artwork

### Draft

> An enterprise buyer reviewing an AI workflow should see four separate controls before it touches company data.
>
> OpenAI's September 24 Enterprise release notes give a concrete example. Global admins can separately control whether ChatGPT Sites use connected apps and whether applications access ChatGPT Ads.
>
> OpenAI also separates identity-only sign-in from data access. Workspace and individual app settings remain in the authorization chain, and both new permissions start off by default during preview.
>
> The operating model should make four decisions visible:
>
> • who can sign in
> • which source can be read
> • which action can run
> • when a human must approve it
>
> If one person cannot point to the data source, action scope, and human approval step, the access model is not ready for production.

## Deterministic verification

- Manual-fixture tests: 6/6 passed
- Full LinkedIn Content OS suite: 239/239 passed
- Python compilation: passed
- `git diff --check`: passed
- Exact replay: byte-identical for both packets and images
- Conflicting replay: refused
- Source freshness: enforced at 14 days for teardown and 5 days for public AI news
- Claim/source binding, image metadata, packet hashes, privacy, and rights: fail closed
- JT LinkedIn voice guard: 100/100 for both drafts
- Content distribution guard: passed for both drafts
- Secret-prefix scans: no matches
- Visual inspection: passed at original 1080×1350 resolution

## Boundaries

No Mission Control write, Drive upload, deployment, scheduling, recurrence, provider call, credential change, application, publication, or external send occurred. The packets remain local and unapproved. Independent review and JT's voice/usefulness/visual ratings are still required before any later admission decision.
