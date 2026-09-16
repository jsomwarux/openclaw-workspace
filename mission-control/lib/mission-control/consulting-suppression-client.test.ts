import { describe, expect, test } from "bun:test";
import { recordConsultingSuppressionClear } from "./consulting-suppression-client";

describe("fixed consulting suppression client", () => {
  test("uses fixed interpreter/script/cwd, allowlisted environment, timeout, and exact clear args", async () => {
    let captured: unknown;
    const result = await recordConsultingSuppressionClear({ schemaVersion: "outreach-suppression-event-v1", requestId: "suppression_request_" + "1".repeat(20), prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64), state: "clear", evidenceToken: "evidence_" + "3".repeat(64), actorId: "jt:mission-control-clear" }, async (file, args, options) => {
      captured = { file, args, options };
      return { stdout: '{"created":true,"eventId":"suppression_event_44444444444444444444","ownerRevision":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","observedAt":"2026-09-16T14:00:00Z"}\n', stderr: "" };
    });
    expect(result).toEqual({ created: true, eventId: "suppression_event_44444444444444444444", ownerRevision: "a".repeat(64), observedAt: "2026-09-16T14:00:00Z" });
    expect(captured).toMatchObject({ file: "/usr/bin/python3", options: { cwd: "/Users/jtsomwaru/projects/jt-consulting-pipeline", timeout: 5000, env: { LANG: "C.UTF-8" } } });
    expect(JSON.stringify(captured)).not.toContain("TOKEN");
    expect(JSON.stringify(captured)).not.toContain("PROXY");
  });
  test("rejects stderr, extra stdout, and malformed responses", async () => {
    const input = { schemaVersion: "outreach-suppression-event-v1", requestId: "suppression_request_" + "1".repeat(20), prospectId: "prospect.alpha", organizationFactId: "fact-org:alpha", channelFingerprint: "2".repeat(64), state: "clear", evidenceToken: "evidence_" + "3".repeat(64), actorId: "jt:mission-control-clear" } as const;
    for (const output of [{ stdout: "{}\n{}\n", stderr: "" }, { stdout: "{}\n", stderr: "warning" }, { stdout: "not-json\n", stderr: "" }]) {
      let failed = false; try { await recordConsultingSuppressionClear(input, async () => output); } catch { failed = true; }
      expect(failed).toBe(true);
    }
  });
});
