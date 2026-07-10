import { existsSync, readdirSync, readFileSync } from "fs";
import { join } from "path";

export type PassiveIncomeStatus = "exploring" | "building" | "launched" | "shelved";

export type ScoreDimension = {
  label: string;
  value: number;
};

export interface PassiveIncomeIdea {
  title: string;
  score: number;
  status: PassiveIncomeStatus;
  source: string;
  sourceFile: string;
  reportDate: string;
  concept: string;
  revenueModel: string;
  jtStackFit: string;
  longevitySignal: string;
  researchSignal: string;
  creativityCheck: string;
  scoreRationale: string;
  scoreBreakdown: ScoreDimension[];
  detailCompleteness: number;
  decision: "build" | "watch" | "pass" | "queued" | "explore";
}

const NON_IDEA_SECTION_PATTERNS = [
  /summary/i,
  /deduplication/i,
  /saturation/i,
  /scorecard/i,
  /deep analysis/i,
  /blueprints?/i,
  /recommendation/i,
  /commentary/i,
  /verdict summary/i,
  /queued/i,
  /push to mission control/i,
  /report saved/i,
  /sunday digest/i,
  /prior recommendations/i,
  /^step\s+\d+:/i,
];

const NORTH_STAR_SCORE_OVERRIDES: Record<string, number> = {
  PADELRANK: 8.2,
  ROUTESAFE: 8.0,
  PETBOWLPROOF: 7.9,
  PICKLERANK: 7.8,
  ProfessionBox: 7.6,
  ROASTERRANK: 7.4,
  NootropIQ: 7.4,
  "SUPPLEMENT SCORE": 7.2,
  GYMLORE: 7.1,
  GLAMBOXMATCH: 7.1,
  "ProductionBible AI": 7.0,
  "FITBRIEF AI": 7.0,
  DISCRANK: 7.0,
  VINYLIQ: 6.9,
  "CRYPTO TAX NOMAD": 6.8,
  "CULTUREFIT NUTRITION": 6.7,
  TRADIECOMMS: 6.6,
  IMMIGRANTIQ: 6.5,
  ANCESTRYCANVAS: 6.4,
  TARIFFSWITCH: 6.4,
  VisaPathAI: 6.3,
  FANDOMDROP: 6.2,
  "QUOTE PILOT": 5.8,
  "CAP TABLE SPLIT": 5.4,
  "RECIPE RANKINGS": 5.2,
  HOAFlow: 5.1,
  "SITEAUDIT.AI": 4.8,
  LeagueBot: 4.2,
};

function normalizeTitle(title: string): string {
  return title
    .replace(/[\uD800-\uDFFF]/g, "")
    .replace(/^\s*[^A-Za-z0-9]*(?:PASS|BUILD|WATCH|IDEAS?\s*\d*)?\s*[—–:-]?\s*/i, "")
    .replace(/^\s*(?:IDEAS?\s*\d+|WATCH)\s*[—–:-]\s*/i, "")
    .replace(/\s*[—–-]\s*Score:\s*\d+\.?\d*\/10.*$/i, "")
    .replace(/\s*[—–-]\s*\d+\.?\d*\/10.*$/i, "")
    .replace(/\s*\([^)]*\d+\.?\d*\/10[^)]*\).*$/i, "")
    .replace(/\s*⭐\s*TOP PICK.*$/i, "")
    .replace(/\s+TOP PICK.*$/i, "")
    .replace(/\s+←\s+Top Pick.*$/i, "")
    .replace(/\s*⚠️.*$/, "")
    .trim();
}

function normalizedKey(title: string): string {
  return title.toUpperCase().replace(/[^A-Z0-9]/g, "");
}

function isNonIdeaTitle(title: string): boolean {
  return NON_IDEA_SECTION_PATTERNS.some((pattern) => pattern.test(title));
}

function reportDateFromFile(fileName: string): string {
  return fileName.match(/(\d{4}-\d{2}-\d{2})/)?.[1] ?? "";
}

function extractField(section: string, field: string): string {
  const regex = new RegExp(`\\*\\*${field}:\\*\\*\\s*(.+?)(?=\\n\\*\\*|\\n---|\\n###|$)`, "s");
  return regex.exec(section)?.[1]?.trim() ?? "";
}

