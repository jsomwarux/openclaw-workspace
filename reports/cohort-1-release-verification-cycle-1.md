# Cohort-one release verification — cycle 1

VERDICT: FAIL

1. **The proof boundary is contradicted by current release artifacts.**
   - Canonical card says runtime is unverified and forbids human pre-send approval claims: `docs/standards/proof-assets/coi-tracking.md:5-10,16-17,52,59-60,75-77`.
   - Section 7 nevertheless says each rewritten proof sentence “still leaves the approval with a person”: `reports/cohort-1-review.md:293-298`.
   - Manifest still calls it a “live COI tracking system”: `reports/cohort-1-manifest.json:875-877`.
   - All five source briefs likewise call it live and claim approval remains with a person: `reports/cohort-1-briefs/community-access.md:55-65`, `goddard-riverside.md:55-65`, `voa-gny.md:55-65`, `westhab.md:55-65`, `comunilife.md:55-65`.
   - The five actual M1 proof sentences themselves are source-export-supported historical build descriptions and contain no live/runtime, named-client, outcome, or metric claim: `reports/cohort-1-send-sheet.md:33-35,66-68,103-105,138-140,171-173`.

2. **Four of five M1s violate their binding 80-word minimum.**
   - Every standalone brief requires 80–130 words, e.g. `reports/cohort-1-briefs/community-access.md:74-94`; the same rule is at line 78 in all five briefs.
   - Current counts are P1 75, P2 75, P3 75, P4 76, P5 80: `reports/cohort-1-review.md:364-371,422-429,492-499,555-562,613-620`.
   - The release test incorrectly enforces 75–150 instead: `scripts/tests/test_cohort_send_release.py:17-21`.

3. **Source-freshness disclosures are false/incomplete.**
   - P2’s brief requires the 336-day age or plain-language equivalent: `reports/cohort-1-briefs/goddard-riverside.md:31-40,92`; its M1 supplies neither a year, month, closure date, nor age: `reports/cohort-1-send-sheet.md:65-68`.
   - Manifest falsely records `age_disclosed_in_m1: true`: `reports/cohort-1-manifest.json:280-286`.
   - P4’s source date is only inferred from HTTP `last-modified`; its brief requires hedging and forbids presenting publication date as established: `reports/cohort-1-briefs/westhab.md:31-40,96-103`. M1 asserts “Westhab posted ... in August”: `reports/cohort-1-send-sheet.md:137-140`.
   - Section 7 itself admits the date is inferred but claims every M1 states age correctly: `reports/cohort-1-review.md:312-317,528-540`.

4. **The five M1s fail structural-independence requirements.**
   - Cold-email skill requires 3–4 structurally distinct opener formats and no consecutive default: `/Users/jtsomwaru/.openclaw/workspace/skills/cold-email/SKILL.md:287`.
   - All five use the same chassis: salutation, dated company signal, inferred workflow question, COI proof paragraph, final open question. The report itself identifies this fixed chassis and penultimate proof slot: `reports/cohort-1-review.md:1427-1442,1468-1472`.
   - Independent lexical comparison found maximum cross-prospect overlap of six consecutive words, so the eight-word ceiling passes; structural/template diversity does not.

5. **The M1s do not satisfy mandatory cold-email delivery rules.**
   - Email signatures are required: `/Users/jtsomwaru/.openclaw/workspace/skills/cold-email/SKILL.md:332`. All five M1s omit one: `reports/cohort-1-send-sheet.md:31-36,64-69,101-106,136-141,169-174`.
   - Every M1 must contain an individual-specific signal or explicitly note none: skill line 395. All five use company-level signals only, with no such note in the send sheet.
   - M1 CTA must be answerable in five words or fewer: skill line 393. All five ask process-explanation questions rather than reply-sized checks: send sheet lines `35,68,105,140,173`.
   - Subjects pass: all are lowercase, internal-looking, and three words: send sheet lines `27,60,97,132,165`.
   - Voice otherwise passes: no em dashes, corporate filler, client names, metrics, links, attachments, or meeting asks in the M1s.

