// The supported description formatting (DECISIONS 4.8): paragraphs, "## " headings, "- "
// bullets, ordered sub-lists and **Label:** bold labels. Everything else stays literal text.

export interface OrderedItem { n: string; text: string }
export interface BulletItem { label: string | null; text: string; children: OrderedItem[] }

export type DescriptionBlock =
  | { kind: "heading"; text: string }
  | { kind: "paragraph"; lines: string[] }
  | { kind: "bullets"; items: BulletItem[] }
  | { kind: "ordered"; items: OrderedItem[] }
  | { kind: "answerSlot" };

const BULLET = /^- (.*)$/;
const ORDERED = /^(\s*)(\d+)\.\s+(.*)$/;
const LABELLED = /^\*\*([^*]+?:)\*\*(.*)$/;
const EMPTY_ANSWER = /^- \*\*Answer:\*\*\s*$/;

/** answerSlot: replace the empty "- **Answer:**" bullet with the answer box (Q and AP cards). */
export function parseDescription(text: string, options: { answerSlot: boolean }): DescriptionBlock[] {
  const blocks: DescriptionBlock[] = [];
  const last = () => blocks[blocks.length - 1];
  let open: "paragraph" | "bullets" | "ordered" | null = null;

  for (const raw of text.split("\n")) {
    const line = raw.endsWith("\r") ? raw.slice(0, -1) : raw;
    if (line.trim() === "") {
      open = null;
      continue;
    }
    if (line.startsWith("## ")) {
      blocks.push({ kind: "heading", text: line.slice(3) });
      open = null;
      continue;
    }
    if (options.answerSlot && EMPTY_ANSWER.test(line)) {
      blocks.push({ kind: "answerSlot" });
      open = null;
      continue;
    }
    const bullet = BULLET.exec(line);
    if (bullet) {
      const labelled = LABELLED.exec(bullet[1]);
      const item: BulletItem = labelled
        ? { label: labelled[1], text: labelled[2], children: [] }
        : { label: null, text: bullet[1], children: [] };
      if (open === "bullets") (last() as Extract<DescriptionBlock, { kind: "bullets" }>).items.push(item);
      else blocks.push({ kind: "bullets", items: [item] });
      open = "bullets";
      continue;
    }
    const ordered = ORDERED.exec(line);
    if (ordered) {
      const item = { n: ordered[2], text: ordered[3] };
      if (ordered[1].length > 0 && open === "bullets") {
        const items = (last() as Extract<DescriptionBlock, { kind: "bullets" }>).items;
        items[items.length - 1].children.push(item);
      } else if (open === "ordered") {
        (last() as Extract<DescriptionBlock, { kind: "ordered" }>).items.push(item);
      } else {
        blocks.push({ kind: "ordered", items: [item] });
        open = "ordered";
      }
      continue;
    }
    if (open === "paragraph") (last() as Extract<DescriptionBlock, { kind: "paragraph" }>).lines.push(line);
    else blocks.push({ kind: "paragraph", lines: [line] });
    open = "paragraph";
  }
  return blocks;
}

/** Splits a line into plain and bold segments; only **Label:** pairs become bold. */
export function inlineSegments(text: string): { text: string; bold: boolean }[] {
  const segments: { text: string; bold: boolean }[] = [];
  const pattern = /\*\*([^*]+?:)\*\*/g;
  let cursor = 0;
  for (const match of text.matchAll(pattern)) {
    const index = match.index ?? 0;
    if (index > cursor) segments.push({ text: text.slice(cursor, index), bold: false });
    segments.push({ text: match[1], bold: true });
    cursor = index + match[0].length;
  }
  if (cursor < text.length) segments.push({ text: text.slice(cursor), bold: false });
  return segments;
}
