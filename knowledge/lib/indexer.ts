/**
 * Auto-indexer — scans markdown files and adds them to the knowledge base
 * Tracks what's already indexed by path + mtime to avoid duplicates
 */
import { readdirSync, readFileSync, statSync, existsSync } from "fs";
import { join, extname, basename } from "path";
import { Database } from "bun:sqlite";
import { getDb, insertItem, storeEmbedding, Category, VALID_CATEGORIES } from "./db.ts";
import { embed, MODEL_NAME } from "./embed.ts";

type IndexSource = "daily-notes" | "research" | "general";

/**
 * Detect best category for a file based on its path and content
 */
function detectCategory(filePath: string, content: string): Category {
  const lower = `${filePath} ${content.slice(0, 500)}`.toLowerCase();
  if (lower.includes("crypto") || lower.includes("bitcoin") || lower.includes("eth")) return "crypto";
  if (lower.includes("opticfy") || lower.includes("client") || lower.includes("market")) return "business";
  if (lower.includes("ai") || lower.includes("llm") || lower.includes("model") || lower.includes("tool")) return "tech";
  if (lower.includes("health") || lower.includes("habit") || lower.includes("goal")) return "personal";
  if (lower.includes("project") || lower.includes("build") || lower.includes("feature")) return "projects";
  return "tech"; // default
}

/**
 * Extract tags from markdown content (looks for #tags or common keywords)
 */
function extractTags(content: string, filePath: string): string[] {
  const tags = new Set<string>();

  // Hashtags in content
  const hashMatches = content.matchAll(/#([a-zA-Z][a-zA-Z0-9-_]+)/g);
  for (const m of hashMatches) tags.add(m[1].toLowerCase());

  // Date pattern in filename (daily notes)
  const dateMatch = basename(filePath).match(/(\d{4}-\d{2}-\d{2})/);
  if (dateMatch) tags.add("daily-note");

  // Keywords
  if (content.toLowerCase().includes("opticfy")) tags.add("opticfy");
  if (content.toLowerCase().includes("bitcoin") || content.toLowerCase().includes("btc")) tags.add("bitcoin");
  if (content.toLowerCase().includes("ethereum") || content.toLowerCase().includes("eth")) tags.add("ethereum");

  return [...tags].slice(0, 10);
}

/**
 * Split a markdown file into sections (by ## headings).
 * Returns [{title, content}] pairs.
 */
function splitIntoSections(
  fileContent: string,
  fileName: string
): Array<{ title: string; content: string }> {
  const lines = fileContent.split("\n");
  const sections: Array<{ title: string; content: string }> = [];

  let currentTitle = basename(fileName, ".md").replace(/-/g, " ");
  let currentLines: string[] = [];

  for (const line of lines) {
    const headingMatch = line.match(/^#{1,3}\s+(.+)/);
    if (headingMatch) {
      if (currentLines.join("\n").trim().length > 50) {
        sections.push({
          title: currentTitle,
          content: currentLines.join("\n").trim(),
        });
      }
      currentTitle = headingMatch[1].trim();
      currentLines = [];
    } else {
      currentLines.push(line);
    }
  }

  // Last section
  if (currentLines.join("\n").trim().length > 50) {
    sections.push({
      title: currentTitle,
      content: currentLines.join("\n").trim(),
    });
  }

  // If no sections found, treat whole file as one item
  if (sections.length === 0 && fileContent.trim().length > 50) {
    sections.push({
      title: basename(fileName, ".md").replace(/-/g, " "),
      content: fileContent.trim(),
    });
  }

  return sections;
}

export async function indexDirectory(
  dir: string,
  opts: {
    source?: IndexSource;
    category?: Category;
    recursive?: boolean;
    verbose?: boolean;
  } = {}
): Promise<{ added: number; skipped: number; updated: number }> {
  const db = getDb();
  const source = opts.source ?? "general";
  const recursive = opts.recursive ?? false;
  const verbose = opts.verbose ?? false;

  if (!existsSync(dir)) {
    throw new Error(`Directory not found: ${dir}`);
  }

  let added = 0;
  let skipped = 0;
  let updated = 0;

  const files = scanDir(dir, recursive);
  const mdFiles = files.filter((f) => extname(f) === ".md");

  if (verbose) console.error(`[indexer] Found ${mdFiles.length} markdown files in ${dir}`);

  for (const filePath of mdFiles) {
    const stat = statSync(filePath);
    const mtime = Math.floor(stat.mtimeMs / 1000);

    // Check if already indexed and unchanged
    const existing = db
      .prepare("SELECT mtime FROM indexed_files WHERE path = ?")
      .get(filePath) as { mtime: number } | null;

    if (existing && existing.mtime === mtime) {
      if (verbose) console.error(`[indexer] Skip (unchanged): ${filePath}`);
      skipped++;
      continue;
    }

    const content = readFileSync(filePath, "utf-8");
    const sections = splitIntoSections(content, filePath);
    const category = opts.category ?? detectCategory(filePath, content);
    const tags = extractTags(content, filePath);

    let fileItemCount = 0;
    for (const section of sections) {
      if (section.content.length < 80) continue; // Skip tiny sections

      const itemId = insertItem(db, {
        title: section.title,
        content: section.content,
        summary: null,
        category,
        tags,
        source,
        source_path: filePath,
      });

      // Generate embedding
      try {
        const embText = `${section.title}\n\n${section.content}`;
        const embedding = await embed(embText);
        storeEmbedding(db, itemId, embedding, MODEL_NAME);
      } catch (e) {
        if (verbose) console.error(`[indexer] Embedding failed for item ${itemId}:`, e);
      }

      fileItemCount++;
      added++;
    }

    // Record indexed file
    db.prepare(`
      INSERT OR REPLACE INTO indexed_files (path, mtime, indexed_at, item_count)
      VALUES (?, ?, unixepoch(), ?)
    `).run(filePath, mtime, fileItemCount);

    if (verbose) console.error(`[indexer] Indexed: ${filePath} → ${fileItemCount} items`);
    if (existing) updated++;
  }

  return { added, skipped, updated };
}

function scanDir(dir: string, recursive: boolean): string[] {
  const results: string[] = [];
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith(".")) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory() && recursive) {
      results.push(...scanDir(full, true));
    } else if (entry.isFile()) {
      results.push(full);
    }
  }
  return results;
}
