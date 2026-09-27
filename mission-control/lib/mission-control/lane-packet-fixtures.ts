// Synthetic lane-packet fixtures. Every value is invented for tests: no real
// company, contact, application, or client appears here.
import type { LanePacketSubmission } from "./lane-packet";

export const FIXTURE_NOW = Date.UTC(2026, 8, 28, 13, 0, 0); // 2026-09-28 09:00 ET
const DAY_MS = 24 * 60 * 60 * 1000;

export function jobsPacketFixture(overrides: Partial<LanePacketSubmission> = {}): LanePacketSubmission {
  return {
    lane: "jobs",
    dedupeKey: "job-market-agent:role:synthetic-acme-ai-enablement-lead",
    sourceSystem: "job-market-agent",
    title: "Apply: AI Enablement Lead (synthetic Acme Robotics)",
    whyItMatters: "Role clears the 20/25 competitiveness gate and the salary floor; the posting closes Friday.",
    exactSteps: [
      "Open the tailored resume and cover letter from the artifact link.",
      "Submit through the employer portal using the paste-ready answers.",
      "Paste the portal confirmation ID into Mission Control as evidence.",
    ],
    pasteReadyPrompt: "Why this role: I turn manual operating work into governed AI workflows with measured outcomes.",
    pasteDestination: "Employer portal → 'Why are you interested in this role?' field",
    doneState: "Application submitted and the portal confirmation ID is recorded as evidence.",
    artifactRef: {
      system: "drive",
      id: "synthetic-acme-application-package-v1",
      url: "https://drive.google.com/drive/folders/synthetic-acme-package",
      sha256: "1".repeat(64),
    },
    doneEvidenceType: "application-ref",
    expiresAt: FIXTURE_NOW + 4 * DAY_MS,
    estMinutes: 25,
    workstream: "career-hedge",
    project: "Job Market",
    ...overrides,
  };
}

export function linkedinPacketFixture(overrides: Partial<LanePacketSubmission> = {}): LanePacketSubmission {
  return {
    lane: "linkedin",
    dedupeKey: "eve:linkedin:proof-packet:synthetic-build-note-1",
    sourceSystem: "eve",
    title: "Post: build note on idempotent task admission (synthetic)",
    whyItMatters: "Proof-led post from a verified build; keeps the weekly proof cadence without a new claim.",
    exactSteps: [
      "Read the draft and the proof record it cites.",
      "Approve the draft, or append feedback for a revision.",
      "Publish on LinkedIn and paste the post URL as evidence.",
    ],
    pasteReadyPrompt: "Retries should be boring. Here is how a create-only admission route makes them boring.",
    pasteDestination: "LinkedIn → Start a post",
    doneState: "Post is live and its URL is recorded as evidence.",
    artifactRef: {
      system: "jt-ops",
      id: "proof-ledger/synthetic-build-note-1",
      sha256: "2".repeat(64),
    },
    doneEvidenceType: "post-url",
    expiresAt: FIXTURE_NOW + 3 * DAY_MS,
    estMinutes: 15,
    workstream: "compounding-bet",
    project: "Content",
    proofRequired: true,
    ...overrides,
  };
}
