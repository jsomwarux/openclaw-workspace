import { describe, expect, test } from "bun:test";
import { readdirSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { renderToStaticMarkup } from "react-dom/server";
import { PathnameContext } from "next/dist/shared/lib/hooks-client-context.shared-runtime";
import Sidebar from "@/components/Sidebar";
import { hidesLegacyChrome } from "@/lib/mission-control/nav-layout";

const APP_DIR = fileURLToPath(new URL("../../app", import.meta.url));

// Every page route that exists in app/, as a concrete path ("[slug]" filled in).
function pageRoutes(dir = APP_DIR): string[] {
  const routes: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      if (name === "api") continue;
      routes.push(...pageRoutes(full));
    } else if (name === "page.tsx") {
      const rel = relative(APP_DIR, dir).split(sep).filter(Boolean)
        .filter((part) => !part.startsWith("("))
        .map((part) => (part.startsWith("[") ? "sample" : part));
      routes.push(`/${rel.join("/")}`);
    }
  }
  return routes;
}

function renderSidebarAt(path: string): string {
  return renderToStaticMarkup(
    <PathnameContext.Provider value={path}>
      <Sidebar />
    </PathnameContext.Provider>,
  );
}

describe("old chrome on the cockpit route", () => {
  test("only /cockpit and paths under it hide the old chrome", () => {
    expect(hidesLegacyChrome("/cockpit")).toBe(true);
    expect(hidesLegacyChrome("/cockpit/anything")).toBe(true);
    expect(hidesLegacyChrome("/cockpits")).toBe(false);
    expect(hidesLegacyChrome("/")).toBe(false);
    expect(hidesLegacyChrome(null)).toBe(false);
  });

  test("every existing page keeps the old chrome", () => {
    const routes = pageRoutes().filter((route) => route !== "/cockpit");
    expect(routes.length).toBeGreaterThan(20);
    expect(routes).toContain("/work");
    for (const route of routes) expect(hidesLegacyChrome(route)).toBe(false);
  });

  test("the Sidebar renders nothing on /cockpit and the same markup elsewhere", () => {
    expect(renderSidebarAt("/cockpit")).toBe("");
    const work = renderSidebarAt("/work");
    expect(work).toContain("Mission Control");
    expect(work).toContain('href="/clients"');
  });
});
