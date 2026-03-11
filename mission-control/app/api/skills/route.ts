import { NextResponse } from "next/server";
import { existsSync, readdirSync, readFileSync, statSync } from "fs";
import { homedir } from "os";
import path from "path";

const HOME = homedir();
const WORKSPACE_SKILLS = path.join(HOME, ".openclaw/workspace/skills");
const BUNDLED_SKILLS   = "/opt/homebrew/lib/node_modules/openclaw/skills";

type Skill = {
  slug:        string;
  name:        string;
  description: string;
  source:      "custom" | "bundled";
  commands:    string[];
  files:       string[];
  hasScript:   boolean;
  version:     string | null;
};

/** Extract description from SKILL.md — handles both YAML front-matter and markdown headings */
function parseSkillMd(content: string): { description: string; commands: string[] } {
  // YAML front-matter description
  const yamlDesc = content.match(/^---[\s\S]*?^description:\s*[>|]?\s*\n?([\s\S]*?)(?=^\w|\n---)/m);
  let description = "";
  if (yamlDesc) {
    description = yamlDesc[1]
      .split("\n")
      .map(l => l.trim())
      .filter(Boolean)
      .join(" ");
  }

  // Fallback: first paragraph after first heading
  if (!description) {
    const lines = content.split("\n");
    let pastHeading = false;
    for (const line of lines) {
      if (!pastHeading && line.startsWith("#")) { pastHeading = true; continue; }
      if (pastHeading && line.trim() && !line.startsWith("#") && !line.startsWith("---")) {
        description = line.trim();
        break;
      }
    }
  }

  // Commands — look for a table in "Available Commands" section or ## Commands
  const commands: string[] = [];
  const cmdSection = content.match(/##\s+(Available )?Commands[\s\S]*?(?=^##|\Z)/m);
  if (cmdSection) {
    const tableRows = cmdSection[0].matchAll(/\|\s*(`\/[\w-]+`|\/[\w-]+)\s*\|/g);
    for (const row of tableRows) {
      commands.push(row[1].replace(/`/g, "").trim());
    }
  }

  return { description: description.replace(/\s+/g, " ").trim(), commands };
}

function loadSkillsFromDir(dir: string, source: "custom" | "bundled"): Skill[] {
  if (!existsSync(dir)) return [];

  const skills: Skill[] = [];

  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const slug = entry.name;
    const skillDir = path.join(dir, slug);
    const skillMdPath = path.join(skillDir, "SKILL.md");
    if (!existsSync(skillMdPath)) continue;

    const content = readFileSync(skillMdPath, "utf8");
    const { description, commands } = parseSkillMd(content);

    // List notable files (non-SKILL.md, non-hidden, non-node_modules)
    let files: string[] = [];
    try {
      files = readdirSync(skillDir)
        .filter(f => f !== "SKILL.md" && !f.startsWith(".") && f !== "node_modules")
        .filter(f => {
          try { return statSync(path.join(skillDir, f)).isFile(); } catch { return false; }
        });
    } catch { /* ignore */ }

    // Version from _meta.json if present
    let version: string | null = null;
    try {
      const meta = JSON.parse(readFileSync(path.join(skillDir, "_meta.json"), "utf8"));
      version = meta.version ?? null;
    } catch { /* none */ }

    const hasScript = files.some(f => /\.(ts|js|py|sh)$/.test(f));

    // Human-readable name: strip common suffixes, title-case
    const name = slug
      .replace(/-/g, " ")
      .replace(/\b\w/g, c => c.toUpperCase());

    skills.push({ slug, name, description, source, commands, files, hasScript, version });
  }

  return skills.sort((a, b) => a.slug.localeCompare(b.slug));
}

export async function GET() {
  const custom  = loadSkillsFromDir(WORKSPACE_SKILLS, "custom");
  const bundled = loadSkillsFromDir(BUNDLED_SKILLS,   "bundled");
  return NextResponse.json({ custom, bundled });
}
