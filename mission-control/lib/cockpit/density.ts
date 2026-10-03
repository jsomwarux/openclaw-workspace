// README spacing: 4 px-based steps, each scaled by the density token --mc-d. Shared by the
// Tailwind config (which turns them into p-d20, gap-d16 and so on) and the cockpit's class merger.
export const DENSITY_STEPS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 56];

export const densitySpacing: Record<string, string> = Object.fromEntries(
  DENSITY_STEPS.map((px) => [`d${px}`, `calc(${px}px * var(--mc-d, 1))`]),
);
