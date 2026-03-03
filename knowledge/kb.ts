#!/usr/bin/env bun
/**
 * Eve's Knowledge Base CLI
 * Usage: bun kb.ts <command> [options]
 *
 * Commands:
 *   add      Add a new knowledge item
 *   search   Search by meaning (semantic) or keyword
 *   list     List items, optionally filtered
 *   show     Show full content of an item
 *   delete   Remove an item
 *   index    Auto-index a directory of markdown files
 *   embed    Generate embeddings for un-embedded items
 *   stats    Show database stats
 */

import minimist from "minimist";
import { getDb, insertItem, getItem, deleteItem, listItems, storeEmbedding, getStats, VALID_CATEGORIES, type Category } from "./lib/db.ts";
import { embed, MODEL_NAME } from "./lib/embed.ts";
import { search, type SearchMode } from "./lib/search.ts";
import { indexDirectory } from "./lib/indexer.ts";
import { homedir } from "os";

const argv = minimist(process.argv.slice(2), {
  string: ["title", "content", "summary", "category", "tags", "source", "dir", "mode", "tag"],
  number: ["limit", "offset"],
  boolean: ["verbose", "recursive", "help"],
  alias: { h: "help", v: "verbose", c: "category", l: "limit" },
  default: { limit: 10, offset: 0, mode: "hybrid", recursive: false },
});

const cmd = argv._[0];

function usage() {
  console.log(`
Eve Knowledge Base — bun kb.ts <command> [options]

Commands:
  add       --title "..." --content "..." --category <cat> [--tags "a,b"] [--summary "..."]
  search    "<query>" [--category <cat>] [--limit N] [--mode semantic|keyword|hybrid]
  list      [--category <cat>] [--tag <tag>] [--limit N]
  show      <id>
  delete    <id>
  index     --dir <path> [--category <cat>] [--source daily-notes|research|general] [--recursive]
  embed     (generate embeddings for items that don't have one yet)
  stats

Categories: ${VALID_CATEGORIES.join(", ")}

Examples:
  bun kb.ts add --title "Competitor found" --content "..." --category business --tags "opticfy,competitors"
  bun kb.ts search "AI tools for document processing" --category tech
  bun kb.ts search "bitcoin price analysis" --mode semantic --limit 5
  bun kb.ts list --category crypto --limit 20
  bun kb.ts index --dir ~/.openclaw/workspace/memory --source daily-notes
  bun kb.ts index --dir ~/.openclaw/workspace/memory/research --source research --recursive
  bun kb.ts stats
`);
}

function formatDate(ts: number) {
  return new Date(ts * 1000).toLocaleDateString("en-US", {
    year: "numeric", month: "short", day: "numeric"
  });
}

function printItem(item: any, full = false) {
  const tags = item.tags?.length ? ` [${item.tags.join(", ")}]` : "";
  const date = formatDate(item.created_at);
  console.log(`\n#${item.id} · ${item.category.toUpperCase()}${tags} · ${date}`);
  console.log(`  ${item.title}`);
  if (item.summary) console.log(`  Summary: ${item.summary}`);
  if (full) {
    console.log(`\n${item.content}`);
    if (item.source_path) console.log(`\nSource: ${item.source_path}`);
  } else {
    const preview = item.content.slice(0, 120).replace(/\n/g, " ");
    console.log(`  ${preview}${item.content.length > 120 ? "..." : ""}`);
  }
}

