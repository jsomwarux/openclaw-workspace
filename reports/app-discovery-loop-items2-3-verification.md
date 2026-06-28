# App Discovery Loop Phase 2 Items 2-3 Verification

Scope: items 2 and 3 batched, plus JT-approved Stage 3 and Stage 4 fixes in `skills/app-discovery-loop/SKILL.md`.

Did not touch: `skills/product-build-loop/SKILL.md`, crons, schedules, runtime config, or passive-income doc rewiring.

## Files Changed / Added
- Updated: `skills/app-discovery-loop/SKILL.md`
- Added: `scripts/app_discovery_evidence_guard.py`
- Added: `scripts/test_app_discovery_evidence_guard.py`
- Added: `memory/app-discovery/fixtures/failing_missing_snippet.md`
- Added: `memory/app-discovery/fixtures/passing_sourced_or_unverified.md`
- Added: `memory/app-discovery/samples/sample_niche_os.md`
- Added templates under `memory/app-discovery/templates/`

## Self-Audit
- Item 2 evidence guard: PASS. Unit tests pass; failing fixture returns `ok=false` with missing `source_snippet`; passing fixture returns `ok=true`.
- Item 3 templates: PASS. File list present; template diffs included; guard run against templates returns `ok=true`.
- Stage 3 fix: PASS. `rg` finds `frontier-class reasoning` in skill and Stage 3 template.
- Stage 4 fix: PASS. `rg` finds distribution feasibility gate, low-competition channel, and `DEPRIORITIZE` in skill/template.
- Item 4: NOT RUN. `skills/product-build-loop/SKILL.md` was not edited and remains gated for separate approval.

## UNVERIFIED Items
- `memory/app-discovery/samples/sample_niche_os.md` intentionally includes one `UNVERIFIED` sample claim: scorecard sharing may create organic distribution. The guard accepts it because it has an explicit `unverified_reason`.
- No blocking UNVERIFIED verification claims in this audit.

## Bootstrap budget check

Command:
```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md SOUL.md IDENTITY.md USER.md
```
Exit code: `0`

Output:
```text
   27516 AGENTS.md
    7306 MEMORY.md
    5168 TOOLS.md
    4189 HEARTBEAT.md
    5267 SOUL.md
    1201 IDENTITY.md
    4704 USER.md
   55351 total
```

## Unit tests

Command:
```bash
python3 scripts/test_app_discovery_evidence_guard.py
```
Exit code: `0`

