# LinkedIn Manual Fixtures — Claude Review Reconciliation

**Date:** 2026-09-29
**First reviewed commit:** `75d505896ee6ab86b00149507d75d6c578ebde3a`
**First Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 12 Important, 8 Minor
**Second reviewed commit:** `9b090fa27a551084eeee34c919a01e911a53c6bc`
**Second Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 5 Important, 10 Minor
**Current state:** Second bounded repair is builder-verified; fresh independent acceptance still required.

## Replacement decision

The AppFolio teardown was retired because the active Altmark/property-operations adjacency could not be cleared from silence. The stale September 24 OpenAI item was also retired. Neither rejected packet is an admission or publication candidate.

Replacement packets:

- `linkedin-teardown-servicenow-inry-2026-09-29-v1`
  - Source: exact ServiceNow/INRY primary-story permalink, September 23, 2026
  - Draft: `827ef257c9801ac2d59e6c7c43f58eb51c86d67a8810d8420618bff82481c17a`
  - Payload: `0fd9b0d316e0cd2c656fe3dad3138dcfadbdf8b98c69dd905715dfeed587cdf7`
  - Image: `992f8e781fa4bed559a17923c1ae2596ba3162840c7bb40a685ac0abb3b742d8`
- `linkedin-ai-news-openai-health-2026-09-29-v1`
  - Source: OpenAI ChatGPT release notes, September 28, 2026
  - Draft: `1462c8503619bd74dfc615f764d1e4aabd81af4a63d492f4191e92a71173a02e`
  - Payload: `16620a18f4cb02bc2c3fef96014295d096e2469305e64b8074476ef92a89bfa2`
  - Image: `51f98d10833f690b278a404beffff07004586fb7cfada7a9ec7ae100544f2d86`

## Important findings closed locally

1. Source freshness is recomputed during build and validation; packet expiry cannot exceed the earliest source window.
2. Validation re-derives the full normalized contract instead of trusting packet-owned hashes and pass strings.
3. Packet and revision IDs are slug-only before any filesystem path is constructed.
4. Earned angles bind exact source bytes, exact excerpts, and a dedicated immutable posted-confirmation record.
5. Teardown packets require all five closed conflict results; the conflicted AppFolio candidate was replaced.
6. Every material claim is an exact span of both its frozen source excerpt and the outbound post, with recorded offsets.
7. The AI-news replacement contains one fully bound public claim and separates source fact from JT interpretation.
8. The AI visual credits OpenAI only for the source fact and labels the operating model as JT's lens.
9. Prohibited contrast constructions, colon-led lists, blocked semantic repeats, and internal terms fail closed across public text surfaces.
10. The teardown copy now uses a concrete employee-request scene and labels the proposed workflow as a hypothesis.
11. Post, visual, and alt text use the same stage order.
12. Renderer minimum sizes, overflow checks, safe areas, and numeral centering were hardened and visually inspected.

## Second-review findings closed locally

1. Earned-angle authority now resolves through the append-only governed outcome ledger. It requires a `posted_confirmed` history event, one exact `publication_acknowledged` event, the real LinkedIn URL, exact final text, and matching source/final-text hashes. The retired builder-authored confirmation file is no longer authoritative.
2. Validation deterministically re-renders `visualRoute` and requires byte equality with the tracked PNG. Renderer identity records Pillow plus regular/mono font hashes and is hash-bound into the packet.
3. Every existing path component is checked for symlinks before build or validation; resolved-root containment is mandatory. Exclusive packet locks and orphan-asset refusal prevent unsafe overwrite races.
4. One canonical public-text guard covers post, title, subtitle, stages, footer, alt text, and attribution surfaces with the full prohibited machinery and voice-shape block list.
5. The ServiceNow teardown cites the exact primary-story permalink. Its date, deployment window, and portal-replacement claims are exact source/post spans; the unsupported statement about what the page omitted was removed.

Adjacent findings absorbed: official-release claims require `vendor_assertion`; conflict checks bind hash-addressed evidence records; `createdAt` cannot predate retrieval; horizontal word and eyebrow overflow fail closed; stage/footer sizes increased for mobile legibility; the AI footer distinguishes JT's lens from the source; both packet families start honestly at v1; tracked candidate packets and PNGs replay byte-identically; dates are claim-bound; the teardown language gives JT the action; and both closing lines were revised.

## Verification

- Focused manual-fixture suite: 24/24 passed.
- Full LinkedIn Content OS suite: 257/257 passed with real-path `/private/tmp` `TMPDIR`.
- Python compilation and `git diff --check`: passed.
- JT voice guard: 100/100 for both posts; content distribution guard passed for both.
- Exact replay, hostile tamper probes, and tracked-artifact equality: passed.
- Governed outcome ledger validation: 27/27 events accepted.
- Scoped credential-pattern scan: no matches.
- Original-resolution visual inspection: completed for both 1080×1350 PNGs; hierarchy, stage order, alignment, and source/JT separation are readable without overlap.

## Closed gates

No Mission Control write, Drive upload, deployment, schedule, recurrence, provider call, credential change, application, publication, or external send occurred. Local green evidence is not independent acceptance. A fresh Claude review of the immutable repair commit is still required.
