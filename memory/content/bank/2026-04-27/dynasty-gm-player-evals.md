# Dynasty GM Player Evaluation Posts — 2026-04-27

## Status: INVALIDATED / DO NOT POST

JT caught a source-comparability flaw in the first version of this pack.

Problem:
- KTC `2552` was a source-specific trade value, not overall rank.
- FantasyCalc `233` was also a source-specific trade value, not RB rank.
- DynastyProcess `37` was also a value on its own scale.
- Those values are not apples-to-apples across sources.

Correct Kendre Miller snapshot after schema audit:
- KeepTradeCut: value 2552, overall rank 257, RB69
- FantasyCalc: value 233, overall rank 366, RB90
- FantasyPros: overall rank 341, RB91
- DynastyProcess: value 37, overall rank ~240, RB~68

Correct interpretation:
- KTC and DynastyProcess are closer on rank/position rank.
- FantasyCalc and FantasyPros are lower.
- This is a rank-disagreement candidate, not proof that KTC is wildly overpricing him by raw value.

System fix applied:
- Added FantasyPros consensus rankings as a primary source.
- Kept KTC as primary.
- Kept FantasyCalc as primary.
- Demoted DynastyProcess to secondary sanity check.
- Updated `sports_gm_generate_report.py` to compare ranks/position ranks, not raw cross-source values.

Do not use the prior Kendre/Rashod/Jaylen/Ja'Tavion drafts without rebuilding them under the corrected methodology.
