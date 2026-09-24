# Cohort-Two Verified Seed Expansion

## Goal

Expand the exhausted nine-organization seed universe with at least 14 additional verified NYC supportive-housing providers, while removing domain guessing for roster candidates and making empty-run Mission Control copy truthful.

## Evidence-backed candidates

Each candidate below has both official supportive-housing evidence and a primary host. Geography must be re-derived from NYC HPD (`feu5-w2e2` + `tesw-yqqr`) with the existing strict role and normalization rules; unresolved or conflicting candidates are excluded rather than guessed.

| Organization | Primary host | Official segment evidence | Expected HPD identity family |
|---|---|---|---|
| Center for Urban Community Services | `cucs.org` | https://www.cucs.org/ | CENTER FOR URBAN COMMUNITY SERVICE(S) |
| FACES NY | `facesny.org` | https://www.facesny.org/services | FACES NY, INC / FACES NY HDFC |
| Odyssey House | `odysseyhousenyc.org` | https://odysseyhousenyc.org/nyc-housing/ | ODYSSEY HOUSE / ODYSSEY HOUSE, INC |
| Unique People Services | `uniquepeopleservices.org` | https://uniquepeopleservices.org/about-us/ | UNIQUE PEOPLE SERVICES variants |
| HELP USA | `helpusa.org` | https://www.helpusa.org/contact/ | HELP USA |
| Housing Plus Solutions | `housingplusnyc.org` | https://housingplusnyc.org/ | HOUSING PLUS / HOUSING PLUS SOLUTIONS |
| Housing Works | `housingworks.org` | https://www.housingworks.org/housing | HOUSING WORKS INC / HDFC variants |
| Lower Eastside Service Center | `lesc.org` | https://www.lesc.org/contact/ | LESC / LOWER EASTSIDE SERVICE CENTER |
| Praxis Housing Initiatives | `praxishousing.org` | https://www.praxishousing.org/about/ | PRAXIS HOUSING INITIATIVES INC variants |
| The Fortune Society | `fortunesociety.org` | https://fortunesociety.org/services-that-build-lives/ | FORTUNE SOCIETY INC / THE FORTUNE SOCIETY |
| West Side Federation for Senior and Supportive Housing | `wsfssh.org` | https://wsfssh.org/ | WEST SIDE FEDERATION variants |
| Women In Need | `winnyc.org` | https://winnyc.org/supportive-housing/ | WOMEN IN NEED variants |
| Samaritan Daytop Village | `samaritanvillage.org` | https://www.samaritanvillage.org/permanent-housing/ | SAMARITAN DAYTOP VILLAGE variants |
| Transitional Services for New York | `tsiny.org` | https://www.tsiny.org/about-us/ | TRANSITIONAL SERVICES FOR NEW YORK INC variants |

Common official NYC provider evidence:

- https://www.nyc.gov/site/nycccoc/projects/PSH.page
- https://www.nyc.gov/site/hra/help/15-15-initiative.page
- https://www.nyc.gov/assets/hpd/downloads/pdfs/services/2023-december-qualified-list.pdf

## Contract

### Seed roster v2

Every organization, including the existing nine, must have:

- a unique non-empty `name`;
- `verified_hosts`: one to three unique lowercase registrable hosts with no scheme, path, port, wildcard, IP literal, localhost, or denied-host match;
- `segment_evidence.source_url`, `segment_evidence.verified_at`, and a concise factual `claim` showing supportive/permanent housing work;
- existing authoritative `geography`, including a valid NY/NJ `business_state`, non-empty NYC borough list, re-runnable HPD URLs, matched corporation names and registration IDs, and `geography_verified_at`;
- evidence timestamps no later than run start and no older than the configured/authority 30-day source window.

The file schema becomes `c2-seed-roster-v2`. Generation/derivation tools must produce the file deterministically; generated artifacts may not be hand-edited.

### N03 preflight

Before any public GET or model call, N03 fails closed on:

- wrong roster schema or unexpected top-level shape;
- empty roster, duplicate normalized organization names, or duplicate verified hosts across organizations;
- missing/malformed/denied verified hosts;
- missing, stale, future, non-HTTPS, or malformed segment/geography evidence;
- missing/invalid NY/NJ geography, empty borough evidence, or missing registration identities.

### N09 candidate construction

- A roster candidate uses only its `verified_hosts`; no name-derived host guesses are generated for it.
- A roster-only candidate inherits the verified roster `business_state` and borough evidence, so G0 evaluates a known fact rather than an empty string.
- A live HPD match may fill missing current facts but may not silently contradict verified roster geography. A non-empty conflict fails closed.
- Non-roster HPD candidates keep the existing deterministic derived-host behavior.
- Existing candidate and page caps remain unchanged.

### N33 empty/short-run card

For fewer than five records, the card must not tell JT to review five prospects or approve a nonexistent cohort. It must state that no usable cohort exists, link the short-cohort/run receipts, and make the next action diagnosis or universe expansion. The exact-five branch retains the existing review/commit instructions.

## Verification

- TDD for roster v2, host validation, duplicate detection, stale/future evidence, geography conflicts, roster-only G0 inputs, verified-host priority, and truthful empty/short cards.
- At least 14 new candidates survive the derivation tool and v2 validator; unresolved candidates are omitted with a report.
- Source/render equality, workflow generation, offline/full suite, topology, inactive/no-send guards, credential/PII scan, visibility check, and zero skipped tests.
- One fresh non-builder review attacks evidence provenance, host ownership, schema bypasses, geography conflicts, generated-file drift, empty-card truthfulness, activation/send boundaries, and fixture coverage.
- No live deployment, pilot, model call, credential operation, schedule, activation, Mission Control write, heartbeat, suppression capability, draft, or send.

