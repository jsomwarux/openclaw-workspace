# App Marketing OS — Optimization Rules

Last updated: 2026-05-12

Use this file before generating future app/product content.

## nash-satoshi / tiktok

### Reuse — validated net-positive only
- hook:contradiction (1 winner rows, net positive vs losers)
- topic:model_consensus (1 winner rows, net positive vs losers)
- specificity:high (1 winner rows, net positive vs losers)
- proof:model_names (1 winner rows, net positive vs losers)
### Conflicted — do not blindly reuse
- format:slideshow (winner rows 2, loser rows 8)
- topic:game_theory_explainer (winner rows 1, loser rows 1)
- specificity:low (winner rows 1, loser rows 6)
- proof:none (winner rows 1, loser rows 8)
- hook:specific_number_unexpected_context (winner rows 1, loser rows 2)
### Avoid / Rework
- format:slideshow (8 loser rows)
- proof:none (8 loser rows)
- topic:unclear (7 loser rows)
- hook:one_liner_gut_punch (6 loser rows)
- specificity:low (6 loser rows)
- hook:specific_number_unexpected_context (2 loser rows)
- specificity:medium (2 loser rows)
- topic:game_theory_explainer (1 loser rows)
### Generation Instruction
- Generate new posts by reusing only validated net-positive structures/topics. Do not reuse conflicted features without adding new proof, specificity, or tension.
- If a feature appears in both winners and losers, treat it as unresolved until it repeats with clean performance.

## nash-satoshi / x

### Conflicted — do not blindly reuse
- hook:specific_number_unexpected_context (winner rows 1, loser rows 2)
- topic:model_consensus (winner rows 1, loser rows 2)
- format:status_update (winner rows 1, loser rows 1)
- specificity:high (winner rows 1, loser rows 1)
- proof:model_names (winner rows 1, loser rows 2)
### Avoid / Rework
- specificity:low (4 loser rows)
- proof:none (3 loser rows)
- hook:specific_number_unexpected_context (2 loser rows)
- topic:model_consensus (2 loser rows)
- format:methodology_explainer (2 loser rows)
- proof:model_names (2 loser rows)
- hook:question_prompt (2 loser rows)
- format:question_prompt (2 loser rows)
### Generation Instruction
- Winner data exists, but no feature is net-positive yet. Treat winners as examples to study, not rules to copy.
- Keep testing one variable at a time and require stronger proof/tension before scaling.

## vista / tiktok

### Conflicted — do not blindly reuse
- topic:rating_precision (winner rows 2, loser rows 3)
- format:slideshow (winner rows 2, loser rows 8)
- proof:none (winner rows 2, loser rows 7)
- hook:specific_number_unexpected_context (winner rows 1, loser rows 3)
- specificity:high (winner rows 1, loser rows 1)
- hook:unclear (winner rows 1, loser rows 3)
- specificity:low (winner rows 1, loser rows 5)
### Avoid / Rework
- format:slideshow (8 loser rows)
- proof:none (7 loser rows)
- specificity:low (5 loser rows)
- topic:unclear (4 loser rows)
- hook:specific_number_unexpected_context (3 loser rows)
- hook:unclear (3 loser rows)
- topic:rating_precision (3 loser rows)
- specificity:medium (2 loser rows)
### Generation Instruction
- Winner data exists, but no feature is net-positive yet. Treat winners as examples to study, not rules to copy.
- Keep testing one variable at a time and require stronger proof/tension before scaling.
