# X Algorithm Signal — Alex Finn thread (2026-05-15)

Source: https://x.com/AlexFinn/status/2055312478469591441

Observed metrics at first pull: ~236K impressions, 1.3K likes, 163 reposts, 259 replies, 106 quotes, 1.6K bookmarks.

User-provided thread claims:
- Posts get positive and negative engagement scores.
- Positive signals include replies, reposts, photo clicks, profile clicks, shares, DM shares, copied links, and long dwell.
- Negative signals include fast scrolls, not interested, blocks, mutes, and reports.
- The feed tries to avoid showing too many posts by the same author; repeated posting can decay distribution.
- Ad-safety logic affects ranking.
- The algorithm looks for high-quality “bangers” and mentions category/tag/quality/slop scoring.
- Content labels such as NSFW, gore, and violence can dock distribution.
- AI slop, copied content, bait, and low-quality AI media are likely risky.

System implications adopted:
1. Add volume gate for X: one strong post per audience window beats several mediocre posts.
2. Add originality/slop gate: every X draft needs JT-specific proof, data, build experience, or verified source.
3. Add ad-safety/ragebait gate: avoid advertiser-hostile angles even if they could drive replies.
4. Keep source-teardown pattern, but require actual source inspection and saved evidence.
5. For Nash X, block proof:none/generic ranking updates and require live ranking delta, named token, model disagreement, market context, or methodology proof.

Caution:
Treat Alex Finn’s thread as useful creator/operator interpretation, not official documentation. Use the behavioral implications because they match existing observed X incentives, but do not make public claims like “the algorithm definitely does X” unless source-verified.
