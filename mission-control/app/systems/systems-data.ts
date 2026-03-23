import type { Node, Edge } from "reactflow";

/* ── helpers ── */
function n(
  id: string,
  label: string,
  type: string,
  x: number,
  y: number,
  subtitle?: string
): Node {
  return {
    id,
    type,
    position: { x, y },
    data: { label, dark: true, subtitle },
  };
}

function e(
  source: string,
  target: string,
  label?: string,
  animated?: boolean
): Edge {
  return {
    id: `${source}-${target}`,
    source,
    target,
    label,
    animated,
    style: { stroke: "#525252", strokeWidth: 1.5 },
    labelStyle: { fontSize: 9, fill: "#a1a1aa", fontWeight: 500 },
    labelBgStyle: { fill: "transparent" },
  };
}

/* ── row Y positions ── */
const R1 = 0;
const R2 = 80;
const R3 = 160;

/* ── column X positions (compact) ── */
const C1 = 0;
const C2 = 180;
const C3 = 360;
const C4 = 540;
const C5 = 720;

export interface SystemDef {
  name: string;
  subtitle: string;
  nodes: Node[];
  edges: Edge[];
  width: number;
  height: number;
}

export const systems: SystemDef[] = [
  /* ── 1. Consulting Pipeline ── */
  {
    name: "Consulting Pipeline",
    subtitle: "Automated prospect discovery, outreach drafting, and follow-up sequences",
    width: 900,
    height: 280,
    nodes: [
      n("cp-1", "Prospect Discovery", "cronNode", C1, R1, "cron"),
      n("cp-2", "Shortlists", "processNode", C2, R1),
      n("cp-3", "Outreach Pipeline", "cronNode", C3, R1, "2AM daily"),
      n("cp-4", "T3 Cold Hook", "cronNode", C3, R2, "Tue/Thu"),
      n("cp-5", "Drive Drafts", "processNode", C4, R1),
      n("cp-6", "JT Reviews & Sends", "inputNode", C4, R2),
      n("cp-7", "M2/M3 Follow-ups", "processNode", C5, R1),
      n("cp-8", "Reply", "alertNode", C5, R2),
      n("cp-9", "Client", "outputNode", C5 + 160, R1),
    ],
    edges: [
      e("cp-1", "cp-2"),
      e("cp-2", "cp-3"),
      e("cp-2", "cp-4"),
      e("cp-3", "cp-5"),
      e("cp-4", "cp-5"),
      e("cp-5", "cp-6"),
      e("cp-6", "cp-7"),
      e("cp-7", "cp-8"),
      e("cp-8", "cp-9"),
    ],
  },

  /* ── 2. Content Machine ── */
  {
    name: "Content Machine",
    subtitle: "LinkedIn + X content generation, banking, daily reminders, and posting",
    width: 900,
    height: 300,
    nodes: [
      n("cm-1a", "technical-angles.md", "inputNode", C1, R1),
      n("cm-1b", "consulting-obs.md", "inputNode", C1, R2),
      n("cm-1c", "recent-builds.md", "inputNode", C1, R3),
      n("cm-2a", "Generate LinkedIn", "cronNode", C2, R1, "Mon 7AM"),
      n("cm-2b", "Generate X", "cronNode", C2, R2, "Mon 7:25AM"),
      n("cm-3", "Bank Posts", "processNode", C3, R1),
      n("cm-4", "Reminder Cron", "cronNode", C4, R1, "Tue-Sat 8AM"),
      n("cm-5", "JT Posts", "inputNode", C5, R1),
      n("cm-6", "posted-log.jsonl", "outputNode", C5 + 160, R1),
    ],
    edges: [
      e("cm-1a", "cm-2a"),
      e("cm-1b", "cm-2a"),
      e("cm-1b", "cm-2b"),
      e("cm-1c", "cm-2b"),
      e("cm-2a", "cm-3"),
      e("cm-2b", "cm-3"),
      e("cm-3", "cm-4"),
      e("cm-4", "cm-5"),
      e("cm-5", "cm-6"),
    ],
  },

  /* ── 3. Job Market ── */
  {
    name: "Job Market",
    subtitle: "Daily job research, morning briefs, application tracking, stale-app monitoring",
    width: 900,
    height: 220,
    nodes: [
      n("jm-1", "Daily Research", "cronNode", C1, R1, "5:15AM"),
      n("jm-2", "daily-brief.md", "processNode", C2, R1),
      n("jm-3", "Morning Brief", "alertNode", C3, R1, "18+/25 roles"),
      n("jm-4", "JT Applies", "inputNode", C4, R1),
      n("jm-5", "Job Tracker", "cronNode", C4, R2, "Tue/Thu"),
      n("jm-6", "Stale App Alerts", "alertNode", C5, R2),
    ],
    edges: [
      e("jm-1", "jm-2"),
      e("jm-2", "jm-3"),
      e("jm-3", "jm-4"),
      e("jm-4", "jm-5"),
      e("jm-5", "jm-6", "monitors"),
    ],
  },

  /* ── 4. Crypto Intelligence ── */
  {
    name: "Crypto Intelligence",
    subtitle: "Game-theoretic analysis, pulse checks, material-move alerts",
    width: 900,
    height: 220,
    nodes: [
      n("ci-1", "Full Analysis", "cronNode", C1, R1, "6AM"),
      n("ci-2", "Midday Pulse", "cronNode", C1, R2, "12PM"),
      n("ci-3", "Evening Pulse", "cronNode", C2, R2, "8:30PM"),
      n("ci-4", "Alert Filter", "processNode", C3, R1, "material only"),
      n("ci-5", "Alerts", "alertNode", C4, R1),
      n("ci-6", "latest-analysis.md", "outputNode", C4, R2),
    ],
    edges: [
      e("ci-1", "ci-4"),
      e("ci-2", "ci-4"),
      e("ci-3", "ci-4"),
      e("ci-4", "ci-5"),
      e("ci-4", "ci-6"),
    ],
  },

  /* ── 5. Passive Income / Vibe Marketing ── */
  {
    name: "Passive Income / Vibe Marketing",
    subtitle: "Trend scouting, idea scoring, vibe marketing content, and publishing",
    width: 950,
    height: 220,
    nodes: [
      n("pi-1", "Scout", "cronNode", C1, R1, "Sun 6:30AM"),
      n("pi-2", "5 Ideas", "processNode", C2, R1, "trend research"),
      n("pi-3", "Strategist", "cronNode", C3, R1, "Sun 8:30AM"),
      n("pi-4", "8-Dim Scoring", "processNode", C3, R2),
      n("pi-5", "Vibe Marketing", "cronNode", C4, R1, "Mon 4:45AM"),
      n("pi-6", "JT Approves", "inputNode", C5, R1),
      n("pi-7", "PostBridge", "outputNode", C5 + 160, R1, "schedules"),
    ],
    edges: [
      e("pi-1", "pi-2"),
      e("pi-2", "pi-3"),
      e("pi-3", "pi-4"),
      e("pi-4", "pi-5", "winners"),
      e("pi-5", "pi-6"),
      e("pi-6", "pi-7", "approved only"),
    ],
  },

  /* ── 6. Overnight Autonomy ── */
  {
    name: "Overnight Autonomy",
    subtitle: "3AM agent reads MC board, executes high-priority tasks, logs proofs",
    width: 900,
    height: 220,
    nodes: [
      n("oa-1", "3AM Trigger", "cronNode", C1, R1, "daily"),
      n("oa-2", "Read MC HIGH Tasks", "processNode", C2, R1),
      n("oa-3", "Select up to 2", "processNode", C3, R1),
      n("oa-4", "Execute", "processNode", C4, R1, "sub-agents OK"),
      n("oa-5", "Write Log", "outputNode", C4, R2),
      n("oa-6", "Morning Brief", "alertNode", C5, R1, "$1.50 cap"),
    ],
    edges: [
      e("oa-1", "oa-2"),
      e("oa-2", "oa-3"),
      e("oa-3", "oa-4"),
      e("oa-4", "oa-5"),
      e("oa-4", "oa-6"),
    ],
  },

  /* ── 7. Spanish Learning ── */
  {
    name: "Spanish Learning",
    subtitle: "Daily TTS lessons, weekly evaluations, progress tracking",
    width: 900,
    height: 220,
    nodes: [
      n("sl-1", "Daily Lesson", "cronNode", C1, R1, "Mon-Sat 8:05PM"),
      n("sl-2", "TTS Phrases", "processNode", C2, R1),
      n("sl-3", "JT Practices", "inputNode", C3, R1),
      n("sl-4", "Weekly Eval", "cronNode", C3, R2, "Sun 8PM"),
      n("sl-5", "3-Part Spoken Test", "processNode", C4, R2),
      n("sl-6", "Score", "alertNode", C5, R1),
      n("sl-7", "state.json", "outputNode", C5, R2),
    ],
    edges: [
      e("sl-1", "sl-2"),
      e("sl-2", "sl-3"),
      e("sl-3", "sl-4"),
      e("sl-4", "sl-5"),
      e("sl-5", "sl-6"),
      e("sl-5", "sl-7"),
    ],
  },

  /* ── 8. Health Tracking ── */
  {
    name: "Health Tracking",
    subtitle: "Nightly check-in, SQLite storage, weekly reports with pattern analysis",
    width: 900,
    height: 220,
    nodes: [
      n("ht-1", "Evening Check-in", "cronNode", C1, R1, "9PM"),
      n("ht-2", "5 Questions", "processNode", C2, R1),
      n("ht-3", "JT Answers", "inputNode", C3, R1),
      n("ht-4", "health.sqlite", "processNode", C4, R1),
      n("ht-5", "Weekly Report", "cronNode", C4, R2, "Sun 9:20AM"),
      n("ht-6", "Protocol Reminder", "alertNode", C5, R1, "included nightly"),
    ],
    edges: [
      e("ht-1", "ht-2"),
      e("ht-2", "ht-3"),
      e("ht-3", "ht-4"),
      e("ht-4", "ht-5"),
      e("ht-5", "ht-6"),
    ],
  },
];
