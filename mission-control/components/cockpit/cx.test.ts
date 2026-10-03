import { describe, expect, test } from "bun:test";
import { cx } from "./cx";

describe("cockpit class merging knows the bundle's token classes", () => {
  test("a token font size and a token color both survive", () => {
    expect(cx("text-mc-11 text-mc-ink-muted")).toBe("text-mc-11 text-mc-ink-muted");
    expect(cx("text-mc-13", "text-mc-ink-secondary")).toBe("text-mc-13 text-mc-ink-secondary");
  });

  test("conflicting token sizes, density spacing and radii merge to the last one", () => {
    expect(cx("text-mc-11 text-mc-13")).toBe("text-mc-13");
    expect(cx("px-d10 py-d4 px-d12")).toBe("py-d4 px-d12");
    expect(cx("rounded-btn rounded-card")).toBe("rounded-card");
    expect(cx("font-semibold font-bold")).toBe("font-bold");
  });

  test("the bundle's fonts merge as font families, not weights", () => {
    expect(cx("font-mc-mono font-medium")).toBe("font-mc-mono font-medium");
  });
});
