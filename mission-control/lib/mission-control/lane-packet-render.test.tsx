import { describe, expect, test } from "bun:test";
import { renderToStaticMarkup } from "react-dom/server";
import { InspectionDrawer } from "@/components/mission-control/InspectionDrawer";
import { admitLanePacket, transitionLanePacket } from "../../convex/tasks";
import { taskToSignal } from "./adapters";
import { ConvexTestDb, testCtx, withEnv } from "./convex-test-db";
import { FIXTURE_NOW, jobsPacketFixture, linkedinPacketFixture } from "./lane-packet-fixtures";
import { formatLaneOverflow } from "./lane-capacity";
import { lanePacketActions, lanePacketDetails } from "./lane-packet-display";
import type { LanePacketSubmission } from "./lane-packet";

type Handler = (context: any, args: any) => Promise<any>;
const handler = (fn: unknown) => (fn as { _handler: Handler })._handler;
const ENV = { LANE_PACKET_CAPABILITY: "lane-producer-test-value", LANE_PACKET_DECISION_CAPABILITY: "lane-decision-test-value" };

function atFixtureTime<T>(run: () => Promise<T>): Promise<T> {
  const realNow = Date.now;
  Date.now = () => FIXTURE_NOW;
  return run().finally(() => { Date.now = realNow; });
}

async function admitTwice(db: ConvexTestDb, packet: LanePacketSubmission) {
  return atFixtureTime(() => withEnv(ENV, async () => {
    const first = await handler(admitLanePacket)(testCtx(db), { packet, capability: ENV.LANE_PACKET_CAPABILITY });
    const retry = await handler(admitLanePacket)(testCtx(db), { packet, capability: ENV.LANE_PACKET_CAPABILITY });
    return { first, retry };
  }));
}

// Render at fixture time: the drawer's available actions depend on expiry, so a
// real clock would make this test pass or fail depending on the day it runs.
function render(row: Record<string, unknown>): string {
  const realNow = Date.now;
  Date.now = () => FIXTURE_NOW + 60_000;
  try {
    return renderToStaticMarkup(<InspectionDrawer signal={taskToSignal(row as any)} onClose={() => {}} />);
  } finally {
    Date.now = realNow;
  }
}

