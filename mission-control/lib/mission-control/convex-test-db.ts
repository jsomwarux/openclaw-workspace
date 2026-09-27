// Test-only in-memory stand-in for the Convex `ctx.db` surface the task
// mutations use. Patch mirrors Convex semantics: an `undefined` value removes
// the field.
export type TestRow = Record<string, any> & { _id: string };

function fieldValue(row: TestRow, field: string): unknown {
  return field.split(".").reduce<unknown>(
    (value, segment) => (value && typeof value === "object" ? (value as Record<string, unknown>)[segment] : undefined),
    row,
  );
}

export class ConvexTestDb {
  rows: TestRow[] = [];
  writes = 0;
  private nextId = 1;

  seed(fields: Record<string, unknown>): string {
    const id = `seed-${this.nextId++}`;
    this.rows.push({ _id: id, ...structuredClone(fields) });
    return id;
  }

  query(_table: string) {
    const rows = () => this.rows.map((row) => row);
    const ordered = (order: "asc" | "desc", source: TestRow[]) => (order === "desc" ? [...source].reverse() : source);
    const chain = (source: () => TestRow[]) => ({
      collect: async () => source(),
      first: async () => source()[0] ?? null,
      take: async (count: number) => source().slice(0, count),
      order: (order: "asc" | "desc") => ({
        collect: async () => ordered(order, source()),
        take: async (count: number) => ordered(order, source()).slice(0, count),
      }),
    });
    return {
      ...chain(rows),
      withIndex: (_name: string, apply?: (q: any) => any) => {
        const filters: Array<[string, unknown]> = [];
        const q = { eq: (field: string, value: unknown) => { filters.push([field, value]); return q; } };
        apply?.(q);
        return chain(() => rows().filter((row) => filters.every(([field, value]) => fieldValue(row, field) === value)));
      },
    };
  }

  async get(id: string) {
    return this.rows.find((row) => row._id === id) ?? null;
  }

  async insert(_table: string, fields: Record<string, unknown>) {
    this.writes += 1;
    const id = `task-${this.nextId++}`;
    this.rows.push({ _id: id, ...structuredClone(fields) });
    return id;
  }

  async patch(id: string, fields: Record<string, unknown>) {
    const row = this.rows.find((candidate) => candidate._id === id);
    if (!row) throw new Error("missing row");
    this.writes += 1;
    for (const [key, value] of Object.entries(fields)) {
      if (value === undefined) delete row[key];
      else row[key] = structuredClone(value);
    }
  }

  async delete(id: string) {
    this.writes += 1;
    this.rows = this.rows.filter((row) => row._id !== id);
  }

  snapshot(id: string): TestRow | undefined {
    const row = this.rows.find((candidate) => candidate._id === id);
    return row ? structuredClone(row) : undefined;
  }
}

export function testCtx(db: ConvexTestDb) {
  return { db } as any;
}

export async function withEnv<T>(values: Record<string, string | undefined>, run: () => Promise<T>): Promise<T> {
  const previous = Object.fromEntries(Object.keys(values).map((key) => [key, process.env[key]]));
  for (const [key, value] of Object.entries(values)) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
  try {
    return await run();
  } finally {
    for (const [key, value] of Object.entries(previous)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
}
