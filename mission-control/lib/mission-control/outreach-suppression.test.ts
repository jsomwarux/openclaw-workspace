import { describe, expect, test } from "bun:test";
import vectors from "../../contracts/outreach-suppression-v1-vectors.json";
import {
  hashSuppressionEventRevision,
  hashSuppressionOwnerRevision,
  resolveMissionControlSuppressionAdmission,
  resolveSuppressionQuery,
  validateMissionControlSuppressionSubmission,
  type SuppressionEvent,
} from "./outreach-suppression";

const owner = vectors.ownerLedgers.find((entry) => entry.owner === "mission-control")!;

describe("outreach suppression shared contract", () => {
  test("matches the shared event and owner revision golden vectors", async () => {
    for (const event of owner.events) {
      const { revision, ...withoutRevision } = event;
      expect(await hashSuppressionEventRevision(withoutRevision as Omit<SuppressionEvent, "revision">)).toBe(revision);
    }
    for (const vector of owner.ownerRevisions) {
      expect(await hashSuppressionOwnerRevision("mission-control", owner.events.slice(0, vector.eventCount) as SuppressionEvent[]))
        .toBe(vector.revision);
    }
    expect(await hashSuppressionOwnerRevision("mission-control", [...owner.events].reverse() as SuppressionEvent[]))
      .toBe(await hashSuppressionOwnerRevision("mission-control", owner.events as SuppressionEvent[]));
  });

  test("matches shared state precedence and freshness vectors", async () => {
    for (const vector of owner.queryVectors) {
      const result = await resolveSuppressionQuery(
        "mission-control",
        owner.events.slice(0, vector.eventCount) as SuppressionEvent[],
        {
          prospectId: "prospect.alpha",
          organizationFactId: "fact-org:alpha",
          channelFingerprint: owner.events[0].channelFingerprint,
        },
        vector.queriedAt,
      );
      expect(result.observed).toBe(vector.expectedObserved);
      expect(result.clear).toBe(vector.expectedClear);
      expect(result.ownerRevision).toBe(vector.expectedOwnerRevision);
      expect(result.current?.sequence ?? null).toBe(vector.expectedCurrentSequence);
      expect(result.prospectTerminal?.sequence ?? null).toBe(vector.expectedProspectTerminalSequence);
      expect(result.channelTerminal?.sequence ?? null).toBe(vector.expectedChannelTerminalSequence);
    }
  });

  test("validates exact JT-owned caller schema and idempotency", async () => {
    const original = owner.events[0] as SuppressionEvent;
    const submission = {
      schemaVersion: original.schemaVersion,
      requestId: original.requestId,
      prospectId: original.prospectId,
      organizationFactId: original.organizationFactId,
      channelFingerprint: original.channelFingerprint,
      state: original.state,
      evidenceToken: original.evidenceToken,
    };
    validateMissionControlSuppressionSubmission(submission);
    expect(await resolveMissionControlSuppressionAdmission([original], submission, "2026-09-16T14:30:00Z", "f".repeat(20)))
      .toEqual({ operation: "existing", event: original });
    let conflict = "";
    try { await resolveMissionControlSuppressionAdmission([original], { ...submission, state: "manual_hold" }, "2026-09-16T14:30:00Z", "f".repeat(20)); } catch (error) { conflict = String(error); }
    expect(conflict.includes("conflict")).toBe(true);
    for (const malformed of [
      { ...submission, actorId: "jt" },
      { ...submission, observedAt: "2026-09-16T14:30:00Z" },
      { ...submission, unknown: true },
      { ...submission, requestId: "bad" },
    ]) expect(thrown(() => validateMissionControlSuppressionSubmission(malformed))).toBe(true);
  });

  test("rejects corrupt duplicate owner rows before idempotency or sequence allocation", async () => {
    const first = owner.events[0] as SuppressionEvent;
    const second = owner.events[1] as SuppressionEvent;
    const submission = {
      schemaVersion: first.schemaVersion,
      requestId: first.requestId,
      prospectId: first.prospectId,
      organizationFactId: first.organizationFactId,
      channelFingerprint: first.channelFingerprint,
      state: first.state,
      evidenceToken: first.evidenceToken,
    };
    const signed = async (candidate: SuppressionEvent): Promise<SuppressionEvent> => {
      const { revision: _revision, ...withoutRevision } = candidate;
      return { ...withoutRevision, revision: await hashSuppressionEventRevision(withoutRevision) };
    };
    for (const corrupt of [
      [first, await signed({ ...second, sequence: first.sequence })],
      [first, await signed({ ...second, eventId: first.eventId })],
      [first, await signed({ ...second, requestId: first.requestId })],
    ]) {
      let failure = "";
      try { await resolveMissionControlSuppressionAdmission(corrupt as SuppressionEvent[], submission, "2026-09-16T14:30:00Z", "f".repeat(20)); } catch (error) { failure = String(error); }
      expect(failure.includes("corrupt suppression owner")).toBe(true);
      let queryFailure = "";
      try {
        await resolveSuppressionQuery("mission-control", corrupt as SuppressionEvent[], {
          prospectId: first.prospectId,
          organizationFactId: first.organizationFactId,
          channelFingerprint: first.channelFingerprint,
        }, "2026-09-16T14:30:00Z");
      } catch (error) { queryFailure = String(error); }
      expect(queryFailure.includes("corrupt suppression owner")).toBe(true);
    }
  });
});

function thrown(run: () => unknown) { try { run(); return false; } catch { return true; } }
