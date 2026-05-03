# Autoresearch Checklist — portfolio-card

Evaluate the portfolio-card skill against realistic project-card update tasks.

Answer yes/no for each test case:

1. Does the skill require a preflight check before editing the portfolio repo?
2. Does it verify whether the project already exists before adding a new card?
3. Does it include concrete build/verification steps before claiming success?
4. Does it guard against common schema/component mismatches in `projects.ts` and `Work.tsx`?
5. Does it include deployment/production verification rather than stopping at local edits?
6. Does it avoid uploading or publishing externally when prerequisites such as Drive/Vercel access are missing?