function assertSevenFieldCard(html: string, packet: LanePacketSubmission) {
  // The seven universal card fields, rendered by the existing drawer in order.
  const markers = [
    packet.title,
    "Why it matters", packet.whyItMatters,
    "Exact steps", `1. ${packet.exactSteps[0]}`, `${packet.exactSteps.length}. ${packet.exactSteps[packet.exactSteps.length - 1]}`,
    "Paste-ready prompt", packet.pasteReadyPrompt!,
    "Paste/use location", packet.pasteDestination!,
    "Done condition", packet.doneState,
    "Feedback", "No feedback recorded yet.",
  ].map((marker) => marker.replace(/&/g, "&amp;").replace(/'/g, "&#x27;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;"));
  let cursor = -1;
  for (const marker of markers) {
    const index = html.indexOf(marker, cursor + 1);
    expect(index).toBeGreaterThan(cursor);
    cursor = index;
  }
}

describe("one Jobs packet and one LinkedIn packet: admitted idempotently, rendered as seven-field cards", () => {
  test("each fixture is admitted once; its exact retry returns the same task", async () => {
    const db = new ConvexTestDb();
    const jobs = await admitTwice(db, jobsPacketFixture());
    const linkedin = await admitTwice(db, linkedinPacketFixture());
    expect(jobs.first.created).toBe(true);
    expect(jobs.retry).toEqual({ ...jobs.first, created: false });
    expect(linkedin.first.created).toBe(true);
    expect(linkedin.retry).toEqual({ ...linkedin.first, created: false });
    expect(db.rows).toHaveLength(2);
  });

  test("the existing InspectionDrawer renders both admitted packets as seven-field cards plus the envelope", async () => {
    const db = new ConvexTestDb();
    const cases: Array<[LanePacketSubmission, string, string, string]> = [
      [jobsPacketFixture(), "Jobs", "Application confirmation", "25 min"],
      [linkedinPacketFixture(), "LinkedIn", "Post URL", "15 min"],
    ];
    for (const [packet, laneLabel, evidenceLabel, minutes] of cases) {
      const { first } = await admitTwice(db, packet);
      const html = render(db.snapshot(first.taskId)!);
      assertSevenFieldCard(html, packet);
      expect(html).toContain("Lane packet");
      expect(html).toContain(laneLabel);
      expect(html).toContain("Pending approval");
      expect(html).toContain(evidenceLabel);
      expect(html).toContain(minutes);
      expect(html).toContain(">Approve<");
      expect(html.includes("Record evidence")).toBe(false);
      expect(html).toContain("Complete or close this card with the lane packet controls.");
    }
  });

  test("after JT approves, the card asks for the typed evidence instead of offering approval", async () => {
    const db = new ConvexTestDb();
    const { first } = await admitTwice(db, jobsPacketFixture());
    await atFixtureTime(() => withEnv(ENV, () => handler(transitionLanePacket)(testCtx(db), {
      id: first.taskId, transition: { action: "approve", payloadHash: first.payloadHash }, actor: "jt", capability: ENV.LANE_PACKET_DECISION_CAPABILITY,
    })));
    const html = render(db.snapshot(first.taskId)!);
    expect(html).toContain("Approved");
    expect(html).toContain("Record evidence");
    expect(html.includes(">Approve<")).toBe(false);
  });

  test("a legacy seven-field task still renders without any lane packet section", () => {
    const html = render({
      _id: "legacy-1", title: "Legacy card", status: "todo", assignee: "jt", priority: "medium",
      whyItMatters: "Because", exactSteps: ["One"], doneState: "Done when done", createdAt: 1, updatedAt: 1,
    });
    expect(html).toContain("Why it matters");
    expect(html.includes("Lane packet")).toBe(false);
    expect(html.includes("lane packet controls")).toBe(false);
  });
});

describe("lane packet display helpers", () => {
  const base = taskToSignal({
    _id: "p1", title: "Packet", status: "todo", assignee: "jt", priority: "medium",
    packetSchema: "lane-packet-v1", growthLane: "linkedin", approvalState: "pending", payloadHash: "a".repeat(64),
    doneEvidenceType: "post-url", estMinutes: 15, expiresAt: FIXTURE_NOW + 1000,
    artifactRef: { system: "jt-ops", id: "proof/1", sha256: "b".repeat(64) }, createdAt: 1, updatedAt: 1,
  } as any);

  test("adapter carries the typed envelope and feeds estMinutes to the effort control", () => {
    expect(base).toMatchObject({ packetSchema: "lane-packet-v1", growthLane: "linkedin", approvalState: "pending", estMinutes: 15, effortMinutes: 15 });
  });

  test("actions follow the state machine", () => {
    expect(lanePacketActions(base, FIXTURE_NOW)).toEqual({ canApprove: true, canComplete: false, needsEvidence: true, canClose: true });
    expect(lanePacketActions({ ...base, approvalState: "approved", approvedPayloadHash: "a".repeat(64) }, FIXTURE_NOW)).toEqual({ canApprove: false, canComplete: true, needsEvidence: true, canClose: true });
    expect(lanePacketActions({ ...base, doneEvidenceType: "none" }, FIXTURE_NOW)).toEqual({ canApprove: true, canComplete: true, needsEvidence: false, canClose: true });
    expect(lanePacketActions(base, FIXTURE_NOW + 1000)).toEqual({ canApprove: false, canComplete: false, needsEvidence: true, canClose: true });
    const closed = { ...base, status: "archived" as const, closureReason: { kind: "skipped" as const, closedAt: 1, closedBy: "eve" as const } };
    expect(lanePacketActions(closed, FIXTURE_NOW)).toEqual({ canApprove: false, canComplete: false, needsEvidence: true, canClose: false });
  });

  test("details show outcome and typed closure when present", () => {
    const done = lanePacketDetails({
      ...base,
      status: "done",
      doneEvidence: { type: "post-url", ref: "https://www.linkedin.com/feed/update/1", recordedAt: 1, recordedBy: "jt" },
      outcomeRef: { system: "notion", id: "row-1", recordedAt: 1 },
    });
    const rows = (details: Array<[string, string]>) => details.map(([label, value]) => `${label}=${value}`);
    expect(rows(done)).toContain("Evidence recorded=Post URL: https://www.linkedin.com/feed/update/1");
    expect(rows(done)).toContain("Outcome=notion · row-1");
    const closed = lanePacketDetails({ ...base, status: "archived", closureReason: { kind: "no-action", note: "Stale", closedAt: 1, closedBy: "jt" } });
    expect(rows(closed)).toContain("Closed=No action by JT — Stale");
  });

  test("overflow reads as one line, not a list", () => {
    expect(formatLaneOverflow([])).toBe(null);
    expect(formatLaneOverflow([{ lane: "linkedin", count: 1, minutes: 15 }, { lane: "jobs", count: 2, minutes: 70 }])).toBe(
      "3 over lane capacity (LinkedIn 1 · 15m, Jobs 2 · 70m)",
    );
  });
});
