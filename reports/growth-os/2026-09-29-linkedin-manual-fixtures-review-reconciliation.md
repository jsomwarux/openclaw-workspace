# LinkedIn Manual Fixtures — Claude Review Reconciliation

**Date:** 2026-09-29
**First reviewed commit:** `75d505896ee6ab86b00149507d75d6c578ebde3a`
**First Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 12 Important, 8 Minor
**Second reviewed commit:** `9b090fa27a551084eeee34c919a01e911a53c6bc`
**Second Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 5 Important, 10 Minor
**Third reviewed commit:** `c4aefeaba5847d3c0ad703489f6aa2234b6c1365`
**Third Claude verdict:** `CHANGES REQUIRED` — 0 Critical, 3 Important, 7 Minor
**Current state:** JT's 2026-09-30 human-gate answer is governed through the new Program 0 supplemental correction path. Both fixtures are regenerated, bound to the canonical ledger authority, and listed as candidates pending independent review. This is builder evidence only; fresh independent acceptance is still required.

## Supplemental governed confirmation (2026-09-30, Addendum A)

### Answer governed

- **Legacy row:** `fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf`. JT's 2026-09-28 answer was `still_unknown`; on 2026-09-30 JT answered `posted` (`confirmedAt` 2026-09-30T09:01:38-04:00).
- **Public URL:** `https://www.linkedin.com/feed/update/urn:li:activity:7490053069380964353/`.
- **Final text:** 1,083 bytes, SHA-256 `fb2d82be18e796fdf3eb32dbb4c109792460aa2e90d86ea2fdbfa6b806b4bdea`. The byte length and hash were verified before any mutation and round-tripped through the supplement document.
- **Engagement snapshot:** the 2 likes / 2 comments snapshot is intentionally omitted. The governed `metric_snapshot` schema requires an observed `windowDays`, and the window is unknown.

### Why a new path

`ingest-human-gate` is a one-shot boundary and refused the answer (`phase-two run context predates confirmedAt`; `human-gate replay conflicts with the existing event block`). It is unchanged. The new closed command `ingest-history-correction` appends a supplemental block and never edits prior ledger bytes.

### Governed commands (from the worktree root)

1. `python3 -m scripts.linkedin_content_os.cli init-run --generated-at now --outcomes memory/content/linkedin-content-os/outcomes.v1.jsonl --output memory/content/linkedin-content-os/run-context.supplement-1.v1.json` → `generatedAt` 2026-09-30T13:46:48.234145+00:00, run ID `sha256:bedfa9f8366176463cbf8c4562c979dd983f6eb01d45ae700613c5e994a88766`.
2. `capture-boundaries --phase supplement-before --run-context …supplement-1… --mc-output …mission-control.snapshot.supplement-1.v1.json --output …boundaries.supplement-1.before.v1.json`. This makes one read-only loopback GET plus the cron inventory: Mission Control 54 tasks, 0 LinkedIn packets.
3. `ingest-history-correction --supplement …human-gate-supplement-1.v1.json --base-response …human-gate-response.v1.json --base-manifest …corpus-authority-manifest.v1.json --base-authority-run-context …run-context.phase-2-authority.v1.json --recovery-request …historical-recovery-request.phase-1.v1.json --outcomes …outcomes.v1.jsonl --run-context …run-context.supplement-1.v1.json --corpus-authority-manifest-output …corpus-authority-manifest.supplement-1.v1.json --authority-run-context-output …run-context.supplement-1-authority.v1.json`.
4. `audit-history` and then `build-corpus`, both under `corpus-authority-manifest.supplement-1.v1.json` / `run-context.supplement-1-authority.v1.json`, writing the canonical phase-2 paths.
5. `capture-boundaries --phase supplement-after` with the same run context.
6. `verify` with the approved phase-1-fresh and phase-2-replacement pairs plus all six supplement arguments.

### Ledger linkage

