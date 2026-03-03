import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const LOGS_DIR = path.join(process.env.HOME!, ".openclaw/workspace/agents/overnight/logs");
const QUEUE_FILE = path.join(process.env.HOME!, ".openclaw/workspace/agents/portfolio-updater/queue.jsonl");
const WORKSPACE = path.join(process.env.HOME!, ".openclaw/workspace");

function parseLog(content: string, filename: string) {
  const date = filename.replace("-log.md", "");
  const modelMatch = content.match(/\*\*Model:\*\*\s*([^\s|]+)/);
  const subagentsMatch = content.match(/\*\*Sub-agents used:\*\*\s*([^\s\n]+)/);
  const costMatch = content.match(/## Total Estimated Cost:\s*~?\$?([\d.]+)/);

  const completedTasks: Array<{
    name: string; output?: string; whatWasDone?: string;
    reviewNeeded?: string; cost?: string;
  }> = [];

  const completedSection = content.match(/## Tasks Completed([\s\S]*?)(?=## Tasks Skipped|## Total|$)/);
  if (completedSection) {
    const taskBlocks = completedSection[1].split(/### ✅/).filter(b => b.trim());
    for (const block of taskBlocks) {
      const lines = block.split("\n");
      const name = lines[0].trim();
      const outputMatch = block.match(/\*\*Output:\*\*\s*`([^`]+)`/);
      const doneMatch = block.match(/\*\*What was done:\*\*\s*([^\n]+)/);
      const reviewMatch = block.match(/\*\*Review needed:\*\*\s*([^\n]+)/);
      const costMatch2 = block.match(/\*\*Estimated cost:\*\*\s*([^\n]+)/);
      completedTasks.push({
        name, output: outputMatch?.[1],
        whatWasDone: doneMatch?.[1]?.trim(),
        reviewNeeded: reviewMatch?.[1]?.trim(),
        cost: costMatch2?.[1]?.trim(),
      });
    }
  }

  const skippedTasks: Array<{ name: string; reason: string }> = [];
  const skippedSection = content.match(/## Tasks Skipped([\s\S]*?)(?=##|$)/);
  if (skippedSection) {
    const skippedLines = skippedSection[1].match(/- \*\*([^*]+)\*\* — ([^\n]+)/g) || [];
    for (const line of skippedLines) {
      const m = line.match(/- \*\*([^*]+)\*\* — ([^\n]+)/);
      if (m) skippedTasks.push({ name: m[1].trim(), reason: m[2].trim() });
    }
  }

  const feedbackItems: string[] = [];
  const feedbackSection = content.match(/## Feedback Needed([\s\S]*?)(?=##|$)/);
  if (feedbackSection) {
    const items = feedbackSection[1].match(/\d+\.\s+[^\n]+/g) || [];
    feedbackItems.push(...items.map(i => i.replace(/^\d+\.\s+/, "").trim()));
  }

  const portfolioSection = content.match(/## Portfolio Updates([\s\S]*?)(?=##|$)/);
  const portfolioLines: string[] = [];
  if (portfolioSection) {
    const lines = portfolioSection[1].match(/- \*\*[^:]+:\*\*[^\n]+/g) || [];
    portfolioLines.push(...lines.map(l => l.trim()));
  }

  return {
    date, model: modelMatch?.[1] || "unknown",
    subagents: subagentsMatch?.[1] || "0/2",
    totalCost: costMatch?.[1] ? `$${costMatch[1]}` : "unknown",
    completedTasks, skippedTasks, feedbackItems, portfolioLines,
  };
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const action = searchParams.get("action");

  if (action === "file") {
    const filePath = searchParams.get("path");
    if (!filePath) return NextResponse.json({ error: "path required" }, { status: 400 });
    const fullPath = filePath.startsWith("/") ? filePath : path.join(WORKSPACE, filePath);
    if (!fullPath.startsWith(WORKSPACE)) return NextResponse.json({ error: "forbidden" }, { status: 403 });
    try {
      const content = fs.readFileSync(fullPath, "utf-8");
      return NextResponse.json({ content });
    } catch {
      return NextResponse.json({ error: "file not found" }, { status: 404 });
    }
  }

  if (action === "queue") {
    try {
      const content = fs.readFileSync(QUEUE_FILE, "utf-8");
      const items = content.trim().split("\n").filter(Boolean).map(line => {
        try { return JSON.parse(line); } catch { return null; }
      }).filter(Boolean);
      return NextResponse.json({ items });
    } catch {
      return NextResponse.json({ items: [] });
    }
  }

  try {
    if (!fs.existsSync(LOGS_DIR)) return NextResponse.json({ runs: [] });
    const files = fs.readdirSync(LOGS_DIR)
      .filter(f => f.endsWith("-log.md"))
      .sort().reverse();
    const runs = files.map(filename => {
      const content = fs.readFileSync(path.join(LOGS_DIR, filename), "utf-8");
      return parseLog(content, filename);
    });
    return NextResponse.json({ runs });
  } catch (err) {
    return NextResponse.json({ error: String(err) }, { status: 500 });
  }
}

export async function PATCH(req: Request) {
  const body = await req.json();
  const { id, status } = body;
  if (!id || !status) return NextResponse.json({ error: "id and status required" }, { status: 400 });
  try {
    const content = fs.readFileSync(QUEUE_FILE, "utf-8");
    const lines = content.trim().split("\n").filter(Boolean);
    const updated = lines.map(line => {
      try {
        const item = JSON.parse(line);
        const itemId = item.id || item.slug;
        if (itemId === id) {
          return JSON.stringify({ ...item, status, decidedAt: new Date().toISOString() });
        }
        return line;
      } catch { return line; }
    });
    fs.writeFileSync(QUEUE_FILE, updated.join("\n") + "\n");
    return NextResponse.json({ success: true });
  } catch (err) {
    return NextResponse.json({ error: String(err) }, { status: 500 });
  }
}
