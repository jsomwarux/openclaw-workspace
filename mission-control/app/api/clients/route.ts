/**
 * Read-only join for the Clients lane: the clients table + each client's linked
 * payments (and collected total) + client-scoped active tasks (by clientId) +
 * on-disk status text and proof-asset filenames from memory/clients/<slug>/.
 *
 * GET /api/clients → { clients: [...] }
 */
import { existsSync, readdirSync, readFileSync, statSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "@/convex/_generated/api";

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
const WORKSPACE = join(homedir(), ".openclaw", "workspace");

export const dynamic = "force-dynamic";

// First non-empty prose line after any heading — a one-line on-disk status.
function statusExcerpt(memoryPath?: string): { path: string; excerpt: string } | null {
  if (!memoryPath) return null;
  const dir = join(WORKSPACE, memoryPath);
  for (const name of ["status.md", "README.md"]) {
    const full = join(dir, name);
    if (!existsSync(full)) continue;
    const lines = readFileSync(full, "utf8").split("\n");
    const excerpt = lines.find((l) => l.trim() && !l.startsWith("#") && !l.startsWith("---"))?.trim() ?? "";
    return { path: `${memoryPath}/${name}`, excerpt };
  }
  return null;
}

function proofAssets(memoryPath?: string): string[] {
  if (!memoryPath) return [];
  const dir = join(WORKSPACE, memoryPath, "proof-assets");
  if (!existsSync(dir)) return [];
  try {
    return readdirSync(dir).filter((f) => {
      try {
        return statSync(join(dir, f)).isFile();
      } catch {
        return false;
      }
    });
  } catch {
    return [];
  }
}

const WEEK_MS = 7 * 24 * 60 * 60 * 1000;

export async function GET() {
  const [clients, payments, active, archived] = await Promise.all([
    convex.query(api.clients.list, {}).catch(() => []),
    convex.query(api.payments.list, {}).catch(() => []),
    convex.query(api.tasks.listActive, {}).catch(() => []),
    convex.query(api.tasks.listArchived, {}).catch(() => []),
  ]);

  const weekAgo = Date.now() - WEEK_MS;

  const enriched = clients.map((client) => {
    const clientPayments = payments.filter((p) => p.clientId === client._id);
    const collected = clientPayments
      .filter((p) => p.cleared && p.kind === "consulting")
      .reduce((sum, p) => sum + p.amount, 0);

    const mine = active.filter((t) => t.clientId === client._id);
    const openTasks = mine.filter((t) => t.status !== "done" && t.status !== "archived");
    const done = mine.filter((t) => t.status === "done");
    const completedThisWeek = done.filter((t) => (t.updatedAt ?? 0) >= weekAgo);
    // Older completions: done > 7d ago plus any archived task still carrying the link.
    const olderCompletions = [
      ...done.filter((t) => (t.updatedAt ?? 0) < weekAgo),
      ...archived.filter((t) => t.clientId === client._id),
    ];
    const openDollars = openTasks.reduce((sum, t) => sum + (t.dollars ?? 0), 0);

    return {
      ...client,
      payments: clientPayments,
      collected,
      openDollars,
      openTaskCount: openTasks.length,
      openTasks,
      completedThisWeek,
      olderCompletions,
      statusFile: statusExcerpt(client.memoryPath),
      proofAssets: proofAssets(client.memoryPath),
    };
  });

  return NextResponse.json({ clients: enriched });
}
