import { describe, expect, test } from "bun:test";
import tailwindConfig from "../../tailwind.config";

describe("tailwind content paths", () => {
  test("scans mission-control lib files used for shared class names", () => {
    const content = Array.isArray(tailwindConfig.content) ? tailwindConfig.content : [];

    expect(content.includes("./lib/**/*.{ts,tsx}")).toBe(true);
  });
});
