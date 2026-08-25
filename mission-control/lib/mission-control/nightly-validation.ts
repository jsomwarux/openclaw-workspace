const PENDING_STALE_MS = 24 * 60 * 60 * 1000;

export type NightlyPromotion = {
  candidateId: string;
  sourceHash: string;
  verdict: string;
  verifierConfirmed: boolean;
  verifiedAt: string;
  score: number;
  evidenceScore: number;
  distributionScore: number;
  fatalConstraint: boolean;
  title: string;
  firstAction: string;
  whyItMatters: string;
  doneState: string;
  evidenceFound?: string;
  question?: string;
  nextTrigger?: string;
  workstream: string;
};

export type NightlyRunFile = {
  runId: string;
  admissionText: string;
  promotionFiles: Array<{ name: string; text: string }>;
};

export type NightlyValidationSnapshot = {
  status: "no-work" | "admitted" | "reconciled" | "blocked";
  queue: Array<Record<string, unknown>>;
  state: {
    lastCompletedRun?: string;
    nextRun?: string;
    failures: Array<Record<string, unknown>>;
  };
  runs: Array<{
    runId: string;
    runAt: string;
    status: "admitted" | "reconciled" | "blocked";
    lane: string | null;
    selected: Array<Record<string, unknown>>;
    promotions: NightlyPromotion[];
    promotionArtifact?: string;
    issue?: string;
  }>;
};

function parseQueue(text: string): Array<Record<string, unknown>> {
  return text.split(/\r?\n/).flatMap((line, index) => {
    if (!line.trim()) return [];
    try {
      const value = JSON.parse(line);
      if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("object required");
      return [value as Record<string, unknown>];
    } catch (error) {
      throw new Error(`queue line ${index + 1}: ${error instanceof Error ? error.message : String(error)}`);
    }
  });
}

function stateValue(text: string, key: string): string | undefined {
  const line = text.split(/\r?\n/).find((entry) => entry.startsWith(`${key}:`));
  return line?.slice(key.length + 1).trim() || undefined;
}

function stateArray(text: string, key: string): Array<Record<string, unknown>> {
  const raw = stateValue(text, key);
  if (!raw) return [];
  try {
    const value = JSON.parse(raw);
    if (!Array.isArray(value)) throw new Error("array required");
    return value as Array<Record<string, unknown>>;
  } catch (error) {
    throw new Error(`${key}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function parseObject(text: string, label: string): Record<string, unknown> {
  try {
    const value = JSON.parse(text);
    if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("object required");
    return value as Record<string, unknown>;
  } catch (error) {
    throw new Error(`${label}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function requiredString(value: Record<string, unknown>, field: string, label: string): string {
  if (typeof value[field] !== "string" || !value[field]) throw new Error(`${label}: ${field} required`);
  return value[field] as string;
}

function parsePromotion(value: unknown, label: string): NightlyPromotion {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: object required`);
  const record = value as Record<string, unknown>;
  const strings = ["candidateId", "sourceHash", "verdict", "verifiedAt", "title", "firstAction", "whyItMatters", "doneState", "workstream"];
  for (const field of strings) requiredString(record, field, label);
  if (typeof record.verifierConfirmed !== "boolean") throw new Error(`${label}: verifierConfirmed boolean required`);
  if (typeof record.fatalConstraint !== "boolean") throw new Error(`${label}: fatalConstraint boolean required`);
  for (const field of ["score", "evidenceScore", "distributionScore"]) {
    if (typeof record[field] !== "number") throw new Error(`${label}: ${field} number required`);
  }
  return record as NightlyPromotion;
}

function parseAdmission(text: string, runId: string) {
  const admission = parseObject(text, `${runId} admission`);
  if (admission.schema !== "nightly-validation-admission-v1" || admission.generatedBy !== "nightly-validation-controller") {
    throw new Error(`${runId} admission: unsupported schema or generator`);
  }
  const runAt = requiredString(admission, "runAt", `${runId} admission`);
  if (!Number.isFinite(Date.parse(runAt))) throw new Error(`${runId} admission: invalid runAt`);
  if (!Array.isArray(admission.selected) || admission.selected.length === 0) {
    throw new Error(`${runId} admission: selected candidates required`);
  }
  return {
    runAt,
    lane: typeof admission.lane === "string" ? admission.lane : null,
    selected: admission.selected as Array<Record<string, unknown>>,
    admissionHash: requiredString(admission, "admissionHash", `${runId} admission`),
  };
}

function parsePromotionEnvelope(text: string, runId: string, admissionHash: string) {
  const envelope = parseObject(text, `${runId} promotion envelope`);
  if (envelope.schema !== "nightly-validation-promotion-v1" || envelope.generatedBy !== "nightly-validation-controller") {
    throw new Error(`${runId} promotion envelope: unsupported schema or generator`);
  }
  if (envelope.admissionHash !== admissionHash) throw new Error(`${runId} promotion envelope: admission hash mismatch`);
  requiredString(envelope, "generatedAt", `${runId} promotion envelope`);
  requiredString(envelope, "artifactHash", `${runId} promotion envelope`);
  if (!Array.isArray(envelope.promotions)) throw new Error(`${runId} promotion envelope: promotions array required`);
  return envelope.promotions.map((item, index) => parsePromotion(item, `${runId} promotion ${index + 1}`));
}

export function parseNightlyValidationSnapshot(input: {
  queueText: string;
  stateText: string;
  runFiles: NightlyRunFile[];
  now?: number;
}): NightlyValidationSnapshot {
  const now = input.now ?? Date.now();
  const runs = input.runFiles.map((file) => {
    const admission = parseAdmission(file.admissionText, file.runId);
    const latestPromotion = [...file.promotionFiles].sort((a, b) => a.name.localeCompare(b.name)).at(-1);
    if (latestPromotion) {
      return {
        runId: file.runId,
        runAt: admission.runAt,
        status: "reconciled" as const,
        lane: admission.lane,
        selected: admission.selected,
        promotions: parsePromotionEnvelope(latestPromotion.text, file.runId, admission.admissionHash),
        promotionArtifact: latestPromotion.name,
      };
    }
    const stale = now - Date.parse(admission.runAt) > PENDING_STALE_MS;
    return {
      runId: file.runId,
      runAt: admission.runAt,
      status: stale ? "blocked" as const : "admitted" as const,
      lane: admission.lane,
      selected: admission.selected,
      promotions: [],
      issue: stale ? "Admission is stale and has not been reconciled within 24 hours." : undefined,
    };
  }).sort((a, b) => b.runAt.localeCompare(a.runAt));

  const failures = stateArray(input.stateText, "failures_json");
  const latestStatus = runs[0]?.status;
  return {
    status: latestStatus ?? (failures.length ? "blocked" : "no-work"),
    queue: parseQueue(input.queueText),
    state: {
      lastCompletedRun: stateValue(input.stateText, "last_completed_run"),
      nextRun: stateValue(input.stateText, "next_run"),
      failures,
    },
    runs,
  };
}
