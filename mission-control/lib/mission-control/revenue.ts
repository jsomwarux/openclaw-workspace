type RawPipelineItem = {
  name: string;
  lane?: string;
  stage: string;
  value: number;
  weight: number;
  next_action: string;
  waiting_on: string;
  last_touch: string;
  source: string;
};

type RawTask = {
  title: string;
  project?: string;
  priority?: string;
  status?: string;
  description?: string;
  updatedAt?: number;
};

export type RevenueMetric = {
  consultingCollected: number;
  unemploymentCollected: number;
  totalCollected: number;
  weightedForecast: number;
  gapCollected: number;
  gapWithForecast: number;
};

export type PipelineItem = RawPipelineItem & {
  weightedValue: number;
  status: "active" | "proposal" | "lead" | "contacted" | "closed";
};

function moneyAfter(label: string, text: string): number {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`${escaped}[^$]*\\$([\\d,]+)`, "i");
  const match = pattern.exec(text);
  return match ? Number(match[1].replace(/,/g, "")) : 0;
}

const NORTH_STAR_LABELS = ["Total collected:", "Pipeline-weighted forecast:", "Consulting:"];

/**
 * A north-star file that parses to all zeros is indistinguishable from one that
 * says JT earned nothing. Callers that show cash need to know which it is, so
 * report whether any metric label was actually present.
 */
export function hasNorthStarMetrics(markdown: string): boolean {
  return NORTH_STAR_LABELS.some((label) => new RegExp(`${label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[^$]*\\$`, "i").test(markdown));
}

export function parseNorthStarMetrics(markdown: string): RevenueMetric {
  return {
    consultingCollected: moneyAfter("Consulting:", markdown),
    unemploymentCollected: moneyAfter("Unemployment:", markdown),
    totalCollected: moneyAfter("Total collected:", markdown),
    weightedForecast: moneyAfter("Pipeline-weighted forecast:", markdown),
    gapCollected: moneyAfter("Gap to $10K collected:", markdown),
    gapWithForecast: moneyAfter("Gap to $10K including weighted forecast:", markdown),
  };
}

export function parsePipelineJsonl(jsonl: string): { items: PipelineItem[]; totals: { openWeighted: number; closedValue: number } } {
  const items = jsonl
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line) as RawPipelineItem)
    .map((item) => ({
      ...item,
      status: item.stage as PipelineItem["status"],
      weightedValue: Math.round((item.value * item.weight) / 100),
    }));

  const totals = items.reduce(
    (acc, item) => {
      if (item.stage === "closed") acc.closedValue += item.value;
      else acc.openWeighted += item.weightedValue;
      return acc;
    },
    { openWeighted: 0, closedValue: 0 },
  );

  return { items, totals };
}

export function revenueTasks(tasks: RawTask[]) {
  const active = tasks.filter((task) => task.status !== "done" && task.status !== "archived");
  return {
    jobUpside: active.filter((task) => task.project === "Job Market" || /^Apply:/i.test(task.title)).slice(0, 5),
    appUpside: active.filter((task) => task.project === "App Marketing").slice(0, 5),
  };
}
