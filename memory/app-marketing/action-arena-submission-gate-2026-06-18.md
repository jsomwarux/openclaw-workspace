# Action Arena Submission Gate
Date: 2026-06-18

## Current Finding
Action Arena is the timed app gate. The source/build path is now found and cloned locally.

Searches run:
- `find /Users/jtsomwaru/projects -maxdepth 4 -type d | rg -i '(action|arena|bet|pick|sports)'`
- `rg -n "Action Arena|fake budget|weekly fake|no real money|parlays|teasers" /Users/jtsomwaru/projects ~/.openclaw/workspace -g '!node_modules' -g '!*.sqlite' -g '!*.db'`

Result:
- GitHub repo found: `jsomwarux/action-arena` private app repo.
- Local app repo: `/Users/jtsomwaru/projects/action-arena`.
- Site repo: `/Users/jtsomwaru/projects/action-arena-site`.
- App repo latest observed commit: `5721ea7 Merge branch 'chore/reminder-cron-migration'`.
- App Store metadata exists at `/Users/jtsomwaru/projects/action-arena/docs/app-store-submission.md`.

## Submission Blocker
The exact blocker shifted from **source/build discovery** to **Apple Developer Organization transfer + EAS/TestFlight/App Store submission readiness**.

Found and fixed one build-readiness/security blocker:
- `eas.json` no longer hardcodes Supabase URL, Supabase anon key, or Odds API key in preview/production profiles.
- `package.json` now includes `eas-build-pre-build` so EAS runs `npm run prebuild:prod-check`.
- README and App Store submission docs now require EAS secrets for Supabase/Odds config.

Open blockers before acquisition spend:
- finish moving JT's Apple Developer membership from individual to organization under the LLC, because Action Arena includes in-app purchases and could not be submitted from the individual account;
- after the organization transfer clears, configure/confirm required EAS project secrets outside the repo;
- confirm App Store Connect/TestFlight app record and current build status under the correct organization account;
- produce or locate the next EAS preview/production iOS build;
- decide whether the remaining npm audit findings should be handled in a separate dependency-upgrade pass. Do not run `npm audit fix --force` inside the submission gate because it requires breaking Expo/React Native upgrades.

Do not create the optional paid UGC/creator test yet. That belongs after App Store approval/live state, attribution setup, and kickoff timing.

## Next Action
Wait for the Apple Developer Organization transfer to clear, then configure/verify EAS secrets and locate the App Store Connect/TestFlight record under the LLC organization.

Acceptable evidence:
- Apple Developer Program account/team shows the LLC organization membership active;
- TestFlight build number/status;
- App Store Connect app record/status;
- Expo/EAS project path or build dashboard;
- EAS secrets confirmed set for `EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY`, and `EXPO_PUBLIC_ODDS_API_KEY`.

## JT Ask If Eve Cannot Locate It
Send one concrete ask:

`I found the Action Arena source at /Users/jtsomwaru/projects/action-arena. Once the Apple Developer Organization transfer to the LLC clears, I need the App Store Connect/TestFlight or Expo/EAS project status next: app record, latest build number/status, or confirmation that EAS secrets are already set.`

## Verification
2026-06-18:
- `npm run typecheck` passed.
- `npm run prebuild:prod-check` passed.
- `npm run test:prod-mock-data-guard` passed.
- `npx expo export --platform ios --output-dir /tmp/action-arena-export` passed after reverting unsafe `npm audit fix` lockfile churn.
- Secret scan for the removed Supabase/Odds values returned no matches outside ignored dependencies/lockfile.
- `npm audit fix` was not kept because it introduced a nested React Native 0.86 tree and broke iOS bundling with `VirtualViewNativeComponent` syntax/event-argument failure.

## Acquisition Impact
This is different from the prior app marketing strategy because it removes the build/submission bottleneck before making more launch assets. User acquisition for Action Arena depends on a working install path; commissioner outreach, kickoff posts, and the capped creator test cannot convert if TestFlight/App Store submission is blocked or a production build ships mock data or exposed keys.

2026-06-18 update: JT is moving the Apple Developer membership from individual to organization under an LLC because Action Arena includes in-app purchases and could not be submitted from the individual account. This is now the first external gate before EAS secret confirmation and App Store submission status checks.

## Guardrails
- Deadline: submit by 2026-07-15 or pause until next preseason.
- Positioning: fake budget, real bragging rights, no real money.
- Do not use regulated betting/gambling language.
- No new features unless the named submission blocker requires code.
- Optional UGC: SideShift/Home From College only as a capped kickoff test after app live + per-creator attribution ready; 2-3 creators before scale.
