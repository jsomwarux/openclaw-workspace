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
  const regex = new RegExp(`\\*\\*${field}:\\*\\*\\s*(.+?)(?=\\n\\*\\*|\\n---|\\n###|$)`, "s");
  const match = regex.exec(section);
  return match ? match[1].trim() : "";
}

function parseScoutReport(content: string, fileName: string): ParsedIdea[] {
  const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})/);
  const reportDate = dateMatch ? dateMatch[1] : "";
  const ideas: ParsedIdea[] = [];

  // Scout titles: "### 1. FITBRIEF AI" or "### 1. FITBRIEF AI — Score: 8.1/10"
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

    // Parse score from title if embedded (e.g. "FITBRIEF AI — Score: 8.1/10")
    // Skip unscored scout entries — strategist re-analyzes everything with better context
    const titleMatch = positions[i].title.match(/^(.+?)\s*[—–-]\s*Score:\s*(\d+\.?\d*)\/10/);
    const cleanTitle = titleMatch ? titleMatch[1].trim() : positions[i].title;
    const score = titleMatch ? parseFloat(titleMatch[2]) : 0;
    if (score === 0) continue; // skip unscored scout ideas

    ideas.push({
      title: cleanTitle,
      score,
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

  const skipSections = [
    "Already Queued", "Saturation Filter", "Deep Analysis",
    "Portfolio Commentary", "Verdict Summary", "Research Summary",
    "Full Scoring Summary", "SATURATION FILTER RESULTS", "WATCH IDEAS",
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

    // Extract score — try multiple formats:
    // 1. **Score: 5.8/10** (fully bold-wrapped, March 8 e.g. SITEAUDIT)
    // 2. Score: **7.5/10** (Score: plain, number bold — March 8/15)
    // 3. **Weighted total: 8.6/10** (markdown tables, March 22+)
    // 4. Score: 7.6/10 (plain, March 29+)
    let score = 0;
    const fullyBoldMatch = section.match(/\*\*Score:\s*(\d+\.?\d*)\/10\*\*/);
    if (fullyBoldMatch) {
      score = parseFloat(fullyBoldMatch[1]);
    } else {
      const scoreBoldMatch = section.match(/Score:\s*\*\*(\d+\.?\d*)\/10/);
      if (scoreBoldMatch) {
        score = parseFloat(scoreBoldMatch[1]);
      } else {
        const weightedMatch = section.match(/\*\*Weighted total:\s*(\d+\.?\d*)\/10/);
        if (weightedMatch) {
          score = parseFloat(weightedMatch[1]);
        } else {
          const plainMatch = section.match(/Score:\s*(\d+\.?\d*)\/10(?!\*)/);
          if (plainMatch) {
            score = parseFloat(plainMatch[1]);
          }
        }
      }
    }

    // Extract verdict for status hint
    let status: ParsedIdea["status"] = "exploring";
    if (/BUILD/.test(section)) status = "building";

    // Normalize title — remove verdict emoji + verdict word + embedded scores + TOP PICK markers
    // e.g. "PADELRANK ⭐ TOP PICK" → "PADELRANK"
    // e.g. "🔴 PASS — SITEAUDIT.AI" → "SITEAUDIT.AI"
    // e.g. "🟡 WATCH — QUOTE PILOT" → "QUOTE PILOT"
    // e.g. "FITBRIEF AI — Score: 8.1/10" → "FITBRIEF AI"
    const rawTitle = positions[i].title;
    const cleanTitle = rawTitle
      .replace(/^\s*[🟢🟡🔴]\s*(?:PASS|BUILD|WATCH|IDEAS?\s*\d*)\s*[—–-]?\s*/i, "")
      .replace(/^\s*[🟢🟡🔴]\s*/, "")
      .replace(/\s*[-—]\s*Score:\s*\d+\.?\d*\/10.*$/i, "")
      .replace(/\s*[-—]\s*\d+\.?\d*\/10.*$/i, "")
      .replace(/\s*⭐\s*TOP PICK.*$/i, "")
      .replace(/\s+TOP PICK.*$/i, "")
      .replace(/\s+←\s+Top Pick.*$/i, "")
      .replace(/\s*⚠️.*$/, "")
      .trim();

    ideas.push({
      title: cleanTitle,
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
  const match = regex.exec(section);
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

  // Parse strategist reports first (they have scores, most authoritative)
  const strategistFiles = files.filter((f) => f.includes("strategist")).sort().reverse();
  const scoutFiles = files.filter((f) => f.includes("scout")).sort().reverse();

  for (const file of strategistFiles) {
    const content = readFileSync(join(dir, file), "utf-8");
    const ideas = parseStrategistReport(content, file);
    for (const idea of ideas) {
      // Dedupe: normalize for comparison (strip emoji/decorations, uppercase + alphanumeric only)
      const normalized = idea.title.toUpperCase().replace(/[^A-Z0-9]/g, "");
      if (!seenTitles.has(normalized)) {
        seenTitles.add(normalized);
        allIdeas.push(idea);
      }
    }
  }

  for (const file of scoutFiles) {
    const content = readFileSync(join(dir, file), "utf-8");
    const ideas = parseScoutReport(content, file);
    for (const idea of ideas) {
      const normalized = idea.title.toUpperCase().replace(/[^A-Z0-9]/g, "");
      if (!seenTitles.has(normalized)) {
        seenTitles.add(normalized);
        allIdeas.push(idea);
      }
    }
  }

  return NextResponse.json({ ideas: allIdeas });
}