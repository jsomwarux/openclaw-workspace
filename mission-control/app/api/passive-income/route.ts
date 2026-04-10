import { NextResponse } from "next/server";
import { readdirSync, readFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

interface ParsedIdea {
  title: string;
  score: number;
  status: "exploring" | "building" | "launched" | "shelved";
  source: string;
  reportDate: string;
  concept: string;
  revenueModel: string;
  jtStackFit: string;
  longevitySignal: string;
  researchSignal: string;
  creativityCheck: string;
}

function extractField(section: string, field: string): string {
  const regex = new RegExp(`\\*\\*${field}:\\*\\*\\s*(.+?)(?=\\n\\*\\*|\\n---|\n###|$)`, "s");
  const match = section.match(regex);
  return match ? match[1].trim() : "";
}

function parseScoutReport(content: string, fileName: string): ParsedIdea[] {
  const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})/);
  const reportDate = dateMatch ? dateMatch[1] : "";
  const ideas: ParsedIdea[] = [];

  // Scout ideas are under ### N. IDEANAME
  const ideaRegex = /### \d+\.\s+(.+?)(?=\n)/g;
  let match;
  const positions: { title: string; index: number }[] = [];

  while ((match = ideaRegex.exec(content)) !== null) {
    positions.push({ title: match[1].trim(), index: match.index });
  }

  for (let i = 0; i < positions.length; i++) {
    const start = positions[i].index;
    const end = i + 1 < positions.length ? positions[i + 1].index : content.length;
    const section = content.slice(start, end);

    ideas.push({
      title: positions[i].title,
      score: 0,
      status: "exploring",
      source: `scout (${reportDate})`,
      reportDate,
      concept: extractField(section, "Concept"),
      revenueModel: extractField(section, "Revenue model"),
      jtStackFit: extractField(section, "JT stack fit"),
      longevitySignal: extractField(section, "Longevity signal"),
      researchSignal: extractField(section, "Research signal"),
      creativityCheck: extractField(section, "Creativity check"),
    });
  }

  return ideas;
}

function parseStrategistReport(content: string, fileName: string): ParsedIdea[] {
  const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})/);
  const reportDate = dateMatch ? dateMatch[1] : "";
  const ideas: ParsedIdea[] = [];

  // Strategist ideas are under ## IDEANAME (skip meta sections)
  const skipSections = [
    "Already Queued",
    "Saturation Filter",
    "Deep Analysis",
    "Portfolio Commentary",
    "Verdict Summary",
    "Research Summary",
  ];

  const sectionRegex = /^## (.+)$/gm;
  let match;
  const positions: { title: string; index: number }[] = [];

  while ((match = sectionRegex.exec(content)) !== null) {
    const title = match[1].trim();
    if (skipSections.some((s) => title.includes(s))) continue;
    positions.push({ title, index: match.index });
  }

  for (let i = 0; i < positions.length; i++) {
    const start = positions[i].index;
    const end = i + 1 < positions.length ? positions[i + 1].index : content.length;
    const section = content.slice(start, end);

    // Extract score from verdict line
    const scoreMatch = section.match(/Score:\s*(\d+\.?\d*)\/10/);
    const score = scoreMatch ? parseFloat(scoreMatch[1]) : 0;

    // Extract verdict for status hint
    let status: ParsedIdea["status"] = "exploring";
    if (/BUILD/.test(section)) status = "building";

    ideas.push({
      title: positions[i].title,
      score,
      status,
      source: `strategist (${reportDate})`,
      reportDate,
      concept: extractField(section, "Concept") || extractOpportunity(section),
      revenueModel: extractField(section, "Revenue model") || extractNumberedSection(section, "5. Monetization") || extractNumberedSection(section, "Monetization"),
      jtStackFit: extractField(section, "JT stack fit") || extractNumberedSection(section, "4. Build Reality Check") || "",
      longevitySignal: extractField(section, "Longevity signal") || "",
      researchSignal: extractField(section, "Research signal") || "",
      creativityCheck: extractField(section, "Creativity check") || extractNumberedSection(section, "6. What") || "",
    });
  }

  return ideas;
}

function extractOpportunity(section: string): string {
  const match = section.match(/### 1\. The Opportunity\n([\s\S]+?)(?=\n###)/);
  return match ? match[1].trim() : "";
}

function extractNumberedSection(section: string, heading: string): string {
  const regex = new RegExp(`### ${heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[\\s\\S]*?\\n([\\s\\S]+?)(?=\\n###|$)`);
  const match = section.match(regex);
  return match ? match[1].trim() : "";
}

export async function GET() {
  const dir = join(homedir(), ".openclaw/workspace/memory/passive-income");

  if (!existsSync(dir)) {
    return NextResponse.json({ ideas: [], error: "Directory not found" });
  }

  const files = readdirSync(dir).filter((f) => f.endsWith(".md"));
  const allIdeas: ParsedIdea[] = [];
  const seenTitles = new Set<string>();

  // Parse strategist reports first (they have scores)
  const strategistFiles = files.filter((f) => f.includes("strategist")).sort().reverse();
  const scoutFiles = files.filter((f) => f.includes("scout")).sort().reverse();

  for (const file of strategistFiles) {
    const content = readFileSync(join(dir, file), "utf-8");
    const ideas = parseStrategistReport(content, file);
    for (const idea of ideas) {
      if (!seenTitles.has(idea.title)) {
        seenTitles.add(idea.title);
        allIdeas.push(idea);
      }
    }
  }

  for (const file of scoutFiles) {
    const content = readFileSync(join(dir, file), "utf-8");
    const ideas = parseScoutReport(content, file);
    for (const idea of ideas) {
      if (!seenTitles.has(idea.title)) {
        seenTitles.add(idea.title);
        allIdeas.push(idea);
      }
    }
  }

  return NextResponse.json({ ideas: allIdeas });
}