6. **Report → manifest → send-sheet byte parity passes, but semantic state is stale and contradictory.**
   - `extract_cohort_manifest.py --check` and `build_send_sheet.py --check` both pass.
   - Manifest still says the fifth clean pass is pending: `reports/cohort-1-manifest.json:867-870`.
   - Manifest metadata still says P4 has no subject and `subject_line` is null: `reports/cohort-1-manifest.json:888-893`, while current P4 subject is present at line 507 and send sheet line 132.
   - Section 7 directs readers to §11.5 for current verification: `reports/cohort-1-review.md:286-291`, but §11.5 contains superseded counts and claims all M1s are 80–130 and all ages disclosed: `reports/cohort-1-review.md:1592-1603`.

7. **Named-buyer/channel boundaries and signal-to-question logic pass.**
   - P1/P2 use verified individual mailboxes; P3/P4/P5 use published organizational mailboxes explicitly labeled gatekeeper/inferred: `reports/cohort-1-review.md:303-310,333-344,393-404,459-469,523-533,584-594`.
   - Each company signal connects coherently to its final question, and inferred pain is asked rather than asserted.
   - No unsupported client outcome, result, metric, testimonial, or named-client claim appears in any M1.

8. **Tests pass but are insufficient release guards.**
   - `scripts/tests/test_cohort_send_release.py:17-53` checks only 75–150 words, a narrow banned-phrase list, subjects, and proof labels.
   - It does not test the briefs’ 80–130 requirement, actual source-age disclosure, inferred-date hedging, signatures, individual signals, CTA effort, structural rotation, report/manifest/send-sheet parity, stale metadata, or report-level live/approval claims.
   - `scripts/tests/test_proof_asset_card.py:31-61` checks only the card, so it cannot catch contradictions in the report, briefs, manifest, or send sheet.

9. **Exact commands/results.**
   1. `python3.12 -m unittest scripts.tests.test_proof_asset_card scripts.tests.test_cohort_send_release -v`  
      Result: exit 0; 9 tests; `OK`.
   2. `python3.12 -m unittest discover -s scripts/tests -v`  
      Result: exit 1; 117 collected; 7 import errors because `jsonschema` was unavailable.
   3. `PYTHON=python3.12 bash scripts/bootstrap.sh`  
      Result: exit 2; Homebrew Python rejected both system and `--user` installation under PEP 668.
   4. Temporary Python 3.12 venv outside the repo, install `requirements.txt`, then `/tmp/cohort-release-verify.cpnDab/venv/bin/python -m unittest discover -s scripts/tests -v`  
      Result: exit 0; 385 tests; `OK (skipped=1)`.
   5. `python3.12 scripts/extract_cohort_manifest.py --check`  
      Result: exit 0; `manifest matches the report: 5 packets, 15 messages`.
   6. `python3.12 scripts/build_send_sheet.py --check`  
      Result: exit 0; `send sheet matches the manifest: 5 prospects, 15 messages`.
   7. `/tmp/cohort-release-verify.cpnDab/venv/bin/python scripts/ci/check_test_count.py`  
      Result: exit 0; `OK — 385 test(s) collected, matching the committed count (was 376).`
   8. Independent manifest audit  
      Result: M1 counts `75,75,75,76,80`; one question each; zero em dashes; zero signatures; all subjects three lowercase words; longest pairwise lexical overlap six words.
   9. `git status --short` before and after verification  
      Result: identical pre-existing dirty state; verifier modified no repository files.

10. **All failures.**
   1. Current/live runtime language remains in manifest and all five briefs.
   2. Section 7 falsely says the proof leaves approval with a person.
   3. P1–P4 are below the binding 80-word minimum.
   4. P2 omits mandatory signal-age disclosure while manifest marks it present.
   5. P4 presents an inferred publication month as established instead of hedging.
   6. Five M1s share one structural template despite mandatory opener rotation.
   7. All five cold-email M1s lack required signatures.
   8. All five lack individual-specific signals or explicit no-signal notes.
   9. All five CTAs exceed the mandatory reply-sized standard.
   10. Manifest contains stale P4 subject metadata and a pending fifth-pass state.
   11. §11.5 contains superseded, false verification claims while §7 points to it as authoritative.
   12. Release tests false-green because they omit the binding constraints above.
