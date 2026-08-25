import { describe, expect, test } from "bun:test";
import { spawnSync } from "node:child_process";
import { parseNightlyValidationSnapshot } from "./nightly-validation";

function errorMessage(run: () => void): string | undefined {
  try { run(); } catch (error) { return error instanceof Error ? error.message : String(error); }
  return undefined;
}

const admission = {
  schema: "nightly-validation-admission-v1",
  generatedBy: "nightly-validation-controller",
  status: "ADMISSION_READY",
  runAt: "2026-08-24T23:00:00Z",
  lane: "workflow",
  selected: [{ candidate_id: "workflow-high", lane: "workflow", score: 95, status: "pending", source_hash: "sha256:hash" }],
  admissionHash: "sha256:admission",
};

const promotion = {
  candidateId: "workflow-high",
  sourceHash: "sha256:hash",
  verdict: "promote",
  verifierConfirmed: true,
  verifiedAt: "2026-08-24T23:10:00Z",
  score: 34,
  evidenceScore: 4,
  distributionScore: 3,
  fatalConstraint: false,
  title: "Review validated workflow signal",
  firstAction: "Open the artifact",
  whyItMatters: "Fresh evidence passed",
  doneState: "Record a decision",
  evidenceFound: "Buyer evidence",
  question: "Will this compound",
  nextTrigger: "New buyer evidence",
  workstream: "compounding-bet",
};

const envelope = {
  schema: "nightly-validation-promotion-v1",
  generatedBy: "nightly-validation-controller",
  generatedAt: "2026-08-24T23:15:00Z",
  admissionPath: "memory/agent-portfolio/runs/2026-08-24/run-1/admission.json",
  admissionHash: "sha256:admission",
  promotions: [promotion],
  artifactHash: "sha256:artifact",
};

