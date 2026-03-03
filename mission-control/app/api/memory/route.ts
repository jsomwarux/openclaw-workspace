import { NextResponse } from "next/server";
import { readdirSync, readFileSync, existsSync, statSync } from "fs";
import { homedir } from "os";
import { join } from "path";

function searchInText(text: string, query: string): boolean {
  if (!query) return true;
  return text.toLowerCase().includes(query.toLowerCase());
}

function parseMemoryFile(filePath: string, fileName: string): any[] {
  const content = readFileSync(filePath, "utf-8");
  const stat = statSync(filePath);
  const sections: any[] = [];

  // Split by ## headings
  const parts = content.split(/^(#{1,3} .+)$/m);
  let currentTitle = fileName.replace(".md", "");

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (part.match(/^#{1,3} /)) {
      currentTitle = part.replace(/^#{1,3} /, "").trim();
    } else if (part.trim().length > 30) {
      sections.push({
        file: fileName,
        filePath,
        section: currentTitle,
        content: part.trim().slice(0, 500),
        preview: part.trim().slice(0, 120),
        mtime: stat.mtimeMs,
      });
    }
  }

  if (sections.length === 0 && content.trim().length > 30) {
    sections.push({
      file: fileName,
      filePath,
      section: fileName.replace(".md", ""),
      content: content.trim().slice(0, 500),
      preview: content.trim().slice(0, 120),
      mtime: stat.mtimeMs,
    });
  }

  return sections;
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get("q") ?? "";

  const workspace = `${homedir()}/.openclaw/workspace`;
  const memoryDir = join(workspace, "memory");
  const results: any[] = [];

  // Root .md files
  const rootFiles = ["MEMORY.md", "SOUL.md", "HEARTBEAT.md", "AGENTS.md", "TOOLS.md"];
  for (const file of rootFiles) {
    const fp = join(workspace, file);
    if (!existsSync(fp)) continue;
    const sections = parseMemoryFile(fp, file);
    results.push(...sections);
  }

  // Daily notes from memory/
  if (existsSync(memoryDir)) {
    const files = readdirSync(memoryDir)
      .filter(f => f.endsWith(".md") && /\d{4}-\d{2}-\d{2}/.test(f))
      .sort().reverse().slice(0, 14); // last 14 days

    for (const file of files) {
      const sections = parseMemoryFile(join(memoryDir, file), file);
      results.push(...sections);
    }
  }

  // Filter by query
  const filtered = query
    ? results.filter(r => searchInText(r.section + " " + r.content, query))
    : results;

  return NextResponse.json({ results: filtered.slice(0, 100), total: filtered.length });
}
