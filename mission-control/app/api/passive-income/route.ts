import { NextResponse } from "next/server";
import { existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { loadPassiveIncomeIdeas } from "@/lib/mission-control/passive-income";

export async function GET() {
  const dir = join(homedir(), ".openclaw/workspace/memory/passive-income");

  if (!existsSync(dir)) {
    return NextResponse.json({ ideas: [], error: "Directory not found" });
  }

  return NextResponse.json({ ideas: loadPassiveIncomeIdeas(dir) });
}
