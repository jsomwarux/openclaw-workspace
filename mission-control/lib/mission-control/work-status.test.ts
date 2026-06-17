import { describe, expect, test } from "bun:test";
import { statusActionLabel, statusOptions, toTaskStatus } from "./work-status";

describe("work lane status controls", () => {
  test("exposes explicit task status options for mobile rows", () => {
    expect(statusOptions.map((option) => option.value).join(",")).toBe("todo,in-progress,done");
    expect(statusOptions.map((option) => option.label).join(",")).toBe("Todo,Doing,Done");
  });

  test("maps signal statuses back to task statuses", () => {
    expect(toTaskStatus("awaiting-decision")).toBe("todo");
    expect(toTaskStatus("awaiting-approval")).toBe("todo");
    expect(toTaskStatus("in-progress")).toBe("in-progress");
    expect(toTaskStatus("done")).toBe("done");
  });

  test("uses short action labels that fit in mobile task rows", () => {
    expect(statusActionLabel("in-progress")).toBe("Doing");
  });
});
