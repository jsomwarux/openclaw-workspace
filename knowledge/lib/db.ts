/**
 * Database layer — SQLite via bun:sqlite
 * Schema: knowledge_items + embeddings + FTS5
 */
import { Database } from "bun:sqlite";
import { existsSync, mkdirSync } from "fs";
import { dirname } from "path";
import { homedir } from "os";

export const DB_PATH =
  process.env.KB_PATH ??
  `${homedir()}/.openclaw/workspace/knowledge/kb.sqlite`;

let _db: Database | null = null;

export function getDb(): Database {
  if (_db) return _db;

  const dir = dirname(DB_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  _db = new Database(DB_PATH);
  _db.exec("PRAGMA journal_mode = WAL;");
  _db.exec("PRAGMA foreign_keys = ON;");
  initSchema(_db);
  return _db;
}

function initSchema(db: Database) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS knowledge_items (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      title       TEXT    NOT NULL,
      content     TEXT    NOT NULL,
      summary     TEXT,
      category    TEXT    NOT NULL CHECK(category IN ('business','tech','crypto','personal','projects')),
      tags        TEXT    DEFAULT '[]',   -- JSON array of strings
      source      TEXT    DEFAULT 'manual',
      source_path TEXT,
      created_at  INTEGER NOT NULL DEFAULT (unixepoch()),
      updated_at  INTEGER NOT NULL DEFAULT (unixepoch())
    );

    CREATE TABLE IF NOT EXISTS embeddings (
      item_id     INTEGER PRIMARY KEY REFERENCES knowledge_items(id) ON DELETE CASCADE,
      embedding   BLOB    NOT NULL,       -- Float32Array buffer
      model       TEXT    NOT NULL,
      dims        INTEGER NOT NULL,
      embedded_at INTEGER NOT NULL DEFAULT (unixepoch())
    );

    -- FTS5 for keyword search
    CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
      title, content, tags,
      content='knowledge_items',
      content_rowid='id'
    );

    -- Keep FTS in sync
    CREATE TRIGGER IF NOT EXISTS ki_ai AFTER INSERT ON knowledge_items BEGIN
      INSERT INTO knowledge_fts(rowid, title, content, tags)
        VALUES (new.id, new.title, new.content, new.tags);
    END;

    CREATE TRIGGER IF NOT EXISTS ki_au AFTER UPDATE ON knowledge_items BEGIN
      INSERT INTO knowledge_fts(knowledge_fts, rowid, title, content, tags)
        VALUES ('delete', old.id, old.title, old.content, old.tags);
      INSERT INTO knowledge_fts(rowid, title, content, tags)
        VALUES (new.id, new.title, new.content, new.tags);
    END;

    CREATE TRIGGER IF NOT EXISTS ki_ad AFTER DELETE ON knowledge_items BEGIN
      INSERT INTO knowledge_fts(knowledge_fts, rowid, title, content, tags)
        VALUES ('delete', old.id, old.title, old.content, old.tags);
    END;

    -- Track indexed file paths to avoid duplicates
    CREATE TABLE IF NOT EXISTS indexed_files (
      path        TEXT    PRIMARY KEY,
      mtime       INTEGER NOT NULL,
      indexed_at  INTEGER NOT NULL DEFAULT (unixepoch()),
      item_count  INTEGER NOT NULL DEFAULT 0
    );
  `);
}

export type KbItem = {
  id: number;
  title: string;
  content: string;
  summary: string | null;
  category: "business" | "tech" | "crypto" | "personal" | "projects";
  tags: string[];
  source: string;
  source_path: string | null;
  created_at: number;
  updated_at: number;
};

export type Category = KbItem["category"];
export const VALID_CATEGORIES: Category[] = [
  "business",
  "tech",
  "crypto",
  "personal",
  "projects",
];

export function insertItem(
  db: Database,
  item: Omit<KbItem, "id" | "created_at" | "updated_at">
): number {
  const stmt = db.prepare(`
    INSERT INTO knowledge_items (title, content, summary, category, tags, source, source_path)
    VALUES ($title, $content, $summary, $category, $tags, $source, $source_path)
    RETURNING id
  `);
  const row = stmt.get({
    $title: item.title,
    $content: item.content,
    $summary: item.summary ?? null,
    $category: item.category,
    $tags: JSON.stringify(item.tags),
    $source: item.source,
    $source_path: item.source_path ?? null,
  }) as { id: number };
  return row.id;
}

export function getItem(db: Database, id: number): KbItem | null {
  const row = db
    .prepare("SELECT * FROM knowledge_items WHERE id = ?")
    .get(id) as any;
  if (!row) return null;
  return { ...row, tags: JSON.parse(row.tags ?? "[]") };
}

export function deleteItem(db: Database, id: number): boolean {
  const r = db
    .prepare("DELETE FROM knowledge_items WHERE id = ?")
    .run(id);
  return r.changes > 0;
}

export function listItems(
  db: Database,
  opts: { category?: string; tag?: string; limit?: number; offset?: number }
): KbItem[] {
  let sql = "SELECT * FROM knowledge_items WHERE 1=1";
  const params: any = {};

  if (opts.category) {
    sql += " AND category = $category";
    params.$category = opts.category;
  }
  if (opts.tag) {
    sql += " AND json_each.value = $tag";
    // Use EXISTS subquery for tag filtering
    sql = `SELECT ki.* FROM knowledge_items ki
           WHERE 1=1
           ${opts.category ? "AND ki.category = $category" : ""}
           AND EXISTS (
             SELECT 1 FROM json_each(ki.tags) WHERE value = $tag
           )`;
    params.$tag = opts.tag;
    if (opts.category) params.$category = opts.category;
  }

  sql += " ORDER BY updated_at DESC";
  sql += ` LIMIT ${opts.limit ?? 20} OFFSET ${opts.offset ?? 0}`;

  const rows = db.prepare(sql).all(params) as any[];
  return rows.map((r) => ({ ...r, tags: JSON.parse(r.tags ?? "[]") }));
}

export function storeEmbedding(
  db: Database,
  itemId: number,
  embedding: Float32Array,
  model: string
) {
  db.prepare(`
    INSERT OR REPLACE INTO embeddings (item_id, embedding, model, dims, embedded_at)
    VALUES (?, ?, ?, ?, unixepoch())
  `).run(itemId, Buffer.from(embedding.buffer), model, embedding.length);
}

export function getEmbedding(
  db: Database,
  itemId: number
): Float32Array | null {
  const row = db
    .prepare("SELECT embedding FROM embeddings WHERE item_id = ?")
    .get(itemId) as { embedding: Buffer } | null;
  if (!row) return null;
  return new Float32Array(row.embedding.buffer);
}

export function getAllEmbeddings(
  db: Database
): Array<{ item_id: number; embedding: Float32Array }> {
  const rows = db
    .prepare("SELECT item_id, embedding FROM embeddings")
    .all() as Array<{ item_id: number; embedding: Buffer }>;
  return rows.map((r) => ({
    item_id: r.item_id,
    embedding: new Float32Array(r.embedding.buffer),
  }));
}

export function keywordSearch(
  db: Database,
  query: string,
  opts: { category?: string; limit?: number }
): Array<{ id: number; rank: number }> {
  let sql = `
    SELECT ki.id, fts.rank
    FROM knowledge_fts fts
    JOIN knowledge_items ki ON ki.id = fts.rowid
    WHERE knowledge_fts MATCH ?
  `;
  const params: any[] = [query];
  if (opts.category) {
    sql += " AND ki.category = ?";
    params.push(opts.category);
  }
  sql += ` ORDER BY fts.rank LIMIT ${opts.limit ?? 20}`;

  try {
    return db.prepare(sql).all(...params) as Array<{ id: number; rank: number }>;
  } catch {
    return [];
  }
}

export function getStats(db: Database) {
  const total = (
    db.prepare("SELECT COUNT(*) as n FROM knowledge_items").get() as any
  ).n;
  const byCategory = db
    .prepare(
      "SELECT category, COUNT(*) as n FROM knowledge_items GROUP BY category"
    )
    .all() as Array<{ category: string; n: number }>;
  const embedded = (
    db.prepare("SELECT COUNT(*) as n FROM embeddings").get() as any
  ).n;
  const dbSize = (
    db.prepare("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()").get() as any
  )?.size ?? 0;
  return { total, byCategory, embedded, dbSize };
}
