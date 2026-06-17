import { existsSync, readFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { NextResponse } from "next/server";
import { parseNorthStarMetrics, parsePipelineJsonl } from "@/lib/mission-control/revenue";

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
    sources: {
      northStar: "memory/north-star.md",
      pipeline: "memory/pipeline.jsonl",
      sendQueue: "memory/send-queue.md",
    },
  });
}
