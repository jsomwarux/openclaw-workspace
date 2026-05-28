---
name: portfolio-card
description: Adds or updates project cards on jtsomwaru.com — edits projects.ts, adds screenshots, builds and deploys to Vercel, uploads to Google Drive. Use when JT says "add this to the portfolio", "add a portfolio card", "add to jtsomwaru.com", "update the site with this project", "portfolio card for", or when a build is complete and needs to be added to the personal website. NOT for: coding the project itself (use coding-agent), writing general site copy, or any page other than the /work project cards.
---

# SKILL: Portfolio Card Addition
*Done 5+ times in one week — follow this exactly, no re-derivation needed.*

---

## Step 0: Preflight Check (Run This First)

Run the preflight script before touching any files. It validates the repo, TypeScript compile, and screenshot presence deterministically.

```bash
bash ~/.openclaw/workspace/skills/portfolio-card/scripts/preflight.sh [project-slug]
# Example: bash ~/.openclaw/workspace/skills/portfolio-card/scripts/preflight.sh nash-satoshi
```

If it exits non-zero: fix the reported errors before continuing. Do NOT proceed past a failed preflight.

## Step 1: Prerequisites
- Repo: `~/projects/jtsomwaru-com/`
- Key file: `src/data/projects.ts`
- Graphics: `src/components/project-graphics/index.tsx`
- Layout: `src/components/Work.tsx`
- Vercel auto-deploys on push to `main`

Run `git pull origin main` first if there's any chance the repo is behind.

## Step 1a: Existing Card + Access Gate
Before adding anything new, search `src/data/projects.ts` for the requested project slug, title, and obvious aliases.
- If the card already exists, update only the requested fields; do not create a duplicate project entry or duplicate graphic component.
- If a required external action cannot be verified, stop and report the blocker instead of publishing partial work. Examples: missing Drive file access for a demo video, no usable Vercel/deploy visibility, or a failed `git push`.

---

## Step 1: Define the card data
Every project entry in `projects.ts` follows this shape:
```ts
{
  slug: "kebab-case-unique-id",
  title: "Display Title",
  category: "automation" | "agentforce" | "product",
  featured: true | false,          // featured: true = shows in top 2; excess goes to "view more"
  demoVideo: "https://drive.google.com/file/d/FILE_ID/preview",  // optional
  description: "1-2 sentence description.",
  tags: ["tag1", "tag2", "tag3"],
  outcomes: [
    "Outcome statement 1",
    "Outcome statement 2",
    "Outcome statement 3",
  ],
  graphic: "ComponentName",        // must match export in project-graphics/index.tsx
}
```

**Featured cap rule:** Work.tsx caps featured at 2 per section. Setting `featured: true` on a 3rd card in the same category is fine — it will appear in "view more," not break the layout.

**Google Drive video URLs:** Convert share URL to embed format:
- Share: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- Embed: `https://drive.google.com/file/d/FILE_ID/preview`

---

## Step 2: Add the entry to projects.ts
Find the correct section (automation / agentforce / product) in `src/data/projects.ts`.
Insert the new object. Maintain consistent formatting.

If adding a `demoVideo` field to an existing card: just add the field, don't touch the rest.

---

## Step 3: Build the graphic component (new cards only)
Every new card needs a React graphic component. Skip this step if updating an existing card.

Open `src/components/project-graphics/index.tsx`. Add:
```tsx
export function YourProjectGraphic() {
  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-[color1] to-[color2] rounded-lg p-6">
      {/* SVG or simple layout showing the workflow */}
      {/* Keep it minimal — 3-4 nodes connected by arrows works for every automation demo */}
    </div>
  );
}
```

Pattern for automation demos: show 3-4 boxes with right-arrows between them. Input → Process → Output(s). Labels match the real workflow. Color scheme: use teal/blue/slate for n8n, purple for Agentforce, green for product.

Reference any existing graphic (e.g., `SupportTriageGraphic`) for exact structure.

---

## Step 4: Wire the graphic in Work.tsx (new cards only)
In `src/components/Work.tsx`, find the graphic rendering section.
Add the import and the conditional render for the new slug. Same pattern as all other entries.

---

## Step 5: Build and verify
```bash
cd ~/projects/jtsomwaru-com
npm run build
```

Fix any TypeScript errors before pushing. Common issues:
- Missing export in project-graphics/index.tsx
- `graphic` field in projects.ts doesn't match component name exactly
- `demoVideo` field added to a project where the type doesn't include it (check Project interface)

---

## Step 6: Commit and push
```bash
git add -A
git commit -m "feat: [describe what was added/updated]"
git push origin main
```

Vercel deploys automatically. Confirm deploy succeeds (check Vercel dashboard or wait ~90s and visit jtsomwaru.com).

---

## Step 7: Report back to JT
Include:
- What was added/changed
- Whether it's featured or in "view more"
- Vercel deploy status (auto-deploying / deployed)
- If a demo video was added: remind JT the Drive file must be "Anyone with link can view"
