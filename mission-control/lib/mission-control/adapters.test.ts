import { describe, expect, test } from "bun:test";
import { agentToSignal, cronToSignal, extractEvidence, proofToSignal, taskToSignal } from "./adapters";

const now = Date.now();

describe("taskToSignal", () => {
  test("maps a JT high priority consulting task to a revenue decision signal", () => {
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
    expect(signal.status).toBe("awaiting-decision");
    expect(signal.lane).toBe("revenue");
    expect(signal.evidence[0]).toMatchObject({ kind: "drive", quality: "verified" });
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
