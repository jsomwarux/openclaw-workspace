import { NextResponse } from "next/server";
import { readdirSync, readFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const limitParam = parseInt(searchParams.get("limit") ?? "20");
  const typeFilter = searchParams.get("type") ?? "";

  const proofsDir = `${homedir()}/.openclaw/workspace/proofs`;
  if (!existsSync(proofsDir)) return NextResponse.json({ entries: [] });

  const entries: any[] = [];

  // Read all YYYY-MM-DD dirs, most recent first
  const dates = readdirSync(proofsDir)
    .filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d))
    .sort()
    .reverse();

  for (const date of dates) {
    const file = join(proofsDir, date, "actions.jsonl");
    if (!existsSync(file)) continue;
    const lines = readFileSync(file, "utf-8").trim().split("\n").filter(Boolean);
    for (const line of lines.reverse()) {
      try {
        const entry = JSON.parse(line);
        if (typeFilter && entry.action_type !== typeFilter) continue;
        entries.push({ ...entry, date });
        if (entries.length >= limitParam) break;
      } catch {}
    }
    if (entries.length >= limitParam) break;
  }

  const types = [...new Set(entries.map(e => e.action_type))].sort();
  return NextResponse.json({ entries, types });
}
