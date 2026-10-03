// Run progress lives in this browser's storage, keyed by local date (DECISIONS 8 interim rule,
// override 2). Only keys this module writes are read; nothing is ever cleared.
import type { StoredRun } from "./types";

export interface KeyValueStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  key(index: number): string | null;
  readonly length: number;
}

export const RUN_PREFIX = "mission-control:cockpit-run";

export function memoryStorage(initial: Record<string, string> = {}): KeyValueStorage {
  const map = new Map(Object.entries(initial));
  return {
    getItem: (key) => map.get(key) ?? null,
    setItem: (key, value) => void map.set(key, value),
    key: (index) => [...map.keys()][index] ?? null,
    get length() {
      return map.size;
    },
  };
}

export function browserStorage(): KeyValueStorage | null {
  try {
    return typeof window === "undefined" ? null : window.localStorage;
  } catch {
    return null;
  }
}

function parse(raw: string | null, date: string): StoredRun | null {
  if (!raw) return null;
  try {
    const run = JSON.parse(raw) as StoredRun;
    return run && run.version === 1 && run.localDate === date && Array.isArray(run.items) ? run : null;
  } catch {
    return null;
  }
}

export interface RunStorage {
  load(date: string): StoredRun | null;
  save(run: StoredRun): boolean;
  latestBefore(date: string): StoredRun | null;
}

export function runStorage(storage: KeyValueStorage | null, prefix = RUN_PREFIX): RunStorage {
  const keyFor = (date: string) => `${prefix}:${date}`;
  return {
    load(date) {
      try {
        return parse(storage?.getItem(keyFor(date)) ?? null, date);
      } catch {
        return null;
      }
    },
    save(run) {
      try {
        if (!storage) return false;
        storage.setItem(keyFor(run.localDate), JSON.stringify(run));
        return true;
      } catch {
        return false;
      }
    },
    latestBefore(date) {
      try {
        if (!storage) return null;
        const dates: string[] = [];
        for (let i = 0; i < storage.length; i += 1) {
          const key = storage.key(i);
          if (key && key.startsWith(`${prefix}:`)) dates.push(key.slice(prefix.length + 1));
        }
        const earlier = dates.filter((candidate) => /^\d{4}-\d{2}-\d{2}$/.test(candidate) && candidate < date).sort();
        const latest = earlier[earlier.length - 1];
        return latest ? parse(storage.getItem(keyFor(latest)), latest) : null;
      } catch {
        return null;
      }
    },
  };
}
