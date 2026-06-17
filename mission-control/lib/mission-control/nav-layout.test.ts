import { describe, expect, test } from "bun:test";
import { mobileNavInnerClassName, mobileNavShellClassName, mobileMainClassName } from "./nav-layout";

describe("mobile shell layout", () => {
  test("centers the bottom nav rail instead of left-starting the items", () => {
    expect(mobileNavShellClassName).toContain("pb-[max(0.75rem,env(safe-area-inset-bottom))]");
    expect(mobileNavInnerClassName).toContain("mx-auto");
    expect(mobileNavInnerClassName).toContain("max-w-[430px]");
    expect(mobileNavInnerClassName).toContain("justify-center");
  });

  test("reserves enough mobile bottom space for the app nav", () => {
    expect(mobileMainClassName).toContain("pb-28");
    expect(mobileMainClassName).toContain("md:pb-0");
  });
});
