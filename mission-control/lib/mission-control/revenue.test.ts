import { describe, expect, test } from "bun:test";
import { hasNorthStarMetrics, parseNorthStarMetrics, parsePipelineJsonl, revenueTasks } from "./revenue";

const northStar = `# North Star Scoreboard - 2026-06

Targets: $10K safe / $30K free / $100K rich monthly income.

Current June collected:
- Consulting: $3,375 confirmed from Altmark ($1,125 insurance final 50% + $2,250 rent delinquency kickoff).
- Unemployment: ~$2,200 for 3 weeks.
- Crypto/apps: $0 current income; crypto remains monitor-only.
- Total collected: ~$5,575.

Pipeline-weighted forecast: ~$4,058 from \`memory/pipeline.jsonl\`.
Gap to $10K collected: ~$4,425.
Gap to $10K including weighted forecast: ~$368.
`;

const pipeline = [
  {
    name: "Altmark rent delinquency remaining",
    lane: "consulting",
    stage: "active",
    value: 2250,
    weight: 55,
    next_action: "Send/confirm packet",
    waiting_on: "client",
    last_touch: "2026-06-11",
    source: "source.md",
  },
  {
    name: "Aya StreetEasy scraper",
    lane: "consulting",
    stage: "closed",
    value: 1000,
    weight: 0,
    next_action: "Closed/cancelled",
    waiting_on: "none",
    last_touch: "2026-06-11",
    source: "JT",
  },
]
  .map((entry) => JSON.stringify(entry))
  .join("\n");

describe("parseNorthStarMetrics", () => {
  test("extracts current cash scoreboard values", () => {
    expect(parseNorthStarMetrics(northStar)).toMatchObject({
      consultingCollected: 3375,
      unemploymentCollected: 2200,
      totalCollected: 5575,
      weightedForecast: 4058,
      gapCollected: 4425,
      gapWithForecast: 368,
    });
  });
});

describe("hasNorthStarMetrics", () => {
  test("reports metrics present when the scoreboard carries cash labels", () => {
    expect(hasNorthStarMetrics(northStar)).toBe(true);
  });

  test("reports no metrics for an empty or prose-only file, so zeros are never shown as real cash", () => {
    expect(hasNorthStarMetrics("")).toBe(false);
    expect(hasNorthStarMetrics("# North Star\n\nJuly collected consulting cash: UNVERIFIED.\n")).toBe(false);
  });
});

describe("parsePipelineJsonl", () => {
  test("parses active pipeline and calculates weighted value", () => {
    const result = parsePipelineJsonl(pipeline);

    expect(result.items).toHaveLength(2);
    expect(result.items[0]).toMatchObject({
      name: "Altmark rent delinquency remaining",
      weightedValue: 1238,
      status: "active",
    });
    expect(result.totals.openWeighted).toBe(1238);
    expect(result.totals.closedValue).toBe(1000);
  });
});

describe("revenueTasks", () => {
  test("groups job and app upside tasks without mixing in machine work", () => {
    const grouped = revenueTasks([
      { title: "Apply: Decagon Agent Development Team", project: "Job Market", priority: "medium", status: "todo" },
      { title: "Nash Satoshi: submit first methodology-backed directory listing", project: "App Marketing", priority: "high", status: "todo" },
      { title: "OpenClaw beta update", project: "Skills", priority: "medium", status: "todo" },
    ]);

    expect(grouped.jobUpside).toHaveLength(1);
    expect(grouped.appUpside).toHaveLength(1);
  });
});