function extractHeadingSection(section: string, heading: string): string {
  const regex = new RegExp(`### ${heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\n([\\s\\S]+?)(?=\\n###|\\n##|$)`);
  return regex.exec(section)?.[1]?.trim() ?? "";
}

function extractNumberedSection(section: string, heading: string): string {
  const regex = new RegExp(`### ${heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[\\s\\S]*?\\n([\\s\\S]+?)(?=\\n###|$)`);
  return regex.exec(section)?.[1]?.trim() ?? "";
}

function compactText(value: string, max = 520): string {
  return value.replace(/\s+/g, " ").trim().slice(0, max);
}

function parseScore(section: string, rawTitle: string): number {
  const patterns = [
    /\*\*Score:\s*(\d+\.?\d*)\/10\*\*/,
    /Score:\s*\*\*(\d+\.?\d*)\/10/,
    /\*\*Weighted (?:total|overall):\s*(\d+\.?\d*)\/10/,
    /Score:\s*(?:\*\*)?(\d+\.?\d*)\/10/,
  ];

  for (const pattern of patterns) {
    const match = section.match(pattern);
    if (match) return parseFloat(match[1]);
  }

  const headingScoreMatch = rawTitle.match(/\((\d+\.?\d*)\/10\)/);
  return headingScoreMatch ? parseFloat(headingScoreMatch[1]) : 0;
}

function parseDecision(section: string): PassiveIncomeIdea["decision"] {
  if (/ALREADY QUEUED|🔁/i.test(section)) return "queued";
  if (/PASS THIS|PASS\b|🔴/i.test(section)) return "pass";
  if (/WATCH|🟡/i.test(section)) return "watch";
  if (/BUILD THIS|BUILD\b|🟢/i.test(section)) return "build";
  return "explore";
}

function statusFromDecision(decision: PassiveIncomeIdea["decision"]): PassiveIncomeStatus {
  if (decision === "build") return "building";
  if (decision === "pass") return "shelved";
  return "exploring";
}

function parseScoreBreakdown(section: string): ScoreDimension[] {
  const lines = section.split("\n");
  for (let i = 0; i < lines.length - 2; i += 1) {
    if (!lines[i].includes("|") || !lines[i + 2].includes("|")) continue;
    const labels = lines[i].split("|").map((cell) => cell.trim()).filter(Boolean);
    const values = lines[i + 2].split("|").map((cell) => cell.trim()).filter(Boolean);
    if (labels.length < 3 || labels.length !== values.length) continue;
    const parsed = labels.map((label, index) => ({ label, value: Number(values[index]) })).filter((item) => Number.isFinite(item.value));
    if (parsed.length >= 3) return parsed;
  }
  return [];
}

function dimensionSummary(scoreBreakdown: ScoreDimension[]): { strengths: string[]; watchouts: string[] } {
  const strengths = scoreBreakdown.filter((item) => item.value >= 8).map((item) => item.label.toLowerCase());
  const watchouts = scoreBreakdown.filter((item) => item.value <= 6).map((item) => item.label.toLowerCase());
  return { strengths, watchouts };
}

function scoreRationale(score: number, decision: PassiveIncomeIdea["decision"], scoreBreakdown: ScoreDimension[], section: string): string {
  const blocker = extractHeadingSection(section, "Blocker");
  if (blocker) return compactText(blocker, 320);

  const { strengths, watchouts } = dimensionSummary(scoreBreakdown);
  const decisionText =
    decision === "build"
      ? "Strong fit"
      : decision === "watch"
        ? "Promising but not first in line"
        : decision === "pass"
          ? "Low-priority"
          : decision === "queued"
            ? "Already represented on the board"
            : score >= 7.5
              ? "Strong candidate"
              : "Needs more proof";

  const strengthText = strengths.length > 0 ? strengths.slice(0, 3).join(", ") : score >= 7.5 ? "overall score" : "some market signal";
  const watchoutText = watchouts.length > 0 ? watchouts.slice(0, 3).join(", ") : "no single low-scoring dimension was captured";

  return `${decisionText}: strongest on ${strengthText}. Watchouts: ${watchoutText}.`;
}

