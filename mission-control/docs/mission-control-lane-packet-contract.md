# Mission Control Lane Packet Contract (Growth OS card envelope v1)

This is the integration contract for Growth OS lane producers (Jobs, LinkedIn, X, apps, passive income, networking, profile/site, and non-review outreach cards). It stays inactive until Mission Control is deployed with `LANE_PACKET_CAPABILITY`, `LANE_PACKET_DECISION_CAPABILITY`, and `LANE_PACKET_JT_LOGIN` configured in Next, plus both capabilities in Convex. Every boundary returns 503 while any of these is missing or blank, or while the two capabilities are equal. Capability values never appear in payloads, artifacts, or logs.

Outreach draft review keeps its own immutable routes (`docs/mission-control-outreach-review-contract.md`). A lane packet can never create, read, or change an outreach review snapshot or decision, and a generic outreach-lane packet never satisfies the outreach pre-send decision lookup.

## Admit a lane packet

`POST /api/tasks/lane-packet`

Header: `X-Lane-Packet-Capability` (producer capability)

```ts
type LanePacketSubmission = {
  lane: "linkedin" | "x" | "outreach" | "jobs" | "apps" | "passive-income" | "networking" | "profile-site";
  dedupeKey: string;          // producer's stable key, 1-200 chars of [A-Za-z0-9._:/-]; not "lane-packet:"-prefixed
  sourceSystem: string;       // producer id, e.g. "job-market-agent"; never "nightly-validation-controller"
  // Seven-field card (feedback starts empty and is append-only)
  title: string;
  whyItMatters: string;
  exactSteps: string[];       // 1-20 non-empty steps
  pasteReadyPrompt?: string;
  pasteDestination?: string;  // required when pasteReadyPrompt is present
  doneState: string;
  description?: string;
  firstAction?: string;
  // Envelope
  artifactRef: { system: string; id: string; url?: string; sha256: string }; // sha256: 64 lowercase hex; url: http(s)
  doneEvidenceType: "post-url" | "message-ref" | "application-ref" | "rsvp-ref" | "profile-edit-ref" | "deploy-ref" | "none";
  expiresAt: number;          // epoch ms, in the future and within 90 days
  estMinutes: number;         // whole minutes, 1-480
  // Optional scoring inputs (same meaning as generic tasks)
  evidenceLinks?: string[]; project?: string; priority?: "high" | "medium" | "low";
  dueDate?: number; dueDateSource?: "external" | "self"; dollars?: number; stageProbability?: number;
  cashDirect?: boolean; proofRequired?: boolean; riskContainment?: boolean; blocks?: number;
  workstream?: "paid-delivery" | "career-hedge" | "compounding-bet" | "administrative" | "other";
  payloadHash?: string;       // optional assertion; must equal the server-computed hash
};
```

Any other field is rejected with 400. The server derives and never accepts from callers: `status` (`todo`), `assignee` (`jt`), `approvalState` (`pending`), `payloadHash`, `admittedPayloadHash`, `packetSchema` (`lane-packet-v1`), `growthLane`, the Signal routing `lane`, and the stored `dedupeKey` (`lane-packet:v1:<lane>:<producer key>`). `approvalState`, `outcomeRef`, `closureReason`, `doneEvidence`, and every outreach review/decision field are rejected by name.

`payloadHash` is SHA-256 over the canonical JSON of the lane, the seven card fields plus `description` and `firstAction`, `artifactRef`, and `doneEvidenceType`. Scheduling metadata (`expiresAt`, `estMinutes`, priority, due date) is not part of it.

Response `200`:

```json
{ "taskId": "…", "created": true, "dedupeKey": "lane-packet:v1:jobs:…", "payloadHash": "…", "approvalState": "pending", "writeMode": "create-only" }
```

Idempotency is keyed by `dedupeKey + payloadHash`:

- An exact retry returns the same `taskId` with `created: false`, even after the card was edited.
- A different payload while a packet with that key is still open returns 409. It is never a silent replace.
- A revised payload may be admitted as a new packet once every earlier version is closed or done.
- A stored key that belongs to a non-packet task returns 409.

Errors are enumerated: 400 (fixed validation message), 401 `lane packet capability required`, 409 `lane packet conflict`, 503 `lane packet authority is not configured`, 500 `lane packet request failed`.

## Transition a lane packet

`PATCH /api/tasks/lane-packet`

| Action | Body | Actor | Effect |
|---|---|---|---|
| `approve` | `{ id, action, payloadHash }` | JT | `approvalState: approved`, bound to that exact hash. A stale hash is 409. Refused after expiry. |
| `reject` | `{ id, action, payloadHash, note? }` | JT | `approvalState: rejected`, `closureReason.kind: rejected`, status `archived`. |
| `complete` | `{ id, action, evidence?, outcomeRef? }` | JT | External action: `evidence.type` must equal `doneEvidenceType` (`post-url` must be https) and the current hash must be approved. Writes `doneEvidence` and, only if supplied, `outcomeRef`. `none` packets complete without evidence or approval. |
| `skip` | `{ id, action, note? }` | JT or Eve | `closureReason.kind: skipped`, status `archived`. |
| `no-action` | `{ id, action, note? }` | JT or Eve | `closureReason.kind: no-action`, status `archived`. |

Authentication:

- With `X-Lane-Packet-Capability`, the actor is Eve (producer) and only `skip` / `no-action` are allowed (403 otherwise). The header never falls through to JT identity.
- Without it, the request must carry `Tailscale-User-Login` equal to `LANE_PACKET_JT_LOGIN`. The server then uses its own `LANE_PACKET_DECISION_CAPABILITY`, which producers never hold. Convex re-checks the capability, so a producer calling Convex directly cannot approve, reject, or complete.

Expiry is server-only. Today hides open packets past `expiresAt` immediately. The internal mutation `tasks:expireDueLanePackets` persists `closureReason.kind: expired` (`closedBy: server`). It is not scheduled; scheduling it is a separately approved `convex/crons.ts` change.

No closure ever writes `outcomeRef` or `doneEvidence`.

## Generic task paths

- `POST`/`PATCH /api/tasks` and `/api/tasks/create-only` reject every envelope field and the reserved `lane-packet:` dedupe prefix. The generic Convex mutations do not accept envelope fields.
- A generic edit to a packet's card content re-hashes the payload. If the packet was approved, it returns to `pending`.
- Generic Done on an external-action packet, generic archive, delete, upsert, dedupe-key changes, reopening a closed or done packet, and snoozing past `expiresAt` fail with a `LANE_PACKET_*` error (409/400).
- `append-feedback` works on packets unchanged and never touches the hash or approval.

## Focus row and Today

The weekly focus row may carry:

- `mandate: "consulting-cash" | "none"` arms or disarms the ship cap. A legacy row without the field keeps `consulting-cash`; no focus row means no mandate.
- `laneCapacity: [{ lane, minutes }]` sets whole minutes from 0 to 1440, one entry per lane. Today presents at most that many estimated minutes of each listed lane's packets at once. Unlisted lanes and non-packet tasks are uncapped. `0` keeps a lane silent.

`allocateToday` in `lib/mission-control/score.ts` is the only function that orders Today. It applies exclusions and expiry, scores, sorts once, then filters by lane capacity in rank order. Packets with an external deadline inside 24 hours bypass capacity but still consume it, and the rest are reported as overflow. `commandQueue` and the command brief read its result. The Priority Audit's `priority`, `sortOrder`, and `rankScore` are Work-lane fields and never affect Today order. Overflow appears as one line in the UP NEXT header, never as a list.
