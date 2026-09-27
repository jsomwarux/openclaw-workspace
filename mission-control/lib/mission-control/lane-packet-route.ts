import { NextResponse } from "next/server";
import { assertDistinctServerCapability, authorizeJtIdentity, OutreachAuthError } from "./outreach-auth";
import { LanePacketError, validateLanePacketSubmission, type ApprovalState, type LanePacketSubmission } from "./lane-packet";
import {
  validateLanePacketTransition,
  type LanePacketActor,
  type LanePacketTransition,
} from "./lane-packet-transitions";

export const LANE_PACKET_CAPABILITY_HEADER = "X-Lane-Packet-Capability";

type AdmissionResult = {
  taskId: string;
  created: boolean;
  dedupeKey: string;
  payloadHash: string;
  approvalState: ApprovalState;
};

type TransitionResult = {
  taskId: string;
  changed: boolean;
  status: unknown;
  approvalState: unknown;
  payloadHash: unknown;
};

type Dependencies = {
  producerCapability: string | undefined;
  decisionCapability: string | undefined;
  trustedJtLogin: string | undefined;
  admit: (input: { packet: LanePacketSubmission; capability: string }) => Promise<AdmissionResult>;
  transition: (input: {
    id: string;
    transition: LanePacketTransition;
    actor: LanePacketActor;
    capability: string;
  }) => Promise<TransitionResult>;
  now?: () => number;
};

const PRODUCER_ACTIONS = new Set<LanePacketTransition["action"]>(["skip", "no-action"]);

const DEPENDENCY_ERRORS: Record<string, [number, string]> = {
  CONFLICT: [409, "lane packet conflict"],
  CLOSED: [409, "lane packet is already closed"],
  EXPIRED: [409, "lane packet expired"],
  TRANSITION_REQUIRED: [409, "lane packet change requires /api/tasks/lane-packet"],
  NOT_FOUND: [404, "lane packet not found"],
  FORBIDDEN: [403, "lane packet action forbidden"],
  INVALID: [400, "invalid lane packet request"],
  NOT_CONFIGURED: [503, "lane packet authority is not configured"],
  UNAUTHORIZED: [401, "lane packet capability required"],
};

/**
 * Maps an enumerated `LANE_PACKET_*` Convex error to a safe response. Returns
 * null for anything else so generic routes keep their existing behavior.
 */
export function lanePacketDependencyErrorResponse(error: unknown): Response | null {
  const message = error instanceof Error ? error.message : "";
  const match = /(?:^|[^A-Z0-9_])LANE_PACKET_([A-Z_]+)(?:$|[^A-Z0-9_])/.exec(message);
  const mapped = match ? DEPENDENCY_ERRORS[match[1]] : undefined;
  if (!mapped) return null;
  return NextResponse.json({ error: mapped[1] }, { status: mapped[0] });
}

function dependencyError(error: unknown): Response {
  return lanePacketDependencyErrorResponse(error)
    ?? NextResponse.json({ error: "lane packet request failed" }, { status: 500 });
}

function authError(error: OutreachAuthError): Response {
  if (error.status === 503) return NextResponse.json({ error: "lane packet authority is not configured" }, { status: 503 });
  if (error.status === 403) return NextResponse.json({ error: "JT identity forbidden" }, { status: 403 });
  if (error.message === "JT identity required") return NextResponse.json({ error: "JT identity required" }, { status: 401 });
  return NextResponse.json({ error: "lane packet capability required" }, { status: 401 });
}

function requestError(error: unknown): Response {
  if (error instanceof OutreachAuthError) return authError(error);
  if (error instanceof LanePacketError) return NextResponse.json({ error: error.message }, { status: 400 });
  return NextResponse.json({ error: "invalid lane packet request" }, { status: 400 });
}

async function readJson(req: Request): Promise<unknown> {
  try {
    return await req.json();
  } catch {
    throw new LanePacketError("invalid", "invalid JSON body");
  }
}

/**
 * Generic Growth OS lane-packet boundary.
 *
 * POST  — create-only, idempotent admission. Requires the producer capability.
 * PATCH — governed transitions. With the producer capability header the actor
 *         is Eve and only skip/no-action are allowed. Without it, the request
 *         must carry JT's Tailscale identity; the server then uses its own
 *         decision capability, which producers never hold.
 */
export function createLanePacketHandlers(dependencies: Dependencies) {
  const now = dependencies.now ?? Date.now;

  async function producerCapability(provided: string | undefined): Promise<string> {
    return assertDistinctServerCapability(provided, dependencies.producerCapability, dependencies.decisionCapability);
  }

  async function jtDecisionCapability(req: Request): Promise<string> {
    authorizeJtIdentity(req.headers, dependencies.trustedJtLogin);
    return assertDistinctServerCapability(
      dependencies.decisionCapability,
      dependencies.decisionCapability,
      dependencies.producerCapability,
    );
  }

  return {
    POST: async (req: Request) => {
      let packet: LanePacketSubmission;
      let capability: string;
      try {
        capability = await producerCapability(req.headers.get(LANE_PACKET_CAPABILITY_HEADER) ?? undefined);
        packet = validateLanePacketSubmission(await readJson(req), now());
      } catch (error) {
        return requestError(error);
      }
      try {
        const result = await dependencies.admit({ packet, capability });
        return NextResponse.json({
          taskId: result.taskId,
          created: result.created,
          dedupeKey: result.dedupeKey,
          payloadHash: result.payloadHash,
          approvalState: result.approvalState,
          writeMode: "create-only",
        });
      } catch (error) {
        return dependencyError(error);
      }
    },

    PATCH: async (req: Request) => {
      let actor: LanePacketActor;
      let capability: string;
      let request;
      try {
        if (req.headers.has(LANE_PACKET_CAPABILITY_HEADER)) {
          capability = await producerCapability(req.headers.get(LANE_PACKET_CAPABILITY_HEADER) ?? undefined);
          actor = "eve";
        } else {
          capability = await jtDecisionCapability(req);
          actor = "jt";
        }
        request = validateLanePacketTransition(await readJson(req));
      } catch (error) {
        return requestError(error);
      }
      const { id, ...transition } = request;
      if (actor === "eve" && !PRODUCER_ACTIONS.has(transition.action)) {
        return NextResponse.json({ error: "producers may only skip or close lane packets with no action" }, { status: 403 });
      }
      try {
        const result = await dependencies.transition({ id, transition, actor, capability });
        return NextResponse.json({
          taskId: result.taskId,
          changed: result.changed,
          status: result.status,
          approvalState: result.approvalState,
          payloadHash: result.payloadHash,
        });
      } catch (error) {
        return dependencyError(error);
      }
    },
  };
}
