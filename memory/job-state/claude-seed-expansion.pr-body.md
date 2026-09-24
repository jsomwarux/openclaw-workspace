## Summary

D16: the cohort-two seed roster moves to a verified v2 (`c2-seed-roster-v2`). Every roster organization now has verified hosts, host evidence, segment evidence and HPD geography, each timestamped. N03 validates all of it. N09 fetches only verified hosts. The N33 short-run card now reports what the run actually produced.

- **Roster:** 20 organizations: 7 of cohort one's 9, plus **13 new verified providers**: Center for Urban Community Services, FACES NY, Odyssey House, Unique People Services, HELP USA, Housing Plus Solutions, Housing Works, LESC (Lower Eastside Service Center), Praxis Housing Initiatives, The Fortune Society, Women In Need, Samaritan Daytop Village, Transitional Services for New York. Three candidates are omitted with recorded reasons: West Side Federation, Housing and Services, Inc., and Urban Pathways.
- **N03:** a single shared validator (`seedRoster` block in `src/lib/shared.js`) enforces the whole roster contract, and every rule fails closed. Evidence ages out after 30 days (it expires 2026-10-23T22:32:59Z).
- **N09:** a roster candidate fetches only its verified hosts; nothing is guessed from its name. If any of the organization's CorporateOwner/Agent HPD rows disagrees on state, the run stops.
- **N33:** a 0–4 record run gets a truthful "no usable cohort (k of 5 qualified)" card. The exact-five card is byte-identical to before.

## Repair cycles (each defect reproduced before the fix, test-first)

1. `0cb0ce7`: N09's conflict check only looked at the first-registration state of a framed candidate. It now checks every live row.
2. `7cf9e1d`: the validator accepted a blank borough (`boros: ['']`). It now refuses it, and roster entries whose own HPD rows disagree are excluded.
3. `d794397`: `isRegistrableHost` refuses hosts under the special-use/private TLDs `localhost`, `localdomain`, `local`, `internal`, `lan`, `home`, `corp`, `test`, `invalid`, `example`, `onion` and `arpa`. It compares the whole TLD, so `internal.org`, `example.org`, `.homes` and `.land` stay valid. The accepted grammar is unchanged otherwise, and there is no public-suffix dependency.

## Verification at `4e86de7904829fa96b6e46301f9df57750d7fb91`

- Full bootstrapped suite: **623 passed, 0 failed, 0 skipped**, run in the worktree and again in a clean clone.
- Running `render-src.js` and `build-workflow.js` leaves `git status` empty.
- Main workflow has 58 nodes and the error workflow has 4. Connections and settings are unchanged from base. The only Code bodies changed are N03, N09 and N33.
- Both workflows are `active: false`. T1, N39 and N43H are disabled. No node type in either workflow can send. Mission Control write is off, and the heartbeat is disabled.
- No credential patterns and no private IPs in the added lines. The only email-shaped strings are synthetic test inputs.
- Mutation testing: every new guard is killed by a named test.
- Fresh independent review at this exact SHA: **CONFIRM**, with no blocking defects.

## Not in this PR

Nothing is deployed, activated or scheduled. There were no live n8n calls, model calls or sends, and the installed n8n package is unchanged. Do not merge without JT's decision.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
