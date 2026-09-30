# LinkedIn Manual Fixtures — Claude Review Reconciliation

**Date:** 2026-09-29
**Base reviewed commit:** `75d505896ee6ab86b00149507d75d6c578ebde3a`
**Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 12 Important, 8 Minor
**Current state:** Local repair verified; fresh independent acceptance still required.

## Replacement decision

The AppFolio teardown was retired because the active Altmark/property-operations adjacency could not be cleared from silence. The stale September 24 OpenAI item was also retired. Neither rejected packet is an admission or publication candidate.

Replacement packets:

- `linkedin-teardown-servicenow-inry-2026-09-29-v2`
  - Source: ServiceNow newsroom, September 23, 2026
  - Draft: `6d764b4245739c285e1a565f19b5b91df8bede1745aafcc6de44fe587aeebf7a`
  - Payload: `4f9cd79a807487e46ff5191dc23c9a473765609b8b35887281f1d122f64afcc7`
  - Image: `0f04e93e3420a6399f3a8b34f55e7489f065729f947fee41e0c1edff275b612b`
- `linkedin-ai-news-openai-health-2026-09-29-v2`
  - Source: OpenAI ChatGPT release notes, September 28, 2026
  - Draft: `943dd02bf1cdeb232d8a4aabf45b5274c441bb1645c247516b802f519c49ce13`
  - Payload: `17778cf6b312f6420eca6ac350241328e6a84417464b70133a3cfc01ef5a034d`
  - Image: `7da35d1ff586034207c58d8c104b6848c38e04ad55a122010d43295fb1f397b6`

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

Minor findings absorbed now: obsolete `edit`/`hold` decisions were replaced by `approve`/`reject`/`skip`; the full suite uses a resolved real-path `TMPDIR`; symlink assets and wrong packet asset paths fail closed; deterministic font absence fails closed.

## Verification

- Focused manual-fixture suite: 12/12 passed.
- Full LinkedIn Content OS suite: 245/245 passed with real-path `TMPDIR`.
- Python compilation: passed.
- `git diff --check`: passed.
- JT voice guard: 100/100 for both posts.
- Content distribution guard: passed for both posts.
- Exact replay and conflicting-replay behavior: passed.
- Hostile tamper classes: forged QA, internal text, lane relabel, bogus claim, stale source, traversal ID, symlink asset, forged angle, and overlong expiry all rejected.
- Original-resolution visual inspection: passed for both 1080×1350 PNGs.

## Closed gates

No Mission Control write, Drive upload, deployment, schedule, recurrence, provider call, credential change, application, publication, or external send occurred. Local green evidence is not independent acceptance. A fresh Claude review of the immutable repair commit is still required.
