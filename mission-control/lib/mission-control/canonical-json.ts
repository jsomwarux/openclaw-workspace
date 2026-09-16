type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

function hasLoneSurrogate(value: string): boolean {
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) return true;
      index += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) return true;
  }
  return false;
}

function normalize(value: unknown, seen: Set<object>): JsonValue {
  if (value === null || typeof value === "boolean") return value;
  if (typeof value === "string") {
    if (hasLoneSurrogate(value)) throw new Error("invalid canonical JSON");
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("invalid canonical JSON");
    return value;
  }
  if (typeof value !== "object" || seen.has(value)) throw new Error("invalid canonical JSON");
  seen.add(value);
  const normalized = Array.isArray(value)
    ? value.map((item) => normalize(item, seen))
    : Object.fromEntries(Object.keys(value as Record<string, unknown>).sort().map((key) => [key, normalize((value as Record<string, unknown>)[key], seen)]));
  seen.delete(value);
  return normalized;
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(normalize(value, new Set()));
}

export async function hashCanonicalJson(value: unknown): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalJson(value)));
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}
