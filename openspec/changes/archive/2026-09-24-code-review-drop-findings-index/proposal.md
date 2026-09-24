## Why

After #217, `/code-review` uses numbered findings for humans but still appends a **Findings index** Markdown table for
`/review-fixer`. On github.com that table stays unreadable (too-narrow columns). The numbered list already carries
`Path:`; the table is redundant UI debt (#246, seen-in-the-wild).

## What Changes

- **BREAKING** (report shape): Drop the Findings index table from the skill/docs template. Published bodies keep the
  marker + verdict + numbered findings only.
- Teach `extract_code_review_findings` / `review-open` to parse numbered `- **Path:** \`…\`` (and related fields); keep
  parsing legacy tables so older PR reviews still triage.
- Update OpenSpec contracts for `code-review` and `agent-ai-gh` (supersedes dual-layout “must include compact table”).
- Close out / align any in-flight `code-review-readable-findings` change that still requires the dual table.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `code-review`: Published findings MUST be numbered blocks only (no Findings index table).
- `agent-ai-gh`: Extract `/code-review` summary findings from numbered Path lines; MAY still accept legacy path tables.

## Impact

- `.agents/skills/code-review/SKILL.md`, `.cursor/commands/code-review.md`, `docs/code-review.md`
- `scripts/ai` extractors + tests; `review-fixer` skill text if it mentions the table
- OpenSpec deltas → archive into main specs
