/**
 * Search layer — hybrid semantic + keyword search
 */
import { Database } from "bun:sqlite";
import { embed, cosineSimilarity } from "./embed.ts";
import {
  getDb,
  getAllEmbeddings,
  keywordSearch,
  getItem,
  KbItem,
} from "./db.ts";

export type SearchMode = "semantic" | "keyword" | "hybrid";

export type SearchResult = {
  item: KbItem;
  score: number;
  mode: "semantic" | "keyword" | "both";
};

/**
 * Main search function. Hybrid by default.
 */
export async function search(
  query: string,
  opts: {
    category?: string;
    limit?: number;
    mode?: SearchMode;
  } = {}
): Promise<SearchResult[]> {
  const db = getDb();
  const limit = opts.limit ?? 10;
  const mode = opts.mode ?? "hybrid";

  const results = new Map<number, SearchResult>();

  // === Semantic Search ===
  if (mode === "semantic" || mode === "hybrid") {
    const queryVec = await embed(query);
    const allEmbeddings = getAllEmbeddings(db);

    const scored = allEmbeddings
      .map(({ item_id, embedding }) => ({
        item_id,
        score: cosineSimilarity(queryVec, embedding),
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit * 2); // get extras for hybrid merge

    for (const { item_id, score } of scored) {
      const item = getItem(db, item_id);
      if (!item) continue;
      if (opts.category && item.category !== opts.category) continue;
      results.set(item_id, { item, score, mode: "semantic" });
    }
  }

  // === Keyword Search (FTS5) ===
  if (mode === "keyword" || mode === "hybrid") {
    const kws = keywordSearch(db, query, { category: opts.category, limit: limit * 2 });

    for (const { id, rank } of kws) {
      // FTS5 rank is negative (lower = better match), normalize to 0-1
      const normalizedScore = 1 / (1 + Math.abs(rank));

      if (results.has(id)) {
        // Boost items found by both methods
        const existing = results.get(id)!;
        existing.score = existing.score * 0.7 + normalizedScore * 0.3;
        existing.mode = "both";
      } else {
        const item = getItem(db, id);
        if (!item) continue;
        results.set(id, { item, score: normalizedScore, mode: "keyword" });
      }
    }
  }

  // Sort by score, take top N
  return [...results.values()]
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

/**
 * Ensure an item has a fresh embedding. Useful after add/update.
 */
export async function ensureEmbedded(db: Database, itemId: number) {
  const { storeEmbedding, getItem, getEmbedding } = await import("./db.ts");
  const { embed, MODEL_NAME } = await import("./embed.ts");

  // Check if already embedded
  const existing = getEmbedding(db, itemId);
  if (existing) return;

  const item = getItem(db, itemId);
  if (!item) return;

  const text = `${item.title}\n\n${item.content}`;
  const embedding = await embed(text);
  storeEmbedding(db, itemId, embedding, MODEL_NAME);
}