describe("nightly validation parser", () => {
  test("parses artifacts produced by the real Python controller", () => {
    const script = `
import hashlib, importlib.util, json, tempfile
from datetime import datetime, timezone
from pathlib import Path
spec = importlib.util.spec_from_file_location("controller", "../scripts/nightly_validation_controller.py")
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
now = datetime(2026, 8, 24, 23, 15, tzinfo=timezone.utc)
evidence = module.WORKSPACE / "memory/agent-portfolio/evidence/fixtures/evidence-a.json"
candidate = {"candidate_id":"c1","lane":"workflow","score":95,"status":"pending","not_before":"2026-08-24T20:00:00Z","source_hash":"sha256:"+hashlib.sha256(evidence.read_bytes()).hexdigest(),"evidence_path":str(evidence),"evidence_timestamp":"2026-08-24T22:00:00Z"}
result = {"candidateId":"c1","sourceHash":candidate["source_hash"],"verdict":"promote","verifierConfirmed":True,"verifiedAt":"2026-08-24T23:00:00Z","score":34,"evidenceScore":4,"distributionScore":3,"fatalConstraint":False,"question":"Will it compound?","sourcesChecked":["fixture"],"evidenceFound":"Evidence","falsificationResult":"None","artifactPaths":[str(evidence)],"decision":"promote","confidence":"medium","nextTrigger":"New evidence","title":"Validated signal","firstAction":"Open artifact","whyItMatters":"It passed","doneState":"Record decision","workstream":"compounding-bet"}
with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp); state=root/"state.md"
  admitted=module.admit_candidates([candidate], now, state, root/"runs", False)
  results=root/"results.jsonl"; results.write_text(json.dumps(result)+"\\n")
  reconciled=module.reconcile_results(Path(admitted["admissionPath"]), results, now, state, False)
  admission_path=Path(admitted["admissionPath"]); promotion_path=Path(reconciled["promotionPath"])
  print(json.dumps({"runId":admission_path.parent.name,"admissionText":admission_path.read_text(),"promotionName":promotion_path.name,"promotionText":promotion_path.read_text()}))
`;
    const generated = spawnSync("python3", ["-c", script], { cwd: process.cwd(), encoding: "utf-8" });
    expect(generated.status).toBe(0);
    const artifact = JSON.parse(generated.stdout);
    const snapshot = parseNightlyValidationSnapshot({
      queueText: "",
      stateText: "failures_json: []\n",
      runFiles: [{ runId: artifact.runId, admissionText: artifact.admissionText, promotionFiles: [{ name: artifact.promotionName, text: artifact.promotionText }] }],
      now: Date.parse("2026-08-24T23:30:00Z"),
    });
    expect(snapshot.status).toBe("reconciled");
    expect(snapshot.runs[0].promotions[0].candidateId).toBe("c1");
  });

  test("parses the controller's timestamped admission and promotion envelope", () => {
    const snapshot = parseNightlyValidationSnapshot({
      queueText: "",
      stateText: "last_completed_run: 2026-08-24T23:15:00Z\nnext_run: 2026-08-25T23:15:00Z\nfailures_json: []\n",
      runFiles: [{
        runId: "2026-08-24/run-20260824T230000000000Z",
        admissionText: JSON.stringify(admission),
        promotionFiles: [
          { name: "promotions-231000000000.json", text: JSON.stringify({ ...envelope, generatedAt: "2026-08-24T23:10:00Z" }) },
          { name: "promotions-231500000000.json", text: JSON.stringify(envelope) },
        ],
      }],
      now: Date.parse("2026-08-24T23:30:00Z"),
    });

    expect(snapshot.status).toBe("reconciled");
    expect(snapshot.runs[0]).toMatchObject({
      runId: "2026-08-24/run-20260824T230000000000Z",
      status: "reconciled",
      promotionArtifact: "promotions-231500000000.json",
    });
    expect(snapshot.runs[0].promotions[0]).toMatchObject({
      candidateId: "workflow-high",
      verifierConfirmed: true,
      firstAction: "Open the artifact",
      evidenceScore: 4,
      distributionScore: 3,
    });
  });

  test("shows admitted, blocked stale, and no-work states", () => {
    const admitted = parseNightlyValidationSnapshot({
      queueText: "",
      stateText: "failures_json: []\n",
      runFiles: [{ runId: "fresh", admissionText: JSON.stringify(admission), promotionFiles: [] }],
      now: Date.parse("2026-08-24T23:30:00Z"),
    });
    expect(admitted.status).toBe("admitted");

    const blocked = parseNightlyValidationSnapshot({
      queueText: "",
      stateText: "failures_json: []\n",
      runFiles: [{ runId: "stale", admissionText: JSON.stringify({ ...admission, runAt: "2026-08-22T20:00:00Z" }), promotionFiles: [] }],
      now: Date.parse("2026-08-24T23:30:00Z"),
    });
    expect(blocked.status).toBe("blocked");
    expect(blocked.runs[0].issue).toContain("stale");

    const noWork = parseNightlyValidationSnapshot({ queueText: "", stateText: "failures_json: []\n", runFiles: [], now: 0 });
    expect(noWork.status).toBe("no-work");
  });

  test("fails loud on malformed or legacy promotion artifacts", () => {
    const legacy = [{ candidate_id: "workflow-high", verifier_confirmed: true }];
    expect(errorMessage(() => parseNightlyValidationSnapshot({
      queueText: "",
      stateText: "failures_json: []\n",
      runFiles: [{ runId: "bad", admissionText: JSON.stringify(admission), promotionFiles: [{ name: "promotions-1.json", text: JSON.stringify(legacy) }] }],
      now: Date.parse("2026-08-24T23:30:00Z"),
    }))).toContain("promotion envelope");
  });

  test("fails loud with line evidence for malformed queue data", () => {
    expect(errorMessage(() => parseNightlyValidationSnapshot({ queueText: "{bad", stateText: "", runFiles: [], now: 0 }))).toContain("queue line 1");
  });
});
