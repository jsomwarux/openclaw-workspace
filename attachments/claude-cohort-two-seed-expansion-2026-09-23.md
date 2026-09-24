# Claude Code Controller — Cohort-Two Verified Seed Expansion

Run Claude Code on the Mac Mini from `/Users/jtsomwaru/projects/n8n-agent`, then paste everything below verbatim.

```text
You are the autonomous implementation controller for JT Somwaru's cohort-two verified seed-universe expansion.

Repository:
- repo: /Users/jtsomwaru/projects/n8n-agent
- remote: https://github.com/jsomwarux/n8n-agent.git
- required base: origin/main at 41ef3bfb49dd6a0579377355cc5d0af7ce442093
- design: /Users/jtsomwaru/.openclaw/workspace/plans/2026-09-23-cohort-two-seed-expansion.md
- handoff: /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json

Before editing:
1. Read CLAUDE.md and tasks/lessons.md completely.
2. Fetch origin and verify origin/main is exactly 41ef3bfb49dd6a0579377355cc5d0af7ce442093. Stop BLOCKED if it differs.
3. Verify `gh repo view jsomwarux/n8n-agent --json visibility,isPrivate` reports PRIVATE.
4. Read the design file completely.
5. Create an isolated worktree at `/Users/jtsomwaru/.openclaw/workspace/.worktrees/n8n-cohort-two-seed-expansion` on branch `eve/cohort-two-seed-expansion` from exact origin/main. Do not modify the user's main checkout.
6. Reproduce the current defects before implementation:
   - roster entries have no verified-host contract;
   - roster-only candidates depend on guessed domains;
   - N03 does not fully validate roster evidence;
   - N33 tells JT to review five prospects when records_written < 5.

Task:
Implement the approved design exactly. This is a bounded seed-evidence, validation, candidate-host, and card-copy change. Do not redesign discovery, pagination, gates, ranking, model prompts, output schemas, or downstream authority.

Required provider candidates (14):
1. Center for Urban Community Services — cucs.org — https://www.cucs.org/
2. FACES NY — facesny.org — https://www.facesny.org/services
3. Odyssey House — odysseyhousenyc.org — https://odysseyhousenyc.org/nyc-housing/
4. Unique People Services — uniquepeopleservices.org — https://uniquepeopleservices.org/about-us/
5. HELP USA — helpusa.org — https://www.helpusa.org/contact/
6. Housing Plus Solutions — housingplusnyc.org — https://housingplusnyc.org/
7. Housing Works — housingworks.org — https://www.housingworks.org/housing
8. Lower Eastside Service Center — lesc.org — https://www.lesc.org/contact/
9. Praxis Housing Initiatives — praxishousing.org — https://www.praxishousing.org/about/
10. The Fortune Society — fortunesociety.org — https://fortunesociety.org/services-that-build-lives/
11. West Side Federation for Senior and Supportive Housing — wsfssh.org — https://wsfssh.org/
12. Women In Need — winnyc.org — https://winnyc.org/supportive-housing/
13. Samaritan Daytop Village — samaritanvillage.org — https://www.samaritanvillage.org/permanent-housing/
14. Transitional Services for New York — tsiny.org — https://www.tsiny.org/about-us/

Official corroborating lists:
- https://www.nyc.gov/site/nycccoc/projects/PSH.page
- https://www.nyc.gov/site/hra/help/15-15-initiative.page
- https://www.nyc.gov/assets/hpd/downloads/pdfs/services/2023-december-qualified-list.pdf

Implementation requirements:
A. Evidence and generation
- Use read-only public GETs only to the official organization sites above and NYC government/Open Data hosts.
- Do not call any model or third-party enrichment/search API.
- Extend the checked-in roster derivation/validation tooling rather than hand-editing generated evidence.
- Re-derive authoritative geography from NYC HPD `feu5-w2e2` and `tesw-yqqr` using the lane's existing normalized-name and CorporateOwner/Agent rules.
- A candidate that cannot be tied reproducibly to NY/NJ geography and official supportive-housing evidence must be omitted and reported; never guess or weaken validation.
- At least 10 of the 14 candidates must survive. If fewer than 10 survive, stop BLOCKED and report the unresolved candidates rather than changing scope.
- Upgrade the complete roster, including the existing nine entries, to `c2-seed-roster-v2`.

B. Roster v2 contract
Every entry must carry:
- unique non-empty `name`;
- 1-3 unique `verified_hosts`, lowercase registrable hosts only: no scheme, path, port, wildcard, IP, localhost, or denied host;
- `segment_evidence` with HTTPS `source_url`, UTC `verified_at`, and concise factual `claim`;
- authoritative `geography` with NY/NJ `business_state`, non-empty NYC `boros`, reproducible source URLs, matched corporation names and registration IDs, and UTC verification timestamp.
Evidence timestamps must not be in the future and must fit the lane's 30-day source-age ceiling.

C. N03 fail-closed validation
Validate the complete v2 contract before any fetch/model call. Reject wrong schema/shape, empty roster, duplicate normalized names, duplicate hosts across organizations, malformed/denied hosts, missing/stale/future/non-HTTPS evidence, invalid geography, empty borough evidence, and missing registration identities.

D. N09 candidate construction
- Roster candidates use only `verified_hosts`; generate no name-derived guesses for them.
- Roster-only candidates inherit roster business_state and borough evidence.
- If a current non-empty HPD state conflicts with verified roster state, fail closed. A missing current state may fall back to the roster fact.
- Non-roster HPD candidates retain existing domain derivation.
- Do not change caps, G0-G4, ranking, exactly-five/all-or-nothing, or recheck semantics.

E. N33 truthful card copy
- Exact-five branch keeps the five-prospect review/commit instructions.
- Any 0-4 branch must say no usable cohort exists, must not ask JT to review or approve five prospects, must link the run receipt/short-cohort evidence, and must make the next action diagnosis/universe expansion.

F. Generated artifacts and docs
- Update authored sources first, then regenerate rendered nodes/workflow JSON using the checked-in generators.
- Never hand-edit a generated artifact.
- Update README/FINDINGS/runbook only where counts or contracts became stale.
- Keep main/error workflows inactive and preserve zero send-capable nodes and disabled schedule/Mission Control/heartbeat nodes.

TDD and verification:
1. Add failing tests before implementation for every new contract.
2. Focused tests must cover:
   - wrong roster version/shape;
   - malformed, denied, duplicate, cross-org duplicate, or absent hosts;
   - stale/future/non-HTTPS evidence;
   - missing/conflicting geography;
   - roster-only business_state/borough propagation;
   - verified-host ordering with no guessed roster domains;
   - unchanged derived hosts for non-roster candidates;
   - exact-five card copy;
   - 0, 1, and 4 prospect card copy;
   - generated-source/render equality.
3. Run the derivation tool and prove at least 10 new organizations survive with reproducible evidence.
4. Run focused tests during development.
5. At the apparent final SHA, run the full bootstrapped suite with zero failures and zero skips, workflow generation/equality, topology, inactive/no-send guards, credential/PII scan, repository visibility, and clean worktree.
6. Launch one fresh non-builder review in a clean clone at the exact SHA. The reviewer must attack evidence provenance, host ownership, schema bypasses, duplicate hosts/names, stale/future timestamps, geography conflicts, generated-file drift, empty-card truthfulness, activation/send boundaries, and test-corpus non-emptiness.
7. If FAIL, repair only reproduced defects test-first and repeat with a fresh reviewer. Maximum two repair cycles. A new architecture decision or third failure stops HUMAN_DECISION/BLOCKED.
8. On CONFIRM, push exact confirmed SHA, open/update a PR against main, and wait for available checks. Do not merge or deploy.

Prohibited:
- touching live n8n, live cohort state, credentials, secrets, OpenClaw config, or Mission Control;
- model calls, third-party enrichment/search APIs, real outreach, drafting, sends, activation, schedules, heartbeat, suppression capability, or a pilot run;
- broadening beyond supportive-housing providers in NYC/NY;
- modifying the installed n8n package;
- merging the PR.

Handoff JSON must include:
- status: COMPLETE | BLOCKED | HUMAN_DECISION | BLOCKED_NOTIFICATION;
- repo, base SHA, branch, final SHA, PR URL;
- exact surviving new provider count and names;
- omitted/unresolved candidates and reasons;
- focused/full/zero-skip/generation/topology/security/visibility results;
- fresh reviewer verdict and reviewed SHA;
- proof workflows remain inactive/send-free;
- blockers, next_owner, exact_next_action.

Write the handoff to:
/Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json

Then notify Eve with acknowledged delivery:
openclaw system event --session-key agent:main:telegram:direct:6608544825 --text "Claude lane cohort-two-seed-expansion: <STATUS>; handoff at /Users/jtsomwaru/.openclaw/workspace/memory/job-state/claude-seed-expansion.json" --mode now --expect-final --json

Inspect the returned JSON and require acknowledged/final delivery. Retry exactly once if delivery is not acknowledged. If the second attempt is not acknowledged, set status `BLOCKED_NOTIFICATION` in the handoff and stop; do not falsely report that Eve was notified.

Terminal response: one line only — status + handoff path.
```