Output:
```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

## Py compile

Command:
```bash
python3 -m py_compile scripts/app_discovery_evidence_guard.py scripts/test_app_discovery_evidence_guard.py
```
Exit code: `0`

Output:
```text
(no output)
```

## Failing fixture raw output

Command:
```bash
python3 scripts/app_discovery_evidence_guard.py memory/app-discovery/fixtures/failing_missing_snippet.md || true
```
Exit code: `0`

Output:
```text
{
  "claim_tables": 1,
  "claims_checked": 1,
  "files": [
    {
      "claim_tables": 1,
      "claims_checked": 1,
      "path": "memory/app-discovery/fixtures/failing_missing_snippet.md",
      "problems": [
        "memory/app-discovery/fixtures/failing_missing_snippet.md: claim row 1: missing source_snippet"
      ]
    }
  ],
  "files_checked": 1,
  "ok": false,
  "problems": [
    "memory/app-discovery/fixtures/failing_missing_snippet.md: claim row 1: missing source_snippet"
  ]
}
```

## Passing fixture raw output

Command:
```bash
python3 scripts/app_discovery_evidence_guard.py memory/app-discovery/fixtures/passing_sourced_or_unverified.md
```
Exit code: `0`

Output:
```text
{
  "claim_tables": 1,
  "claims_checked": 2,
  "files": [
    {
      "claim_tables": 1,
      "claims_checked": 2,
      "path": "memory/app-discovery/fixtures/passing_sourced_or_unverified.md",
      "problems": []
    }
  ],
  "files_checked": 1,
  "ok": true,
  "problems": []
}
```

## Templates guard raw output

Command:
```bash
python3 scripts/app_discovery_evidence_guard.py memory/app-discovery/templates/*.md
```
Exit code: `0`

Output:
```text
{
  "claim_tables": 1,
  "claims_checked": 0,
  "files": [
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/build_ready_spec.md",
      "problems": []
    },
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/candidate_niches.md",
      "problems": []
    },
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/concept_brief.md",
      "problems": []
    },
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/landscape_audit.md",
      "problems": []
    },
    {
      "claim_tables": 1,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/niche_os.md",
      "problems": []
    },
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/stage_3_equilibrium.md",
      "problems": []
    },
    {
      "claim_tables": 0,
      "claims_checked": 0,
      "path": "memory/app-discovery/templates/validation_gate.md",
      "problems": []
    }
  ],
  "files_checked": 7,
  "ok": true,
  "problems": []
}
```

## Sample Niche OS guard raw output

Command:
```bash
python3 scripts/app_discovery_evidence_guard.py memory/app-discovery/samples/sample_niche_os.md
```
Exit code: `0`

Output:
```text
{
  "claim_tables": 1,
  "claims_checked": 2,
  "files": [
    {
      "claim_tables": 1,
      "claims_checked": 2,
      "path": "memory/app-discovery/samples/sample_niche_os.md",
      "problems": []
    }
  ],
  "files_checked": 1,
  "ok": true,
  "problems": []
}
```

## Stage 3/4 rg check

Command:
```bash
rg -n "frontier-class reasoning|distribution feasibility gate|DEPRIORITIZE|low-competition channel" skills/app-discovery-loop/SKILL.md memory/app-discovery/templates
```
Exit code: `0`

Output:
```text
skills/app-discovery-loop/SKILL.md:65:Run this stage on frontier-class reasoning. This is the one discovery stage where model quality pays for itself because the task is structural skepticism, not artifact formatting.
skills/app-discovery-loop/SKILL.md:92:- distribution feasibility gate: if the niche has no searchable or reachable low-competition channel, deprioritize regardless of how clean the gap looks
skills/app-discovery-loop/SKILL.md:96:If the distribution feasibility gate fails, mark `DEPRIORITIZE` and stop before validation.
memory/app-discovery/templates/stage_3_equilibrium.md:3:Reasoning class: frontier-class reasoning required.
memory/app-discovery/templates/concept_brief.md:14:- distribution feasibility gate:
memory/app-discovery/templates/concept_brief.md:18:Reachable/searchable low-competition channel:
memory/app-discovery/templates/concept_brief.md:22:Decision: `CONTINUE` or `DEPRIORITIZE`
memory/app-discovery/templates/concept_brief.md:24:If the niche has no searchable or reachable low-competition channel, mark `DEPRIORITIZE` regardless of how clean the gap looks.
memory/app-discovery/templates/concept_brief.md:27:Decision: `CONTINUE`, `KILL_OR_SHRINK`, or `DEPRIORITIZE`
```

## App-discovery file list

Command:
```bash
find memory/app-discovery -type f | sort
```
Exit code: `0`

Output:
```text
memory/app-discovery/fixtures/failing_missing_snippet.md
memory/app-discovery/fixtures/passing_sourced_or_unverified.md
memory/app-discovery/samples/sample_niche_os.md
memory/app-discovery/templates/build_ready_spec.md
memory/app-discovery/templates/candidate_niches.md
memory/app-discovery/templates/concept_brief.md
memory/app-discovery/templates/landscape_audit.md
memory/app-discovery/templates/niche_os.md
memory/app-discovery/templates/stage_3_equilibrium.md
memory/app-discovery/templates/validation_gate.md
```

## No item 4 live-file diff check

Command:
```bash
git diff --name-only -- skills/product-build-loop/SKILL.md || true
```
Exit code: `0`

Output:
```text
(no output)
```

## Stage 3/4 skill diff against /dev/null because skill remains untracked from item 1

Command:
```bash
git diff --no-index -- /dev/null skills/app-discovery-loop/SKILL.md || true
```
Exit code: `0`

Output:
```diff
diff --git a/skills/app-discovery-loop/SKILL.md b/skills/app-discovery-loop/SKILL.md
new file mode 100644
index 0000000..acbb29b
--- /dev/null
+++ b/skills/app-discovery-loop/SKILL.md
@@ -0,0 +1,158 @@
+---
+name: app-discovery-loop
+description: "Use when evaluating a niche, app idea, passive-income product concept, or product opportunity before build work starts."
+---
+
+# App Discovery Loop
+
+Use this before building a new app, ranking product, dashboard, passive-income product, or major app wedge. The goal is not autonomous ideation volume. The goal is one evidence-backed opportunity, strict kill gates, and a build-ready contract only after validation.
+
+## Hard Rules
+- One niche at a time. One active folder at `memory/app-discovery/[slug]/`.
+- No cron creation or modification from this skill.
+- No passive-income doc rewiring unless JT separately approves it.
+- No code before Stage 5 validation passes and a build-ready spec exists.
+- If a claim cannot be sourced, mark it `UNVERIFIED` instead of smoothing it into confident prose.
+- "Same app, cleaner UI" is not enough. Kill or shrink unless there is a real owned edge.
+
+## Stage 0 - Source Selection
+Create `candidate_niches.md`.
+
+Rank sources in this order:
+1. Founder-market fit: niches JT understands, can reach, or can credibly talk to.
+2. Distribution-adjacent: niches with obvious X, LinkedIn, Reddit, TikTok, SEO, marketplace, or community access.
+3. Demand signal: reviews, forum complaints, search terms, job postings, paid tools, templates, spreadsheets, agencies, or repeated workarounds.
+4. Chart-chasing: trend lists, generic startup ideas, broad AI hype. Use only as weak input.
+
+Each candidate needs `source_quality`, `evidence_paths_or_urls`, `why_now`, `distribution_surface`, and `kill_reason_if_any`.
+
+## Stage 1 - Niche OS
+Create `niche_os.md`.
+
+Required sections:
+- user archetypes
+- repeated pains
+- existing workarounds
+- emotional language / voice of customer
+- willingness-to-pay evidence
+- frequency / retention hypothesis
+- trust signals and anti-needs
+- distribution surfaces
+- needs claims table
+
+Evidence rule: every needs claim must include `claim`, `source_url_or_path`, `source_snippet`, and `confidence`, or be marked `UNVERIFIED` with a reason. Run `scripts/app_discovery_evidence_guard.py` when it exists. Until then, manually inspect the claims table and label any unsupported claim `UNVERIFIED`.
+
+## Stage 2 - App Landscape Audit
+Create `landscape_audit.md`.
+
+Inspect app stores, web apps, Chrome extensions, templates, Reddit mentions, Product Hunt, GitHub when relevant, and SEO results. Score competitors by:
+- target user
+- core promise
+- pricing
+- feature coverage
+- review complaints
+- freshness
+- acquisition channel
+- retention hooks
+- trust / compliance posture
+- visible gaps
+
+Output a gap matrix: `users want X`, `existing options do Y poorly`, `evidence is Z`, `risk is R`.
+
+## Stage 3 - Equilibrium Interrogation
+Create `stage_3_equilibrium.md`. This is a gate, not a brainstorming section.
+
+Run this stage on frontier-class reasoning. This is the one discovery stage where model quality pays for itself because the task is structural skepticism, not artifact formatting.
+
+Answer:
+- Why does this gap still exist?
+- What current equilibrium keeps users on bad tools or manual workarounds?
+- What would incumbents do if this worked?
+- What distribution barrier blocks new entrants?
+- What trust, switching-cost, or willingness-to-pay barrier could kill this?
+- What wedge lets JT enter and hold ground?
+- Which owned edge powers it: game-theoretic moat-check, SEO-first distribution, ensemble methodology, data pipelines/client adjacency, or another explicit JT edge?
+
+Verdict must be exactly `KILL`, `PAUSE`, or `CONTINUE`. `CONTINUE` requires a credible wedge and at least one owned edge.
+
+## Stage 4 - Product Concept And Unique Mechanism
+Create `concept_brief.md`.
+
+Required fields:
+- target user
+- painful moment
+- current workaround
+- wedge feature
+- unique mechanism
+- edge_that_powers_it
+- share artifact
+- retention loop
+- monetization hypothesis
+- first distribution channel
+- distribution feasibility gate: if the niche has no searchable or reachable low-competition channel, deprioritize regardless of how clean the gap looks
+- why this is not just cleaner UI
+
+If the unique mechanism is weak, shrink the product until the mechanism is real or mark `KILL_OR_SHRINK`.
+If the distribution feasibility gate fails, mark `DEPRIORITIZE` and stop before validation.
+
+## Stage 5 - Validation Gate
+Create `validation_gate.md` before any build task.
+
+Use the smallest proof step that can kill or sharpen the idea:
+- fake-door page
+- waitlist
+- concierge MVP
+- direct probe interviews/messages
+- Reddit/X/LinkedIn positioning test
+- SEO demand test
+- manual spreadsheet/template test
+
+Required fields:
+- validation method
+- audience reached
+- proof artifact path or URL
+- activation signal
+- objections
+- result
+- threshold
+- decision: `KILL`, `PAUSE`, `ITERATE`, or `BUILD`
+
+`BUILD` requires evidence stronger than "I like this idea." If validation is skipped, mark the build decision `UNVERIFIED` and stop.
+
+## Stage 6 - Build-Ready Spec And Contract Freeze
+Create `build_ready_spec.md` only after Stage 5 returns `BUILD`.
+
+Required sections:
+- frozen problem statement
+- frozen target user
+- MVP scope
+- non-goals
+- frozen data contract: entities, fields, event names, API shape, import/export formats, and analytics events
+- frontend states and screens
+- backend responsibilities
+- validation evidence link
+- risks and kill thresholds
+- launch and retention measurement plan
+
+The frozen data contract is the handoff boundary. This contract freeze happens before frontend implementation or build routing. Claude Design may explore visuals from the spec, but it must not invent product behavior. Frontend implementation is blocked until the data contract is frozen.
+
+## Bounded `/goal` Templates
+Use one bounded goal per phase. Do not run one giant forever loop.
+
+Stage 1:
+`/goal Create a sourced Niche OS for [niche]. Done when memory/app-discovery/[slug]/niche_os.md has sourced or UNVERIFIED needs claims and an evidence-guard result.`
+
+Stage 2:
+`/goal Create an app landscape audit for [niche]. Done when memory/app-discovery/[slug]/landscape_audit.md has competitor scoring and a sourced gap matrix.`
+
+Stage 3:
+`/goal Run equilibrium interrogation for [niche/app concept]. Done when stage_3_equilibrium.md has KILL, PAUSE, or CONTINUE with explicit structural reasons.`
+
+Stage 5:
+`/goal Design and evaluate the smallest validation gate for [concept]. Done when validation_gate.md has evidence, objections, threshold result, and KILL/PAUSE/ITERATE/BUILD.`
+
+Stage 6:
+`/goal Produce build-ready spec for [validated concept]. Done when build_ready_spec.md freezes scope, data contract, validation link, launch metrics, and kill thresholds.`
+
+## Completion Artifact
+Return paths for every artifact created, commands run, and any `UNVERIFIED` claims. If a stage is blocked, stop at the gate and report the missing evidence.
```

## Evidence guard script diff

Command:
```bash
git diff --no-index -- /dev/null scripts/app_discovery_evidence_guard.py || true
```
Exit code: `0`

Output:
```diff
diff --git a/scripts/app_discovery_evidence_guard.py b/scripts/app_discovery_evidence_guard.py
new file mode 100755
index 0000000..4d7ae5e
--- /dev/null
+++ b/scripts/app_discovery_evidence_guard.py
@@ -0,0 +1,156 @@
+#!/usr/bin/env python3
+"""Validate app-discovery evidence claims in Markdown artifacts."""
+
+from __future__ import annotations
+
+import argparse
+import json
+import re
+import sys
+from pathlib import Path
+
+
+REQUIRED_HEADERS = {"claim", "source_url_or_path", "source_snippet", "confidence"}
+PLACEHOLDERS = {"", "todo", "tbd", "[todo]", "[source]", "[snippet]", "placeholder"}
+
+
+def normalize_cell(value: str) -> str:
+    value = value.strip()
+    if value.startswith("**") and value.endswith("**") and len(value) > 4:
+        value = value[2:-2].strip()
+    return value.replace("`", "").strip()
+
+
+def split_row(line: str) -> list[str]:
+    return [normalize_cell(cell) for cell in line.strip().strip("|").split("|")]
+
+
+def is_separator(cells: list[str]) -> bool:
+    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)
+
+
+def parse_claim_tables(text: str) -> list[dict[str, object]]:
+    lines = text.splitlines()
+    tables: list[dict[str, object]] = []
+    i = 0
+    while i < len(lines) - 1:
+        line = lines[i].strip()
+        next_line = lines[i + 1].strip()
+        if not (line.startswith("|") and next_line.startswith("|")):
+            i += 1
+            continue
+
+        headers = [header.lower() for header in split_row(line)]
+        separator = split_row(next_line)
+        if not REQUIRED_HEADERS.issubset(set(headers)) or not is_separator(separator):
+            i += 1
+            continue
+
+        rows: list[dict[str, str]] = []
+        i += 2
+        while i < len(lines) and lines[i].strip().startswith("|"):
+            cells = split_row(lines[i])
+            if len(cells) < len(headers):
+                cells.extend([""] * (len(headers) - len(cells)))
+            rows.append(dict(zip(headers, cells)))
+            i += 1
+        tables.append({"headers": headers, "rows": rows})
+    return tables
+
+
+def is_blank_or_placeholder(value: str) -> bool:
+    return normalize_cell(value).strip().lower() in PLACEHOLDERS
+
+
+def row_is_unverified(row: dict[str, str]) -> bool:
+    fields = [
+        row.get("status", ""),
+        row.get("confidence", ""),
+        row.get("source_url_or_path", ""),
+    ]
+    return any(normalize_cell(field).upper() == "UNVERIFIED" for field in fields)
+
+
+def row_is_blank(row: dict[str, str]) -> bool:
+    return all(is_blank_or_placeholder(value) for value in row.values())
+
+
+def check_row(path: Path, row: dict[str, str], row_number: int) -> list[str]:
+    problems: list[str] = []
+    prefix = f"{path}: claim row {row_number}"
+
+    if is_blank_or_placeholder(row.get("claim", "")):
+        problems.append(f"{prefix}: missing claim")
+
+    if row_is_unverified(row):
+        reason = row.get("unverified_reason", "") or row.get("reason", "")
+        if is_blank_or_placeholder(reason):
+            problems.append(f"{prefix}: UNVERIFIED claim missing unverified_reason")
+        return problems
+
+    for field in ("source_url_or_path", "source_snippet", "confidence"):
+        if is_blank_or_placeholder(row.get(field, "")):
+            problems.append(f"{prefix}: missing {field}")
+    return problems
+
+
+def check_file(path: Path) -> dict[str, object]:
+    text = path.read_text(encoding="utf-8")
+    tables = parse_claim_tables(text)
+    problems: list[str] = []
+    claims_checked = 0
+
+    for table in tables:
+        rows = table["rows"]
+        for index, row in enumerate(rows, start=1):
+            if row_is_blank(row):
+                continue
+            claims_checked += 1
+            problems.extend(check_row(path, row, index))
+
+    return {
+        "path": str(path),
+        "claim_tables": len(tables),
+        "claims_checked": claims_checked,
+        "problems": problems,
+    }
+
+
+def check_files(paths: list[Path]) -> dict[str, object]:
+    file_results = [check_file(path) for path in paths]
+    problems = [problem for result in file_results for problem in result["problems"]]
+    return {
+        "ok": not problems,
+        "files_checked": len(file_results),
+        "claim_tables": sum(int(result["claim_tables"]) for result in file_results),
+        "claims_checked": sum(int(result["claims_checked"]) for result in file_results),
+        "problems": problems,
+        "files": file_results,
+    }
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser()
+    parser.add_argument("paths", nargs="+", help="Markdown artifacts to validate")
+    args = parser.parse_args()
+
+    paths = [Path(path) for path in args.paths]
+    missing = [str(path) for path in paths if not path.exists()]
+    if missing:
+        result = {
+            "ok": False,
+            "files_checked": 0,
+            "claim_tables": 0,
+            "claims_checked": 0,
+            "problems": [f"missing file: {path}" for path in missing],
+            "files": [],
+        }
+    else:
+        result = check_files(paths)
+
+    print(json.dumps(result, indent=2, sort_keys=True))
+    return 0 if result["ok"] else 1
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
```

## Evidence guard test diff

Command:
```bash
git diff --no-index -- /dev/null scripts/test_app_discovery_evidence_guard.py || true
```
Exit code: `0`

Output:
```diff
diff --git a/scripts/test_app_discovery_evidence_guard.py b/scripts/test_app_discovery_evidence_guard.py
new file mode 100644
index 0000000..6adbf36
--- /dev/null
+++ b/scripts/test_app_discovery_evidence_guard.py
@@ -0,0 +1,54 @@
+import tempfile
+import unittest
+from pathlib import Path
+
+import app_discovery_evidence_guard as guard
+
+
+FAILING = """# Failing Niche OS
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence |
+|---|---|---|---|
+| Users need a faster way to compare skincare routines. | https://example.com/review |  | high |
+"""
+
+
+PASSING = """# Passing Niche OS
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence | unverified_reason |
+|---|---|---|---|---|
+| Users compare products by ingredient conflict. | https://example.com/review | "I need to know what clashes before buying." | high |  |
+| Users might share scorecards if they look credible. | UNVERIFIED |  | UNVERIFIED | No direct source yet; must validate in Stage 4 distribution gate. |
+"""
+
+
+class AppDiscoveryEvidenceGuardTests(unittest.TestCase):
+    def test_missing_source_snippet_fails(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            path = Path(tmp) / "niche_os.md"
+            path.write_text(FAILING)
+
+            result = guard.check_files([path])
+
+            self.assertFalse(result["ok"])
+            self.assertEqual(result["claims_checked"], 1)
+            self.assertTrue(any("missing source_snippet" in p for p in result["problems"]))
+
+    def test_all_claims_sourced_or_unverified_passes(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            path = Path(tmp) / "niche_os.md"
+            path.write_text(PASSING)
+
+            result = guard.check_files([path])
+
+            self.assertTrue(result["ok"])
+            self.assertEqual(result["claims_checked"], 2)
+            self.assertEqual(result["problems"], [])
+
+
+if __name__ == "__main__":
+    unittest.main()
```

## Template diffs

Command:
```bash
find memory/app-discovery/templates -type f -name '*.md' -print0 | sort -z | xargs -0 -I{} sh -c 'git diff --no-index -- /dev/null "$1" || true' sh {}
```
Exit code: `0`

Output:
```diff
diff --git a/memory/app-discovery/templates/build_ready_spec.md b/memory/app-discovery/templates/build_ready_spec.md
new file mode 100644
index 0000000..d97517b
--- /dev/null
+++ b/memory/app-discovery/templates/build_ready_spec.md
@@ -0,0 +1,27 @@
+# Build-Ready Spec And Contract Freeze
+
+## Frozen Problem Statement
+
+## Frozen Target User
+
+## MVP Scope
+
+## Non-Goals
+
+## Frozen Data Contract
+- entities:
+- fields:
+- event names:
+- API shape:
+- import/export formats:
+- analytics events:
+
+## Frontend States And Screens
+
+## Backend Responsibilities
+
+## Validation Evidence Link
+
+## Risks And Kill Thresholds
+
+## Launch And Retention Measurement Plan
diff --git a/memory/app-discovery/templates/candidate_niches.md b/memory/app-discovery/templates/candidate_niches.md
new file mode 100644
index 0000000..4010dc4
--- /dev/null
+++ b/memory/app-discovery/templates/candidate_niches.md
@@ -0,0 +1,18 @@
+# Candidate Niches
+
+## Candidate Table
+
+| niche | source_quality | evidence_paths_or_urls | why_now | distribution_surface | kill_reason_if_any |
+|---|---|---|---|---|---|
+|  |  |  |  |  |  |
+
+## Ranking Notes
+- Founder-market fit:
+- Distribution adjacency:
+- Demand signal:
+- Chart-chasing caveat:
+
+## Decision
+Verdict: `KILL`, `PAUSE`, or `CONTINUE`
+
+Reason:
diff --git a/memory/app-discovery/templates/concept_brief.md b/memory/app-discovery/templates/concept_brief.md
new file mode 100644
index 0000000..e5ce4f5
--- /dev/null
+++ b/memory/app-discovery/templates/concept_brief.md
@@ -0,0 +1,27 @@
+# Concept Brief
+
+## Required Fields
+- target user:
+- painful moment:
+- current workaround:
+- wedge feature:
+- unique mechanism:
+- edge_that_powers_it:
+- share artifact:
+- retention loop:
+- monetization hypothesis:
+- first distribution channel:
+- distribution feasibility gate:
+- why this is not just cleaner UI:
+
+## Distribution Feasibility Gate
+Reachable/searchable low-competition channel:
+
+Evidence:
+
+Decision: `CONTINUE` or `DEPRIORITIZE`
+
+If the niche has no searchable or reachable low-competition channel, mark `DEPRIORITIZE` regardless of how clean the gap looks.
+
+## Mechanism Decision
+Decision: `CONTINUE`, `KILL_OR_SHRINK`, or `DEPRIORITIZE`
diff --git a/memory/app-discovery/templates/landscape_audit.md b/memory/app-discovery/templates/landscape_audit.md
new file mode 100644
index 0000000..0838d00
--- /dev/null
+++ b/memory/app-discovery/templates/landscape_audit.md
@@ -0,0 +1,15 @@
+# App Landscape Audit
+
+## Competitor Scoring
+
+| competitor | target_user | core_promise | pricing | feature_coverage | review_complaints | freshness | acquisition_channel | retention_hooks | trust_posture | visible_gaps |
+|---|---|---|---|---|---|---|---|---|---|---|
+|  |  |  |  |  |  |  |  |  |  |  |
+
+## Gap Matrix
+
+| users_want_x | existing_options_do_y_poorly | evidence_is_z | risk_is_r |
+|---|---|---|---|
+|  |  |  |  |
+
+## Notes
diff --git a/memory/app-discovery/templates/niche_os.md b/memory/app-discovery/templates/niche_os.md
new file mode 100644
index 0000000..e80ebc2
--- /dev/null
+++ b/memory/app-discovery/templates/niche_os.md
@@ -0,0 +1,25 @@
+# Niche OS
+
+## User Archetypes
+
+## Repeated Pains
+
+## Existing Workarounds
+
+## Emotional Language / Voice Of Customer
+
+## Willingness-To-Pay Evidence
+
+## Frequency / Retention Hypothesis
+
+## Trust Signals And Anti-Needs
+
+## Distribution Surfaces
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence | unverified_reason |
+|---|---|---|---|---|
+|  |  |  |  |  |
+
+Every row must either include `claim`, `source_url_or_path`, `source_snippet`, and `confidence`, or set `confidence` to `UNVERIFIED` with `unverified_reason`.
diff --git a/memory/app-discovery/templates/stage_3_equilibrium.md b/memory/app-discovery/templates/stage_3_equilibrium.md
new file mode 100644
index 0000000..148c130
--- /dev/null
+++ b/memory/app-discovery/templates/stage_3_equilibrium.md
@@ -0,0 +1,19 @@
+# Stage 3 Equilibrium Interrogation
+
+Reasoning class: frontier-class reasoning required.
+
+## Questions
+- Why does this gap still exist?
+- What current equilibrium keeps users on bad tools or manual workarounds?
+- What would incumbents do if this worked?
+- What distribution barrier blocks new entrants?
+- What trust, switching-cost, or willingness-to-pay barrier could kill this?
+- What wedge lets JT enter and hold ground?
+- Which owned edge powers it?
+
+## Verdict
+Verdict: `KILL`, `PAUSE`, or `CONTINUE`
+
+Structural reason:
+
+Owned edge:
diff --git a/memory/app-discovery/templates/validation_gate.md b/memory/app-discovery/templates/validation_gate.md
new file mode 100644
index 0000000..f28db8d
--- /dev/null
+++ b/memory/app-discovery/templates/validation_gate.md
@@ -0,0 +1,15 @@
+# Validation Gate
+
+## Method
+- validation method:
+- audience reached:
+- proof artifact path or URL:
+- activation signal:
+- objections:
+- result:
+- threshold:
+- decision: `KILL`, `PAUSE`, `ITERATE`, or `BUILD`
+
+## Evidence Notes
+
+## Decision Rationale
```

## Fixture/sample diffs

Command:
```bash
find memory/app-discovery/fixtures memory/app-discovery/samples -type f -name '*.md' -print0 | sort -z | xargs -0 -I{} sh -c 'git diff --no-index -- /dev/null "$1" || true' sh {}
```
Exit code: `0`

Output:
```diff
diff --git a/memory/app-discovery/fixtures/failing_missing_snippet.md b/memory/app-discovery/fixtures/failing_missing_snippet.md
new file mode 100644
index 0000000..3ba4de1
--- /dev/null
+++ b/memory/app-discovery/fixtures/failing_missing_snippet.md
@@ -0,0 +1,7 @@
+# Failing Evidence Guard Fixture
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence |
+|---|---|---|---|
+| Users need a faster way to compare skincare routines. | https://example.com/review |  | high |
diff --git a/memory/app-discovery/fixtures/passing_sourced_or_unverified.md b/memory/app-discovery/fixtures/passing_sourced_or_unverified.md
new file mode 100644
index 0000000..d8d6b1c
--- /dev/null
+++ b/memory/app-discovery/fixtures/passing_sourced_or_unverified.md
@@ -0,0 +1,8 @@
+# Passing Evidence Guard Fixture
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence | unverified_reason |
+|---|---|---|---|---|
+| Users compare products by ingredient conflict before buying. | https://example.com/review | "I need to know what clashes before buying." | high |  |
+| Users might share scorecards if the output looks credible. | UNVERIFIED |  | UNVERIFIED | No direct source yet; must validate in Stage 4 distribution gate. |
diff --git a/memory/app-discovery/samples/sample_niche_os.md b/memory/app-discovery/samples/sample_niche_os.md
new file mode 100644
index 0000000..fdd9fe1
--- /dev/null
+++ b/memory/app-discovery/samples/sample_niche_os.md
@@ -0,0 +1,34 @@
+# Sample Niche OS
+
+## User Archetypes
+- Ingredient-checker buyer
+- Routine optimizer
+
+## Repeated Pains
+- Product comparisons are fragmented across reviews, ingredient databases, and creator posts.
+
+## Existing Workarounds
+- Manual spreadsheet, Reddit searches, screenshots, and creator recommendations.
+
+## Emotional Language / Voice Of Customer
+- "I need to know what clashes before buying."
+
+## Willingness-To-Pay Evidence
+- UNVERIFIED: no paid-intent artifact in this sample.
+
+## Frequency / Retention Hypothesis
+- Weekly during active shopping cycles; lower outside purchase windows.
+
+## Trust Signals And Anti-Needs
+- Needs transparent ingredient logic and source links.
+- Anti-need: black-box "AI says this is good" recommendations.
+
+## Distribution Surfaces
+- Search terms, Reddit threads, TikTok skincare creators, and comparison pages.
+
+## Needs Claims Table
+
+| claim | source_url_or_path | source_snippet | confidence | unverified_reason |
+|---|---|---|---|---|
+| Buyers want conflict checks before buying products. | memory/app-discovery/samples/sample_niche_os.md | "I need to know what clashes before buying." | medium |  |
+| Scorecard sharing may create organic distribution. | UNVERIFIED |  | UNVERIFIED | Needs Stage 4 distribution feasibility proof. |
```