async function main() {
  if (!cmd || argv.help) {
    usage();
    process.exit(0);
  }

  const db = getDb();

  // ── ADD ──────────────────────────────────────────────────────────────────
  if (cmd === "add") {
    const { title, content, summary, category, tags: tagsStr, source } = argv;

    if (!title || !content || !category) {
      console.error("Error: --title, --content, and --category are required.");
      process.exit(1);
    }

    if (!VALID_CATEGORIES.includes(category)) {
      console.error(`Error: category must be one of: ${VALID_CATEGORIES.join(", ")}`);
      process.exit(1);
    }

    const tags = tagsStr ? tagsStr.split(",").map((t: string) => t.trim()) : [];

    console.log("Generating embedding...");
    const embText = `${title}\n\n${content}`;
    const embedding = await embed(embText);

    const id = insertItem(db, {
      title,
      content,
      summary: summary ?? null,
      category: category as Category,
      tags,
      source: source ?? "manual",
      source_path: null,
    });

    storeEmbedding(db, id, embedding, MODEL_NAME);

    console.log(`✓ Added item #${id}: "${title}" [${category}]`);
    return;
  }

  // ── SEARCH ───────────────────────────────────────────────────────────────
  if (cmd === "search") {
    const query = argv._[1];
    if (!query) {
      console.error("Error: provide a search query. e.g. bun kb.ts search \"AI tools\"");
      process.exit(1);
    }

    console.error(`Searching (${argv.mode})...`);
    const results = await search(query, {
      category: argv.category,
      limit: argv.limit,
      mode: argv.mode as SearchMode,
    });

    if (results.length === 0) {
      console.log("No results found.");
      return;
    }

    console.log(`\n${results.length} result(s) for: "${query}"\n`);
    for (const { item, score, mode } of results) {
      const tags = item.tags?.length ? ` [${item.tags.join(", ")}]` : "";
      const scoreStr = (score * 100).toFixed(1);
      console.log(`#${item.id} · ${item.category.toUpperCase()}${tags} · score: ${scoreStr}% (${mode})`);
      console.log(`  ${item.title}`);
      const preview = item.content.slice(0, 150).replace(/\n/g, " ");
      console.log(`  ${preview}${item.content.length > 150 ? "..." : ""}\n`);
    }
    return;
  }

  // ── LIST ─────────────────────────────────────────────────────────────────
  if (cmd === "list") {
    const items = listItems(db, {
      category: argv.category,
      tag: argv.tag,
      limit: argv.limit,
      offset: argv.offset,
    });

    if (items.length === 0) {
      console.log("No items found.");
      return;
    }

    console.log(`\n${items.length} item(s):\n`);
    for (const item of items) printItem(item);
    return;
  }

  // ── SHOW ─────────────────────────────────────────────────────────────────
  if (cmd === "show") {
    const id = Number(argv._[1]);
    if (!id) {
      console.error("Error: provide an item ID. e.g. bun kb.ts show 42");
      process.exit(1);
    }
    const item = getItem(db, id);
    if (!item) {
      console.error(`Item #${id} not found.`);
      process.exit(1);
    }
    printItem(item, true);
    return;
  }

  // ── DELETE ───────────────────────────────────────────────────────────────
  if (cmd === "delete") {
    const id = Number(argv._[1]);
    if (!id) {
      console.error("Error: provide an item ID. e.g. bun kb.ts delete 42");
      process.exit(1);
    }
    const item = getItem(db, id);
    if (!item) {
      console.error(`Item #${id} not found.`);
      process.exit(1);
    }
    const ok = deleteItem(db, id);
    console.log(ok ? `✓ Deleted item #${id}: "${item.title}"` : "Failed.");
    return;
  }

  // ── INDEX ─────────────────────────────────────────────────────────────────
  if (cmd === "index") {
    const dir = argv.dir
      ? argv.dir.replace("~", homedir())
      : null;

    if (!dir) {
      console.error("Error: --dir is required. e.g. bun kb.ts index --dir ~/.openclaw/workspace/memory");
      process.exit(1);
    }

    const category = argv.category as Category | undefined;
    if (category && !VALID_CATEGORIES.includes(category)) {
      console.error(`Error: category must be one of: ${VALID_CATEGORIES.join(", ")}`);
      process.exit(1);
    }

    console.log(`Indexing ${dir}...`);
    const result = await indexDirectory(dir, {
      source: argv.source ?? "general",
      category,
      recursive: argv.recursive,
      verbose: argv.verbose,
    });

    console.log(`✓ Done: ${result.added} added, ${result.updated} updated, ${result.skipped} skipped (unchanged)`);
    return;
  }

  // ── EMBED ────────────────────────────────────────────────────────────────
  if (cmd === "embed") {
    // Find items without embeddings and generate them
    const unembedded = db
      .prepare(`
        SELECT ki.id, ki.title, ki.content
        FROM knowledge_items ki
        LEFT JOIN embeddings e ON e.item_id = ki.id
        WHERE e.item_id IS NULL
      `)
      .all() as Array<{ id: number; title: string; content: string }>;

    if (unembedded.length === 0) {
      console.log("All items are already embedded.");
      return;
    }

    console.log(`Generating embeddings for ${unembedded.length} item(s)...`);
    for (let i = 0; i < unembedded.length; i++) {
      const item = unembedded[i];
      const text = `${item.title}\n\n${item.content}`;
      const embedding = await embed(text);
      storeEmbedding(db, item.id, embedding, MODEL_NAME);
      process.stdout.write(`\r  ${i + 1}/${unembedded.length}`);
    }
    console.log(`\n✓ Done.`);
    return;
  }

  // ── STATS ────────────────────────────────────────────────────────────────
  if (cmd === "stats") {
    const stats = getStats(db);
    const sizeMB = (stats.dbSize / 1024 / 1024).toFixed(2);

    console.log(`\n📚 Knowledge Base Stats`);
    console.log(`   Total items:   ${stats.total}`);
    console.log(`   Embedded:      ${stats.embedded}/${stats.total}`);
    console.log(`   DB size:       ${sizeMB} MB`);
    console.log(`   Path:          ${db.filename}`);
    console.log(`\nBy category:`);
    for (const { category, n } of stats.byCategory) {
      console.log(`   ${category.padEnd(12)} ${n}`);
    }
    return;
  }

  console.error(`Unknown command: ${cmd}`);
  usage();
  process.exit(1);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
