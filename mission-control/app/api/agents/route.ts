import { NextResponse } from "next/server";
import { existsSync, readdirSync, readFileSync } from "fs";
import { homedir } from "os";
import path from "path";

const HOME = homedir();
const DATA_FILE = path.join(HOME, ".openclaw/workspace/mission-control/data/agents.json");
const PROJECTS_DIR = path.join(HOME, "projects");

type AgentDef = {
  id: string;
  name: string;
  emoji: string;
  role: string;
  domain: string;
  workspaceRel: string | null;
  github: string | null;
  skills: string[];
  crons: { id: string; name: string; schedule: string }[];
  currentTask: string;
  created: string | null;
  pinned?: boolean;
};

function resolveWorkspace(rel: string | null): string | null {
  if (!rel) return null;
  return path.join(HOME, rel);
}

function resolveStatus(workspacePath: string | null): "active" | "planned" {
  if (!workspacePath) return "planned";
  return existsSync(workspacePath) ? "active" : "planned";
}

export async function GET() {
  // Load agent definitions from JSON config
  let defined: AgentDef[] = [];
  try {
    defined = JSON.parse(readFileSync(DATA_FILE, "utf8"));
  } catch {
    // Fall through to auto-discovery only
  }

  const knownIds = new Set(defined.map(a => a.id));

  // Auto-discover any ~/projects/ directories not in the config
  let discovered: AgentDef[] = [];
  try {
    const dirs = readdirSync(PROJECTS_DIR, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);

    for (const dir of dirs) {
      const id = dir;
      if (knownIds.has(id)) continue;
      discovered.push({
        id,
        name: dir.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
        emoji: "🤖",
        role: "Discovered Project",
        domain: `Auto-discovered at ~/projects/${dir} — add to agents.json to configure`,
        workspaceRel: `projects/${dir}`,
        github: null,
        skills: [],
        crons: [],
        currentTask: "Not yet configured in agents.json",
        created: null,
      });
    }
  } catch {
    // ~/projects/ may not exist — that's fine
  }

  // Combine and resolve
  const all = [...defined, ...discovered].map(a => {
    const workspacePath = resolveWorkspace(a.workspaceRel);
    return {
      id: a.id,
      name: a.name,
      emoji: a.emoji,
      role: a.role,
      domain: a.domain,
      workspace: workspacePath,
      github: a.github ?? null,
      status: resolveStatus(workspacePath),
      skills: a.skills ?? [],
      crons: a.crons ?? [],
      currentTask: a.currentTask ?? "",
      created: a.created ?? null,
    };
  });

  return NextResponse.json({ agents: all });
}
