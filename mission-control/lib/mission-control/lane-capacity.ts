import { GROWTH_LANES, LANE_PACKET_SCHEMA, isGrowthLane, type GrowthLane } from "./lane-packet";
import { GROWTH_LANE_LABELS } from "./lane-packet-display";
import type { Signal } from "./types";

export type LaneCapacity = { lane: GrowthLane; minutes: number };
export type LaneOverflow = { lane: GrowthLane; count: number; minutes: number };

const MAX_LANE_MINUTES = 24 * 60;
const DAY_MS = 24 * 60 * 60 * 1000;

function isPacketSignal(signal: Signal): signal is Signal & { growthLane: GrowthLane; estMinutes: number } {
  return signal.packetSchema === LANE_PACKET_SCHEMA && isGrowthLane(signal.growthLane) && typeof signal.estMinutes === "number";
}

/** An open lane packet at or past its expiry. Legacy tasks never expire here. */
export function isExpiredLanePacket(signal: Signal, now: number): boolean {
  return signal.packetSchema === LANE_PACKET_SCHEMA && typeof signal.expiresAt === "number" && now >= signal.expiresAt;
}

/** A real external deadline inside 24 hours outranks lane budgeting. Self-set dates do not. */
function hasGenuineDeadline(signal: Signal, now: number): boolean {
  return signal.dueDateSource === "external" && typeof signal.dueDate === "number" && signal.dueDate - now <= DAY_MS;
}

/**
 * Applies the focus row's per-lane minute capacity to an already-ranked list.
 * It only filters: kept items stay in rank order. Packets that do not fit are
 * reported as explicit overflow per lane. Lanes without an entry, and signals
 * that are not lane packets, are never capped.
 */
export function applyLaneCapacity(
  ranked: Signal[],
  capacity: LaneCapacity[] | undefined,
  now: number,
): { kept: Signal[]; overflow: LaneOverflow[] } {
  if (!capacity || capacity.length === 0) return { kept: ranked, overflow: [] };
  const limits = new Map(capacity.map((entry) => [entry.lane, entry.minutes]));
  const used = new Map<GrowthLane, number>();
  const overflowByLane = new Map<GrowthLane, LaneOverflow>();
  const kept: Signal[] = [];

  for (const signal of ranked) {
    if (!isPacketSignal(signal) || !limits.has(signal.growthLane)) {
      kept.push(signal);
      continue;
    }
    const lane = signal.growthLane;
    const spent = used.get(lane) ?? 0;
    if (hasGenuineDeadline(signal, now) || spent + signal.estMinutes <= (limits.get(lane) ?? 0)) {
      used.set(lane, spent + signal.estMinutes);
      kept.push(signal);
      continue;
    }
    const entry = overflowByLane.get(lane) ?? { lane, count: 0, minutes: 0 };
    overflowByLane.set(lane, { lane, count: entry.count + 1, minutes: entry.minutes + signal.estMinutes });
  }

  const overflow = GROWTH_LANES.flatMap((lane) => {
    const entry = overflowByLane.get(lane);
    return entry ? [entry] : [];
  });
  return { kept, overflow };
}

/** One muted line for Today's UP NEXT header. Overflow is a count, never a second list. */
export function formatLaneOverflow(overflow: LaneOverflow[]): string | null {
  if (overflow.length === 0) return null;
  const total = overflow.reduce((sum, entry) => sum + entry.count, 0);
  const lanes = overflow.map((entry) => `${GROWTH_LANE_LABELS[entry.lane]} ${entry.count} · ${entry.minutes}m`).join(", ");
  return `${total} over lane capacity (${lanes})`;
}

/** A focus row's capacity list: one entry per lane, whole minutes from 0 to 1440. */
export function isValidLaneCapacity(value: unknown): value is LaneCapacity[] {
  if (!Array.isArray(value)) return false;
  const seen = new Set<string>();
  for (const entry of value) {
    if (!entry || typeof entry !== "object") return false;
    const { lane, minutes } = entry as Record<string, unknown>;
    if (!isGrowthLane(lane) || seen.has(lane)) return false;
    if (typeof minutes !== "number" || !Number.isInteger(minutes) || minutes < 0 || minutes > MAX_LANE_MINUTES) return false;
    seen.add(lane);
  }
  return true;
}