function detailCompleteness(idea: Pick<PassiveIncomeIdea, "concept" | "revenueModel" | "jtStackFit" | "longevitySignal" | "researchSignal" | "creativityCheck" | "scoreRationale">): number {
  return [
    idea.concept,
    idea.revenueModel,
    idea.jtStackFit,
    idea.longevitySignal,
    idea.researchSignal,
    idea.creativityCheck,
    idea.scoreRationale,
  ].filter((value) => value.trim().length > 0).length;
}

function withScoreOverride(idea: PassiveIncomeIdea): PassiveIncomeIdea {
  const score = NORTH_STAR_SCORE_OVERRIDES[idea.title];
  return score === undefined ? idea : { ...idea, score };
}

function extractBlueprints(content: string): Map<string, Partial<PassiveIncomeIdea>> {
  const blueprints = new Map<string, Partial<PassiveIncomeIdea>>();
  const sectionRegex = /^#\s+.*Blueprint:\s+(.+)$/gm;
  const positions: { title: string; index: number }[] = [];
  let match;

  while ((match = sectionRegex.exec(content)) !== null) {
    positions.push({ title: normalizeTitle(match[1].trim()), index: match.index });
  }

  for (let i = 0; i < positions.length; i += 1) {
    const start = positions[i].index;
    const end = i + 1 < positions.length ? positions[i + 1].index : content.length;
    const section = content.slice(start, end);
    const title = positions[i].title;
    if (!title) continue;

    blueprints.set(normalizedKey(title), {
      concept: extractNumberedSection(section, "1. The Opportunity"),
      jtStackFit: new RegExp("- \\*\\*Full tech stack\\*\\*:\\s*([\\s\\S]+?)(?=\\n- \\*\\*|\\n###|$)").exec(section)?.[1]?.trim() || "",
      revenueModel: extractNumberedSection(section, "4. Monetization"),
      researchSignal:
        extractNumberedSection(section, "5. Marketing Strategy (Autonomous — runs without JT)") ||
        extractNumberedSection(section, "5. Marketing Strategy"),
      longevitySignal: extractNumberedSection(section, "6. Automation Stack"),
    });
  }

  return blueprints;
}

function mergeBlueprint(idea: PassiveIncomeIdea, blueprints: Map<string, Partial<PassiveIncomeIdea>>): PassiveIncomeIdea {
  const blueprint = blueprints.get(normalizedKey(idea.title));
  if (!blueprint) return idea;
  return {
    ...idea,
    concept: idea.concept || blueprint.concept || "",
    revenueModel: idea.revenueModel || blueprint.revenueModel || "",
    jtStackFit: idea.jtStackFit || blueprint.jtStackFit || "",
    longevitySignal: idea.longevitySignal || blueprint.longevitySignal || "",
    researchSignal: idea.researchSignal || blueprint.researchSignal || "",
    creativityCheck: idea.creativityCheck || blueprint.creativityCheck || "",
  };
}

function buildIdea(section: string, rawTitle: string, fileName: string, sourceKind: "strategist" | "scout", blueprints = new Map<string, Partial<PassiveIncomeIdea>>()): PassiveIncomeIdea | null {
  const reportDate = reportDateFromFile(fileName);
  const score = parseScore(section, rawTitle);
  if (score === 0) return null;

  const title = normalizeTitle(rawTitle);
  if (!title || isNonIdeaTitle(title)) return null;

  const decision = parseDecision(section);
  const scoreBreakdown = parseScoreBreakdown(section);
  const concept =
    extractField(section, "Concept") ||
    extractHeadingSection(section, "Value Proposition Test") ||
    extractHeadingSection(section, "1. The Opportunity") ||
    extractNumberedSection(section, "1. The Opportunity");
  const revenueModel =
    extractField(section, "Revenue model") ||
    extractHeadingSection(section, "Market Demand Validation") ||
    extractNumberedSection(section, "5. Monetization") ||
    extractNumberedSection(section, "Monetization");
  const jtStackFit =
    extractField(section, "JT stack fit") ||
    extractHeadingSection(section, "Build Reality") ||
    extractNumberedSection(section, "4. Build Reality Check");
  const longevitySignal = extractField(section, "Longevity signal") || extractHeadingSection(section, "Longevity");
  const researchSignal =
    extractField(section, "Research signal") ||
    extractHeadingSection(section, "Competition Landscape") ||
    extractHeadingSection(section, "Autonomous Marketing");
  const creativityCheck =
    extractField(section, "Creativity check") ||
    extractHeadingSection(section, "Vision Fit") ||
    extractHeadingSection(section, "Autonomous Marketing");

  let idea = mergeBlueprint({
    title,
    score,
    status: statusFromDecision(decision),
    source: `${sourceKind} (${reportDate})`,
    sourceFile: `memory/passive-income/${fileName}`,
    reportDate,
    concept: compactText(concept),
    revenueModel: compactText(revenueModel),
    jtStackFit: compactText(jtStackFit),
    longevitySignal: compactText(longevitySignal),
    researchSignal: compactText(researchSignal),
    creativityCheck: compactText(creativityCheck),
    scoreRationale: scoreRationale(score, decision, scoreBreakdown, section),
    scoreBreakdown,
    detailCompleteness: 0,
    decision,
  }, blueprints);

  idea = withScoreOverride(idea);
  return { ...idea, detailCompleteness: detailCompleteness(idea) };
}

