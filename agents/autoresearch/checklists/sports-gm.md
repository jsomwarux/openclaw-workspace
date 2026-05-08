# Sports GM Autoresearch Checklist

Evaluate Sports GM outputs with yes/no answers:

1. Did the workflow fetch current market prices itself instead of asking JT for manual data pulls?
2. Are all player-specific recommendations backed by at least two market sources and one football/context source?
3. Does every recommendation include a confidence tier and risk case?
4. Are source disagreements framed as research candidates rather than automatic buy/sell calls?
5. If a public call is made, was a row added or prepared for `memory/sports-gm/receipts.csv`?
6. Does the content avoid generic rankings/waiver slop and stay in the GM/front-office positioning lane?
7. For @dynastyjig content packs, do at least 3 of 5 drafts mention a current player, rookie tier, team context, pick range, betting market, game context, or rank gap?
8. If fresh dynasty/betting signal is thin, does the output fail closed (`SKIP_PACK` / `BLOCKED`) instead of filling with generic rebuild/parlay psychology?
