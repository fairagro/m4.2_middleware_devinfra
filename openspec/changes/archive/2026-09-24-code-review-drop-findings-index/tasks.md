## 1. Specs / cleanup

- [x] 1.1 Confirm delta specs for `code-review` and `agent-ai-gh` match lock-in A; remove or abandon conflicting
      `openspec/changes/code-review-readable-findings/` dual-table artifacts if still present (verify folder gone or
      clearly superseded)

## 2. Extractor + tests

- [x] 2.1 Update `extract_code_review_findings` to parse numbered **Path** bullets (legacy table fallback); verify unit
      tests cover numbered-only, dual (prefer numbered or document), and legacy table-only
- [x] 2.2 Run focused `uv run --project scripts/ai pytest` on affected review tests and verify they pass

## 3. Skill / docs

- [x] 3.1 Update `.agents/skills/code-review/SKILL.md` and `.cursor/commands/code-review.md` to drop Findings index;
      verify example body has no table
- [x] 3.2 Update `docs/code-review.md` and any `review-fixer` mentions of the Findings index table; verify docs say
      numbered Path extraction

## 4. Verify

- [x] 4.1 Run Prettier on `openspec/changes/code-review-drop-findings-index/**` and
      `openspec validate     code-review-drop-findings-index --strict`; verify both pass