- **Before:** `e27dc5bb…660e953`, 25 events. **After:** `10a7b5bf4b45573b2df5ffcdef6c34df646c14ec752e6e79d0ef61ba787ca732`, 29 events. The approved 25-event prefix is preserved byte-for-byte.
- **Preserved target:** `history:fabf927a…` (`status_unknown`), `efdce6b62d51133b261f4b6b1426bb4aa529459273f68174caa2e27f1b6f8e86`.
- **Replacement:** `history-supplement-1:fabf927a…` (`posted_confirmed`), `0f829647ddda7a6ba3cd27b78d4c584c009c94833737f1ffb181d22393b70057`.
- **Publication:** `publication-supplement-1:fabf927a…`, `22c5512b6f76f46c676131a9ef7b45f2916fe644e1e50f46d1614f3bfcc35976`.
- **Exact-text receipt:** `authority-supplement-1:fabf927a…`, `0fddd8d77da1af2f938b941f70e8c0b4236a2e32ff26befe5fa70b155c041cc9`. Its fresh corpus run ID is `22f32fd051f10c96d2816610bba444263eda5f45ace7a512498c22e89f3c68fb`.
- **Correction:** `correction-supplement-1:fabf927a…`, which targets the preserved event with the replacement hash: `22356a769973587033f7cafd1817f3235f976cb3bebbd9855b736508ef74d2f1`.

### Authority artifacts

| Artifact | Before | After |
|---|---|---|
| Supplement document | — | `40a368e64b7675f37bbec3410fce8851a8d3562ebd33b006d01605108d007229` |
| Supplement manifest (file / `manifestSha256`) | — | `624429279edc…` / `f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf` |
| Supplement authority context | — | `3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb` |
| Supplement run context | — | `e461a1c566655f8d23a0101e015050b111bf2c0a7a2daac55ed742a2bc06add5` |
| Supplement boundaries (before / after) | — | `227319012527…` / `e838c3f7fb9a…` (governed values equal) |
| Base manifest, base authority context, focus receipt/anchor | unchanged | unchanged |
| `historical-audit.v1.json` | `a0b66794f739…` | `c9f6b666b906…` |
| `historical-recovery-request.v1.json` | `62deff6d0e48…` | `2086eab6a4ac…` |
| `authority-consumption.phase-2-audit.v1.json` | `7bcbaa2af794…` | `76caa21bd222…` |
| `authority-consumption.phase-2-corpus.v1.json` | `a6b617375527…` | `c01fb3e13090…` |
| `voice-gold.v0.jsonl` | `6a489405bf58…` | `69f80dd463c0…` |
| `contrastive-pairs.v0.jsonl` | `6a489405bf58…` | `6262b750eaa9…` |
| Program 0 report | `f1eeabcb7b60…` | `bdc1557ec523…` |

The prior phase-2 artifacts remain recoverable at `d4c3bcd8906cc18648b7eecb935d5971a759073c`.

### Program 0 verification

- **Verdict:** `program-0-local-proof-ready-for-independent-verification`.
- **Status counts:** `posted_confirmed` 1, `status_unknown` 100, `not_posted_confirmed` 0. Missing URL 0 and missing final text 0.
- **Corpus:** voice gold 1 (text `fb2d82be…`), contrastive pairs 0.
- **Human gate:** 23 answers; `humanGateResolved` true.
- **Boundaries:** three equal run-bound pairs (phase-1-fresh, phase-2-replacement, supplement-1); `liveOrExternalActionOccurred` false.
- **Unchanged derivatives:** `build-focus`, phase-2 `build-fixtures`, and `preview-checkin` reran byte-identically, so the focus authority artifacts are unchanged.

### Fixtures

Both specs' `createdAt` moved to 2026-09-30T09:48:00-04:00, after the governed authority was recorded. Both packets were built twice plus a replay, byte-identically, promoted, and validated in place against the canonical ledger. Each binds `publication-supplement-1:fabf927a…`, the ledger prefix `10a7b5bf…` at position 29, the URL, the final-text hash `fb2d82be…`, and the source draft `2ed35201…`.

| Packet | Spec | Draft | Payload | Image |
|---|---|---|---|---|
| `linkedin-teardown-servicenow-inry-2026-09-29-v1` | `6daa1f9c…` | `fc246d1270730c965a280da72227e6fde54b85a9e0c8aace7102066cb6c437f4` | `a694c694ebe2fb406e73fe47f30ae2cbe50d5861cd64bc67f6331cd9470f1102` | `992f8e781fa4bed559a17923c1ae2596ba3162840c7bb40a685ac0abb3b742d8` |
| `linkedin-ai-news-openai-health-2026-09-29-v1` | `d22416ba…` | `5be5bbbc41ef47242f4e18319fabd550e09f136b9f5b6724771da99d8fd29d75` | `c8033d0335a057af00710585a4b0b86a38a9198863f64ef81e837838240543b9` | `51f98d10833f690b278a404beffff07004586fb7cfada7a9ec7ae100544f2d86` |

The AI-news evidence is valid at regeneration: it expires 2026-10-02T23:59:59-04:00, with 62 hours remaining at 09:48 ET.

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
