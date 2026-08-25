import { describe, expect, test } from "bun:test";
import { spawnSync } from "node:child_process";
import { validateTaskAdmission } from "./task-admission";

function errorMessage(run: () => void): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

describe("controller to Mission Control admission contract", () => {
  test("accepts the exact payload emitted by the Python controller", () => {
    const verifiedAt = new Date().toISOString();
    const script = `
import importlib.util, json
spec = importlib.util.spec_from_file_location("controller", "../scripts/nightly_validation_controller.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
promotion = {
  "title":"Validated signal", "evidenceFound":"Evidence", "firstAction":"Open artifact",
  "whyItMatters":"It passed", "doneState":"Decision recorded", "candidateId":"c1",
  "sourceHash":"sha256:h1", "workstream":"compounding-bet", "score":34,
  "question":"Will it work?", "nextTrigger":"New evidence", "verdict":"promote",
  "verifierConfirmed":True, "verifiedAt":${JSON.stringify(verifiedAt)}, "evidenceScore":4,
  "distributionScore":3, "fatalConstraint":False
}
print(json.dumps(module.build_admission_payload(promotion, "memory/agent-portfolio/runs/run/promotions.json")))
`;
    const result = spawnSync("python3", ["-c", script], { cwd: process.cwd(), encoding: "utf-8" });
    expect(result.status).toBe(0);
    const payload = JSON.parse(result.stdout);
    expect(errorMessage(() => validateTaskAdmission(payload))).toBe(undefined);
    expect(payload).toMatchObject({ sourceSystem: "nightly-validation-controller", verdict: "promote", promotionScore: 34 });
  });
});
