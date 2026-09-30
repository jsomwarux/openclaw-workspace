# LinkedIn Manual Fixtures — Claude Review Reconciliation

**Date:** 2026-09-29
**First reviewed commit:** `75d505896ee6ab86b00149507d75d6c578ebde3a`
**First Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 12 Important, 8 Minor
**Second reviewed commit:** `9b090fa27a551084eeee34c919a01e911a53c6bc`
**Second Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 5 Important, 10 Minor
**Third reviewed commit:** `c4aefeaba5847d3c0ad703489f6aa2234b6c1365`
**Third Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 3 Important, 7 Minor
**Current state:** Authority repair is builder-verified. Both fixtures are blocked pending a governed JT publication confirmation; there are zero accepted candidates. Fresh independent acceptance is still required.

## Third-review authority repair (2026-09-30)

### Root causes

1. **Caller-selected evidence paths.** `c4aefea` let the fixture spec choose the confirmation ledger file and trusted any `posted_confirmed` event in it. A self-consistent JSONL anywhere in the repository established authority, and a later governed retraction was ignored.
2. **Duplicated policy subsets.** Public-copy enforcement was a hand-maintained subset in `manual_fixtures.py`. Forbidden words, several canonical blocked phrases, statement-colon and non-Oxford colon lists, and exclamation points passed on every surface.
3. **Unpropagated governed-ledger mutation.** `c4aefea` appended `history-public:fabf927a…` (`posted_confirmed`) and `publication:fabf927a…` to `outcomes.v1.jsonl`. That broke Program 0's whole-file receipt bindings, so the approved verifier failed with `bound receipt byte hash mismatch`. Program 0's `audit-history` also refuses the extended ledger with `empty authority allowlist requires all status_unknown human-gate answers`: JT's governed human-gate response of 2026-09-28 answered `still_unknown` for exactly this legacy row, and the builder capture overrode it without a governed path.

### Decision

JT chose to restore the approved ledger and hold both fixtures. The two builder-appended events were removed; `outcomes.v1.jsonl` is byte-identical to the Program 0 approved bytes again (`e27dc5bbef8eae4baf2e5788f076aac09d94147faba96dce30e37b554660e953`, 25 events). The only governed route to `posted_confirmed` is JT answering the human gate for legacy row `fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf` as posted with its public URL and final text, ingested through `ingest-human-gate` with its boundary capture in a separately approved run.

### Repair

- Earned-angle authority resolves only the canonical ledger `memory/content/linkedin-content-os/outcomes.v1.jsonl` beneath the fixed repository root. `confirmationPath`, `confirmationExcerpt`, and `confirmationFileSha256` are removed from the spec contract; the spec carries only `kind`, `path`, `excerpt`, and `fileSha256`.
- Status comes from Program 0's latest-wins `_governed_evidence`; the source row comes from Program 0's `_legacy_row_hash` over the strict, contained posted log. The packet binds `legacyRowSha256`, the exact publication event ID and hash, the public URL, the final-text hash, and the ledger prefix hash and position through the last event for that row. Unrelated later events keep packets valid; any later event for the row forces re-derivation.
- Lock files open with `O_NOFOLLOW`; a planted lock symlink raises `lock path must not be a symlink` without creating the target. The posted log and canonical ledger reject symlink components.
- `scripts/linkedin_content_os/content_policy.py` is the single public-copy authority, applied to post, eyebrow, title, subtitle, stages, footer, attribution, and alt text. It encodes the content-voice Forbidden Words, the hard-banned hooks (Questions 2, 3, 5, 7), named slogan pairs, contrarian-setup and importance bans, the content-rules originality and internal-machinery blocks, the Stop Slop delta patterns, and the punctuation rules (em dash, exclamation point, repeated question marks, hashtags, prose colons, numbered lists, noun stacks, tricolon negation, happened/changed/worked-when closings).
- The teardown copy now reads "I start with one employee request and follow it from intake through outcome."
- The rejected `c4aefea` packet/image pairs were removed from the tracked tree and recorded by hash in `accepted-set.v1.json` `rejectedArtifacts`. Both specs are recorded under `blockedCandidates` with their SHA-256, the exact block reason, and the unblock requirement.

### Verification (builder evidence, not acceptance)

- RED before production changes: 8/8 authority, filesystem, and lock regressions failed for the reviewed reasons; 129/129 policy examples, 1,032 surface cases, and 161 fixture-surface cases failed.
- Focused manual-fixture and content-policy suites: 39/39 passed.
- Full `test_linkedin_content_os*.py` suite: 272/272 passed with `TMPDIR=/private/tmp/linkedin-authority-repair-20260930` (real path).
- Program 0 `audit-history`, `build-corpus`, and `verify` through the canonical CLI with network denied: every regenerated artifact is byte-identical to the approved tracked bytes; `verify` returned `program-0-local-proof-ready-for-independent-verification` with 101 `status_unknown` rows, `boundaryPairsEqual: true`, and `liveOrExternalActionOccurred: false`.
- Both tracked specs fail against the canonical ledger with `earned angle source row is not governed posted_confirmed (latest status: status_unknown)`.
- In an isolated copy with synthetic governed confirmation, both specs build and replay byte-identically, conflicting replays are refused, and the rendered PNGs equal the `c4aefea`-reviewed images (`992f8e781fa4bed559a17923c1ae2596ba3162840c7bb40a685ac0abb3b742d8`, `51f98d10833f690b278a404beffff07004586fb7cfada7a9ec7ae100544f2d86`). Image swap, forged ledger prefix, forged URL, and later retraction are rejected.
- JT voice guard 100/100 and content distribution guard PASS for both posts; the content policy reports no violation on any public surface of either spec.
- Original-resolution inspection of both 1080×1350 renders: text inside the safe area, centered numerals, stage order matching post and alt text, accurate footer attribution.
- Credential-pattern scan over added lines: only the synthetic `token=abc123` policy example and the policy's own secret regex.

## Replacement decision

The AppFolio teardown was retired because the active Altmark/property-operations adjacency could not be cleared from silence. The stale September 24 OpenAI item was also retired. Neither rejected packet is an admission or publication candidate.

Blocked candidates (no tracked packets; build only after governed confirmation):

- `linkedin-teardown-servicenow-inry-2026-09-29-v1`
  - Source: exact ServiceNow/INRY primary-story permalink, September 23, 2026
  - Source spec SHA-256: `fa046d43f54477103f031cbaafb624e0ec0245a3d8cadb5ca20a81df43181d13`
  - Rejected `c4aefea` artifact: draft `827ef257…`, payload `0fd9b0d3…`, image `992f8e78…`
- `linkedin-ai-news-openai-health-2026-09-29-v1`
  - Source: OpenAI ChatGPT release notes, September 28, 2026; evidence window ends `2026-10-02T23:59:59-04:00`
  - Source spec SHA-256: `862adc7da14e8059cb69c43a9e40b3d3f1063c5605d9b756aa5edafb84dcb6fd`
  - Rejected `c4aefea` artifact: draft `1462c850…`, payload `16620a18…`, image `51f98d10…`

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

1. Earned-angle authority now resolves through the append-only governed outcome ledger. It requires a `posted_confirmed` history event, one exact `publication_acknowledged` event, the real LinkedIn URL, exact final text, and matching source/final-text hashes. The retired builder-authored confirmation file is no longer authoritative. (Superseded 2026-09-30: the third review found the ledger path was still caller-selected and the appended events contradicted JT's human-gate answer; see the authority repair above.)
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
