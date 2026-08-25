import { describe, expect, test } from "bun:test";
import { agentToSignal, cronToSignal, extractEvidence, proofToSignal, taskToSignal } from "./adapters";

const now = Date.now();

describe("taskToSignal", () => {
  test("treats a JT-owned todo as work in flight, not a decision", () => {
    const signal = taskToSignal({
      _id: "task-1",
      title: "Apply: Decagon Agent Development Team",
      description: "Resume\nhttps://docs.google.com/document/d/example/edit",
      status: "todo",
      assignee: "jt",
      priority: "high",
      project: "Job Market",
      updatedAt: now,
    });

    expect(signal.id).toBe("task-1");
    expect(signal.owner).toBe("jt");
    expect(signal.status).toBe("in-progress");
    expect(signal.lane).toBe("revenue");
    expect(signal.evidence[0]).toMatchObject({ kind: "drive", quality: "verified" });
  });

  test("maps the external-block and snooze statuses through", () => {
    const base = { title: "Yair signs scope", assignee: "jt", priority: "high" } as const;
    expect(taskToSignal({ ...base, status: "waiting-external" }).status).toBe("waiting-external");
    expect(taskToSignal({ ...base, status: "snoozed" }).status).toBe("snoozed");
    expect(taskToSignal({ ...base, status: "archived" }).status).toBe("archived");
  });

  test("a shared high-priority task is still a real approval gate", () => {
    const signal = taskToSignal({
      title: "Approve Altmark retainer",
      status: "todo",
      assignee: "both",
      priority: "high",
      project: "Consulting",
    });
    expect(signal.status).toBe("awaiting-approval");
  });

  test("a stored lane wins over the title regex fallback", () => {
    const stored = taskToSignal({
      title: "Client outreach sequence",
      status: "todo",
      assignee: "jt",
      priority: "medium",
      project: "Consulting",
      lane: "machine",
    });
    expect(stored.lane).toBe("machine");

    const fallback = taskToSignal({
      title: "Client outreach sequence",
      status: "todo",
      assignee: "jt",
      priority: "medium",
      project: "Consulting",
    });
    expect(fallback.lane).toBe("revenue");
  });

  test("carries stored scoring fields onto the signal", () => {
    const signal = taskToSignal({
      title: "Collect DHCR deposit",
      status: "todo",
      assignee: "jt",
      priority: "high",
      lane: "revenue",
      dollars: 3500,
      stageProbability: 1,
      dueDate: 1_700_000_000_000,
      dueDateSource: "external",
      effortMinutes: 30,
      proofRequired: true,
      waitingOn: { who: "Yair", what: "signature", since: 1, nudgeAfterDays: 3 },
    });

    expect(signal).toMatchObject({
      dollars: 3500,
      stageProbability: 1,
      dueDate: 1_700_000_000_000,
      dueDateSource: "external",
      effortMinutes: 30,
      proofRequired: true,
    });
    expect(signal.waitingOn?.who).toBe("Yair");
  });

  test("carries agent operating-system metadata without changing the task lane", () => {
    const signal = taskToSignal({
      title: "Validate a career hedge",
      status: "todo",
      assignee: "jt",
      priority: "medium",
      lane: "work",
      firstAction: "Open the verified posting",
      whyItMatters: "Preserves the income hedge",
      doneState: "Application decision recorded",
      evidenceLinks: ["https://example.com/proof"],
      sourceSystem: "nightly-validation-controller",
      reviewAt: 1_800_000_000_000,
      dedupeKey: "nightly-validation:candidate:hash",
      workstream: "career-hedge",
      hypothesis: "The role maps to direct evidence",
      nextTest: "Verify the top three duties",
      killDate: 1_810_000_000_000,
      promotionScore: 32,
      verdict: "promote",
      verifierConfirmed: true,
      verifiedAt: "2026-08-24T23:00:00Z",
      candidateId: "candidate",
      sourceHash: "sha256:hash",
      evidenceScore: 4,
      distributionScore: 3,
      fatalConstraint: false,
      revivalTrigger: "A matching role reopens",
    });

    expect(signal.lane).toBe("work");
    expect(signal).toMatchObject({
      firstAction: "Open the verified posting",
      whyItMatters: "Preserves the income hedge",
      doneState: "Application decision recorded",
      sourceSystem: "nightly-validation-controller",
      workstream: "career-hedge",
      promotionScore: 32,
      verdict: "promote",
      verifierConfirmed: true,
      candidateId: "candidate",
      sourceHash: "sha256:hash",
      evidenceScore: 4,
      distributionScore: 3,
      fatalConstraint: false,
    });
    expect(signal.evidenceLinks).toEqual(["https://example.com/proof"]);
    expect(signal.evidence).toEqual([{
      kind: "url",
      label: "Evidence 1",
      href: "https://example.com/proof",
      quality: "verified",
    }]);
  });

  test("keeps Eve in-progress work out of the JT decision queue", () => {
    const signal = taskToSignal({
      _id: "task-2",
      title: "Draft AppFolio teardown",
      status: "in-progress",
      assignee: "eve",
      priority: "medium",
      project: "Content",
      updatedAt: now,
    });

    expect(signal.owner).toBe("eve");
    expect(signal.status).toBe("in-progress");
    expect(signal.lane).toBe("ship");
  });
});

describe("cronToSignal", () => {
  test("maps failed cron jobs to machine risk signals", () => {
    const signal = cronToSignal({
      jobId: "cron-1",
      name: "Mission Control Next",
      enabled: true,
      failed: true,
      running: false,
      lastRun: now - 60_000,
      payload: "agentTurn",
    });

    expect(signal.source).toBe("cron");
    expect(signal.status).toBe("failed");
    expect(signal.owner).toBe("eve");
    expect(signal.lane).toBe("machine");
  });
});

describe("agentToSignal", () => {
  test("maps agent definitions to machine signals", () => {
    const signal = agentToSignal({
      id: "research-agent",
      name: "Research Agent",
      role: "Market research",
      domain: "Consulting",
      status: "active",
      currentTask: "Scanning property-management signals",
    });

    expect(signal.id).toBe("agent-research-agent");
    expect(signal.status).toBe("in-progress");
    expect(signal.context).toContain("Market research");
  });
});

describe("proofToSignal", () => {
  test("maps proof entries to evidence signals with verified refs", () => {
    const signal = proofToSignal({
      id: "proof-1",
      title: "Decagon package",
      action_type: "file_creation",
      outcome: "success",
      date: "2026-06-16",
      files: ["memory/drafts/decagon-resume.md"],
      timestamp: "2026-06-16T18:00:00Z",
    });

    expect(signal.id).toBe("proof-proof-1");
    expect(signal.status).toBe("done");
    expect(signal.lane).toBe("evidence");
    expect(signal.evidence[0]).toMatchObject({ kind: "file", quality: "verified" });
  });
});

describe("extractEvidence", () => {
  test("extracts Drive and plain URL evidence from text", () => {
    const evidence = extractEvidence("Doc https://docs.google.com/document/d/abc/edit\nSite https://example.com/x");

    expect(evidence).toHaveLength(2);
    expect(evidence[0].kind).toBe("drive");
    expect(evidence[1].kind).toBe("url");
  });
});
