import { describe, expect, test } from "bun:test";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import appConfig from "../../tailwind.config";
import bundleConfig from "../../docs/design/mission-control-redesign/tokens/tailwind.config";

const ROOT = fileURLToPath(new URL("../..", import.meta.url));
type Extend = Record<string, Record<string, unknown>>;
const app = (appConfig.theme as { extend: Extend }).extend;
const bundle = (bundleConfig.theme as { extend: Extend }).extend;

function sourceFiles(dir: string): string[] {
  if (!existsSync(dir)) return [];
  const out: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...sourceFiles(full));
    else if (/\.(ts|tsx|css)$/.test(name) && !/\.test\.tsx?$/.test(name)) out.push(full);
  }
  return out;
}

describe("cockpit tokens come from the design bundle by name", () => {
  test("every bundle color is exposed under its token name with the bundle's value", () => {
    expect(app.colors.mc).toEqual(bundle.colors.mc);
  });

  test("type sizes, radii and layout widths match the bundle exactly", () => {
    for (const group of ["fontSize", "borderRadius", "maxWidth", "height", "width"]) {
      for (const [key, value] of Object.entries(bundle[group])) {
        expect(app[group][key]).toEqual(value);
      }
    }
  });

  test("cockpit fonts use the bundle families under their own names, leaving the current fonts alone", () => {
    expect(app.fontFamily["mc-sans"]).toEqual(bundle.fontFamily.sans);
    expect(app.fontFamily["mc-mono"]).toEqual(bundle.fontFamily.mono);
    expect(app.fontFamily.mono).toEqual(["'JetBrains Mono'", "Menlo", "monospace"]);
    expect(app.fontFamily.sans).toBe(undefined);
  });

  test("cockpit spacing follows the README's 4 px scale and scales with the density token", () => {
    expect(app.spacing.d4).toBe("calc(4px * var(--mc-d, 1))");
    expect(app.spacing.d20).toBe("calc(20px * var(--mc-d, 1))");
    expect(app.spacing.d56).toBe("calc(56px * var(--mc-d, 1))");
    expect(Object.keys(app.spacing).every((key) => key.startsWith("d"))).toBe(true);
  });

  test("the current interface's colors are untouched", () => {
    expect(app.colors.accent).toEqual({ DEFAULT: "#10b981", dim: "#059669", glow: "#34d399" });
    expect(app.colors.surface).toEqual({ DEFAULT: "#111111", raised: "#1a1a1a", border: "#2a2a2a" });
  });

  test("the cockpit route loads the bundle's tokens.css itself, not a copy", () => {
    const layout = readFileSync(join(ROOT, "app", "cockpit", "layout.tsx"), "utf8");
    expect(layout).toContain("docs/design/mission-control-redesign/tokens/tokens.css");
  });

  test("no cockpit source file hand-types a color value", () => {
    const files = [
      ...sourceFiles(join(ROOT, "app", "cockpit")),
      ...sourceFiles(join(ROOT, "components", "cockpit")),
      ...sourceFiles(join(ROOT, "lib", "cockpit")),
    ];
    expect(files.length).toBeGreaterThan(10);
    const offenders = files.filter((file) => /oklch\(|rgba?\(|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b/.test(readFileSync(file, "utf8")));
    expect(offenders).toEqual([]);
  });
});
