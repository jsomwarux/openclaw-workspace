import { existsSync, readFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { NextResponse } from "next/server";
import { hasNorthStarMetrics, parseNorthStarMetrics, parsePipelineJsonl } from "@/lib/mission-control/revenue";

function readWorkspaceFile(path: string) {
  const fullPath = join(homedir(), ".openclaw", "workspace", path);
  if (!existsSync(fullPath)) return "";
  return readFileSync(fullPath, "utf-8");
}

export async function GET() {
  const northStar = readWorkspaceFile("memory/north-star.md");
  const pipeline = readWorkspaceFile("memory/pipeline.jsonl");
  const sendQueue = readWorkspaceFile("memory/send-queue.md");

  return NextResponse.json({
    metrics: parseNorthStarMetrics(northStar),
    pipeline: parsePipelineJsonl(pipeline),
    sendQueue,
    // Parsing an unreadable or label-less file yields zeros. Callers need to tell
    // that apart from a genuine $0, so say plainly which sources actually parsed.
    available: {
      northStar: hasNorthStarMetrics(northStar),
      pipeline: pipeline.length > 0,
      sendQueue: sendQueue.length > 0,
    },
    sources: {
      northStar: "memory/north-star.md",
      pipeline: "memory/pipeline.jsonl",
      sendQueue: "memory/send-queue.md",
    },
  });
}