function parseScoutReport(content: string, fileName: string): PassiveIncomeIdea[] {
  const ideaRegex = /### \d+\.\s+(.+?)(?=\n)/g;
  const positions: { title: string; index: number }[] = [];
  let match;

  while ((match = ideaRegex.exec(content)) !== null) {
    positions.push({ title: match[1].trim(), index: match.index });
  }

  return positions
    .map((position, index) => {
      const end = index + 1 < positions.length ? positions[index + 1].index : content.length;
      return buildIdea(content.slice(position.index, end), position.title, fileName, "scout");
    })
    .filter((idea): idea is PassiveIncomeIdea => Boolean(idea));
}

function parseStrategistReport(content: string, fileName: string): PassiveIncomeIdea[] {
  const skipSections = [
    "Already Queued",
    "Saturation Filter",
    "Deep Analysis",
    "Portfolio Commentary",
    "Verdict Summary",
    "Research Summary",
    "Full Scoring Summary",
    "SATURATION FILTER RESULTS",
    "WATCH IDEAS",
  ];
  const blueprints = extractBlueprints(content);
  const sectionRegex = /^#{1,2} (.+)$/gm;
  const positions: { title: string; index: number }[] = [];
  let match;

  while ((match = sectionRegex.exec(content)) !== null) {
    const title = match[1].trim();
    if (skipSections.some((skip) => title.includes(skip))) continue;
    if (/Blueprint:/i.test(title)) continue;
    positions.push({ title, index: match.index });
  }

  return positions
    .map((position, index) => {
      const end = index + 1 < positions.length ? positions[index + 1].index : content.length;
      const section = content.slice(position.index, end);
      if (isNonIdeaTitle(position.title) || /ALREADY QUEUED/i.test(section)) return null;
      return buildIdea(section, position.title, fileName, "strategist", blueprints);
    })
    .filter((idea): idea is PassiveIncomeIdea => Boolean(idea));
}

export function parsePassiveIncomeReport(content: string, fileName: string): PassiveIncomeIdea[] {
  return fileName.includes("strategist") ? parseStrategistReport(content, fileName) : parseScoutReport(content, fileName);
}

export function loadPassiveIncomeIdeas(dir: string): PassiveIncomeIdea[] {
  if (!existsSync(dir)) return [];

  const files = readdirSync(dir).filter((file) => file.endsWith(".md"));
  const allIdeas: PassiveIncomeIdea[] = [];
  const seenTitles = new Set<string>();
  const orderedFiles = [
    ...files.filter((file) => file.includes("strategist")).sort().reverse(),
    ...files.filter((file) => file.includes("scout")).sort().reverse(),
  ];

  for (const file of orderedFiles) {
    const content = readFileSync(join(dir, file), "utf-8");
    for (const idea of parsePassiveIncomeReport(content, file)) {
      const key = normalizedKey(idea.title);
      if (seenTitles.has(key)) continue;
      seenTitles.add(key);
      allIdeas.push(idea);
    }
  }

  return allIdeas.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return b.reportDate.localeCompare(a.reportDate) || a.title.localeCompare(b.title);
  });
}
