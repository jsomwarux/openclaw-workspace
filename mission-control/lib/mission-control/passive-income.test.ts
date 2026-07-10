import { describe, expect, test } from "bun:test";
import { parsePassiveIncomeReport } from "./passive-income";

const strategistReport = `# Passive Income Strategist - 2026-07-09

# Full Analysis + Scorecards

## SignalDesk
**Verdict:** BUILD | Score: 8.1/10

### Value Proposition Test
Turns messy client proof into a ranked, source-backed operating packet.

### Market Demand Validation
Operators already pay for reporting, QA, and workflow accountability.

### Competition Landscape
Generic task tools miss the evidence trail, but agency dashboards are crowded.

### Build Reality
Small Next.js app, file parser, and weekly report writer.

### Autonomous Marketing
SEO is weak, but consultant proof artifacts and LinkedIn examples are strong.

### Longevity
Workflow proof survives model churn because operators still need audit trails.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|
| 8 | 7 | 9 | 6 | 8 | 7 | 6 | 8 |
**Weighted total:** 8.1/10
`;

describe("passive income report parsing", () => {
  test("returns decision-quality rationale and score dimensions for strategist ideas", () => {
    const ideas = parsePassiveIncomeReport(strategistReport, "2026-07-09-strategist.md");

    expect(ideas).toHaveLength(1);
    expect(ideas[0]).toMatchObject({
      title: "SignalDesk",
      score: 8.1,
      reportDate: "2026-07-09",
      sourceFile: "memory/passive-income/2026-07-09-strategist.md",
      scoreRationale: "Strong fit: strongest on longevity, build, revenue. Watchouts: marketing, competition.",
      detailCompleteness: 7,
    });
    expect(ideas[0].scoreBreakdown.map((item) => `${item.label}:${item.value}`).join(",")).toBe(
      "Longevity:8,Autonomy:7,Build:9,Marketing:6,Revenue:8,Uniqueness:7,Competition:6,Agent-Purchasable Fit:8",
    );
  });
});
