import { NextResponse } from "next/server";
import { readdirSync, readFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";
import { execSync } from "child_process";

const HOME = homedir();
const COSTS_DIR = join(HOME, ".openclaw/workspace/memory/costs");
const X_API_LOG = join(COSTS_DIR, "x-api.jsonl");
const ALERTS = { session: 2.0, daily: 10.0, monthly: 75.0, goal: 50.0 };
// X API budget targets (weekly)
const X_BUDGET = { weekly_target: 10.0, weekly_warn: 8.0 };

function loadXApiCosts(): { today: number; week: number; month: number; daily: Record<string, number>; weekly_pace: number } {
  const result = { today: 0, week: 0, month: 0, daily: {} as Record<string, number>, weekly_pace: 0 };
  if (!existsSync(X_API_LOG)) return result;
  try {
    const lines = readFileSync(X_API_LOG, "utf-8").trim().split("\n").filter(Boolean);
    const now = new Date();
    const todayStr = now.toISOString().slice(0, 10);
    const weekAgo = new Date(now); weekAgo.setDate(now.getDate() - 7);
    const monthStr = now.toISOString().slice(0, 7);
    for (const line of lines) {
      try {
        const e = JSON.parse(line);
        const cost = e.cost_usd || 0;
        const date = e.date || "";
        if (date === todayStr) result.today += cost;
        if (new Date(date) >= weekAgo) result.week += cost;
        if (date.startsWith(monthStr)) result.month += cost;
        result.daily[date] = (result.daily[date] || 0) + cost;
      } catch { /* skip malformed */ }
    }
    // Weekly pace: extrapolate from days seen this week
    const daysWithData = Object.keys(result.daily).filter(d => new Date(d) >= weekAgo).length;
    result.weekly_pace = daysWithData > 0 ? (result.week / daysWithData) * 7 : 0;
  } catch { /* non-fatal */ }
  return result;
}

function loadSnapshot(date: string): any | null {
  const fp = join(COSTS_DIR, `${date}.json`);
  if (!existsSync(fp)) return null;
  try { return JSON.parse(readFileSync(fp, "utf-8")); } catch { return null; }
}

export async function GET() {
  // Refresh today's snapshot live before reading — ensures current-session spend is shown
  try {
    execSync(`python3 ${join(homedir(), ".openclaw/workspace/scripts/cost-tracker.py")} --snapshot`, {
      timeout: 8000,
      stdio: "ignore",
    });
  } catch {
    // Non-fatal — fall through to cached snapshot if live fetch fails
  }

  if (!existsSync(COSTS_DIR)) return NextResponse.json({ error: "No cost data found" }, { status: 404 });

  // Load all available snapshots, most recent first
  const dates = readdirSync(COSTS_DIR)
    .filter(f => f.endsWith(".json") && /^\d{4}-\d{2}-\d{2}\.json$/.test(f))
    .map(f => f.replace(".json", ""))
    .sort()
    .reverse();

  const snapshots = dates.map(d => ({ date: d, data: loadSnapshot(d) })).filter(s => s.data);

  if (snapshots.length === 0) return NextResponse.json({ error: "No snapshots available" }, { status: 404 });

  const today = snapshots[0];
  const yesterday = snapshots[1] ?? null;

  // Monthly totals (current calendar month)
  const currentMonth = today.date.slice(0, 7); // YYYY-MM
  const monthSnapshots = snapshots.filter(s => s.date.startsWith(currentMonth));
  const monthTotal = monthSnapshots.reduce((sum, s) => sum + (s.data.total_usd ?? 0), 0);
  const daysInMonth = new Date(
    parseInt(currentMonth.split("-")[0]),
    parseInt(currentMonth.split("-")[1]),
    0
  ).getDate();
  const dayOfMonth = parseInt(today.date.split("-")[2]);
  const monthlyPace = dayOfMonth > 0 ? (monthTotal / dayOfMonth) * daysInMonth : 0;

  // By-model aggregation across month
  const byModel: Record<string, { sessions: number; cost_usd: number; input_tokens: number; output_tokens: number; cache_read: number }> = {};
  for (const snap of monthSnapshots) {
    for (const [model, data] of Object.entries(snap.data.by_model ?? {})) {
      if (model === "unknown") continue;
      const d = data as any;
      if (!byModel[model]) byModel[model] = { sessions: 0, cost_usd: 0, input_tokens: 0, output_tokens: 0, cache_read: 0 };
      byModel[model].sessions   += d.sessions ?? 0;
      byModel[model].cost_usd   += d.cost_usd ?? 0;
      byModel[model].input_tokens  += d.input_tokens ?? 0;
      byModel[model].output_tokens += d.output_tokens ?? 0;
      byModel[model].cache_read    += d.cache_read ?? 0;
    }
  }

  // Daily trend — last 14 days
  const dailyTrend = snapshots.slice(0, 14).map(s => ({
    date: s.date,
    total_usd: s.data.total_usd ?? 0,
  })).reverse();

  // X API costs
  const xCosts = loadXApiCosts();

  // Alerts
  const alerts: { type: string; message: string; level: "warning" | "critical" }[] = [];
  if (today.data.total_usd >= ALERTS.daily)
    alerts.push({ type: "daily", message: `Daily spend $${today.data.total_usd.toFixed(2)} exceeded $${ALERTS.daily} limit`, level: "critical" });
  if (monthlyPace >= ALERTS.monthly)
    alerts.push({ type: "monthly_pace", message: `Monthly pace $${monthlyPace.toFixed(2)} exceeds $${ALERTS.monthly} cap`, level: "critical" });
  else if (monthlyPace >= ALERTS.goal)
    alerts.push({ type: "monthly_pace", message: `Monthly pace $${monthlyPace.toFixed(2)} is above $${ALERTS.goal} goal`, level: "warning" });
  if (xCosts.weekly_pace >= X_BUDGET.weekly_target)
    alerts.push({ type: "x_weekly", message: `X API weekly pace $${xCosts.weekly_pace.toFixed(2)} exceeds $${X_BUDGET.weekly_target} target`, level: "critical" });
  else if (xCosts.weekly_pace >= X_BUDGET.weekly_warn)
    alerts.push({ type: "x_weekly", message: `X API weekly pace $${xCosts.weekly_pace.toFixed(2)} approaching $${X_BUDGET.weekly_target} target`, level: "warning" });

  return NextResponse.json({
    today: {
      date: today.date,
      total_usd: today.data.total_usd ?? 0,
      by_model: today.data.by_model ?? {},
      alerts_fired: today.data.alerts_fired ?? [],
    },
    yesterday: yesterday ? {
      date: yesterday.date,
      total_usd: yesterday.data.total_usd ?? 0,
    } : null,
    month: {
      label: currentMonth,
      total_usd: monthTotal,
      pace_usd: monthlyPace,
      goal_usd: ALERTS.goal,
      cap_usd: ALERTS.monthly,
      days_elapsed: dayOfMonth,
      days_in_month: daysInMonth,
      pct_of_goal: Math.min((monthTotal / ALERTS.goal) * 100, 100),
    },
    by_model: byModel,
    daily_trend: dailyTrend,
    alerts,
    thresholds: ALERTS,
    x_api: {
      today_usd: parseFloat(xCosts.today.toFixed(4)),
      week_usd: parseFloat(xCosts.week.toFixed(4)),
      month_usd: parseFloat(xCosts.month.toFixed(4)),
      weekly_pace_usd: parseFloat(xCosts.weekly_pace.toFixed(4)),
      weekly_target_usd: X_BUDGET.weekly_target,
      daily_breakdown: xCosts.daily,
    },
  });
}
